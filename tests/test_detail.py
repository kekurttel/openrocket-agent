"""Ek bileşenler: halka, bulkhead, kaplin, ray butonu, kademe ayrılması."""

from __future__ import annotations

import pytest

import rocketlib
from rocketlib.detail import (
    add_bulkhead,
    add_centering_ring,
    add_rail_button,
    add_tube_coupler,
    set_stage_separation,
)


def _base():
    doc = rocketlib.new_design("Detail test")
    rocketlib.add_nose_cone(doc, length=0.10, radius=0.019)
    rocketlib.add_body_tube(doc, length=0.40, radius=0.019, thickness=0.001)
    return doc


def _rt(doc, path):
    rocketlib.save_design(doc, path)
    return rocketlib.load_design(path)


def test_centering_ring_roundtrip(or_session, tmp_design):
    doc = _base()
    add_centering_ring(doc, "CR", length=0.006, outer_radius=0.0185,
                       inner_radius=0.012, offset=0.20)
    c = rocketlib.find_component(_rt(doc, tmp_design), "CR")
    assert c.getLength() == pytest.approx(0.006)
    assert c.getOuterRadius() == pytest.approx(0.0185)
    assert c.getInnerRadius() == pytest.approx(0.012)
    assert c.getComponentMass() > 0


def test_bulkhead_roundtrip(or_session, tmp_design):
    doc = _base()
    add_bulkhead(doc, "BH", length=0.004, radius=0.018, offset=0.25)
    c = rocketlib.find_component(_rt(doc, tmp_design), "BH")
    assert c.getLength() == pytest.approx(0.004)
    assert c.getOuterRadius() == pytest.approx(0.018)
    assert c.getComponentMass() > 0


def test_tube_coupler_roundtrip(or_session, tmp_design):
    doc = _base()
    add_tube_coupler(doc, "CO", length=0.147, outer_radius=0.0185,
                     thickness=0.003, offset=0.45)
    c = rocketlib.find_component(_rt(doc, tmp_design), "CO")
    assert c.getLength() == pytest.approx(0.147)
    assert c.getOuterRadius() == pytest.approx(0.0185)
    assert c.getInnerRadius() == pytest.approx(0.0155, abs=1e-4)


def test_rail_button_roundtrip(or_session, tmp_design):
    doc = _base()
    add_rail_button(doc, "RB1", outer_diameter=0.015, height=0.0128,
                    offset=0.12)
    add_rail_button(doc, "RB2", offset=0.42)
    doc2 = _rt(doc, tmp_design)
    for n in ("RB1", "RB2"):
        c = rocketlib.find_component(doc2, n)
        assert c.getOuterDiameter() == pytest.approx(0.015)
        assert c.getTotalHeight() == pytest.approx(0.0128)
        assert c.getComponentMass() > 0


def test_stage_separation_roundtrip(or_session, tmp_design):
    doc = _base()
    rocketlib.add_stage(doc, "Booster")
    set_stage_separation(doc, 1, event="altitude_descending", altitude=500.0)
    doc2 = _rt(doc, tmp_design)
    stage = doc2.getRocket().getStage(1)
    cfg = stage.getSeparationConfiguration()
    assert str(cfg.getSeparationEvent().name()) == "ALTITUDE_DESCENDING"
    assert cfg.getSeparationAltitude() == pytest.approx(500.0)
    assert cfg.getSeparationDelay() == pytest.approx(0.0)

def test_parachute_packed_roundtrip(or_session, tmp_design):
    doc = _base()
    rocketlib.add_parachute(doc, "CH", diameter=0.9, line_count=8,
                            line_length=2.0)
    rocketlib.set_parachute_packed(doc, "CH", length=0.12, diameter=0.08)
    doc2 = _rt(doc, tmp_design)
    c = rocketlib.find_component(doc2, "CH")
    assert c.getLength() == pytest.approx(0.12)
    assert c.getRadius() == pytest.approx(0.04)
