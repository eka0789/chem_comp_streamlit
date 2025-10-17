"""
Core computations for the Chemical Computation mini-app.
All formulas are aligned with the lecture slides you uploaded.
No external internet dependencies.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Dict, Tuple, List
import math

# ---------- Geometry: Cylinder Tank ----------
def cylinder_volume_liters(diameter_cm: float, height_m: float) -> float:
    """
    Volume of a vertical cylinder tank in liters.
    - diameter in cm
    - height in meters
    Returns liters.
    """
    if diameter_cm <= 0 or height_m <= 0:
        raise ValueError("Diameter and height must be positive.")
    radius_m = (diameter_cm / 100.0) / 2.0
    volume_m3 = math.pi * radius_m**2 * height_m
    return volume_m3 * 1000.0  # 1 m^3 = 1000 L

def fill_height_for_fraction(total_height_m: float, fraction: float) -> float:
    """
    For a vertical cylinder, liquid height is proportional to volume fraction.
    Returns the liquid height (m) corresponding to a filled fraction (0..1).
    """
    if not (0.0 <= fraction <= 1.0):
        raise ValueError("fraction must be in [0,1].")
    if total_height_m <= 0:
        raise ValueError("total_height_m must be positive.")
    return total_height_m * fraction

# ---------- Temperature Conversion ----------
def celsius_to_fahrenheit(c: float) -> float:
    return (9.0/5.0) * c + 32.0

def c_to_f_table(start: float = 0.0, stop: float = 100.0, step: float = 5.0):
    if step <= 0:
        raise ValueError("step must be positive.")
    vals = []
    x = start
    # Handle float increments robustly
    while x <= stop + 1e-9:
        vals.append((round(x, 6), round(celsius_to_fahrenheit(x), 6)))
        x += step
    return vals

# ---------- Antoine Equation ----------
@dataclass
class AntoineParams:
    """
    Antoine parameters for the ln-form used in the slides:
        ln(P_kPa) = A - B / (T_K + C)
    Units:
        - T in Kelvin (K)
        - P in kPa
    """
    A: float
    B: float
    C: float

def psat_antoine_ln(T_K: float, params: AntoineParams) -> float:
    if T_K <= 0:
        raise ValueError("Temperature in Kelvin must be > 0.")
    return params.A - params.B / (T_K + params.C)

def psat_antoine(T_K: float, params: AntoineParams) -> float:
    """
    Returns saturation vapor pressure in kPa using the ln-form.
    """
    return math.exp(psat_antoine_ln(T_K, params))

# ---------- Mixture (Ideal, Raoult's Law) ----------
def mixture_psat_raoult_kPa(T_K: float, components: List[Tuple[float, AntoineParams]]) -> float:
    """
    Ideal mixture (Raoult's law): P = sum_i x_i * P_sat_i(T).
    components: list of tuples (xi, AntoineParams)
    xi should sum to 1.0 (tolerance applied); we will normalize defensively.
    """
    if len(components) == 0:
        raise ValueError("components cannot be empty.")
    total_x = sum(x for x, _ in components)
    if total_x <= 0:
        raise ValueError("Sum of mole fractions must be positive.")
    # Normalize to be safe
    norm_components = [ (x/total_x, p) for x,p in components ]
    return sum(x * psat_antoine(T_K, p) for x,p in norm_components)
