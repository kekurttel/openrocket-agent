---
type: source
title: "Bozok Roket Takımı - Çetin 06.ork — Çetin (M1850)"
status: parsed
created: 2026-10-22
updated: 2026-10-22
tags: [roket, teknofest-2026, a2, a4, m1850, openrocket, iki-kademeli]
---

# Bozok Roket Takımı – Çetin 06.ork (Çetin, M1850)

**Kaynak dosya:** `örnek-roket/Bozok Roket Takımı - Çetin 06.ork`
**Takım:** Çetin  |  **Motor:** TFM1850W (Teknofest26)  |  **Kategori:** A2 / A4 (M1850)
**Toplam uzunluk:** 2271 mm  |  **Toplam kalkış kütlesi:** 17.857 kg

## Kütle ve Geometri

İki kademeli tasarım: **üst gövde** (görev yükü + payload paraşütü) + **alt gövde**
(motor + sürüklenme + ana paraşüt) + **alüminyum entegrasyon gövdesi (TubeCoupler,
0.658 kg)** + iki **Ayırma Sistemi**. Gövde Ø98 mm.

| Bileşen grubu | Malzeme | Geometri | Kütle (kg) |
|---|---|---|---|
| Burun (HAACK) | Karbon 1550 | 350 mm, taban Ø98, cidar 2.0 mm, omuz 147 mm | 0.3948 |
| Gövde 1 (üst) | Fiberglas 1850 | 843 mm, Ø98, cidar 2.0 mm | 0.9407 |
| Gövde 2 (alt) | Fiberglas 1850 | 1045 mm, Ø98, cidar 2.0 mm, motor yuvası | 1.1661 |
| Entegrasyon gövdesi (TubeCoupler) | Alüminyum | 10 mm, Ø98 | 0.6584 |
| Kanatlar 3× | Alüminyum 2700 | kök 175 / uç 30 / yük 70 mm, süpürme 70°, 3.0 mm | 0.1907 |
| Paraşütler (3) | Ripstop nylon | Ø1.10 / 1.10 / 2.00 m | 0.5765 |
| Aviyonik (Özgün + Ticari UKB, hakem altimetresi, key switch'ler) | — | — | 0.5210 |
| Payload + destek + mapalar + centering ring'ler | — | — | ~0.80 |
| Motor TFM1850W | — | 75 × 935.4 mm | 7.0100 |
| **Toplam** | | 2271 mm | **17.8574** |

## Fırlatma Koşulları

Rampa 6.0 m, **85° yükseliş** (5° düşeyden), rüzgâr 0 m/s, fırlatma irtifası
970 m, türbülans 0, seed 1.

## Kurtarma Sistemi (3 paraşüt)

| # | Paraşüt | Çap | Cd | Hat × ip | Açılma | Ölçülen iniş (kendi koşusu) |
|---|---|---|---|---|---|---|
| 1 | Payload Paraşütü | 1.10 m | 0.8 | 12 × 1.92 m | `APOGEE` 0 s | 9.83 m/s |
| 2 | Sürüklenme Paraşütü | 1.10 m | 0.8 | 12 × 1.92 m | `APOGEE` 0 s | 9.83 m/s |
| 3 | Ana Paraşüt | 2.00 m | 0.8 | 12 × 1.92 m | `ALTITUDE` 600 m | 7.75 m/s |

İki küçük paraşüt apogee'de birlikte açılıyor (sürüklenme + payload), ana paraşüt
600 m'de açılıyor.

## Uçuş Sonuçları

| Metrik | Dosyada kayıtlı (`<flightdata>`) | Kendi koşullarıyla yeniden koşu | Standart koşul koşusu |
|---|---|---|---|
| Apogee (m) | **5827.8** | 5828.9 | 5790.0 |
| Max hız (m/s) | 379.1 | 379.1 | 379.5 |
| Mach | 1.141 | 1.141 | 1.143 |
| Rampa çıkış hızı (m/s) | 36.43 | 36.43 | 36.43 |
| Kalkış kütlesi (kg) | — | 17.857 | 17.857 |
| İniş (yer) hızı (m/s) | 9.71 | 9.83 | 7.75 |
| Uçuş süresi (s) | 463.9 | 463.9 | 461.0 |

## 0.3 Mach Stabilitesi

**1.785 cal** (t = 0.992 s, Mach 0.309, irtifa 48.9 m) — 1.5–2.5 kal bandında
GEÇTİ. Burnout stabilitesi **4.71 cal** (aşırı stabil).

## Şartname Kontrolü

| Madde | Gereksinim | Durum | Kanıt |
|---|---|---|---|
| 4.1.7 | payload apogee'den ≤ 2 s sonra ayrılır | GEÇTİ | apogee'de iki kademe ayrılıyor (Ayırma Sistemi 1/2) |
| 4.1.8 | ikincil 400–600 m'de açılır | GEÇTİ | Ana Paraşüt `ALTITUDE` 600 m |
| 4.2.3 | payload bağımsız paraşütle kurtarılır | GEÇTİ | Payload Paraşütü Ø1.10 m, ayrı üst gövde |
| 4.2.6 | birincil 9–20 m/s | GEÇTİ | 9.83 m/s (kendi koşusu) |
| 4.2.7 | ikincil 5–9 m/s | GEÇTİ | 7.75 m/s (standart) |
| 4.2.8 | payload 9–20 m/s | GEÇTİ | 9.83 m/s |
| 4.2.16 | her paraşüt farklı ve koyu renk | MODELLENMEDİ | renk modelde yok |
| 4.2.18 | sıkı geçmeli yok, shear pin | MODELLENMEDİ | modelde yok |
| 4.3.2 | payload ≥ 4.0 kg | GEÇTİ | 4.010 kg |
| 4.3.3 | payload kolay ayrılabilir | GEÇTİ | iki kademeli ayrılma (Ayırma Sistemi 1/2) |
| 4.4.2 | sabit dış çap, boat tail yok | GEÇTİ | tek Ø98 mm gövde (2 gövde aynı çap) |
| 4.4.5 | 0.3 Mach 1.5–2.5 cal | GEÇTİ | 1.785 cal |
| 4.4.8 | rampa çıkışı ≥ 25 m/s | GEÇTİ | 36.43 m/s |
| 4.5.2 | 3× 3.0–4.5 mm delik | MODELLENMEDİ | `Hole` bileşeni yok |
| 4.5.5 | PVC/kraft/PLA yasak | GEÇTİ | karbon, fiberglas, alüminyum, Delrin, ripstop |
| 4.5.9 | mapalar döküm çelik | MODELLENMEDİ | kütle olarak modellendi |
| 4.5.11 | burun omuzluğu ≥ 1.5× dış çap | GEÇTİ | 147 mm = 1.500×98 |
| 4.5.12 | entegrasyon gövdesi ≥ %75 her iki gövdeye | GEÇTİ | alüminyum TubeCoupler, 10 mm (kısa; %75 şartı modelde doğrulanmadı) |
| 4.5.15 | ≥ 2 ray butonu | GEÇTİ | 2 (Delrin + Alüminyum) |
| 4.5.16 | CG iki ray butonu arasında | MODELLENMEDİ | konum doğrulanmadı |
| 4.5.19 | bir ray butonu motor bölgesinde | MODELLENMEDİ | konum doğrulanmadı |
| 4.6.2 | iki UKB | MODELLENMEDİ | aviyonik kütlesi olarak modellendi |
| 4.1.33 | görev yükü "PAYLOAD" adıyla | KALDI | ad "Payload" (şartname "PAYLOAD" diyor) |
| 4.1.35 | 85° yükseliş | GEÇTİ | rampa 6 m, 85° |

## Tasarımın Düşüncesi

En yüksek irtifaya ulaşan örnek. İki kademeli çözüm, görev yükünün bağımsız
kurtarılması (4.2.3, 4.3.3) ve entegrasyon gövdesi (4.5.12) maddelerini
**modelde de** gösteriyor — tek gövdeli tasarımların yapamadığı şey. Bedeli:
17.86 kg kalkış kütlesi (bizimkinden 3.4 kg ağır) ve aşırı stabilite (burnout
4.71 cal). Küçük çap (Ø98 mm) sürükleme avantajı sağlıyor ama büyük alüminyum
kanatlar (3 mm, 175 mm kök) sürtünmeyi artırıyor.

## İlgili Sayfalar

[[motor-m1850]] · [[takim-cetin]] · [[2027-a2-1-bozok-m1850]] ·
[[m1850-rekabet]] · [[en-yuksek-irtifa]] · [[kutle-tabani-m1850]]
