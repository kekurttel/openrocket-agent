---
type: source
title: "Bu projenin M1850 yarışma tasarımı (A2/A4)"
status: parsed
created: 2026-10-22
updated: 2026-10-22
tags: [roket, teknofest-2026, m1850, a2, a4, bizim-tasarim]
---

# Bu Projenin M1850 Yarışma Tasarımı

**Kaynak dosya:** `designs/m1850-teknofest/rocket.ork`
**Rapor:** `designs/m1850-teknofest/FINAL_REPORT.md`
**Motor:** AeroTech **M1850 / TFM1850W** (sabit) · **Kategori:** A2 Orta İrtifa / A4
**Toplam uzunluk:** 1968 mm

## Kütle Bütçesi (kalkış 14.4948 kg)

| Bileşen | Malzeme | Geometri | kg |
|---|---|---|---|
| Motor TFM1850W | — | 75 × 935.4 mm | 7.0100 |
| **PAYLOAD** | — | 170 × Ø110 mm, tek MassComponent | **4.0000** |
| Gövde | Karbon 1550 | Ø117 dış / Ø114 iç, 1.5 mm × 1500 mm | 1.2655 |
| Aviyonik | — | 80 × Ø100 mm | 1.0000 |
| Motor yuvası | Karbon 1550 | Ø79/77 × 938 mm | 0.3563 |
| Burun (ogive, L/D 4.0) | Karbon 1550 | 468 mm, taban Ø117, omuz 175.5 mm | 0.2639 |
| Kanatlar 3× | G10 1900 | kök 200 / uç 60 / yük 96 mm, süpürme 50°, 3.0 mm | 0.2134 |
| Paraşütler (3) | Ripstop nylon | Ø1.10 / 1.70 / 1.00 m | 0.3858 |
| **Toplam** | | | **14.4948** |

## Fırlatma Koşulları

| Koşul | Değer |
|---|---|
| Rampa | 6.0 m, **85° yükseliş** (OpenRocket'ta 5° düşeyden) |
| Fırlatma irtifası | 1000 m (Aksaray) |
| Rüzgâr / türbülans | 0 / 0 |
| Seed | 1 |

## Kurtarma Sistemi

| # | Paraşüt | Çap | Cd | Hat × ip | Açılma | Ölçülen iniş hızı |
|---|---|---|---|---|---|---|
| 1 | Birincil drogue (**yeşil**) | 1.10 m | 0.8 | 8 × 2.20 m | `APOGEE` 0 s | **15.31 m/s** (payload ayrılınca türetilen 11.90) |
| 2 | İkincil ana (**sarı**) | 1.70 m | 0.8 | 12 × 2.50 m | `ALTITUDE` 500 m | **8.40 m/s** (ayrılma sonrası 6.57) |
| 3 | Görev yükü (**turuncu**) | 1.00 m | 0.8 | 8 × 2.20 m | `APOGEE` +1.0 s | **10.98 m/s** (ayrı iki kademeli pod simi) |

## Uçuş Sonuçları (gerçek simülasyon, seed 1)

| Metrik | Değer | Şartname | Durum |
|---|---|---|---|
| **Apogee (AGL)** | **5857.6 m** | 4930–6670 m (5800 ± %15) | GEÇTİ |
| Max hız | 450.4 m/s (**Mach 1.359**) | — | — |
| **0.3 Mach stabilite** | **1.738 cal** (t=0.820 s, Mach 0.3169) | 1.5–2.5 cal | GEÇTİ |
| Kalkış stabilitesi | 1.610 cal | > 0 | GEÇTİ |
| Burnout stabilitesi | 3.086 cal | — | (aşırı stabil) |
| **Rampa çıkış hızı** | **41.87 m/s** | ≥ 25 m/s | GEÇTİ |
| Kalkış kütlesi | 14.4948 kg | 10.5–11.5 kg bandı | **KALDI** (bkz. [[kutle-tabani-m1850]]) |
| Bileşke iniş hızı | 7.71 m/s | — | (üç paraşüt aynı gövdede) |
| Yer hızı | 7.56 m/s | — | — |
| Uçuş süresi | 495.8 s | — | — |
| Rüzgâr duyarlılığı | 0/3/6/9 m/s → 5857.6 / 5804.4 / 5720.9 / 5644.8 m | — | — |

`validate()` → 0 sorun. `pytest -q` → 48 passed.

## Şartname Kontrolü

| Madde | Gereksinim | Durum | Kanıt |
|---|---|---|---|
| 4.1.7 | payload apogee'den ≤ 2 s sonra ayrılır | **MODELLENMEDİ** | ana `.ork` tek gövde; ayrılma bağımsız pod simiyle ölçüldü |
| 4.1.8 | ikincil 400–600 m'de açılır | GEÇTİ | `ALTITUDE` 500 m |
| 4.2.3 | payload bağımsız paraşütle kurtarılır | KALDI (model) | üç paraşüt ayrı tanımlı, fiziksel ayrılma modellenmedi |
| 4.2.6 | birincil 9–20 m/s | GEÇTİ | 15.31 m/s (ayrı koşu) |
| 4.2.7 | ikincil 5–9 m/s | GEÇTİ | 8.40 m/s (ayrı koşu) |
| 4.2.8 | payload 9–20 m/s | GEÇTİ | 10.98 m/s (pod simi) |
| 4.2.16 | her paraşüt farklı ve koyu renk | MODELLENMEDİ | renk `.ork` modelinde yok |
| 4.3.2 | payload ≥ 4.0 kg | GEÇTİ | 4.0000 kg, ad "PAYLOAD" |
| 4.3.3 | payload kolay ayrılabilir | MODELLENMEDİ | ayrılma mekanizması modelde yok |
| 4.4.2 | sabit dış çap, boat tail yok | GEÇTİ | tek Ø117 mm gövde, transition yok |
| 4.4.5 | 0.3 Mach 1.5–2.5 cal | GEÇTİ | 1.738 cal |
| 4.4.8 | rampa çıkışı ≥ 25 m/s | GEÇTİ | 41.87 m/s |
| 4.5.2 | 3× 3.0–4.5 mm delik | MODELLENMEDİ | OpenRocket'ta delik bileşeni kullanılmadı |
| 4.5.5 | PVC/kraft/PLA yasak | GEÇTİ | karbon, G10, ripstop |
| 4.5.11 | burun omuzluğu ≥ 1.5× dış çap | GEÇTİ | 175.5 mm = 1.500×117 |
| 4.5.15 | ≥ 2 ray butonu | MODELLENMEDİ | ray butonu bileşeni kullanılmadı |
| 4.5.19 | bir ray butonu motor bölgesinde | MODELLENMEDİ | aynı |
| 4.6.2 | iki UKB | MODELLENMEDİ | 1.0 kg aviyonik kütlesi olarak modellendi |
| 4.1.35 | 85° yükseliş | GEÇTİ | `rod_angle=85` → 5° düşeyden |

## Tasarımın Düşüncesi

Motor ve payload zorunlu kütlesi 11.010 kg olduğu için 10.5–11.5 kg bandına
inilemiyor; hedef, asgari irtifayı güvenli aşan **en yüksek** irtifa olacak şekilde
kütle ve sürükleme dengelendi. Karbon gövde/burun (1.5 mm) ile fiberglas yerine
geçildiğinde kütle ~1.1 kg artıyordu; motor yuvası kısaltılarak, paraşüt ipleri
kısaltılarak ve aviyonik 1.0 kg'ya çekilerek bu artık telafi edildi. Sonuç:
14.49 kg ile 5857.6 m.

**Örneklerle fark:** iki kademeli çözüm kullanan [[bozok-cetin-06-m1850]] ve
[[2027-a2-1-bozok-m1850]] görev yükünün ayrılmasını modelde de gösteriyor; bizim
tasarımımızda bu ayrılma simülasyonda yapılamıyor (payload çıkınca gövde statik
kararsızlaşıyor). Fakat aynı motorla **5857.6 m** ile onlardan yüksek.

## İlgili Sayfalar

[[en-yuksek-irtifa]] · [[m1850-rekabet]] · [[motor-m1850]] · [[kutle-tabani-m1850]] ·
[[rampa-acisi-konusu]] · [[parasut-acilma-olaylari]]
