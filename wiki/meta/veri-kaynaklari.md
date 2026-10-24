---
type: meta
title: "Veri Kaynakları"
status: active
created: 2026-10-22
updated: 2026-10-22
tags: [wiki, meta, veri]
---

# Veri Kaynakları

| Dosya | İçerik | Üretici |
|---|---|---|
| `örnek-roket/*.ork` (8 dosya) | ham yarışma tasarımları (değiştirilmez) | takımlar / OpenRocket |
| `örnek-roket/parsed.json` | çözümlenmiş veri + gerçek simülasyon sonuçları | `scratch/parse_ornek.py` |
| `scratch/sartname.txt` | TEKNOFEST 2026 teknik şartname metni (v1.9) | `pdftotext -layout şartname.pdf` |
| `şartname.pdf` | şartnamenin aslı | TEKNOFEST |
| `designs/m1850-teknofest/rocket.ork` | bu projenin nihai M1850 tasarımı | `designs/m1850_build.py` |
| `designs/m1850-teknofest/FINAL_REPORT.md` | nihai tasarım raporu (kütle bütçesi + 24 maddelik uyum matrisi) | subagent + doğrulama |
| `designs/m1850-teknofest/simulation-results.json` | nihai tasarımın simülasyon özeti | aynı |
| `designs/m1850-teknofest/CORRECTED_BASELINE.md` | iki kritik hatanın (rampa açısı, paraşüt olayı) düzeltme notu | bu oturum |
| `~/.openrocket/ThrustCurves/Teknofest26_{L1256,M1850,N3300}_Rev1.eng` | motor itki eğrileri | `Aerotech_Motorlarına_İlişkin_Teknik_Bilgiler_...zip` |
| `wiki/entities/motor-m1850.md`, `motor-l1256ws.md` | motor eğrilerinden türetilen entegre itki/tepe itki | `.eng` noktalarının trapezoidal integrali |

## Motor eğrileri neden `~/.openrocket/ThrustCurves/` altında?

OpenRocket 24.12, `.ork` dosyasının içine thrust curve **gömmez** (bu özellik
24.12'den sonra eklendi). Motor, kullanıcı motor dizinindeki eğri digest'iyle
eşleşerek bulunur. Bu dizin boşken `.ork` dosyaları motoru kaybediyordu.

## İlgili Sayfalar

[[parsing-methodology]] · [[index]]
