"""Bileşen ekleme / güncelleme / silme testleri.

Her değişiklik için: değiştir → kaydet → yeniden yükle → parametreler aynı mı?
"""

from __future__ import annotations

import math

import pytest

import rocketlib


def _base_design(name="Test roketi"):
    """Testler için küçük bir temel tasarım (motor yuvası ve kurtarma sistemi ile)."""
    doc = rocketlib.new_design(name)
    rocketlib.add_nose_cone(doc, length=0.10, radius=0.019)
    rocketlib.add_body_tube(doc, length=0.30, radius=0.019)
    rocketlib.add_inner_tube(doc, length=0.070, radius=0.0125)
    rocketlib.add_parachute(doc, diameter=0.30)
    return doc


def _roundtrip(doc, path):
    """Kaydet → geri yükle → döndür."""
    rocketlib.save_design(doc, path)
    return rocketlib.load_design(path)


# --------------------------------------------------------------------------
# add_* fonksiyonları
# --------------------------------------------------------------------------
def test_add_nose_cone_roundtrip(or_session, tmp_design):
    doc = _base_design()
    rocketlib.add_nose_cone(doc, name="NC2", length=0.12, radius=0.018,
                            shape="conical", thickness=0.0015)
    doc2 = _roundtrip(doc, tmp_design)
    comp = rocketlib.find_component(doc2, "NC2")
    assert comp.getLength() == pytest.approx(0.12)
    assert comp.getBaseRadius() == pytest.approx(0.018)
    assert comp.getThickness() == pytest.approx(0.0015)
    assert str(comp.getShapeType().name()) == "CONICAL"


def test_add_body_tube_roundtrip(or_session, tmp_design):
    doc = _base_design()
    rocketlib.add_body_tube(doc, name="BT2", length=0.25, radius=0.015,
                            thickness=0.0008)
    doc2 = _roundtrip(doc, tmp_design)
    comp = rocketlib.find_component(doc2, "BT2")
    assert comp.getLength() == pytest.approx(0.25)
    assert comp.getOuterRadius() == pytest.approx(0.015)
    assert comp.getInnerRadius() == pytest.approx(0.015 - 0.0008, abs=1e-4)


def test_add_transition_roundtrip(or_session, tmp_design):
    doc = _base_design()
    rocketlib.add_transition(doc, name="TR", length=0.04, fore_radius=0.019,
                             aft_radius=0.012, shape="conical")
    doc2 = _roundtrip(doc, tmp_design)
    comp = rocketlib.find_component(doc2, "TR")
    assert comp.getLength() == pytest.approx(0.04)
    assert comp.getForeRadius() == pytest.approx(0.019)
    assert comp.getAftRadius() == pytest.approx(0.012)


def test_add_trapezoidal_fin_set_roundtrip(or_session, tmp_design):
    doc = _base_design()
    rocketlib.add_fin_set(doc, name="Fins", shape="trapezoidal", count=4,
                          root_chord=0.055, tip_chord=0.025, height=0.04,
                          sweep=50.0, thickness=0.002)
    doc2 = _roundtrip(doc, tmp_design)
    comp = rocketlib.find_component(doc2, "Fins")
    assert comp.getFinCount() == 4
    assert comp.getRootChord() == pytest.approx(0.055)
    assert comp.getTipChord() == pytest.approx(0.025)
    assert comp.getHeight() == pytest.approx(0.04)
    assert math.degrees(comp.getSweepAngle()) == pytest.approx(50.0, abs=1e-3)
    assert comp.getThickness() == pytest.approx(0.002)


def test_add_elliptical_fin_set_roundtrip(or_session, tmp_design):
    doc = _base_design()
    rocketlib.add_fin_set(doc, name="EFins", shape="elliptical", count=3,
                          root_chord=0.04, height=0.035, thickness=0.0015)
    doc2 = _roundtrip(doc, tmp_design)
    comp = rocketlib.find_component(doc2, "EFins")
    assert comp.getFinCount() == 3
    assert comp.getHeight() == pytest.approx(0.035)
    assert comp.getThickness() == pytest.approx(0.0015)


def test_add_inner_tube_roundtrip(or_session, tmp_design):
    doc = _base_design()
    rocketlib.add_inner_tube(doc, name="IT2", length=0.05, radius=0.0125)
    doc2 = _roundtrip(doc, tmp_design)
    comp = rocketlib.find_component(doc2, "IT2")
    assert comp.getLength() == pytest.approx(0.05)
    assert comp.getOuterRadius() == pytest.approx(0.0125)
    assert comp.isMotorMount() is True


def test_add_mass_component_roundtrip(or_session, tmp_design):
    doc = _base_design()
    rocketlib.add_mass_component(doc, name="Payload", length=0.03, radius=0.01,
                                 mass=0.012)
    doc2 = _roundtrip(doc, tmp_design)
    comp = rocketlib.find_component(doc2, "Payload")
    assert comp.getLength() == pytest.approx(0.03)
    assert comp.getComponentMass() == pytest.approx(0.012)


def test_add_parachute_roundtrip(or_session, tmp_design):
    doc = _base_design()
    rocketlib.add_parachute(doc, name="Chute2", diameter=0.45, line_count=8,
                            line_length=0.4, cd=0.9)
    doc2 = _roundtrip(doc, tmp_design)
    comp = rocketlib.find_component(doc2, "Chute2")
    assert comp.getDiameter() == pytest.approx(0.45)
    assert comp.getLineCount() == 8
    assert comp.getLineLength() == pytest.approx(0.4)
    assert comp.getCD() == pytest.approx(0.9)


def test_add_shock_cord_roundtrip(or_session, tmp_design):
    doc = _base_design()
    rocketlib.add_shock_cord(doc, name="Cord", length=0.25)
    doc2 = _roundtrip(doc, tmp_design)
    comp = rocketlib.find_component(doc2, "Cord")
    assert comp.getCordLength() == pytest.approx(0.25)


# --------------------------------------------------------------------------
# update_component / remove_component
# --------------------------------------------------------------------------
def test_update_component_roundtrip(or_session, tmp_design):
    doc = _base_design()
    rocketlib.add_fin_set(doc, name="Fins", count=3, root_chord=0.05,
                          tip_chord=0.02, height=0.03, sweep=45.0)
    rocketlib.update_component(doc, "Fins", count=4, root_chord=0.07,
                               height=0.045, sweep=60.0)
    doc2 = _roundtrip(doc, tmp_design)
    comp = rocketlib.find_component(doc2, "Fins")
    assert comp.getFinCount() == 4
    assert comp.getRootChord() == pytest.approx(0.07)
    assert comp.getHeight() == pytest.approx(0.045)
    assert math.degrees(comp.getSweepAngle()) == pytest.approx(60.0, abs=1e-3)


def test_update_component_rename(or_session, tmp_design):
    doc = _base_design()
    rocketlib.update_component(doc, "Body tube", name="Gövde")
    doc2 = _roundtrip(doc, tmp_design)
    assert "Gövde" in [str(c.getName()) for c in rocketlib.list_components(doc2)]


def test_remove_component_roundtrip(or_session, tmp_design):
    doc = _base_design()
    rocketlib.add_mass_component(doc, name="Atılacak", mass=0.02)
    before = len(rocketlib.list_components(doc))
    rocketlib.remove_component(doc, "Atılacak")
    doc2 = _roundtrip(doc, tmp_design)
    names = [str(c.getName()) for c in rocketlib.list_components(doc2)]
    assert "Atılacak" not in names
    assert len(names) == before - 1


# --------------------------------------------------------------------------
# hata yolları
# --------------------------------------------------------------------------
def test_negative_size_raises(or_session):
    doc = _base_design()
    with pytest.raises(rocketlib.DesignError):
        rocketlib.add_body_tube(doc, length=-0.1)
    with pytest.raises(rocketlib.DesignError):
        rocketlib.add_mass_component(doc, mass=-1.0)


def test_unknown_component_raises(or_session):
    doc = _base_design()
    with pytest.raises(rocketlib.ComponentNotFoundError):
        rocketlib.update_component(doc, "Yok", length=0.1)
    with pytest.raises(rocketlib.ComponentNotFoundError):
        rocketlib.remove_component(doc, "Yok")


def test_duplicate_name_raises(or_session):
    doc = _base_design()
    with pytest.raises(rocketlib.DuplicateComponentError):
        rocketlib.add_body_tube(doc, name="Body tube")


def test_unknown_motor_raises(or_session):
    doc = _base_design()
    with pytest.raises(rocketlib.MotorError):
        rocketlib.set_motor(doc, "ZZZ999", manufacturer="Estes")


def test_auto_names_are_unique(or_session):
    doc = _base_design()
    a = rocketlib.add_body_tube(doc, length=0.2, radius=0.015)
    b = rocketlib.add_body_tube(doc, length=0.2, radius=0.015)
    assert str(a.getName()) != str(b.getName())
    names = [str(c.getName()) for c in rocketlib.list_components(doc)]
    assert len(names) == len(set(names))


def test_component_order_is_front_to_back(or_session):
    """Burun konisi gövdenin önünde, geçiş arkasında olmalı."""
    doc = rocketlib.new_design("Sıra")
    rocketlib.add_nose_cone(doc, length=0.10, radius=0.019)
    rocketlib.add_body_tube(doc, length=0.30, radius=0.019)
    rocketlib.add_transition(doc, length=0.05, fore_radius=0.019, aft_radius=0.01)
    stage = doc.getRocket().getStage(0)
    order = [str(c.getName()) for c in stage.getChildren()]
    assert order.index("Nose cone") < order.index("Body tube") < order.index("Transition")


def test_set_component_material_and_finish_roundtrip(or_session, tmp_design):
    """Malzeme ve yüzey kaplaması kaydedilip yeniden yüklendiğinde korunmalı."""
    doc = _base_design("Malzeme testi")
    rocketlib.set_component_material(
        doc, "Body tube", material_name="Carbon fiber composite", density=1550.0
    )
    rocketlib.set_surface_finish(doc, "Nose cone", "polished")

    reloaded = _roundtrip(doc, tmp_design)
    body = rocketlib.find_component(reloaded, "Body tube")
    nose = rocketlib.find_component(reloaded, "Nose cone")

    assert body.getMaterial().getName() == "Carbon fiber composite"
    assert body.getMaterial().getDensity() == pytest.approx(1550.0, rel=1e-6)
    # OpenRocket "polished" = FINISHPOLISHED (0.5 µm)
    assert str(nose.getFinish().name()) == "FINISHPOLISHED"


def test_set_component_material_rejects_unknown_group(or_session):
    """Bilinmeyen malzeme grubu DesignError üretmeli."""
    doc = _base_design("Grup testi")
    with pytest.raises(rocketlib.DesignError):
        rocketlib.set_component_material(
            doc, "Body tube", material_name="X", density=1000.0, group="UNOBTAINIUM"
        )


def test_set_parachute_deployment_roundtrip(or_session, tmp_design):
    """Paraşüt açılma olayı/gecikmesi kaydedilip yeniden yüklendiğinde korunmalı."""
    doc = _base_design("Paraşüt olayı testi")
    rocketlib.set_parachute_deployment(doc, "Parachute", event="apogee", delay=1.0)

    reloaded = _roundtrip(doc, tmp_design)
    chute = rocketlib.find_component(reloaded, "Parachute")
    cfg = chute.getDeploymentConfigurations().getDefault()
    assert str(cfg.getDeployEvent().name()) == "APOGEE"
    assert cfg.getDeployDelay() == pytest.approx(1.0, rel=1e-6)

    rocketlib.set_parachute_deployment(
        reloaded, "Parachute", event="altitude", altitude=500.0
    )
    chute = rocketlib.find_component(reloaded, "Parachute")
    cfg = chute.getDeploymentConfigurations().getDefault()
    assert str(cfg.getDeployEvent().name()) == "ALTITUDE"
    assert cfg.getDeployAltitude() == pytest.approx(500.0, rel=1e-6)


def test_set_nose_shoulder_roundtrip(or_session, tmp_design):
    """Burun omuzluk uzunluğu kaydedilip yeniden yüklendiğinde korunmalı."""
    doc = _base_design("Omuzluk testi")
    rocketlib.set_nose_shoulder(doc, "Nose cone", length=0.1755)
    reloaded = _roundtrip(doc, tmp_design)
    nose = rocketlib.find_component(reloaded, "Nose cone")
    assert nose.getShoulderLength() == pytest.approx(0.1755, rel=1e-6)


def test_set_nose_shoulder_radius_roundtrip(or_session, tmp_design):
    """Omuzluk yarıçapı ve cidarı kaydedilip yeniden yüklendiğinde korunmalı."""
    doc = _base_design("Omuzluk yarıçapı testi")
    # omuzluk yarıçapı burun taban yarıçapından (0.019) büyükse OpenRocket
    # bunu taban yarıçapına kırpar; bu yüzden küçük bir değer seçilir.
    rocketlib.set_nose_shoulder(doc, "Nose cone", length=0.1755, radius=0.015,
                                thickness=0.002)
    reloaded = _roundtrip(doc, tmp_design)
    nose = rocketlib.find_component(reloaded, "Nose cone")
    assert nose.getShoulderLength() == pytest.approx(0.1755, rel=1e-6)
    assert nose.getShoulderRadius() == pytest.approx(0.015, rel=1e-6)
    assert nose.getShoulderThickness() == pytest.approx(0.002, rel=1e-6)


def test_set_component_position_absolute(or_session, tmp_design):
    """Mutlak (absolute) konum: ofset roketin burun ucundan ölçülmeli."""
    doc = _base_design("Konum testi")
    rocketlib.add_mass_component(doc, name="Payload", length=0.10, radius=0.015,
                                 mass=1.0)
    rocketlib.set_component_position(doc, "Payload", method="absolute", offset=0.25)
    comp = rocketlib.find_component(doc, "Payload")
    # mutlak ofset = roket koordinatı (burun ucu = 0)
    assert comp.getAxialOffset() == pytest.approx(0.25, abs=1e-6)
    # gövde burun ucundan 0.10 m sonra başlıyor → bileşen gövdeye göre 0.15 m
    assert comp.getPosition().x == pytest.approx(0.15, abs=1e-6)

    reloaded = _roundtrip(doc, tmp_design)
    comp2 = rocketlib.find_component(reloaded, "Payload")
    assert comp2.getAxialOffset() == pytest.approx(0.25, abs=1e-6)
    assert comp2.getPosition().x == pytest.approx(0.15, abs=1e-6)


def test_set_component_position_relative_methods(or_session):
    """top/bottom/middle yöntemleri OpenRocket'ın göreli konumlarını kullanmalı."""
    doc = _base_design("Göreli konum testi")
    rocketlib.add_mass_component(doc, name="Yük", length=0.10, radius=0.015, mass=1.0)
    rocketlib.set_component_position(doc, "Yük", method="bottom")
    comp = rocketlib.find_component(doc, "Yük")
    # "bottom": bileşenin arka ucu gövdenin arka ucuyla (0.40 m) çakışır;
    # bileşen 0.10 m uzun → gövdeye göre 0.20 m, roket koordinatında 0.30 m.
    assert comp.getPosition().x == pytest.approx(0.20, abs=1e-6)
    assert comp.getPosition().x + 0.10 == pytest.approx(0.30, abs=1e-6)


def test_set_component_position_rejects_unknown_method(or_session):
    """Bilinmeyen konum yöntemi DesignError üretmeli."""
    doc = _base_design("Hatalı konum testi")
    with pytest.raises(rocketlib.DesignError):
        rocketlib.set_component_position(doc, "Body tube", method="yok")
    with pytest.raises(rocketlib.ComponentNotFoundError):
        rocketlib.set_component_position(doc, "Yok", method="absolute", offset=0.1)


def test_set_motor_ignition_roundtrip(or_session, tmp_design):
    """Motor ateşleme olayı ve gecikmesi kaydedilip yeniden yüklendiğinde korunmalı."""
    doc = _base_design("Ateşleme testi")
    rocketlib.set_motor(doc, "C6", manufacturer="Estes")
    rocketlib.set_motor_ignition(doc, event="launch", delay=1.5)

    reloaded = _roundtrip(doc, tmp_design)
    mount = rocketlib.find_component(reloaded, "Inner Tube")
    fcid = reloaded.getSimulation(0).getFlightConfigurationId()
    cfg = mount.getMotorConfig(fcid)
    assert str(cfg.getIgnitionEvent()).upper() == "LAUNCH"
    assert cfg.getIgnitionDelay() == pytest.approx(1.5, rel=1e-6)


def test_set_motor_ignition_rejects_unknown_event(or_session):
    """Bilinmeyen ateşleme olayı DesignError üretmeli."""
    doc = _base_design("Hatalı ateşleme testi")
    rocketlib.set_motor(doc, "C6", manufacturer="Estes")
    with pytest.raises(rocketlib.DesignError):
        rocketlib.set_motor_ignition(doc, event="yanlış")


# --------------------------------------------------------------------------
# kademe işlemleri
# --------------------------------------------------------------------------
def test_add_stage_and_move_component(or_session, tmp_design):
    """Yeni kademe eklenip bileşenler oraya taşınabilmeli."""
    doc = _base_design("Kademe testi")
    rocketlib.add_stage(doc, "Booster")
    rocketlib.add_body_tube(doc, name="Booster govdesi", length=0.20, radius=0.019)
    rocketlib.move_component(doc, "Booster govdesi", "Booster")

    reloaded = _roundtrip(doc, tmp_design)
    rocket = reloaded.getRocket()
    stages = [str(s.getName()) for s in rocket.getSubStages()]
    assert stages == ["Sustainer", "Booster"]
    booster = rocketlib.find_component(reloaded, "Booster govdesi")
    assert str(booster.getStage().getName()) == "Booster"


def test_move_component_rejects_unknown(or_session):
    """Bilinmeyen bileşen/hedef hata üretmeli."""
    doc = _base_design("Hatalı taşıma testi")
    rocketlib.add_stage(doc, "Booster")
    with pytest.raises(rocketlib.ComponentNotFoundError):
        rocketlib.move_component(doc, "Yok", "Booster")
    with pytest.raises(rocketlib.ComponentNotFoundError):
        rocketlib.move_component(doc, "Body tube", "Yok")
