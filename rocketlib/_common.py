"""rocketlib içinde ortak kullanılan yardımcılar."""

from __future__ import annotations

from typing import Any

from .errors import SimulationError

__all__ = ["ensure_simulation"]


def ensure_simulation(doc: Any, index: int = 0):
    """Belgede simülasyon varsa onu, yoksa oluşturup ekler.

    Oluşturulan/var olan simülasyonun uçuş konfigürasyonu (FCID) roketin
    konfigürasyon kümesine **kaydedilir**; aksi hâlde motor atamaları
    kaydedilen .ork dosyasında kaybolur (OpenRocket yalnız kayıtlı
    konfigürasyonların motor ayarlarını yazar).

    :param doc: OpenRocket belgesi.
    :param index: hedef simülasyon indeksi.
    :return: ``Simulation`` nesnesi.
    :raises SimulationError: simülasyon oluşturulamazsa.
    """
    session = _session_or_fail()
    count = int(doc.getSimulationCount())
    if count == 0:
        try:
            sim = session.core.document.Simulation(doc, doc.getRocket())
            doc.addSimulation(sim)
        except Exception as e:
            raise SimulationError(f"Simülasyon oluşturulamadı: {e}") from e
        count = int(doc.getSimulationCount())
    if not 0 <= index < count:
        raise SimulationError(
            f"Simülasyon indeksi {index} geçersiz (belgede {count} simülasyon var)."
        )
    sim = doc.getSimulation(index)
    _register_flight_configuration(doc, sim)
    return sim


def _register_flight_configuration(doc: Any, sim: Any) -> None:
    """Simülasyonun uçuş konfigürasyonunu roketin konfigürasyon kümesine yazar.

    Kayıtlı değilse yeni (tüm kademeleri aktif) bir konfigürasyon üretilir ve
    simülasyona atanır — böylece motor atamaları dosyaya yazılabilir hâle gelir.
    """
    try:
        rocket = doc.getRocket()
        fcid = sim.getFlightConfigurationId()
        known = {str(i) for i in rocket.getIds()}
        if str(fcid) in known:
            return
        config = rocket.createFlightConfiguration(None)
        config.setAllStages()
        sim.setFlightConfigurationId(config.getFlightConfigurationID())
    except Exception:
        # Kayıt başarısız olursa motor ataması kaybolabilir; ama işlemi bozma.
        pass


def _session_or_fail():
    from .session import get_session

    return get_session()
