"""validate() testleri: bilinçli bozuk tasarımlar.

- kararsız roket (kanatçıksız / küçük kanatçık)
- gövdeye sığmayan motor
- paraşütsüz roket
- motorsuz roket
- tekrar eden bileşen adı
"""

from __future__ import annotations

import pytest

import rocketlib


def _codes(issues):
    return {i["code"] for i in issues}


def _severities(issues):
    return {i["code"]: i["severity"] for i in issues}


def test_unstable_rocket_is_flagged(or_session):
    """Kanatçıksız (veya çok küçük kanatçıklı) roket kararsız sayılmalı."""
    doc = rocketlib.new_design("Kararsız")
    rocketlib.add_nose_cone(doc, length=0.10, radius=0.019)
    rocketlib.add_body_tube(doc, length=0.30, radius=0.019)
    rocketlib.add_inner_tube(doc, length=0.070, radius=0.0125)
    rocketlib.add_parachute(doc, diameter=0.30)
    rocketlib.set_motor(doc, "C6", manufacturer="Estes")
    rocketlib.set_launch_conditions(doc, rod_length=1.0, rod_angle=15.0, wind_speed=0.0)

    issues = rocketlib.validate(doc, seed=1)
    codes = _codes(issues)
    assert "stability-critical" in codes or "stability-low" in codes, issues
    assert _severities(issues)["stability-critical"] == "error" if (
        "stability-critical" in codes
    ) else True


def test_missing_recovery_is_error(or_session):
    """Paraşüt/streamer yoksa hata verilmeli."""
    doc = rocketlib.new_design("Kurtarmasız")
    rocketlib.add_nose_cone(doc, length=0.10, radius=0.019)
    rocketlib.add_body_tube(doc, length=0.30, radius=0.019)
    rocketlib.add_fin_set(doc, count=3, root_chord=0.05, tip_chord=0.02,
                          height=0.03, sweep=45.0)
    rocketlib.add_inner_tube(doc, length=0.070, radius=0.0125)
    rocketlib.set_motor(doc, "C6", manufacturer="Estes")

    issues = rocketlib.validate(doc, seed=1)
    assert "no-recovery" in _codes(issues)
    assert _severities(issues)["no-recovery"] == "error"


def test_missing_motor_is_error(or_session):
    """Motor atanmamışsa hata verilmeli."""
    doc = rocketlib.new_design("Motorsuz")
    rocketlib.add_nose_cone(doc, length=0.10, radius=0.019)
    rocketlib.add_body_tube(doc, length=0.30, radius=0.019)
    rocketlib.add_fin_set(doc, count=3, root_chord=0.05, tip_chord=0.02,
                          height=0.03, sweep=45.0)
    rocketlib.add_inner_tube(doc, length=0.070, radius=0.0125)
    rocketlib.add_parachute(doc, diameter=0.30)

    issues = rocketlib.validate(doc, seed=1)
    assert "no-motor" in _codes(issues)
    assert _severities(issues)["no-motor"] == "error"


def test_oversized_motor_is_error(or_session):
    """18 mm'lik yuvaya 24 mm'lik motor sığmıyor → hata."""
    doc = rocketlib.new_design("Sığmayan motor")
    rocketlib.add_nose_cone(doc, length=0.10, radius=0.019)
    rocketlib.add_body_tube(doc, length=0.30, radius=0.019)
    rocketlib.add_fin_set(doc, count=3, root_chord=0.05, tip_chord=0.02,
                          height=0.03, sweep=45.0)
    rocketlib.add_inner_tube(doc, length=0.070, radius=0.0105, thickness=0.0005)
    #  → iç çap 20 mm
    rocketlib.add_parachute(doc, diameter=0.30)
    rocketlib.set_motor(doc, "D12", manufacturer="Estes")        # 24 mm'lik motor
    rocketlib.set_launch_conditions(doc, rod_length=1.0, rod_angle=15.0, wind_speed=0.0)

    issues = rocketlib.validate(doc, seed=1)
    codes = _codes(issues)
    assert "motor-too-fat" in codes or "motor-too-long" in codes, issues
    assert _severities(issues).get("motor-too-fat", "error") == "error"


def test_duplicate_component_name_is_warning(or_session):
    """Aynı adı iki bileşen kullandığında uyarı verilmeli."""
    doc = rocketlib.new_design("Tekrar eden ad")
    rocketlib.add_nose_cone(doc, length=0.10, radius=0.019)
    rocketlib.add_body_tube(doc, length=0.30, radius=0.019)
    rocketlib.add_inner_tube(doc, length=0.070, radius=0.0125)
    rocketlib.add_parachute(doc, diameter=0.30)
    # kütüphane tekrar eden adı engeller → doğrudan Java API ile oluşturulur
    rocket = doc.getRocket()
    chute = rocketlib.find_component(doc, "Parachute")
    chute.setName("Body tube")

    issues = rocketlib.validate(doc, seed=1)
    assert "duplicate-name" in _codes(issues)
    assert _severities(issues)["duplicate-name"] == "warning"


def test_low_rail_velocity_is_warning(or_session):
    """Kısa rampa/çok yavaş motor → rampa çıkış hızı uyarısı."""
    doc = rocketlib.new_design("Yavaş çıkış")
    rocketlib.add_nose_cone(doc, length=0.10, radius=0.019)
    rocketlib.add_body_tube(doc, length=0.30, radius=0.019)
    rocketlib.add_fin_set(doc, count=3, root_chord=0.05, tip_chord=0.02,
                          height=0.03, sweep=45.0)
    rocketlib.add_inner_tube(doc, length=0.070, radius=0.0125)
    rocketlib.add_parachute(doc, diameter=0.30)
    rocketlib.set_motor(doc, "A8", manufacturer="Estes")   # 0.5 Ns'lik zayıf motor
    rocketlib.set_launch_conditions(doc, rod_length=0.05, rod_angle=0.0, wind_speed=0.0)

    issues = rocketlib.validate(doc, seed=1)
    assert "rail-velocity-low" in _codes(issues)
    assert _severities(issues)["rail-velocity-low"] == "warning"


def test_validate_returns_issue_schema(or_session):
    """Her uyarı sözlüğü {severity, code, message} şemasında olmalı."""
    doc = rocketlib.new_design("Şema")
    rocketlib.add_nose_cone(doc, length=0.10, radius=0.019)
    rocketlib.add_body_tube(doc, length=0.30, radius=0.019)
    issues = rocketlib.validate(doc, seed=1)
    assert isinstance(issues, list)
    for issue in issues:
        assert set(issue) == {"severity", "code", "message"}
        assert issue["severity"] in ("error", "warning")
        assert isinstance(issue["message"], str) and issue["message"]
