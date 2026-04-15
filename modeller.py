from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Ogrenci:
    ad: str
    soyad: str
    numara: str
    id: Optional[int] = None
    kayit_tarihi: Optional[str] = None
    def __post_init__(self) -> None:
        if not self.ad.strip() or not self.soyad.strip():
            raise ValueError("Ad ve soyad boş olamaz.")
        if not self.numara.strip():
            raise ValueError("Öğrenci numarası boş olamaz.")
        self.ad = self.ad.strip().title()
        self.soyad = self.soyad.strip().upper()
    @property
    def tam_ad(self) -> str:
        return f"{self.ad} {self.soyad}"
    def __str__(self) -> str:
        return f"[{self.numara}] {self.tam_ad}"
@dataclass
class Ders:
    ders_adi: str
    kredi: int
    id: Optional[int] = None
    def __post_init__(self) -> None:
        if not self.ders_adi.strip():
            raise ValueError("Ders adı boş olamaz.")
        if self.kredi <= 0:
            raise ValueError("Kredi 0'dan büyük olmalı.")
        self.ders_adi = self.ders_adi.strip().title()
    def __str__(self) -> str:
        return f"{self.ders_adi} ({self.kredi} kredi)"
@dataclass
class Not:
    ogrenci_id: int
    ders_id: int
    vize: float
    final: float
    id: Optional[int] = None
    ogrenci_adi: Optional[str] = field(default=None, repr=False)
    ders_adi: Optional[str] = field(default=None, repr=False)
    def __post_init__(self) -> None:
        if not (0 <= self.vize <= 100):
            raise ValueError("Vize notu 0-100 arasında olmalı.")
        if not (0 <= self.final <= 100):
            raise ValueError("Final notu 0-100 arasında olmalı.")
    @property
    def ortalama(self) -> float:
        return self.vize * 0.4 + self.final * 0.6
    @property
    def harf_notu(self) -> str:
        return Not.ortalamadan_harf(self.ortalama)
    @property
    def gecti_mi(self) -> bool:
        return self.ortalama >= 50.0
    @staticmethod
    def ortalamadan_harf(ortalama: float) -> str:
        if ortalama >= 90:
            return "AA"
        elif ortalama >= 85:
            return "BA"
        elif ortalama >= 80:
            return "BB"
        elif ortalama >= 75:
            return "CB"
        elif ortalama >= 70:
            return "CC"
        elif ortalama >= 65:
            return "DC"
        elif ortalama >= 60:
            return "DD"
        elif ortalama >= 50:
            return "FD"
        else:
            return "FF"
    def __str__(self) -> str:
        return (f"Vize: {self.vize:.0f} | Final: {self.final:.0f} | "
                f"Ort: {self.ortalama:.1f} | {self.harf_notu}")
