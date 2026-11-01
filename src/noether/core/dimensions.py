from fractions import Fraction
from dataclasses import dataclass
from typing import Self

@dataclass(frozen=True)
class Q8Lattice:
    """
    Immutable representation of the 8-dimensional SI unit lattice:
    (Length, Mass, Time, Current, Temperature, Amount, LuminousIntensity, SolidAngle)
    """
    exponents: tuple[Fraction, Fraction, Fraction, Fraction, Fraction, Fraction, Fraction, Fraction]

    @classmethod
    def dimensionless(cls) -> Self:
        return cls(tuple([Fraction(0)] * 8))  # type: ignore

    @classmethod
    def base(cls, index: int) -> Self:
        vec = [Fraction(0)] * 8
        vec[index] = Fraction(1)
        return cls(tuple(vec))  # type: ignore

    def __mul__(self, other: Self) -> Self:
        return Q8Lattice(tuple(a + b for a, b in zip(self.exponents, other.exponents)))  # type: ignore

    def __truediv__(self, other: Self) -> Self:
        return Q8Lattice(tuple(a - b for a, b in zip(self.exponents, other.exponents)))  # type: ignore

    def __pow__(self, power: int | Fraction) -> Self:
        p = Fraction(power)
        return Q8Lattice(tuple(a * p for a in self.exponents))  # type: ignore

    def is_dimensionless(self) -> bool:
        return all(e == Fraction(0) for e in self.exponents)


# Standard SI Bases
Length = Q8Lattice.base(0)
Mass = Q8Lattice.base(1)
Time = Q8Lattice.base(2)
Current = Q8Lattice.base(3)
Temperature = Q8Lattice.base(4)
Amount = Q8Lattice.base(5)
LuminousIntensity = Q8Lattice.base(6)
SolidAngle = Q8Lattice.base(7)