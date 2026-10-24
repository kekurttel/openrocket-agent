---
type: meta
title: "Çözümleme Yöntemi"
status: active
created: 2026-10-22
updated: 2026-10-22
tags: [wiki, meta, metodoloji, openrocket]
---

# Çözümleme Yöntemi

8 `.ork` dosyasının tamamı **tek bir betikle** çözüldü ve **gerçek simülasyonlarla**
doğrulandı. Model çıktısı değil, kod çıktısıdır.

## Betik

`scratch/parse_ornek.py` → `örnek-roket/parsed.json`

Her dosya için üç aşama:

### 1. Yapı çözümlemesi (deterministik)
`rocketlib` + doğrudan OpenRocket Java API ile:

- Bileşen listesi: tip, ad, kütle, **malzeme adı + yoğunluğu**, geometri
  (uzunluk, yarıçap, cidar, kanat sayısı/kök/kanat/süpürme, omuzluk, paraşüt
  çapı/Cd/hat/ip), eksenel konum, üst bileşen.
- Motor: tanım, üretici, çap, uzunluk, yakıt/toplam kütle, ateşleme olayı/gecikmesi.
- Fırlatma koşulları: rampa boyu, **rampa açısı (düşeyden ve yükseliş olarak)**,
  rüzgâr + türbülans, fırlatma irtifası, sıcaklık, basınç, seed, simülasyon adı.
- Paraşüt olayları: `DeployEvent`, `deployAltitude`, `deployDelay`.
- Dosyaya gömülü `<flightdata>`: `maxaltitude`, `maxvelocity`, `maxmach`,
  `timetoapogee`, `flighttime`, `groundhitvelocity`, `launchrodvelocity`,
  `deploymentvelocity`, `optimumdelay` + olay listesi.

### 2. Gerçek yeniden simülasyon (iki koşu)
1. **Kendi koşullarıyla:** dosyanın kendi ayarlarıyla, `seed=1`.
2. **Standart koşul koşusu:** `rod_length=6.0`, `rod_angle=85` (yani 5° düşeyden),
   `launch_altitude=1000`, `wind_speed=0`, `wind_turbulence=0`, `seed=1`.

Ek olarak 0.3 Mach stabilitesi, zaman serisinden (`TYPE_MACH_NUMBER`,
`TYPE_STABILITY`) Mach ≥ 0.3 olan ilk nokta alınarak okundu.

### 3. Otomatik şartname kontrolü
24 maddenin makine-okunabilir kısmı: sabit çap / transition yok, payload adı ve
kütlesi, paraşüt sayısı ve olayları, yasak malzeme taraması (karton/PVC/kraft/PLA),
gövde cidarı, kanat cidarı, burun omuzluğu oranı, delik sayısı, ray butonu sayısı,
apogee ≥ 2438 m, rampa çıkışı ≥ 25 m/s, 0.3 Mach stabilitesi 1.5–2.5 kal.

## Doğrulama

Yeniden koşular, dosyalara gömülü kayıtlarla **< 0.7 %** içinde eşleşti
(ör. Bozok Çetin 06: kayıtlı 5827.8 m ↔ kendi koşuluyla 5828.9 m). Bu, hem
motor eğrisinin hem de simülasyon ayarlarının doğru yüklendiğini kanıtlıyor.

## Sınırlar

- OpenRocket Barrowman aerodinamiğidir; CFD değildir.
- Supersonik hızda OpenRocket "gövde hesapları tam doğru olmayabilir" uyarısı verir.
- Renk, malzeme markası, üretim detayı (shear pin, SGU, mapalar) `.ork` modelinde
  yoktur → bu maddeler "MODELLENMEDİ" olarak işaretlenir.
- Rüzgâr/türbülans modelleri OpenRocket 24.12'de **süreç başına entropi** çeker;
  rüzgârlı koşular arası tekrarlanabilirlik yoktur (rüzgârsız koşular birebir
  aynıdır).

## İlgili Sayfalar

[[veri-kaynaklari]] · [[en-yuksek-irtifa]] · [[rampa-acisi-konusu]]
