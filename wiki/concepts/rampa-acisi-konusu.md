---
type: concept
title: "Rampa Açısı Konusu (85° Yükseliş)"
status: active
created: 2026-10-22
updated: 2026-10-22
tags: [kavram, openrocket, firlatma, hata]
---

# Rampa Açısı Konusu

## Kural

**OpenRocket rampa açısını düşeyden ölçer** (0° = tam dikey) ve değeri
**±60° ile sınırlar**. Şartname 4.1.35 ise **85° yükseliş** (yataydan) ister.

Dönüşüm: `OpenRocket açısı = 90° − yükseliş`

| Yükseliş (yataydan) | OpenRocket (düşeyden) | Durum |
|---|---|---|
| 90° | 0° | dikey |
| 85° | **5°** | şartnamenin istediği |
| 60° | 30° | |
| 30° | 60° | OpenRocket'ın üst sınırı |
| < 30° | — | **OpenRocket'ta modellenemez** (60°'ye kırpılır) |

## Bu depodaki hata ve etkisi

`rocketlib.set_launch_conditions()` `rod_angle` değerini "yataydan" diye
belgeliyordu ama OpenRocket'a olduğu gibi (radyan olarak) gönderiyordu. 85° isteği
→ OpenRocket 85° düşeyden → **60°'ye kırpıldı** → roket **30° yükselişle** uçtu.

Ölçülen fark (aynı tasarım, M1850, 13.86 kg):

| Model | Apogee |
|---|---|
| 85° yanlış (30° yükseliş) + paraşütler burnout'ta | **795.8 m** |
| 85° doğru (85° yükseliş) + paraşütler apogee'de | **5282.8 m** |

Hata iki kez birleşince "M1850 ile 6 km imkânsız" gibi görünen bir sonuç
doğdu; oysa iki tasarım da doğru yorumlandığında hedef bandın içindeydi.

**Düzeltme:** `rocketlib/launch.py` artık `math.radians(90.0 - rod_angle)` gönderiyor.
Böylece `rod_angle=85` → 5° düşeyden → gerçek 85° yükseliş.

## Şartnamedeki karşılığı

- 4.1.35 → 85° yükseliş ✅
- 4.4.8 → rampa çıkış hızı ≥ 25 m/s (85° ile 41.87 m/s; 30° ile ~17 m/s olurdu)

## İlgili Sayfalar

[[parasut-acilma-olaylari]] · [[kutle-tabani-m1850]] · [[bizim-tasarim-m1850]] ·
[[parsing-methodology]]
