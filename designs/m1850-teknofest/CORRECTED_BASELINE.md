# Düzeltilmiş Başlangıç (22 Ekim 2026)

Bu not, `README.md` ve `simulation-results.json` içindeki **795.8 m** apogee
sonucunun neden geçersiz olduğunu ve gerçek başlangıç noktasını kaydeder.

## İki kritik hata düzeltildi

1. **Rampa açısı ters yorumlanıyordu.** `rocketlib.set_launch_conditions()`
   `rod_angle` değerini "yataydan" diye belgeliyor, fakat OpenRocket'a olduğu
   gibi gönderiyordu. OpenRocket rampa açısını **düşeyden** ölçer ve ±60° ile
   sınırlar. Sonuç: 85° isteği 60° düşeyden (= 30° yükseliş) uçuşa dönüştü.
   `rocketlib/launch.py` artık `90° − rod_angle` gönderiyor. 85° → 5° düşeyden
   (85° yükseliş) olarak doğru modelleniyor.
2. **Paraşütler burnout'ta açılıyordu.** Üç paraşüt de `deployevent=ejection`
   idi; motorun ejeksiyon gecikmesi 0 olduğu için 355 m/s'de açılıp apogee'yi
   796 m'de kesiyordu. Doğru olaylar: birincil `APOGEE`, ikincil `ALTITUDE
   500 m`, görev yükü `APOGEE + 1 s`.

## Gerçek ölçümler (seed=1, rüzgâr 0, fırlatma irtifası 1000 m, 6 m rampa)

| Tasarım | Kalkış kütlesi | Apogee (AGL) | Max hız | Rampa çıkışı | 0.3 Mach stabilite |
|---|---|---|---|---|---|
| Mevcut `.ork` (karton yoğunluğu 680 kg/m³) | 13.86 kg | **5282.8 m** | 449.5 m/s (M1.36) | 42.6 m/s | ~1.86 cal |
| Aynı geometri, gerçek karbon (1550) + G10 (1900) | 14.97 kg | **5085.1 m** | 418.5 m/s (M1.26) | 40.4 m/s | **1.81 cal** |

> Not: Mevcut `.ork`'taki "carbon/fiberglass/G10" adlı bileşenlerin malzemesi
> gerçekte **karton** (680 kg/m³). Gerçek malzemeler kütleyi ~1.1 kg artırır.

## Kütle tabanı (fiziksel)

- M1850 motor toplam kütlesi: **7.010 kg**
- PAYLOAD: **4.000 kg**
- Zorunlu toplam: **11.010 kg**

Geriye hava çerçevesi + kurtarma + aviyonik için yalnızca **0.49 kg** kalır ki
114 mm gövdeli, 1.45 m'lik bir roket için bu mümkün değildir. Gerçekçi en
düşük kalkış kütlesi **~13.5–14.0 kg**'dır. 10.5–11.5 kg bandı, motor ve
görev yükü kütleleri nedeniyle ulaşılamaz; hedef irtifa bandı (4930–6670 m)
ise gerçek malzemelerle de ulaşılabilir (5085 m ölçüldü).

## Motorun dosyada kalıcı olması

OpenRocket 24.12 `.ork` içine thrust curve **gömmüyor**. Motorun yeniden
yüklenebilmesi için `.eng` dosyası kullanıcı motor dizininde olmalı:

```
~/.openrocket/ThrustCurves/Teknofest26_M1850_Rev1.eng
```

Bu makinede bu dosya kuruldu; `rocket-baseline-85deg.ork` yeniden açıldığında
motor `TFM1850W` olarak geliyor ve aynı apogee'yi (5282.8 m) veriyor.

## Paraşüt olaylarını ayarlama

```python
rocketlib.set_parachute_deployment(doc, "Drogue proxy", event="apogee")
rocketlib.set_parachute_deployment(doc, "Payload chute", event="apogee", delay=1.0)
rocketlib.set_parachute_deployment(doc, "Main proxy", event="altitude", altitude=500.0)
```

Malzeme ve yüzey kaplaması için:

```python
rocketlib.set_component_material(doc, "Body tube", material_name="Carbon fiber", density=1550.0)
rocketlib.set_surface_finish(doc, "Body tube", "polished")
rocketlib.set_nose_shoulder(doc, "Nose cone", length=0.1755)
```

## 0.3 Mach stabilitesi

Zaman serisinden okunur (`TYPE_MACH_NUMBER` + `TYPE_STABILITY`); gerçek
malzemeli geometride **1.81 cal** (t=0.82 s, Mach 0.306). Hedef 1.5–2.5 cal.

## Dosyalar

- `rocket-baseline-85deg.ork` — düzeltilmiş koşullarla kaydedilmiş mevcut
  geometri (karton malzeme; karşılaştırma tabanı).
- `motors/Teknofest26_M1850_Rev1.eng` — sabit motor eğrisi.
- `simulation-results.json` / `README.md` — **eski**, 795.8 m'lik hatalı
  sonuca dayanır; yeni tasarım raporu bunların yerine geçmelidir.
