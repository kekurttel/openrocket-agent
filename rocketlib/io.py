"""Tasarım dosyası (``.ork``) yükleme / kaydetme / kopyalama / oluşturma.

Birimler: yol uzunlukları metre değil, dosya sistemi yoludur; tasarım
parametreleri SI'dır (bkz. :mod:`rocketlib.build`).
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from .errors import DesignError
from .session import get_session

__all__ = [
    "load_design",
    "save_design",
    "copy_design",
    "new_design",
    "save_design_with_data",
]


def load_design(path: str | os.PathLike[str]) -> Any:
    """``.ork`` dosyasını yükler ve OpenRocket belgesini döndürür.

    :param path: ``.ork`` dosya yolu.
    :return: ``info.openrocket.core.document.OpenRocketDocument``
    :raises DesignError: dosya yoksa veya okunamazsa.
    """
    p = Path(path)
    if not p.exists():
        raise DesignError(f"Tasarım dosyası bulunamadı: {p}")
    session = get_session()
    try:
        doc = session.helper.load_doc(str(p))
    except Exception as e:
        raise DesignError(f"{p} okunamadı (geçerli bir .ork dosyası mı?): {e}") from e
    if doc is None:
        raise DesignError(f"{p} yüklenemedi: OpenRocket belge döndürmedi.")
    return doc


def save_design(doc: Any, path: str | os.PathLike[str]) -> Path:
    """Belgeyi ``.ork`` olarak kaydeder.

    :param doc: OpenRocket belgesi.
    :param path: hedef dosya yolu.
    :return: kaydedilen dosyanın :class:`~pathlib.Path` nesnesi.
    :raises DesignError: kaydedilemezse.
    """
    session = get_session()
    p = Path(path)
    if p.parent and not p.parent.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
    try:
        import jpype

        # Doğrudan GeneralRocketSaver kullanılır: `.ork` içine motorun thrust
        # curve'ünü (`thrustcurves/<digest>.rse`) de gömer. orlab helper'ı
        # bunu yapmadığı için dosya yeniden açıldığında motor kayboluyordu.
        saver = session.core.file.GeneralRocketSaver()
        opts = doc.getDefaultStorageOptions()
        opts.setSaveSimulationData(False)
        opts.setExplicitlySet(True)
        saver.save(jpype.java.io.File(str(p)), doc, opts)
    except Exception as e:
        raise DesignError(f"{p} kaydedilemedi: {e}") from e
    return p


def save_design_with_data(
    doc: Any, path: str | os.PathLike[str], *, flight_data: bool = True
) -> Path:
    """Belgeyi, OpenRocket'ın kendi uçuş verisiyle birlikte kaydeder.

    ``StorageOptions.setSaveSimulationData(True)`` ile ``.ork`` içine
    ``<flightdata>`` özeti yazılır; böylece dosya "OpenRocket'ın kendi
    sonucu" ile karşılaştırma (baseline) için kullanılabilir.

    :param doc: OpenRocket belgesi.
    :param path: hedef dosya yolu.
    :param flight_data: uçuş verisi kaydedilsin mi.
    :return: kaydedilen dosyanın :class:`~pathlib.Path` nesnesi.
    :raises DesignError: kaydedilemezse.
    """
    import jpype

    session = get_session()
    p = Path(path)
    if p.parent and not p.parent.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
    try:
        saver = session.core.file.GeneralRocketSaver()
        opts = doc.getDefaultStorageOptions()
        opts.setSaveSimulationData(bool(flight_data))
        opts.setExplicitlySet(True)
        saver.save(jpype.java.io.File(str(p)), doc, opts)
    except Exception as e:
        raise DesignError(f"{p} kaydedilemedi: {e}") from e
    return p


def copy_design(doc: Any) -> Any:
    """Belgenin bağımsız bir kopyasını döndürür.

    :param doc: OpenRocket belgesi.
    :return: kopyalanmış OpenRocket belgesi.
    :raises DesignError: kopyalanamazsa.
    """
    try:
        return doc.copy()
    except Exception as e:
        raise DesignError(f"Belge kopyalanamadı: {e}") from e


def new_design(
    name: str = "Rocket", *, stage_name: str = "Sustainer"
) -> Any:
    """Boş bir roket tasarımı (bir kademe) oluşturur.

    :param name: roket adı.
    :param stage_name: kademe adı.
    :return: yeni OpenRocket belgesi.
    :raises DesignError: oluşturulamazsa.
    """
    session = get_session()
    try:
        doc = session.core.document.OpenRocketDocumentFactory.createNewRocket()
        rocket = doc.getRocket()
        if name:
            rocket.setName(str(name))
        stage = rocket.getStage(0)
        if stage is not None and stage_name:
            stage.setName(str(stage_name))
        # Uçuş konfigürasyonu ilk simülasyon oluşturulurken kaydedilir
        # (bkz. rocketlib._common.ensure_simulation) — motor atamalarının
        # dosyada korunması için gereklidir.
    except Exception as e:
        raise DesignError(f"Yeni tasarım oluşturulamadı: {e}") from e
    return doc
