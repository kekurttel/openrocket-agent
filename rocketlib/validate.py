"""Tasarım doğrulama.

Kurallar (model roket için):

============================  ==========  ==========================================
Kontrol                       Seviye      Koşul
============================  ==========  ==========================================
stabilite marjı (kalkışta)    hata        < 0.5 kalibre
stabilite marjı (kalkışta)    uyarı       < 1.0 kalibre
stabilite marjı (kalkışta)    uyarı       > 2.5 kalibre
stabilite marjı (güçlü uçuş)  uyarı       < 1.0 kalibre
rampa çıkış hızı              uyarı       < 15 m/s
kurtarma sistemi yok          hata        paraşüt/streamer bulunamadı
motor yok                     hata        uçuş konfigürasyonunda motor atanmadı
motor sığmıyor                hata        çap veya boy uyuşmuyor
bileşen adı tekrarı           uyarı       aynı ad birden fazla bileşende
simülasyon yok/başarısız      hata        simülasyon yok ya da çalışmadı
============================  ==========  ==========================================

Her uyarı ``{"severity": "error"|"warning", "code": "...", "message": "..."}``
biçimindedir. Birimler SI'dır (m, m/s, kg, kalibre).

Örnek::

    for issue in rocketlib.validate(doc):
        print(issue["severity"], issue["code"], issue["message"])
"""

from __future__ import annotations

from typing import Any

from ._common import ensure_simulation
from .errors import ValidationError
from .session import get_session

__all__ = [
    "validate",
    "MIN_STABILITY_CAL",
    "MAX_STABILITY_CAL",
    "CRITICAL_STABILITY_CAL",
    "MIN_RAIL_EXIT_SPEED_MPS",
]

CRITICAL_STABILITY_CAL = 0.5
MIN_STABILITY_CAL = 1.0
MAX_STABILITY_CAL = 2.5
MIN_RAIL_EXIT_SPEED_MPS = 15.0


def _issue(severity: str, code: str, message: str) -> dict[str, str]:
    return {"severity": severity, "code": code, "message": message}


def _safe(fn, default=None):
    try:
        return fn()
    except Exception:
        return default


def validate(
    doc: Any,
    *,
    simulation_index: int = 0,
    seed: int | None = None,
    run_simulation: bool = True,
) -> list[dict[str, str]]:
    """Tasarımı doğrular ve uyarı/hata listesini döndürür.

    :param doc: OpenRocket belgesi.
    :param simulation_index: doğrulanacak simülasyon indeksi.
    :param seed: simülasyon için sabit tohum (None → OpenRocket varsayılanı).
    :param run_simulation: simülasyon çalıştırılsın mı (kontrol için gerekli).
    :return: ``[{"severity", "code", "message"}, ...]`` listesi.
    :raises ValidationError: doğrulama yapılamıyorsa.
    """
    session = get_session()
    issues: list[dict[str, str]] = []
    rocket = doc.getRocket()

    from orlab import JIterator

    comps = list(JIterator(rocket))

    # ---------- bileşen adı tekrarı ----------
    names: dict[str, int] = {}
    for comp in comps:
        n = str(comp.getName())
        names[n] = names.get(n, 0) + 1
    for n, count in sorted(names.items()):
        if count > 1:
            issues.append(
                _issue("warning", "duplicate-name",
                       f"'{n}' adı {count} bileşende kullanılıyor; adlar benzersiz olmalı.")
            )

    # ---------- kurtarma sistemi ----------
    recovery = [c for c in comps
                if str(c.getClass().getSimpleName()) in ("Parachute", "Streamer")]
    if not recovery:
        issues.append(
            _issue("error", "no-recovery",
                   "Kurtarma sistemi yok (paraşüt/streamer bulunamadı) — uçuş güvenli değil.")
        )

    # ---------- motor ----------
    motor_info = _motor_report(session, doc, comps, simulation_index, issues)

    # ---------- simülasyon ----------
    if int(doc.getSimulationCount()) == 0:
        issues.append(
            _issue("error", "no-simulation",
                   "Belgede simülasyon yok; stabilite ve iniş hızı doğrulanamaz.")
        )
        return issues

    sim = doc.getSimulation(simulation_index)
    metrics: dict[str, Any] = {}
    if run_simulation:
        from .run import run

        try:
            metrics = run(doc, seed=seed, simulation_index=simulation_index)
        except Exception as e:
            issues.append(
                _issue("error", "simulation-failed",
                       f"Simülasyon çalıştırılamadı: {e}")
            )
            return issues

        stab = metrics.get("stability_at_launch_cal")
        if stab is None:
            issues.append(
                _issue("warning", "stability-unknown",
                       "Kalkış anı stabilite marjı hesaplanamadı (rampa çıkışı yok?).")
            )
        elif stab < CRITICAL_STABILITY_CAL:
            issues.append(
                _issue("error", "stability-critical",
                       f"Stabilite marjı {stab:.2f} kal — kritik (< {CRITICAL_STABILITY_CAL} kal), "
                       "roket kararsız.")
            )
        elif stab < MIN_STABILITY_CAL:
            issues.append(
                _issue("warning", "stability-low",
                       f"Stabilite marjı {stab:.2f} kal düşük (< {MIN_STABILITY_CAL} kal).")
            )
        elif stab > MAX_STABILITY_CAL:
            issues.append(
                _issue("warning", "stability-high",
                       f"Stabilite marjı {stab:.2f} kal yüksek (> {MAX_STABILITY_CAL} kal); "
                       "hava direnci nedeniyle performans düşebilir.")
            )

        stab_min = metrics.get("stability_min_powered_cal")
        if stab_min is None:
            stab_min = metrics.get("stability_min_cal")
        if stab_min is not None and stab_min < MIN_STABILITY_CAL:
            issues.append(
                _issue("warning", "stability-min-low",
                       f"Güçlü uçuş boyunca en düşük stabilite marjı {stab_min:.2f} kal "
                       f"(< {MIN_STABILITY_CAL} kal).")
            )

        rail = metrics.get("rail_exit_velocity_mps")
        if rail is None:
            issues.append(
                _issue("warning", "rail-velocity-unknown",
                       "Rampa çıkış hızı ölçülemedi (LAUNCHROD olayı yok).")
            )
        elif rail < MIN_RAIL_EXIT_SPEED_MPS:
            issues.append(
                _issue("warning", "rail-velocity-low",
                       f"Rampa çıkış hızı {rail:.2f} m/s düşük "
                       f"(< {MIN_RAIL_EXIT_SPEED_MPS} m/s).")
            )

    _ = motor_info
    _ = sim
    return issues


def _motor_report(session, doc, comps, simulation_index, issues) -> list[dict[str, Any]]:
    """Motor varlığını ve gövdeye sığma durumunu kontrol eder.

    :return: motor raporu ( sözlük listesi ).
    """
    from ._common import ensure_simulation

    report: list[dict[str, Any]] = []
    try:
        sim = ensure_simulation(doc, simulation_index)
    except Exception:
        sim = None

    motor_mount_cls = session.core.rocketcomponent.MotorMount
    fcid = str(sim.getFlightConfigurationId()) if sim is not None else None

    found_any = False
    for comp in comps:
        try:
            is_mount = isinstance(comp, motor_mount_cls) and comp.isMotorMount()
        except Exception:
            is_mount = False
        if not is_mount:
            continue
        config = None
        if sim is not None and fcid is not None:
            config = _safe(lambda: comp.getMotorConfig(
                sim.getFlightConfigurationId()))
        motor = _safe(lambda: config.getMotor()) if config is not None else None
        if motor is None:
            continue
        found_any = True
        designation = str(_safe(lambda: motor.getDesignation(), "?"))
        diameter = _safe(motor.getDiameter)
        length = _safe(motor.getLength)
        entry = {
            "mount": str(comp.getName()),
            "designation": designation,
            "diameter_m": diameter,
            "length_m": length,
        }
        report.append(entry)

        # sığma kontrolü
        cls = str(comp.getClass().getSimpleName())
        if cls == "BodyTube":
            avail = _safe(comp.getInnerRadius)
        elif cls == "InnerTube":
            outer = _safe(comp.getOuterRadius)
            thick = _safe(comp.getThickness, 0.0) or 0.0
            avail = outer - thick
        else:
            avail = None
        if avail is not None and diameter is not None:
            if diameter > 2 * avail + 1e-9:
                issues.append(
                    _issue("error", "motor-too-fat",
                           f"Motor {designation} çapı {diameter * 1000:.1f} mm, "
                           f"'{comp.getName()}' yuvasının iç çapı "
                           f"{2 * avail * 1000:.1f} mm'den büyük — sığmıyor.")
                )
        mount_len = _safe(comp.getLength)
        if mount_len is not None and length is not None and length > mount_len + 1e-9:
            issues.append(
                _issue("error", "motor-too-long",
                       f"Motor {designation} boyu {length * 1000:.1f} mm, "
                       f"'{comp.getName()}' yuvası {mount_len * 1000:.1f} mm — sığmıyor.")
            )

    if not found_any:
        issues.append(
            _issue("error", "no-motor",
                   "Uçuş konfigürasyonunda motor atanmamış — simülasyon motorla yapılmadı.")
        )
    return report
