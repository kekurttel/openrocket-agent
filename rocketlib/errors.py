"""rocketlib hataları.

Tüm kütüphane hataları :class:`RocketLibError` türevleridir; çağıran taraf
tek bir ``except RocketLibError`` ile yakalayabilir.
"""

__all__ = [
    "RocketLibError",
    "SessionError",
    "DesignError",
    "ComponentNotFoundError",
    "DuplicateComponentError",
    "MotorError",
    "SimulationError",
    "ValidationError",
]


class RocketLibError(Exception):
    """rocketlib hatalarının taban sınıfı."""


class SessionError(RocketLibError):
    """OpenRocket oturumu (JVM) kurulamadı ya da kullanılamaz durumda."""


class DesignError(RocketLibError):
    """Geçersiz tasarım girdisi (negatif boyut, bilinmeyen alan, ...)."""


class ComponentNotFoundError(DesignError):
    """Adı verilen bileşen bulunamadı."""


class DuplicateComponentError(DesignError):
    """Aynı adda sahip bileşen zaten var."""


class MotorError(RocketLibError):
    """Motor bulunamadı, okunamadı veya atanamadı."""


class SimulationError(RocketLibError):
    """Simülasyon çalıştırılamadı veya sonuçları okunamadı."""


class ValidationError(RocketLibError):
    """Doğrulama işlemi tamamlanamadı."""
