# OpenRocket Agent — Headless Roket Tasarım Kütüphanesi

**OpenRocket 24.12**'yi arayüzden bağımsız (headless) çalıştıran bir Python
kütüphanesi (`rocketlib`) ve bu kütüphaneyi kullanan bir **agent skill**'i.
TEKNOFEST 2026 roket yarışması tasarımlarında doğrulandı.

> Bu repo iki şey içerir: (1) `rocketlib` Python kütüphanesi, (2) bir AI
> agent'ın bu kütüphaneyi kullanarak roket tasarımı yapmasını öğreten
> `SKILL.md`.

## Gereksinimler

- Python 3.10+ (3.12 önerilir)
- JDK 17+ (`JAVA_HOME` veya `/usr/lib/jvm/java-17-openjdk`)
- Ağ erişimi (ilk kurulumda OpenRocket jar'ı indirilir)

## Kurulum

```bash
git clone https://github.com/<kullanici>/openrocket-agent.git
cd openrocket-agent

python3.12 -m venv .venv
.venv/bin/pip install -r requirements.txt

# OpenRocket 24.12 jar'ını indir ve doğrula (sha256 sabitlenmiş)
.venv/bin/python -m orlab fetch
.venv/bin/python -m orlab which

# Motor eğrilerini kullanıcı motor dizinine kur (zorunlu!)
mkdir -p ~/.openrocket/ThrustCurves
cp designs/examples/*.eng ~/.openrocket/ThrustCurves/ 2>/dev/null
# veya kendi .eng dosyalarınızı buraya kopyalayın

# Testleri çalıştır
.venv/bin/python -m pytest -q
```

`rocketlib` JVM yolunu otomatik bulur (`ROCKETLIB_JVM` → `JAVA_HOME` →
`/usr/lib/jvm/java-17-openjdk` → `/usr/lib/jvm/java-21-openjdk`).

## Hızlı başlangıç

```python
import rocketlib

doc = rocketlib.new_design("Mini")
rocketlib.add_nose_cone(doc, length=0.08, radius=0.012, thickness=0.003)
rocketlib.add_body_tube(doc, length=0.32, radius=0.012, thickness=0.0008)
rocketlib.add_fin_set(doc, count=3, root_chord=0.075, tip_chord=0.075,
                      height=0.065, sweep=40.0, thickness=0.0006)
rocketlib.add_inner_tube(doc, length=0.07, radius=0.0105, thickness=0.0008)
rocketlib.add_parachute(doc, diameter=0.25)
rocketlib.set_motor(doc, "C6", manufacturer="Estes", delay=5.0)
rocketlib.set_launch_conditions(doc, rod_length=1.0, rod_angle=15.0, wind_speed=3.0)

m = rocketlib.run(doc, seed=1)
print(m["apogee_m"], m["stability_at_launch_cal"], m["landing_velocity_mps"])
for issue in rocketlib.validate(doc, seed=1):
    print(issue["severity"], issue["code"], issue["message"])
```

## Agent skill olarak kullanım

Bu repodaki `SKILL.md` dosyasını AI agent'ınızın skills dizinine kopyalayın:

```bash
# Claude Code
cp SKILL.md ~/.claude/skills/openrocket-design/SKILL.md

# OpenCode
cp SKILL.md ~/.config/opencode/skills/openrocket-design/SKILL.md
```

Agent'a "roket tasarla", "OpenRocket simülasyonu çalıştır", "apogee hesapla"
gibi komutlar verildiğinde skill otomatik tetiklenir.

## Birimler (SI)

| Büyüklük | Birim | Not |
|---|---|---|
| Uzunluk, yarıçap, çap | metre (m) | |
| Kütle | kilogram (kg) | |
| Hız | m/s | |
| Açı | **derece (°)** | Java API radyan bekler; dönüşüm kütüphane içinde |
| Stabilite marjı | kalibre (cal) | (CP−CG)/referans uzunluk |
| Rüzgâr hızı | m/s | |

## Kritik konvansiyonlar

1. **Rampa açısı:** `rod_angle` parametresi **yataydan yükseliş** açısıdır.
   OpenRocket rampa açısını **düşeyden** ölçer; kütüphane dönüşümü kendisi yapar.
   85° yükseliş → OpenRocket'a 5° düşeyden.
2. **Paraşüt olayları:** `EJECTION` motorun atma gecikmesidir (gecikme 0 ise
   burnout anı). Doğru olaylar: `APOGEE` (+delay), `ALTITUDE` (irtifa).
3. **Motor kalıcılığı:** OpenRocket 24.12 `.ork` içine thrust curve **gömmüyor**.
   Motorun yeniden yüklenmesi için `.eng` dosyası `~/.openrocket/ThrustCurves/`
   dizininde olmalı.
4. **Determinizm:** sabit `seed` + `randomize_seed=False` aynı süreç içinde
   birebir aynı sonuç verir.

## Lisans

MIT. OpenRocket (GPL) ve orlab (MIT) bağımlılıkları kendi lisanslarıyla gelir.
EOF
echo "README yazıldı"