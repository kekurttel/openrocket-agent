"""Ek OpenRocket bileşenleri: halka, bulkhead, kaplin, ray butonu, kademe ayrılması.

Bu modül `rocketlib.build` içindeki yardımcıları yeniden kullanır; tüm dışa
açık fonksiyonlar **SI** birimleri kullanır (m, kg, derece).
"""

from __future__ import annotations

from typing import Any

from .build import (
    _add_child,
    _check_number,
    _check_unique_name,
    _resolve_parent,
    _set,
    _set_position,
    _unique_name,
    find_component,
)
from .errors import DesignError
from .session import get_session

__all__ = [
    "add_centering_ring",
    "add_bulkhead",
    "add_tube_coupler",
    "add_rail_button",
    "set_parachute_packed",
    "set_stage_separation",
]


def _place(comp: Any, position: str | None, offset: float) -> None:
    """Eksenel konumu ayarlar: relative yöntem + ofset (m)."""
    _set_position(comp, position or "top")
    if offset:
        _set(comp, "setAxialOffset", float(offset), label="eksenel ofset")


def add_centering_ring(
    doc: Any,
    name: str | None = None,
    *,
    length: float = 0.006,
    outer_radius: float = 0.048,
    inner_radius: float = 0.0395,
    position: str = "absolute",
    offset: float = 0.0,
    parent: Any | str | None = None,
) -> Any:
    """Merkezleme/hizalama halkası ekler (alüminyum).

    :param length: halka boyu (m).
    :param outer_radius: dış yarıçap (m).
    :param inner_radius: iç yarıçap (m).
    :param position: "absolute" → offset roket burnundan (m).
    :param parent: üst bileşen (None → son gövde tüpü).
    """
    session = get_session()
    length = _check_number("length", length, minimum=0.0, unit="m")
    outer_radius = _check_number("outer_radius", outer_radius, minimum=0.0, unit="m")
    inner_radius = _check_number("inner_radius", inner_radius, minimum=0.0, unit="m")
    if inner_radius >= outer_radius:
        raise DesignError("iç yarıçap dış yarıçaptan küçük olmalı")
    rocket = doc.getRocket()
    if name is None:
        name = _unique_name(rocket, "Centering ring")
    else:
        _check_unique_name(rocket, name)
    comp = session.component_class("CenteringRing")()
    comp.setName(name)
    _set(comp, "setLength", length, label="halka boyu")
    _set(comp, "setOuterRadiusAutomatic", False, label="halka dış yarıçapı")
    _set(comp, "setInnerRadiusAutomatic", False, label="halka iç yarıçapı")
    _set(comp, "setOuterRadius", outer_radius, label="halka dış yarıçapı")
    _set(comp, "setInnerRadius", inner_radius, label="halka iç yarıçapı")
    _place(comp, position, offset)
    return _add_child(_resolve_parent(doc, parent, body_level=False), comp)


def add_bulkhead(
    doc: Any,
    name: str | None = None,
    *,
    length: float = 0.004,
    radius: float = 0.0475,
    position: str = "absolute",
    offset: float = 0.0,
    parent: Any | str | None = None,
) -> Any:
    """Bölme (bulkhead) ekler; dış yarıçap gövdeye otomatik oturur.

    :param length: kalınlık (m).
    :param radius: dış yarıçap (m) — gövde iç yarıçapına eşit seçilir.
    """
    session = get_session()
    length = _check_number("length", length, minimum=0.0, unit="m")
    radius = _check_number("radius", radius, minimum=0.0, unit="m")
    rocket = doc.getRocket()
    if name is None:
        name = _unique_name(rocket, "Bulkhead")
    else:
        _check_unique_name(rocket, name)
    comp = session.component_class("Bulkhead")()
    comp.setName(name)
    _set(comp, "setLength", length, label="bulkhead kalınlığı")
    _set(comp, "setOuterRadiusAutomatic", False, label="bulkhead yarıçapı")
    _set(comp, "setOuterRadius", radius, label="bulkhead yarıçapı")
    _place(comp, position, offset)
    return _add_child(_resolve_parent(doc, parent, body_level=False), comp)


def add_tube_coupler(
    doc: Any,
    name: str | None = None,
    *,
    length: float = 0.15,
    outer_radius: float = 0.047,
    thickness: float = 0.003,
    position: str = "absolute",
    offset: float = 0.0,
    parent: Any | str | None = None,
) -> Any:
    """Entegrasyon gövdesi (kaplin/tube coupler) ekler.

    Şartname 4.5.12: iki gövdeye de dış çapın en az %75'i kadar girmelidir.
    """
    session = get_session()
    length = _check_number("length", length, minimum=0.0, unit="m")
    outer_radius = _check_number("outer_radius", outer_radius, minimum=0.0, unit="m")
    thickness = _check_number("thickness", thickness, minimum=0.0, unit="m")
    rocket = doc.getRocket()
    if name is None:
        name = _unique_name(rocket, "Tube coupler")
    else:
        _check_unique_name(rocket, name)
    comp = session.component_class("TubeCoupler")()
    comp.setName(name)
    _set(comp, "setLength", length, label="kaplin boyu")
    _set(comp, "setOuterRadius", outer_radius, label="kaplin dış yarıçapı")
    _set(comp, "setInnerRadius", max(outer_radius - thickness, 1e-4),
         label="kaplin iç yarıçapı")
    _place(comp, position, offset)
    return _add_child(_resolve_parent(doc, parent, body_level=False), comp)


def set_parachute_packed(
    doc: Any,
    name: str,
    *,
    length: float,
    diameter: float,
) -> Any:
    """Paraşütün paketlenmiş (katlanmış) boyutlarını ayarlar.

    OpenRocket, paraşüt kütlesini kanopi alanından hesaplar; paket boyutları
    yalnızca ağırlık merkezini ve gövde içi hacim kontrolünü etkiler.

    :param name: paraşüt bileşeninin adı.
    :param length: paket uzunluğu (m).
    :param diameter: paket çapı (m); gövde iç çapından küçük olmalı.
    """
    length = _check_number("length", length, minimum=0.0, unit="m")
    diameter = _check_number("diameter", diameter, minimum=0.0, unit="m")
    comp = find_component(doc, name)
    if str(comp.getClass().getSimpleName()) != "Parachute":
        raise DesignError(f"'{name}' bir paraşüt değil.")
    _set(comp, "setLength", length, label="paraşüt paket uzunluğu")
    _set(comp, "setRadius", diameter / 2.0, label="paraşüt paket yarıçapı")
    return comp


def add_rail_button(
    doc: Any,
    name: str | None = None,
    *,
    outer_diameter: float = 0.015,
    height: float = 0.0128,
    position: str = "absolute",
    offset: float = 0.0,
    parent: Any | str | None = None,
) -> Any:
    """Fırlatma ray butonu ekler (alüminyum, 2 adet zorunlu)."""
    session = get_session()
    outer_diameter = _check_number("outer_diameter", outer_diameter,
                                   minimum=0.0, unit="m")
    height = _check_number("height", height, minimum=0.0, unit="m")
    rocket = doc.getRocket()
    if name is None:
        name = _unique_name(rocket, "Rail button")
    else:
        _check_unique_name(rocket, name)
    comp = session.component_class("RailButton")()
    comp.setName(name)
    _set(comp, "setOuterDiameter", outer_diameter, label="ray butonu çapı")
    _set(comp, "setTotalHeight", height, label="ray butonu yüksekliği")
    _place(comp, position, offset)
    return _add_child(_resolve_parent(doc, parent, body_level=False), comp)


_SEPARATION_EVENTS = {
    "launch": "LAUNCH",
    "ignition": "IGNITION",
    "burnout": "BURNOUT",
    "ejection": "EJECTION",
    "upper_ignition": "UPPER_IGNITION",
    "altitude_ascending": "ALTITUDE_ASCENDING",
    "apogee": "APOGEE",
    "altitude_descending": "ALTITUDE_DESCENDING",
    "never": "NEVER",
}


def set_stage_separation(
    doc: Any,
    stage: int | str = 1,
    *,
    event: str = "altitude_descending",
    altitude: float = 500.0,
    delay: float = 0.0,
) -> Any:
    """Bir kademenin ayrılma olayını ayarlar.

    ``event="altitude_descending"`` + ``altitude=500`` → kademe yere 500 m
    kalınca (alçalırken) ayrılır; OpenRocket'ın ``ALTITUDE_DESCENDING`` olayı.
    """
    rocket = doc.getRocket()
    if isinstance(stage, str):
        target = None
        for i in range(rocket.getStageCount()):
            if str(rocket.getStage(i).getName()) == stage:
                target = rocket.getStage(i)
                break
        if target is None:
            raise DesignError(f"Kademe bulunamadı: {stage!r}")
    else:
        idx = int(stage)
        if idx < 0 or idx >= rocket.getStageCount():
            raise DesignError(f"Kademe indeksi geçersiz: {idx}")
        target = rocket.getStage(idx)
    key = str(event).strip().lower()
    if key not in _SEPARATION_EVENTS:
        raise DesignError(
            f"Bilinmeyen ayrılma olayı: {event!r}. Geçerli: "
            f"{', '.join(sorted(_SEPARATION_EVENTS))}"
        )
    altitude = _check_number("altitude", altitude, minimum=0.0, unit="m")
    delay = _check_number("delay", delay, minimum=0.0, unit="s")
    session = get_session()
    enum_cls = session.core.rocketcomponent.StageSeparationConfiguration.SeparationEvent
    cfg = target.getSeparationConfiguration()
    _set(cfg, "setSeparationEvent", getattr(enum_cls, _SEPARATION_EVENTS[key]),
         label="kademe ayrılma olayı")
    _set(cfg, "setSeparationAltitude", altitude, label="kademe ayrılma irtifası")
    _set(cfg, "setSeparationDelay", delay, label="kademe ayrılma gecikmesi")
    return target
