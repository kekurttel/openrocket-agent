"""Bileşen ekleme / güncelleme / silme.

Tüm dışa açık fonksiyonlarda **SI birimleri** kullanılır:
uzunluk **metre**, kütle **kg**, açı **derece**, yarıçap/çap **metre**.
(OpenRocket'ın Java API'si açıları radyan bekler; dönüşüm burada yapılır.)

Örnekler::

    doc = rocketlib.new_design("Test")
    rocketlib.add_nose_cone(doc, length=0.10, radius=0.019)
    rocketlib.add_body_tube(doc, length=0.30, radius=0.019)
    rocketlib.add_fin_set(doc, count=3, root_chord=0.05, tip_chord=0.02,
                          height=0.03, sweep=45.0)
    rocketlib.add_parachute(doc, diameter=0.30)
"""

from __future__ import annotations

import math
from typing import Any, Iterable

from .errors import ComponentNotFoundError, DesignError, DuplicateComponentError
from .session import get_session

__all__ = [
    "add_nose_cone",
    "add_body_tube",
    "add_transition",
    "add_fin_set",
    "add_inner_tube",
    "add_mass_component",
    "add_parachute",
    "add_shock_cord",
    "update_component",
    "remove_component",
    "find_component",
    "list_components",
    "set_component_material",
    "set_parachute_deployment",
    "set_nose_shoulder",
    "set_surface_finish",
    "set_component_position",
    "add_stage",
    "move_component",
]

# Bileşen adları (otomatik ad üretimi için temel adlar)
_BASENAMES = {
    "NoseCone": "Nose cone",
    "BodyTube": "Body tube",
    "Transition": "Transition",
    "TrapezoidFinSet": "Trapezoidal fin set",
    "EllipticalFinSet": "Elliptical fin set",
    "InnerTube": "Inner Tube",
    "MassComponent": "Mass component",
    "Parachute": "Parachute",
    "ShockCord": "Shock cord",
    "Streamer": "Streamer",
}


# --------------------------------------------------------------------------
# yardımcılar
# --------------------------------------------------------------------------
def _check_number(name: str, value: Any, *, minimum: float | None = None,
                  maximum: float | None = None, unit: str = "") -> float:
    """Sayısal girdiyi doğrular (NaN/inf yok, gerekiyorsa sınır kontrolü).

    :raises DesignError: geçersiz değer.
    """
    try:
        v = float(value)
    except (TypeError, ValueError) as e:
        raise DesignError(f"{name} sayısal olmalı, verilen: {value!r}") from e
    if math.isnan(v) or math.isinf(v):
        raise DesignError(f"{name} NaN/inf olamaz ({unit})")
    if minimum is not None and v < minimum:
        raise DesignError(f"{name} en az {minimum} {unit} olmalı, verilen: {v} {unit}")
    if maximum is not None and v > maximum:
        raise DesignError(f"{name} en çok {maximum} {unit} olmalı, verilen: {v} {unit}")
    return v


def _components(rocket: Any) -> list[Any]:
    """Roketin tüm bileşenlerini (kök dahil) listeler."""
    from orlab import JIterator

    return list(JIterator(rocket))


def list_components(doc: Any) -> list[Any]:
    """Belgedeki tüm bileşenleri Java nesneleri olarak döndürür.

    :param doc: OpenRocket belgesi.
    :return: bileşen listesi.
    """
    return _components(doc.getRocket())


def find_component(doc: Any, name: str) -> Any:
    """Ada göre bileşen bulur.

    :param doc: OpenRocket belgesi.
    :param name: bileşen adı (büyük/küçük harf duyarlı).
    :raises ComponentNotFoundError: bulunamazsa.
    """
    for comp in _components(doc.getRocket()):
        if str(comp.getName()) == name:
            return comp
    raise ComponentNotFoundError(f"Bileşen bulunamadı: {name!r}")


def _unique_name(rocket: Any, base: str) -> str:
    """Benzersiz bir bileşen adı üretir ("Body tube", "Body tube 2", ...)."""
    existing = {str(c.getName()) for c in _components(rocket)}
    if base not in existing:
        return base
    i = 2
    while f"{base} {i}" in existing:
        i += 1
    return f"{base} {i}"


def _check_unique_name(rocket: Any, name: str) -> None:
    existing = {str(c.getName()) for c in _components(rocket)}
    if name in existing:
        raise DuplicateComponentError(
            f"Bu ad zaten kullanılıyor: {name!r}. Bileşen adları benzersiz olmalı."
        )


def _stage(doc: Any) -> Any:
    """Roketin ilk (sustainer) kademesini döndürür."""
    rocket = doc.getRocket()
    try:
        stage = rocket.getStage(0)
    except Exception as e:
        raise DesignError(f"Kademe alınamadı: {e}") from e
    if stage is None:
        raise DesignError("Bu tasarımda kademe yok.")
    return stage


def _last_body_tube(doc: Any) -> Any:
    """Tasarımdaki son BodyTube bileşenini döndürür."""
    tubes = [c for c in _components(doc.getRocket())
             if str(c.getClass().getSimpleName()) == "BodyTube"]
    if not tubes:
        raise DesignError(
            "Bu tasarımda gövde tüpü (BodyTube) yok; önce add_body_tube() çağır."
        )
    return tubes[-1]


def _resolve_parent(doc: Any, parent: Any | str | None, *, body_level: bool) -> Any:
    """Bileşenin ekleneceği üst bileşeni belirler.

    :param doc: OpenRocket belgesi.
    :param parent: üst bileşen nesnesi ya da adı (None → varsayılan).
    :param body_level: True → gövde bileşenleri (stage'in çocukları),
        False → iç/kanatçık bileşenleri (BodyTube'nun çocukları).
    :return: üst bileşen.
    :raises DesignError: üst bileşen bulunamazsa.
    """
    if parent is None:
        return _stage(doc) if body_level else _last_body_tube(doc)
    if isinstance(parent, str):
        return find_component(doc, parent)
    return parent


_BODY_COMPONENT_CLASSES = ("NoseCone", "BodyTube", "Transition")


def _body_insert_index(parent: Any, comp: Any) -> int:
    """Gövde bileşeninin ekleneceği sıra.

    OpenRocket'ta gövde bileşenleri kademenin çocuk listesinde **önden arkaya**
    sıralanır (burun konisi → gövde tüpü → geçiş). Burun konisi daima en önde,
    diğer gövde bileşenleri mevcut gövde bileşenlerinin hemen ardında durur.

    :param parent: üst bileşen.
    :param comp: eklenecek bileşen.
    :return: ekleme indeksi.
    """
    children = list(parent.getChildren())
    cls = str(comp.getClass().getSimpleName())
    if cls == "NoseCone":
        idx = 0
        while idx < len(children) and str(
            children[idx].getClass().getSimpleName()
        ) == "NoseCone":
            idx += 1
        return idx
    idx = 0
    while idx < len(children) and str(
        children[idx].getClass().getSimpleName()
    ) in _BODY_COMPONENT_CLASSES:
        idx += 1
    return idx


def _add_child(parent: Any, comp: Any, index: int | None = None) -> Any:
    """Bileşeni üst bileşene ekler (JPype belirsizlik için 3 argümanlı overload).

    :param parent: üst bileşen.
    :param comp: eklenecek bileşen.
    :param index: ekleme indeksi; None → gövde/ iç bileşen sıralamasına göre.
    :return: eklenen bileşen.
    :raises DesignError: eklenemezse.
    """
    if index is None:
        index = _body_insert_index(parent, comp)
    try:
        parent.addChild(comp, int(index), True)
    except Exception as e:
        raise DesignError(
            f"{comp.getClass().getSimpleName()} bileşeni {parent.getName()!r} altına "
            f"eklenemedi: {e}"
        ) from e
    return comp


def _set(comp: Any, setter: str, value: Any, *, label: str) -> None:
    """Setter çağırır, hataları anlaşılır hale getirir."""
    try:
        getattr(comp, setter)(value)
    except Exception as e:
        raise DesignError(f"{label} ayarlanamadı ({setter}): {e}") from e


def _set_position(comp: Any, position: str | None) -> None:
    """Bileşenin eksenel konumunu ayarlar.

    :param comp: bileşen.
    :param position: "top" | "bottom" | "middle" | "after" | "absolute"
        (None → bileşenin varsayılanı bırakılır).
    :raises DesignError: bilinmeyen konum.
    """
    if position is None:
        return
    session = get_session()
    key = str(position).strip().lower()
    mapping = {
        "top": "TOP",
        "bottom": "BOTTOM",
        "middle": "MIDDLE",
        "center": "MIDDLE",
        "after": "AFTER",
        "absolute": "ABSOLUTE",
    }
    if key not in mapping:
        raise DesignError(
            f"Bilinmeyen konum: {position!r} "
            f"(seçenekler: {', '.join(sorted(mapping))})"
        )
    axial_cls = session.core.rocketcomponent.position.AxialMethod
    for constant in axial_cls.class_.getEnumConstants():
        if str(constant.name()) == mapping[key]:
            _set(comp, "setAxialMethod", constant, label="bileşen konumu")
            return
    raise DesignError(f"Konum enum'u bulunamadı: {mapping[key]}")


# --------------------------------------------------------------------------
# bileşen ekleyiciler
# --------------------------------------------------------------------------
def add_nose_cone(
    doc: Any,
    name: str | None = None,
    *,
    length: float = 0.10,
    radius: float = 0.019,
    shape: str = "ogive",
    shape_parameter: float = 0.5,
    thickness: float = 0.002,
    parent: Any | str | None = None,
) -> Any:
    """Burun konisi ekler.

    :param doc: OpenRocket belgesi.
    :param name: bileşen adı (None → benzersiz otomatik ad).
    :param length: koni boyu (m).
    :param radius: taban yarıçapı (m).
    :param shape: koni şekli ("ogive", "conical", "elliptical", "parabolic",
        "powerseries", "haack" …).
    :param shape_parameter: şekle özgü parametre (ogive için 0…1).
    :param thickness: duvar kalınlığı (m).
    :param parent: üst bileşen (None → ilk kademe).
    :return: eklenen bileşen.
    :raises DesignError: geçersiz girdi.
    """
    session = get_session()
    length = _check_number("length", length, minimum=0.0, unit="m")
    radius = _check_number("radius", radius, minimum=0.0, unit="m")
    thickness = _check_number("thickness", thickness, minimum=0.0, unit="m")
    shape_parameter = _check_number("shape_parameter", shape_parameter, unit="")

    rocket = doc.getRocket()
    if name is None:
        name = _unique_name(rocket, _BASENAMES["NoseCone"])
    else:
        _check_unique_name(rocket, name)

    comp = session.component_class("NoseCone")()
    comp.setName(name)
    _set(comp, "setLength", length, label="burun konisi boyu")
    _set(comp, "setShapeType", session.transition_shape(shape), label="burun konisi şekli")
    _set(comp, "setShapeParameter", shape_parameter, label="burun konisi şekil parametresi")
    _set(comp, "setBaseRadius", radius, label="burun konisi yarıçapı")
    _set(comp, "setThickness", thickness, label="burun konisi kalınlığı")
    return _add_child(_resolve_parent(doc, parent, body_level=True), comp)


def add_body_tube(
    doc: Any,
    name: str | None = None,
    *,
    length: float = 0.30,
    radius: float = 0.019,
    thickness: float | None = None,
    motor_mount: bool = False,
    parent: Any | str | None = None,
) -> Any:
    """Gövde tüpü ekler.

    :param doc: OpenRocket belgesi.
    :param name: bileşen adı (None → benzersiz otomatik ad).
    :param length: tüp boyu (m).
    :param radius: dış yarıçap (m).
    :param thickness: duvar kalınlığı (m); None → OpenRocket'un otomatik değeri.
    :param motor_mount: tüp aktif motor yuvası olsun mu (varsayılan: hayır).
    :param parent: üst bileşen (None → ilk kademe).
    :return: eklenen bileşen.
    :raises DesignError: geçersiz girdi.
    """
    session = get_session()
    length = _check_number("length", length, minimum=0.0, unit="m")
    radius = _check_number("radius", radius, minimum=0.0, unit="m")

    rocket = doc.getRocket()
    if name is None:
        name = _unique_name(rocket, _BASENAMES["BodyTube"])
    else:
        _check_unique_name(rocket, name)

    comp = session.component_class("BodyTube")()
    comp.setName(name)
    _set(comp, "setLength", length, label="gövde boyu")
    _set(comp, "setOuterRadius", radius, label="gövde yarıçapı")
    if thickness is not None:
        thickness = _check_number("thickness", thickness, minimum=0.0, unit="m")
        _set(comp, "setInnerRadius", max(radius - thickness, 1e-4),
             label="gövde iç yarıçapı")
    _set(comp, "setMotorMount", bool(motor_mount), label="motor yuvası")
    return _add_child(_resolve_parent(doc, parent, body_level=True), comp)


def add_transition(
    doc: Any,
    name: str | None = None,
    *,
    length: float = 0.05,
    fore_radius: float | None = None,
    aft_radius: float | None = None,
    shape: str = "conical",
    shape_parameter: float = 0.5,
    parent: Any | str | None = None,
) -> Any:
    """Geçiş (transition) ekler.

    :param doc: OpenRocket belgesi.
    :param name: bileşen adı (None → benzersiz otomatik ad).
    :param length: geçiş boyu (m).
    :param fore_radius: ön yarıçap (m); None → otomatik.
    :param aft_radius: arka yarıçap (m); None → otomatik.
    :param shape: şekil ("conical", "ogive", …).
    :param shape_parameter: şekle özgü parametre.
    :param parent: üst bileşen (None → ilk kademe).
    :return: eklenen bileşen.
    :raises DesignError: geçersiz girdi.
    """
    session = get_session()
    length = _check_number("length", length, minimum=0.0, unit="m")

    rocket = doc.getRocket()
    if name is None:
        name = _unique_name(rocket, _BASENAMES["Transition"])
    else:
        _check_unique_name(rocket, name)

    comp = session.component_class("Transition")()
    comp.setName(name)
    _set(comp, "setLength", length, label="geçiş boyu")
    _set(comp, "setShapeType", session.transition_shape(shape), label="geçiş şekli")
    _set(comp, "setShapeParameter", shape_parameter, label="geçiş şekil parametresi")
    if fore_radius is not None:
        fore_radius = _check_number("fore_radius", fore_radius, minimum=0.0, unit="m")
        _set(comp, "setForeRadius", fore_radius, label="geçiş ön yarıçapı")
    if aft_radius is not None:
        aft_radius = _check_number("aft_radius", aft_radius, minimum=0.0, unit="m")
        _set(comp, "setAftRadius", aft_radius, label="geçiş arka yarıçapı")
    return _add_child(_resolve_parent(doc, parent, body_level=True), comp)


def add_fin_set(
    doc: Any,
    name: str | None = None,
    *,
    shape: str = "trapezoidal",
    count: int = 3,
    root_chord: float = 0.050,
    tip_chord: float = 0.020,
    height: float = 0.030,
    sweep: float = 45.0,
    thickness: float = 0.002,
    position: str | None = "bottom",
    parent: Any | str | None = None,
) -> Any:
    """Kanatçık seti ekler (trapezoidal veya eliptikal).

    :param doc: OpenRocket belgesi.
    :param name: bileşen adı (None → benzersiz otomatik ad).
    :param shape: "trapezoidal" veya "elliptical".
    :param count: kanatçık sayısı.
    :param root_chord: kök kordon uzunluğu (m); eliptikalde gövde uzunluğu.
    :param tip_chord: uç kordon (m); yalnız trapezoidal.
    :param height: kanatçık yüksekliği (m).
    :param sweep: süpürme açısı (**derece**); yalnız trapezoidal.
    :param thickness: kanatçık kalınlığı (m).
    :param position: eksenel konum ("top"/"bottom"/"middle"/"after"/"absolute");
        None → OpenRocket varsayılanı.
    :param parent: üst bileşen (None → son gövde tüpü).
    :return: eklenen bileşen.
    :raises DesignError: geçersiz girdi.
    """
    session = get_session()
    shape_key = str(shape).lower()
    if shape_key in ("trapezoidal", "trapezoid", "trap"):
        java_cls = "TrapezoidFinSet"
    elif shape_key in ("elliptical", "ellipse"):
        java_cls = "EllipticalFinSet"
    else:
        raise DesignError(
            f"Bilinmeyen kanatçık şekli: {shape!r} ('trapezoidal' veya 'elliptical')"
        )

    count = int(count)
    if count < 1:
        raise DesignError(f"count en az 1 olmalı, verilen: {count}")
    root_chord = _check_number("root_chord", root_chord, minimum=0.0, unit="m")
    tip_chord = _check_number("tip_chord", tip_chord, minimum=0.0, unit="m")
    height = _check_number("height", height, minimum=0.0, unit="m")
    thickness = _check_number("thickness", thickness, minimum=0.0, unit="m")
    sweep = _check_number("sweep", sweep, unit="deg")

    rocket = doc.getRocket()
    base = _BASENAMES[java_cls]
    if name is None:
        name = _unique_name(rocket, base)
    else:
        _check_unique_name(rocket, name)

    comp = session.component_class(java_cls)()
    comp.setName(name)
    _set(comp, "setFinCount", count, label="kanatçık sayısı")
    _set(comp, "setHeight", height, label="kanatçık yüksekliği")
    _set(comp, "setThickness", thickness, label="kanatçık kalınlığı")
    if java_cls == "TrapezoidFinSet":
        _set(comp, "setRootChord", root_chord, label="kök kordon")
        _set(comp, "setTipChord", tip_chord, label="uç kordon")
        # Java radyan bekliyor; yükseklik önce ayarlanmalı (süpürme = tan(r)*yükseklik)
        _set(comp, "setSweepAngle", math.radians(sweep), label="süpürme açısı")
    else:
        _set(comp, "setLength", root_chord, label="kanatçık kök uzunluğu")
    _set_position(comp, position)
    return _add_child(_resolve_parent(doc, parent, body_level=False), comp)


def add_inner_tube(
    doc: Any,
    name: str | None = None,
    *,
    length: float = 0.070,
    radius: float = 0.0125,
    thickness: float | None = None,
    motor_mount: bool = True,
    position: str | None = "bottom",
    parent: Any | str | None = None,
) -> Any:
    """Motor tüpü (iç boru) ekler.

    :param doc: OpenRocket belgesi.
    :param name: bileşen adı (None → benzersiz otomatik ad).
    :param length: tüp boyu (m).
    :param radius: dış yarıçap (m).
    :param thickness: duvar kalınlığı (m); None → OpenRocket varsayılanı.
        Motor yuvası olarak kullanılacaksa iç çap motor çapından büyük olmalıdır
        (ör. 18 mm motor → iç yarıçap ≥ 0.009 m).
    :param motor_mount: tüp aktif motor yuvası olsun mu (varsayılan: evet).
    :param position: eksenel konum (varsayılan "bottom" — arkada).
    :param parent: üst bileşen (None → son gövde tüpü).
    :return: eklenen bileşen.
    :raises DesignError: geçersiz girdi.
    """
    session = get_session()
    length = _check_number("length", length, minimum=0.0, unit="m")
    radius = _check_number("radius", radius, minimum=0.0, unit="m")

    rocket = doc.getRocket()
    if name is None:
        name = _unique_name(rocket, _BASENAMES["InnerTube"])
    else:
        _check_unique_name(rocket, name)

    comp = session.component_class("InnerTube")()
    comp.setName(name)
    _set(comp, "setLength", length, label="iç boru boyu")
    _set(comp, "setOuterRadius", radius, label="iç boru yarıçapı")
    if thickness is not None:
        thickness = _check_number("thickness", thickness, minimum=0.0, unit="m")
        _set(comp, "setInnerRadius", max(radius - thickness, 1e-4),
             label="iç boru iç yarıçapı")
    # OpenRocket'da tüp "aktif motor yuvası" olmadan motor kabul etmez
    _set(comp, "setMotorMount", bool(motor_mount), label="motor yuvası")
    _set_position(comp, position)
    return _add_child(_resolve_parent(doc, parent, body_level=False), comp)


def add_mass_component(
    doc: Any,
    name: str | None = None,
    *,
    length: float = 0.030,
    radius: float = 0.019,
    mass: float = 0.010,
    position: str | None = None,
    parent: Any | str | None = None,
) -> Any:
    """Kütle bileşeni ekler.

    :param doc: OpenRocket belgesi.
    :param name: bileşen adı (None → benzersiz otomatik ad).
    :param length: bileşen boyu (m).
    :param radius: bileşen yarıçapı (m).
    :param mass: bileşen kütlesi (kg).
    :param position: eksenel konum (None → OpenRocket varsayılanı).
    :param parent: üst bileşen (None → son gövde tüpü).
    :return: eklenen bileşen.
    :raises DesignError: geçersiz girdi.
    """
    session = get_session()
    length = _check_number("length", length, minimum=0.0, unit="m")
    radius = _check_number("radius", radius, minimum=0.0, unit="m")
    mass = _check_number("mass", mass, minimum=0.0, unit="kg")

    rocket = doc.getRocket()
    if name is None:
        name = _unique_name(rocket, _BASENAMES["MassComponent"])
    else:
        _check_unique_name(rocket, name)

    comp = session.component_class("MassComponent")()
    comp.setName(name)
    _set(comp, "setLength", length, label="kütle bileşeni boyu")
    _set(comp, "setRadius", radius, label="kütle bileşeni yarıçapı")
    _set(comp, "setComponentMass", mass, label="kütle bileşeni kütlesi")
    _set_position(comp, position)
    return _add_child(_resolve_parent(doc, parent, body_level=False), comp)


def add_parachute(
    doc: Any,
    name: str | None = None,
    *,
    diameter: float = 0.30,
    line_count: int = 6,
    line_length: float = 0.30,
    cd: float = 0.8,
    position: str | None = "bottom",
    parent: Any | str | None = None,
) -> Any:
    """Paraşüt ekler.

    :param doc: OpenRocket belgesi.
    :param name: bileşen adı (None → benzersiz otomatik ad).
    :param diameter: paraşüt çapı (m).
    :param line_count: ip sayısı.
    :param line_length: ip uzunluğu (m).
    :param cd: sürükleme katsayısı.
    :param position: eksenel konum (varsayılan "bottom" — arkada).
    :param parent: üst bileşen (None → son gövde tüpü).
    :return: eklenen bileşen.
    :raises DesignError: geçersiz girdi.
    """
    session = get_session()
    diameter = _check_number("diameter", diameter, minimum=0.0, unit="m")
    line_length = _check_number("line_length", line_length, minimum=0.0, unit="m")
    cd = _check_number("cd", cd, minimum=0.0)
    line_count = int(line_count)
    if line_count < 1:
        raise DesignError(f"line_count en az 1 olmalı, verilen: {line_count}")

    rocket = doc.getRocket()
    if name is None:
        name = _unique_name(rocket, _BASENAMES["Parachute"])
    else:
        _check_unique_name(rocket, name)

    comp = session.component_class("Parachute")()
    comp.setName(name)
    _set(comp, "setDiameter", diameter, label="paraşüt çapı")
    _set(comp, "setLineCount", line_count, label="paraşüt ip sayısı")
    _set(comp, "setLineLength", line_length, label="paraşüt ip uzunluğu")
    _set(comp, "setCD", cd, label="paraşüt CD")
    _set_position(comp, position)
    return _add_child(_resolve_parent(doc, parent, body_level=False), comp)


def add_shock_cord(
    doc: Any,
    name: str | None = None,
    *,
    length: float = 0.30,
    position: str | None = "bottom",
    parent: Any | str | None = None,
) -> Any:
    """Şok kordonu ekler.

    :param doc: OpenRocket belgesi.
    :param name: bileşen adı (None → benzersiz otomatik ad).
    :param length: kordon boyu (m).
    :param position: eksenel konum (varsayılan "bottom" — arkada).
    :param parent: üst bileşen (None → son gövde tüpü).
    :return: eklenen bileşen.
    :raises DesignError: geçersiz girdi.
    """
    session = get_session()
    length = _check_number("length", length, minimum=0.0, unit="m")

    rocket = doc.getRocket()
    if name is None:
        name = _unique_name(rocket, _BASENAMES["ShockCord"])
    else:
        _check_unique_name(rocket, name)

    comp = session.component_class("ShockCord")()
    comp.setName(name)
    _set(comp, "setCordLength", length, label="şok kordonu boyu")
    try:
        material = session.core.material.Material.newMaterial(
            session.core.material.Material.Type.LINE,
            "Polyester cord",
            0.0014,
            session.core.material.MaterialGroup.THREADS_LINES,
            True,
        )
        comp.setMaterial(material)
    except Exception:
        # Malzeme atanamazsa kordon yine de eklenir (kütlesiz kalır).
        pass
    _set_position(comp, position)
    return _add_child(_resolve_parent(doc, parent, body_level=False), comp)


# --------------------------------------------------------------------------
# güncelleme / silme
# --------------------------------------------------------------------------
_UPDATERS = {
    "NoseCone": {
        "length": "setLength",
        "radius": "setBaseRadius",
        "base_radius": "setBaseRadius",
        "thickness": "setThickness",
        "shape_parameter": "setShapeParameter",
    },
    "BodyTube": {
        "length": "setLength",
        "radius": "setOuterRadius",
        "outer_radius": "setOuterRadius",
        "thickness": None,
    },
    "Transition": {
        "length": "setLength",
        "fore_radius": "setForeRadius",
        "aft_radius": "setAftRadius",
        "shape_parameter": "setShapeParameter",
    },
    "TrapezoidFinSet": {
        "count": "setFinCount",
        "fin_count": "setFinCount",
        "root_chord": "setRootChord",
        "tip_chord": "setTipChord",
        "height": "setHeight",
        "thickness": "setThickness",
    },
    "EllipticalFinSet": {
        "count": "setFinCount",
        "fin_count": "setFinCount",
        "height": "setHeight",
        "thickness": "setThickness",
        "root_chord": "setLength",
    },
    "InnerTube": {
        "length": "setLength",
        "radius": "setOuterRadius",
        "outer_radius": "setOuterRadius",
    },
    "MassComponent": {
        "length": "setLength",
        "radius": "setRadius",
        "mass": "setComponentMass",
    },
    "Parachute": {
        "diameter": "setDiameter",
        "line_count": "setLineCount",
        "line_length": "setLineLength",
        "cd": "setCD",
    },
    "ShockCord": {
        "length": "setCordLength",
        "cord_length": "setCordLength",
    },
}


def update_component(doc: Any, component_name: str, **params: Any) -> Any:
    """Bileşen parametrelerini günceller.

    Desteklenen parametreler bileşen tipine göre değişir (aşağıdaki tablo).
    Alan adları **snake_case** ve **SI**'dır (uzunluk m, kütle kg, açı derece).
    Bileşeni yeniden adlandırmak için ``name="Yeni ad"`` kullanılır.

    ==================  =====================================================
    Bileşen             Alanlar
    ==================  =====================================================
    NoseCone            length, radius/base_radius, thickness, shape_parameter
    BodyTube            length, radius/outer_radius
    Transition          length, fore_radius, aft_radius, shape_parameter
    TrapezoidFinSet     count/fin_count, root_chord, tip_chord, height, thickness
    EllipticalFinSet    count/fin_count, height, thickness, root_chord
    InnerTube           length, radius/outer_radius
    MassComponent       length, radius, mass
    Parachute           diameter, line_count, line_length, cd
    ShockCord           length/cord_length
    ==================  =====================================================

    :param doc: OpenRocket belgesi.
    :param component_name: bileşen adı.
    :param params: güncellenecek alanlar.
    :return: güncellenen bileşen.
    :raises ComponentNotFoundError: bileşen yoksa.
    :raises DesignError: alan/parametre geçersizse.
    """
    comp = find_component(doc, component_name)
    cls = str(comp.getClass().getSimpleName())
    if cls not in _UPDATERS:
        raise DesignError(f"'{cls}' bileşeni için parametre güncelleme desteklenmiyor.")
    table = _UPDATERS[cls]
    if not params:
        raise DesignError("Güncellenecek en az bir parametre verilmeli.")

    for key, value in params.items():
        field = key.lower()
        if field == "name":
            _check_unique_name(doc.getRocket(), str(value))
            comp.setName(str(value))
            continue
        if field == "sweep":
            if cls != "TrapezoidFinSet":
                raise DesignError("'sweep' yalnız trapezoidal kanatçıkta güncellenebilir.")
            _set(comp, "setSweepAngle", math.radians(_check_number("sweep", value, unit="deg")),
                 label="süpürme açısı")
            continue
        if field == "shape":
            session = get_session()
            _set(comp, "setShapeType", session.transition_shape(value),
                 label="bileşen şekli")
            continue
        if field == "thickness" and cls == "BodyTube":
            t = _check_number("thickness", value, minimum=0.0, unit="m")
            outer = float(comp.getOuterRadius())
            _set(comp, "setInnerRadius", max(outer - t, 1e-4),
                 label="gövde iç yarıçapı")
            continue
        if field not in table:
            raise DesignError(
                f"'{cls}' bileşeninde '{key}' alanı yok. "
                f"Desteklenenler: {', '.join(sorted(set(table) | {'name', 'shape', 'thickness'}))}"
            )
        setter = table[field]
        if setter is None:
            raise DesignError(f"'{cls}' bileşeninde '{key}' alanı doğrudan güncellenemez.")
        if field in ("count", "fin_count", "line_count"):
            ivalue = int(value)
            if ivalue < 1:
                raise DesignError(f"{key} en az 1 olmalı, verilen: {ivalue}")
            _set(comp, setter, ivalue, label=key)
        elif field == "mass":
            _set(comp, setter, _check_number(key, value, minimum=0.0, unit="kg"), label=key)
        elif field == "cd":
            _set(comp, setter, _check_number(key, value, minimum=0.0), label=key)
        else:
            _set(comp, setter, _check_number(key, value, minimum=0.0, unit="m"), label=key)
    return comp


def remove_component(doc: Any, name: str) -> None:
    """Bileşeni siler.

    :param doc: OpenRocket belgesi.
    :param name: silinecek bileşenin adı.
    :raises ComponentNotFoundError: bileşen yoksa.
    :raises DesignError: silinemiyorsa.
    """
    comp = find_component(doc, name)
    parent = comp.getParent()
    if parent is None:
        raise DesignError(f"'{name}' silinemez (üst bileşeni yok / roketin kökü).")
    try:
        ok = parent.removeChild(comp)
    except Exception as e:
        raise DesignError(f"'{name}' silinemedi: {e}") from e
    if not ok:
        raise DesignError(f"'{name}' silinemedi (OpenRocket reddetti).")


# --------------------------------------------------------------------------
# malzeme ve yüzey kaplaması
# --------------------------------------------------------------------------
_MATERIAL_GROUPS = (
    "METALS", "WOODS", "PLASTICS", "FABRICS", "PAPER", "FOAMS",
    "COMPOSITES", "FIBERS", "ELASTICS", "KEVLARS", "NYLONS", "OTHER", "CUSTOM",
)

_FINISHES = {
    "rough": "ROUGH",
    "rough_unfinished": "ROUGHUNFINISHED",
    "roughunfinished": "ROUGHUNFINISHED",
    "unfinished": "UNFINISHED",
    "normal": "NORMAL",
    "smooth": "SMOOTH",
    "optimum": "OPTIMUM",
    "polished": "FINISHPOLISHED",
    "mirror": "MIRROR",
}


def set_component_material(
    doc: Any,
    component_name: str,
    *,
    material_name: str,
    density: float,
    group: str = "COMPOSITES",
) -> Any:
    """Bir bileşene **hacimsel (bulk)** malzeme atar.

    Kütle, OpenRocket tarafından malzeme yoğunluğu × hacim olarak hesaplanır.
    Tipik değerler: karbon fiber kompozit ~1550 kg/m³, fiberglas ~1850 kg/m³,
    G10 ~1900 kg/m³, karton ~680 kg/m³.

    :param doc: OpenRocket belgesi.
    :param component_name: bileşen adı.
    :param material_name: malzeme adı (ör. ``"Carbon fiber composite"``).
    :param density: yoğunluk (kg/m³).
    :param group: malzeme grubu (``COMPOSITES``, ``METALS``, …).
    :return: güncellenen bileşen.
    :raises ComponentNotFoundError: bileşen yoksa.
    :raises DesignError: grup/yoğunluk geçersizse.
    """
    comp = find_component(doc, component_name)
    density = _check_number("density", density, minimum=0.0, unit="kg/m³")
    group_key = str(group).strip().upper()
    if group_key not in _MATERIAL_GROUPS:
        raise DesignError(
            f"Bilinmeyen malzeme grubu: {group!r}. Geçerli: {', '.join(_MATERIAL_GROUPS)}"
        )
    session = get_session()
    Material = session.core.material.Material
    MaterialGroup = session.core.material.MaterialGroup
    mat = Material.newMaterial(
        Material.Type.BULK,
        str(material_name),
        density,
        getattr(MaterialGroup, group_key),
        True,
    )
    _set(comp, "setMaterial", mat, label="malzeme")
    return comp


def set_surface_finish(doc: Any, component_name: str, finish: str = "optimum") -> Any:
    """Dış yüzey kaplamasını (pürüzlülük) ayarlar.

    ``finish``: ``rough``, ``unfinished``, ``normal``, ``smooth``, ``optimum``,
    ``polished`` veya ``mirror``. OpenRocket'ın eski ``POLISHED`` değeri
    ("aircraft sheet-metal") yerine gerçek cilalı yüzey için ``polished``
    → ``FINISHPOLISHED`` eşlenir.

    :param doc: OpenRocket belgesi.
    :param component_name: bileşen adı.
    :param finish: yüzey kaplaması adı.
    :return: güncellenen bileşen.
    :raises ComponentNotFoundError: bileşen yoksa.
    :raises DesignError: kaplama adı geçersizse veya bileşen dış yüzey değilse.
    """
    comp = find_component(doc, component_name)
    key = str(finish).strip().lower()
    if key not in _FINISHES:
        raise DesignError(
            f"Bilinmeyen yüzey kaplaması: {finish!r}. Geçerli: {', '.join(sorted(_FINISHES))}"
        )
    session = get_session()
    Finish = session.core.rocketcomponent.ExternalComponent.Finish
    _set(comp, "setFinish", getattr(Finish, _FINISHES[key]), label="yüzey kaplaması")
    return comp


_DEPLOY_EVENTS = {
    "launch": "LAUNCH",
    "ejection": "EJECTION",
    "apogee": "APOGEE",
    "altitude": "ALTITUDE",
    "never": "NEVER",
}


def set_parachute_deployment(
    doc: Any,
    component_name: str,
    *,
    event: str = "apogee",
    altitude: float = 500.0,
    delay: float = 0.0,
) -> Any:
    """Paraşüt açılma olayını ayarlar.

    :param doc: OpenRocket belgesi.
    :param component_name: paraşüt bileşeninin adı.
    :param event: ``launch``, ``ejection``, ``apogee``, ``altitude`` veya ``never``.
    :param altitude: ``event="altitude"`` için açılma irtifası (m, yere göre);
        diğer olaylarda ölü alan olarak da yazılır (dosyada yanıltıcı değer
        kalmaması için).
    :param delay: olaydan sonra gecikme (s).
    :return: güncellenen paraşüt bileşeni.
    :raises ComponentNotFoundError: bileşen yoksa.
    :raises DesignError: bileşen paraşüt değilse veya olay/irtifa geçersizse.
    """
    comp = find_component(doc, component_name)
    if str(comp.getClass().getSimpleName()) != "Parachute":
        raise DesignError(f"'{component_name}' bir paraşüt değil.")
    key = str(event).strip().lower()
    if key not in _DEPLOY_EVENTS:
        raise DesignError(
            f"Bilinmeyen açılma olayı: {event!r}. Geçerli: {', '.join(_DEPLOY_EVENTS)}"
        )
    altitude = _check_number("altitude", altitude, minimum=0.0, unit="m")
    delay = _check_number("delay", delay, minimum=0.0, unit="s")
    if key == "altitude" and altitude <= 0:
        raise DesignError("'altitude' olayı için altitude > 0 olmalı.")

    session = get_session()
    DeployEvent = session.core.rocketcomponent.DeploymentConfiguration.DeployEvent
    cfg = comp.getDeploymentConfigurations().getDefault()
    _set(cfg, "setDeployEvent", getattr(DeployEvent, _DEPLOY_EVENTS[key]),
         label="paraşüt açılma olayı")
    _set(cfg, "setDeployDelay", delay, label="paraşüt açılma gecikmesi")
    # Açılma irtiftası her olayda yazılır: "altitude" olayında kullanılır, diğer
    # olaylarda ölü alandır ama dosyada yanıltıcı bir değer kalmaması için
    # temizlenir.
    _set(cfg, "setDeployAltitude", altitude, label="paraşüt açılma irtifası")
    return comp


def set_nose_shoulder(
    doc: Any,
    component_name: str,
    *,
    length: float,
    radius: float | None = None,
    thickness: float | None = None,
) -> Any:
    """Burun konisinin gövdeye giren omuzluk (shoulder) geometrisini ayarlar.

    Şartname (4.5.11): omuzluk, gövde dış çapının en az **1.5 katı** olmalı.
    Örn. 117 mm gövde için ≥ 175.5 mm.

    Omuzluk yarıçapı verilmezse OpenRocket'un kendi varsayılanı (burun
    taban yarıçapına eşitlenir) korunur; ``radius`` verilirse yarıçap ve
    ``thickness`` verilirse omuzluk cidarı ayrıca ayarlanır. Omuzluk cidarı
    verilmezse koninin kendi cidarı (``thickness``) kullanılır.

    :param doc: OpenRocket belgesi.
    :param component_name: burun konisi bileşeninin adı.
    :param length: omuzluk uzunluğu (m).
    :param radius: omuzluk dış yarıçapı (m); None → değiştirilmez.
    :param thickness: omuzluk cidarı (m); None → değiştirilmez.
    :return: güncellenen burun konisi.
    :raises ComponentNotFoundError: bileşen yoksa.
    :raises DesignError: bileşen burun konisi değilse veya uzunluk geçersizse.
    """
    comp = find_component(doc, component_name)
    if str(comp.getClass().getSimpleName()) != "NoseCone":
        raise DesignError(f"'{component_name}' bir burun konisi değil.")
    length = _check_number("length", length, minimum=0.0, unit="m")
    _set(comp, "setShoulderLength", length, label="burun omuzluk uzunluğu")
    if radius is not None:
        radius = _check_number("radius", radius, minimum=0.0, unit="m")
        _set(comp, "setShoulderRadius", radius, label="burun omuzluk yarıçapı")
    if thickness is not None:
        thickness = _check_number("thickness", thickness, minimum=0.0, unit="m")
        _set(comp, "setShoulderThickness", thickness, label="burun omuzluk cidarı")
    return comp


_AXIAL_METHODS = {
    "top": "TOP",
    "bottom": "BOTTOM",
    "middle": "MIDDLE",
    "after": "AFTER",
    "absolute": "ABSOLUTE",
}


def set_component_position(
    doc: Any, component_name: str, *, method: str = "absolute", offset: float = 0.0
) -> Any:
    """Bileşenin uçuş ekseni boyunca konumunu ayarlar.

    ``method="absolute"`` seçilirse ``offset``, OpenRocket'ın **referans
    noktasından** (roketin burun ucu) itibaren ölçülen eksenel konumdur (m).
    Diğer yöntemler (``top``/``bottom``/``middle``/``after``) OpenRocket'ın
    kendi göreli konum tanımlarını kullanır; bu yöntemlerde ``offset``
    yalnızca göreli konum kaydırma değeri olarak yorumlanır.

    Bu, gövde içine yerleştirilen yük ve kurtarma donanımının birbirinin
    içine girmemesi için gereklidir: gövde tüpünün "top" ucu, burun
    omuzluğunun gövdeye girdiği bölgede olduğundan, mutlak konum kullanılır.

    :param doc: OpenRocket belgesi.
    :param component_name: bileşen adı.
    :param method: "absolute", "top", "bottom", "middle" veya "after".
    :param offset: konum (m).
    :return: güncellenen bileşen.
    :raises ComponentNotFoundError: bileşen yoksa.
    :raises DesignError: yöntem geçersizse.
    """
    comp = find_component(doc, component_name)
    key = str(method).strip().lower()
    if key not in _AXIAL_METHODS:
        raise DesignError(
            f"Bilinmeyen konum yöntemi: {method!r}. "
            f"Geçerli: {', '.join(sorted(_AXIAL_METHODS))}"
        )
    offset = _check_number("offset", offset, unit="m")
    session = get_session()
    AxialMethod = session.core.rocketcomponent.position.AxialMethod
    _set(comp, "setAxialMethod", getattr(AxialMethod, _AXIAL_METHODS[key]),
         label="bileşen konum yöntemi")
    if key == "absolute":
        _set(comp, "setAxialOffset", offset, label="bileşen eksenel konumu")
    else:
        _set(comp, "setAxialOffset", offset, label="bileşen konum kaydırması")
    return comp


# --------------------------------------------------------------------------
# bulkhead ve centering ring kalınlığı (eksenel uzunluk)
# --------------------------------------------------------------------------
def set_bulkhead_thickness(doc: Any, component_name: str, thickness: float) -> Any:
    """Bulkhead'in eksenel kalınlığını (uzunluğunu) ayarlar.

    :param doc: OpenRocket belgesi.
    :param component_name: bulkhead adı.
    :param thickness: kalınlık (m).
    :return: güncellenen bileşen.
    """
    comp = find_component(doc, component_name)
    if comp.getClass().getSimpleName() != "Bulkhead":
        raise DesignError(f"'{component_name}' bir Bulkhead değil.")
    t = _check_number("thickness", thickness, minimum=0.001, unit="m")
    _set(comp, "setLength", t, label="bulkhead kalınlığı")
    return comp


def set_centering_ring_thickness(doc: Any, component_name: str, thickness: float) -> Any:
    """Centering ring'in eksenel kalınlığını (uzunluğunu) ayarlar.

    :param doc: OpenRocket belgesi.
    :param component_name: centering ring adı.
    :param thickness: kalınlık (m).
    :return: güncellenen bileşen.
    """
    comp = find_component(doc, component_name)
    if comp.getClass().getSimpleName() != "CenteringRing":
        raise DesignError(f"'{component_name}' bir CenteringRing değil.")
    t = _check_number("thickness", thickness, minimum=0.001, unit="m")
    _set(comp, "setLength", t, label="centering ring kalınlığı")
    return comp


# --------------------------------------------------------------------------
# kademe (stage) işlemleri
# --------------------------------------------------------------------------
def add_stage(doc: Any, name: str = "Booster") -> Any:
    """Rokete yeni bir kademe (AxialStage) ekler.

    Eklenen kademe mevcut kademelerin **arkasına** (altına) gelir; OpenRocket'ta
    alt kademe (booster) motor sönümünde ayrılır, üst kademe (sustainer)
    uçuşu sürdürür.

    :param doc: OpenRocket belgesi.
    :param name: kademe adı.
    :return: eklenen kademe.
    :raises DesignError: kademe eklenemezse.
    """
    session = get_session()
    rocket = doc.getRocket()
    try:
        stage = session.core.rocketcomponent.AxialStage()
    except Exception as e:
        raise DesignError(f"Kademe oluşturulamadı: {e}") from e
    stage.setName(str(name))
    try:
        rocket.addChild(stage, rocket.getChildCount(), True)
    except Exception as e:
        raise DesignError(f"Kademe eklenemedi: {e}") from e
    rocket.update()
    return stage


def move_component(doc: Any, component_name: str, target_name: str) -> Any:
    """Bileşeni başka bir üst bileşene taşır (ör. bir alt kademeye).

    Bileşen önce eski ebeveyninden çıkarılır, sonra hedefe eklenir; alt bileşenler
    (kanatçık, paraşüt, iç boru …) bileşenle birlikte taşınır.

    :param doc: OpenRocket belgesi.
    :param component_name: taşınacak bileşenin adı.
    :param target_name: hedef üst bileşenin (ör. kademenin) adı.
    :return: taşınan bileşen.
    :raises ComponentNotFoundError: bileşen ya da hedef yoksa.
    :raises DesignError: taşıma yapılamazsa.
    """
    comp = find_component(doc, component_name)
    target = find_component(doc, target_name)
    if comp is target:
        raise DesignError("Bileşen zaten hedef bileşenin içinde.")
    parent = comp.getParent()
    if parent is None:
        raise DesignError(f"'{component_name}' taşınamaz (üst bileşeni yok).")
    if parent is target:
        return comp
    try:
        parent.removeChild(comp)
        target.addChild(comp, target.getChildCount(), True)
    except Exception as e:
        raise DesignError(f"'{component_name}' taşınamadı: {e}") from e
    doc.getRocket().update()
    return comp
