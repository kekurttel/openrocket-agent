---
name: openrocket-design
description: Design, simulate, and optimize rockets with OpenRocket 24.12 headless via rocketlib (Python). Use when the user asks to design a rocket, run an OpenRocket simulation, compute apogee/stability/rail-exit, optimize mass or aerodynamics, validate a design against a spec, or compare rocket configurations. Triggers on: "roket tasarla", "OpenRocket simülasyonu", "apogee hesapla", "stabilite", "rampa çıkışı", "paraşüt", "motor", ".ork dosyası", "design a rocket", "simulate rocket", "rocket optimization", "TEKNOFEST", "roket yarışması".
---

# OpenRocket Headless Roket Tasarım Skill'i

Bu skill, **OpenRocket 24.12**'yi arayüzden bağımsız (headless) çalıştıran bir
Python kütüphanesi (`rocketlib`) üstünde roket tasarımı yapmayı öğretir. Tüm
OpenRocket erişimi `rocketlib` üzerinden yapılır; ham Java/JPype çağrılmaz.

## Ne zaman kullanılır

- Kullanıcı roket tasarımı yapmak, simülasyon çalıştırmak veya optimize etmek
  istiyor.
- Kullanıcı bir `.ork` dosyasını incelemek, değiştirmek veya yeniden çalıştırmak
  istiyor.
- Kullanıcı bir şartnameye (ör. TEKNOFEST) göre tasarım doğrulaması istiyor.
- Kullanıcı roket tasarımlarını karşılaştırmak istiyor.

## Kurulum (ilk kez)

```bash
python3.12 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m orlab fetch
mkdir -p ~/.openrocket/ThrustCurves
cp designs/examples/*.eng ~/.openrocket/ThrustCurves/ 2>/dev/null
```

JDK 17+ gerekir. JVM bir kez başlar ve süreç boyunca yaşar (JPype kısıtı).

## Kişisel bilgi tabanı (wiki) — isteğe bağlı

Bu skill, **kişisel bir bilgi tabanı** ile birlikte gelmez. Kullanıcı kendi
tasarımlarını ve öğrenilen dersleri takip etmek isterse, kendi wiki'sini
oluşturabilir. Skill, kullanıcı kendi wiki'sini oluşturduğunda şu kuralları
uygular:

1. **Kullanıcının wiki'si varsa** (`wiki/index.md` veya `learn.md` mevcutsa):
   - Her tasarım oturumunun başında `wiki/hot.md` ve `wiki/index.md` oku.
   - Tasarım kararları verirken `wiki/concepts/` ve `wiki/sources/` sayfalarını danış.
   - Her iterasyondan sonra `wiki/log.md`'ye tek satır yaz.
   - `wiki/hot.md`'yi güncelle.

2. **Kullanıcının wiki'si yoksa**: wiki oluşturma teklif et (isteğe bağlı).
   Wiki oluşturma için `wiki` skill'i kullanılabilir.

3. **Kişisel veriler (tasarımlar, .ork dosyaları, wiki sayfaları) repoya
   push edilmemeli.** `.gitignore` dosyası bu verileri zaten hariç tutar.
   Kullanıcı kendi verisini kendi agent'ına sağlar.

## Kritik dersler (learn.md'den özet)

Bu skill, önceki tasarım süreçlerinden öğrenilen şu kritik dersleri içerir.
**Her tasarım oturumunun başında** bu dersleri hatırla:

1. **Rampa açısı:** OpenRocket rampa açısını düşeyden ölçer. `rod_angle=85`
   verin (kütüphane dönüşümü yapar). 85° yükseliş = 5° düşeyden.
2. **Paraşüt olayları:** `EJECTION` yerine `APOGEE`/`ALTITUDE` kullan.
   Motor gecikmesi 0 ise `EJECTION` = burnout anıdır.
3. **Motor kalıcılığı:** `.eng` dosyasını `~/.openrocket/ThrustCurves/` altına
   kopyala. OpenRocket 24.12 `.ork` içine thrust curve **gömmüyor**.
4. **Malzeme kontrolü:** `getMaterial().getDensity()` ile yoğunluğu kontrol et.
   "Ad" kozmetiktir, "yoğunluk" fiziktir.
5. **Kütle tabanı:** Motor + PAYLOAD zorunlu tabanı. 10.5–11.5 kg bandı
   ulaşılamaz (M1850 + 4 kg payload = 11.010 kg).
6. **Stabilite marjı:** 0.3 Mach stabilitesi en az 1.65–1.7 cal hedeflenmeli.
   Burnout stabilitesi 2.5–4.0 cal arasında tutulmalı.
7. **İki kademeli çözüm:** payload'ın bağımsız kurtarılması için gerekli.
8. **Paraşüt paketleme:** paraşüt çapı büyüdükçe paketleme hacmi artar.
9. **Yanma sırasında kütle değişimi:** CG öne kayar; stabilite artar. Kalkış ve
   burnout stabilitesi ayrı raporlanmalı.
10. **Determinizm:** rüzgâr 0, sabit seed.

**Yeni bir tasarım yaparken** `designs/examples/` altındaki örnek `.ork`
dosyalarını incele. Negatif örnekler (Ares, CAL Roket) neyin yapılmaması
gerektiğini gösterir. Kullanıcının kendi wiki'si varsa, oradaki negatif
örnekleri de incele.

## Birimler (SI)

| Büyüklük | Birim | Not |
|---|---|---|
| Uzunluk, yarıçap, çap | metre (m) | |
| Kütle | kilogram (kg) | |
| Hız | m/s | |
| Açı | **derece (°)** | Java API radyan bekler; dönüşüm kütüphane içinde |
| Stabilite marjı | kalibre (cal) | (CP−CG)/referans uzunluk |
| Rüzgâr hızı | m/s | |

## Temel iş akışı

```
1. OLUŞTUR   → new_design() veya load_design()
2. EKLE      → add_nose_cone, add_body_tube, add_fin_set, add_inner_tube,
               add_parachute, add_mass_component, ...
3. AYARLA    → set_component_material, set_surface_finish, set_parachute_deployment,
               set_nose_shoulder, set_component_position, set_motor, set_launch_conditions
4. DOĞRULA   → validate(doc, seed=1)  → hata varsa DUR
5. UÇUR      → run(doc, seed=1)       → metrikleri al
6. KARŞILAŞTIR → hedeflerle karşılaştır
7. GÜNLÜĞE YAZ → log.md'ye tek satır
8. KAYDET    → save_design(doc, path)
```

`validate()` hata veriyorsa tasarımı uçurma; önce hatayı çöz.

## Kritik konvansiyonlar

### 1. Rampa açısı (EN ÖNEMLİ HATA)

OpenRocket rampa açısını **düşeyden** ölçer (0° = tam dikey) ve ±60° ile
sınırlar. Bu kütüphanede `rod_angle` parametresi **yataydan yükseliş** açısıdır;
kütüphane dönüşümü kendisi yapar: `OpenRocket = 90° − rod_angle`.

| Yükseliş (yataydan) | OpenRocket (düşeyden) |
|---|---|
| 85° | 5° |
| 60° | 30° |
| 30° | 60° (OpenRocket üst sınırı) |
| < 30° | **modellenemez** (60°'ye kırpılır) |

**Yanlış:** `set_launch_conditions(rod_angle=85)` → OpenRocket 85° düşeyden →
60°'ye kırpılır → roket 30° yükselişle uçar (yanlış!).

**Doğru:** kütüphane zaten dönüşümü yapıyor; `rod_angle=85` verin, OpenRocket'a
5° düşeyden gönderilir.

### 2. Paraşüt açılma olayları

| Olay | Anlamı |
|---|---|
| `LAUNCH` | fırlatma anında |
| `EJECTION` | **motorun atma gecikmesi dolduğunda** (burnout + gecikme) |
| `APOGEE` | apogee olayında (+ `deploydelay` saniye) |
| `ALTITUDE` | verilen irtifada (+ `deploydelay`) |
| `NEVER` | hiç açılmaz |

**Kritik ayrım:** `EJECTION` bir zaman noktasıdır (motor gecikmesi), `APOGEE`
bir olaydır. Motorun atma gecikmesi 0 ise `EJECTION` = burnout anıdır.

```python
rocketlib.set_parachute_deployment(doc, "Birincil", event="apogee")
rocketlib.set_parachute_deployment(doc, "Ikincil", event="altitude", altitude=500.0)
rocketlib.set_parachute_deployment(doc, "Payload", event="apogee", delay=1.0)
```

### 3. Motor kalıcılığı

OpenRocket 24.12 `.ork` içine thrust curve **gömmüyor**. Motorun yeniden
yüklenmesi için `.eng` dosyası `~/.openrocket/ThrustCurves/` dizininde olmalı.
Yeni motor eğrisi kullanılacaksa **önce** bu dizine kopyalanmalı.

### 4. Determinizm

Sabit `seed` + `randomize_seed=False` aynı süreç içinde birebir aynı sonuç verir.
Rüzgâr açıkken 24.12'de rüzgâr modeli **süreç başına ek entropi** çektiği için
farklı süreçlerde sapma olur. Süreçler arası tekrarlanabilirlik için rüzgârı 0'a al.

### 5. Malzeme kontrolü

Her bileşenin `getMaterial()` ile yoğunluğu kontrol edilmeli. "Ad" kozmetiktir,
"yoğunluk" fiziktir. Örnek: "carbon" adlı bileşen gerçekte karton (680 kg/m³)
olabilir.

### 6. Kütle tabanı (M1850)

Motor 7.010 kg + PAYLOAD 4.000 kg = **11.010 kg zorunlu taban**. 10.5–11.5 kg
bandı ulaşılamaz; gerçekçi taban ~14–15 kg (M1850 için).

### 7. Stabilite marjı

- 0.3 Mach stabilitesi **en az 1.65–1.7 cal** hedeflenmeli (1.5 cal sınırına
  çok yakın değerler kabul edilmemeli).
- Min powered stabilite **≥ 1.5 cal** (tercihen ≥ 1.65 cal).
- Burnout stabilitesi **2.5–4.0 cal** arasında tutulmalı (aşırı stabilite
  weathercocking riski taşır).

### 8. İki kademeli çözüm

Payload'ın bağımsız kurtarılması (4.2.3, 4.3.3) için iki kademeli model gerekli.
Tek gövdeli modelde bu maddeler "MODELLENMEDİ" olarak işaretlenmeli.

### 9. Paraşüt paketleme

Paraşüt çapı büyüdükçe paketleme hacmi artar. Gövde uzunluğu paraşüt paketleme
hacmini hesaba katmalı (~0.2–0.3 m ek gövde uzunluğu).

### 10. Yanma sırasında kütle değişimi

Yanma sırasında CG öne kayar; stabilite artar. Kalkış stabilitesi ve burnout
stabilitesi ayrı raporlanmalı. Min powered stabilite (kalkış stabilitesi) ≥ 1.0 cal
(ideally ≥ 1.5 cal).

## Fonksiyon listesi (özet)

### Oturum
- `start_session(jar_path=None, log_level="ERROR")` — JVM + OpenRocket başlat
- `get_session()` — aktif oturumu döndür (yoksa başlat)
- `session_info()` — `{"started", "version", "profile_exact", "jvm_path", "jar_path"}`

### Dosya işlemleri
- `load_design(path)` — `.ork` yükle
- `save_design(doc, path)` — `.ork` kaydet (GeneralRocketSaver, motor korunur)
- `copy_design(doc)` — bağımsız kopya
- `new_design(name="Rocket", stage_name="Sustainer")` — boş roket + bir kademe

### İnceleme
- `inspect_design(doc)` — `{"rocket", "components", "simulations"}`
- `list_components(doc)` / `find_component(doc, name)` — bileşen listesi / ada göre arama

### Kurulum
- `add_nose_cone(doc, length, radius, shape="ogive", thickness, parent=None)`
- `add_body_tube(doc, length, radius, thickness=None, motor_mount=False, parent=None)`
- `add_transition(doc, length, fore_radius, aft_radius, shape="conical", parent=None)`
- `add_fin_set(doc, shape="trapezoidal", count, root_chord, tip_chord, height, sweep=45.0, thickness, position="bottom", parent=None)`
- `add_inner_tube(doc, length, radius, thickness=None, motor_mount=True, position="bottom", parent=None)`
- `add_mass_component(doc, length, radius, mass, position=None, parent=None)`
- `add_parachute(doc, diameter, line_count, line_length, cd=0.8, position="bottom", parent=None)`
- `add_shock_cord(doc, length, position="bottom", parent=None)`
- `update_component(doc, name, **params)` — alan güncelle
- `remove_component(doc, name)` — bileşen sil
- `set_component_material(doc, name, material_name=..., density=..., group="COMPOSITES")`
- `set_surface_finish(doc, name, "optimum"/"polished"/...)`
- `set_parachute_deployment(doc, name, event="apogee"/"altitude"/"ejection"/"never", altitude=500.0, delay=0.0)`
- `set_nose_shoulder(doc, name, length=...)`
- `set_component_position(doc, name, method="absolute", offset=0.0)`
- `set_motor_ignition(doc, event="launch"/"automatic"/"never", delay=0.0)`
- `add_stage(doc, "Booster")` — yeni kademe
- `move_component(doc, name, hedef_ad)` — bileşen taşı

### Fırlatma ve motor
- `set_launch_conditions(doc, rod_length=1.0, rod_angle=18.0, wind_speed=0.0, wind_turbulence=0.1, launch_altitude=0.0, temperature=None, pressure=None, launch_into_wind=False, simulation_index=0)`
- `set_motor(doc, motor, designation=None, manufacturer=None, delay=None, simulation_index=0, mount=None)`
- `get_motor(doc, simulation_index=0, mount=None)`

### Simülasyon ve doğrulama
- `run(doc, seed=None, simulation_index=0, branch=0)` — metrik sözlüğü
- `validate(doc, simulation_index=0, seed=None, run_simulation=True)` — uyarı/hata listesi

## Tasarım iterasyon döngüsü

```
1. DEĞİŞTİR   → add_/update_/remove_ ile tasarımı değiştir
2. DOĞRULA    → validate(doc, seed=1) → hata varsa DUR
3. UÇUR       → run(doc, seed=1) → metrikleri al
4. KARŞILAŞTIR → hedeflerle karşılaştır
5. GÜNLÜĞE YAZ → log.md'ye tek satır
6. KAYDET     → designs/iterations/ altına .ork kaydet
```

Maksimum 15 iterasyon. Hedefe ulaşılamazsa veya aynı hata 3 kez tekrarlarsa
DUR ve raporla.

## 0.3 Mach stabilitesi ölçümü

OpenRocket'ın `stability_at_launch_cal` değeri 0.3 Mach stabilitesini **vermeyebilir**.
Zaman serisinden oku:

```python
session = rocketlib.get_session()
sim = doc.getSimulation(0)
raw = session.helper.get_timeseries(
    sim, ["TYPE_TIME", "TYPE_MACH_NUMBER", "TYPE_STABILITY"], branch_number=0)
t = np.asarray(raw["TYPE_TIME"], float)
mach = np.asarray(raw["TYPE_MACH_NUMBER"], float)
stab = np.asarray(raw["TYPE_STABILITY"], float)
i = int(np.argmax(mach >= 0.3))
print(f"0.3 Mach: t={t[i]:.3f} s, Mach={mach[i]:.3f}, stability={stab[i]:.3f} cal")
```

## Kütle tabanı (M1850)

Motor 7.010 kg + PAYLOAD 4.000 kg = **11.010 kg zorunlu taban**. 10.5–11.5 kg
bandı ulaşılamaz; gerçekçi taban ~14–15 kg (M1850 için).

## Yaygın hatalar ve çözümleri

1. **Rampa açısı:** `rod_angle=85` verin (kütüphane dönüşümü yapar). 85° yükseliş
   = 5° düşeyden.
2. **Paraşüt olayları:** `EJECTION` yerine `APOGEE`/`ALTITUDE` kullan.
3. **Motor kaybı:** `.eng` dosyasını `~/.openrocket/ThrustCurves/` altına kopyala.
4. **Malzeme kontrolü:** `getMaterial().getDensity()` ile yoğunluğu kontrol et.
5. **Bileşke iniş hızı:** faz bazlı koşu yap; bileşke hız hiçbir maddeyi doğrulamaz.
6. **İki kademeli model:** payload'ın bağımsız kurtarılması için gerekli.
7. **Determinizm:** rüzgâr 0, sabit seed.
8. **Stabilite marjı:** 0.3 Mach stabilitesi en az 1.65–1.7 cal hedeflenmeli.
9. **Burnout stabilitesi:** 2.5–4.0 cal arasında tutulmalı.

## Testler

```bash
.venv/bin/python -m pytest -q   # 48-54 test geçmeli
```

## Referanslar

- `docs/api_notes.md` — doğrulanmış OpenRocket/orlab API notları
- `designs/examples/` — OpenRocket'ın örnek `.ork` dosyaları
- `third_party/openrocket/` — OpenRocket kaynak kodu (salt okunur)
- `learn.md` — öğrenilen dersler (hatalar, prensipler, şartname uyumu)
- `wiki/` — Obsidian uyumlu bilgi tabanı (14 tasarım, kavramlar, karşılaştırmalar)
EOF
echo "SKILL.md güncellendi"