---
type: source
title: "BAŞLI 3 (Ahmet Efe BAŞLI) — TFL1256WS"
status: parsed
created: 2026-10-23
updated: 2026-10-23
tags: [roket, teknofest-2026, a1, tfl1256ws, openrocket, tek-kademeli, basli]
---

# BAŞLI 3 (Ahmet Efe BAŞLI) — TFL1256WS

**Kaynak dosya:** `BAŞLI 3 roket.ork.zip` (içinde `rocket.ork`)  
**Takım/Tasarımcı:** Ahmet Efe BAŞLI  |  **Motor:** TFL1256WS (Teknofest26)  |  **Kategori (motor bazlı):** A1 (Lise)  
**Toplam uzunluk:** 2009.5 mm  |  **Toplam kalkış kütlesi:** 14.375 kg  |  **Gövde çapı:** Ø120 mm

## Kütle ve Geometri

Tek kademeli, 3 parçalı gövde (üst gövde + aviyonik gövde + alt gövde), fiberglas Ø120 mm gövde, parabolik fiberglas burun, 3× plywood kanatçık, motor bölmesi (plywood inner tube). Görev yükü 4.0 kg "FAYDALI YÜK" (ad şartnameye aykırı).

| Bileşen | Malzeme | Geometri | Kütle (kg) |
|---|---|---|---|
| Burun (parabolik) | Fiberglass 1850 | 250 mm, Ø120, cidar 3.0 mm, omuz 180 mm | 0.9180 |
| Burun kapağı | Plywood 630 | bulkhead | 0.1033 |
| Üst gövde | Fiberglass 1850 | 700 mm, Ø120, cidar 3.0 mm | 1.4280 |
| Görev yükü (FAYDALI YÜK) | — | 125 mm, Ø105, 4.0 kg | 4.0000 |
| Sürüklenme paraşütü | Ripstop nylon | Ø1.00 m, Cd 0.8, 8×1.2 m | 0.0699 |
| Şok kordonu | Tubular nylon | 605 mm | 0.0800 |
| Aviyonik gövde | Fiberglass 1850 | 200 mm, Ø120, cidar 3.0 mm | 0.4080 |
| Üst-alt gövde birleştirme (TubeCoupler) | Plywood 630 | coupler | 0.2636 |
| Üst kapak ×2 | Plywood 630 | bulkhead | 0.2067 |
| Aviyonik | — | 185 mm, Ø105, 0.5 kg | 0.5000 |
| Alt gövde | Fiberglass 1850 | 850 mm, Ø120, cidar 3.0 mm, motor yuvası | 1.7340 |
| Kanatçıklar 3× | Plywood 630 | kök 120 / uç 30 / yükseklik 105 mm, süpürme 46.2°, 3.0 mm | 0.0442 |
| Motor bölmesi (inner tube) | Plywood 630 | 535 mm, Ø85, cidar 0.5 mm | 0.0447 |
| Motor bölmesi halkası ×2 | Plywood 630 | centering ring | 0.0893 |
| Ana paraşüt | Ripstop nylon | Ø3.00 m, Cd 0.8, 12×2.5 m | 0.5786 |
| Şok kordonu 2 | Braided nylon | 225 mm | 0.0014 |
| Motor TFL1256WS | Teknofest26 | Ø75 × 530.6 mm, yakıt 1.905 kg | (gömülü) |
| **Toplam** | | 2009.5 mm | **14.375** |

## Fırlatma Koşulları (tasarımda kayıtlı)

Rampa 1.0 m, yükseliş 90° (düşeyden 0°), rüzgâr (null → 0), fırlatma irtifası 0 m, türbülans (null), seed 240960812. **Şartname standardı (85°, 6 m rampa, 1000 m, rüzgâr 0) ile uyumsuz.**

## Kurtarma Sistemi (2 paraşüt)

| # | Paraşüt | Çap | Cd | Hat × ip | Açılma | Ölçülen iniş (standart koşu) |
|---|---|---|---|---|---|---|
| 1 | Sürüklenme paraşütü | 1.00 m | 0.8 | 8 × 1.2 m | `APOGEE` delay 1.5 s (22.88 s) | — |
| 2 | Ana paraşüt | 3.00 m | 0.8 | 12 × 2.5 m | `ALTITUDE` 500 m | 5.91 m/s |

**Notlar:** Birincil paraşüt apogee'den 1.5 s sonra açılıyor (≤2 s şartı OK). İkincil paraşüt 500 m'de açılıyor (400–600 m bandı OK). Ancak görev yüküne ayrı paraşüt atanmamış (4.2.3 ihlali). Birincil paraşüt deploy anında 22.4 m/s (high-speed warning; 9–20 m/s bandı aşıyor).

## Uçuş Sonuçları

| Metrik | Dosyada kayıtlı (`<flightdata>`) | Kendi koşullarıyla yeniden koşu | Standart koşul koşusu (85°, 6 m, 1000 m) |
|---|---|---|---|
| Apogee (m) | **2228.67** | 2228.75 | 2276.45 |
| Max hız (m/s) | 231.11 | 231.11 | 232.35 |
| Mach | 0.682 | 0.682 | 0.694 |
| Rampa çıkış hızı (m/s) | 13.09 | 13.09 | 33.10 |
| Kalkış kütlesi (kg) | — | 14.375 | 14.375 |
| İniş (yer) hızı (m/s) | 5.91 | 6.00 | 5.91 |
| Uçuş süresi (s) | 200.15 | 200.14 | 194.19 |

## 0.3 Mach Stabilitesi

**Own koşu:** 2.069 cal (t = 1.157 s, Mach 0.305, irtifa 56.8 m)  
**Standart koşu:** 2.203 cal (t = 1.144 s, Mach 0.305, irtifa 55.2 m)  
Her iki koşuda da 1.5–2.5 kal bandında GEÇTİ. Burnout stabilitesi ~3.0 cal (aşırı stabil bölgeye yakın).

## Şartname Kontrolü (24 madde)

| # | Madde | Gereksinim | Durum | Kanıt |
|---|---|---|---|---|
| 1 | 3.2.17 | asgari irtifa (A1 1219 m / A2 2438 m) | KISMİ | Own 2229 m; A1 asgari OK, A2 asgari FAIL |
| 2 | 4.1.33 | görev yükü adı "PAYLOAD" | FAIL | Ad "FAYDALI YÜK" |
| 3 | 4.1.33 | görev yükü ≥4 kg, tek parça | OK | 4.0 kg |
| 4 | 4.1.35 | fırlatma yükseliş açısı 85° | FAIL | Tasarımda 90° |
| 5 | 4.1.6 | tüm bileşenler paraşütle kurtarma | ŞÜPHELİ | 2 paraşüt; görev yükü ayrı paraşüt yok |
| 6 | 4.2.3 | görev yükü ayrı paraşütle kurtarma | FAIL | Ayrı görev yükü paraşütü yok |
| 7 | 4.2.6 | birincil paraşüt 9–20 m/s | UYARI | Deploy anında 22.4 m/s (high-speed warning) |
| 8 | 4.2.7 | ikincil paraşüt iniş 5–9 m/s | OK | 5.91 m/s |
| 9 | 4.2.8 | görev yükü paraşütü 9–20 m/s | FAIL | Ayrı görev yükü paraşütü yok |
| 10 | 4.1.7 | görev yükü apogee sonrası ≤2 s ayrılma | OK | Drift deploy delay 1.5 s |
| 11 | 4.1.8 | ikincil paraşüt 400–600 m | OK | 500 m |
| 12 | 4.2.2 | paraşüt kurtarma | OK | 2 paraşüt mevcut |
| 13 | 4.4.2 | sabit gövde çapı | OK | 120 mm sabit, transition yok |
| 14 | 4.4.5 | 0.3 Mach stabilite 1.5–2.5 cal | OK | Own 2.069 / Standart 2.203 |
| 15 | 4.4.8 | rampa çıkış hızı (A1 15 / A2 25 m/s) | KISMİ | Own 13.1 (FAIL), standart 33.1 (OK) |
| 16 | 4.5.2 | havalandırma deliği 3.0–4.5 mm | FAIL | 0 delik |
| 17 | 4.5.11 | burun omuzluğu ≥1.5×OD | OK | 180 mm = 1.5×120 |
| 18 | 4.5.15 | en az 2 fırlatma kılavuz butonu | FAIL | 0 buton |
| 19 | 4.5.16 | CG butonlar arasında | N/A | Buton yok |
| 20 | 4.3.2 | görev yükü ≥4 kg | OK | 4.0 kg |
| 21 | 4.4.6 | dış sensör/anten/kamera hariç çıkıntı yok | OK | Bileşen yok |
| 22 | 4.5.5 | yasaklı malzeme yok | OK | Fiberglass/plywood/nylon |
| 23 | 4.1.10/4.1.18 | motor kategori uyumu | UYARI | TFL1256WS (A1 motoru) kullanılıyor; A2/A4 için M1850 gerekir |
| 24 | 4.1.30 | OpenRocket simülasyon çıktısı | OK | Embedded flightdata mevcut ve koşuyla eşleşiyor |

## Değerlendirme

**Güçlü yönler:**
- 0.3 Mach stabilitesi 2.07–2.20 cal (şartname bandında).
- Standart koşulda rampa çıkış 33.1 m/s (A1 15 m/s eşiğini aşıyor).
- İniş hızı 5.91 m/s (5–9 m/s bandında).
- Gövde çapı sabit 120 mm, transition yok.
- Yasaklı malzeme yok; burun omuzluğu 1.5×OD şartını tam karşılıyor.
- Embedded flightdata koşuyla birebir eşleşiyor (güvenilir simülasyon).

**Zayıf yönler / eksikler:**
- Görev yükü adı "FAYDALI YÜK" (şartname "PAYLOAD" ister) → elenme riski.
- Görev yüküne ayrı paraşüt yok (4.2.3) → elenme riski.
- Fırlatma koşulları standartla uyumsuz (90° yükseliş, 1 m rampa, 0 m irtifa); gerçek atışta performans değişir.
- Havalandırma deliği ve fırlatma kılavuz butonu yok (4.5.2, 4.5.15) → elenme riski.
- Birincil paraşüt deploy anında 22.4 m/s (9–20 m/s bandı dışı).
- Motor TFL1256WS = A1 (Lise) kategorisi motoru; A2/A4 için M1850 gerekir. Apogee 2229 m A1 asgari (1219 m) aşıyor ama A2 asgari (2438 m) aşılamıyor.

**Sonuç:** Tasarım A1 (Lise) kategorisinde asgari irtifayı (1219 m) aşıyor ve stabilite/rampa çıkış/iniş hızı kriterlerini karşılıyor; ancak görev yükü adlandırması, ayrı görev yükü paraşütü, havalandırma deliği, fırlatma kılavuz butonu ve fırlatma koşulları standart uyumsuzlukları nedeniyle şartnameye tam uyumlu değil. A2/A4 kategorisi için motor ve irtifa yetersiz.

## İlgili Sayfalar

[[motor-l1256ws]] · [[en-yuksek-irtifa]] · [[m1850-rekabet]] · [[bozok-cetin-06-m1850]]
