from veritabani import veritabani_olustur
from modeller import Ogrenci, Ders, Not
from yonetici import NotSistemi, KayitBulunamadiError, CiftKayitError

def giris_al(mesaj: str, tip: type = str, zorunlu: bool = True):
    while True:
        deger = input(f"  {mesaj}").strip()
        if not deger and not zorunlu:
            return None
        if not deger:
            print("  ! Bu alan zorunlu.")
            continue
        try:
            return tip(deger)
        except ValueError:
            print(f"  ! Geçerli bir {tip.__name__} girin.")
def ogrenci_ekle_menu(sistem: NotSistemi) -> None:
    print("\n  ── Öğrenci Ekle ──")
    try:
        ogrenci = Ogrenci(
            ad=giris_al("Ad: "),
            soyad=giris_al("Soyad: "),
            numara=giris_al("Numara: "),
        )
        yeni_id = sistem.ogrenci_ekle(ogrenci)
        print(f"  + {ogrenci.tam_ad} eklendi (ID: {yeni_id})")
    except (ValueError, CiftKayitError) as e:
        print(f"  ! Hata: {e}")
def ogrenci_listele_menu(sistem: NotSistemi) -> None:
    print("\n  ── Öğrenci Listesi ──")
    ogrenciler = sistem.ogrencileri_getir()
    if not ogrenciler:
        print("  Kayıtlı öğrenci yok.")
        return
    print(f"  {'ID':<4} {'Numara':<10} {'Ad Soyad':<25} {'Kayıt Tarihi'}")
    print("  " + "─" * 55)
    for o in ogrenciler:
        print(f"  {o.id:<4} {o.numara:<10} {o.tam_ad:<25} {o.kayit_tarihi}")
def ogrenci_ara_menu(sistem: NotSistemi) -> None:
    print("\n  ── Öğrenci Ara ──")
    arama = giris_al("Arama: ")
    bulunan = False
    for ogrenci in sistem.ogrenci_ara(arama):
        print(f"  → {ogrenci}")
        bulunan = True
    if not bulunan:
        print("  Sonuç bulunamadı.")
def ogrenci_sil_menu(sistem: NotSistemi) -> None:
    print("\n  ── Öğrenci Sil ──")
    ogrenci_listele_menu(sistem)
    try:
        oid = giris_al("Silinecek ID: ", int)
        sistem.ogrenci_sil(oid)
        print(f"  - ID={oid} silindi.")
    except (KayitBulunamadiError, ValueError) as e:
        print(f"  ! Hata: {e}")
def ders_ekle_menu(sistem: NotSistemi) -> None:
    print("\n  ── Ders Ekle ──")
    try:
        ders = Ders(
            ders_adi=giris_al("Ders adı: "),
            kredi=giris_al("Kredi: ", int),
        )
        yeni_id = sistem.ders_ekle(ders)
        print(f"  + {ders} eklendi (ID: {yeni_id})")
    except (ValueError, CiftKayitError) as e:
        print(f"  ! Hata: {e}")
def ders_listele_menu(sistem: NotSistemi) -> None:
    print("\n  ── Ders Listesi ──")
    dersler = sistem.dersleri_getir()
    if not dersler:
        print("  Kayıtlı ders yok.")
        return
    print(f"  {'ID':<4} {'Ders Adı':<20} {'Kredi'}")
    print("  " + "─" * 30)
    for d in dersler:
        print(f"  {d.id:<4} {d.ders_adi:<20} {d.kredi}")
def not_ekle_menu(sistem: NotSistemi) -> None:
    print("\n  ── Not Gir ──")
    ogrenci_listele_menu(sistem)
    ders_listele_menu(sistem)
    try:
        not_bilgisi = Not(
            ogrenci_id=giris_al("Öğrenci ID: ", int),
            ders_id=giris_al("Ders ID: ", int),
            vize=giris_al("Vize (0-100): ", float),
            final=giris_al("Final (0-100): ", float),
        )
        yeni_id = sistem.not_ekle(not_bilgisi)
        print(f"  + Not kaydedildi (ID: {yeni_id})")
        print(f"    {not_bilgisi}")
    except (ValueError, CiftKayitError) as e:
        print(f"  ! Hata: {e}")
def not_guncelle_menu(sistem: NotSistemi) -> None:
    print("\n  ── Not Güncelle ──")
    try:
        oid = giris_al("Öğrenci ID: ", int)
        did = giris_al("Ders ID: ", int)
        vize = giris_al("Yeni Vize (0-100): ", float)
        final = giris_al("Yeni Final (0-100): ", float)
        sistem.not_guncelle(oid, did, vize, final)
        print("  ✓ Not güncellendi.")
    except (KayitBulunamadiError, ValueError) as e:
        print(f"  ! Hata: {e}")
def karne_menu(sistem: NotSistemi) -> None:
    print("\n  ── Öğrenci Karnesi ──")
    ogrenci_listele_menu(sistem)
    try:
        oid = giris_al("Öğrenci ID: ", int)
        notlar = sistem.ogrenci_karnesi(oid)
        gpa = sistem.gpa_hesapla(oid)
        print(f"\n  Öğrenci: {notlar[0].ogrenci_adi}")
        print(f"  {'Ders':<20} {'Vize':>6} {'Final':>6} {'Ort':>6} {'Harf':>5} {'Durum':>8}")
        print("  " + "─" * 55)
        for n in notlar:
            durum = "Geçti" if n.gecti_mi else "Kaldı"
            print(f"  {n.ders_adi:<20} {n.vize:>6.0f} {n.final:>6.0f} "
                  f"{n.ortalama:>6.1f} {n.harf_notu:>5} {durum:>8}")
        print("  " + "─" * 55)
        print(f"  GPA: {gpa}/4.00")
    except (KayitBulunamadiError, ValueError) as e:
        print(f"  ! Hata: {e}")
def istatistik_menu(sistem: NotSistemi) -> None:
    print("\n  ── Sınıf İstatistikleri ──")
    ist = sistem.sinif_istatistikleri()
    if ist["toplam_not"] == 0:
        print("  Henüz not girişi yapılmamış.")
        return
    print(f"  Toplam not kaydı   : {ist['toplam_not']}")
    print(f"  Genel ortalama     : {ist['genel_ortalama']:.1f}")
    print(f"  En yüksek          : {ist['en_yuksek']:.1f}")
    print(f"  En düşük           : {ist['en_dusuk']:.1f}")
    print(f"  Geçen / Kalan      : {ist['gecen']} / {ist['kalan']}")
    if ist["ders_bazli"]:
        print(f"\n  {'Ders':<20} {'Ortalama':>8} {'Öğrenci':>8}")
        print("  " + "─" * 40)
        for d in ist["ders_bazli"]:
            print(f"  {d['ders']:<20} {d['ortalama']:>8.1f} {d['ogrenci']:>8}")
def menu():
    print("\n  ╔══════════════════════════════════╗")
    print("  ║    ÖĞRENCİ NOT SİSTEMİ          ║")
    print("  ╠══════════════════════════════════╣")
    print("  ║  1. Öğrenci ekle                 ║")
    print("  ║  2. Öğrenci listele              ║")
    print("  ║  3. Öğrenci ara                  ║")
    print("  ║  4. Öğrenci sil                  ║")
    print("  ║  5. Ders ekle                    ║")
    print("  ║  6. Ders listele                 ║")
    print("  ║  7. Not gir                      ║")
    print("  ║  8. Not güncelle                 ║")
    print("  ║  9. Karne görüntüle              ║")
    print("  ║ 10. Sınıf istatistikleri         ║")
    print("  ║  0. Çıkış                        ║")
    print("  ╚══════════════════════════════════╝")
def main():
    veritabani_olustur()
    sistem = NotSistemi()
    islemler = {
        "1": ogrenci_ekle_menu,
        "2": ogrenci_listele_menu,
        "3": ogrenci_ara_menu,
        "4": ogrenci_sil_menu,
        "5": ders_ekle_menu,
        "6": ders_listele_menu,
        "7": not_ekle_menu,
        "8": not_guncelle_menu,
        "9": karne_menu,
        "10": istatistik_menu,
    }
    print("\n  Öğrenci Not Sistemine hoş geldiniz.")
    while True:
        menu()
        secim = input("\n  Seçim: ").strip()
        if secim == "0":
            print("\n  Güle güle!\n")
            break
        elif secim in islemler:
            islemler[secim](sistem)
        else:
            print("  ! Geçersiz seçim.")
if __name__ == "__main__":
    main()