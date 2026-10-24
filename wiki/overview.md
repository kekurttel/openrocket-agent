---
type: meta
title: "Yönetici Özeti"
status: active
created: 2026-10-22
updated: 2026-10-22
tags: [wiki, ozet, teknofest-2026]
---

# Yönetici Özeti

## Ne yapıldı

`örnek-roket/` klasöründeki **8 yarışma tasarımının tamamı** çözümlendi
(`scratch/parse_ornek.py` → `örnek-roket/parsed.json`): bileşen dökümü, kütle,
malzeme, geometri, motor, fırlatma koşulları, paraşüt olayları, dosyaya gömülü
`<flightdata>` ve **gerçek OpenRocket 24.12 yeniden simülasyonları** (hem tasarımın
kendi koşullarıyla hem de standart koşul koşuluyla).

## En yüksek irtifa

Şartname 3.2.17, takımlardan "asgari irtifalardan daha düşük olmamak kaydıyla
**en yüksek irtifaya erişecek**" roketleri tasarlamalarını istiyor. A2/A4 için
asgari irtifa **8.000 ft (2438 m)**.

| # | Tasarım | Motor | Kayıtlı apogee | Standart koşu | Kalkış kütlesi |
|---|---|---|---|---|---|
| 1 | **Bu projenin M1850 tasarımı** | M1850 | — | **6288.8 m** | 16.07 kg |
| 2 | Bozok – Çetin 06 | M1850 | **5827.8 m** | 5790.0 m | 17.86 kg |
| 3 | 2027 A2_1 – Bozok | M1850 | 5815.2 m | 5776.9 m | 17.88 kg |
| 4 | 13930_A2_bozokroket | M1850 | 4246.1 m | 4215.3 m | 20.11 kg |
| 5 | Üçok – Çetin 05 | L1256WS | 4001.4 m | 3976.1 m | 11.24 kg |
| 6 | 2027 A1_3 – Bozok | L1256WS | 3735.4 m | 3709.8 m | 11.28 kg |
| 7 | Çerkezköy 2027 | L1256WS | 3699.1 m | 3674.9 m | 11.35 kg |
| 8 | Altınok – Çetin 04 | L1256WS | 3685.4 m | 3661.7 m | 11.38 kg |
| 9 | 2027 A1_1 – Çetin 04 | L1256WS | 3656.2 m | 3632.8 m | 11.40 kg |
| 10 | Kızlar – Bozok | L1256WS | 3411.1 m | 3388.6 m | 12.02 kg |
| 11 | Bozok_Roket (AHR) | L1256WS | 2838.8 m | 2821.4 m | 12.84 kg |
| 12 | rocket (2) – Üçok | L1256WS | 2700.0 m | 2686.3 m | 12.86 kg |
| 13 | Ares Rocket Team | Cesaroni 8429M2020-P | 3084.2 m | 3091.9 m | 27.90 kg |
| 14 | CAL Roket | Cesaroni 3727L1050-P | 1522.7 m | 1519.2 m | 17.88 kg |

**Hüküm:** Örnekler arasında en yüksek irtifa **Bozok Roket Takımı – Çetin 06**
(5827.8 m kayıtlı). Bu projenin M1850 tasarımı aynı motorla **5857.6 m** ile
onu geçiyor. L1256WS (A1) ailesi 3.4–4.0 km'de kalıyor.

## Motor sınıfı ne belirliyor

- **A1 → L1256WS** (şartname 4.1.18), **A2/A4 → M1850** (4.1.19),
  **A3 → N3300** (4.1.20). Motor seçimi takımın elinde değil, kategoriyle belirlenir.
- Aynı motor içinde kazananı **kütle–sürükleme dengesi** belirliyor: örnek M1850
  roketleri 17.86 kg ve ince (98 mm) gövdeyle, bizimki 14.49 kg ve kalın (117 mm)
  gövdeyle neredeyse aynı irtifaya ulaşıyor. Detay: [[m1850-apogee-fizigi]].

## Şartname uyumunda öne çıkan tespitler

- **4.2.3 / 4.3.3 (görev yükünün bağımsız kurtarılması):** iki M1850 örneği
  **iki kademeli** çözüm kullanıyor (üst gövde + alt gövde + alüminyum entegrasyon
  gövdesi + ayırma sistemi). A1 örnekleri tek kademede kalıyor.
- **4.2.16 (her paraşüt farklı ve koyu renk):** modellerde renk bilgisi yok —
  tasarım dosyasında karşılanamayan, imalat/kayıt aşamasında sağlanan madde.
- **4.5.2 (3× 3.0–4.5 mm havalandırma deliği):** 8 tasarımın **hiçbirinde**
  `Hole` bileşeni yok → modelde modellenmemiş.
- **4.1.33 (görev yükü "PAYLOAD" adıyla):** örneklerde ad "Payload";
  şartnamedeki isimlilik kuralına tam uymuyor.
- **0.3 Mach stabilitesi (4.4.5):** tüm örnekler 1.99–2.59 kal bandında;
  `2027 A1_1` 2.593 kal ile 2.5 üstünde (sınır dışı).
- **4.5.11 (burun omuzluğu ≥ 1.5× dış çap):** 8 örnekte de tam 1.5 oranı,
  ölçülerek sağlanmış.

## Öğrenilen dersler (bu depodaki kütüphane hataları)

1. [[rampa-acisi-konusu]] — hatalı açı yorumu 795.8 m'lik (gerçek: 5282.8 m) sahte bir
   başarısızlık üretti.
2. [[parasut-acilma-olaylari]] — `ejection` olayı, motor gecikmesi 0 ise
   burnout'ta açılır ve apogee'yi keser.
3. [[kutle-tabani-m1850]] — motor + payload zorunlu tabanı 11.010 kg.
