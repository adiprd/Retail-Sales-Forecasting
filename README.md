
---

# Retail Sales Forecasting System

Machine Learning for Monthly Retail Demand Prediction

Proyek ini merupakan sistem otomatis untuk **forecasting penjualan retail bulanan** menggunakan algoritma **Random Forest Regressor** dengan pipeline preprocessing lengkap. Sistem dapat:

* Melatih model berbasis data historis 24 bulan
* Mengevaluasi akurasi model
* Menampilkan grafik perbandingan penjualan aktual vs prediksi
* Melakukan forecasting bulan berikutnya (bulan ke-25)
* Menampilkan produk yang diprediksi paling laku

Proyek ini dirancang sebagai fondasi untuk kebutuhan analitik retail maupun pengembangan dashboard prediksi bisnis.

---

## Features

### 1. Automated Machine Learning Pipeline

Menggunakan kombinasi:

* StandardScaler (numerik)
* OneHotEncoder (kategori)
* ColumnTransformer
* RandomForestRegressor
* Penyimpanan model via `joblib`

### 2. Training & Evaluation

Sistem menghasilkan:

* Model forecasting dalam bentuk file `.pkl`
* Akurasi model menggunakan metrik **R² Score**

### 3. Trend Visualization

Sistem menampilkan grafik:

* Penjualan asli 24 bulan
* Prediksi model 24 bulan
  Disertai garis tren untuk analisis kesesuaian model.

### 4. Forecast Next Month (Bulan ke-25)

Forecast mempertimbangkan perubahan:

* Iklan (diasumsikan naik 10%)
* Musim (di-set menjadi Winter)
* Previous sales otomatis diambil dari bulan sebelumnya
  Sistem menampilkan **Top 5 produk** dengan prediksi penjualan tertinggi.

---

## Project Structure

```
├── data_retail_monthly.csv     # Dataset historis (24 bulan)
├── model_forecast.pkl          # Model yang tersimpan (hasil training)
├── forecast_train.py           # Script utama training + forecast
└── README.md                   # Dokumentasi proyek
```

---

## Dataset Format

Dataset harus memiliki kolom:

| Column           | Type   | Description                       |
| ---------------- | ------ | --------------------------------- |
| Month            | int    | Bulan ke-1 sampai ke-24           |
| Category         | string | Kategori produk                   |
| Price            | float  | Harga jual produk                 |
| Competitor_Price | float  | Harga kompetitor                  |
| Tech_Score       | float  | Skor tren teknologi               |
| Social_Hype      | float  | Indeks hype media sosial          |
| Prev_Sales       | float  | Penjualan bulan sebelumnya        |
| Ad_Spend         | float  | Budget iklan                      |
| Season           | string | Musim (Spring/Summer/Fall/Winter) |
| Sales_Qty        | float  | Target penjualan aktual           |

---

## Installation

Pastikan Python 3.8+ tersedia.

Install dependency:

```bash
pip install -r requirements.txt
```

Atau manual:

```bash
pip install pandas numpy matplotlib scikit-learn joblib
```

---

## Usage

### 1. Pastikan dataset tersedia

```
data_retail_monthly.csv
```

Jika belum ada, jalankan generator data Anda terlebih dahulu.

### 2. Jalankan training + visualisasi + forecasting

```bash
python forecast_train.py
```

Sistem akan menampilkan:

* Status training
* Akurasi R²
* Grafik tren
* Hasil forecast bulan ke-25
* Top 5 produk paling laku

---

## Code Overview

Script utama:

```python
python forecast_train.py
```

Fungsi inti:

* `train_visualize_forecast()`

  * Load dataset
  * Training model ML
  * Visualisasi tren
  * Forecast bulan ke-25
  * Simpan model

Model otomatis tersimpan ke:

```
model_forecast.pkl
```

---

## Example Output (Console)

```text
AI sedang training...
Model Disimpan. Akurasi R2: 0.87

Sedang membuat Grafik Perbandingan Per Bulan...

--- PREDIKSI BULAN DEPAN (BULAN KE-25) ---
Top 5 Produk yang diprediksi paling laku bulan depan:
  Category   Price  Prev_Sales  Forecast_Sales_Bln_25
3    Gadget  329.0        540               575.21
5    Laptop  799.0        490               560.44
...
```

---

## Planned Improvements

* Penambahan model ARIMA/LSTM untuk multistep forecasting
* Implementasi SHAP untuk interpretabilitas fitur
* Integrasi ke dashboard analitik (Streamlit, React, atau PowerBI)
* Export otomatis ke Excel/Database

---

## License

Proyek ini dapat digunakan untuk riset, tugas akademik, atau pengembangan bisnis internal.

---
