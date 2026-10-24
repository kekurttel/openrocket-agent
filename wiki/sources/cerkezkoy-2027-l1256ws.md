---
type: source
title: "Çerkezköy 2027.ork — Çerkezköy (L1256WS)"
status: parsed
created: 2026-10-22
updated: 2026-10-22
tags: [roket, teknofest-2026, a1, l1256ws, openrocket]
---

# Çerkezköy 2027.ork (Çerkezköy, L1256WS)

**Kaynak dosya:** `örnek-roket/Çerkezköy 2027.ork`
**Takım:** Çerkezköy  |  **Motor:** TFL1256WS (Teknofest26)  |  **Kategori:** A1 (L1256WS)
**Toplam uzunluk:** 1412 mm  |  **Toplam kalkış kütlesi:** 11.352 kg

## Kütle ve Geometri

Çetin 04 mimarisinin bir varyantı: aynı Ø97 mm gövde ve Ø1.50/1.10 m paraşüt
düzeni, ama **daha uzun gövde** (1.165 m) ve **daha uzun burun** (220 mm) +
**daha geniş kanatlar** (kök 158 / uç 25 / yük 78 mm, süpürme 64°). Apogee
3699.1 m — 2027 A1_1'den (3656.2) +43 m daha yüksek.

| Bileşen | Malzeme | Geometri | Kütle (kg) |
|---|---|---|---|
| Burun (HAACK) | Karbon 1550 | 220 mm, Ø97, cidar 2.0 mm, omuz 145.5 mm | 0.3026 |
| Gövde | Fiberglas 1850 | 1165 mm, Ø97, cidar 1.5 mm, motor yuvası | 0.9699 |
| Kanatlar 3× | Alüminyum 2700 | kök 158 / uç 25 / yük 78 mm, süpürme 64°, 3.0 mm | 0.1820 |
| Paraşütler (2) | Ripstop nylon | Ø1.50 / Ø1.10 m | 0.3291 |
| Aviyonik (Özgün + Ticari UKB, hakem altimetresi, key switch'ler) | — | — | 0.4410 |
| Payload + destek + mapalar + centering ring'ler | — | — | ~0.70 |
| Motor TFL1256WS | — | 75 × 530.6 mm | 3.9050 |
| **Toplam** | | 1412 mm | **11.3521** |

## Fırlatma Koşulları

Rampa 6.0 m, 85° yükseliş (5° düşeyden), rüzgâr 0, fırlatma irtifası 970 m,
türbülans 0, seed 1.

## Kurtarma Sistemi (2 paraşüt — A1 bütünsel)

| # | Paraşüt | Çap | Cd | Hat × ip | Açılma | Ölçülen iniş (kendi koşusu) |
|---|---|---|---|---|---|---|
| 1 | Ana Paraşüt | 1.50 m | 0.8 | 12 × 2.40 m | `APOGEE` 0 s | 8.73 m/s |
| 2 | Payload Paraşütü | 1.10 m | 0.8 | 8 × 1.65 m | `APOGEE` 0 s | 8.73 m/s |

## Uçuş Sonuçları

| Metrik | Dosyada kayıtlı (`<flightdata>`) | Kendi koşullarıyla yeniden koşu | Standart koşul koşusu |
|---|---|---|---|
| Apogee (m) | **3699.1** | 3699.7 | 3674.9 |
| Max hız (m/s) | 315.8 | 316.2 | 316.2 |
| Mach | 0.944 | 0.946 | 0.946 |
| Rampa çıkış hızı (m/s) | 37.35 | 37.36 | 37.36 |
| Kalkış kütlesi (kg) | — | 11.352 | 11.352 |
| İniş (yer) hızı (m/s) | 10.57 | 8.73 | 8.73 |
| Uçuş süresi (s) | 415.2 | 415.2 | 412.2 |

## 0.3 Mach Stabilitesi

**2.055 cal** (t = 0.829 s, Mach 0.306, irtifa 39.7 m) — 1.5–2.5 kal bandında
GEÇTİ. Burnout stabilitesi **3.25 cal** (aşırı stabil).

## Şartname Kontrolü (A1 kategorisi)

| Madde | Gereksinim | Durum | Kanıt |
|---|---|---|---|
| 4.1.7 | payload apogee'den ≤ 2 s sonra ayrılır | GEÇTİ | her iki paraşüt `APOGEE` 0 s |
| 4.2.4 | A1'de bütünsel kurtarma tek paraşütle | MODELLENMEDİ | iki paraşüt modelde var |
| 4.2.8 | payload inişi 9–20 m/s | GEÇTİ | 8.73 m/s (yer hızı; paraşüt hızı 9.52 m/s) |
| 4.2.16 | her paraşüt farklı ve koyu renk | MODELLENMEDİ | renk modelde yok |
| 4.3.2 | payload ≥ 4.0 kg | GEÇTİ | 4.010 kg |
| 4.4.2 | sabit dış çap, boat tail yok | GEÇTİ | tek Ø97 mm gövde |
| 4.4.5 | 0.3 Mach 1.5–2.5 cal | GEÇTİ | 2.055 cal |
| 4.4.8 | rampa çıkışı ≥ 25 m/s | GEÇTİ | 37.36 m/s |
| 4.5.2 | 3× 3.0–4.5 mm delik | MODELLENMEDİ | `Hole` yok |
| 4.5.5 | PVC/kraft/PLA yasak | GEÇTİ | karbon, fiberglas, alüminyum, Delrin, ripstop |
| 4.5.11 | burun omuzluğu ≥ 1.5× dış çap | GEÇTİ | 145.5 mm = 1.500×97 |
| 4.5.15 | ≥ 2 ray butonu | GEÇTİ | 2 |
| 4.1.33 | görev yükü "PAYLOAD" adıyla | KALDI | ad "Payload" |
| 4.1.35 | 85° yükseliş | GEÇTİ | rampa 6 m, 85° |
| 3.2.17 | asgari irtifa 4000 ft (1219 m) | GEÇTİ | 3699.1 m |

## Tasarımın Düşüncesi

Çetin 04'ün **daha uzun gövdeli ve daha geniş kanatlı** varyantı. Gövde 1.165 m
(1.20 → 1.165, biraz kısaltılmış) ama kanatlar daha geniş (158/25/78 mm) →
sürükleme artmış, apogee **3699.1 m** — 2027 A1_1'den (3656.2) +43 m daha
yüksek, Altınok'tan (3685.4) +14 m daha yüksek.

## İlgili Sayfalar

[[motor-l1256ws]] · [[takim-cetin]] · [[2027-a1-1-cetin-04-l1256ws]] ·
[[altinok-cetin-04-l1256ws]] · [[a1-l1256ws-ailesi]]
