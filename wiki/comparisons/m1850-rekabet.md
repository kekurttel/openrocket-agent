---
type: comparison
title: "M1850 Tasarımları: Rekabet Karşılaştırması"
status: active
created: 2026-10-22
updated: 2026-10-22
tags: [comparison, m1850, rekabet, teknofest-2026]
---

# M1850 Tasarımları: Rekabet Karşılaştırması

A2/A4 kategorisinde motor sabittir (M1850, 4.1.19); kazananı **tasarım**
belirler. İki örnek M1850 tasarımı (Bozok – Çetin 06 ve 2027 A2_1 – Bozok)
ile bu projenin tasarımı karşılaştırılıyor.

## 1. Temel metrikler

| Metrik | Bozok – Çetin 06 | 2027 A2_1 – Bozok | **Bu projenin tasarımı** |
|---|---|---|---|
| Kayıtlı apogee (m) | **5827.8** | 5815.2 | — |
| Standart koşu apogee (m) | 5790.0 | 5776.9 | **5857.6** |
| Kalkış kütlesi (kg) | 17.857 | 17.879 | **14.495** |
| Burnout kütlesi (kg) | ~13.75 | ~13.77 | ~10.39 |
| Max hız (m/s) | 379.1 | 378.5 | **450.4** |
| Mach | 1.141 | 1.140 | **1.359** |
| Rampa çıkışı (m/s) | 36.43 | 36.38 | **41.87** |
| 0.3 Mach stabilite (cal) | 1.785 | 1.749 | **1.738** |
| Burnout stabilitesi (cal) | 4.71 | 4.75 | 3.09 |
| Kalkış stabilitesi (cal) | 0.718 | 0.740 | 1.610 |
| Uçuş süresi (s) | 463.9 | 462.7 | 495.8 |
| İniş (yer) hızı (m/s) | 9.71 | 9.90 | 7.56 |

## 2. Geometri karşılaştırması

| Özellik | Bozok – Çetin 06 | 2027 A2_1 – Bozok | Bu proje |
|---|---|---|---|
| Toplam uzunluk (mm) | 2271 | 2291 | **1968** |
| Gövde çapı (mm) | 98 | 98 | **117** |
| Gövde cidarı (mm) | 2.0 | 2.0 | **1.5** |
| Gövde malzemesi | Fiberglas | Fiberglas | **Karbon** |
| Burun | HAACK, 350 mm, karbon | HAACK, 350 mm, karbon | Ogive, 468 mm, karbon (L/D 4.0) |
| Kanat | 3× alüminyum, 175/30/70 mm, 70°, 3 mm | 3× alüminyum, 175/31/70 mm, 70°, 3 mm | 3× G10, 200/60/96 mm, 50°, 3 mm |
| Aviyonik (kg) | 0.521 | 0.521 | 1.000 |
| Paraşütler | Ø1.10 / Ø1.10 / Ø2.00 | Ø1.10 / Ø1.10 / Ø2.00 | Ø1.10 / Ø1.70 / Ø1.00 |
| Ray butonu | 2 | 2 | modelde yok |

## 3. Görev yükünün ayrılabilirliği (4.3.3, 4.2.3)

**İki örnek M1850 tasarımının en önemli farkı:** ikisi de **iki kademeli**.

- Üst gövde (Gövde 1): görev yükü (4.01 kg) + payload paraşütü + şok kordonu.
- Alt gövde (Gövde 2): motor + ana/sürüklenme paraşütleri + aviyonik.
- Aralarında **alüminyum TubeCoupler (Entegrasyon Parçası, 0.658 kg)** —
  şartname 4.5.12 (entegrasyon gövdesi ≥ %75 her iki gövdeye girer) için.
- İki "Ayırma Sistemi" (0.078 kg) — şartname 4.2.9 (SGÜ/piroteknik) ile
  uyumlu ayrılma.

Bu sayede **payload'ın gövdeden bağımsız kurtarılması (4.2.3) ve kolay
ayrılabilmesi (4.3.3) modelde de temsil edilir**. Bizim tek gövdeli tasarımımızda
bu ayrılma modelde yapılamıyor (payload çıkınca gövde statik kararsızlaşıyor,
CP−CG = −0.056 m → sayısal ayrışma).

**Ders:** 4.3.3/4.2.3 maddelerini geçmek için **iki kademeli model** şart.
Bizim tasarımımızın bu maddeleri "MODELLENMEDİ" olarak işaretlenmesi
gerekti.

## 4. Paraşüt düzeni

| # | Örnekler (2 tasarım) | Bu proje |
|---|---|---|
| 1 | Payload Paraşütü Ø1.10 m (`APOGEE` 0 s) | Birincil drogue Ø1.10 m (`APOGEE` 0 s) |
| 2 | Sürüklenme Paraşütü Ø1.10 m (`APOGEE` 0 s) | İkincil ana Ø1.70 m (`ALTITUDE` 500 m) |
| 3 | Ana Paraşüt Ø2.00 m (`ALTITUDE` 600 m) | Payload Ø1.00 m (`APOGEE` +1.0 s) |

Örneklerde ikincil paraşüt 600 m'de açılıyor (şartname 4.1.8: 400–600 m → sınırda).
Bizimki 500 m (bandın ortası). Örneklerde iki küçük paraşüt (Ø1.10) birlikte
apogee'de açılıyor (sürüklenme + payload); bizimki tek drogue + payload ayrı.

## 5. Hangi maddelerde kim daha iyi?

| Madde | Örnekler | Bizim tasarım | Yorum |
|---|---|---|---|
| 4.1.7 (payload apogee'den ≤ 2 s sonra ayrılır) | ✅ GEÇTİ (modelde) | ❌ MODELLENMEDİ | bizim tek gövde modeli ayrılımı temsil edemez |
| 4.2.3 / 4.3.3 (bağımsız kurtarma) | ✅ GEÇTİ | ❌ MODELLENMEDİ | aynı |
| 4.2.6 (birincil 9–20 m/s) | ✅ 9.83 m/s | ✅ 15.31 m/s | bizimki daha hızlı (daha küçük drogue) |
| 4.2.7 (ikincil 5–9 m/s) | ✅ 7.75 m/s | ✅ 8.40 m/s | her ikisi de band içinde |
| 4.2.8 (payload 9–20 m/s) | ✅ 9.83 m/s | ✅ 10.98 m/s | her ikisi de band içinde |
| 4.4.2 (sabit çap) | ✅ Ø98 mm | ✅ Ø117 mm | bizimki daha kalın (daha fazla sürükleme) |
| 4.4.5 (0.3 Mach 1.5–2.5 cal) | ✅ 1.75–1.79 | ✅ 1.738 | her ikisi de band içinde |
| 4.4.8 (rampa ≥ 25 m/s) | ✅ 36.4 | ✅ 41.9 | bizimki daha iyi |
| 4.5.11 (omuzluk ≥ 1.5×) | ✅ 1.500× | ✅ 1.500× | eşit |
| 4.5.12 (entegrasyon gövdesi ≥ %75) | ✅ modelde var | ❌ MODELLENMEDİ | bizim tek gövdede entegrasyon parçası yok |
| 4.5.15 (≥ 2 ray butonu) | ✅ 2 | ❌ MODELLENMEDİ | bizim modelde ray butonu yok |
| 4.1.33 ("PAYLOAD" adı) | ❌ "Payload" | ✅ "PAYLOAD" | bizimki şartnameye uygun |
| 4.5.5 (malzeme) | ✅ karbon/fiberglas/alüminyum/Delrin | ✅ karbon/G10/ripstop | her ikisi de uygun |
| 4.5.9 (mapalar) | ❌ MODELLENMEDİ | ❌ MODELLENMEDİ | her ikisi de kütle olarak modellendi |

## Sonuç: kim daha iyi?

**İrtifa:** Bizim tasarım **5857.6 m** (standart koşu) vs örneklerin en yükseği
**5827.8 m** (kayıtlı). Fark **+30 m**. Yani bizimki daha yüksek.

**Küt (kalkış):** Bizimki **14.49 kg** vs örnekler **17.86 kg** (3.4 kg fark).
Daha hafif gövde (karbon 1.5 mm vs fiberglas 2.0 mm) ve daha hafif aviyonik
(1.0 kg vs 0.52 kg + alüminyum merkezleme halkaları) sayesinde.

**Max hız:** Bizimki 450 m/s (Mach 1.36) vs örnekler 379 m/s (Mach 1.14). Daha
hafif roket daha hızlı çıkıyor.

**0.3 Mach stabilite:** Bizimki 1.738 vs örnekler 1.75–1.79. Eşit.

**Kalkış stabilitesi:** Bizimki 1.610 cal vs örnekler 0.72–0.74 cal. **Bizimki
çok daha iyi** (örnekler `stability-min-low` uyarısı alıyor).

**Burnout stabilitesi:** Bizimki 3.09 cal vs örnekler 4.71–4.75 cal. **Örnekler
aşırı stabil** (weathercocking riski daha yüksek).

**Kurtarma:** Örnekler 4.2.3/4.3.3/4.5.12'yi **modelde de** gösteriyor (iki kademe).
Bizimki bu maddeleri modelde gösteremiyor (tek gövde). Bu, bizim tasarımın
**en büyük eksikliği**.

## İlgili Sayfalar

[[en-yuksek-irtifa]] · [[bozok-cetin-06-m1850]] · [[2027-a2-1-bozok-m1850]] ·
[[bizim-tasarim-m1850]] · [[kutle-tabani-m1850]] · [[m1850-apogee-fizigi]] ·
[[motor-m1850]]
