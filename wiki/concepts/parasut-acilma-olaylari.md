---
type: concept
title: "Paraşüt Açılma Olayları"
status: active
created: 2026-10-22
updated: 2026-10-22
tags: [kavram, openrocket, kurtarma, hata]
---

# Paraşüt Açılma Olayları

## OpenRocket olayları

`DeploymentConfiguration.DeployEvent` değerleri:

| Olay | Anlamı |
|---|---|
| `LAUNCH` | fırlatma anında |
| `EJECTION` | **motorun atma gecikmesi dolduğunda** (burnout + gecikme) |
| `APOGEE` | apogee olayında (+ `deploydelay` saniye) |
| `ALTITUDE` | verilen irtifada (+ `deploydelay`) |
| `NEVER` | hiç açılmaz |

Kritik ayrım: **`EJECTION` bir zaman noktasıdır (motor gecikmesi), `APOGEE` bir
olaydır.** Motorun atma gecikmesi 0 ise `EJECTION` = burnout anıdır.

## Bu depodaki hata ve etkisi

Örnek tasarımlarda üç paraşüt de `ejection` olayına bağlıydı. Motor gecikmesi 0
olduğu için hepsi **burnout'ta, ~355 m/s'de** açılıyordu ve apogee'yi 796 m'de
kesiyordu. `APOGEE` + `ALTITUDE 500 m` + `APOGEE + 1 s` olarak düzeltildiğinde
apogee 5282.8 m'ye çıktı.

## Şartname eşlemesi

| Madde | Olay |
|---|---|
| 4.1.7 — payload apogee'den ≤ 2 s sonra ayrılır | `APOGEE` + delay ≤ 2 s |
| 4.1.8 — ikincil paraşüt yere 400–600 m kala | `ALTITUDE` 500 m |
| 4.2.6 — birincil 9–20 m/s | `APOGEE` (0 s) |
| 4.2.7 — ikincil 5–9 m/s | `ALTITUDE` |
| 4.2.8 — payload 9–20 m/s | payload'ın kendi paraşütü, ayrı gövdede |

## Uygulama

```python
rocketlib.set_parachute_deployment(doc, "Birincil drogue", event="apogee")
rocketlib.set_parachute_deployment(doc, "Ikincil ana", event="altitude", altitude=500.0)
rocketlib.set_parachute_deployment(doc, "Gorev yuku parasutu", event="apogee", delay=1.0)
```

## Tek gövde sınırı

Üç paraşüt aynı gövdede iken **bileşke** iniş hızı hesaplanır; bu, faz bazlı
hızları (4.2.6/4.2.7/4.2.8) doğrulamaz. Bu yüzden her faz **ayrı koşu** ile
ölçülmeli (yalnız birinci paraşüt açık / iki paraşüt açık / ayrı payload podu).

## İlgili Sayfalar

[[rampa-acisi-konusu]] · [[bizim-tasarim-m1850]] · [[m1850-rekabet]] ·
[[a1-l1256ws-ailesi]]
