"""pytest ortak kurulumu.

JPype bir süreçte yalnızca bir JVM başlatabilir; bu yüzden OpenRocket oturumu
**session-scoped** bir fixture ile bir kez kurulur ve tüm testler paylaşır.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import rocketlib  # noqa: E402


@pytest.fixture(scope="session")
def or_session():
    """Açık OpenRocket oturumu (JVM + çekirdek)."""
    return rocketlib.get_session()


@pytest.fixture(scope="session")
def examples_dir() -> Path:
    """Örnek .ork dosyalarının bulunduğu klasör."""
    return ROOT / "designs" / "examples"


@pytest.fixture(scope="session")
def baselines() -> dict:
    """Regresyon baseline verisi."""
    import json

    path = ROOT / "tests" / "baselines.json"
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture
def tmp_design(tmp_path) -> Path:
    """Çalışma alanı için geçici .ork dosyası yolu."""
    return tmp_path / "design.ork"
