# Komputasi Teknik Kimia — Mini App (Streamlit)

Dibuat berdasarkan materi presentasi: **silinder (volume & tinggi 80%)**, **tabel konversi suhu (°C → °F)**, dan **tekanan uap jenuh menggunakan persamaan Antoine** termasuk **campuran ideal (Raoult)**.

## Fitur
1. **Silinder**: Hitung volume (L) dari diameter (cm) dan tinggi (m). Hitung ketinggian cairan untuk fraksi pengisian (contoh: 80%).
2. **Konversi Suhu**: Bangkitkan tabel °C → °F dari rentang dan step yang dipilih, serta ekspor CSV.
3. **Antoine (Komponen Tunggal)**: `ln(P_kPa) = A - B/(T_K + C)`
   - Input parameter A, B, C
   - Hitung `P_sat (kPa)` pada satu suhu atau sweep T (tabel + grafik + CSV)
4. **Campuran Ideal (Raoult + Antoine)**:
   - Masukkan dua komponen (x₁, x₂) dan parameternya (A, B, C) masing-masing
   - Tampilkan `P_campuran (kPa)` vs T (°C) + unduh CSV

> **Catatan penting satuan**: Sesuai slide, suhu **T dalam Kelvin** dan tekanan **P dalam kPa** di persamaan Antoine. Panel campuran menerima input suhu dalam °C untuk kenyamanan lalu dikonversi ke K.

## Struktur Folder
```
chem_comp_streamlit/
├─ app.py                   # UI Streamlit
├─ README.md
├─ src/
│  └─ chem/
│     └─ physics.py         # Fungsi-fungsi inti (silinder, konversi suhu, Antoine, Raoult)
└─ tests/
   └─ test_core.py          # Unit test dasar (pytest)
```

## Menjalankan
1. Buat environment (opsional) dan install dependensi minimal:
   ```bash
   pip install streamlit pandas pytest
   ```
2. Jalankan aplikasi Streamlit:
   ```bash
   streamlit run app.py
   ```
3. Jalankan unit test:
   ```bash
   pytest -q
   ```

## Parameter Antoine
Slide menyediakan contoh **n-heksana**: `A=14.0568`, `B=2825.42`, `C=-42.7089` untuk bentuk **ln(P_kPa) = A - B/(T_K + C)**.
Untuk komponen lain (mis. etanol & air pada tugas 01), **isikan manual** parameter Antoine sesuai referensi yang menggunakan **bentuk dan satuan yang sama**.

> **Tip**: Parameter Antoine di literatur sering bervariasi bentuk & satuan (log10 atau ln, P dalam bar/torr/kPa, T dalam °C/K). Pastikan **konsisten** dengan bentuk ln dan unit **kPa** serta **K** di aplikasi ini atau konversi terlebih dahulu.

## Validasi Cepat (Contoh dari Slide)
- **Silinder**: diameter 140 cm, tinggi 2 m → volume ≈ 3.079 m³ = **≈ 3078.76 L**; ketinggian 80% = **1.6 m**.
- **Konversi suhu**: 0 °C → 32 °F; 100 °C → 212 °F.
- **Antoine**: dengan parameter contoh, `P_sat` meningkat saat T meningkat (uji monotonisitas di unit test).

## Ekstensi yang Disarankan
- Tambah **grafik semi-log** untuk `P_sat`.
- Tambah **komponen lebih dari dua** pada panel campuran.
- Simpan & muat preset parameter komponen (JSON).
- Tambah **bahasa Indonesia/Inggris** toggle.
- Tambah panel **regresi/interpolasi** sesuai bagian metode numerik.

## Lisensi
Untuk tujuan pendidikan/latihan. Silakan modifikasi sesuai kebutuhan kelas.
