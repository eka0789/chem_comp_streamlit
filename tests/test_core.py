import math
from src.chem.physics import (
    cylinder_volume_liters, fill_height_for_fraction,
    celsius_to_fahrenheit, c_to_f_table, AntoineParams, psat_antoine, mixture_psat_raoult_kPa
)

def test_cylinder_volume_and_height():
    vol = cylinder_volume_liters(140.0, 2.0)
    # volume = pi * r^2 * h = pi*(0.7^2)*2 m^3 = pi*0.49*2= ~3.07876 m^3 = 3078.76 L
    assert 3070 < vol < 3090
    assert fill_height_for_fraction(2.0, 0.8) == 1.6

def test_temp_conversion():
    assert celsius_to_fahrenheit(0.0) == 32.0
    assert celsius_to_fahrenheit(100.0) == 212.0
    table = c_to_f_table(0, 10, 5)
    assert table == [(0, 32.0), (5, 41.0), (10, 50.0)]

def test_antoine_ln_form_monotonic():
    # Using the n-hexane-like example parameters from slides
    params = AntoineParams(A=14.0568, B=2825.42, C=-42.7089)
    P1 = psat_antoine(293.15, params)
    P2 = psat_antoine(303.15, params)
    assert P2 > P1  # higher T -> higher P_sat

def test_mixture_raoult():
    p = AntoineParams(A=14.0568, B=2825.42, C=-42.7089)
    P = mixture_psat_raoult_kPa(298.15, [(0.5, p), (0.5, p)])
    # Should equal the pure-component P when both components identical and x=0.5+0.5
    assert abs(P - psat_antoine(298.15, p)) < 1e-9
