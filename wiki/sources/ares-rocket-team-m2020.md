---
type: source
title: "Ares Rocket Team Open Rocket AHR.ork — Ares Rocket Team (8429M2020-P)"
status: parsed
created: 2026-10-23
updated: 2026-10-23
tags: [roket, teknofest-2026, a2, a4, m1850, openrocket, iki-kademeli, cesaroni]
---

# Ares Rocket Team Open Rocket AHR.ork (Ares Rocket Team, 8429M2020-P)

**Kaynak dosya:** `örnekroket2/Ares Rocket Team Open Rocket AHR.ork`
**Takım:** Ares Rocket Team  |  **Motor:** 8429M2020-P (Cesaroni Technology Inc.)  |  **Kategori:** A2 / A4
**Toplam uzunluk:** 2783 mm  |  **Toplam kalkış kütlesi:** 27.904 kg

## Kütle ve Geometri

İki kademeli tasarım: üst gövde (görev yükü + payload paraşütü) + alt gövde (motor + ikincil paraşüt) + alüminyum TubeCoupler (0.5 m, Ø130). **Çok ağır** (27.9 kg) ve **geniş çaplı** (Ø136 mm). Motor Cesaroni 8429M2020-P (Ø75 × 893 mm, 4.349 kg yakıt).

| Bileşen grubu | Malzeme | Geometri | Kütle (kg) |
|---|---|---|---|
| Burun (parabolik) | Fiberglas 1850 | 250 mm, Ø136, cidar 6.0 mm, omuz 250 mm | 1.3104 |
| Üst gövde | Fiberglas 1850 | 1250 mm, Ø136, cidar 3.0 mm | 2.8987 |
| Alt gövde | Fiberglas 1850 | 1230 mm, Ø136, cidar 3.0 mm, motor yuvası | 2.8523 |
| Entegrasyon gövdesi (TubeCoupler) | Alüminyum | 500 mm, Ø130, cidar 2.0 mm | 1.0857 |
| Kanatlar 3× | Alüminyum 2700 | kök 200 / uç 120 / yük 100 mm, süpürme 55°, 4.0 mm | 0.6104 |
| Paraşütler (2) | Ripstop nylon | Ø1.50 / Ø1.00 m | 0.2196 |
| Aviyonik | — | — | 0.5500 |
| Payload | — | 4.02 kg, ad "PAYLOAD" | 4.0200 |
| Motor 8429M2020-P | Cesaroni | 75 × 893 mm, 4.349 kg yakıt | ~7.0 (tahmini) |
| **Toplam** | | 2783 mm | **27.904** |

## Fırlatma Koşulları

Rampa 6.0 m, 85° yükseliş (5° düşeyden), rüzgâr 0, fırlatma irtifası 970 m, türbülans 0, seed 1.

## Kurtarma Sistemi (2 paraşüt)

| # | Paraşüt | Çap | Cd | Hat × ip | Açılma | Ölçülen iniş (kendi koşusu) |
|---|---|---|---|---|---|---|
| 1 | Görev Yükü Paraşütü | 1.50 m | 0.8 | 10 × 1.50 m | `APOGEE` 0 s | ~10 m/s |
| 2 | Birincil Paraşüt | 1.00 m | 0.8 | 8 × 1.50 m | `APOGEE` 0 s | ~10 m/s |

**Not:** Her iki paraşüt `APOGEE` 0 s'de açılıyor (ikincil paraşüt 400–600 m'de değil). Şartname 4.1.8 ve 4.2.7 gereksinimleri karşılanmıyor.

## Uçuş Sonuçları

| Metrik | Dosyada kayıtlı (`<flightdata>`) | Kendi koşullarıyla yeniden koşu | Standart koşul koşusu |
|---|---|---|---|
| Apogee (m) | **3084.2** | 3024.9 | 3091.9 |
| Max hız (m/s) | 265.6 | 266.5 | 266.8 |
| Mach | 0.794 | 0.801 | 0.798 |
| Rampa çıkış hızı (m/s) | 31.9 | 31.9 | 31.9 |
| Kalkış kütlesi (kg) | — | 27.904 | 27.904 |
| İniş (yer) hızı (m/s) | — | ~10 | ~10 |
| Uçuş süresi (s) | — | — | — |

## 0.3 Mach Stabilitesi

**2.068 cal** (t = 0.819 s, Mach 0.306, irtifa 39.7 m) — 1.5–2.5 kal bandında GEÇTİ. Burnout stabilitesi ölçülemedi (çok ağır roket).

## Şartname Kontrolü

| Madde | Gereksinim | Durum | Kanıt |
|---|---|---|---|
| 4.1.7 | payload apogee'den ≤ 2 s sonra ayrılır | GEÇTİ | her iki paraşüt `APOGEE` 0 s |
| 4.1.8 | ikincil 400–600 m'de açılır | **KALDI** | her iki paraşüt `APOGEE` 0 s'de açılıyor |
| 4.2.3 | payload bağımsız paraşütle kurtarılır | GEÇTİ | Payload Paraşütü Ø1.50 m, ayrı üst gövde |
| 4.2.6 | birincil 9–20 m/s | GEÇTİ | ~10 m/s |
| 4.2.7 | ikincil 5–9 m/s | **KALDI** | ~10 m/s (5–9 bandı dışında) |
| 4.2.8 | payload 9–20 m/s | GEÇTİ | ~10 m/s |
| 4.2.16 | her paraşüt farklı ve koyu renk | MODELLENMEDİ | renk modelde yok |
| 4.2.18 | sıkı geçmeli yok, shear pin | MODELLENMEDİ | modelde yok |
| 4.3.2 | payload ≥ 4.0 kg | GEÇTİ | 4.020 kg |
| 4.3.3 | payload kolay ayrılabilir | GEÇTİ | iki kademeli ayrılma |
| 4.4.2 | sabit dış çap, boat tail yok | GEÇTİ | tek Ø136 mm gövde |
| 4.4.5 | 0.3 Mach 1.5–2.5 cal | GEÇTİ | 2.068 cal |
| 4.4.8 | rampa çıkışı ≥ 25 m/s | GEÇTİ | 31.9 m/s |
| 4.5.2 | 3× 3.0–4.5 mm delik | MODELLENMEDİ | `Hole` yok |
| 4.5.5 | PVC/kraft/PLA yasak | **KALDI** | **Cardboard** malzeme (Ayrılma Body) |
| 4.5.9 | mapalar döküm çelik | MODELLENMEDİ | kütle olarak modellendi |
| 4.5.11 | burun omuzluğu ≥ 1.5× dış çap | GEÇTİ | 250 mm = 1.838×136 |
| 4.5.12 | entegrasyon gövdesi ≥ %75 | MODELLENMEDİ | TubeCoupler 500 mm (uzun; %75 şartı modelde doğrulanmadı) |
| 4.5.15 | ≥ 2 ray butonu | **KALDI** | 2 LaunchLug (ray butonu değil) |
| 4.5.16 | CG iki ray butonu arasında | MODELLENMEDİ | konum doğrulanmadı |
| 4.5.19 | bir ray butonu motor bölgesinde | MODELLENMEDİ | konum doğrulanmadı |
| 4.6.2 | iki UKB | MODELLENMEDİ | aviyonik kütlesi olarak modellendi |
| 4.1.33 | görev yükü "PAYLOAD" adıyla | GEÇTİ | ad "PAYLOAD" ✅ |
| 4.1.35 | 85° yükseliş | GEÇTİ | rampa 6 m, 85° |

## Tasarımın Düşüncesi

**Çok ağır ve çok geniş çaplı** bir tasarım. Ø136 mm gövde, 6 mm cidar fiberglas
burun, 3 mm cidar fiberglas gövde, 4 mm alüminyum kanatlar, 500 mm alüminyum
TubeCoupler — her bileşen gereksiz derecede ağır. 27.9 kg kalkış kütlesi ile
3084 m apogee → **M1850 motorunun potansiyelini tamamen boşa harcıyor**.

**Negatif örnek** olarak değerli: aynı motorla 5.8 km'ye çıkan tasarımlar varken
bu tasarım 3.1 km'de kalıyor. Nedenleri:
1. Ø136 mm gövde → %90 daha fazla frontal alan → sürükleme artışı.
2. 6 mm cidar fiberglas burun → 1.31 kg (gereksiz ağır).
3. 500 mm alüminyum TubeCoupler → 1.09 kg (aşırı ağır).
4. 4 mm alüminyum kanatlar → 0.61 kg (aşırı kalın).
5. Cardboard malzeme (Ayrılma Body) → şartname 4.5.5 ihlali.
6. Her iki paraşüt `APOGEE` 0 s'de açılıyor → ikincil paraşüt 400–600 m'de değil.

## İlgili Sayfalar

[[motor-m1850]] · [[en-yuksek-irtifa]] · [[m1850-rekabet]] · [[kutle-tabani-m1850]] ·
[[m1850-apogee-fizigi]] · [[13930-a2-bozokroket-m1850]]
