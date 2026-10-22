"""Tasarımı JSON'a çevrilebilir bir sözlüğe dökme.

Birimler: uzunluk **m**, kütle **kg**, açı **derece**.

Örnek::

    import json
    print(json.dumps(rocketlib.inspect_design(doc), indent=2, ensure_ascii=False))
"""

from __future__ import annotations

import math
from typing import Any

from .session import get_session

__all__ = ["inspect_design", "inspect_component"]


def _num(value: Any) -> float | None:
    try:
        v = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(v) or math.isinf(v):
        return None
    return v


def _safe(fn, default=None):
    try:
        return fn()
    except Exception:
        return default


def inspect_component(comp: Any) -> dict[str, Any]:
    """Tek bir bileşeni sözlüğe çevirir.

    :param comp: Java bileşen nesnesi.
    :return: bileşenin parametrelerini içeren sözlük.
    """
    cls = str(comp.getClass().getSimpleName())
    parent = _safe(lambda: comp.getParent())
    out: dict[str, Any] = {
        "name": str(comp.getName()),
        "type": cls,
        "parent": str(parent.getName()) if parent is not None else None,
        "length_m": _num(_safe(lambda: comp.getLength())),
        "mass_kg": _num(_safe(lambda: comp.getComponentMass())),
        "axial_offset_m": _num(_safe(lambda: comp.getAxialOffset())),
        "instance_count": _safe(lambda: int(comp.getInstanceCount())),
    }
    details: dict[str, Any] = {}

    if cls == "NoseCone":
        out["radius_m"] = _num(_safe(lambda: comp.getBaseRadius()))
        details["shape"] = str(_safe(lambda: comp.getShapeType().name(), ""))
        details["shape_parameter"] = _num(_safe(lambda: comp.getShapeParameter()))
        details["thickness_m"] = _num(_safe(lambda: comp.getThickness()))
    elif cls == "BodyTube":
        out["radius_m"] = _num(_safe(lambda: comp.getOuterRadius()))
        details["inner_radius_m"] = _num(_safe(lambda: comp.getInnerRadius()))
    elif cls == "Transition":
        out["fore_radius_m"] = _num(_safe(lambda: comp.getForeRadius()))
        out["aft_radius_m"] = _num(_safe(lambda: comp.getAftRadius()))
        details["shape"] = str(_safe(lambda: comp.getShapeType().name(), ""))
        details["shape_parameter"] = _num(_safe(lambda: comp.getShapeParameter()))
    elif cls in ("TrapezoidFinSet", "EllipticalFinSet"):
        out["fin_count"] = _safe(lambda: int(comp.getFinCount()))
        out["height_m"] = _num(_safe(lambda: comp.getHeight()))
        details["thickness_m"] = _num(_safe(lambda: comp.getThickness()))
        if cls == "TrapezoidFinSet":
            out["root_chord_m"] = _num(_safe(lambda: comp.getRootChord()))
            out["tip_chord_m"] = _num(_safe(lambda: comp.getTipChord()))
            details["sweep_deg"] = (
                math.degrees(_safe(lambda: comp.getSweepAngle(), 0.0) or 0.0)
            )
        details["cant_angle_deg"] = math.degrees(_safe(lambda: comp.getCantAngle(), 0.0) or 0.0)
    elif cls == "InnerTube":
        out["radius_m"] = _num(_safe(lambda: comp.getOuterRadius()))
        details["inner_radius_m"] = _num(_safe(lambda: comp.getInnerRadius()))
    elif cls == "MassComponent":
        out["radius_m"] = _num(_safe(lambda: comp.getRadius()))
        details["component_mass_kg"] = _num(_safe(lambda: comp.getComponentMass()))
    elif cls == "Parachute":
        out["diameter_m"] = _num(_safe(lambda: comp.getDiameter()))
        details["line_count"] = _safe(lambda: int(comp.getLineCount()))
        details["line_length_m"] = _num(_safe(lambda: comp.getLineLength()))
        details["cd"] = _num(_safe(lambda: comp.getCD()))
    elif cls == "ShockCord":
        details["cord_length_m"] = _num(_safe(lambda: comp.getCordLength()))
    elif cls == "Streamer":
        details["strip_length_m"] = _num(_safe(lambda: comp.getStripLength()))
        details["strip_width_m"] = _num(_safe(lambda: comp.getStripWidth()))
    elif cls == "LaunchLug":
        out["radius_m"] = _num(_safe(lambda: comp.getRadius()))
        details["angle_deg"] = math.degrees(_safe(lambda: comp.getAngle(), 0.0) or 0.0)
    elif cls == "EngineBlock":
        out["radius_m"] = _num(_safe(lambda: comp.getOuterRadius()))

    if details:
        out["details"] = details
    return out


def inspect_design(doc: Any) -> dict[str, Any]:
    """Tasarımın tamamını JSON'a çevrilebilir bir sözlük olarak döndürür.

    :param doc: OpenRocket belgesi.
    :return: ``{"rocket": {...}, "components": [...], "simulations": [...]}``
    """
    session = get_session()
    from orlab import JIterator

    rocket = doc.getRocket()
    comps = list(JIterator(rocket))

    rocket_info = {
        "name": str(rocket.getName()),
        "designer": str(_safe(lambda: rocket.getDesigner(), "") or ""),
        "length_m": _num(_safe(rocket.getLength)),
        "mass_kg": _num(_safe(rocket.getMass)),
        "stage_count": _safe(lambda: int(rocket.getStageCount())),
    }

    simulations = []
    for i in range(int(doc.getSimulationCount())):
        sim = doc.getSimulation(i)
        opts = sim.getOptions()
        import math as _math

        simulations.append(
            {
                "index": i,
                "name": str(sim.getName()),
                "status": str(sim.getStatus()),
                "flight_configuration_id": str(sim.getFlightConfigurationId()),
                "motor": _safe(lambda: session.helper.get_motor(sim)),
                "launch": {
                    "rod_length_m": _num(opts.getLaunchRodLength()),
                    "rod_angle_deg": _math.degrees(opts.getLaunchRodAngle()),
                    "wind_speed_mps": _num(opts.getWindSpeedAverage()),
                    "wind_turbulence": _num(opts.getWindTurbulenceIntensity()),
                    "launch_altitude_m": _num(opts.getLaunchAltitude()),
                    "temperature_K": _num(opts.getLaunchTemperature()),
                    "pressure_Pa": _num(opts.getLaunchPressure()),
                    "isa_atmosphere": bool(opts.isISAAtmosphere()),
                    "random_seed": int(opts.getRandomSeed()),
                },
            }
        )

    return {
        "rocket": rocket_info,
        "components": [inspect_component(c) for c in comps],
        "simulations": simulations,
    }
