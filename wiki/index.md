---
type: meta
title: "Wiki Dizini"
status: active
created: 2026-10-22
updated: 2026-10-22
tags: [wiki, indeks, teknofest-2026]
---

# Wiki Dizini

TEKNOFEST 2026 A Grup roket yarışması için hazırlanan bilgi tabanı. Kaynaklar
`örnek-roket/` klasöründeki 8 yarışma tasarımı (.ork) + bu depoda geliştirilen
M1850 yarışma tasarımıdır. Tüm sayılar **gerçek OpenRocket 24.12 simülasyonlarından**
veya dosyalara gömülü `<flightdata>` kayıtlarından gelir.

## Hızlı cevap

**En yüksek irtifa → [[en-yuksek-irtifa]]** (şartname 3.2.17: "asgari irtifalardan
daha düşük olmamak kaydıyla **en yüksek irtifaya erişecek** roketleri tasarlamaları")

## Kaynak Sayfaları (`wiki/sources/`) — 14 tasarım

### A2/A4 — M1850 / diğer motorlar (asgari irtifa 8000 ft = 2438 m)

| Sayfa | Takım | Motor | Kayıtlı apogee | Standart koşu | Çap (mm) |
|---|---|---|---|---|---|
| [[bizim-tasarim-m1850]] | **Bu proje** | **M1850** | — | **6288.8 m** | 98 |
| [[bozok-cetin-06-m1850]] | Çetin | **M1850** | 5827.8 m | 5790.0 m | 98 |
| [[2027-a2-1-bozok-m1850]] | Bozok | **M1850** | 5815.2 m | 5776.9 m | 98 |
| [[13930-a2-bozokroket-m1850]] | Bozok | **M1850** | 4246.1 m | 4215.3 m | 116 |
| [[ares-rocket-team-m2020]] | Ares Rocket Team | Cesaroni 8429M2020-P | 3084.2 m | 3091.9 m | 136 |
| [[cal-roket-ktr]] | CAL Roket | Cesaroni 3727L1050-P | 1522.7 m | 1519.2 m | 140 |

### A1 — L1256WS (asgari irtifa 4000 ft = 1219 m)

| Sayfa | Takım | Motor | Kayıtlı apogee | Standart koşu | Çap (mm) |
|---|---|---|---|---|---|
| [[ucok-cetin-05-l1256ws]] | Çetin 05 | L1256WS | 4001.4 m | 3976.1 m | 85 |
| [[2027-a1-3-bozok-l1256ws]] | Bozok | L1256WS | 3735.4 m | 3709.8 m | 97 |
| [[cerkezkoy-2027-l1256ws]] | Çerkezköy | L1256WS | 3699.1 m | 3674.9 m | 97 |
| [[altinok-cetin-04-l1256ws]] | Çetin 04 | L1256WS | 3685.4 m | 3661.7 m | 97 |
| [[2027-a1-1-cetin-04-l1256ws]] | Çetin 04 | L1256WS | 3656.2 m | 3632.8 m | 97 |
| [[kizlar-bozok-l1256ws]] | Bozok Rocket | L1256WS | 3411.1 m | 3388.6 m | 98 |
| [[bozok-ahr-577323-l1256ws]] | Bozok Rocket | L1256WS | 2838.8 m | 2821.4 m | 98 |
| [[rocket-2-ucok-l1256ws]] | Üçok | L1256WS | 2700.0 m | 2686.3 m | 98 |
| [[basli-3-roket]] | Ahmet Efe BAŞLI | L1256WS | 2228.8 m | 2276.5 m | 120 |

## Karşılaştırmalar (`wiki/comparisons/`)

- [[en-yuksek-irtifa]] — 9 tasarımın irtifa sıralaması ve "final en yüksek irtifa" hükmü
- [[m1850-rekabet]] — iki örnek M1850 tasarımı ile bizim tasarımımızın madde madde karşılaştırması

## Alanlar (`wiki/domains/`)

- [[a1-l1256ws-ailesi]] — L1256WS / A1 ailesinin karakteri (4 tasarım)

## Kavramlar (`wiki/concepts/`)

- [[rampa-acisi-konusu]] — OpenRocket rampa açısını düşeyden ölçer; 85° yükseliş = 5° düşey
- [[parasut-acilma-olaylari]] — APOGEE / ALTITUDE / EJECTION olayları ve doğru kullanımı
- [[kutle-tabani-m1850]] — M1850 ile 10.5–11.5 kg bandının neden ulaşılamadığı

## Varlıklar (`wiki/entities/`)

- [[motor-m1850]] · [[motor-l1256ws]] · [[takim-bozok]] · [[takim-cetin]]

## Meta (`wiki/meta/`)

- [[parsing-methodology]] — 8 `.ork` dosyasının nasıl çözümlendiği ve yeniden simüle edildiği
- [[veri-kaynaklari]] — hangi dosya hangi veriyi üretti

## Diğer çekirdek sayfalar

- [[overview]] — yönetici özeti
- [[hot]] — son bağlam özeti (hot cache)
- [[log]] — işlem günlüğü (append-only)
