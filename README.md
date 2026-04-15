# 🎓 Student Grade System
SQLite veritabanlı, modüler yapıda bir öğrenci not yönetim sistemi.
## 📂 Proje Yapısı
```
not_sistemi/
├── veritabani.py   → Veritabanı bağlantı katmanı
├── modeller.py     → Veri modelleri
├── yonetici.py     → İş mantığı katmanı
├── uygulama.py     → Ana uygulama (giriş noktası)
├── README.md
└── .gitignore
```
## 🚀 Kurulum ve Çalıştırma
```bash
git clone https://github.com/KULLANICI_ADIN/student-grade-system.git
cd student-grade-system
python uygulama.py
```
> Harici kütüphane gerektirmez. Python 3.10+ yeterlidir.
## 📋 Özellikler
- Öğrenci ekleme, listeleme, arama ve silme
- Ders ekleme ve listeleme
- Not girişi ve güncelleme
- Karne görüntüleme (harf notu + GPA hesaplama)
- Sınıf istatistikleri (ortalama, en yüksek/düşük, geçme oranı, ders bazlı)
- Otomatik log dosyası
## 🔧 Kullanılan Teknik Kavramlar
| Kavram | Dosya |
|--------|-------|
| Context Manager (`__enter__` / `__exit__`) | `veritabani.py` |
| Dataclass, Property, `__post_init__` | `modeller.py` |
| `@staticmethod` | `modeller.py` |
| Custom Decorator (`@loglama`, `@sure_olc`) | `yonetici.py` |
| Generator (`yield`) | `yonetici.py` |
| Custom Exception | `yonetici.py` |
| Type Hints | Tümü |
| List Comprehension | `yonetici.py` |
| Logging | `yonetici.py` |
| SQLite (JOIN, GROUP BY, Foreign Key) | `veritabani.py` |
## 🗃️ Veritabanı Şeması
```
ogrenciler          dersler             notlar
├── id              ├── id              ├── id
├── ad              ├── ders_adi        ├── ogrenci_id (FK)
├── soyad           └── kredi           ├── ders_id (FK)
├── numara                              ├── vize
└── kayit_tarihi                        └── final
```
## 📊 Harf Notu Tablosu
| Ortalama | Harf | Katsayı |
|----------|------|---------|
| 90-100   | AA   | 4.0     |
| 85-89    | BA   | 3.5     |
| 80-84    | BB   | 3.0     |
| 75-79    | CB   | 2.5     |
| 70-74    | CC   | 2.0     |
| 65-69    | DC   | 1.5     |
| 60-64    | DD   | 1.0     |
| 50-59    | FD   | 0.5     |
| 0-49     | FF   | 0.0     |
> Ortalama = Vize × %40 + Final × %60
