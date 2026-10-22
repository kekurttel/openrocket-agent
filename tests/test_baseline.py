"""Regresyon testleri: `tests/baselines.json` ile %1 toleranslı karşılaştırma.

Baseline'lar `scratch/make_baselines.py` ile üretildi: her örnek dosyanın her
simülasyonu, **rüzgâr 0 / türbülans 0** (süreçler arası deterministik) ve sabit
seed (1) ile uçuruldu. Test, aynı koşulları kurup aynı simülasyonu tekrar
çalıştırır ve sonuçları %1 toleransla karşılaştırır.
"""

from __future__ import annotations

import pytest

import rocketlib

FIELDS = (
    "apogee_m",
    "max_velocity_mps",
    "max_acceleration_mps2",
    "time_to_apogee_s",
    "flight_time_s",
    "rail_exit_velocity_mps",
    "deployment_velocity_mps",
    "landing_velocity_mps",
    "optimum_delay_s",
    "stability_at_launch_cal",
)

TOLERANCE = 0.01  # %1


def _cases(baselines):
    """(dosya adı, baseline girdisi, simülasyon) üçlüleri."""
    for name, entry in sorted(baselines.items()):
        for sim in entry["simulations"]:
            yield name, entry, sim


def test_baseline_files_exist(baselines):
    assert baselines, "tests/baselines.json boş olamaz"
    assert len(baselines) >= 2
    assert sum(len(e["simulations"]) for e in baselines.values()) >= 5


def test_regression_against_baseline(or_session, examples_dir, baselines):
    """Her örnek dosyanın her simülasyonu baseline ile %1 toleransla eşleşmeli."""
    failures = []
    checked = 0

    for name, entry in sorted(baselines.items()):
        path = examples_dir / name
        assert path.exists(), f"baseline'daki dosya yok: {path}"
        doc = rocketlib.load_design(path)

        for sim in entry["simulations"]:
            index = sim["index"]
            # baseline koşulları: dosyanın kendi rampa ayarı + rüzgâr/türbülans 0
            rocketlib.set_launch_conditions(
                doc,
                rod_length=None,
                rod_angle=None,
                wind_speed=0.0,
                wind_turbulence=0.0,
                simulation_index=index,
            )
            metrics = rocketlib.run(doc, seed=entry["seed"], simulation_index=index)

            for field in FIELDS:
                expected = sim.get(field)
                actual = metrics.get(field)
                if expected is None and actual is None:
                    continue
                assert expected is not None, f"{name} sim{index}: {field} baseline'da yok"
                assert actual is not None, f"{name} sim{index}: {field} sonuçta yok"
                denom = abs(expected) if abs(expected) > 1e-9 else 1.0
                rel = abs(actual - expected) / denom
                checked += 1
                if rel > TOLERANCE:
                    failures.append(
                        f"{name} sim{index} {field}: beklenen {expected!r}, alınan {actual!r} "
                        f"(sapma %{rel * 100:.3f})"
                    )

    assert not failures, "baseline sapmaları:\n" + "\n".join(failures)
    assert checked > 0, "hiçbir metrik karşılaştırılmadı"


def test_baseline_is_deterministic(or_session, examples_dir):
    """Aynı simülasyon iki kez çalıştırılınca sonuç birebir aynı olmalı."""
    path = examples_dir / "simple_model.ork"
    doc = rocketlib.load_design(path)
    rocketlib.set_launch_conditions(
        doc, rod_length=None, rod_angle=None, wind_speed=0.0, wind_turbulence=0.0,
        simulation_index=0,
    )
    a = rocketlib.run(doc, seed=7, simulation_index=0)
    b = rocketlib.run(doc, seed=7, simulation_index=0)
    assert a["apogee_m"] == b["apogee_m"]
    assert a["max_velocity_mps"] == b["max_velocity_mps"]
    assert a["landing_velocity_mps"] == b["landing_velocity_mps"]


def test_stored_openrocket_results_match(or_session, examples_dir):
    """OpenRocket'ın .ork içine kaydettiği sonuçlar bizim sonuçlarımızla uyuşmalı.

    Tolerans %5 (görev kuralı): fark seed kaynaklı rastgelelikten doğar.
    """
    path = examples_dir / "simple_model.ork"
    doc = rocketlib.load_design(path)
    sim = doc.getSimulation(0)
    assert sim.hasSummaryData(), "örnek dosyada kayıtlı uçuş özeti yok"
    stored = sim.getSimulatedData()

    metrics = rocketlib.run(doc, seed=1, simulation_index=0)

    pairs = (
        (metrics["apogee_m"], float(stored.getMaxAltitude())),
        (metrics["max_velocity_mps"], float(stored.getMaxVelocity())),
        (metrics["flight_time_s"], float(stored.getFlightTime())),
        (metrics["rail_exit_velocity_mps"], float(stored.getLaunchRodVelocity())),
    )
    for ours, theirs in pairs:
        assert ours is not None and theirs is not None
        denom = abs(theirs) if abs(theirs) > 1e-9 else 1.0
        assert abs(ours - theirs) / denom < 0.05, (
            f"sapma çok büyük: bizim {ours}, OpenRocket {theirs}"
        )
