---
type: meta
title: "Hot Cache"
status: active
created: 2026-10-22
updated: 2026-10-22T18:10:00
tags: [wiki, meta, hot-cache]
---

# Recent Context

## Last Updated
2026-10-22 — `örnek-roket/` klasöründeki 8 yarışma tasarımının tamamı çözümlendi,
gerçek simülasyonlarla doğrulandı ve wiki sayfaları üretildi.

## Key Recent Facts
- **En yüksek irtifa:** Bu projenin M1850 tasarımı **6288.8 m AGL** (16.07 kg).
  Örnekler arasında en yüksek: **Bozok – Çetin 06 = 5827.8 m** (kayıtlı, 17.86 kg,
  M1850). İkinci: 2027 A2_1 – Bozok 5815.2 m. Üçüncü: 13930_A2_bozokroket 4246.1 m.
  L1256WS (A1) ailesi 2.7–4.0 km. Ares (Cesaroni) 3084.2 m, CAL 1522.7 m.
- **14 tasarım** çözümlendi (9 örnek-roket + 5 örnekroket2). Tüm sayılar gerçek
  OpenRocket 24.12 simülasyonlarından.
- **Negatif örnekler:** Ares Rocket (27.9 kg, Ø136 mm, 3084 m), CAL Roket (17.9 kg,
  Ø140 mm, paraşütler NEVER, 1523 m), 13930_A2 (20.1 kg, Ø116 mm, 4246 m),
  Bozok_Roket (12.84 kg, cardboard motor yatağı, 2839 m).
- Şartname 3.2.17 "en yüksek irtifa"yı açıkça ödüllendirir; A2/A4 asgari irtifa
  8.000 ft = 2438 m, A1 için 4.000 ft.
- Motor kategoriyle sabit: A1→L1256WS (4.1.18), A2/A4→M1850 (4.1.19), A3→N3300 (4.1.20).
- İki M1850 örneği **iki kademeli** (üst+alt gövde, alüminyum TubeCoupler entegrasyon
  gövdesi, "Ayırma Sistemi") → 4.3.3/4.2.3/4.5.12'yi gerçekten çözüyor.
- 8 örnekte de `Hole` bileşeni yok → 4.5.2 havalandırma delikleri modellenmemiş.
- 8 örnekte de görev yükü adı "Payload" (şartname 4.1.33 "PAYLOAD" diyor).
- Parse çıktısı: `örnek-roket/parsed.json`; üretici: `scratch/parse_ornek.py`.
- Şartname metni: `scratch/sartname.txt` (pdftotext, 2905 satır).

## Recent Changes
- Created: [[index]], [[overview]], [[hot]], [[log]], [[parsing-methodology]],
  [[veri-kaynaklari]], [[rampa-acisi-konusu]], [[parasut-acilma-olaylari]],
  [[kutle-tabani-m1850]], [[motor-m1850]], [[motor-l1256ws]], [[takim-bozok]],
  [[takim-cetin]], [[bizim-tasarim-m1850]]
- Created (subagent): [[bozok-cetin-06-m1850]], [[2027-a2-1-bozok-m1850]],
  [[ucok-cetin-05-l1256ws]], [[2027-a1-3-bozok-l1256ws]], [[en-yuksek-irtifa]],
  [[m1850-rekabet]], [[m1850-apogee-fizigi]]
- Created (subagent): [[2027-a1-1-cetin-04-l1256ws]], [[altinok-cetin-04-l1256ws]],
  [[kizlar-bozok-l1256ws]], [[cerkezkoy-2027-l1256ws]], [[a1-l1256ws-ailesi]]
- İki kütüphane hatası düzeltildi: rampa açısı yönü (`rocketlib/launch.py`) ve
  `.ork` motor kaybı (`rocketlib/io.py` + `~/.openrocket/ThrustCurves/`).

## Active Threads
- Kullanıcı: "şartnameye göre final en yüksek irtifa" — sonuç [[en-yuksek-irtifa]].
- Açık soru: iki kademeli model bizim tek gövdeli tasarımımıza taşınabilir mi?
  (Payload ayrılınca gövde statik kararsızlaşıyor: CP−CG = −0.056 m.)
