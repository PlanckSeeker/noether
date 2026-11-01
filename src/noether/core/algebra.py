import sympy as sp


class SparseMultivector:
    """
    Symbolic Multivector for Projective Geometric Algebra G(3,0,1).
    Basis bitmask representation (bits 0 to 3):
    - Bit 0 (0b0001): e0 (nilpotent origin, e0*e0 = 0)
    - Bit 1 (0b0010): e1 (e1^2 = 1)
    - Bit 2 (0b0100): e2 (e2^2 = 1)
    - Bit 3 (0b1000): e3 (e3^2 = 1)
    """

    def __init__(self, blades: dict[int, sp.Expr]):
        self.blades = {k: sp.sympify(v) for k, v in blades.items() if v != 0}

    @staticmethod
    def _multiply_basis(b1: int, b2: int) -> tuple[int, int]:
        """
        Multiplies two basis blades represented as bitmasks.
        Returns a tuple of (target_bitmask, sign_multiplier (+1 or -1)).
        Enforces e0*e0 = 0 (returns sign 0 if nilpotent collision occurs).
        """
        # Check for e0 * e0 collision (Bit 0 set in both)
        if (b1 & 1) and (b2 & 1):
            return 0, 0

        target = b1 ^ b2
        sign = 1

        # Count anti-commutation swaps needed for standard basis ordering
        # Extract active spatial indices (bits 1, 2, 3)
        swaps = 0
        # Simple bubble-sort inversion count for bits 1, 2, 3
        active_bits = []
        for i in range(1, 4):
            if b1 & (1 << i):
                active_bits.append(i)
        for i in range(1, 4):
            if b2 & (1 << i):
                active_bits.append(i)

        # Count inversions to determine sign change from anti-commutation (ei * ej = -ej * ei)
        for i in range(len(active_bits)):
            for j in range(i + 1, len(active_bits)):
                if active_bits[i] > active_bits[j]:
                    swaps += 1

        if swaps % 2 == 1:
            sign *= -1

        # Account for metric squares: e1^2 = 1, e2^2 = 1, e3^2 = 1; e0^2 = 0
        # Whenever identical spatial generators meet (e_i * e_i = +1)
        for i in range(1, 4):
            if (b1 & (1 << i)) and (b2 & (1 << i)):
                sign *= 1

        return target, sign

    def __mul__(self, other: 'SparseMultivector') -> 'SparseMultivector':
        result: dict[int, sp.Expr] = {}
        for k1, v1 in self.blades.items():
            for k2, v2 in other.blades.items():
                target, sign = self._multiply_basis(k1, k2)
                if sign == 0:
                    continue  # Nilpotent term vanished (e.g. e0*e0 = 0)

                term = sign * v1 * v2
                result[target] = result.get(target, 0) + term

        return SparseMultivector(result)