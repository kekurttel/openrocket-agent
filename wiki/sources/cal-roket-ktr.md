---
type: source
title: "CAL Roket Takımı KTR OpenRocket Dosyası.ork — CAL Roket (3727L1050-P)"
status: parsed
created: 2026-10-23
updated: 2026-10-23
tags: [roket, teknofest-2026, a2, a4, cesaroni, openrocket]
---

# CAL Roket Takımı KTR OpenRocket Dosyası.ork (CAL Roket, 3727L1050-P)

**Kaynak dosya:** `örnekroket2/CAL Roket Takımı KTR OpenRocket Dosyası.ork`
**Takım:** CAL Roket Takımı  |  **Motor:** 3727L1050-P (Cesaroni Technology Inc.)  |  **Kategori:** A2 / A4 (?)
**Toplam uzunluk:** 1945 mm  |  **Toplam kalkış kütlesi:** 17.884 kg

## Kütle ve Geometri

Çok ağır ve karmaşık bir tasarım: Ø140 mm gövde, alüminyum gövde (2.0 mm),
3.0 mm cidar, 4 kanatlı, HAACK burun (ABS, 6 mm cidar), Ø2.60 m ana paraşüt
(Cd 2.2), Ø1.10 m payload paraşütü. Motor Cesaroni 3727L1050-P (Ø75 × 486 mm,
1.863 kg yakıt). **En düşük apogee: 1522.7 m** (standart koşu 1519.2 m).

| Bileşen grubu | Malzeme | Geometri | Kütle (kg) |
|---|---|---|---|
| Burun (HAACK) | ABS 100% infill | 290 mm, Ø140, cidar 2.0 mm, omuz 210 mm | 0.3668 |
| Gövde | Alüminyum | 950 mm, Ø140, cidar 2.0 mm | 2.2241 |
| Entegrasyon gövdesi (TubeCoupler) | Alüminyum | 210 mm, Ø135, cidar 2.0 mm | 0.4738 |
| Kanatlar 4× | Alüminyum 2700 | kök 300 / uç 100 / yük 100 mm, süpürme 56.3°, 3.0 mm | 0.7452 |
| Paraşütler (2) | Ripstop nylon | Ø2.60 (Cd 2.2) / Ø1.10 (Cd 2.2) | 0.6613 |
| Aviyonik | — | 0.22 kg + altimetre + switch'ler | 0.2400 |
| Payload | — | 4.35 kg, ad "PAYLOAD" | 4.3500 |
| Kaydırma rayları (3×) | — | 0.33 m × 3 | 0.2291 |
| Motor 3727L1050-P | Cesaroni | 75 × 486 mm, 1.863 kg yakıt | ~3.0 (tahmini) |
| **Toplam** | | 1945 mm | **17.884** |

## Fırlatma Koşulları

Rampa 6.0 m, 85° yükseliş (5° düşeyden), rüzgâr 0, fırlatma irtifası 970 m,
türbülans 0, seed 1.

## Kurtarma Sistemi (2 paraşüt)

| # | Paraşüt | Çap | Cd | Hat × ip | Açılma | Ölçülen iniş (kendi koşusu) |
|---|---|---|---|---|---|---|
| 1 | Ana Paraşüt | 2.60 m | 2.2 | 24 × 4.00 m | `NEVER` | — (hiç açılmıyor!) |
| 2 | PAYLOAD Paraşütü | 1.10 m | 2.2 | 24 × 1.60 m | `NEVER` | — (hiç açılmıyor!) |

**KRİTİK:** Her iki paraşüt `NEVER` olayına ayarlı — **hiç açılmıyor**. Bu tasarım
uçuşta kurtarma sistemi olmadan uçuyor. Şartname 4.2.2 (paraşüt zorunlu) ve
4.2.6/4.2.7/4.2.8 (iniş hızları) **KALDI**.

## Uçuş Sonuçları

| Metrik | Dosyada kayıtlı (`<flightdata>`) | Kendi koşullarıyla yeniden koşu | Standart koşul koşusu |
|---|---|---|---|
| Apogee (m) | **1522.7** | 1455.3 | 1519.2 |
| Max hız (m/s) | 174.9 | 175.3 | 175.7 |
| Mach | 0.522 | 0.527 | 0.524 |
| Rampa çıkış hızı (m/s) | 25.29 | 25.29 | 25.30 |
| Kalkış kütlesi (kg) | — | 17.884 | 17.884 |
| İniş (yer) hızı (m/s) | — | — | — |
| Uçuş süresi (s) | — | — | — |

## 0.3 Mach Stabilitesi

**2.043 cal** (t = 0.829 s, Mach 0.306, irtifa 39.7 m) — 1.5–2.5 kal bandında
GEÇTİ. Burnout stabilitesi ölçülemedi.

## Şartname Kontrolü

| Madde | Gereksinim | Durum | Kanıt |
|---|---|---|---|
| 4.1.7 | payload apogee'den ≤ 2 s sonra ayrılır | **KALDI** | paraşütler `NEVER` — ayrılma yok |
| 4.1.8 | ikincil 400–600 m'de açılır | **KALDI** | paraşütler hiç açılmıyor |
| 4.2.2 | kurtarma sistemi paraşüt olmalı | **KALDI** | paraşütler `NEVER` |
| 4.2.3 | payload bağımsız paraşütle kurtarılır | **KALDI** | paraşütler hiç açılmıyor |
| 4.2.6 | birincil 9–20 m/s | **KALDI** | paraşüt yok |
| 4.2.7 | ikincil 5–9 m/s | **KALDI** | paraşüt yok |
| 4.2.8 | payload 9–20 m/s | **KALDI** | paraşüt yok |
| 4.2.16 | her paraşüt farklı ve koyu renk | MODELLENMEDİ | renk modelde yok |
| 4.2.18 | sıkı geçmeli yok, shear pin | MODELLENMEDİ | modelde yok |
| 4.3.2 | payload ≥ 4.0 kg | GEÇTİ | 4.350 kg |
| 4.4.2 | sabit dış çap, boat tail yok | GEÇTİ | tek Ø140 mm gövde |
| 4.4.5 | 0.3 Mach 1.5–2.5 cal | GEÇTİ | 2.043 cal |
| 4.4.8 | rampa çıkışı ≥ 25 m/s | GEÇTİ | 25.30 m/s (sınırda) |
| 4.5.2 | 3× 3.0–4.5 mm delik | MODELLENMEDİ | `Hole` yok |
| 4.5.5 | PVC/kraft/PLA yasak | GEÇTİ | ABS, alüminyum, çelik, fiberglas |
| 4.5.9 | mapalar döküm çelik | MODELLENMEDİ | kütle olarak modellendi |
| 4.5.11 | burun omuzluğu ≥ 1.5× dış çap | GEÇTİ | 210 mm = 1.500×140 |
| 4.5.15 | ≥ 2 ray butonu | **KALDI** | 2 LaunchLug (ray butonu değil) |
| 4.5.16 | CG iki ray butonu arasında | MODELLENMEDİ | konum doğrulanmadı |
| 4.5.19 | bir ray butonu motor bölgesinde | MODELLENMEDİ | konum doğrulanmadı |
| 4.6.2 | iki UKB | MODELLENMEDİ | aviyonik kütlesi olarak modellendi |
| 4.1.33 | görev yükü "PAYLOAD" adıyla | GEÇTİ | ad "PAYLOAD" ✅ |
| 4.1.35 | 85° yükseliş | GEÇTİ | rampa 6 m, 85° |
| 3.2.17 | asgari irtifa 4000 ft (1219 m) | GEÇTİ | 1522.7 m (sınırda) |

## Tasarımın Düşüncesi

**En düşük apogee'li tasarım (1522.7 m)** ve **en çok şartname ihlali** olan tasarım.
Motor Cesaroni 3727L1050-P (Ø75 × 486 mm, 1.863 kg yakıt) — AeroTech motorları
değil; bu motor şartname dışı (şartname 4.1.18/4.1.19/4.1.20 yalnız A1→L1256,
A2/A4→M1850, A3→N3300 verir).

**Negatif örnek** olarak değerli:
1. Paraşütler `NEVER` olayına ayarlı → kurtarma sistemi yok.
2. 17.884 kg kalkış kütlesi ile 1522.7 m apogee → **çok ağır, çok düşük**.
3. Ø140 mm gövde, 2.0 mm cidar alüminyum → gereksiz ağır.
4. 4 kanatlı, 300/100/100 mm kanatlar → aşırı büyük kanatlar.
5. ABS burun 6 mm cidar → 0.37 kg (gereksiz).
6. Kaydırma rayları (launch lug) ray butonu yerine kullanılmış.
7. Rampa çıkışı 25.30 m/s → sınırda (≥25).

## İlgili Sayfalar

[[en-yuksek-irtifa]] · [[kutle-tabani-m1850]] · [[m1850-apogee-fizigi]] ·
[[13930-a2-bozokroket-m1850]] · [[ares-rocket-team-m2020]]
