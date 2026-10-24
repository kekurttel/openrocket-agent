---
type: source
title: "Altınok Roket Takımı - Çetin 04.ork — Çetin 04 (L1256WS)"
status: parsed
created: 2026-10-22
updated: 2026-10-22
tags: [roket, teknofest-2026, a1, l1256ws, openrocket]
---

# Altınok Roket Takımı – Çetin 04.ork (Çetin 04, L1256WS)

**Kaynak dosya:** `örnek-roket/Altınok Roket Takımı - Çetin 04.ork`
**Takım:** Çetin 04  |  **Motor:** TFL1256WS (Teknofest26)  |  **Kategori:** A1 (L1256WS)
**Toplam uzunluk:** 1453 mm  |  **Toplam kalkış kütlesi:** 11.384 kg

## Kütle ve Geometri

`2027 A1_1`'in **kopyası** (aynı gövde Ø97 mm, 1.20 m, aynı paraşüt düzeni),
yalnız **burun biraz daha uzun** (222 mm vs 200 mm) ve **kanatlar daha ince**
(kök 158 / uç 30 / yük 74 mm, süpürme 65°). Apogee'de +29 m fark.

| Bileşen | Malzeme | Geometri | Kütle (kg) |
|---|---|---|---|
| Burun (HAACK) | Karbon 1550 | 222 mm, Ø97, cidar 2.0 mm, omuz 145.5 mm | 0.3040 |
| Gövde | Fiberglas 1850 | 1200 mm, Ø97, cidar 1.5 mm, motor yuvası | 0.9991 |
| Kanatlar 3× | Alüminyum 2700 | kök 158 / uç 30 / yük 74 mm, süpürme 65°, 3.0 mm | 0.1782 |
| Paraşütler (2) | Ripstop nylon | Ø1.50 / Ø1.10 m | 0.3291 |
| Aviyonik (Özgün + Ticari UKB, hakem altimetresi, key switch'ler) | — | — | 0.4410 |
| Payload + destek + mapalar + centering ring'ler | — | — | ~0.70 |
| Motor TFL1256WS | — | 75 × 530.6 mm | 3.9050 |
| **Toplam** | | 1453 mm | **11.3844** |

## Fırlatma Koşulları

Rampa 6.0 m, 85° yükseliş (5° düşeyden), rüzgâr 0, fırlatma irtifası 970 m,
türbülans 0, seed 1.

## Kurtarma Sistemi (2 paraşüt — A1 bütünsel)

| # | Paraşüt | Çap | Cd | Hat × ip | Açılma | Ölçülen iniş (kendi koşusu) |
|---|---|---|---|---|---|---|
| 1 | Ana Paraşüt | 1.50 m | 0.8 | 12 × 2.40 m | `APOGEE` 0 s | 8.74 m/s |
| 2 | Payload Paraşütü | 1.10 m | 0.8 | 8 × 1.65 m | `APOGEE` 0 s | 8.74 m/s |

## Uçuş Sonuçları

| Metrik | Dosyada kayıtlı (`<flightdata>`) | Kendi koşullarıyla yeniden koşu | Standart koşul koşusu |
|---|---|---|---|
| Apogee (m) | **3685.4** | 3686.4 | 3661.7 |
| Max hız (m/s) | 314.9 | 315.3 | 315.3 |
| Mach | 0.941 | 0.943 | 0.941 |
| Rampa çıkış hızı (m/s) | 37.23 | 37.24 | 37.24 |
| Kalkış kütlesi (kg) | — | 11.384 | 11.384 |
| İniş (yer) hızı (m/s) | 10.44 | 8.74 | 8.74 |
| Uçuş süresi (s) | 413.2 | 413.2 | 410.2 |

## 0.3 Mach Stabilitesi

**2.070 cal** (t = 0.819 s, Mach 0.306, irtifa 39.7 m) — 1.5–2.5 kal bandında
GEÇTİ. Burnout stabilitesi **3.31 cal** (aşırı stabil).

## Şartname Kontrolü (A1 kategorisi)

| Madde | Gereksinim | Durum | Kanıt |
|---|---|---|---|
| 4.1.7 | payload apogee'den ≤ 2 s sonra ayrılır | GEÇTİ | her iki paraşüt `APOGEE` 0 s |
| 4.2.4 | A1'de bütünsel kurtarma tek paraşütle | MODELLENMEDİ | iki paraşüt modelde var |
| 4.2.8 | payload inişi 9–20 m/s | GEÇTİ | 8.74 m/s (yer hızı; paraşüt hızı 9.53 m/s) |
| 4.2.16 | her paraşüt farklı ve koyu renk | MODELLENMEDİ | renk modelde yok |
| 4.3.2 | payload ≥ 4.0 kg | GEÇTİ | 4.010 kg |
| 4.4.2 | sabit dış çap, boat tail yok | GEÇTİ | tek Ø97 mm gövde |
| 4.4.5 | 0.3 Mach 1.5–2.5 cal | GEÇTİ | 2.070 cal |
| 4.4.8 | rampa çıkışı ≥ 25 m/s | GEÇTİ | 37.24 m/s |
| 4.5.2 | 3× 3.0–4.5 mm delik | MODELLENMEDİ | `Hole` yok |
| 4.5.5 | PVC/kraft/PLA yasak | GEÇTİ | karbon, fiberglas, alüminyum, Delrin, ripstop |
| 4.5.11 | burun omuzluğu ≥ 1.5× dış çap | GEÇTİ | 145.5 mm = 1.500×97 |
| 4.5.15 | ≥ 2 ray butonu | GEÇTİ | 2 |
| 4.1.33 | görev yükü "PAYLOAD" adıyla | KALDI | ad "Payload" |
| 4.1.35 | 85° yükseliş | GEÇTİ | rampa 6 m, 85° |
| 3.2.17 | asgari irtifa 4000 ft (1219 m) | GEÇTİ | 3685.4 m |

## Tasarımın Düşüncesi

`2027 A1_1`'in kopyası: burun biraz uzatılmış (200→222 mm) ve kanatlar biraz
inceleştirilmiş (süpürme 61.3→65°, uç 48→30 mm). Sonuç: **+29 m** apogee
(3656.2 → 3685.4) ve stabilite 2.593 → 2.070 cal (daha dengeli). Kütle
neredeyse aynı (11.397 vs 11.384 kg). Küçük değişikliklerin bile apogee'yi
etkilediğini gösteren güzel bir örnek.

## İlgili Sayfalar

[[motor-l1256ws]] · [[takim-cetin]] · [[2027-a1-1-cetin-04-l1256ws]] ·
[[ucok-cetin-05-l1256ws]] · [[a1-l1256ws-ailesi]]
