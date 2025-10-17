import streamlit as st
import pandas as pd
from src.chem.physics import (
    cylinder_volume_liters, fill_height_for_fraction,
    c_to_f_table, AntoineParams, psat_antoine, mixture_psat_raoult_kPa
)

st.set_page_config(page_title="Komputasi Teknik Kimia - Mini App", layout="wide")

st.title("TK611056 • Komputasi Teknik Kimia — Mini App")
st.caption("Dibuat berdasarkan materi: matriks/visualisasi, kontrol alur, dan contoh soal (silinder, konversi suhu, Antoine).")

tab1, tab2, tab3, tab4 = st.tabs([
    "1) Silinder (Volume & 80%)",
    "2) Tabel °C → °F",
    "3) P_sat (Antoine) — Komponen Tunggal",
    "4) P_campuran (Raoult + Antoine)"
])

with tab1:
    st.subheader("Volume Tangki Silinder & Ketinggian pada 80%")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        diameter_cm = st.number_input("Diameter alas (cm)", min_value=0.0, value=140.0, step=1.0)
    with col_b:
        height_m = st.number_input("Tinggi tangki (m)", min_value=0.0, value=2.0, step=0.1)
    with col_c:
        fraction = st.slider("Fraksi pengisian (0–1)", 0.0, 1.0, 0.8, 0.05)
    if st.button("Hitung Volume & Tinggi"):
        try:
            vol_L = cylinder_volume_liters(diameter_cm, height_m)
            h80 = fill_height_for_fraction(height_m, fraction)
            st.metric("Volume penuh (L)", f"{vol_L:,.2f}")
            st.metric(f"Tinggi pada {fraction*100:.0f}% (m)", f"{h80:,.3f}")
        except Exception as e:
            st.error(str(e))

with tab2:
    st.subheader("Konversi Suhu: Celsius → Fahrenheit (Tabel)")
    c1, c2, c3 = st.columns(3)
    with c1:
        start = st.number_input("Mulai (°C)", value=0.0, step=1.0)
    with c2:
        stop = st.number_input("Selesai (°C)", value=100.0, step=1.0)
    with c3:
        step = st.number_input("Langkah (°C)", value=5.0, step=0.5)
    if st.button("Buat Tabel"):
        try:
            data = c_to_f_table(start, stop, step)
            df = pd.DataFrame(data, columns=["Celsius (°C)", "Fahrenheit (°F)"])
            st.dataframe(df, use_container_width=True)
            st.download_button("Unduh CSV", df.to_csv(index=False).encode("utf-8"), "c_to_f.csv", "text/csv")
        except Exception as e:
            st.error(str(e))

with tab3:
    st.subheader("Tekanan Uap Jenuh (P_sat) — Persamaan Antoine (ln P = A - B/(T + C))")
    st.markdown("**Catatan:** Gunakan satuan **T dalam Kelvin** dan **P dalam kPa** sesuai slide.")
    col = st.columns(4)
    T_K = col[0].number_input("T (K)", min_value=0.0, value=298.15, step=1.0)
    A = col[1].number_input("A", value=14.0568)
    B = col[2].number_input("B", value=2825.42)
    C = col[3].number_input("C", value=-42.7089)
    if st.button("Hitung P_sat (kPa)"):
        try:
            params = AntoineParams(A=A, B=B, C=C)
            P_kPa = psat_antoine(T_K, params)
            st.metric("P_sat (kPa)", f"{P_kPa:,.4f}")
        except Exception as e:
            st.error(str(e))

    st.divider()
    st.markdown("### Sweep Temperatur")
    colR = st.columns(3)
    Tmin = colR[0].number_input("T_min (K)", value=293.15)
    Tmax = colR[1].number_input("T_max (K)", value=373.15)
    dT = colR[2].number_input("ΔT (K)", min_value=0.001, value=5.0)
    if st.button("Buat Tabel & Grafik P_sat vs T"):
        try:
            params = AntoineParams(A=A, B=B, C=C)
            Ts, Ps = [], []
            T = Tmin
            while T <= Tmax + 1e-9:
                Ts.append(T)
                Ps.append(psat_antoine(T, params))
                T += dT
            df = pd.DataFrame({"T (K)": Ts, "P_sat (kPa)": Ps})
            st.dataframe(df, use_container_width=True)
            st.line_chart(df, x="T (K)", y="P_sat (kPa)")
            st.download_button("Unduh CSV", df.to_csv(index=False).encode("utf-8"), "psat_single.csv", "text/csv")
        except Exception as e:
            st.error(str(e))

with tab4:
    st.subheader("Campuran Ideal (Raoult): P = Σ xᵢ P_sat,ᵢ (kPa)")
    st.markdown("**Contoh tugas:** 50% etanol + 50% air, T = 20–100 °C (konversi ke K terlebih dahulu).")
    st.markdown("Masukkan parameter Antoine tiap komponen. (Jika tidak yakin, isi manual dari data referensi.)")
    c_top = st.columns(3)
    TminC = c_top[0].number_input("T_min (°C)", value=20.0)
    TmaxC = c_top[1].number_input("T_max (°C)", value=100.0)
    dTC = c_top[2].number_input("ΔT (°C)", min_value=0.001, value=10.0)

    st.markdown("#### Komponen 1")
    cc1 = st.columns(4)
    x1 = cc1[0].number_input("x₁ (fraksi mol)", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
    A1 = cc1[1].number_input("A₁", value=14.0568)
    B1 = cc1[2].number_input("B₁", value=2825.42)
    C1 = cc1[3].number_input("C₁", value=-42.7089)

    st.markdown("#### Komponen 2")
    cc2 = st.columns(4)
    x2 = cc2[0].number_input("x₂ (fraksi mol)", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
    A2 = cc2[1].number_input("A₂", value=14.0)
    B2 = cc2[2].number_input("B₂", value=2800.0)
    C2 = cc2[3].number_input("C₂", value=-40.0)

    if st.button("Hitung & Plot P_campuran vs T"):
        import numpy as np
        try:
            params1 = AntoineParams(A=A1, B=B1, C=C1)
            params2 = AntoineParams(A=A2, B=B2, C=C2)
            TsC = np.arange(TminC, TmaxC + 1e-9, dTC)
            TsK = TsC + 273.15
            Pmix = []
            for T in TsK:
                P = mixture_psat_raoult_kPa(T, [(x1, params1), (x2, params2)])
                Pmix.append(P)
            df = pd.DataFrame({"T (°C)": TsC, "P_campuran (kPa)": Pmix})
            st.dataframe(df, use_container_width=True)
            st.line_chart(df, x="T (°C)", y="P_campuran (kPa)")
            st.download_button("Unduh CSV", df.to_csv(index=False).encode("utf-8"), "psat_mixture.csv", "text/csv")
        except Exception as e:
            st.error(str(e))
