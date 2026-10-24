---
type: source
title: "Bozok_Roket_AHR Takım ID 577323.ork — Bozok Rocket (L1256WS)"
status: parsed
created: 2026-10-23
updated: 2026-10-23
tags: [roket, teknofest-2026, a1, l1256ws, openrocket]
---

# Bozok_Roket_AHR Takım ID 577323.ork (Bozok Rocket, L1256WS)

**Kaynak dosya:** `örnekroket2/Bozok_Roket_AHR Takım ID 577323.ork`
**Takım:** Bozok Rocket  |  **Motor:** TFL1256WS (Teknofest26)  |  **Kategori:** A1 (L1256WS)
**Toplam uzunluk:** 1797 mm  |  **Toplam kalkış kütlesi:** 12.839 kg

## Kütle ve Geometri

Çetin 04 / Altınok mimarisinin bir varyantı: Ø98 mm gövde, HAACK burun, alüminyum
kanatlar, 2 paraşüt. **Motor yatağı cardboard** (yasak malzeme). Gövde 1.50 m
(en uzun L1256WS gövde). Apogee 2838.8 m — L1256WS ailesinin en düşüğü.

| Bileşen | Malzeme | Geometri | Kütle (kg) |
|---|---|---|---|
| Burun (HAACK) | Fiberglas 1850 | 250 mm, Ø98, cidar 2.0 mm, omuz 147 mm | 0.3453 |
| Gövde | Fiberglas 1850 | 1500 mm, Ø98, cidar 2.0 mm, motor yuvası | 1.6738 |
| Kanatlar 3× | Alüminyum 2700 | kök 158 / uç 48 / yük 86 mm, süpürme 61.3°, 3.0 mm | 0.2502 |
| Paraşütler (2) | Ripstop nylon | Ø1.60 / Ø1.10 m | 0.3211 |
| Aviyonik (Özgün + Ticari UKB, hakem altimetresi, key switch'ler) | — | — | 0.4410 |
| Payload + destek + mapalar + centering ring'ler | — | — | ~0.70 |
| Motor TFL1256WS | — | 75 × 530.6 mm | 3.9050 |
| **Toplam** | | 1797 mm | **12.839** |

## Fırlatma Koşulları

Rampa 6.0 m, 85° yükseliş (5° düşeyden), rüzgâr 0, fırlatma irtifası 970 m,
türbülans 0, seed 1.

## Kurtarma Sistemi (2 paraşüt — A1 bütünsel)

| # | Paraşüt | Çap | Cd | Hat × ip | Açılma | Ölçülen iniş (kendi koşusu) |
|---|---|---|---|---|---|---|
| 1 | Ana Paraşüt | 1.60 m | 0.8 | 12 × 1.92 m | `APOGEE` 0 s | 10.46 m/s |
| 2 | Payload Paraşütü | 1.10 m | 0.8 | 8 × 1.50 m | `APOGEE` 0 s | 10.46 m/s |

## Uçuş Sonuçları

| Metrik | Dosyada kayıtlı (`<flightdata>`) | Kendi koşullarıyla yeniden koşu | Standart koşul koşusu |
|---|---|---|---|
| Apogee (m) | **2838.8** | 2738.3 | 2821.4 |
| Max hız (m/s) | 271.6 | 271.5 | 271.9 |
| Mach | 0.811 | 0.814 | 0.812 |
| Rampa çıkış hızı (m/s) | 35.68 | 35.68 | 35.69 |
| Kalkış kütlesi (kg) | — | 12.839 | 12.839 |
| İniş (yer) hızı (m/s) | 10.82 | 10.46 | 10.46 |
| Uçuş süresi (s) | — | — | — |

## 0.3 Mach Stabilitesi

**2.396 cal** (t = 0.929 s, Mach 0.319, irtifa 46.5 m) — 1.5–2.5 kal bandında
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
| 4.4.5 | 0.3 Mach 1.5–2.5 cal | GEÇTİ | 2.396 cal |
| 4.4.8 | rampa çıkışı ≥ 25 m/s | GEÇTİ | 35.68 m/s |
| 4.5.2 | 3× 3.0–4.5 mm delik | MODELLENMEDİ | `Hole` yok |
| 4.5.5 | PVC/kraft/PLA yasak | **KALDI** | **Cardboard** malzeme (Motor Yatağı) |
| 4.5.11 | burun omuzluğu ≥ 1.5× dış çap | GEÇTİ | 147 mm = 1.500×98 |
| 4.5.15 | ≥ 2 ray butonu | GEÇTİ | 2 |
| 4.1.33 | görev yükü "PAYLOAD" adıyla | KALDI | ad "Payload" |
| 4.1.35 | 85° yükseliş | GEÇTİ | rampa 6 m, 85° |
| 3.2.17 | asgari irtifa 4000 ft (1219 m) | GEÇTİ | 2838.8 m |

## Tasarımın Düşüncesi

**Çetin 04 mimarisinin kopyası** ama daha **ağır ve daha düşük irtifalı**. Gövde
1.50 m (en uzun L1256WS gövde), fiberglas burun (karbon yerine), Ø1.60 m ana
paraşüt, motor yatağı cardboard (yasak malzeme). Apogee 2838.8 m — L1256WS
ailesinin en düşüğü (Kızlar 3411.1 m, 2027 A1_1 3656.2 m).

**Negatif örnek:** aynı motorla 4001.4 m'ye çıkan Üçok tasarımı varken bu
tasarım 2838.8 m'de kalıyor. Nedenleri:
1. **Fiberglas burun** (karbon yerine) → 0.345 kg (karbon 0.289 kg).
2. **1.50 m gövde** (1.20 m yerine) → 1.674 kg (Çetin 04: 0.999 kg).
3. **Cardboard motor yatağı** → şartname 4.5.5 ihlali.
4. **Ø1.60 m ana paraşüt** → daha ağır paraşüt + daha düşük iniş hızı.

## İlgili Sayfalar

[[motor-l1256ws]] · [[takim-bozok]] · [[a1-l1256ws-ailesi]] ·
[[kizlar-bozok-l1256ws]] · [[2027-a1-1-cetin-04-l1256ws]] ·
[[en-yuksek-irtifa]]
