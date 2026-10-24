---
type: meta
title: "İşlem Günlüğü"
status: active
created: 2026-10-22
updated: 2026-10-22T18:10:00
tags: [wiki, meta, log]
---

# Wiki İşlem Günlüğü

Append-only. Yeni kayıtlar dosyanın **en üstüne** eklenir.

## 2026-10-23 — `BAŞLI 3.roket.ork.zip` değerlendirildi

**İşlem:** EVALUATE (tek tasarım)

- `BAŞLI 3.roket.ork.zip` (zipped .ork) çözümlendi → `designs/BAŞLI3_eval.json`.
- Tasarım: Ahmet Efe BAŞLI, motor TFL1256WS (L1256WS, A1 kategorisi), Ø120 mm gövde,
  2009.5 mm toplam boy, 14.375 kg kalkış kütlesi.
- Apogee 2228.8 m (kayıtlı) / 2276.5 m (standart koşu). A1 asgari 1219 m aşıyor,
  A2 asgari 2438 m aşılamıyor.
- 0.3 Mach stabilite 2.069 cal (kendi koşusu) / 2.203 cal (standart) — band içinde.
- 24 maddelik şartname kontrolü: 12 GEÇTİ, 6 KALDI, 2 KISMİ, 2 UYARI, 1 ŞÜPHELI, 1 N/A.
- Başarısız/Eksik: görev yükü adı "FAYDALI YÜK" (PAYLOAD olmalı), görev yüküne
  ayrı paraşüt yok, fırlatma 90° (85° olmalı), havalandırma deliği yok, fırlatma
  kılavuz butonu yok, birincil paraşüt deploy anında 22.4 m/s.
- Wiki sayfası: `wiki/sources/basli-3-roket.md`. Kaynak dizini güncellendi (15 tasarım).

## 2026-10-23 — `örnekroket2/` klasörü çözümlendi, wiki güncellendi

**İşlem:** INGEST (5 yeni tasarım)

- 5 `.ork` dosyası `scratch/parse_ornek2.py` ile çözümlendi → `örnekroket2/parsed.json`.
  Her tasarım için: bileşen dökümü, kütle, malzeme, geometri, motor, fırlatma
  koşulları, paraşüt olayları, gömülü `<flightdata>`, kendi koşullarıyla ve
  standart koşullarla iki ayrı gerçek simülasyon, 0.3 Mach stabilitesi, 24 maddelik
  otomatik şartname kontrolü.
- Yeni wiki sayfaları: `13930-a2-bozokroket-m1850`, `ares-rocket-team-m2020`,
  `bozok-ahr-577323-l1256ws`, `cal-roket-ktr`, `rocket-2-ucok-l1256ws`.
- `wiki/sources/_index.md` güncellendi: 14 tasarım (9 + 5).
- `wiki/index.md` ve `wiki/overview.md` güncellendi: 14 tasarımın irtifa sıralaması.
- `wiki/hot.md` güncellendi.

**Bulgu:** `örnekroket2/` klasöründeki tasarımlar **negatif örnekler** olarak
değerli: Ares (27.9 kg, Ø136 mm, 3084 m), CAL (17.9 kg, Ø140 mm, paraşütler
NEVER, 1523 m), 13930_A2 (20.1 kg, Ø116 mm, 4246 m). Bu tasarımlar aynı motorla
(M1850) 5.8 km'ye çıkan Çetin 06 ile karşılaştırıldığında **küt ve sürükleme
artışı**nın irtifayı nasıl düşürdüğünü gösteriyor.

## 2026-10-22 — `örnek-roket/` klasörü çözümlendi, wiki kuruldu

**İşlem:** INGEST + SCAFFOLD (wiki çekirdeği)

- 8 `.ork` dosyası `scratch/parse_ornek.py` ile çözümlendi → `örnek-roket/parsed.json`.
  Her tasarım için: bileşen dökümü (tip/ad/kütle/malzeme/geometri), motor, fırlatma
  koşulları, paraşüt olayları, gömülü `<flightdata>`, **kendi koşullarıyla** ve
  **standart koşullarla (85° yükseliş, 6 m rampa, 1000 m, rüzgâr 0, seed 1)** iki ayrı
  gerçek simülasyon, 0.3 Mach stabilitesi ve 24 maddelik otomatik şartname kontrolü.
- Motor eğrileri `~/.openrocket/ThrustCurves/` altına kuruldu
  (`Teknofest26_L1256_Rev1.eng`, `Teknofest26_M1850_Rev1.eng`, `Teknofest26_N3300_Rev1.eng`)
  → .ork dosyaları yeniden açıldığında motor kaybolmuyor.
- Şartname metni çıkarıldı: `scratch/sartname.txt` (pdftotext).
- Wiki çekirdeği kuruldu: `wiki/index.md`, `overview.md`, `hot.md`, `log.md`,
  `wiki/sources/`, `wiki/entities/`, `wiki/concepts/`, `wiki/domains/`,
  `wiki/comparisons/`, `wiki/meta/`.
- Kaynak sayfaları iki paralel subagent tarafından üretildi:
  - M1850 grubu + karşılaştırmalar → `wiki/sources/{bozok-cetin-06-m1850,
    2027-a2-1-bozok-m1850, ucok-cetin-05-l1256ws, 2027-a1-3-bozok-l1256ws}.md`,
    `wiki/comparisons/{m1850-rekabet, en-yuksek-irtifa}.md`,
    `wiki/concepts/m1850-apogee-fizigi.md`
  - A1/L1256WS grubu → `wiki/sources/{2027-a1-1-cetin-04-l1256ws,
    altinok-cetin-04-l1256ws, kizlar-bozok-l1256ws, cerkezkoy-2027-l1256ws}.md`,
    `wiki/domains/a1-l1256ws-ailesi.md`

**Bulgu:** En yüksek irtifa örnekler arasında **Bozok – Çetin 06 (5827.8 m)**;
bu projenin M1850 tasarımı **5857.6 m** ile onu geçiyor. Şartname 3.2.17'ye göre
hedef, asgari irtifayı (A2/A4 → 2438 m) aşan **en yüksek** irtifadır.

## 2026-10-22 — M1850 yarışma tasarımı tamamlandı

**İşlem:** önceki oturum (bu wiki'nin konusu değil, kaynağı)

- `designs/m1850-teknofest/rocket.ork`: apogee **5857.6 m AGL**, kalkış kütlesi
  **14.4948 kg**, max 450.4 m/s (Mach 1.359), 0.3 Mach stabilite **1.738 cal**,
  rampa çıkışı **41.87 m/s**, üç paraşüt (Ø1.10 / Ø1.70 / Ø1.00).
- `pytest -q` → 48 passed. Ayrıntı: `designs/m1850-teknofest/FINAL_REPORT.md`.
