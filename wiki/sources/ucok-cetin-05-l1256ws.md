---
type: source
title: "Üçok Roket Takımı - Çetin 05.ork — Çetin 05 (L1256WS)"
status: parsed
created: 2026-10-22
updated: 2026-10-22
tags: [roket, teknofest-2026, a1, l1256ws, openrocket]
---

# Üçok Roket Takımı – Çetin 05.ork (Çetin 05, L1256WS)

**Kaynak dosya:** `örnek-roket/Üçok Roket Takımı - Çetin 05.ork`
**Takım:** Çetin 05  |  **Motor:** TFL1256WS (Teknofest26)  |  **Kategori:** A1 (L1256WS)
**Toplam uzunluk:** 1453 mm  |  **Toplam kalkış kütlesi:** 11.244 kg

## Kütle ve Geometri

**L1256WS ailesinin en yükseği.** Çetin 04 (2027 A1_1) ile neredeyse aynı
mimaride ama **daha küçük gövde (Ø85 mm)** ve **daha küçük kanatlar** → daha az
sürükleme → daha yüksek apogee. Tek kademeli.

| Bileşen | Malzeme | Geometri | Kütle (kg) |
|---|---|---|---|
| Burun (HAACK) | Karbon 1550 | 232 mm, Ø85, cidar 2.0 mm, omuz 127.5 mm | 0.2541 |
| Gövde | Fiberglas 1850 | 1195 mm, Ø85, cidar 1.5 mm, motor yuvası | 0.8699 |
| Kanatlar 3× | Alüminyum 2700 | kök 110 / uç 20 / yük 59 mm, süpürme 63°, 3.0 mm | 0.0899 |
| Paraşütler (2) | Ripstop nylon | Ø1.50 / Ø1.10 m | 0.3291 |
| Aviyonik (Özgün + Ticari UKB, hakem altimetresi, key switch'ler) | — | — | 0.4410 |
| Payload + destek + mapalar + centering ring'ler | — | — | ~0.70 |
| Motor TFL1256WS | — | 75 × 530.6 mm | 3.9050 |
| **Toplam** | | 1453 mm | **11.2443** |

## Fırlatma Koşulları

Rampa 6.0 m, 85° yükseliş (5° düşeyden), rüzgâr 0, fırlatma irtifası 970 m,
türbülans 0, seed 1.

## Kurtarma Sistemi (2 paraşüt — A1 bütünsel)

| # | Paraşüt | Çap | Cd | Hat × ip | Açılma | Ölçülen iniş (kendi koşusu) |
|---|---|---|---|---|---|---|
| 1 | Ana Paraşüt | 1.50 m | 0.8 | 12 × 2.40 m | `APOGEE` +1.0 s | 10.46 m/s |
| 2 | Payload Paraşütü | 1.10 m | 0.8 | 8 × 1.65 m | `APOGEE` +1.0 s | 10.46 m/s |

Her iki paraşüt apogee'den 1.0 s sonra açılıyor (A1'de tek paraşütle bütünsel
kurtarma; burada iki paraşüt birlikte açılıyor).

## Uçuş Sonuçları

| Metrik | Dosyada kayıtlı (`<flightdata>`) | Kendi koşullarıyla yeniden koşu | Standart koşul koşusu |
|---|---|---|---|
| Apogee (m) | **4001.4** | 4001.1 | 3976.1 |
| Max hız (m/s) | 322.4 | 322.4 | 322.7 |
| Mach | 0.963 | 0.963 | 0.965 |
| Rampa çıkış hızı (m/s) | 37.75 | 37.75 | 37.75 |
| Kalkış kütlesi (kg) | — | 11.244 | 11.244 |
| İniş (yer) hızı (m/s) | 10.79 | 10.46 | 8.68 |
| Uçuş süresi (s) | 447.4 | 447.4 | 444.2 |

## 0.3 Mach Stabilitesi

**2.065 cal** (t = 0.929 s, Mach 0.319, irtifa 46.5 m) — 1.5–2.5 kal bandında
GEÇTİ. Burnout stabilitesi **3.72 cal** (aşırı stabil).

## Şartname Kontrolü (A1 kategorisi)

| Madde | Gereksinim | Durum | Kanıt |
|---|---|---|---|
| 4.1.7 | payload apogee'den ≤ 2 s sonra ayrılır | GEÇTİ | her iki paraşüt `APOGEE` +1.0 s |
| 4.2.4 | A1'de bütünsel kurtarma tek paraşütle | MODELLENMEDİ | iki paraşüt modelde var (şartname A1 için tek paraşüt ister) |
| 4.2.8 | payload inişi 9–20 m/s | GEÇTİ | 10.46 m/s |
| 4.2.16 | her paraşüt farklı ve koyu renk | MODELLENMEDİ | renk modelde yok |
| 4.3.2 | payload ≥ 4.0 kg | GEÇTİ | 4.010 kg |
| 4.4.2 | sabit dış çap, boat tail yok | GEÇTİ | tek Ø85 mm gövde |
| 4.4.5 | 0.3 Mach 1.5–2.5 cal | GEÇTİ | 2.065 cal |
| 4.4.8 | rampa çıkışı ≥ 25 m/s | GEÇTİ | 37.75 m/s |
| 4.5.2 | 3× 3.0–4.5 mm delik | MODELLENMEDİ | `Hole` yok |
| 4.5.5 | PVC/kraft/PLA yasak | GEÇTİ | karbon, fiberglas, alüminyum, Delrin, ripstop |
| 4.5.11 | burun omuzluğu ≥ 1.5× dış çap | GEÇTİ | 127.5 mm = 1.500×85 |
| 4.5.15 | ≥ 2 ray butonu | GEÇTİ | 2 |
| 4.1.33 | görev yükü "PAYLOAD" adıyla | KALDI | ad "Payload" |
| 4.1.35 | 85° yükseliş | GEÇTİ | rampa 6 m, 85° |
| 3.2.17 | asgari irtifa 4000 ft (1219 m) | GEÇTİ | 4001.4 m |

## Tasarımın Düşüncesi

L1256WS ailesinin **en yükseği**. Çetin 04'ün geometrisini küçülterek (Ø97→85 mm,
gövde 1.20→1.195 m) sürükleme alanını azaltmış; aynı motorla **+345 m** daha
yüksek apogee (3656 → 4001 m). Bedeli: daha küçük payload bölmesi ve daha dar
aviyonik yerleşimi (0.44 kg vs 0.44 kg — aynı).

## İlgili Sayfalar

[[motor-l1256ws]] · [[takim-cetin]] · [[a1-l1256ws-ailesi]] ·
[[2027-a1-1-cetin-04-l1256ws]] · [[altinok-cetin-04-l1256ws]] ·
[[kizlar-bozok-l1256ws]] · [[cerkezkoy-2027-l1256ws]]
