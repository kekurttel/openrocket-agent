---
type: source
title: "13930_A2_bozokroket_752583_openrocket_KTR.ork — Bozok (M1850)"
status: parsed
created: 2026-10-23
updated: 2026-10-23
tags: [roket, teknofest-2026, a2, a4, m1850, openrocket, iki-kademeli]
---

# 13930_A2_bozokroket_752583_openrocket_KTR.ork (Bozok, M1850)

**Kaynak dosya:** `örnekroket2/13930_A2_bozokroket_752583_openrocket_KTR.ork`
**Takım:** Bozok  |  **Motor:** TFM1850W (Teknofest26)  |  **Kategori:** A2 / A4 (M1850)
**Toplam uzunluk:** 2390 mm  |  **Toplam kalkış kütlesi:** 20.109 kg

## Kütle ve Geometri

İki kademeli tasarım: üst gövde (görev yükü + payload paraşütü + sürüklenme paraşütü) + alt gövde (motor + ana paraşüt) + alüminyum entegrasyon gövdesi (TubeCoupler, **1.025 kg**, 190 mm, Ø116) + iki Ayırma Sistemi. Gövde Ø116 mm.

| Bileşen grubu | Malzeme | Geometri | Kütle (kg) |
|---|---|---|---|
| Burun (HAACK) | Karbon 1550 | 350 mm, Ø116, cidar 2.0 mm, omuz 174 mm | 0.5046 |
| Gövde 1 (üst) | Fiberglas 1850 | 970 mm, Ø116, cidar 2.0 mm | 1.2854 |
| Gövde 2 (alt) | Fiberglas 1850 | 1060 mm, Ø116, cidar 2.0 mm, motor yuvası | 1.4046 |
| Entegrasyon gövdesi (TubeCoupler) | Alüminyum | 190 mm, Ø116, cidar 6.0 mm | **1.0250** |
| Kanatlar 3× | Alüminyum 2700 | kök 270 / uç 66 / yük 88 mm, süpürme 68.4°, 3.0 mm | 0.3972 |
| Paraşütler (3) | Ripstop nylon | Ø1.10 / 1.10 / 2.00 m | 0.5797 |
| Aviyonik (Özgün UKB 0.48 + Ticari UKB 0.12 + hakem altimetresi) | — | — | 0.6310 |
| Payload + destek + mapalar + centering ring'ler | — | — | ~1.00 |
| Motor TFM1850W | — | 75 × 935.4 mm | 7.0100 |
| **Toplam** | | 2390 mm | **20.109** |

## Fırlatma Koşulları

Rampa 6.0 m, 85° yükseliş (5° düşeyden), rüzgâr 0, fırlatma irtifası 970 m, türbülans 0, seed 1.

## Kurtarma Sistemi (3 paraşüt)

| # | Paraşüt | Çap | Cd | Hat × ip | Açılma | Ölçülen iniş (kendi koşusu) |
|---|---|---|---|---|---|---|
| 1 | Payload Paraşütü | 1.10 m | 0.8 | 12 × 1.92 m | `APOGEE` 0 s | ~9.8 m/s |
| 2 | Sürüklenme Paraşütü | 1.10 m | 0.8 | 12 × 1.92 m | `APOGEE` 0 s | ~9.8 m/s |
| 3 | Ana Paraşüt | 2.00 m | 0.8 | 12 × 1.92 m | `ALTITUDE` 600 m | 7.95 m/s |

## Uçuş Sonuçları

| Metrik | Dosyada kayıtlı (`<flightdata>`) | Kendi koşullarıyla yeniden koşu | Standart koşul koşusu |
|---|---|---|---|
| Apogee (m) | **4246.1** | 4245.9 | 4215.3 |
| Max hız (m/s) | 319.2 | 319.2 | 319.6 |
| Mach | 0.958 | 0.958 | 0.960 |
| Rampa çıkış hızı (m/s) | 33.74 | 33.74 | 33.74 |
| Kalkış kütlesi (kg) | — | 20.109 | 20.109 |
| İniş (yer) hızı (m/s) | 9.898 | ~9.8 | 7.95 |
| Uçuş süresi (s) | 424.7 | — | — |

## 0.3 Mach Stabilitesi

**2.245 cal** (t = 0.992 s, Mach 0.308, irtifa 48.8 m) — 1.5–2.5 kal bandında GEÇTİ. Burnout stabilitesi **4.75 cal** (aşırı stabil).

## Şartname Kontrolü

| Madde | Gereksinim | Durum | Kanıt |
|---|---|---|---|
| 4.1.7 | payload apogee'den ≤ 2 s sonra ayrılır | GEÇTİ | apogee'de iki kademe ayrılıyor |
| 4.1.8 | ikincil 400–600 m'de açılır | GEÇTİ | Ana Paraşüt `ALTITUDE` 600 m |
| 4.2.3 | payload bağımsız paraşütle kurtarılır | GEÇTİ | Payload Paraşütü Ø1.10 m, ayrı üst gövde |
| 4.2.6 | birincil 9–20 m/s | GEÇTİ | ~9.8 m/s |
| 4.2.7 | ikincil 5–9 m/s | GEÇTİ | 7.95 m/s |
| 4.2.8 | payload 9–20 m/s | GEÇTİ | ~9.8 m/s |
| 4.2.16 | her paraşüt farklı ve koyu renk | MODELLENMEDİ | renk modelde yok |
| 4.2.18 | sıkı geçmeli yok, shear pin | MODELLENMEDİ | modelde yok |
| 4.3.2 | payload ≥ 4.0 kg | GEÇTİ | 4.010 kg |
| 4.3.3 | payload kolay ayrılabilir | GEÇTİ | iki kademeli ayrılma |
| 4.4.2 | sabit dış çap, boat tail yok | GEÇTİ | iki gövde aynı Ø116 mm |
| 4.4.5 | 0.3 Mach 1.5–2.5 cal | GEÇTİ | 2.245 cal |
| 4.4.8 | rampa çıkışı ≥ 25 m/s | GEÇTİ | 33.74 m/s |
| 4.5.2 | 3× 3.0–4.5 mm delik | MODELLENMEDİ | `Hole` yok |
| 4.5.5 | PVC/kraft/PLA yasak | GEÇTİ | karbon, fiberglas, alüminyum, Delrin, ripstop |
| 4.5.9 | mapalar döküm çelik | MODELLENMEDİ | kütle olarak modellendi |
| 4.5.11 | burun omuzluğu ≥ 1.5× dış çap | GEÇTİ | 174 mm = 1.500×116 |
| 4.5.12 | entegrasyon gövdesi ≥ %75 | MODELLENMEDİ | TubeCoupler 190 mm (kısa; %75 şartı modelde doğrulanmadı) |
| 4.5.15 | ≥ 2 ray butonu | GEÇTİ | 2 |
| 4.5.16 | CG iki ray butonu arasında | MODELLENMEDİ | konum doğrulanmadı |
| 4.5.19 | bir ray butonu motor bölgesinde | MODELLENMEDİ | konum doğrulanmadı |
| 4.6.2 | iki UKB | MODELLENMEDİ | aviyonik kütlesi olarak modellendi |
| 4.1.33 | görev yükü "PAYLOAD" adıyla | KALDI | ad "Payload" |
| 4.1.35 | 85° yükseliş | GEÇTİ | rampa 6 m, 85° |

## Tasarımın Düşüncesi

**Aynı motor (M1850) ile 4246 m** — Çetin 06 (5827.8 m) ve 2027 A2_1 (5815.2 m) ile karşılaştırıldığında **~1580 m daha düşük**. Neden?

1. **Ø116 mm gövde** (Ø98 mm yerine) → %40 daha fazla frontal alan → sürükleme artışı.
2. **20.109 kg kalkış kütlesi** (Çetin 06: 17.857 kg) → 2.25 kg daha ağır. Özellikle TubeCoupler (1.025 kg, 6 mm cidar) ve bulkhead'ler (0.266 kg × 2) çok ağır.
3. **Kanatlar 3 mm alüminyum** (kök 270 mm, uç 66 mm, yük 88 mm, süpürme 68.4°) → büyük kanatlar, yüksek sürükleme.
4. **Aviyonik 0.63 kg** (Çetin 06: 0.52 kg) — biraz daha ağır.

Bu tasarım, **aşırı yapısal kütleye** sahip bir M1850 tasarım örneği. Aynı motorla 5.8 km'ye ulaşmak için gövde çapı Ø98 mm'ye düşürülmeli, TubeCoupler hafifletilmeli, kanatlar küçültülmeli.

## İlgili Sayfalar

[[motor-m1850]] · [[takim-bozok]] · [[en-yuksek-irtifa]] · [[m1850-rekabet]] ·
[[m1850-apogee-fizigi]] · [[kutle-tabani-m1850]]
