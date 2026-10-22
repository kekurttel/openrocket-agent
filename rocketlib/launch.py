"""Fırlatma koşulları ve motor atama.

Birimler: uzunluk **m**, hız **m/s**, açı **derece**, sıcaklık **K**,
basınç **Pa**, irtifa **m**. (Java API radyan bekler; dönüşüm burada yapılır.)

Örnek::

    rocketlib.set_launch_conditions(doc, rod_length=1.0, rod_angle=18.0, wind_speed=3.0)
    rocketlib.set_motor(doc, "C6", manufacturer="Estes")
"""

from __future__ import annotations

import math
import os
from typing import Any

from ._common import ensure_simulation
from .errors import DesignError, MotorError
from .session import get_session

__all__ = ["set_launch_conditions", "set_motor", "get_motor", "set_motor_ignition",
           "LAUNCH_CONDITION_FIELDS"]


def _check(name: str, value: Any, *, minimum: float | None = None,
           maximum: float | None = None, unit: str = "") -> float:
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


def set_launch_conditions(
    doc: Any,
    *,
    rod_length: float | None = 1.0,
    rod_angle: float | None = 18.0,
    wind_speed: float | None = 0.0,
    wind_turbulence: float | None = 0.1,
    launch_altitude: float | None = 0.0,
    temperature: float | None = None,
    pressure: float | None = None,
    launch_into_wind: bool | None = False,
    simulation_index: int = 0,
) -> dict[str, float]:
    """Fırlatma koşullarını ayarlar (rampa, rüzgâr, irtifa, atmosfer).

    ``None`` verilen bir koşul **değiştirilmez** (dosyadaki değer korunur).

    :param doc: OpenRocket belgesi.
    :param rod_length: rampa boyu (m).
    :param rod_angle: rampa açısı (**derece, yataydan**). Örn. 85° = neredeyse
        dikey. OpenRocket rampa açısını **düşeyden** saklar ve ±60° ile
        sınırlar; bu fonksiyon dönüşümü kendisi yapar. Bu nedenle yataydan
        30°'nin altındaki açılar OpenRocket'ta 30° olarak modellenir.
    :param wind_speed: rüzgâr hızı (m/s).
    :param wind_turbulence: rüzgâr türbülans şiddeti (oran, 0…1).
    :param launch_altitude: fırlatma irtifası (m).
    :param temperature: atmosfer sıcaklığı (K); None → değiştirilmez.
    :param pressure: atmosfer basıncı (Pa); None → değiştirilmez.
    :param launch_into_wind: rüzgâra dönük fırlatma (bool); None → değiştirilmez.
    :param simulation_index: hangi simülasyonun koşulları değiştirilecek.
    :return: uygulanan koşulların sözlüğü (SI).
    :raises DesignError: geçersiz girdi.
    """
    session = get_session()
    sim = ensure_simulation(doc, simulation_index)
    opts = sim.getOptions()

    applied: dict[str, float] = {}

    def apply(label: str, setter: str, value: Any) -> None:
        try:
            getattr(opts, setter)(value)
        except Exception as e:
            raise DesignError(f"Fırlatma koşulu ayarlanamadı ({label}): {e}") from e

    if rod_length is not None:
        rod_length = _check("rod_length", rod_length, minimum=0.0, unit="m")
        apply("rampa boyu", "setLaunchRodLength", rod_length)
        applied["rod_length_m"] = rod_length
    if rod_angle is not None:
        rod_angle = _check("rod_angle", rod_angle, minimum=0.0, maximum=90.0, unit="deg")
        # OpenRocket rampa açısını düşeyden ölçer (0° = dikey) ve 0…60° aralığına
        # kırpar. API'miz ise yataydan ölçer; bu yüzden 90° − açı gönderilir.
        apply("rampa açısı", "setLaunchRodAngle", math.radians(90.0 - rod_angle))
        applied["rod_angle_deg"] = rod_angle
    if wind_speed is not None:
        wind_speed = _check("wind_speed", wind_speed, minimum=0.0, unit="m/s")
        apply("rüzgâr hızı", "setWindSpeedAverage", wind_speed)
        applied["wind_speed_mps"] = wind_speed
    if wind_turbulence is not None:
        wind_turbulence = _check("wind_turbulence", wind_turbulence, minimum=0.0, unit="")
        apply("türbülans", "setWindTurbulenceIntensity", wind_turbulence)
        applied["wind_turbulence"] = wind_turbulence
    if launch_altitude is not None:
        launch_altitude = _check("launch_altitude", launch_altitude, unit="m")
        apply("fırlatma irtifası", "setLaunchAltitude", launch_altitude)
        applied["launch_altitude_m"] = launch_altitude
    if launch_into_wind is not None:
        apply("rüzgâra dönük", "setLaunchIntoWind", bool(launch_into_wind))
        applied["launch_into_wind"] = bool(launch_into_wind)

    if temperature is not None or pressure is not None:
        apply("ISA", "setISAAtmosphere", False)
        applied["isa_atmosphere"] = False
        if temperature is not None:
            t = _check("temperature", temperature, minimum=0.0, unit="K")
            apply("sıcaklık", "setLaunchTemperature", t)
            applied["temperature_K"] = t
        if pressure is not None:
            p = _check("pressure", pressure, minimum=0.0, unit="Pa")
            apply("basınç", "setLaunchPressure", p)
            applied["pressure_Pa"] = p

    _ = session
    return applied


LAUNCH_CONDITION_FIELDS = (
    "rod_length_m",
    "rod_angle_deg",
    "wind_speed_mps",
    "wind_turbulence",
    "launch_altitude_m",
    "temperature_K",
    "pressure_Pa",
)


def get_motor(doc: Any, *, simulation_index: int = 0, mount: Any | None = None) -> str | None:
    """Simülasyonun uçuş konfigürasyonundaki motorun tanımını döndürür.

    :param doc: OpenRocket belgesi.
    :param simulation_index: simülasyon indeksi.
    :param mount: belirli bir motor yuvası (Java nesnesi); None → otomatik.
    :return: motor tanımı (ör. ``"C6"``) veya None.
    """
    session = get_session()
    sim = ensure_simulation(doc, simulation_index)
    try:
        return session.helper.get_motor(sim, mount=mount)
    except Exception as e:
        raise MotorError(f"Motor okunamadı: {e}") from e


def set_motor(
    doc: Any,
    motor: str | os.PathLike[str] | None = None,
    *,
    designation: str | None = None,
    manufacturer: str | None = None,
    delay: float | None = None,
    simulation_index: int = 0,
    mount: Any | None = None,
) -> str:
    """Simülasyonun uçuş konfigürasyonuna motor atar.

    Motor, roketin *seçili* konfigürasyonuna değil **simülasyonun kendi uçuş
    konfigürasyonuna** atanır (aksi hâlde atama sessizce etkisiz kalır).

    :param doc: OpenRocket belgesi.
    :param motor: motor tanımı (ör. ``"C6"``) **veya** ``.eng``/``.rse``/``.zip``
        dosya yolu.
    :param designation: çoklu motorlu dosyada seçilecek motor (dosya yolu için).
    :param manufacturer: veritabanı aramasında üretici (ör. ``"Estes"``).
    :param delay: atma gecikmesi (s); None → korunur.
    :param simulation_index: simülasyon indeksi.
    :param mount: belirli bir motor yuvası (Java nesnesi); None → otomatik.
    :return: atanan motorun tanımı.
    :raises MotorError: motor bulunamazsa/atanamazsa.
    :raises DesignError: geçersiz girdi.
    """
    session = get_session()
    sim = ensure_simulation(doc, simulation_index)
    if motor is None:
        raise MotorError("Motor verilmedi (tanım veya .eng dosya yolu).")
    if delay is not None:
        delay = _check("delay", delay, minimum=0.0, unit="s")

    # Motor yuvası ve uçuş konfigürasyonuna bağlı motor kaydı hazırlanır.
    resolved_mount = _resolve_motor_mount(session, doc, sim, mount)
    _ensure_motor_config_registered(resolved_mount, sim.getFlightConfigurationId())

    try:
        session.helper.set_motor(
            sim,
            motor,
            mount=resolved_mount,
            manufacturer=manufacturer,
            designation=designation,
            delay=delay,
        )
    except ValueError as e:
        raise MotorError(str(e)) from e
    except Exception as e:
        raise MotorError(f"Motor atanamadı: {e}") from e
    _refresh_configurations(doc, sim)
    result = session.helper.get_motor(sim, mount=resolved_mount)
    return str(result) if result is not None else ""


def _resolve_motor_mount(session, doc, sim, mount=None):
    """Motor yuvasını belirler.

    :param session: aktif oturum.
    :param doc: OpenRocket belgesi.
    :param sim: simülasyon.
    :param mount: verilmiş yuva (Java nesnesi) ya da None.
    :return: ``MotorMount`` bileşeni.
    :raises MotorError: yuva bulunamazsa/ambiguous ise.
    """
    from .build import list_components

    if mount is not None:
        return mount
    interface = session.core.rocketcomponent.MotorMount
    candidates = [
        c for c in list_components(doc)
        if isinstance(c, interface) and c.isMotorMount()
    ]
    if not candidates:
        raise MotorError(
            "Bu rokette aktif motor yuvası yok (iç boru ekle: add_inner_tube(...))."
        )
    if len(candidates) == 1:
        return candidates[0]
    try:
        fcid = sim.getFlightConfigurationId()
        with_motor = [
            c for c in candidates
            if c.getMotorConfig(fcid) is not None
            and c.getMotorConfig(fcid).getMotor() is not None
        ]
    except Exception:
        with_motor = []
    if len(with_motor) == 1:
        return with_motor[0]
    names = sorted(str(c.getName()) for c in candidates)
    raise MotorError(
        f"Birden fazla motor yuvası var ({', '.join(names)}) — hangisinin kullanılacağını belirtin."
    )


def _ensure_motor_config_registered(mount, fcid) -> None:
    """Yuvanın motor ayarını verilen uçuş konfigürasyonuna **kaydeder**.

    OpenRocket'ta bir yuvanın motor ayarı, uçuş konfigürasyonu kimliği (FCID)
    altında kayıtlı olmalıdır. Kayıtlı değilse motor "varsayılan" ayara yazılır
    ve simülasyon kopyasında kaybolur ("No motors defined in the simulation").
    """
    try:
        registered = {str(i) for i in mount.getMotorConfigurationSet().getIds()}
        if str(fcid) in registered:
            return
        current = mount.getMotorConfig(fcid)
        if current is None:
            return
        cloned = current.copy(fcid)
        mount.setMotorConfig(cloned, fcid)
    except Exception:
        # Kayıt yapılamazsa orlab'ın atamasına devam et (var olan .ork dosyalarında
        # FCID zaten kayıtlıdır).
        pass


def _refresh_configurations(doc: Any, sim: Any) -> None:
    """Roketin uçuş konfigürasyonlarını yeniler.

    Motor ataması, konfigürasyonun "aktif motorlar" haritasını kendiliğinden
    güncellemez; bu harita OpenRocket'ta ``FlightConfiguration.update()``
    ile tazelenir. Yenilenmezse simülasyon "No motors defined in the simulation"
    diyerek başlar.
    """
    try:
        rocket = doc.getRocket()
        rocket.update()
    except Exception:
        pass
    try:
        fcid = sim.getFlightConfigurationId()
        config = doc.getRocket().getFlightConfiguration(fcid)
        if config is not None:
            config.update()
    except Exception:
        pass


_IGNITION_EVENTS = {
    "automatic": "AUTOMATIC",
    "launch": "LAUNCH",
    "ejection": "EJECTION_CHARGE",
    "ejection_charge": "EJECTION_CHARGE",
    "burnout": "BURNOUT",
    "never": "NEVER",
}


def set_motor_ignition(
    doc: Any,
    *,
    delay: float | None = None,
    event: str | None = None,
    simulation_index: int = 0,
    mount: Any | None = None,
) -> Any:
    """Motor ateşleme olayını ve/veya gecikmesini ayarlar.

    OpenRocket'ta motor ateşlemesi "ejection" (atma) ve "launch" (fırlatma)
    olaylarına bağlanabilir ya da tamamen kapatılabilir. Bu, yalnız iniş
    hızı ölçmek için kullanılan "serbest düşüş" simülasyonlarında gereklidir:
    paraşüt açılırken motorun itki üretmemesi gerekir (OpenRocket aksi
    hâlde "DEPLOY_UNDER_THRUST" ile simülasyonu iptal eder).

    :param doc: OpenRocket belgesi.
    :param delay: ateşleme gecikmesi (s); None → değiştirilmez.
    :param event: ``automatic``, ``launch``, ``ejection``, ``burnout`` veya
        ``never``; None → değiştirilmez.
    :param simulation_index: simülasyon indeksi.
    :param mount: motor yuvası (Java nesnesi); None → otomatik.
    :return: ilgili motor yuvası.
    :raises MotorError: yuva bulunamazsa/ambiguous ise.
    :raises DesignError: geçersiz olay.
    """
    session = get_session()
    sim = ensure_simulation(doc, simulation_index)
    resolved = _resolve_motor_mount(session, doc, sim, mount)
    fcid = sim.getFlightConfigurationId()

    def _config():
        try:
            cfg = resolved.getMotorConfig(fcid)
        except Exception:
            cfg = None
        if cfg is None:
            cfg = resolved.getDefaultMotorConfig()
        return cfg

    if event is not None:
        key = str(event).strip().lower()
        if key not in _IGNITION_EVENTS:
            raise DesignError(
                f"Bilinmeyen ateşleme olayı: {event!r}. "
                f"Geçerli: {', '.join(sorted(_IGNITION_EVENTS))}"
            )
        IgnitionEvent = session.core.motor.IgnitionEvent
        _config().setIgnitionEvent(getattr(IgnitionEvent, _IGNITION_EVENTS[key]))

    if delay is not None:
        delay = _check("delay", delay, minimum=0.0, unit="s")
        _config().setIgnitionDelay(float(delay))

    return resolved
