#!/usr/bin/env python3
"""sim.py — OpenRocket tasarımları için headless komut satırı aracı.

Alt komutlar:
    inspect  <dosya.ork>                      tasarımı JSON olarak dök
    run      <dosya.ork> [seçenekler]         simülasyonu çalıştır, metrikleri JSON olarak bas
    validate <dosya.ork>                      tasarımı doğrula, uyarı/hata listesini JSON olarak bas
    set      <dosya.ork> <bileşen> alan=değer  bileşen parametresini değiştir ve kaydet

Çıktı **her zaman** stdout'a tek bir JSON nesnesi olarak yazılır; loglar ve uyarılar
stderr'e gider. Hata durumunda stdout'a ``{"ok": false, "error": "..."}`` yazılır ve
program sıfırdan farklı bir çıkış koduyla sonlanır (2 = hata, 3 = doğrulama hatası).

Örnekler:
    python sim.py inspect designs/examples/simple_model.ork
    python sim.py run designs/examples/simple_model.ork --wind 3 --rod 1.0 --angle 18 --seed 1
    python sim.py validate designs/examples/simple_model.ork
    python sim.py set designs/examples/simple_model.ork "Body tube" length=0.25 radius=0.019
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

EXIT_OK = 0
EXIT_ERROR = 2
EXIT_VALIDATION = 3


def _emit(payload: dict) -> None:
    """Sonucu stdout'a tek JSON nesnesi olarak yazar."""
    sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False))
    sys.stdout.write("\n")
    sys.stdout.flush()


def _fail(message: str, code: int = EXIT_ERROR) -> int:
    _emit({"ok": False, "error": message})
    return code


def _setup_logging() -> None:
    """Logları stderr'e yönlendirir (stdout yalnız JSON için)."""
    logging.basicConfig(
        stream=sys.stderr,
        level=logging.WARNING,
        format="%(levelname)s %(name)s: %(message)s",
    )


def _parse_value(raw: str):
    """``alan=değer`` metnini Python değerine çevirir (int/float/bool/str)."""
    text = raw.strip()
    low = text.lower()
    if low in ("true", "yes", "evet"):
        return True
    if low in ("false", "no", "hayir", "hayır"):
        return False
    try:
        return int(text)
    except ValueError:
        pass
    try:
        return float(text)
    except ValueError:
        pass
    return text


def cmd_inspect(args: argparse.Namespace) -> int:
    import rocketlib

    doc = rocketlib.load_design(args.file)
    info = rocketlib.inspect_design(doc)
    _emit({"ok": True, "command": "inspect", "design": info})
    return EXIT_OK


def cmd_run(args: argparse.Namespace) -> int:
    import rocketlib

    doc = rocketlib.load_design(args.file)

    if args.motor or args.motor_file:
        motor = args.motor_file or args.motor
        rocketlib.set_motor(
            doc, motor, manufacturer=args.manufacturer, delay=args.delay,
            simulation_index=args.simulation,
        )

    launch = rocketlib.set_launch_conditions(
        doc,
        rod_length=args.rod,
        rod_angle=args.angle,
        wind_speed=args.wind,
        wind_turbulence=args.turbulence,
        launch_altitude=args.altitude,
        simulation_index=args.simulation,
    )
    metrics = rocketlib.run(
        doc, seed=args.seed, simulation_index=args.simulation, branch=args.branch
    )
    _emit(
        {
            "ok": True,
            "command": "run",
            "file": str(args.file),
            "launch_conditions": launch,
            "metrics": metrics,
        }
    )
    return EXIT_OK


def cmd_validate(args: argparse.Namespace) -> int:
    import rocketlib

    doc = rocketlib.load_design(args.file)
    issues = rocketlib.validate(doc, seed=args.seed, simulation_index=args.simulation)
    errors = [i for i in issues if i["severity"] == "error"]
    warnings = [i for i in issues if i["severity"] == "warning"]
    payload = {
        "ok": not errors,
        "command": "validate",
        "file": str(args.file),
        "issues": issues,
        "error_count": len(errors),
        "warning_count": len(warnings),
    }
    _emit(payload)
    return EXIT_OK if not errors else EXIT_VALIDATION


def cmd_set(args: argparse.Namespace) -> int:
    import rocketlib

    doc = rocketlib.load_design(args.file)
    params = {}
    for item in args.fields:
        if "=" not in item:
            raise ValueError(f"alan=değer biçiminde olmalı: {item!r}")
        key, _, raw = item.partition("=")
        params[key.strip()] = _parse_value(raw)

    rocketlib.update_component(doc, args.component, **params)
    path = rocketlib.save_design(doc, args.output or args.file)
    info = rocketlib.inspect_design(doc)
    _emit(
        {
            "ok": True,
            "command": "set",
            "file": str(path),
            "component": args.component,
            "updated": params,
            "design": info,
        }
    )
    return EXIT_OK


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sim.py",
        description="OpenRocket .ork tasarımları için headless araç (JSON çıktılı).",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_inspect = sub.add_parser("inspect", help="tasarımı JSON olarak dök")
    p_inspect.add_argument("file", help=".ork dosyası")
    p_inspect.set_defaults(func=cmd_inspect)

    p_run = sub.add_parser("run", help="simülasyonu çalıştır")
    p_run.add_argument("file", help=".ork dosyası")
    p_run.add_argument("--wind", type=float, default=None, metavar="M/S",
                       help="rüzgâr hızı (m/s)")
    p_run.add_argument("--rod", type=float, default=None, metavar="METRE",
                       help="rampa boyu (m)")
    p_run.add_argument("--angle", type=float, default=None, metavar="DERECE",
                       help="rampa açısı (derece)")
    p_run.add_argument("--turbulence", type=float, default=None, metavar="ORAN",
                       help="rüzgâr türbülans şiddeti (0-1)")
    p_run.add_argument("--altitude", type=float, default=None, metavar="METRE",
                       help="fırlatma irtifası (m)")
    p_run.add_argument("--seed", type=int, default=None, metavar="N",
                       help="sabit rastgelelik tohumu")
    p_run.add_argument("--motor", default=None, metavar="TANIM",
                       help="kullanılacak motor (ör. C6)")
    p_run.add_argument("--manufacturer", default=None, metavar="ÜRETİCİ",
                       help="motor üreticisi (ör. Estes)")
    p_run.add_argument("--motor-file", default=None, metavar="DOSYA",
                       help="motor dosyası (.eng/.rse)")
    p_run.add_argument("--delay", type=float, default=None, metavar="SANIYE",
                       help="motor atma gecikmesi (s)")
    p_run.add_argument("--simulation", type=int, default=0, metavar="N",
                       help="simülasyon indeksi")
    p_run.add_argument("--branch", type=int, default=0, metavar="N",
                       help="kademe kolu (0 = ana kademe)")
    p_run.set_defaults(func=cmd_run)

    p_validate = sub.add_parser("validate", help="tasarımı doğrula")
    p_validate.add_argument("file", help=".ork dosyası")
    p_validate.add_argument("--seed", type=int, default=None, metavar="N",
                             help="sabit rastgelelik tohumu")
    p_validate.add_argument("--simulation", type=int, default=0, metavar="N",
                             help="simülasyon indeksi")
    p_validate.set_defaults(func=cmd_validate)

    p_set = sub.add_parser("set", help="bileşen parametresini değiştir ve kaydet")
    p_set.add_argument("file", help=".ork dosyası")
    p_set.add_argument("component", help="bileşen adı")
    p_set.add_argument("fields", nargs="+", metavar="alan=değer",
                       help="değiştirilecek alanlar (ör. length=0.25)")
    p_set.add_argument("-o", "--output", default=None, metavar="DOSYA",
                       help="kaydedilecek dosya (varsayılan: girdi dosyası)")
    p_set.set_defaults(func=cmd_set)

    return parser


def main(argv: list[str] | None = None) -> int:
    _setup_logging()
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as e:
        import rocketlib

        if isinstance(e, rocketlib.RocketLibError):
            return _fail(f"{type(e).__name__}: {e}")
        return _fail(f"{type(e).__name__}: {e}")


if __name__ == "__main__":
    sys.exit(main())
