# OpenRocket 24.12 + orlab API notları

Bu dosyadaki her snippet **çalıştırıldı ve doğrulandı** (bkz. `scratch/api_*.py`).
Kaynak: `third_party/openrocket/core/src/main/java/info/openrocket/core/` (klonlanmış repo, salt referans).

## 0. Genel bilgiler (önce oku)

**Paket kökleri.** OpenRocket 24.12, `net.sf.openrocket` paketini `info.openrocket.core` +
`info.openrocket.swing` olarak yeniden adlandırdı. orlab profil dosyası bunu doğru verir:

```python
from orlab import OpenRocketInstance
with OpenRocketInstance() as inst:
    core = inst.openrocket          # info.openrocket.core  (JPackage)
    swing = inst.openrocket_swing   # info.openrocket.swing
    print(inst.or_version, inst.profile.version_string, inst.profile_exact)
# 24.12 24.12 True
```

**Tek JVM kuralı.** JPype bir süreçte yalnız bir JVM başlatabilir. `with OpenRocketInstance(...)`
blokları aynı jar ile tekrar kullanılabilir; farklı jar → `OrlabError`. Bu yüzden kütüphane
tek bir "oturum" yönetir.

**JAR, klondan daha eski olabilir.** `third_party/openrocket` klonu release-24.12 dalının
**uç** commit'ini içerir (591c5e5); yayınlanan 24.12 jar'ı daha eski bir commit'ten
derlenmiş olabilir. İki örnek:
- jar'da `MaterialGroup.THREADS_LINES` var, klonda `NYLONS/ELASTICS/KEVLARS` var.
- jar'da `SimulationOptions.setRandomSeedFixed()` **yok**; klonda var.
→ **Doğrulama daima çalışan jar'a karşı yapılır**, klon yalnız kod okumak içindir.

**Birimler.** OpenRocket iç birimler SI'dır: m, kg, s, K, Pa, N. Tek istisna: **açılar
radyan** (`setLaunchRodAngle`, `setSweepAngle`, `setCantAngle`, `setWindDirection`,
`setLaunchRodDirection`). Kütüphane (rocketlib) dışarıdan **derece** kabul eder ve
kendi içinde radyana çevirir.

**stdout uyarısı.** OpenRocket'in logback logları varsayılan olarak **stdout'a** yazılır
(startup sırasında "Loading motors from file..." gibi satırlar). JSON çıktı istenen
CLI'larda bu ayrıca ele alınır (bkz. Faz 5 notu).

---

## a) .ork yükleme ve kaydetme

```python
from orlab import Helper, OpenRocketInstance

with OpenRocketInstance() as inst:
    helper = Helper(inst)
    doc = helper.load_doc("designs/examples/simple_model.ork")   # → OpenRocketDocument
    rocket = doc.getRocket()
    doc.getSimulationCount()      # 5
    doc.getSimulation(0)          # Simulation
```

Kaydetme (orlab sarmalayıcısı):

```python
helper.save_doc("out.ork", doc)
```

Kaydetme (OpenRocket'ın kendi `GeneralRocketSaver`'ı + `StorageOptions`):

```python
saver = inst.openrocket.file.GeneralRocketSaver()
opts = doc.getDefaultStorageOptions()
opts.setSaveSimulationData(True)     # ← .ork içine <flightdata> yaz
opts.setExplicitlySet(True)
saver.save(jpype.java.io.File("out.ork"), doc, opts)
```

**Doğrulama (yükle → kaydet → yeniden yükle → karşılaştır):** 13 bileşen → 13 bileşen,
isimler birebir aynı, toplam uzunluk 0.4254 m → 0.4254 m (fark < 1e-9),
simülasyon sayısı 5 → 5.

**Kayıtlı simülasyon verisi (baseline için):** `setSaveSimulationData(True)` ile kaydedilen
dosyada `<flightdata maxaltitude="50.59" maxvelocity="29.249" ...>` etiketleri bulunur.
Bu değerler OpenRocket'ın **kendi** hesapladığı sonuçlardır → Phase 6 karşılaştırması için
kullanılabilir. Repodaki örnek .ork dosyalarında da bu özetler **mevcuttur** (ilk kontrol
`<flightdata>` etiketini yanlış aradığım için 0 görünmüştü).

---

## b) Bileşen ağacını gezme

```python
from orlab import JIterator

for comp in JIterator(rocket):          # iterator(true) → tüm alt ağaç, kendisi dahil
    print(comp.getName(), comp.getClass().getSimpleName(),
          comp.getLength(), comp.getComponentMass())
```

Yardımcılar (orlab `Helper`):

```python
helper.get_all_components(rocket)                     # tüm bileşenler (list)
helper.get_component_named(rocket, "Body tube")       # ValueError yoksa
helper.get_components_of_type(rocket, "BodyTube")      # sınıf adı veya JClass
```

Ağaç derinliği için `comp.getParent()` zinciri kullanılabilir (her `getParent()` bir üst
düğüm).

Örnek ağaç (simple_model.ork):

```
'A simple model rocket' [Rocket]
  'Sustainer' [AxialStage]
    'Nose cone' [NoseCone]        length=0.1000  mass=0.013156
    'Body tube' [BodyTube]        length=0.3000  mass=0.015381
      'Parachute' [Parachute]          length=0.0420  mass=0.007976
      'Shock cord' [ShockCord]          length=0.0520  mass=0.000720
      'Wadding' [MassComponent]         length=0.0300  mass=0.002000
      'Launch lug' [LaunchLug]          length=0.0350  mass=0.000449
      'Trapezoidal fin set' [TrapezoidFinSet] length=0.0508 mass=0.006156
      'Centering ring' [CenteringRing]  ...
      'Inner Tube' [InnerTube]          length=0.0750  mass=0.001482
        'Engine block' [EngineBlock]    length=0.0050  mass=0.000481
```

**Yapı kuralı:** gövde bileşenleri (`NoseCone`, `BodyTube`, `Transition`) **stage'in
çocuklarıdır** (birbirinin alt çocuğu olamazlar); kanatçık, paraşüt, iç boru, kütle
bileşeni ise `BodyTube`'nun çocuklarıdır.

---

## c) Bileşen ekleme (sıfırdan)

Sıfırdan belge:

```python
doc = inst.openrocket.document.OpenRocketDocumentFactory.createNewRocket()  # public statik
rocket = doc.getRocket()
rocket.setName("Test roketi")
stage = rocket.getStage(0)          # 'Sustainer' (AxialStage)
```

Ekleme (`addChild` iki argümanlı sürüm JPype'da belirsiz: `addChild(comp,int)` ile
`addChild(comp,boolean)` → Python int her ikisine de uyuyor). Üç argümanlı tek overload
kullanılır:

```python
parent.addChild(comp, index, True)   # index: 0 = başa ekle
```

**Doğrulanmış setter'lar** (24.12 jar'ı):

| Bileşen | Sınıf | Doğrulanmış setter'lar |
|---|---|---|
| Burun konisi | `NoseCone` | `setLength`, `setShapeType(Transition.Shape)`, `setShapeParameter`, `setBaseRadius`, `setThickness`, `setShoulderLength`, `setShoulderRadius` |
| Gövde tüpü | `BodyTube` | `setLength`, `setOuterRadius`, `setInnerRadius` |
| Geçiş | `Transition` | `setLength`, `setShapeType(Transition.Shape.CONICAL/OGIVE/…)`, `setShapeParameter`, `setForeRadius`, `setAftRadius`, `setClipped` |
| Trapezoidal kanatçık | `TrapezoidFinSet` | `setFinCount`, `setRootChord`, `setTipChord`, `setSweep` (m), `setSweepAngle` (**rad**), `setHeight`, `setThickness` |
| Eliptikal kanatçık | `EllipticalFinSet` | `setFinCount`, `setHeight`, `setThickness` |
| İç boru | `InnerTube` | `setOuterRadius`, `setLength`, `setClusterConfiguration` |
| Kütle bileşeni | `MassComponent` | `setLength`, `setRadius`, `setComponentMass` |
| Paraşüt | `Parachute` | `setDiameter`, `setLineCount`, `setLineLength`, `setCD` |
| Şok kordonu | `ShockCord` | `setCordLength`, `setMaterial` |

Malzeme:

```python
mat = core.material.Material.newMaterial(
    core.material.Material.Type.LINE, "Polyester cord", 0.0014,
    core.material.MaterialGroup.THREADS_LINES, True)
```

**Doğrulama:** 9 bileşen tipi sıfırdan kuruldu → kaydedildi → yeniden yüklendi →
değerler aynı: kanatçık fin sayısı 3, kök kordon 0.05 m, süpürme açısı 0.7854 rad,
yükseklik 0.03 m; gövde yarıçapı 0.019 m, boyu 0.30 m; burun yarıçapı 0.019 m,
boyu 0.10 m; paraşüt çapı 0.30 m, 6 hat; iç boru 0.0125 m; kütle 0.01 kg;
şok kordonu 0.30 m.

**Uyarı:** `Transition`, `BodyTube`'nun çocuğu olamaz (IllegalStateException:
"not currently compatible") — stage'in kardeşi olmalıdır.

---

## d) Parametre değiştirme ve silme

```python
body = helper.get_component_named(rocket, "Body tube")
body.setName("Gövde")
body.setLength(0.25)
body.setOuterRadius(0.018)
fins.setFinCount(4)

removed = body.removeChild(chute)      # boolean döner
```

**Doğrulama:** kaydet → geri yükle → gövde boyu 0.25 m, yarıçap 0.018 m, fin sayısı 4,
13 bileşen → 12 bileşen, paraşüt silinmiş ✔.

---

## e) Motor atama

Motor **veritabanından** (üretici + ad):

```python
motor = helper.find_motor("C6", manufacturer="Estes")
# C6 | Estes | çap 0.018 m | boy 0.07 m
helper.set_motor(sim, "C6", manufacturer="Estes")
helper.get_motor(sim)      # 'C6'   (okuma geri doğrulaması set_motor içinde var)
```

Motor **.eng dosyasından**:

```python
helper.set_motor(sim, "motors/C6.eng")     # .eng/.rse/.zip yolu
```

> `.eng` düz metin ise **RASP biçiminde** olmalı (RockSim'in .eng'i XML'dir):
> başlık 7 alan → `designation çap[mm] boy[mm] gecikmeler yakıt[kg] toplam[kg] üretici`,
> ardından `zaman itki` satırları.

**Kritik nokta — uçuş konfigürasyonu:** Motor, roketin "seçili" konfigürasyonuna
değil, **simülasyonun kendi uçuş konfigürasyonuna** atanmalıdır
(`sim.getFlightConfigurationId()`). orlab'in `set_motor` bunu kendi yapar ve atamayı
okuyarak doğrular (mismatch → hata). Doğrulama: simple_model.ork sim[0] motoru A8 → C6
olarak değişti, kaydedildi, yeniden yüklendi, hâlâ C6 ✔.

---

## f) Fırlatma koşulları

Hepsi `sim.getOptions()` üzerinden (birimler: m, m/s, K, Pa; **açılar radyan**):

| Ayar | Setter | Getter | Birim |
|---|---|---|---|
| Rampa boyu | `setLaunchRodLength` | `getLaunchRodLength` | m |
| Rampa açısı | `setLaunchRodAngle` | `getLaunchRodAngle` | rad |
| Rampa yönü | `setLaunchRodDirection` | `getLaunchRodDirection` | rad |
| Rüzgâra dönük fırlatma | `setLaunchIntoWind` | `getLaunchIntoWind` | bool |
| Rüzgâr hızı | `setWindSpeedAverage` | `getWindSpeedAverage` | m/s |
| Rüzgâr sapması | `setWindSpeedDeviation` | `getWindSpeedDeviation` | m/s |
| Türbülans | `setWindTurbulenceIntensity` | `getWindTurbulenceIntensity` | oran |
| Rüzgâr yönü | `setWindDirection` | `getWindDirection` | rad |
| Fırlatma irtifası | `setLaunchAltitude` | `getLaunchAltitude` | m |
| Sıcaklık | `setLaunchTemperature` | `getLaunchTemperature` | K |
| Basınç | `setLaunchPressure` | `getLaunchPressure` | Pa |
| ISA atmosfer | `setISAAtmosphere` | `isISAAtmosphere` | bool |

Örnek (18° rampayı derece olarak verip radyana çevirmek):

```python
import math
opts.setLaunchRodLength(1.0)
opts.setLaunchRodAngle(math.radians(18.0))
opts.setWindSpeedAverage(3.0)
opts.setWindTurbulenceIntensity(0.10)
opts.setLaunchAltitude(100.0)
opts.setISAAtmosphere(False)      # özel sıcaklık/basınç için önce bu
opts.setLaunchTemperature(293.15)
opts.setLaunchPressure(101325.0)
```

**Doğrulama:** okuma geri döndü: 1.0 m / 18.0° (0.314159 rad) / 3.0 m/s / 0.1 / 100 m /
293.15 K / 101325 Pa / ISA=False.

---

## g) Simülasyon çalıştırma ve metrikler

```python
helper.run_simulation(sim)            # randomize_seed=True (varsayılan)
summary = helper.get_summary(sim)     # orlab.core.summary.FlightSummary (dataclass)
```

`FlightSummary` alanları (hepsi float, yoksa NaN):
`velocity_off_rod`, `stability_off_rod_cal`, `apogee`, `time_to_apogee`, `max_velocity`,
`max_acceleration`, `max_mach`, `min_stability_cal`, `max_stability_cal`,
`velocity_at_deployment`, `descent_rate`, `ground_hit_velocity`, `landing_x`, `landing_y`,
`landing_distance`, `landing_bearing_deg`, `flight_time`, `optimum_delay`,
`branch_number`, `branch_name`, `branch_count`, `warnings`.

Zaman serisi (numpy dizileri):

```python
ts = helper.get_timeseries(sim, ["TYPE_TIME", "TYPE_ALTITUDE", "TYPE_VELOCITY_TOTAL",
                                 "TYPE_STABILITY", "TYPE_CG_LOCATION", "TYPE_CP_LOCATION",
                                 "TYPE_MASS", "TYPE_POSITION_X", "TYPE_POSITION_Y"])
```

Uçuş olayları:

```python
events = helper.get_events(sim)
# {'FlightEvent.LAUNCH': [0.0], 'FlightEvent.IGNITION': [0.0], 'FlightEvent.LIFTOFF': [0.105],
#  'FlightEvent.LAUNCHROD': [0.247], 'FlightEvent.BURNOUT': [0.73], 'FlightEvent.APOGEE': [3.241],
#  'FlightEvent.EJECTION_CHARGE': [3.73], 'FlightEvent.RECOVERY_DEVICE_DEPLOYMENT': [3.731],
#  'FlightEvent.GROUND_HIT': [13.724], 'FlightEvent.SIMULATION_END': [13.724]}
```

**Doğrulama (rampa 1 m / 18° / rüzgâr 3 m/s / irtifa 100 m, simple_model.ork sim[0]):**
apogee 42.857 m, apogee'ye süre 3.191 s, max hız 29.442 m/s, max ivme 143.99 m/s²,
rampa çıkış hızı 15.454 m/s, rampa çıkış stabilitesi 1.987 kal, asistan içi
min/max stabilite 1.987/3.123 kal, motor sönümü (t=0.73 s) stabilitesi 2.713 kal,
iniş hızı 5.111 m/s, uçuş süresi 13.724 s, iniş mesafesi 11.82 m.

**Kalkış anı CP = NaN** (ilk örneklerde CP boştur; CP yalnız hava akışı başladıktan
sonra hesaplanır). Bu bir hata değil, OpenRocket davranışı.

---

## h) Seed sabitleme

24.12 jar'ında **yalnız** `getRandomSeed`, `setRandomSeed`, `randomizeSeed` var
(`setRandomSeedFixed` yok — o, klondaki daha yeni sürümde).

```python
opts = sim.getOptions()
opts.setRandomSeed(42)
helper.run_simulation(sim, randomize_seed=False)   # ← randomizeSeed() ÇAĞRILMAZ
```

**Doğrulama (aynı süreç içinde):**
- seed=42, rüzgâr 3 m/s: apogee 43.091208379792945 → 43.091208379792945 (birebir aynı) ✔
- seed=42, rüzgâr 0: apogee 45.9322645723715 → 45.9322645723715 (birebir aynı) ✔
- rastgele seed (varsayılan `randomize_seed=True`): 45.93225465973589 → 45.93214669976853
  (farklı) ✔
- farklı seed (12345): 45.93251773333656 → seed etkisi var ama çok küçük (rüzgârsız).

**Sınır (orlab dokümanı + doğrulama):** 24.12'de rüzgâr modeli süreç başına ek entropi
çektiğinden, sabit seed **aynı süreç içinde** tekrar üretilebilir; **farklı süreçler
arasında rüzgâr açıkken** birebir aynı sonuç garanti edilmez. Bu yüzden baseline
karşılaştırmasında rüzgâr hızı 0 olan koşullar kullanılmalıdır (Phase 6'da ölçülecek).

---

## Çözülemeyen / sınırlı olanlar

- **Bileşen silme**: `removeChild(component)` çalışıyor; "adıyla sil" yardımcısı
  kütüphanede yazılacak (bulunamayan ad → anlaşılır hata).
- **Motor "sığmıyor" kontrolü**: OpenRocket API'si motoru atarken çap/uyum kontrolü
  **yapmıyor**; kütüphane `validate()` içinde kendi kontrolünü yapacak
  (motor çapı > iç boru çapı → hata).
- **Yapısal analiz / flutter**: OpenRocket'da yok.
- **Çok kademeli uçuş**: `get_summary(sim, branch_number)` ile branch bazlı özet var;
  `helper.run_simulation` tüm kademeleri çalıştırır.
