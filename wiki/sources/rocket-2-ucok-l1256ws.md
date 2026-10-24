---
type: source
title: "rocket (2).ork — Üçok (L1256WS)"
status: parsed
created: 2026-10-23
updated: 2026-10-23
tags: [roket, teknofest-2026, a1, l1256ws, openrocket]
---

# rocket (2).ork (Üçok, L1256WS)

**Kaynak dosya:** `örnekroket2/rocket (2).ork`
**Takım:** Üçok  |  **Motor:** TFL1256WS (Teknofest26)  |  **Kategori:** A1 (L1256WS)
**Toplam uzunluk:** 1800 mm  |  **Toplam kalkış kütlesi:** 12.862 kg

## Kütle ve Geometri

`Bozok_Roket_AHR Takım ID 577323.ork` ile **neredeyse aynı** tasarım (aynı
Ø98 mm gövde, aynı kanatlar, aynı paraşüt düzeni). Farklar: gövde biraz daha
uzun (1.55 m vs 1.50 m), aviyonik daha ağır (0.433 kg vs 0.441 kg — aslında
daha hafif), burun fiberglas (aynı). Apogee 2686.3 m — Bozok_Roket (2838.8 m)
ile karşılaştırıldığında **152 m daha düşük**.

| Bileşen | Malzeme | Geometri | Kütle (kg) |
|---|---|---|---|
| Burun (HAACK) | Fiberglas 1850 | 250 mm, Ø98, cidar 2.0 mm, omuz 147 mm | 0.3453 |
| Gövde | Fiberglas 1850 | 1550 mm, Ø98, cidar 2.0 mm, motor yuvası | 1.7296 |
| Kanatlar 3× | Alüminyum 2700 | kök 158 / uç 48 / yük 86 mm, süpürme 61.3°, 3.0 mm | 0.2502 |
| Paraşütler (2) | Ripstop nylon | Ø1.60 / Ø1.10 m | 0.3454 |
| Aviyonik (Özgün + Ticari UKB, hakem altimetresi, key switch'ler) | — | — | 0.4330 |
| Payload + destek + mapalar + centering ring'ler | — | — | ~0.70 |
| Motor TFL1256WS | — | 75 × 530.6 mm | 3.9050 |
| **Toplam** | | 1800 mm | **12.862** |

## Fırlatma Koşulları

Rampa 6.0 m, 85° yükseliş (5° düşeyden), rüzgâr 0, fırlatma irtifası 970 m,
türbülans 0, seed 1.

## Kurtarma Sistemi (2 paraşüt — A1 bütünsel)

| # | Paraşüt | Çap | Cd | Hat × ip | Açılma | Ölçülen iniş (kendi koşusu) |
|---|---|---|---|---|---|---|
| 1 | Ana Paraşüt | 1.60 m | 0.8 | 12 × 2.40 m | `APOGEE` 0 s | 10.46 m/s |
| 2 | Payload Paraşütü | 1.10 m | 0.8 | 8 × 1.65 m | `APOGEE` 0 s | 10.46 m/s |

## Uçuş Sonuçları

| Metrik | Dosyada kayıtlı (`<flightdata>`) | Kendi koşullarıyla yeniden koşu | Standart koşul koşusu |
|---|---|---|---|
| Apogee (m) | **2700.0** | 2701.9 | 2686.3 |
| Max hız (m/s) | 263.0 | 263.0 | 263.4 |
| Mach | 0.785 | 0.785 | 0.787 |
| Rampa çıkış hızı (m/s) | 35.41 | 35.41 | 35.42 |
| Kalkış kütlesi (kg) | — | 12.862 | 12.862 |
| İniş (yer) hızı (m/s) | 10.82 | 10.46 | 8.65 |
| Uçuş süresi (s) | — | — | — |

## 0.3 Mach Stabilitesi

**2.203 cal** (t = 0.819 s, Mach 0.306, irtifa 39.7 m) — 1.5–2.5 kal bandında
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
| 4.4.5 | 0.3 Mach 1.5–2.5 cal | GEÇTİ | 2.203 cal |
| 4.4.8 | rampa çıkışı ≥ 25 m/s | GEÇTİ | 35.41 m/s |
| 4.5.2 | 3× 3.0–4.5 mm delik | MODELLENMEDİ | `Hole` yok |
| 4.5.5 | PVC/kraft/PLA yasak | GEÇTİ | fiberglas, alüminyum, Delrin, ripstop, cardboard (Motor Yatağı) |
| 4.5.11 | burun omuzluğu ≥ 1.5× dış çap | GEÇTİ | 147 mm = 1.500×98 |
| 4.5.15 | ≥ 2 ray butonu | GEÇTİ | 2 |
| 4.1.33 | görev yükü "PAYLOAD" adıyla | KALDI | ad "Payload" |
| 4.1.35 | 85° yükseliş | GEÇTİ | rampa 6 m, 85° |
| 3.2.17 | asgari irtifa 4000 ft (1219 m) | GEÇTİ | 2700.0 m |

## Tasarımın Düşüncesi

`Bozok_Roket_AHR Takım ID 577323.ork` ile **neredeyse aynı** tasarım. Gövde 1.55 m
(1.50 m yerine), aviyonik biraz farklı (0.433 kg vs 0.441 kg). Apogee 2686.3 m —
Bozok_Roket (2838.8 m) ile karşılaştırıldığında **152 m daha düşük**. Gövde 5 cm
daha uzun olmasına rağmen apogee daha düşük — bu, muhtemelen aviyonik kütlesinin
biraz farklı olması veya motor eğrisinin farklı yorumlanması nedeniyle.

**Negatif örnek:** aynı motorla 4001.4 m'ye çıkan Üçok tasarımı varken bu
tasarım 2686.3 m'de kalıyor. Nedenleri:
1. **Fiberglas burun** (karbon yerine) → 0.345 kg.
2. **1.55 m gövde** (1.20 m yerine) → 1.730 kg.
3. **Cardboard motor yatağı** → şartname 4.5.5 ihlali.
4. **Ø1.60 m ana paraşüt** → daha ağır paraşüt + daha düşük iniş hızı.

## İlgili Sayfalar

[[motor-l1256ws]] · [[takim-bozok]] · [[a1-l1256ws-ailesi]] ·
[[bozok-ahr-577323-l1256ws]] · [[kizlar-bozok-l1256ws]] ·
[[en-yuksek-irtifa]]
