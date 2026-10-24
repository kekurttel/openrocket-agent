---
type: concept
title: "M1850 ile Kütle Tabanı"
status: active
created: 2026-10-22
updated: 2026-10-22
tags: [kavram, m1850, kutle, yarisma]
---

# M1850 ile Kütle Tabanı

## Zorunlu kütle

| Bileşen | kg |
|---|---|
| AeroTech M1850 / TFM1850W (toplam) | 7.010 |
| PAYLOAD (şartname 4.3.2, asgari 4.0 kg) | 4.000 |
| **Zorunlu taban** | **11.010** |

11.5 kg bandının üst sınırında yalnızca **0.49 kg** kalır. 114 mm iç çaplı,
1.5 mm karbon gövdeli, kanatlı, üç paraşütlü, aviyonikli bir roket için bu
mümkün değildir; gerçekçi taban **~14.5 kg**'dır.

## Gerçek örnekler ne yapmış?

Şartname motoru kategoriye bağlıyor (4.1.18/4.1.19/4.1.20): A1 → L1256WS,
A2/A4 → M1850, A3 → N3300. Örnekler:

| Tasarım | Motor | Kalkış kütlesi | Apogee (kayıtlı) |
|---|---|---|---|
| Bozok – Çetin 06 | M1850 | 17.857 kg | 5827.8 m |
| 2027 A2_1 – Bozok | M1850 | 17.879 kg | 5815.2 m |
| Bu projenin tasarımı | M1850 | **14.495 kg** | **5857.6 m** |
| 2027 A1_1 – Çetin 04 | L1256WS | 11.397 kg | 3656.2 m |
| Kızlar – Bozok | L1256WS | 12.024 kg | 3411.1 m |

İki örnek M1850 roketi 17.9 kg'da ve ince gövdeyle (Ø98 mm) 5.8 km'ye ulaşıyor;
bizimki 3.4 kg daha hafif ama kalın gövdeli (Ø117 mm) ve **30 m daha yüksek**.

## Fizik

Motor verisi (`.eng` eğrisinden): tepe itki 2411 N, yanma süresi 6.75 s,
ortalama itki 1115 N, entegre itki ≈ 7524 N·s (trapezoidal), yakıt 4.103 kg.

- Apogee'yi belirleyen, kalkıştaki kütle değil **burnout kütlesi** ve **sürükleme**
  birlikte etkisidir.
- Örnekler: burnout kütlesi 13.8 kg, küçük çap (98 mm) → düşük sürükleme,
  ama yüksek başlangıç kütlesi.
- Bizimki: burnout kütlesi 10.4 kg, büyük çap (117 mm) → yüksek sürükleme,
  ama düşük başlangıç kütlesi.
- Net: ikisi de ~5.8 km'de; **kütle kazananı, çap kaybedeni telafi ediyor.**

Bu, 4.5.15–4.5.22 gibi yapısal/müşteri maddelerinin modellenemediği bir
gerçekliktir: 1 gram kütlenin 10 metre irtifa etkisi vardır.

## Tasarım dersi

Kütle bandı zorunlu tabanın altına inemez; irtifa ise **bandın içinde
kalmayı** gerektirir (A2/A4 için asgari 2438 m). Bu yüzden doğru optimizasyon
hedefi "en düşük mümkün kütle" değil, **asgari irtifayı güvenli aşan en yüksek
irtifa**dır (şartname 3.2.17).

## İlgili Sayfalar

[[m1850-apogee-fizigi]] · [[motor-m1850]] · [[kutle-tabani-m1850]] ·
[[bizim-tasarim-m1850]] · [[en-yuksek-irtifa]]
