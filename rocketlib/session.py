"""OpenRocket oturumu (JVM) yönetimi.

JPype bir süreçte yalnızca **bir** JVM başlatabilir; bu yüzden kütüphane
tek bir oturum tutar. ``get_session()`` ilk çağrıda JVM'i (ve OpenRocket'ı)
başlatır, sonraki çağrılarda aynı oturumu döndürür.

Birimler: bu modül JVM yolu/jar yolu gibi işletim sistemi yolları dışında
SI dışı değer üretmez.
"""

from __future__ import annotations

import logging
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .errors import SessionError

__all__ = [
    "Session",
    "get_session",
    "start_session",
    "session_info",
    "LOGBACK_CONFIG",
]

logger = logging.getLogger(__name__)

_LOGBACK_CONFIG = Path(__file__).with_name("logback-stderr.xml")

# OpenRocket 24.12 JDK 17+ ister; sistemdeki JDK'ları tercih sırasıyla dene.
_JVM_CANDIDATES = (
    "/usr/lib/jvm/java-17-openjdk",
    "/usr/lib/jvm/java-21-openjdk",
    "/usr/lib/jvm/java-11-openjdk",
    "/usr/lib/jvm/default",
)


def _detect_jvm_path() -> str | None:
    """Kullanılacak libjvm.so yolunu bulur; bulunamazsa None (JPype'ın
    otomatik seçimine bırakılır).

    Sıra: ``ROCKETLIB_JVM`` → ``JAVA_HOME`` → bilinen JDK dizinleri → None.
    """
    env = os.environ.get("ROCKETLIB_JVM")
    if env:
        return env
    java_home = os.environ.get("JAVA_HOME")
    if java_home:
        candidate = Path(java_home) / "lib" / "server" / "libjvm.so"
        if candidate.exists():
            return str(candidate)
    for base in _JVM_CANDIDATES:
        candidate = Path(base) / "lib" / "server" / "libjvm.so"
        if candidate.exists():
            return str(candidate)
    return None


@dataclass
class Session:
    """Çalışan OpenRocket oturumu.

    :ivar instance: orlab ``OpenRocketInstance`` (JVM + OpenRocket çekirdeği).
    :ivar helper: orlab ``Helper`` (yükle/kaydet/simülasyon yardımcıları).
    :ivar core: ``info.openrocket.core`` JPackage'i.
    """

    instance: Any
    helper: Any
    core: Any

    @property
    def version(self) -> str:
        """Yüklü OpenRocket sürümü (ör. ``"24.12"``)."""
        return str(self.instance.or_version)

    @property
    def profile_exact(self) -> bool:
        """orlab'ın bu sürüm için birebir profili var mı."""
        return bool(self.instance.profile_exact)

    def component_class(self, name: str):
        """``info.openrocket.core.rocketcomponent.<name>`` sınıfını döndürür.

        :param name: Java sınıf adı (ör. ``"BodyTube"``).
        :raises SessionError: sınıf yoksa.
        """
        cls = getattr(self.core.rocketcomponent, name, None)
        if cls is None:
            raise SessionError(f"OpenRocket {self.version} içinde bileşen sınıfı yok: {name}")
        return cls

    def transition_shape(self, shape: str):
        """``Transition.Shape`` enum değerini isimden çözer (ogive/conical/…).

        :param shape: şekil adı (büyük/küçük harf duyarsız).
        :raises SessionError: bilinmeyen şekil.
        """
        shapes = self.core.rocketcomponent.Transition.Shape
        for candidate in shapes.class_.getEnumConstants():
            if str(candidate.name()).lower() == str(shape).lower():
                return candidate
        raise SessionError(
            f"Bilinmeyen geçiş şekli: {shape!r} "
            f"(seçenekler: {', '.join(str(c.name()) for c in shapes.class_.getEnumConstants())})"
        )


_session: Session | None = None


def start_session(
    jar_path: str | os.PathLike[str] | None = None,
    *,
    log_level: str = "ERROR",
    jvm_args: tuple[str, ...] | None = None,
    force_restart: bool = False,
) -> Session:
    """JVM'i ve OpenRocket'ı başlatır, oturumu döndürür.

    Aynı süreçte zaten bir oturum varsa onu döndürür (``force_restart=True``
    ise yeni oturum başlatılamaz — JPype JVM'i yeniden başlatamaz; bu durumda
    :class:`~rocketlib.errors.SessionError` fırlatılır).

    :param jar_path: OpenRocket jar yolu. Verilmezse orlab'ın çözüm sırası
        kullanılır (``ORLAB_JAR`` → ``CLASSPATH`` → çalışma dizini → orlab cache).
    :param log_level: OpenRocket log düzeyi (OFF/ERROR/WARN/INFO/DEBUG/TRACE/ALL).
    :param jvm_args: JVM'e ek argümanlar (ör. ``("-Xmx4g",)``).
    :param force_restart: yalnızca hata mesajı üretmek için kullanılır.
    :raises SessionError: JVM başlatılamazsa.
    """
    global _session
    if _session is not None and not force_restart:
        return _session
    if _session is not None and force_restart:
        raise SessionError(
            "Bu süreçte zaten bir OpenRocket oturumu çalışıyor; JPype JVM'i "
            "yeniden başlatamaz. Yeni bir süreç başlatın."
        )

    try:
        from orlab import Helper, OpenRocketInstance
    except ImportError as e:  # pragma: no cover
        raise SessionError(
            "orlab kurulu değil. `python -m pip install orlab` ve "
            "`python -m orlab fetch` çalıştırın."
        ) from e

    args = list(jvm_args or ())
    # OpenRocket loglarını stdout'a yazmasın: CLI'da JSON saflığı için stderr'a yönlendir.
    if _LOGBACK_CONFIG.exists() and not any(
        a.startswith("-Dlogback.configurationFile=") for a in args
    ):
        args.append(f"-Dlogback.configurationFile={_LOGBACK_CONFIG}")

    jvm_path = _detect_jvm_path()
    try:
        instance = OpenRocketInstance(
            jar_path=None if jar_path is None else str(jar_path),
            log_level=log_level,
            jvm_path=jvm_path,
            jvm_args=tuple(args),
        )
        instance.__enter__()
    except Exception as e:
        raise SessionError(f"OpenRocket oturumu başlatılamadı: {e}") from e

    helper = Helper(instance)
    _session = Session(instance=instance, helper=helper, core=instance.openrocket)
    logger.info(
        "OpenRocket %s oturumu başlatıldı (jvm=%s)", _session.version, jvm_path
    )
    return _session


def get_session() -> Session:
    """Aktif oturumu döndürür; yoksa başlatır.

    :raises SessionError: oturum kurulamazsa.
    """
    if _session is None:
        return start_session()
    return _session


def session_info() -> dict[str, Any]:
    """Oturum durumu hakkında bilgi (JSON'a uygun sözlük).

    :return: ``{"started": bool, "version": str|None, "profile_exact": bool,
        "jvm_path": str|None, "jar_path": str|None}``
    """
    if _session is None:
        return {
            "started": False,
            "version": None,
            "profile_exact": False,
            "jvm_path": _detect_jvm_path(),
            "jar_path": None,
        }
    return {
        "started": True,
        "version": _session.version,
        "profile_exact": _session.profile_exact,
        "jvm_path": _detect_jvm_path(),
        "jar_path": str(_session.instance.jar_path),
    }


def _ensure_stdout_clean() -> None:
    """JVM'in stdout'a yazdığı her şeyi stderr'a yönlendirir.

    JVM çalışırken uygulanabilir; ``start_session`` içinde logback yapılandırması
    ile de desteklenir. Bu fonksiyon, JVM başladıktan **sonra** Java'nın
    ``System.out`` akışını değiştirir.
    """
    try:
        import jpype
    except ImportError:  # pragma: no cover
        return
    if not jpype.isJVMStarted():
        return
    java_io = jpype.JPackage("java").io
    err = java_io.PrintStream(java_io.FileOutputStream(sys.stderr.fileno()), True)
    java_lang = jpype.JPackage("java").lang
    java_lang.System.setOut(err)
