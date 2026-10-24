---
type: source
title: "Kızlar.ork — Bozok Rocket (L1256WS)"
status: parsed
created: 2026-10-22
updated: 2026-10-22
tags: [roket, teknofest-2026, a1, l1256ws, openrocket]
---

# Kızlar.ork (Bozok Rocket, L1256WS)

**Kaynak dosya:** `örnek-roket/Kızlar.ork`
**Takım:** Bozok Rocket  |  **Motor:** TFL1256WS (Teknofest26)  |  **Kategori:** A1 (L1256WS)
**Toplam uzunluk:** 1620 mm  |  **Toplam kalkış kütlesi:** 12.024 kg

## Kütle ve Geometri

**L1256WS ailesinin en ağır ve en düşük irtifalısı.** Ø98 mm gövde (diğer
tasarımlardan 1 mm geniş), **1.40 m uzun gövde** (en uzun), fiberglas burun
(karbon yerine) ve **daha büyük paraşüt** (Ø1.60 m ana). Daha fazla küt
(12.02 kg) ve daha fazla sürükleme → en düşük apogee (3411.1 m).

| Bileşen | Malzeme | Geometri | Kütle (kg) |
|---|---|---|---|
| Burun (HAACK) | Fiberglas 1850 | 220 mm, Ø98, cidar 2.0 mm, omuz 147 mm | 0.3179 |
| Gövde | Fiberglas 1850 | 1400 mm, Ø98, cidar 2.0 mm, motor yuvası | 1.5623 |
| Kanatlar 3× | Alüminyum 2700 | kök 158 / uç 48 / yük 86 mm, süpürme 61.3°, 3.0 mm | 0.2180 |
| Paraşütler (2) | Ripstop nylon | Ø1.60 / Ø1.10 m | 0.3391 |
| Aviyonik (Özgün + Ticari UKB, hakem altimetresi, key switch'ler) | — | — | 0.4410 |
| Payload + destek + mapalar + centering ring'ler | — | — | ~0.70 |
| Motor TFL1256WS | — | 75 × 530.6 mm | 3.9050 |
| **Toplam** | | 1620 mm | **12.0243** |

## Fırlatma Koşulları

Rampa 6.0 m, 85° yükseliş (5° düşeyden), rüzgâr 0, fırlatma irtifası 970 m,
türbülans 0, seed 1.

## Kurtarma Sistemi (2 paraşüt — A1 bütünsel)

| # | Paraşüt | Çap | Cd | Hat × ip | Açılma | Ölçülen iniş (kendi koşusu) |
|---|---|---|---|---|---|---|
| 1 | Ana Paraşüt | 1.60 m | 0.8 | 12 × 2.25 m | `APOGEE` 0 s | 10.46 m/s |
| 2 | Payload Paraşütü | 1.10 m | 0.8 | 8 × 1.65 m | `APOGEE` 0 s | 10.46 m/s |

## Uçuş Sonuçları

| Metrik | Dosyada kayıtlı (`<flightdata>`) | Kendi koşullarıyla yeniden koşu | Standart koşul koşusu |
|---|---|---|---|
| Apogee (m) | **3411.1** | 3411.3 | 3388.6 |
| Max hız (m/s) | 296.4 | 296.7 | 296.7 |
| Mach | 0.885 | 0.887 | 0.887 |
| Rampa çıkış hızı (m/s) | 36.16 | 36.16 | 36.16 |
| Kalkış kütlesi (kg) | — | 12.024 | 12.024 |
| İniş (yer) hızı (m/s) | 10.82 | 10.46 | 8.65 |
| Uçuş süresi (s) | 389.8 | 389.8 | 386.8 |

## 0.3 Mach Stabilitesi

**2.149 cal** (t = 0.819 s, Mach 0.306, irtifa 39.7 m) — 1.5–2.5 kal bandında
GEÇTİ. Burnout stabilitesi **3.29 cal** (aşırı stabil).

## Şartname Kontrolü (A1 kategorisi)

| Madde | Gereksinim | Durum | Kanıt |
|---|---|---|---|
| 4.1.7 | payload apogee'den ≤ 2 s sonra ayrılır | GEÇTİ | her iki paraşüt `APOGEE` 0 s |
| 4.2.4 | A1'de bütünsel kurtarma tek paraşütle | MODELLENMEDİ | iki paraşüt modelde var |
| 4.2.8 | payload inişi 9–20 m/s | GEÇTİ | 10.46 m/s |
| 4.2.16 | her paraşüt farklı ve koyu renk | MODELLENMEDİ | renk modelde yok |
| 4.3.2 | payload ≥ 4.0 kg | GEÇTİ | 4.010 kg |
| 4.4.2 | sabit dış çap, boat tail yok | GEÇTİ | tek Ø98 mm gövde |
| 4.4.5 | 0.3 Mach 1.5–2.5 cal | GEÇTİ | 2.149 cal |
| 4.4.8 | rampa çıkışı ≥ 25 m/s | GEÇTİ | 36.16 m/s |
| 4.5.2 | 3× 3.0–4.5 mm delik | MODELLENMEDİ | `Hole` yok |
| 4.5.5 | PVC/kraft/PLA yasak | GEÇTİ | fiberglas, alüminyum, Delrin, ripstop (burun **fiberglas**, karbon değil) |
| 4.5.11 | burun omuzluğu ≥ 1.5× dış çap | GEÇTİ | 147 mm = 1.500×98 |
| 4.5.15 | ≥ 2 ray butonu | GEÇTİ | 2 |
| 4.1.33 | görev yükü "PAYLOAD" adıyla | KALDI | ad "Payload" |
| 4.1.35 | 85° yükseliş | GEÇTİ | rampa 6 m, 85° |
| 3.2.17 | asgari irtifa 4000 ft (1219 m) | GEÇTİ | 3411.1 m |

## Tasarımın Düşüncesi

En ağır ve en düşük irtifalı L1256WS tasarımı. **Fiberglas burun** (karbon yerine),
**2.0 mm cidar** (1.5 yerine), **1.40 m gövde** (en uzun), **Ø1.60 m ana paraşüt**
(en büyük) → küt (12.02 kg) + sürükleme (Ø98 mm, uzun gövde) → en düşük apogee
(3411.1 m). A1 asgari irtifası 1219 m olduğundan kategori gereksinimini
sağlıyor ama L1256WS ailesinin en kötüsü. **Negatif örnek** olarak değerli.

## İlgili Sayfalar

[[motor-l1256ws]] · [[takim-bozok]] · [[a1-l1256ws-ailesi]] ·
[[2027-a1-1-cetin-04-l1256ws]] · [[ucok-cetin-05-l1256ws]]
