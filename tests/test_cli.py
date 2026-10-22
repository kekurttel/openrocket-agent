"""CLI testleri: `sim.py` alt komutları subprocess ile çağrılır.

Çıktı daima tek JSON nesnesi olmalı; hata durumunda çıkış kodu sıfırdan farklı.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SIM = ROOT / "sim.py"
EXAMPLES = ROOT / "designs" / "examples"


def run_cli(*args, expect_ok=True):
    """sim.py'yi çalıştırır, (exit_code, stdout_json, stderr) döndürür."""
    proc = subprocess.run(
        [sys.executable, str(SIM), *args],
        capture_output=True,
        text=True,
        timeout=600,
        cwd=str(ROOT),
    )
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError as e:  # pragma: no cover
        raise AssertionError(
            f"stdout JSON değil (exit={proc.returncode}):\n{proc.stdout[:2000]}\n"
            f"stderr:\n{proc.stderr[:2000]}"
        ) from e
    if expect_ok:
        assert proc.returncode == 0, f"exit={proc.returncode}: {proc.stdout[:500]}"
    return proc.returncode, payload, proc.stderr


def test_inspect_outputs_json(or_session):
    code, payload, _ = run_cli("inspect", str(EXAMPLES / "simple_model.ork"))
    assert code == 0
    assert payload["ok"] is True
    design = payload["design"]
    assert design["rocket"]["name"]
    assert len(design["components"]) == 13
    names = [c["name"] for c in design["components"]]
    assert "Nose cone" in names and "Body tube" in names
    # JSON'a çevrilebilir olmalı
    json.dumps(payload)


def test_run_outputs_metrics(or_session):
    code, payload, _ = run_cli(
        "run", str(EXAMPLES / "simple_model.ork"),
        "--wind", "3", "--rod", "1.0", "--angle", "18", "--seed", "1",
    )
    assert code == 0
    assert payload["ok"] is True
    m = payload["metrics"]
    assert m["apogee_m"] > 0
    assert m["max_velocity_mps"] > 0
    assert m["flight_time_s"] > 0
    assert payload["launch_conditions"]["wind_speed_mps"] == 3.0
    assert payload["launch_conditions"]["rod_angle_deg"] == 18.0


def test_validate_outputs_issues(or_session):
    code, payload, _ = run_cli("validate", str(EXAMPLES / "simple_model.ork"), "--seed", "1")
    assert code == 0
    assert payload["ok"] is True
    assert "issues" in payload
    assert payload["error_count"] == 0


def test_set_updates_and_saves(or_session, tmp_path):
    target = tmp_path / "copy.ork"
    shutil.copy(EXAMPLES / "simple_model.ork", target)
    code, payload, _ = run_cli("set", str(target), "Body tube", "length=0.25", "radius=0.018")
    assert code == 0
    assert payload["ok"] is True
    assert payload["updated"] == {"length": 0.25, "radius": 0.018}

    # dosya gerçekten değişti mi?
    code2, payload2, _ = run_cli("inspect", str(target))
    body = [c for c in payload2["design"]["components"] if c["name"] == "Body tube"][0]
    assert body["length_m"] == pytest.approx(0.25)
    assert body["radius_m"] == pytest.approx(0.018)


def test_missing_file_returns_error_json(or_session, tmp_path):
    code, payload, _ = run_cli("run", str(tmp_path / "yok.ork"), expect_ok=False)
    assert code != 0
    assert payload["ok"] is False
    assert "error" in payload and payload["error"]


def test_unknown_component_returns_error_json(or_session, tmp_path):
    target = tmp_path / "copy.ork"
    shutil.copy(EXAMPLES / "simple_model.ork", target)
    code, payload, _ = run_cli("set", str(target), "Olmayan Bileşen", "length=0.1",
                               expect_ok=False)
    assert code != 0
    assert payload["ok"] is False
    assert "Olmayan Bileşen" in payload["error"]


def test_stdout_is_only_json(or_session):
    """stdout'ta JSON dışında hiçbir şey olmamalı (loglar stderr'de)."""
    proc = subprocess.run(
        [sys.executable, str(SIM), "run", str(EXAMPLES / "simple_model.ork"), "--seed", "1"],
        capture_output=True, text=True, timeout=600, cwd=str(ROOT),
    )
    assert proc.stdout.lstrip().startswith("{")
    json.loads(proc.stdout)
    assert proc.returncode == 0
