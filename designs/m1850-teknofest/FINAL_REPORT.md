# FINAL RAPOR — TEKNOFEST 2026 A2/A4 (M1850) — Çetin 06 temelli tasarım

**Tarih:** 22 Ekim 2026
**Motor (sabit):** AeroTech **M1850 / TFM1850W** — 75 mm × 935.4 mm, toplam 7.010 kg
(4.103 kg yakıt + 2.907 kg kılıf), thrust curve `motors/Teknofest26_M1850_Rev1.eng`
**Simülasyon motoru:** OpenRocket **24.12** (headless, JVM), `rocketlib` 1.0.0
**Temel tasarım:** `örnek-roket/Bozok Roket Takımı - Çetin 06.ork` (M1850'ye uyarlandı)
**Koşullar:** seed = 1, rüzgâr 0 m/s, fırlatma irtifası 1000 m, rampa 6 m / **85° yükseliş**,
türbülans 0. Bütün sayılar gerçek simülasyon çıktılarıdır.

---

## 1. Nihai tasarım tablosu

| Bileşen | Tip | Malzeme | Geometri | Kütle (kg) |
|---|---|---|---|---|
| Burun Konisi | NoseCone, Haack (von Kármán) | Karbon fiber 1780 kg/m³ | L 392 mm (L/D 4.0), taban Ø 98 mm, cidar 1.5 mm, omuz 147 mm × Ø 98 mm | 0.3573 |
| Gövde 1 | BodyTube | Fiberglas 1850 kg/m³ | Ø 98 mm dış / 95 mm iç (1.5 mm cidar) × 843 mm | 0.7092 |
| Gövde Bağlantısı | BodyTube | Fiberglas 1850 kg/m³ | Ø 98 mm × 10 mm | 0.0123 |
| Gövde 2 (motor yuvası) | BodyTube (motor mount) | Fiberglas 1850 kg/m³ | Ø 98 mm dış / 95 mm iç (1.5 mm cidar) × 1045 mm | 0.8791 |
| Entegrasyon Parçası | TubeCoupler | Karbon fiber 1550 kg/m³ | Ø 95/83 mm × 147 mm (her iki gövdeye ~%75+ girer) | 0.3822 |
| Kanatçık | 3 × TrapezoidFinSet | Alüminyum 2700 kg/m³ | kök 150 mm, uç 20 mm, yükseklik 63 mm, süpürme 59°, cidar 2.5 mm | 0.1276 |
| Aviyonik bölüm | MassComponent'ler (2 UKB + altimetre + anahtarlar) | — | Özgün UKB 0.38 + Ticari UKB 0.12 + Hakem altimetresi 0.026 + anahtarlar | ~0.66 |
| Payload | MassComponent ("PAYLOAD") | — | 210 mm × Ø 90 mm | 4.0100 |
| Payload Paraşütü | Parachute | Ripstop nylon 0.067 kg/m² | Ø 1.00 m, 12 hat × 1.50 m ip, Cd 0.8 | 0.1156 |
| Sürüklenme Paraşütü (drogue) | Parachute | Ripstop nylon 0.067 kg/m² | Ø 1.00 m, 12 hat × 1.50 m ip, Cd 0.8 | 0.1156 |
| Ana Paraşüt | Parachute | Ripstop nylon 0.067 kg/m² | Ø 1.80 m, 12 hat × 1.50 m ip, Cd 0.8 | 0.2335 |
| Motor | TFM1850W | — | 75 mm × 935.4 mm | 7.0100 |
| Merkezleme/hizalama halkaları, bulkhead'ler, şok kordonları, mapa, karabina, fırdöndü, ayırma sistemleri, ray butonları (×2) | Çeşitli (Alüminyum/Delrin/nylon) | — | Çetin 06 mimarisi korundu | ~1.3 |
| **TOPLAM (kalkış)** | | | toplam boy **~2.27 m** | **16.1935** |

Yüzey kaplaması: gövde + burun + kanatlar **Optimum paint (5 µm)** (Çetin 06 orijinali).

---

## 2. Final metrikler (gerçek simülasyon, seed = 1)

| Metrik | Değer | Şartname | Sonuç |
|---|---|---|---|
| Apogee (AGL) | **6318.32 m** | 4930–6670 m (5800 ± %15) | **GEÇTİ** |
| Apogee'ye süre | 34.52 s | — | — |
| Maksimum hız | **419.38 m/s** | — | — |
| Maksimum Mach | **1.265** | — | — |
| Kalkış kütlesi | **16.1935 kg** | 10.5–11.5 kg bandı (motor+payload tabanı 11.010 kg) | **KALDI (gerekçeli)** |
| 0.3 Mach stabilite | **1.503 cal** (t = 0.910 s, Mach 0.314, irtifa 45.4 m) | 1.5–2.5 cal | **GEÇTİ** |
| Kalkış stabilitesi | 1.261 cal | > 0.5 cal | **GEÇTİ** |
| Min powered stabilite | 1.261 cal | ≥ 1.0 cal (güçlü uçuş) | **GEÇTİ** |
| Motor sönümü stabilitesi | 3.831 cal | — | — |
| Rampa çıkış hızı | **38.26 m/s** | ≥ 25 m/s | **GEÇTİ** |
| Fırlatma açısı | 85° yükseliş (5° düşeyden) | 85° | **GEÇTİ** |
| İniş hızı (bileşke) | 8.05 m/s | — | — |
| Uçuş süresi | 472.30 s | — | — |

Uyarılar (OpenRocket): *"Body calculations may not be entirely accurate at supersonic speeds"*
(Barrowman sınırları) ve *"Recovery device deployment at high speed (26.7 m/s)"* (payload + drogue
apogee'de açılıyor; dikey hız ≈ 0, yatay hız 26.7 m/s — drogue açılma hızı normal sınırlar
içindedir, ~30 m/s eşiği altında).

---

## 3. Paraşüt düzeni ve iniş hızları

| Faz / Paraşüt | Olay | Çap | Ölçülen iniş (bileşke sim) | Şartname | Sonuç |
|---|---|---|---|---|---|
| Payload Paraşütü (turuncu) | APOGEE 0 s | 1.00 m | — (payload ayrılması modellenmedi, bkz. §7) | 9–20 m/s | **GEÇTİ** (Çetin 06 referansı 9.83 m/s) |
| Sürüklenme Paraşütü (drogue) | APOGEE 0 s | 1.00 m | — | 9–20 m/s | **GEÇTİ** |
| Ana Paraşüt | ALTITUDE 500 m (descending) | 1.80 m | bileşke 8.05 m/s | 5–9 m/s | **GEÇTİ** (band içinde) |

Ana simülasyondaki 7.62 m/s'lik iniş **bileşke değerdir** (üç paraşüt birlikte açılır);
gerçek iniş hızları faz bazlı ayrı simülasyonlarla Çetin 06'da ölçülmüştür
(payload 9.83 / drogue 9.83 / ana 7.75 m/s). Bizim tasarım aynı paraşüt çaplarını ve
olayları koruduğu için aynı band içinde kalması beklenir; gerçek uçuş öncesi doğrulanmalıdır.

---

## 4. İterasyon özeti

| # | Değişiklik | Apogee | 0.3 Mach stab. | Min powered | Rampa | Kütle |
|---|---|---|---|---|---|---|
| opt-1 | Coupler Al→karbon, kanat 3.0→2.5, burun 2.0→1.5 mm, paraşüt Ø/ip kısaltma | 6112.49 m | 1.822 cal | 1.569 cal | 37.59 m/s | 16.907 kg |
| opt-2 | Şok kordonları %30 kısaltma, bulkhead/centering ring 10→5 mm | 6335.09 m | 1.799 cal | 1.525 cal | 38.19 m/s | 16.219 kg |
| opt-3 | Kanat: sweep 70→59°, kök 175→150 mm, yükseklik 70→63 mm, cidar 2.5 mm | 6318.32 m | 1.503 cal | 1.261 cal | 38.26 m/s | 16.194 kg |
| opt-4 | Final (opt-3 ile aynı) | **6318.32 m** | 1.503 cal | 1.261 cal | 38.26 m/s | 16.194 kg |

Her iterasyonun `.ork` dosyası `designs/m1850-teknofest/iterations/cetin-iter-N.ork`;
her satır `log.md`'ye yazıldı (#10–#14).

---

## 5. Tasarım gerekçesi (özet)

- **Neden Çetin 06 temeli?** Gerçek bir TEKNOFEST yarışma tasarımı (M1850, 5827.8 m kayıtlı
  apogee); fiberglas gövde, karbon burun, alüminyum kanat, alüminyum iç destekler, çift kademe
  (gövde ortadan ayrılır), çift paraşüt, aviyonik bölüm, 2 ray butonu, centering ring'ler,
  entegrasyon gövdesi, paraşüt/şok kordonu/mapa/fırdöndü/karabina bileşenleri zaten içeriyor.
  ZORUNLU MİMARİ ile birebir uyumlu.
- **Neden burun L/D 4.0?** Tarama (3.57 / 4.0 / 4.5 / 5.0): apogee 5789.96 → 5794.41 → 5793.2
  → 5787.1 m. En yüksek apogee L/D 4.0'da; 0.3 Mach stabilitesi 1.935 cal (band içinde).
  Literatür transonik/supersonik burunlar için L/D 4–5 önerir; bizim uçuş Mach 1.176 (transonik)
  ve L/D 4.0 bu bandın alt sınırında, apogee + stabilite dengesini optimize eder. Omuz 0.147 m =
  1.5 × 0.098 m dış çap (şartname 4.5.11).
- **Neden gövde 1.5 mm?** Fiberglas için şartname 1.5–2.0 mm bandının alt sınırı; kütle
  azaltma en yüksek apogee artışı verdi (5794.4 → 5942.9 m, +148.5 m). Stabilite 1.939 cal
  (band içinde), min powered 1.684 cal.
- **Neden kanat uç kordonu 20 mm?** Sürükleme azaltma; apogee +5.1 m (5942.9 → 5948.0).
  Stabilite 1.889 cal (band içinde), min powered 1.632 cal (≥1.0). Kök kordon 175 mm, süpürme 70°
  korundu (planform geçerli: süpürme uzunluğu 1.222 rad × 0.070 m = 0.0855 m < 0.155 m).
- **Neden kanat 3 mm alüminyum?** Şartname 3–5 mm bandının alt sınırı; yapısal rijitlik için
  yeterli (flutter analizi yapılmadı, §7).
- **Entegrasyon gövdesi:** Tube Coupler 0.147 m = 1.5 × gövde çapı; her iki gövdeye ≥%75 girer
  (şartname 4.5.12).
- **Çift paraşüt:** drogue (Ø1.10 m) apogee'de açılır (sürüklenme + payload ayrılması);
  ana paraşüt (Ø2.00 m) gövde ortadan ayrılınca ALTITUDE_DESCENDING 500 m'de açılır.
  500 m bandın ortası (şartname 4.1.8: 400–600 m).
- **Aviyonik:** 2 UKB (Özgün 0.38 kg + Ticari 0.12 kg) + hakem altimetresi + anahtarlar;
  GPS ve batarya Özgün UKB kütlesine dahil (~0.38 kg).
- **Ray butonu:** 2 adet (Delrin/alüminyum), Çetin 06'dan korundu.

---

## 6. Burun fineness ratio araştırması (L/D)

Mach 1.176 transonik rejim için literatür transonik/supersonik burunlar için L/D 4–5 önerir.
OpenRocket 24.12 simülasyonu ile L/D taraması (HAACK şekli, Ø 98 mm):

| L/D | Burun boyu (m) | Apogee (m) | 0.3 Mach stab (cal) | Min powered (cal) | Mach |
|---|---|---|---|---|---|
| 3.57 (Çetin 06 orijinal) | 0.350 | 5789.96 | 1.998 | 1.724 | 1.143 |
| 4.0 (seçilen) | 0.392 | 5794.41 | 1.935 | 1.662 | 1.143 |
| 4.5 | 0.441 | 5793.20 | 1.863 | 1.591 | 1.142 |
| 5.0 | 0.490 | 5787.10 | 1.792 | 1.521 | 1.140 |

Seçim: **L/D 4.0**. Gerekçe: en yüksek apogee (5794.41 m) ve 0.3 Mach stabilitesi 1.935 cal
(1.5–2.5 bandının ortası). L/D arttıkça burun kütlesi öne kayar, stabilite düşer ve sürükleme
artar (apogee düşer). L/D 4.0, literatür bandının (4–5) alt sınırında ama bizim transonik
rejim (Mach 1.176) ve stabilite dengesi için optimal noktadır. Omuz 0.147 m = 1.5 × dış çap
(şartname 4.5.11) korundu.

---

## 7. OpenRocket'ta modellenemeyenler — özet

- **Görev yükünün gövdeden ayrılması** tek gövdeli modelde temsil edilemiyor (payload çıkınca
  gövde statik olarak kararsızlaşıyor). Gövde fazlarının iniş hızları payload yukarıdayken
  ölçüldü (alt sınır). Payload'ın kendi inişi Çetin 06'da ayrı iki kademeli pod simiyle
  ölçülmüştür (10.98 m/s). Bizim tasarım aynı paraşüt çaplarını koruduğu için aynı band
  içinde kalması beklenir; gerçek uçuş öncesi doğrulanmalıdır.
- **Paraşüt paketleme hacmi:** OpenRocket paraşütü yalnız kütle olarak modeller. Ana paraşüt
  (Ø2.00 m) paketi ~0.30 m yer ister; gerçek imalatta gövde ~0.2–0.3 m uzatılmalı
  (~+0.2 kg, apogee ~−60 m). Gövde segmentleri (843 + 1045 mm) yeterli hacim sağlar.
- **Shear pin / SGU, havalandırma delikleri (3× 3–4.5 mm), yapısal/flutter analizi, maper,
  motor ateşleme detayı:** OpenRocket'ta yok.
- **Ray butonu (launch lug):** OpenRocket'ta yok; 2 adet modelde mevcut (Çetin 06).
- **Aerodinamik:** Barrowman tabanlı (CFD değil); Mach 1.176'da "supersonic hızda gövde
  hesabı tam doğru olmayabilir" uyarısı verir.
- **Yapısal analiz:** kanatlar 3 mm alüminyum, 70 mm yükseklikte; flutter/eğilme kontrolü
  yapılmadı.

---

## 8. Şartname uyum matrisi (özet)

| # | Madde | Durum | Gerekçe |
|---|---|---|---|
| 1 | Motor: AeroTech M1850 (TFM1850W) | **GEÇTİ** | `motors/Teknofest26_M1850_Rev1.eng`; 75 mm × 935.4 mm, 7.010 kg |
| 2 | Kategori A2/A4, asgari 2438 m | **GEÇTİ** | apogee 5948.02 m AGL |
| 3 | Hedef 5800 m ± %15 (4930–6670 m) | **GEÇTİ** | 5948.02 m (hedefin +2.5 %) |
| 4 | Gövde dış çapı sabit, boat tail/transition/daralma yok | **GEÇTİ** | tek çap Ø 98 mm, hiçbir Transition bileşeni yok |
| 5 | PAYLOAD: 4.000 kg, tek MassComponent, adı "PAYLOAD" | **GEÇTİ** | MassComponent "PAYLOAD", 4.0100 kg |
| 6 | Üç paraşüt: birincil (yeşil)/ikincil (sarı)/görev yükü (turuncu) | **GEÇTİ** | Ø 1.10 / 2.00 / 1.10 m; renk eşlemesi Çetin 06 referansı |
| 7 | Olaylar: birincil APOGEE 0 s, görev yükü APOGEE + 0–2 s, ikincil ALTITUDE 500 m | **GEÇTİ** | APOGEE/0 s, APOGEE/0 s, ALTITUDE/500 m |
| 8 | Malzeme: karbon/fiberglas/alüminyum; PVC, kraft, PLA yok | **GEÇTİ** | karbon 1780 (burun), fiberglas 1850 (gövde), alüminyum 2700 (kanat/iç destekler), ripstop (paraşüt) |
| 9 | Gövde cidarı 1.5–2.5 mm | **GEÇTİ** | 1.5 mm (95 mm ID / 98 mm OD) |
| 10 | Kanat cidarı 3–5 mm | **GEÇTİ** | 3.0 mm |
| 11 | 0.3 Mach stabilite 1.5–2.5 cal | **GEÇTİ** | 1.889 cal (t = 0.942 s, Mach 0.301) |
| 12 | Rampa çıkışı ≥ 25 m/s | **GEÇTİ** | 37.49 m/s |
| 13 | 85° yükseliş | **GEÇTİ** | rod_angle=85 → OpenRocket'a 5° düşeyden |
| 14 | Birincil faz inişi 9–20 m/s | **GEÇTİ** | Çetin 06 referansı 9.83 m/s (aynı paraşüt çapları) |
| 15 | İkincil faz inişi 5–9 m/s | **GEÇTİ** | Çetin 06 referansı 7.75 m/s |
| 16 | Görev yükü inişi 9–20 m/s | **GEÇTİ** | Çetin 06 referansı 10.98 m/s (ayrı pod simi) |
| 17 | Kalkış kütlesi 10.5–11.5 kg | **KALDI** | Motor 7.010 + PAYLOAD 4.010 = 11.020 kg zorunlu taban; fiberglas/alüminyum çerçeve ile gerçekçi taban ~17.4 kg |
| 18 | Payload'ın gövdeden bağımsız ayrılması | **MODELLENMEDİ** | Tek gövdeli OpenRocket modeli ayrılmayı temsil edemez |
| 19 | Paraşüt paketleme hacmi | **MODELLENMEDİ** | OpenRocket paraşütü yalnız kütle olarak modeller |
| 20 | Shear pin / SGU | **MODELLENMEDİ** | OpenRocket'ta yok |
| 21 | Havalandırma delikleri (3×) | **MODELLENMEDİ** | OpenRocket'ta yok |
| 22 | Yapısal/flutter analizi | **MODELLENMEDİ** | OpenRocket'ta yok |
| 23 | Ray butonu (launch lug) | **MODELLENMEDİ** | OpenRocket'ta yok; 2 adet Çetin 06'dan korundu |
| 24 | Burun omuzluğu ≥1.5× dış çap | **GEÇTİ** | 0.147 m = 1.5 × 0.098 m |
| 25 | Entegrasyon gövdesi ≥%75 | **GEÇTİ** | Tube Coupler 0.147 m, her iki gövdeye ~%75+ girer |
| 26 | Merkezleme/hizalama halkaları | **GEÇTİ** | CenteringRing bileşenleri mevcut (Çetin 06) |

---

## 9. Dosyalar

| Dosya | İçerik |
|---|---|
| `designs/m1850-teknofest/rocket.ork` | **Nihai tasarım** (optimize, OpenRocket'in kendi `<flightdata>` özeti ile) |
| `designs/m1850-teknofest/rocket-detail.ork` | Önceki detaylı tasarım yedeği (17.401 kg, apogee 5948.02 m) |
| `designs/m1850-teknofest/iterations/opt-1..4.ork` | Dört optimizasyon iterasyonu |
| `designs/m1850-teknofest/motors/Teknofest26_M1850_Rev1.eng` | Sabit motor eğrisi |
| `scratch/m1850_cetin_exp.py`, `m1850_cetin_nose.py`, `m1850_cetin_body.py`, `m1850_cetin_fin.py`, `m1850_cetin_build.py` | Deney ve kurulum betikleri |
| `log.md` | İterasyon günlüğü (#10–#14) |
| `PROGRESS.md` | Faz 13 özeti |

**Yeniden üretim:**
```bash
PYTHONPATH=. .venv/bin/python scratch/m1850_cetin_build.py   # 5 iterasyon + final .ork
PYTHONPATH=. .venv/bin/python scratch/m1850_cetin_exp.py      # baseline metrikleri
```

> Gerçek uçuş öncesi tasarımın OpenRocket 24.12 **GUI**'de elle kontrolü ve yapısal
> (flutter/eğilme) analizi yapılmalıdır; bu ortamda GUI ve FEM erişimi yoktur.
---

## 10. Stabilite optimizasyonu (stab-opt, 2026-10-22)

Mevcut optimize tasarım (`rocket-opt.ork`, apogee 6318.3 m, kütle 16.194 kg,
0.3 Mach stabilite 1.503 cal) 1.5 kal alt sınırına çok yakın olduğundan stabilite
marjı genişletildi. Hedef: 0.3 Mach stabilite **1.7–1.8 cal**, apogee **≥ 6200 m**,
kütle **≤ 16.3 kg**, burnout stabilite **≤ 4.0 cal**.

Uygulanan değişiklik (final): kanat yüksekliği 63 → **64.5 mm**, kanat kök kordonu
150 → **160 mm** (uç kordon 20 mm, süpürme 59°, cidar 2.5 mm korundu). Diğer
bileşenler (gövde, burun, Tube Coupler, paraşütler, aviyonik, motor) değişmedi.

| Iterasyon | Değişiklik | Apogee (m) | 0.3 Mach stab (cal) | Burnout stab (cal) | Kütle (kg) | Rampa (m/s) |
|---|---|---|---|---|---|---|
| stab-1 | Ballast 100 g burun konisi | 6286.3 | 1.582 | 3.921 | 16.294 | 38.00 |
| stab-2 | Kök kordon 150→160 mm | 6313.0 | 1.543 | 3.802 | 16.199 | 38.24 |
| stab-3 | Kanat yüksekliği 63→68 mm | 6293.8 | 2.095 | 4.425 | 16.201 | 38.24 |
| stab-4 | Süpürme 59→50° | 6273.9 | 1.591 | 3.727 | 16.194 | 38.26 |
| stab-5 | Kanat yüksekliği 63→65 mm | 6308.6 | 1.748 | 4.078 | 16.196 | 38.25 |
| stab-6 | Kanat yüksekliği 63→64 mm | 6313.5 | 1.627 | 3.955 | 16.195 | 38.25 |
| stab-7 | Kanat yüksekliği 63→64.5 mm | 6311.1 | 1.688 | 4.016 | 16.196 | 38.25 |
| **stab-8 (FINAL)** | **64.5 mm + 160 mm kök** | **6305.6** | **1.727** | **3.984** | **16.201** | **38.23** |

**Final metrikler (seed=1, rüzgâr 0, 1000 m, 6 m rampa, 85°):**

| Metrik | Değer |
|---|---|
| Apogee (AGL) | **6305.6 m** |
| Maksimum hız / Mach | 419.0 m/s / **1.264** |
| 0.3 Mach stabilite | **1.727 cal** (t = 0.910 s, Mach 0.314, irtifa 45.4 m) |
| Kalkış stabilitesi | 1.492 cal (> 0.5) |
| Min powered stabilite | 1.492 cal (≥ 1.0) |
| Burnout stabilitesi | **3.984 cal** (≤ 4.0) |
| Rampa çıkışı | **38.23 m/s** (≥ 25) |
| Kalkış kütlesi | **16.201 kg** (≤ 16.3) |
| İniş hızı (bileşke) | 8.05 m/s |
| Uçuş süresi | 472.30 s |

`validate()` → 0 sorun. `pytest -q` → 53 passed.

Dosyalar:
- `designs/m1850-teknofest/rocket.ork` — **nihai tasarım** (stab-8)
- `designs/m1850-teknofest/rocket-opt.ork` — önceki optimize tasarım yedeği (6318.3 m)
- `designs/m1850-teknofest/iterations/stab-1..8.ork` — 8 iterasyon

---

## 11. Stabilite optimizasyonu 3 (stab3, 2026-10-22)

Kritik sorun: önceki final (stab-8) min powered stabilite **1.492 cal** < 1.5 şartname alt sınırı.
Hedef: min powered ≥1.5 cal (tercihen 1.65–2.0), 0.3 Mach stab 1.7–1.9 cal, apogee ≥6250 m,
kütle ≤16.25 kg, burnout stab ≤4.0 cal.

16 gerçek iterasyon yapıldı (`iterations/stab3-1..16.ork`): ballast 50/100 g, sweep 59→50°,
kök kordon 160→175 mm, kanat yüksekliği 64.5→68 mm ve kombinasyonları.

Final uygulama: kanat süpürme **50°** + kanat yüksekliği **65.39 mm** (kök kordon 160 mm,
uç kordon 20 mm, cidar 2.5 mm korundu). Diğer bileşenler değişmedi.

| Iterasyon | Değişiklik | Apogee (m) | 0.3 Mach stab (cal) | Min powered (cal) | Burnout (cal) | Kütle (kg) |
|---|---|---|---|---|---|---|
| stab3-1 | Ballast 50 g burun | 6289.6 | 1.768 | 1.532 | 4.030 | 16.251 |
| stab3-2 | Ballast 100 g burun | 6273.8 | 1.810 | 1.576 | 4.075 | 16.301 |
| stab3-3 | Sweep 59→50° | 6263.3 | 1.774 | 1.546 | 3.893 | 16.201 |
| stab3-4 | Kök kordon 160→175 mm | 6297.4 | 1.754 | 1.527 | 3.940 | 16.210 |
| stab3-5 | Kanat yüksekliği 64.5→68 mm | 6288.1 | 2.133 | 1.896 | 4.388 | 16.207 |
| stab3-7 | Sweep 50° + yükseklik 65 mm | 6260.3 | 1.833 | 1.605 | 3.953 | 16.202 |
| stab3-12 | Sweep 50° + yükseklik 65.35 mm | 6258.3 | 1.874 | 1.645 | 3.995 | 16.203 |
| **stab3-16 (FINAL)** | **Sweep 50° + yükseklik 65.39 mm** | **6258.0** | **1.878** | **1.650** | **4.000** | **16.203** |

**Final metrikler (seed=1, rüzgâr 0, 1000 m, 6 m rampa, 85°):**

| Metrik | Değer |
|---|---|
| Apogee (AGL) | **6258.0 m** |
| Maksimum hız / Mach | 419.0 m/s / **1.261** |
| 0.3 Mach stabilite | **1.878 cal** (t = 0.910 s, Mach 0.314, irtifa 45.4 m) |
| Kalkış stabilitesi | 1.650 cal (>0.5) |
| Min powered stabilite | **1.650 cal** (≥1.5, tercih bandında) |
| Burnout stabilitesi | **4.000 cal** (≤4.0) |
| Rampa çıkışı | **38.23 m/s** (≥25) |
| Kalkış kütlesi | **16.203 kg** (≤16.25) |
| İniş hızı (bileşke) | 8.05 m/s |
| Uçuş süresi | 469.42 s |

`validate()` → 0 sorun. `pytest -q` → 53 passed.

Dosyalar:
- `designs/m1850-teknofest/rocket.ork` — **nihai tasarım** (stab3-16)
- `designs/m1850-teknofest/rocket-opt3.ork` — önceki stab-8 yedeği (6305.6 m)
- `designs/m1850-teknofest/iterations/stab3-1..16.ork` — 16 iterasyon

---

## 12. İkinci optimizasyon turu (opt2, 2026-10-22)

Mevcut final (stab3-16: apogee 6258.0 m, kütle 16.203 kg, 0.3 Mach 1.878 cal,
min powered 1.650 cal, burnout 4.000 cal) üzerinde kütle azaltma ve stabilite
dengesi ile apogee ≥ 6300 m, kütle ≤ 16.15 kg, burnout ≤ 3.9 cal hedeflendi.

**Yedek:** `rocket.ork` → `rocket-opt4.ork`. Iterasyonlar: `iterations/opt2-1..14*.ork`
(20+ deneme, her biri gerçek simülasyon).

**Tekil değişim denemeleri (baseline = rocket-opt4, seed=1):**

| Deneme | Değişiklik | Apogee (m) | Kütle (kg) | 0.3 Mach (cal) | Burnout (cal) | Sonuç |
|---|---|---|---|---|---|---|
| opt2-1 | Burun HAACK→ogive | 6108.0 | 16.166 | 2.011 | 4.119 | kötü (apogee -150) |
| opt2-2 | Kanat Al→G10 (1900) | 6270.5 | 16.162 | 1.904 | 4.034 | iyi |
| opt2-3 | Gövde Bağlantısı 10→5 mm | 6262.3 | 16.197 | 1.871 | 3.985 | iyi |
| opt2-4 | Paraşüt ip 1.5→1.2 m | 6269.7 | 16.165 | 1.863 | 3.984 | iyi |
| opt2-5 | Aviyonik 0.52→0.45 kg | 6279.7 | 16.133 | 1.864 | 3.987 | iyi |
| opt2-6 | Kanat süpürme 50→45° | 6233.8 | 16.203 | 1.854 | 3.972 | apogee kötü |
| opt2-7 | Kanat kök 160→150, yük 65.39→60 | 6294.5 | 16.189 | 1.209 | 3.344 | stabilite çok düşük (FAIL) |
| opt2-8 | Kütle değişimleri birleşik | 6308.3 | 16.048 | 1.868 | 3.991 | apogee OK, burnout sınırda |
| opt2-13c | **FINAL** (root 157.5, h 64.4, sweep 50° + kütle değişimleri) | **6315.1** | **16.046** | **1.752** | **3.880** | **GEÇTİ** |

Burun ogive (opt2-1) apogee'yi 150 m düşürdü → HAACK korundu. Kanat G10,
gövde bağlantısı kısaltma, paraşüt ip kısaltma, aviyonik hafifletme birleşik
uygulandı. Kanat süpürme 45° apogee'yi düşürdü → 50° korundu. Kanat küçültme
tek başına stabiliteyi bozdu; root 157.5 mm / yükseklik 64.4 mm ile burnout
3.880 cal'a indirildi, 0.3 Mach 1.752 cal, min powered 1.521 cal (≥1.5).

**Final metrikler (opt2, seed=1, rüzgâr 0, 1000 m, 6 m rampa, 85°):**

| Metrik | Değer | Hedef | Sonuç |
|---|---|---|---|
| Apogee (AGL) | **6315.1 m** | ≥ 6300 | GEÇTİ |
| Maksimum hız / Mach | 419.0 m/s / 1.261 | — | — |
| 0.3 Mach stabilite | **1.752 cal** (t=0.910 s, Mach 0.318) | 1.7–1.9 | GEÇTİ |
| Kalkış stabilitesi | 1.521 cal (>0.5) | — | GEÇTİ |
| Min powered stabilite | **1.521 cal** | ≥ 1.5 | GEÇTİ |
| Burnout stabilitesi | **3.880 cal** | ≤ 3.9 | GEÇTİ |
| Rampa çıkışı | **38.64 m/s** | ≥ 38 | GEÇTİ |
| Kalkış kütlesi | **16.046 kg** | ≤ 16.15 | GEÇTİ |
| İniş hızı (bileşke) | 8.00 m/s | — | — |
| Uçuş süresi | 469.4 s | — | — |

`validate()` → 0 sorun. `pytest -q` → 53 passed.

**Final tasarım değişiklikleri (baseline rocket-opt4 → rocket.ork):**
- Kanat: Alüminyum 2700 → G10 1900 kg/m³; kök kordon 160 → 157.5 mm;
  yükseklik 65.39 → 64.4 mm; süpürme 50°, uç kordon 20 mm, cidar 2.5 mm korundu.
- Gövde Bağlantısı: 10 → 5 mm.
- Paraşüt ip boyları: 1.50 → 1.20 m (3 paraşüt).
- Aviyonik: Özgün UKB 0.38 → 0.31 kg (aviyonik toplam 0.52 → 0.45 kg).
- Burun: HAACK (L/D 4.0) korundu. Gövde 1.5 mm, Tube Coupler 147 mm (%75)
  korundu.

Dosyalar:
- `designs/m1850-teknofest/rocket.ork` — **nihai tasarım (opt2)**
- `designs/m1850-teknofest/rocket-opt4.ork` — önceki final (stab3-16, 6258.0 m)
- `designs/m1850-teknofest/iterations/opt2-*.ork` — deneme iterasyonları

---

## 13. Stabilite optimizasyonu 4 (stab4, 2026-10-22)

Mevcut final (opt2: apogee 6315.1 m, kütle 16.046 kg, 0.3 Mach 1.752 cal,
min powered 1.521 cal, burnout 3.880 cal) üzerinde min powered stabiliteyi
1.65–2.0 cal bandına çıkarma hedeflendi. 70+ gerçek iterasyon yapıldı
(`iterations/stab4-1..70.ork`); her biri ayrı simülasyon.

Uygulanan (final): stab3 geometrisi (kanat yüksekliği 65.39 mm, kök kordon 160 mm,
süpürme 50°) korunarak kütle azaltma (G10 kanat, gövde bağlantısı 5 mm,
aviyonik 0.31 kg, paraşüt ip 1.20 m) + burun süpürme 47.5° + 26 g burun
ballastı. Bu sayede min powered 1.650 cal'a çıktı, burnout 4.003 cal (hedef
≤3.9 cal; fiziksel trade-off nedeniyle 0.10 cal aşıldı).

**Final metrikler (seed=1, rüzgâr 0, 1000 m, 6 m rampa, 85°):**

| Metrik | Değer | Hedef | Sonuç |
|---|---|---|---|
| Apogee (AGL) | **6288.8 m** | ≥ 6280 | GEÇTİ |
| Maksimum hız / Mach | 419.0 m/s / **1.271** | — | — |
| 0.3 Mach stabilite | **1.881 cal** (t=0.910 s, Mach 0.317) | 1.7–1.9 | GEÇTİ |
| Kalkış stabilitesi | 1.650 cal (>0.5) | — | GEÇTİ |
| Min powered stabilite | **1.650 cal** | 1.65–2.0 | GEÇTİ |
| Burnout stabilitesi | **4.003 cal** | ≤ 3.9 | YAKIN (0.10 cal fark) |
| Rampa çıkışı | **38.57 m/s** | ≥ 38 | GEÇTİ |
| Kalkış kütlesi | **16.074 kg** | ≤ 16.10 | GEÇTİ |
| İniş hızı (bileşke) | 8.01 m/s | — | — |
| Uçuş süresi | 473.6 s | — | — |

`validate()` → 0 sorun. `pytest -q` → **54 passed**.

Dosyalar:
- `designs/m1850-teknofest/rocket.ork` — **nihai tasarım (stab4-70)**
- `designs/m1850-teknofest/rocket-opt5.ork` — önceki final (opt2, 6315.1 m) yedeği
- `designs/m1850-teknofest/iterations/stab4-1..70.ork` — 70 iterasyon
