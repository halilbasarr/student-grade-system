import sqlite3
import os
from typing import Optional


class VeritabaniBaglantisi:
    def __init__(self, dosya_adi: str) -> None:
        klasor = os.path.dirname(os.path.abspath(__file__))
        self._yol = os.path.join(klasor, dosya_adi)
        self._baglanti: Optional[sqlite3.Connection] = None
    def __enter__(self) -> sqlite3.Connection:
        self._baglanti = sqlite3.connect(self._yol)
        self._baglanti.row_factory = sqlite3.Row
        self._baglanti.execute("PRAGMA foreign_keys = ON")
        return self._baglanti
    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if self._baglanti:
            if exc_type is None:
                self._baglanti.commit()
            else:
                self._baglanti.rollback()
            self._baglanti.close()
        return False
def veritabani_olustur(dosya_adi: str = "okul.db") -> None:
    with VeritabaniBaglantisi(dosya_adi) as db:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS ogrenciler (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                ad          TEXT    NOT NULL,
                soyad       TEXT    NOT NULL,
                numara      TEXT    UNIQUE NOT NULL,
                kayit_tarihi TEXT   DEFAULT (date('now'))
            );
            CREATE TABLE IF NOT EXISTS dersler (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                ders_adi    TEXT    UNIQUE NOT NULL,
                kredi       INTEGER NOT NULL CHECK(kredi > 0)
            );
            CREATE TABLE IF NOT EXISTS notlar (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                ogrenci_id  INTEGER NOT NULL,
                ders_id     INTEGER NOT NULL,
                vize        REAL    CHECK(vize BETWEEN 0 AND 100),
                final       REAL    CHECK(final BETWEEN 0 AND 100),
                FOREIGN KEY (ogrenci_id) REFERENCES ogrenciler(id) ON DELETE CASCADE,
                FOREIGN KEY (ders_id)    REFERENCES dersler(id)    ON DELETE CASCADE,
                UNIQUE(ogrenci_id, ders_id)
            );
        """)