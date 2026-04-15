import functools
import time
import logging

from typing import Generator
from veritabani import VeritabaniBaglantisi
from modeller import Ogrenci, Ders, Not


logging.basicConfig(
    filename="not_sistemi.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)
class KayitBulunamadiError(Exception):
    pass
class CiftKayitError(Exception):
    pass
def loglama(fonksiyon):
    @functools.wraps(fonksiyon)
    def sarmalayici(*args, **kwargs):
        logger.info(f"ÇAĞRI: {fonksiyon.__name__}(args={args[1:]}, kwargs={kwargs})")
        try:
            sonuc = fonksiyon(*args, **kwargs)
            logger.info(f"BAŞARI: {fonksiyon.__name__} → {sonuc}")
            return sonuc
        except Exception as e:
            logger.error(f"HATA: {fonksiyon.__name__} → {type(e).__name__}: {e}")
            raise
    return sarmalayici
def sure_olc(fonksiyon):
    @functools.wraps(fonksiyon)
    def sarmalayici(*args, **kwargs):
        baslangic = time.perf_counter()
        sonuc = fonksiyon(*args, **kwargs)
        bitis = time.perf_counter()
        sure = (bitis - baslangic) * 1000
        logger.info(f"SÜRE: {fonksiyon.__name__} → {sure:.2f}ms")
        return sonuc
    return sarmalayici
class NotSistemi:
    def __init__(self, db_dosya: str = "okul.db") -> None:
        self._db = db_dosya
    @loglama
    def ogrenci_ekle(self, ogrenci: Ogrenci) -> int:
        with VeritabaniBaglantisi(self._db) as db:
            try:
                cursor = db.execute(
                    "INSERT INTO ogrenciler (ad, soyad, numara) VALUES (?, ?, ?)",
                    (ogrenci.ad, ogrenci.soyad, ogrenci.numara),
                )
                return cursor.lastrowid
            except Exception:
                raise CiftKayitError(f"'{ogrenci.numara}' numarası zaten kayıtlı.")
    @loglama
    def ogrenci_sil(self, ogrenci_id: int) -> None:
        with VeritabaniBaglantisi(self._db) as db:
            cursor = db.execute("DELETE FROM ogrenciler WHERE id = ?", (ogrenci_id,))
            if cursor.rowcount == 0:
                raise KayitBulunamadiError(f"ID={ogrenci_id} öğrenci bulunamadı.")
    @sure_olc
    def ogrencileri_getir(self) -> list[Ogrenci]:
        with VeritabaniBaglantisi(self._db) as db:
            satirlar = db.execute(
                "SELECT id, ad, soyad, numara, kayit_tarihi FROM ogrenciler ORDER BY soyad"
            ).fetchall()
            return [
                Ogrenci(
                    id=s["id"], ad=s["ad"], soyad=s["soyad"],
                    numara=s["numara"], kayit_tarihi=s["kayit_tarihi"]
                )
                for s in satirlar
            ]
    def ogrenci_ara(self, arama: str) -> Generator[Ogrenci, None, None]:
        with VeritabaniBaglantisi(self._db) as db:
            satirlar = db.execute(
                "SELECT id, ad, soyad, numara, kayit_tarihi FROM ogrenciler "
                "WHERE ad LIKE ? OR soyad LIKE ? OR numara LIKE ?",
                (f"%{arama}%", f"%{arama}%", f"%{arama}%"),
            ).fetchall()
            for s in satirlar:
                yield Ogrenci(
                    id=s["id"], ad=s["ad"], soyad=s["soyad"],
                    numara=s["numara"], kayit_tarihi=s["kayit_tarihi"]
                )
    @loglama
    def ders_ekle(self, ders: Ders) -> int:
        with VeritabaniBaglantisi(self._db) as db:
            try:
                cursor = db.execute(
                    "INSERT INTO dersler (ders_adi, kredi) VALUES (?, ?)",
                    (ders.ders_adi, ders.kredi),
                )
                return cursor.lastrowid
            except Exception:
                raise CiftKayitError(f"'{ders.ders_adi}' dersi zaten kayıtlı.")
    def dersleri_getir(self) -> list[Ders]:
        with VeritabaniBaglantisi(self._db) as db:
            satirlar = db.execute(
                "SELECT id, ders_adi, kredi FROM dersler ORDER BY ders_adi"
            ).fetchall()
            return [Ders(id=s["id"], ders_adi=s["ders_adi"], kredi=s["kredi"]) for s in satirlar]
    @loglama
    def not_ekle(self, not_bilgisi: Not) -> int:
        with VeritabaniBaglantisi(self._db) as db:
            try:
                cursor = db.execute(
                    "INSERT INTO notlar (ogrenci_id, ders_id, vize, final) VALUES (?, ?, ?, ?)",
                    (not_bilgisi.ogrenci_id, not_bilgisi.ders_id,
                     not_bilgisi.vize, not_bilgisi.final),
                )
                return cursor.lastrowid
            except Exception:
                raise CiftKayitError("Bu öğrencinin bu dersteki notu zaten girilmiş.")
    @loglama
    def not_guncelle(self, ogrenci_id: int, ders_id: int, vize: float, final: float) -> None:
        with VeritabaniBaglantisi(self._db) as db:
            cursor = db.execute(
                "UPDATE notlar SET vize = ?, final = ? WHERE ogrenci_id = ? AND ders_id = ?",
                (vize, final, ogrenci_id, ders_id),
            )
            if cursor.rowcount == 0:
                raise KayitBulunamadiError("Güncellenecek not kaydı bulunamadı.")
    @sure_olc
    def ogrenci_karnesi(self, ogrenci_id: int) -> list[Not]:
        with VeritabaniBaglantisi(self._db) as db:
            satirlar = db.execute("""
                SELECT n.id, n.ogrenci_id, n.ders_id, n.vize, n.final,
                       o.ad || ' ' || o.soyad AS ogrenci_adi,
                       d.ders_adi
                FROM notlar n
                JOIN ogrenciler o ON n.ogrenci_id = o.id
                JOIN dersler d    ON n.ders_id = d.id
                WHERE n.ogrenci_id = ?
                ORDER BY d.ders_adi
            """, (ogrenci_id,)).fetchall()
            if not satirlar:
                raise KayitBulunamadiError(f"ID={ogrenci_id} öğrencisine ait not bulunamadı.")
            return [
                Not(
                    id=s["id"], ogrenci_id=s["ogrenci_id"], ders_id=s["ders_id"],
                    vize=s["vize"], final=s["final"],
                    ogrenci_adi=s["ogrenci_adi"], ders_adi=s["ders_adi"],
                )
                for s in satirlar
            ]
    @sure_olc
    def sinif_istatistikleri(self) -> dict:
        with VeritabaniBaglantisi(self._db) as db:
            genel = db.execute("""
                SELECT
                    COUNT(*)                            AS toplam_not,
                    AVG(vize * 0.4 + final * 0.6)       AS genel_ortalama,
                    MAX(vize * 0.4 + final * 0.6)       AS en_yuksek,
                    MIN(vize * 0.4 + final * 0.6)       AS en_dusuk,
                    SUM(CASE WHEN (vize*0.4+final*0.6) >= 50 THEN 1 ELSE 0 END) AS gecen,
                    SUM(CASE WHEN (vize*0.4+final*0.6) < 50 THEN 1 ELSE 0 END)  AS kalan
                FROM notlar
            """).fetchone()
            ders_bazli = db.execute("""
                SELECT d.ders_adi,
                       AVG(n.vize * 0.4 + n.final * 0.6) AS ort,
                       COUNT(*)                            AS ogrenci_sayisi
                FROM notlar n
                JOIN dersler d ON n.ders_id = d.id
                GROUP BY d.ders_adi
                ORDER BY ort DESC
            """).fetchall()
            return {
                "toplam_not": genel["toplam_not"],
                "genel_ortalama": genel["genel_ortalama"] or 0,
                "en_yuksek": genel["en_yuksek"] or 0,
                "en_dusuk": genel["en_dusuk"] or 0,
                "gecen": genel["gecen"] or 0,
                "kalan": genel["kalan"] or 0,
                "ders_bazli": [
                    {"ders": d["ders_adi"], "ortalama": d["ort"], "ogrenci": d["ogrenci_sayisi"]}
                    for d in ders_bazli
                ],
            }
    def gpa_hesapla(self, ogrenci_id: int) -> float:
        harf_katsayi = {
            "AA": 4.0, "BA": 3.5, "BB": 3.0, "CB": 2.5,
            "CC": 2.0, "DC": 1.5, "DD": 1.0, "FD": 0.5, "FF": 0.0,
        }
        with VeritabaniBaglantisi(self._db) as db:
            satirlar = db.execute("""
                SELECT n.vize, n.final, d.kredi
                FROM notlar n
                JOIN dersler d ON n.ders_id = d.id
                WHERE n.ogrenci_id = ?
            """, (ogrenci_id,)).fetchall()
            if not satirlar:
                return 0.0
            toplam_puan = sum(
                harf_katsayi[Not.ortalamadan_harf(s["vize"] * 0.4 + s["final"] * 0.6)] * s["kredi"]
                for s in satirlar
            )
            toplam_kredi = sum(s["kredi"] for s in satirlar)
            return round(toplam_puan / toplam_kredi, 2) if toplam_kredi > 0 else 0.0
