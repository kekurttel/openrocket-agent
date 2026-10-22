"""Simülasyon çalıştırma ve uçuş metrikleri.

Tüm değerler **SI**'dır ve JSON'a dönüştürülebilir. Ölçülemez/uygulanamaz
değerler ``None`` olur (OpenRocket NaN üretir); nedeni ``notes`` sözlüğünde
belirtilir.

Örnek::

    m = rocketlib.run(doc, seed=1)
    print(m["apogee_m"], m["max_velocity_mps"])
"""

from __future__ import annotations

import math
from typing import Any

from ._common import ensure_simulation
from .errors import SimulationError
from .session import get_session

__all__ = ["run", "METRIC_UNITS"]

METRIC_UNITS = {
    "apogee_m": "m",
    "time_to_apogee_s": "s",
    "max_velocity_mps": "m/s",
    "max_acceleration_mps2": "m/s²",
    "max_mach": "-",
    "rail_exit_velocity_mps": "m/s",
    "stability_at_launch_cal": "cal",
    "stability_min_cal": "cal",
    "stability_max_cal": "cal",
    "stability_at_burnout_cal": "cal",
    "launch_mass_kg": "kg",
    "cg_at_launch_m": "m",
    "cp_at_launch_m": "m",
    "cg_at_burnout_m": "m",
    "cp_at_burnout_m": "m",
    "deployment_velocity_mps": "m/s",
    "descent_rate_mps": "m/s",
    "landing_velocity_mps": "m/s",
    "landing_distance_m": "m",
    "landing_x_m": "m",
    "landing_y_m": "m",
    "flight_time_s": "s",
    "optimum_delay_s": "s",
}


def _clean(value: Any) -> float | None:
    """NaN/inf → None; diğer sayılar → float."""
    if value is None:
        return None
    try:
        v = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(v) or math.isinf(v):
        return None
    return v


def _as_array(series: Any):
    """Seriyi 1-boyutlu float numpy dizisine çevirir (0-dim diziler de dâhil)."""
    import numpy as np

    if series is None:
        return np.array([])
    try:
        return np.atleast_1d(np.asarray(series, dtype=float))
    except (TypeError, ValueError):
        return np.array([])


def _size(series: Any) -> int:
    """Serinin eleman sayısı (numpy dizisi, liste veya 0-dim dizi için)."""
    if series is None:
        return 0
    try:
        import numpy as np

        if isinstance(series, np.ndarray):
            return int(series.size)
    except Exception:  # pragma: no cover
        pass
    try:
        return len(series)
    except TypeError:
        return 0


def _value_at(times, values, t: float) -> float | None:
    """t anındaki ilk geçerli örneği döndürür (NaN atlanır)."""
    import numpy as np

    times_a = _as_array(times)
    values_a = _as_array(values)
    if times_a.size == 0 or values_a.size == 0:
        return None
    idx = int(np.searchsorted(times_a, t, side="left"))
    for i in range(idx, values_a.size):
        if not math.isnan(float(values_a[i])):
            return float(values_a[i])
    return None


def run(
    doc: Any,
    *,
    seed: int | None = None,
    simulation_index: int = 0,
    branch: int = 0,
) -> dict[str, Any]:
    """Simülasyonu çalıştırır ve uçuş metriklerini döndürür.

    :param doc: OpenRocket belgesi.
    :param seed: sabit rastgelelik tohumu. ``None`` → her çalıştırmada yeni
        tohum (OpenRocket'ın varsayılanı). Bir sayı verildiğinde sonuç
        **aynı süreç içinde** tekrarlanabilirdir.
    :param simulation_index: çalıştırılacak simülasyonun indeksi.
    :param branch: özetlenecek kademe kolu (0 = ana kademe).
    :return: metrik sözlüğü (SI birimler, JSON uyumlu).
    :raises SimulationError: simülasyon çalıştırılamazsa.

    Örnek::

        m = rocketlib.run(doc, seed=1)
        print(m["apogee_m"], "m")
    """
    session = get_session()
    sim = ensure_simulation(doc, simulation_index)
    opts = sim.getOptions()

    if seed is not None:
        try:
            opts.setRandomSeed(int(seed))
        except Exception as e:
            raise SimulationError(f"Seed ayarlanamadı: {e}") from e
        randomize = False
    else:
        randomize = True

    try:
        session.helper.run_simulation(sim, randomize_seed=randomize)
    except Exception as e:
        raise SimulationError(f"Simülasyon çalıştırılamadı: {e}") from e

    try:
        summary = session.helper.get_summary(sim, branch_number=branch)
    except Exception as e:
        raise SimulationError(f"Simülasyon sonuçları okunamadı: {e}") from e

    metrics: dict[str, Any] = {
        "apogee_m": _clean(summary.apogee),
        "time_to_apogee_s": _clean(summary.time_to_apogee),
        "max_velocity_mps": _clean(summary.max_velocity),
        "max_acceleration_mps2": _clean(summary.max_acceleration),
        "max_mach": _clean(summary.max_mach),
        "rail_exit_velocity_mps": _clean(summary.velocity_off_rod),
        "stability_at_launch_cal": _clean(summary.stability_off_rod_cal),
        "stability_min_cal": _clean(summary.min_stability_cal),
        "stability_max_cal": _clean(summary.max_stability_cal),
        "deployment_velocity_mps": _clean(summary.velocity_at_deployment),
        "descent_rate_mps": _clean(summary.descent_rate),
        "landing_velocity_mps": _clean(summary.ground_hit_velocity),
        "landing_x_m": _clean(summary.landing_x),
        "landing_y_m": _clean(summary.landing_y),
        "landing_distance_m": _clean(summary.landing_distance),
        "flight_time_s": _clean(summary.flight_time),
        "optimum_delay_s": _clean(summary.optimum_delay),
    }
    notes: dict[str, str] = {}

    # ---------- olaylar ve zaman serileri ----------
    events: dict[str, list[float]] = {}
    try:
        ev = session.helper.get_events(sim, branch_number=branch)
        for key, times in ev.items():
            events[str(key).replace("FlightEvent.", "")] = [float(t) for t in times]
        metrics["events"] = events
    except Exception as e:  # pragma: no cover
        notes["events"] = f"olaylar okunamadı: {e}"

    series_keys = [
        "TYPE_TIME", "TYPE_ALTITUDE", "TYPE_VELOCITY_TOTAL", "TYPE_STABILITY",
        "TYPE_CG_LOCATION", "TYPE_CP_LOCATION", "TYPE_MASS",
    ]
    ts: dict[str, Any] = {}
    try:
        raw = session.helper.get_timeseries(sim, series_keys, branch_number=branch)
        ts = {k: raw[k] for k in raw}
    except Exception as e:
        notes["timeseries"] = f"zaman serisi okunamadı: {e}"

    def event_time(name: str) -> float | None:
        times = events.get(name)
        return float(times[0]) if times else None

    launch_t = event_time("LAUNCH") or 0.0
    burnout_t = event_time("BURNOUT")
    rod_t = event_time("LAUNCHROD")

    if "TYPE_MASS" in ts and _size(ts["TYPE_MASS"]):
        metrics["launch_mass_kg"] = _clean(_as_array(ts["TYPE_MASS"])[0])
    else:
        notes["launch_mass_kg"] = "TYPE_MASS serisi yok"

    if "TYPE_CG_LOCATION" in ts and _size(ts["TYPE_CG_LOCATION"]):
        metrics["cg_at_launch_m"] = _clean(_as_array(ts["TYPE_CG_LOCATION"])[0])
    if "TYPE_CP_LOCATION" in ts and _size(ts["TYPE_CP_LOCATION"]):
        cp_launch = _clean(_as_array(ts["TYPE_CP_LOCATION"])[0])
        metrics["cp_at_launch_m"] = cp_launch
        if cp_launch is None:
            notes["cp_at_launch_m"] = (
                "kalkış anında CP tanımsız (OpenRocket CP'yi hava akışı "
                "başladıktan sonra hesaplar; NaN)"
            )
    if burnout_t is not None:
        if "TYPE_CG_LOCATION" in ts:
            metrics["cg_at_burnout_m"] = _clean(
                _value_at(ts.get("TYPE_TIME", []), ts["TYPE_CG_LOCATION"], burnout_t)
            )
        if "TYPE_CP_LOCATION" in ts:
            metrics["cp_at_burnout_m"] = _clean(
                _value_at(ts.get("TYPE_TIME", []), ts["TYPE_CP_LOCATION"], burnout_t)
            )
        if "TYPE_STABILITY" in ts:
            stab = _value_at(ts.get("TYPE_TIME", []), ts["TYPE_STABILITY"], burnout_t)
            metrics["stability_at_burnout_cal"] = stab
            if stab is None:
                notes["stability_at_burnout_cal"] = "motor sönümü anında stabilite yok"
    else:
        notes["stability_at_burnout_cal"] = "simülasyonda BURNOUT olayı yok"

    # Güçlü uçuş penceresi (kalkış → motor sönümü) içindeki en düşük stabilite.
    # orlab'ın `stability_min_cal` penceresi rampa çıkışı→apogee arasıdır ve
    # rampada/ilk saniyelerdeki geçiş transiyentini de içerir; güçlü uçuş
    # penceresi kararlılık değerlendirmesi için daha anlamlıdır.
    if "TYPE_STABILITY" in ts and "TYPE_TIME" in ts:
        import numpy as np

        times = _as_array(ts["TYPE_TIME"])
        stabilities = _as_array(ts["TYPE_STABILITY"])
        start = event_time("LIFTOFF")
        if start is None:
            start = launch_t
        end = burnout_t if burnout_t is not None else event_time("APOGEE")
        if start is not None and end is not None and times.size:
            mask = (times >= start) & (times <= end)
            values = stabilities[mask]
            finite = values[~np.isnan(values)]
            if finite.size:
                metrics["stability_min_powered_cal"] = float(finite.min())

    if rod_t is not None and metrics.get("stability_at_launch_cal") is None:
        if "TYPE_STABILITY" in ts:
            metrics["stability_at_launch_cal"] = _clean(
                _value_at(ts.get("TYPE_TIME", []), ts["TYPE_STABILITY"], rod_t)
            )

    metrics["simulation_status"] = str(sim.getStatus())
    metrics["simulation_name"] = str(sim.getName())
    metrics["flight_configuration_id"] = str(sim.getFlightConfigurationId())
    metrics["seed"] = int(opts.getRandomSeed()) if seed is not None else None
    metrics["warnings"] = list(summary.warnings)
    metrics["notes"] = notes
    metrics["units"] = dict(METRIC_UNITS)
    return metrics
