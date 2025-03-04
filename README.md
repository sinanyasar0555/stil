# Stil Analiz Uygulaması

Modern ve kullanıcı dostu bir arayüze sahip, yapay zeka destekli kıyafet ve stil analiz uygulaması.

## Özellikler

### 1. Görsel Analiz
- BLIP (Salesforce/blip-image-captioning-large) modeli ile otomatik görsel analizi
- Detaylı kıyafet ve stil tanımlama
- Akıllı renk ve desen tespiti

### 2. Stil Değerlendirmesi
- GPT-3.5 ile profesyonel stil analizi
- Otomatik puanlama sistemi (4 kategori):
  - Tarz Değerlendirmesi
  - Renk Analizi
  - Uyum Değerlendirmesi
  - Genel Etki
- Yıldız bazlı puanlama gösterimi (1-5 arası)

### 3. Detaylı Rapor
- Kategori bazlı detaylı değerlendirmeler
- Güçlü yönlerin analizi
- Kişiselleştirilmiş stil önerileri
- Geliştirme tavsiyeleri

### 4. Modern Arayüz
- Şık ve kullanıcı dostu tasarım
- Koyu tema
- Kaydırılabilir sonuç alanı
- Sezgisel kontroller

### 5. Kaydetme ve Raporlama
- Otomatik tarih-saat etiketli raporlar
- TXT formatında detaylı analiz kaydetme
- Puanlar ve yıldızların dahil olduğu kapsamlı raporlar

## Kurulum

1. Gerekli Python paketlerini yükleyin:
```bash
pip install pillow transformers torch requests
```

2. OpenAI API anahtarınızı ayarlayın:
- Proje klasöründe `ayarlar.json` dosyası oluşturun
- API anahtarınızı aşağıdaki formatta ekleyin:
```json
{
    "api_key": "sizin-api-anahtariniz"
}
```

3. Uygulamayı başlatın:
```bash
python moda_analiz.py
```

## Kullanım

1. "Fotoğraf Seç" butonu ile analiz edilecek görseli seçin
2. "Analiz Et" butonuna tıklayarak yapay zeka analizini başlatın
3. Sonuçları inceleyin:
   - Otomatik puanlamalar
   - Detaylı stil analizi
   - Öneriler ve tavsiyeler
4. "Sonucu Kaydet" butonu ile analizi TXT formatında saklayın

## Teknik Detaylar

- **Görsel Analiz**: BLIP image-to-text modeli
- **Stil Analizi**: GPT-3.5-turbo
- **Arayüz**: Tkinter ile modern UI
- **Dil**: Python 3.x
- **Encoding**: UTF-8 (Türkçe karakter desteği)

## Klasör Yapısı

```
.
├── moda_analiz.py    # Ana uygulama dosyası
├── ayarlar.json      # API ayarları
├── analizler/        # Kaydedilen raporlar
└── README.md         # Dokümantasyon
```

## Gereksinimler

- Python 3.x
- PIL (Pillow)
- Transformers
- Torch
- Requests
- OpenAI API anahtarı

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. 

---

<div align="center">
    <p>Developed with ❄️ by</p>
    <h2>AKBUZ DEVELOPER</h2>
    <p>Yapay Zeka & Yazılım Çözümleri</p>
    <p>© 2024 Tüm hakları saklıdır.</p>
</div> 