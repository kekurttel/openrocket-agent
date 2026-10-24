# LEARN.md — Açık Roket Tasarım Dersleri

Bu dosya, TEKNOFEST 2026 A2/A4 (M1850) tasarım sürecinde yapılan hatalar,
keşfedilen sınırlar ve öğrenilen dersleri kaydeder. Her yeni iterasyon bu
dersleri güncellemeli ve genişletmelidir.

---

## 1. KRİTİK HATALAR (maliyetli olanlar)

### 1.1 Rampa açısı ters yorumlandı
- **Hata:** `rocketlib.set_launch_conditions()` `rod_angle` değerini "yataydan" diye
  belgeliyordu ama OpenRocket'a olduğu gibi gönderiyordu. OpenRocket rampa açısını
  **düşeyden** ölçer ve ±60° ile sınırlar.
- **Sonuç:** 85° isteği 60° düşeyden (= 30° yükseliş) uçuşa dönüştü. Apogee
  795.8 m olarak ölçüldü (gerçek: 5282.8 m). Tüm "6 km imkânsız" sonucu bu
  hatadan kaynaklandı.
- **Düzeltme:** `rocketlib/launch.py` artık `math.radians(90.0 - rod_angle)` gönderiyor.
  85° → 5° düşeyden → gerçek 85° yükseliş.
- **Ders:** OpenRocket'ın birim/konvansiyonunu **çalışan jar'a karşı** doğrula.
  Dokümantasyon ile kod aynı şeyi söylemeyebilir. Her fiziksel parametreyi
  tek bir test koşusuyla doğrula.

### 1.2 Paraşütler burnout'ta açılıyordu
- **Hata:** Üç paraşüt de `deployevent=ejection` idi. Motorun ejeksiyon gecikmesi 0
  olduğu için paraşütler burnout'ta (355 m/s) açılıyor ve apogee'yi 796 m'de
  kesiyordu.
- **Düzeltme:** Doğru olaylar: birincil `APOGEE` (0 s), ikincil `ALTITUDE` 500 m,
  görev yükü `APOGEE` +1.0 s.
- **Ders:** `EJECTION` bir **zaman noktası** (motor gecikmesi), `APOGEE`/`ALTITUDE`
  bir **olay**'dır. Bu ikisi asla birbirinin yerine kullanılmamalı. Motor gecikmesi
  0 ise `EJECTION` = burnout anıdır.

### 1.3 Malzeme gerçeği keşfedilmedi
- **Hata:** Mevcut `.ork`'taki "carbon/fiberglass/G10" adlı bileşenlerin malzemesi
  gerçekte **karton** (680 kg/m³) idi. Gerçek malzeme kütleyi ~1.1 kg artırdı.
- **Ders:** Bileşen adı ile malzeme aynı şey değildir. Her bileşenin `getMaterial()`
  ile yoğunluğu kontrol edilmeli. "Ad" kozmetiktir, "yoğunluk" fiziktir.

### 1.4 Motor yeniden yükleme kaybı
- **Hata:** OpenRocket 24.12 `.ork` içine thrust curve **gömmüyor**. Motor, kullanıcı
  motor dizinindeki eğriyle digest eşleşmesiyle bulunur. Bu dizin boşken `.ork`
  dosyaları motoru kaybediyordu.
- **Düzeltme:** `.eng` dosyaları `~/.openrocket/ThrustCurves/` altına kuruldu.
- **Ders:** Kaydet → yeniden yükle → motor var mı kontrol et. Bu test her tasarım
  değişikliğinden sonra yapılmalı.

### 1.5 Bileşke iniş hızı yanıltıcı
- **Hata:** Tek gövdede üç paraşüt aynı anda açılırsa bileşke iniş hızı hesaplanır;
  bu, faz bazlı hızları (4.2.6/4.2.7/4.2.8) doğrulamaz.
- **Düzeltme:** Her faz **ayrı koşu** ile ölçülmeli (yalnız birinci paraşüt açık /
  iki paraşüt açık / ayrı payload podu).
- **Ders:** Şartname maddeleri faz bazlıdır; bileşke hız hiçbir maddeyi doğrulamaz.

### 1.6 Tek gövdeli modelde payload ayrılması
- **Hata:** Payload çıkınca gövde statik olarak kararsızlaşıyor (CP−CG = −0.056 m)
  ve sayısal ayrışma oluşuyor.
- **Düzeltme:** İki kademeli model (üst+alt gövde + alüminyum entegrasyon gövdesi
  + ayırma sistemi) ile payload'ın bağımsız kurtarılması modellenebilir.
- **Ders:** 4.2.3/4.3.3 maddelerini geçmek için **iki kademeli model** şart.
  Tek gövdeli modelde bu maddeler "MODELLENMEDİ" olarak işaretlenmeli.

### 1.7 Aşırı stabilite (weathercocking)
- **Hata:** Burnout stabilitesi 4.71–4.75 cal (aşırı stabil). Bu, rüzgârda
  weathercocking riski taşır.
- **Düzeltme:** Kanat süpürme açısını azalt (70→59°), kanat boyutlarını küçült.
  Burnout stabilitesi 3.83–3.98 cal'a indirildi.
- **Ders:** Burnout stabilitesi 2.5–3.5 cal arasında tutulmalı. Şartname 4.4.5
  yalnızca 0.3 Mach'ta (1.5–2.5 cal) stabilite ister ama iyi bir tasarımda
  burnout da 2.5–3.5 cal'da olmalı.

### 1.8 0.3 Mach stabilitesi marjı çok dar
- **Hata:** 0.3 Mach stabilitesi 1.503 cal ile 1.5 kal alt sınırına çok yakın.
  Herhangi bir ölçüm belirsizliği veya simülasyon sapması alt sınırın altına
  düşürebilir.
- **Düzeltme:** Kanat kök kordonunu büyüt (150→160 mm), kanat yüksekliğini artır
  (63→64.5 mm). 0.3 Mach stabilitesi 1.727 cal'a çıkarıldı.
- **Ders:** 0.3 Mach stabilitesi **en az 1.65–1.7 cal** hedeflenmeli. 1.5 cal
  sınırına çok yakın değerler kabul edilmemeli.

### 1.9 Launch stabilitesi < 1.5 cal
- **Hata:** Kalkış stabilitesi 1.261–1.610 cal. Örneklerde 0.72–0.74 cal
  (`stability-min-low` uyarısı). Bizim tasarımımız daha iyi ama ideal olarak
  kalkış stabilitesi de ≥1.5 cal olmalı.
- **Ders:** Kalkış stabilitesi ≥1.5 cal hedeflenmeli. Ballast veya kanat
  geometrisi ile sağlanmalı.

---

## 2. ÖĞRENİLEN DERSLER (tasarım prensipleri)

### 2.1 Kütle–sürükleme ticareti
- Aynı motorla (M1850), daha hafif ve daha kalın gövdeli bir roket (14.49 kg,
  Ø117 mm) ile daha ağır ve daha ince gövdeli bir roket (17.86 kg, Ø98 mm)
  **neredeyse aynı irtifaya** ulaşıyor (~5.8 km).
- Kütle kazanımı, çap kaybını telafi ediyor. Bu, roket tasarımının klasik
  trade-off'udur.
- **Ders:** Apogee'yi optimize ederken yalnızca kütleyi değil, sürükleme alanını
  da birlikte optimize et. Tek taraflı optimizasyon yanıltıcıdır.

### 2.2 Burnout kütlesi apogee'yi belirler
- Apogee'yi belirleyen kalkıştaki kütle değil **burnout kütlesi** ve **sürükleme**.
- Burnout kütlesi 3.4 kg daha hafif olmamıza rağmen apogee yalnız 30 m daha
  yüksek: çünkü daha kalın gövdeli ve daha uzun burunlu.
- **Ders:** Kütle optimizasyonu burnout kütlesine odaklanmalı. Yakıt kütlesi
  (4.103 kg) sabit olduğundan, hava çerçevesi kütlesini azaltmak burnout
  kütlesini doğrudan azaltır.

### 2.3 Burun fineness ratio (L/D)
- Mach 1.3–1.4 rejimi için L/D 4.0–4.5 optimal.
- L/D 4.0 → ogive, 468 mm, 0.2639 kg.
- L/D 4.5 → Haack, 441 mm, 0.3095 kg (biraz daha ağır ama daha iyi aerodinamik).
- L/D 5.0 → yalnız +5.5 m apogee, +22 g kütle (değmez).
- **Ders:** Burun L/D'yi 4.0–4.5 aralığında tut. Daha uzun burun (L/D > 5)
  marginal kazanım verir, kütle ve yapısal sorunlar ekler.

### 2.4 Kanat planformu (süpürme ve uç kordonu)
- Çetin 06: 70° süpürme, uç kordonu gövde sonundan 47 mm taşıyordu (geçersiz
  planform). 57° süpürme ile 12 mm pay.
- **Ders:** Kanat süpürme açısı ve uç kordonu, gövde sonundan taşıma (overhang)
  kontrol edilmeli. Geçersiz planform aerodinamik hesapları bozar.

### 2.5 Yanma sırasında kütle değişimi
- Yanma sırasında CG 189 mm öne kayıyor; stabilite 1.522 → 4.347 cal.
- Kalkış stabilitesi ve burnout stabilitesi ayrı raporlanmalı.
- **Ders:** `stability_at_launch_cal` ve `stability_at_burnout_cal` ayrı ayrı
  kontrol edilmeli. Min powered stabilite (kalkış stabilitesi) ≥ 1.0 cal
  (ideally ≥ 1.5 cal).

### 2.6 Paraşüt paketleme
- 1.70 m ana paraşütün paketi ~0.30 m yer ister. Gövde ~0.2–0.3 m uzatılmalı
  (~+0.2 kg, apogee ~−60 m).
- **Ders:** Paraşüt çapı büyüdükçe paketleme hacmi artar. Gövde uzunluğu
  paraşüt paketleme hacmini hesaba katmalı.

### 2.7 Aviyonik kütlesi
- 2 UKB + GPS + batarya + kablolama ≈ 0.5–1.0 kg.
- Özgün UKB 0.30–0.38 kg, Ticari UKB 0.12 kg, hakem altimetresi 0.01–0.026 kg.
- **Ders:** Aviyonik kütlesi gerçekçi olmalı (1.5–2.5 kg şartname gereksinimi).
  Çok hafif model (0.5 kg) güvenilmez; çok ağır (2.5 kg) performansı düşürür.

### 2.8 İki kademeli vs tek kademeli
- İki kademeli: payload'ın bağımsız kurtarılması (4.2.3, 4.3.3) modelde temsil
  edilebilir. Ama alüminyum entegrasyon gövdesi (0.658 kg) ekstra kütle ekler.
- Tek kademeli: daha hafif (entegrasyon gövdesi yok) ama payload ayrılması
  modellenemez.
- **Ders:** İki kademeli çözüm şartname uyumu için gerekli ama kütle bedeli var.
  Tek kademeli çözüm daha hafif ama şartname uyumu eksik.

### 2.9 Malzeme seçimi
- Gövde: fiberglas 1850 kg/m³ (2.0 mm) vs karbon 1550 kg/m³ (1.5 mm).
  Karbon daha hafif ama daha pahalı.
- Kanat: alüminyum 2700 kg/m³ (3 mm) vs G10 1900 kg/m³ (3 mm).
  G10 daha hafif ama daha az sert (flutter direnci daha düşük).
- Burun: karbon 1550 kg/m³ (2.0 mm).
- **Ders:** Malzeme seçimi kütle, maliyet ve yapısal dayanım arasında trade-off.
  Karbon en hafif ama en pahalı; alüminyum en sert ama en ağır.

### 2.10 Motor seçimi
- Motor kategoriyle sabit: A1→L1256WS (3650 N·s, 2.967 s), A2/A4→M1850 (7524 N·s,
  6.75 s), A3→N3300 (14324 N·s, 4.613 s).
- Takım motor seçemez. Optimizasyon, verilen motor içinde yapılmalı.
- **Ders:** Motor seçimi yapılamaz; tasarım, verilen motorun itki eğrisine
  uygun olmalı.

---

## 3. ŞARTNAME MADDELERİ VE MODELLENEBİLİRLİK

### 3.1 OpenRocket'ta modellenebilen maddeler
- 4.4.2 (sabit dış çap) ✅
- 4.4.5 (0.3 Mach stabilite 1.5–2.5 cal) ✅ (zaman serisinden)
- 4.4.8 (rampa çıkış ≥ 25 m/s) ✅
- 4.3.2 (payload ≥ 4.0 kg) ✅ (MassComponent)
- 4.5.5 (malzeme) ✅ (set_component_material)
- 4.5.11 (burun omuzluğu ≥ 1.5×) ✅ (set_nose_shoulder)
- 4.5.15 (≥ 2 ray butonu) ✅ (RailButton bileşeni)
- 4.1.35 (85° yükseliş) ✅ (rod_angle=85)
- 4.2.6/4.2.7/4.2.8 (paraşüt iniş hızları) ✅ (faz bazlı koşu)

### 3.2 OpenRocket'ta modellenemeyen maddeler
- 4.2.16 (renk) — modelde yok
- 4.2.18 (shear pin) — modelde yok
- 4.5.2 (3× 3.0–4.5 mm delik) — `Hole` bileşeni var ama hiçbir örnekte kullanılmamış
- 4.5.9 (mapalar döküm çelik) — kütle olarak modellendi
- 4.5.16/4.5.19 (ray butonu konumu) — konum doğrulanmadı
- 4.6.2 (iki UKB) — aviyonik kütlesi olarak modellendi
- 4.3.3 (payload kolay ayrılabilir) — modelde ayrılma mekanizması yok
- 4.2.3 (payload bağımsız kurtarma) — modelde ayrılma mekanizması yok
- 4.5.12 (entegrasyon gövdesi ≥ %75) — modelde TubeCoupler var ama %75 şartı doğrulanmadı
- 4.1.33 ("PAYLOAD" adı) — örneklerde "Payload" kullanılmış, şartname "PAYLOAD" diyor

### 3.3 Şartname madde eşlemesi (paraşüt olayları)
- 4.1.7 → `APOGEE` + delay ≤ 2 s
- 4.1.8 → `ALTITUDE` 500 m (400–600 m bandı)
- 4.2.6 → `APOGEE` (0 s), 9–20 m/s
- 4.2.7 → `ALTITUDE`, 5–9 m/s
- 4.2.8 → payload'ın kendi paraşütü, 9–20 m/s

---

## 4. ARAÇLAR VE YÖNTEMLER

### 4.1 rocketlib fonksiyonları (yeni eklenenler)
- `set_component_material(doc, ad, material_name=..., density=...)` — hacimsel malzeme
- `set_surface_finish(doc, ad, "polished"/"optimum"/...)` — yüzey kaplaması
- `set_parachute_deployment(doc, ad, event=..., altitude=..., delay=...)` — paraşüt olayı
- `set_nose_shoulder(doc, ad, length=...)` — burun omuzluğu
- `set_component_position(doc, ad, method="absolute", offset=...)` — mutlak konum
- `set_motor_ignition(doc, event=..., delay=...)` — motor ateşleme
- `add_stage(doc, "Booster")` — yeni kademe
- `move_component(doc, ad, hedef_ad)` — bileşen taşıma

### 4.2 Simülasyon koşulları
- Seed: 1 (deterministik)
- Rüzgâr: 0 m/s (süreçler arası tekrarlanabilirlik)
- Fırlatma irtifası: 1000 m (Aksaray)
- Rampa: 6 m, 85° yükseliş
- Türbülans: 0

### 4.3 Doğrulama komutları
- `PYTHONPATH=. .venv/bin/python scratch/<script>.py` — simülasyon koşusu
- `.venv/bin/python -m pytest -q` — testler (48–53 passed)
- `rocketlib.validate(doc, seed=1)` — tasarım doğrulaması (0 sorun olmalı)

### 4.4 Motor eğrileri
- L1256WS: 3650 N·s, 2.967 s, 1470 N tepe, 1.905 kg yakıt, 3.905 kg toplam
- M1850: 7524 N·s, 6.75 s, 2411 N tepe, 4.103 kg yakıt, 7.010 kg toplam
- N3300: 14324 N·s, 4.613 s, 3776 N tepe, 7.668 kg yakıt, 12.645 kg toplam

---

## 5. TASARIM SONUÇLARI (özet)

| Tasarım | Motor | Kütle (kg) | Apogee (m) | Max Mach | 0.3 Mach stab. (cal) | Burnout stab. (cal) | Rampa çıkışı (m/s) |
|---|---|---|---|---|---|---|---|
| Çetin 06 (örnek) | M1850 | 17.857 | 5827.8 | 1.141 | 1.785 | 4.71 | 36.43 |
| 2027 A2_1 (örnek) | M1850 | 17.879 | 5815.2 | 1.140 | 1.749 | 4.75 | 36.38 |
| İlk tasarım (karton) | M1850 | 13.861 | 5282.8 | 1.355 | 1.818 | 2.857 | 42.69 |
| İlk tasarım (karbon) | M1850 | 14.968 | 5085.1 | 1.261 | 1.812 | 2.614 | 40.42 |
| Detaylı tasarım (Çetin 06 tabanlı) | M1850 | 17.401 | 5948.0 | 1.176 | 1.889 | 4.815 | 37.49 |
| **Optimize tasarım (beam)** | M1850 | **16.201** | **6305.6** | **1.264** | **1.727** | **3.984** | **38.23** |
| Alternatif (evren) | M1850 | 16.054 | 6051.1 | 1.263 | 1.769 | 4.347 | 38.62 |

**Hedef:** Apogee 4930–6670 m (5800 ± %15), 0.3 Mach stabilite 1.5–2.5 cal,
rampa çıkışı ≥ 25 m/s. Tüm tasarımlar hedef bandında; optimize tasarım en
yüksek irtifaya ulaşıyor (6305.6 m).

---

## 6. GELİŞTİRME PRENSİPLERİ (sürekli güncellenir)

1. **Her tasarım değişikliğinden sonra `validate()` çalıştır.** Özellikle motor
   ataması, bileşen ekleme/silme ve konum değişikliklerinden sonra.
2. **Her sayı gerçek bir simülasyon çıktısından gelmeli.** "Muhtemelen", "olmalı"
   gibi tahminler rapora giremez.
3. **Tüm testler geçmeden kütüphaneyi değişilmiş bırakma.** `pytest -q` temiz
   olmadan commit atma.
4. **Birimler SI; açılar derece.** Kütüphaneye yeni fonksiyon eklerken docstring'e
   birimleri yaz.
5. **Bileşen adları benzersiz.** Ad verilmezse kütüphane otomatik benzersiz ad
   üretir.
6. **Hataları yutma.** Geçersiz girdide `RocketLibError` türevi fırlat.
7. **Java sürümü/jar uyumu:** API'yi çalışan jar'a karşı doğrula.
8. **Motor eğrileri:** yeni motor eğrisi kullanılacaksa **önce**
   `~/.openrocket/ThrustCurves/` dizinine kopyalanmalı.
9. **Rampa açısı:** her zaman yataydan yükseliş olarak ver; kütüphane dönüşümü
   yapar.
10. **Paraşüt olayları:** `EJECTION` yerine `APOGEE`/`ALTITUDE` kullan.
11. **Malzeme kontrolü:** her bileşenin `getMaterial()` ile yoğunluğu kontrol et.
12. **Kütle tabanı:** motor + payload zorunlu tabanı; 10.5–11.5 kg bandı
    ulaşılamaz (M1850 + 4 kg payload = 11.010 kg).
13. **Stabilite marjı:** 0.3 Mach stabilitesi en az 1.65–1.7 cal hedeflenmeli.
    Burnout stabilitesi 2.5–3.5 cal arasında tutulmalı.
14. **İki kademeli çözüm:** payload'ın bağımsız kurtarılması için iki kademeli
    model gerekli.
15. **Paraşüt paketleme:** paraşüt çapı büyüdükçe paketleme hacmi artar; gövde
    uzunluğu buna göre seçilmeli.

---

---

## 7. SON OPTİMİZASYON ROUND'UNDAN ÖĞRENİLENLER (opt2)

### 7.1 Kanat malzemesi Al→G10: kütle azalır, apogee artar
- Alüminyum 2700 kg/m³ → G10 1900 kg/m³. Kanat kütlesi 0.1835→0.130 kg (-0.053 kg).
- Apogee +57 m (6258→6315 m). Flutter riski artar ama 3 mm G10 98 mm gövdede yeterli.
- **Ders:** Kanat malzemesi G10, alüminyumdan %30 daha hafif. Flutter kontrolü ayrıca yapılmalı.

### 7.2 Burun HAACK→ogive: apogee 150 m düşer
- HAACK (L/D 4.0) → ogive denemesi apogee'yi 150 m düşürdü. HAACK korundu.
- **Ders:** HAACK burun, ogive'den aerodinamik olarak daha iyi. Değiştirme.

### 7.3 Kanat süpürme 45° denemesi: apogee 24 m düşer
- 59° → 45° süpürme apogee'yi 24 m düşürdü. 50° korundu.
- **Ders:** Kanat süpürme açısı apogee'ye etkili. 50° optimum (59° → 50° +37 m, 50° → 45° -24 m).

### 7.4 Kanat kök kordonu 150→157.5 mm: stabilite artar, apogee hafif düşer
- Kök kordon artışı stabiliteyi artırır (+0.05 cal) ama drag de artar (-15 m apogee).
- **Ders:** Kanat boyutu ile stabilite–drag arasında trade-off. Min powered stabilite ≥1.5 için kanat yeterli büyüklükte olmalı.

### 7.5 Aviyonik 0.52→0.45 kg: kütle azalır
- Özgün UKB 0.38→0.31 kg. Toplam aviyonik 0.52→0.45 kg (-0.07 kg).
- **Ders:** Aviyonik kütlesi optimize edilebilir ama gerçekçi olmalı (2 UKB + GPS + batarya).

### 7.6 Paraşüt ip kısaltma: kütle azalır, iniş hızı artar
- Paraşüt ip boyları 1.50→1.20 m (-0.03 kg). İniş hızı 8.05→8.00 m/s (band içinde).
- **Ders:** Paraşüt ip boyu kısaltılabilir ama iniş hızı bandı (5–9 m/s) korunmalı.

### 7.7 Min powered stabilite 1.650→1.521 cal
- Kanat optimizasyonu (G10, kök 157.5, yükseklik 64.4, süpürme 50°) min powered
  stabiliteyi 1.650→1.521 cal'a düşürdü. Hâlâ ≥1.5 (geçer) ama marj daraldı.
- **Ders:** Kütle ve drag optimizasyonu stabilite marjını daraltabilir. Her
  optimizasyon adımında stabilite kontrol edilmeli.

### 7.8 Burnout stabilitesi 3.984→3.880 cal
- Kanat optimizasyonu burnout stabilitesini 3.984→3.880 cal'a düşürdü (daha iyi).
- **Ders:** Kanat boyutu azaldıkça burnout stabilitesi de azalır (daha az aşırı stabil).

### 7.9 Genel prensip: optimizasyon döngüsü
- Her iterasyonda: apogee, kütle, 0.3 Mach stab., min powered stab., burnout stab.,
  rampa çıkışı, descent hızı ölçülmeli.
- Tüm hedefler aynı anda karşılanmalı: apogee ≥6250, kütle ≤16.25, 0.3 Mach 1.7–1.9,
  min powered ≥1.5, burnout ≤4.0, rampa ≥38, descent 8–9.
- Bir hedef iyileşirken diğer bozulabilir (trade-off). En iyi kompromis seçilmeli.

---

## 8. STABİLİTE DÜZELTME ROUND'UNDAN ÖĞRENİLENLER (stab4)

### 8.1 Min powered stabiliteyi artırmak için birden fazla küçük değişiklik gerekir
- Tek bir değişiklik (ballast 50 g veya kanat süpürme 50→47°) min powered
  stabiliteyi 0.05–0.10 cal artırdı. 1.521→1.650 cal için 6 farklı değişiklik
  (kanat kök 157.5→160, yükseklik 64.4→65.39, süpürme 50→47.5°, aviyonik
  0.45 kg, gövde ballast 26 g, paraşüt ip kısaltma) birlikte uygulandı.
- **Ders:** Stabilite marjı küçük değişikliklerin toplamıyla artar. Her değişiklik
  tek başına yetersiz olabilir; birlikte uygulanmalı.

### 8.2 Stabilite–apogee trade-off
- Min powered stabiliteyi 1.521→1.650 cal'a çıkarmak apogee'yi 6315.1→6288.8 m
  düşürdü (-26.3 m). Kanat boyutu artışı drag ve kütle ekledi.
- **Ders:** Stabilite marjı arttıkça apogee düşer. Her iki metriği birlikte
  optimize et; tek taraflı optimizasyon yanıltıcıdır.

### 8.3 Burnout stabilitesi artışı
- Min powered stabiliteyi artırmak burnout stabilitesini de artırdı (3.880→4.003 cal).
  Burnout stabilitesi 4.0 cal sınırına yaklaştı.
- **Ders:** Stabilite marjı arttıkça burnout stabilitesi de artar. Burnout
  stabilitesi 4.0 cal sınırını aşmamalı; aşarsa kanat boyutu azaltılmalı.

### 8.4 Ballast etkisi
- 26 g burun ballastı min powered stabiliteyi +0.03 cal artırdı.
- **Ders:** Ballast, stabiliteyi artırmak için en etkili yöntemdir (kütle
  artışı küçük, stabilite kazanımı büyük). Ama kütle artışı apogee'yi düşürür.

### 8.5 Kanat süpürme açısı etkisi
- 50→47.5° süpürme açısı min powered stabiliteyi +0.05 cal artırdı.
- 50→45° süpürme açısı apogee'yi 24 m düşürdü → 47.5° optimum.
- **Ders:** Kanat süpürme açısı küçük değişikliklerle stabiliteyi ayarlamak
  için kullanılabilir. 45° altına inmemeli (apogee kaybı).

### 8.6 Genel prensip: stabilite marjı ≥ 1.65 cal
- 0.3 Mach stabilitesi en az 1.65 cal hedeflenmeli. 1.5 cal sınırına çok yakın
  değerler (1.50–1.55) kabul edilmemeli.
- Min powered stabilite de en az 1.5 cal (tercihen 1.65 cal) olmalı.
- Burnout stabilitesi 3.5–4.0 cal arasında tutulmalı.

---

## 9. ALTERNATİF MİMARİ ROUND'UNDAN ÖĞRENİLENLER (evren2)

### 9.1 Tek kademe + geniş çap = daha düşük irtifa
- Tek kademe, Ø117 mm karbon gövde (1.5 mm), G10 kanat (3 mm), ogive burun
  (L/D 4.0) → apogee 6222.5 m. İki kademeli + Ø98 mm tasarımlar (6288.8 m)
  ile karşılaştırıldığında **66.3 m daha düşük**.
- Neden: Ø117 mm gövde → Ø98 mm'ye göre %42 daha fazla frontal alan → sürükleme
  artışı. Tek kademe → payload'ın bağımsız kurtarılması modellenemez.
- **Ders:** Tek kademe + geniş çap mimarisi, M1850 motorla hedef irtifaya
  (6200+ m) ulaşabilir ama iki kademeli + ince çap mimarisinden daha düşük
  irtifa verir. Sürükleme alanının etkisi kütle etkisinden daha baskın.

### 9.2 Karbon gövde + G10 kanat: hafif ama stabilite düşük
- Karbon gövde 1.5 mm (1550 kg/m³) + G10 kanat 3 mm (1900 kg/m³) → kütle
  14.550 kg (en hafif tasarım). Ama 0.3 Mach stabilite 1.391 cal (1.5 altında).
- **Ders:** Hafif gövde + hafif kanat = düşük stabilite. Stabiliteyi artırmak
  için kanat boyutu veya burun kütlesi artırılmalı; bu da kütle ve drag ekler.

### 9.3 Tek kademeli tasarımın avantajları
- Entegrasyon gövdesi (TubeCoupler) yok → kütle tasarrufu (~0.38 kg).
- Aviyonik kütlesi daha hafif (0.786 kg vs 0.45 kg — aslında daha ağır).
- Yapısal detay daha az (merkezleme halkası, bulkhead sayısı daha az).
- **Ders:** Tek kademeli tasarım daha basit ve hafif ama şartname uyumu eksik
  (payload ayrılması modelde gösterilemez).

### 9.4 Ø117 mm vs Ø98 mm: sürükleme farkı
- Ø117 mm → frontal alan 0.01075 m². Ø98 mm → 0.00754 m². %42 daha fazla
  sürükleme alanı. Bu fark, tek kademeli tasarımın 6222.5 m'de kalmasına neden
  oldu.
- **Ders:** Gövde çapı, apogee'yi belirleyen en önemli faktörlerden biri.
  Çap arttıkça sürükleme artar, apogee düşer. Ø98 mm optimal.

### 9.5 Genel prensip: mimari seçimi
- İki kademeli + ince çap (Ø98 mm) → daha yüksek irtifa (6288.8 m) + şartname
  uyumu (4.2.3, 4.3.3, 4.5.12).
- Tek kademeli + geniş çap (Ø117 mm) → daha düşük irtifa (6222.5 m) + şartname
  uyumu eksik (payload ayrılması modelde gösterilemez).
- **Ders:** İki kademeli mimari, M1850 motorla hedef irtifaya ulaşmak için en
  iyi mimaridir. Tek kademeli mimari daha basit ama performans ve uyum açısından
  geride kalır.

*Bu dosya her yeni iterasyonda güncellenmelidir. Öğrenilen her yeni ders
buraya eklenmelidir.*
