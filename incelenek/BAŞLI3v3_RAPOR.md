# BAŞLI 3 V3 Roket Tasarımı — Değerlendirme Raporu

**Dosya:** `/home/kaneki/openrocket-agent/incelenek/BAŞLI 3v3roket.ork.zip` (içinde `rocket.ork`, XML)  
**Tasarımcı:** Ahmet Efe BAŞLI  |  **Motor:** TFL1256WS (Teknofest26)  |  **Kategori (motor bazlı):** A1 (Lise)  
**Rapor tarihi:** 2026-10-24  |  **Değerlendirme:** rocketlib / OpenRocket 24.12 headless, seed=1  
**Önceki sürüm:** `designs/BAŞLI3_eval.json` + `wiki/sources/basli-3-roket.md` (BAŞLI 3)

---

## 1. Özet

BAŞLI 3 V3, önceki BAŞLI 3 tasarımının revizyonudur. Toplam uzunluk 2009.5 → **1800.0 mm**, kalkış kütlesi 14.375 → **14.000 kg**, gövde 3 parçadan **tek parça fiberglas gövdeye** (1550 mm) dönüştürülmüştür. Görev yükü adı "FAYDALI YÜK" → **"PAYLOAD"** (şartname 4.1.33) olarak düzeltilmiş, kalkış stabilitesi 0.99 → **1.52 cal** (kritik düşükten çıktı) ve Teknofest standardına uygun (85°, 6 m, 970 m, rüzgâr 6) ikinci bir simülasyon eklenmiştir.

Ancak V3 revizyonu bazı kritik gerilemeler de getirmiştir: **0.3 Mach stabilitesi** varsayılan/standart koşulda 2.62-2.64 cal'a yükselmiş (bandın üstünde, aşırı stabil), **ikincil paraşüt (1.5 m) işlevsiz** hale gelmiş (EJECTION tetikleme + tapalı motor), **iniş hızı** 5.91 → 9.21 m/s'ye çıkmış ve **Cardboard** malzeme eklenmiştir. Apogee 2228.7 → 2298.0/2363.6 m'ye yükselmiş olsa da A2 asgari irtifası (2438 m) hâlâ aşılamamaktadır.

---

## 2. Geometri ve Bileşenler

Tek kademeli, tek parça fiberglas gövde (Ø120 mm, cidar 3.0 mm, motor yuvası), parabolik fiberglas burun (omuz 180 mm = 1.5×OD), 3× plywood kanatçık (kök 120 / uç 30 / yükseklik 135 mm, süpürme 33.6°, cidar 3.0 mm).

| Bileşen | Malzeme | Kütle (kg) | Not |
|---|---|---|---|
| Burun (parabolik) | Fiberglass 1850 | 0.9180 | 250 mm, omuz 180 mm |
| Burun kapağı | Plywood 630 | 0.1033 | bulkhead |
| Mass Component (burun içi) | — | 0.0400 | 0.04 kg |
| Gövde (tek parça) | Fiberglass 1850 | 3.1620 | 1550 mm, motor yuvası |
| Görev yükü (PAYLOAD) | — | 4.0000 | 4.0 kg, tek parça |
| Ana paraşüt | Ripstop nylon | 0.2278 | Ø2.00 m, Cd 0.8, 8×1.2 m |
| Şok kordonu | Tubular nylon | 0.0800 | 695 mm |
| İkincil paraşüt | Ripstop nylon | 0.1216 | Ø1.50 m, Cd 0.8, 6×0.3 m |
| Şok kordonu 2 | Braided nylon | 0.0070 | 55 mm |
| MAPA ×3 | — | 0.1200 | eye bolt |
| Üst kapak | Plywood 630 | 0.1378 | bulkhead |
| Aviyonik kütleleri | — | 0.7170 | 0.187+0.03+0.0+0.5 kg |
| Motor bölmesi (inner tube) | Plywood 630 | 0.0447 | 535 mm, Ø85 |
| Motor bölmesi halkası ×2 | Plywood 630 | 0.0893 | centering ring |
| Kanatçıklar 3× | Plywood 630 | 0.0568 | kök 120 / uç 30 / h 135 mm |
| Kapak / Kapak3 | Plywood / **Cardboard** | 0.1300 | bulkhead |
| Engine Block | **Cardboard** | 0.0753 | 15 mm, Ø114 |
| Küçük kütleler | — | 0.0570 | 0.007 + karabinalar |
| Rail Button ×1 | Aluminum | 0.0169 | tek buton |
| Motor TFL1256WS | Teknofest26 | (gömülü) | Ø75 × 530.6 mm, yakıt 1.905 kg |
| **Toplam** | | **14.000 kg** | **1800.0 mm** |

**Doğrulama (validate):** duplicate-name uyarıları ("KARABİNA" ×4, "Mass Component" ×6) ve rail-velocity-low (13.47 m/s, sim0 koşulunda).

---

## 3. Motor ve Fırlatma Koşulları

**Motor:** TFL1256WS (Teknofest26), Ø75 × 530.6 mm, yakıt kütlesi 1.905 kg, toplam kütle 3.905 kg. Ejection delay = `inf` (tapalı — atma gecikmesi yok). Ateşleme: "Automatic (launch or ejection charge)", gecikme 0.0 s. Digest: `44e3087f74b073af20abd522800b800f` (önceki sürümden aynı).

**Fırlatma koşulları (2 simülasyon):**

| Simülasyon | Rampa (m) | Yükseliş (°) | Rüzgâr (m/s) | İrtifa (m) | Türbülans | Seed |
|---|---|---|---|---|---|---|
| Simulation 1 | 1.0 | 90 | 2.0 (PinkNoise) | 0 | 0.1 | 639242542 |
| TEKNOFEST SİMÜLASYON | 6.0 | 85 | 6.0 (PinkNoise) | 970 | 0.1 | 1298579110 |

Önceki sürümde yalnızca tek simülasyon (90°, 1 m, 0 m, rüzgâr 0) vardı; V3'te Teknofest standardına (85°, 6 m, ~1000 m, rüzgâr 6) uygun ikinci simülasyon eklendi. Varsayılan simülasyon hâlâ 90°.

---

## 4. Kurtarma Sistemi

| # | Paraşüt | Çap | Cd | Hat × ip | Açılma | Durum |
|---|---|---|---|---|---|---|
| 1 | ANA PARAŞÜT | 2.00 m | 0.8 | 8 × 1.2 m | `APOGEE` delay 1.0 s | Çalışıyor |
| 2 | Parachute | 1.50 m | 0.8 | 6 × 0.3 m | `EJECTION` | **İşlevsiz** (motor tapalı) |

**Sorun:** İkincil paraşüt motorun atma gecikmesiyle (EJECTION) tetikleniyor; ancak motor tapalı (ejection charge yok) ve irtifa bazlı (400-600 m) deployment da yok. Simülasyonda tek deployment görülüyor. Görev yüküne ayrı paraşüt atanmamış (4.2.3 ihlali).

---

## 5. Uçuş Sonuçları

| Metrik | Embedded (sim0) | Kendi koşulları (sim0) | Teknofest (sim1) | Standart (85°, 6 m, 1000 m, rüzgâr 0) |
|---|---|---|---|---|
| Apogee (m) | 2297.77 | 2298.00 | 2363.64 | 2350.85 |
| Max hız (m/s) | 237.72 | 237.72 | 238.52 | 239.05 |
| Mach | 0.702 | 0.702 | 0.712 | 0.714 |
| Rampa çıkış hızı (m/s) | 13.47 | 13.47 | 34.09 | 34.10 |
| Kalkış kütlesi (kg) | — | 14.000 | 14.000 | 14.000 |
| İniş hızı (m/s) | 9.04 | 8.99 | 10.81 | 9.21 |
| Uçuş süresi (s) | 270.07 | 270.09 | 265.17 | 263.64 |
| 0.3 Mach stabilite (cal) | — | 2.635 | 2.268 | 2.622 |

Embedded flightdata her iki simülasyon için de koşuyla birebir eşleşiyor (güvenilir simülasyon). Standart koşuda "Recovery device deployment at high speed (20.1 m/s): ANA PARAŞÜT" uyarısı mevcut.

---

## 6. 0.3 Mach Stabilitesi

| Koşul | Stabilite (cal) | t (s) | Mach | İrtifa (m) |
|---|---|---|---|---|
| Own (sim0) | 2.635 | 1.144 | 0.310 | 57.1 |
| Teknofest (sim1) | 2.268 | 1.100 | 0.300 | 52.4 |
| Standart | 2.622 | 1.144 | 0.314 | 56.9 |

Şartname bandı 1.5-2.5 cal. Teknofest koşulunda band içinde; varsayılan/standart koşulda bandın üstünde (2.62-2.64). Burnout stabilitesi ~3.30-3.35 cal (aşırı stabil bölgeye yakın).

---

## 7. Şartname Kontrolü (24 madde)

| # | Madde | Gereksinim | Durum | Kanıt |
|---|---|---|---|---|
| 1 | 3.2.17 | asgari irtifa (A1 1219 / A2 2438) | KISMİ | 2298-2364 m; A1 OK, A2 FAIL |
| 2 | 4.1.33 | görev yükü adı "PAYLOAD" | OK | Ad "PAYLOAD" |
| 3 | 4.1.33 | görev yükü ≥4 kg, tek parça | OK | 4.0 kg |
| 4 | 4.1.35 | fırlatma yükseliş açısı 85° | OK | Teknofest sim 85° mevcut |
| 5 | 4.1.6 | tüm bileşenler paraşütle kurtarma | ŞÜPHELİ | 2 paraşüt; ikincisi işlevsiz |
| 6 | 4.2.3 | görev yükü ayrı paraşüt | FAIL | Ayrı görev yükü paraşütü yok |
| 7 | 4.2.6 | birincil paraşüt 9-20 m/s | UYARI | Deploy anında 20.1 m/s |
| 8 | 4.2.7 | ikincil paraşüt iniş 5-9 m/s | FAIL | İkincil işlevsiz; iniş 8.99-10.81 m/s |
| 9 | 4.2.8 | görev yükü paraşütü 9-20 m/s | FAIL | Ayrı görev yükü paraşütü yok |
| 10 | 4.1.7 | görev yükü apogee sonrası ≤2s ayrılma | OK | Deploy delay 1.0 s |
| 11 | 4.1.8 | ikincil paraşüt 400-600 m | FAIL | EJECTION tetikleme, irtifa bazlı deployment yok |
| 12 | 4.2.2 | paraşüt kurtarma | OK | 2 paraşüt mevcut |
| 13 | 4.4.2 | sabit gövde çapı | OK | 120 mm sabit, transition yok |
| 14 | 4.4.5 | 0.3 Mach stabilite 1.5-2.5 cal | UYARI | 2.635 / 2.268 / 2.622 |
| 15 | 4.4.8 | rampa çıkış hızı (A1 15 / A2 25) | KISMİ | Own 13.47 (FAIL), Teknofest/Std 34.09 (OK) |
| 16 | 4.5.2 | havalandırma deliği 3.0-4.5 mm | FAIL | 0 delik |
| 17 | 4.5.11 | burun omuzluğu ≥1.5×OD | OK | 180 mm = 1.5×120 |
| 18 | 4.5.15 | en az 2 fırlatma kılavuz butonu | FAIL | 1 buton |
| 19 | 4.5.16 | CG butonlar arasında | N/A | Tek buton |
| 20 | 4.3.2 | görev yükü ≥4 kg | OK | 4.0 kg |
| 21 | 4.4.6 | dış sensör/anten/kamera hariç çıkıntı yok | OK | Bileşen yok |
| 22 | 4.5.5 | yasaklı malzeme yok | UYARI | Cardboard: KAPAK3 ve Engine Block |
| 23 | 4.1.10/4.1.18 | motor kategori uyumu | UYARI | TFL1256WS = A1 motoru; A2/A4 için M1850 |
| 24 | 4.1.30 | OpenRocket simülasyon çıktısı | OK | Embedded flightdata (2 sim) koşuyla eşleşiyor |

---

## 8. Önceki Sürümle (BAŞLI 3) Karşılaştırma

| Metrik | BAŞLI 3 | BAŞLI 3 V3 | Değişim |
|---|---|---|---|
| Toplam uzunluk (mm) | 2009.5 | 1800.0 | −209.5 |
| Kalkış kütlesi (kg) | 14.375 | 14.000 | −0.375 |
| Gövde yapısı | 3 parça (üst+aviyonik+alt) | Tek parça 1550 mm | sadeleşti |
| Apogee own (m) | 2228.75 | 2298.00 | +69.3 |
| Apogee teknofest/std (m) | 2276.45 (std) | 2363.64 / 2350.85 | +87.2 / +74.4 |
| Rampa çıkış own (m/s) | 13.09 | 13.47 | +0.38 |
| Rampa çıkış std (m/s) | 33.10 | 34.10 | +1.00 |
| 0.3 Mach stabilite own (cal) | 2.069 | 2.635 | +0.566 (kötüleşti) |
| 0.3 Mach stabilite std (cal) | 2.203 | 2.622 | +0.419 (kötüleşti) |
| Stabilite kalkışta (cal) | 0.986 (FAIL) | 1.517 (OK) | +0.531 (iyileşti) |
| Burnout stabilite (cal) | 2.982 | 3.318 | +0.336 |
| İniş hızı own (m/s) | 6.00 | 8.99 | +2.99 (kötüleşti) |
| İniş hızı std (m/s) | 5.91 | 9.21 | +3.30 (kötüleşti) |
| Uçuş süresi own (s) | 200.14 | 270.09 | +69.95 |
| Paraşüt sayısı / çaplar | 2 (1.0 m + 3.0 m) | 2 (2.0 m + 1.5 m) | küçüldü |
| Paraşüt deployment | drift: APOGEE+1.5s; main: ALTITUDE 500 m | ANA: APOGEE+1.0s; 2.: EJECTION (işlevsiz) | irtifa bazlı deployment kayboldu |
| Görev yükü adı | "FAYDALI YÜK" (FAIL) | "PAYLOAD" (OK) | düzeltildi |
| Havalandırma deliği | 0 | 0 | değişmedi |
| Fırlatma kılavuz butonu | 0 | 1 | +1 (kısmi) |
| Yasaklı malzeme | yok | Cardboard ×2 | yeni sorun |
| Motor | TFL1256WS | TFL1256WS | aynı |
| Fırlatma koşulları sim | tek (90°) | iki (90° + 85° Teknofest) | iyileşti |

**İyileşmeler:** görev yükü adlandırması (4.1.33), kalkış stabilitesi (0.99→1.52), Teknofest simülasyonu eklenmesi, apogee (+69/+87 m), gövde sadeleşmesi, rail butonu (+1), embedded flightdata güvenilirliği.

**Kötüleşmeler:** 0.3 Mach stabilitesi (2.07/2.20 → 2.64/2.62, aşırı stabil), ikincil paraşüt işlevsiz (EJECTION + tapalı motor), iniş hızı (5.91 → 9.21), Cardboard malzeme eklenmesi, bileşen ad tekrarları, uçuş süresi (+70 s), iniş mesafesi (+230/+1265 m).

**Net:** V3 revizyonu görev yükü adlandırması ve kalkış stabilitesi konularında iyileşmiş; ancak 0.3 Mach stabilitesi aşırı stabil bölgeye kaymış, ikincil paraşüt işlevsiz hale gelmiş, iniş hızı artmış ve Cardboard malzeme eklenmiş. Kurtarma sistemi (4.2.3, 4.1.8) şartnameye daha az uyumlu hale gelmiştir.

---

## 9. Öneriler

1. **Stabiliteyi azalt:** 0.3 Mach stabilitesi 2.62-2.64 cal → 1.8-2.2 cal bandına çekmek için kanatçık alanını azalt veya CG'yi ileriye al (burun ağırlığı/motor pozisyonu). Aşırı stabil roket weathercocking riski taşır.
2. **Kurtarma sistemini yeniden tasarla:** İkincil paraşütü EJECTION yerine `ALTITUDE` (400-600 m) ile tetikle; motor tapalı olduğundan EJECTION çalışmaz. Ana paraşüt çapını 2.0 → 2.5-3.0 m'ye çıkar (iniş 5-9 m/s için). Görev yüküne ayrı paraşüt ekle (4.2.3).
3. **Havalandırma deliği aç:** 3 adet 3.0-4.5 mm delik (ön/orta/arka) ekle (4.5.2).
4. **İkinci rail butonu ekle:** En az 2 buton (4.5.15); CG iki buton arasında olmalı (4.5.16).
5. **Cardboard'u değiştir:** KAPAK3 ve Engine Block'ı plywood/fiberglas ile değiştir (4.5.5).
6. **Bileşen adlarını benzersiz yap:** "KARABİNA" ×4 ve "Mass Component" ×6 → benzersiz adlar (validate uyarısı).
7. **Motoru M1850'ye geçir (A2/A4 için):** TFL1256WS = A1 motoru; A2/A4 kategorisinde yarışılacaksa M1850 (apogee ~5800 m) gerekir. Apogee 2364 m → ~5800 m'ye çıkar.
8. **Varsayılan simülasyonu 85°'ye güncelle:** Teknofest simülasyonunu varsayılan yap veya 90° simülasyonu kaldır.

---

## 10. Çıktı Dosyaları

- **Parse verisi:** `designs/BAŞLI3v3_eval.json`
- **Wiki kaynağı:** `wiki/sources/basli-3v3-roket.md`
- **Önceki sürüm (karşılaştırma):** `designs/BAŞLI3_eval.json`, `wiki/sources/basli-3-roket.md`
- **Detaylı rapor:** `/home/kaneki/openrocket-agent/incelenek/BAŞLI3v3_RAPOR.md`
- **Kaynak .ork:** `/home/kaneki/openrocket-agent/incelenek/BAŞLI 3v3roket.ork.zip`
