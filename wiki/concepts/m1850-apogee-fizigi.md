---
type: concept
title: "M1850 ile Apogee Fiziği"
status: active
created: 2026-10-22
updated: 2026-10-22
tags: [kavram, m1850, fizik, apogee, kutle, drag]
---

# M1850 ile Apogee Fiziği

AeroTech M1850 (TFM1850W): toplam kütle 7.010 kg, yakıt 4.103 kg,
entegre itki ≈ 7524 N·s (trapezoidal), yanma 6.75 s, tepe itki 2411 N,
ortalama itki 1115 N, özgül itki ≈ 187 s.

## Zorunlu kütle tabanı

| Bileşen | kg |
|---|---|
| Motor (toplam) | 7.010 |
| PAYLOAD (şartname 4.3.2, asgari 4.0 kg) | 4.000 |
| **Zorunlu taban** | **11.010** |

## Gerçekçi kütle tabanı

114 mm iç çaplı, 1.5 mm karbon gövdeli bir roketin hava çerçevesi payı:

| Alt sistem | Tipik kütle (kg) |
|---|---|
| Gövde (1.5 m × Ø117 mm × 1.5 mm karbon) | 1.3 |
| Burun (468 mm ogive, karbon) | 0.26 |
| Kanatlar (3× G10 3 mm) | 0.21 |
| Motor yuvası (karbon 1.5 mm) | 0.36 |
| Paraşütler (3) | 0.39 |
| Aviyonik (2 UKB + GPS + batarya) | 1.00 |
| Mapalar, centering ring'ler, civatalar | 0.30 |
| **Hava çerçevesi toplamı** | **≈ 3.82** |
| **Gerçekçi taban** | **≈ 14.83 kg** |

Bizim tasarım: **14.49 kg** (burun biraz daha hafif, kanatlar biraz daha küçük).

## Örnekler neden 17.86 kg ile aynı irtifaya ulaşıyor?

Örnek M1850 tasarımları (Bozok Çetin 06, 2027 A2_1):

- **İki kademeli:** üst gövde (görev yükü + payload paraşütü) + alt gövde
  (motor + ana/sürüklenme paraşütleri) + alüminyum entegrasyon gövdesi (0.658 kg).
- **Fiberglas gövde 2.0 mm** (karbon 1.5 mm yerine) → daha ağır gövde.
- **Alüminyum kanatlar 3 mm** (G10 yerine) → daha ağır kanatlar.
- **Aviyonik 0.52 kg** (bizimki 1.00 kg) → daha hafif aviyonik, ama alüminyum
  merkezleme halkaları (0.5–0.6 kg) ekstra kütle.
- **Ø98 mm gövde** (bizimki Ø117 mm) → 42 % daha az frontal alan → daha az sürükleme.

**Net etki:** küt (17.86 vs 14.49, +23 %) ve sürükleme (Ø98 vs Ø117, -42 %)
birbirini **telafi ediyor**; apogee farkı yalnız **+30 m** (%0.5).

## Burnout kütlesi ve apogee

Apogee'yi belirleyen, kalkıştaki kütle değil **burnout kütlesi** ve **sürükleme**
birlikte etkisidir:

| Tasarım | Burnout kütlesi (kg) | Apogee (m) |
|---|---|---|
| Bizimki | ~10.39 | **5857.6** |
| Bozok Çetin 06 | ~13.75 | 5827.8 |
| 2027 A2_1 | ~13.77 | 5815.2 |

Burnout kütlesi 3.4 kg daha hafif olmamıza rağmen apogee yalnız 30 m daha
yüksek: çünkü bizimki daha kalın gövdeli (Ø117 vs Ø98 mm) ve daha uzun burunlu
(468 vs 350 mm) → sürükleme alanımız daha büyük. **Kütle kazanımı, sürükleme
kaybını tam olarak telafi ediyor.**

## Max hız farkı

| Tasarım | Max hız (m/s) | Mach |
|---|---|---|
| Bizimki | **450.4** | 1.359 |
| Bozok Çetin 06 | 379.1 | 1.141 |
| 2027 A2_1 | 378.5 | 1.140 |

Daha hafif roket (14.49 kg) daha hızlı çıkıyor (450 vs 379 m/s, +19 %) ama
daha kalın gövde nedeniyle coast fazında daha fazla sürükleme kaybediyor.
Net: apogee farkı küçük.

## Burnout stabilitesi farkı

| Tasarım | Burnout stabilitesi (cal) |
|---|---|
| Bizimki | 3.09 |
| Bozok Çetin 06 | 4.71 |
| 2027 A2_1 | 4.75 |

Örnekler **aşırı stabil** (> 2.5 cal): weathercocking (rüzgâra dönüş) riski
daha yüksek. Bizimki 3.09 cal ile daha dengeli. Şartname 4.4.5 yalnızca 0.3 Mach'ta
(1.5–2.5 cal) stabilite ister; burnout değeri düzenlenmiyor.

## Kalkış stabilitesi farkı

| Tasarım | Kalkış stabilitesi (cal) |
|---|---|
| Bizimki | **1.610** |
| Bozok Çetin 06 | 0.718 |
| 2027 A2_1 | 0.740 |

Örnekler kalkışta **1.0 cal altında** (örnekler `stability-min-low` uyarısı alıyor).
Bizimki 1.610 cal ile kalkışta çok daha stabil. Bu, bizim tasarımın **en önemli
üstünlüğü**: rüzgârda daha az weathercocking, daha güvenli fırlatma.

## İlgili Sayfalar

[[m1850-rekabet]] · [[kutle-tabani-m1850]] · [[motor-m1850]] ·
[[bozok-cetin-06-m1850]] · [[2027-a2-1-bozok-m1850]] · [[bizim-tasarim-m1850]] ·
[[en-yuksek-irtifa]]
