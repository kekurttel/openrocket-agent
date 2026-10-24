# TEKNOFEST 2026 A2/A4 (M1850) — nihai tasarım

> **Durum: nihai simülasyon tasarımı.** Ayrıntılı rapor ve şartname uyum matrisi:
> **[`FINAL_REPORT.md`](FINAL_REPORT.md)**. Bu klasördeki `README.md` ve
> `simulation-results.json` **eski** (795.8 m) sonuca aittir; 22 Ekim 2026'da
> düzeltilmiş ve nihai tasarımla değiştirilmiştir.
>
> Düzeltme notu (eski sonucun neden geçersiz olduğu):
> [`CORRECTED_BASELINE.md`](CORRECTED_BASELINE.md).

## Dosyalar

| Dosya | İçerik |
|---|---|
| `rocket.ork` | **Nihai tasarım** (OpenRocket 24.12; OpenRocket'in kendi `<flightdata>` özeti ile) |
| `iterations/iter-1..4.ork` | Dört tasarım iterasyonunun tamamı |
| `FINAL_REPORT.md` | Kütle bütçesi, final metrikleri, paraşüt fazları, uyum matrisi, gerekçeler |
| `motors/Teknofest26_M1850_Rev1.eng` | Sabit motor eğrisi (AeroTech M1850 / TFM1850W) |
| `rocket-baseline-85deg.ork` | Düzeltilmiş koşullarla eski geometri (karşılaştırma tabanı, 5282.8 m) |
| `CORRECTED_BASELINE.md` | 795.8 m'lik eski sonucun geçersizliğinin gerekçesi |
| `simulation-results.json` | Nihai ölçümlerin makine-okunur özeti |

## Nihai ölçümler (OpenRocket 24.12, seed=1, rüzgâr 0, 1000 m, 6 m rampa, 85°)

| Metrik | Değer |
|---|---|
| Apogee (AGL) | **5857.6 m** (hedef 5800 ± %15 → 4930–6670) |
| Maksimum hız / Mach | 450.4 m/s / 1.359 |
| 0.3 Mach stabilite | **1.738 cal** (1.5–2.5) |
| Rampa çıkış hızı | **41.87 m/s** (≥ 25) |
| Kalkış kütlesi | **14.4948 kg** |
| Faz iniş hızları | birincil **15.31** / ikincil **8.40** / görev yükü podu **10.98 m/s** |

## Önemli uyarılar

- **10.5–11.5 kg kalkış kütlesi bandı fiziksel olarak imkânsızdır**: motor 7.010 kg +
  zorunlu PAYLOAD 4.000 kg = 11.010 kg zorunlu taban; 114 mm iç çaplı gerçek bir çerçeve
  ile taban ~14.5 kg'dır. Gerekçe: `FINAL_REPORT.md` §5.
- **Görev yükünün gövdeden ayrılması OpenRocket'ta modellenemez** (payload çıkınca
  gövde statik olarak kararsızlaşıyor). Gövde fazlarının iniş hızları payload yukarıdayken
  ölçülmüştür (alt sınır değerleri); payload'ın kendi inişi ayrı iki kademeli pod
  simülasyonuyla ölçülmüştür.
- Shear pin, SGU, havalandırma delikleri, yapısal/flutter analizi, ray butonu ve maper
  OpenRocket'ta modellenemez — uçuş öncesi ayrıca doğrulanmalıdır.
- **Gerçek uçuş öncesi tasarım OpenRocket 24.12 GUI'sinde elle kontrol edilmelidir.**
