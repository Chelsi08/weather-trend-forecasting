# 🌦️ Weather Trend Forecasting

**PM Accelerator — Data Science Technical Assessment**

> **PM Accelerator Mission:** Accelerating the development of the next
> generation of product managers through real-world experience,
> mentorship, and community.

---

## 📌 Project Overview

This project analyzes the **Global Weather Repository** dataset to
forecast future global temperature trends using time series modeling.
It covers end-to-end data science workflow: cleaning, exploratory
analysis, forecasting, and model evaluation.

---

## 📂 Dataset

- **Source:** [Global Weather Repository — Kaggle](https://www.kaggle.com/datasets/nelgiriyewithana/global-weather-repository)
- **Size:** 130,978 rows × 41 columns
- **Coverage:** 211 countries, 257 locations
- **Date range:** May 2024 → March 2026

---

## 🔧 Project Structure
```
weather-trend-forecasting/
│
├── Weather_Forecasting.ipynb   # Main notebook (all code)
├── requirements.txt            # Dependencies
└── README.md                   # This file
```

---

## ⚙️ How to Run

### Option 1 — Google Colab (recommended)
1. Open `Weather_Forecasting.ipynb` in Google Colab
2. Run Cell 1 — it will prompt you to upload your `kaggle.json` API key
3. Run all remaining cells in order

### Option 2 — Local
```bash
git clone https://github.com/Chelsi08/weather-trend-forecasting
cd weather-trend-forecasting
pip install -r requirements.txt
jupyter notebook Weather_Forecasting.ipynb
```
> You will need a Kaggle API key (`kaggle.json`) in `~/.kaggle/`

---

## 📊 Methodology

### 1. Data Cleaning
- Removed duplicate unit columns (kept metric system throughout)
- Parsed `last_updated` as datetime
- Clipped physically implausible wind speed outliers > 200 kph (4 rows)
- Removed 1 anomalous global average temperature reading (3.9°C)
- No missing values or duplicate rows found in the dataset

### 2. Exploratory Data Analysis
- Global mean temperature: **21.4°C** (right-skewed distribution)
- **67%** of observations recorded zero precipitation
- Strong positive correlation between temperature and UV index (0.49)
- Humidity negatively correlated with UV index (-0.55)
- Clear annual seasonal cycle visible in global daily averages

### 3. Forecasting Model — Facebook Prophet
- Aggregated 130K+ rows into **674 daily global averages**
- Train/test split: 614 days training, 60 days holdout test
- Configured with yearly seasonality, conservative changepoint scale

### 4. Model Evaluation

| Metric | Value |
|--------|-------|
| MAE    | 0.81°C |
| RMSE   | 1.05°C |
| MAPE   | 4.97% |

Model correctly captures seasonal patterns — peaking July–September
(+4°C above trend) and troughing in January (−4°C below trend).
Forecast extends **90 days beyond the test period** to June 2026.

---

## 📈 Key Visualizations

| Plot | Description |
|------|-------------|
| `eda_global_patterns.png` | Temperature, humidity, precipitation distributions + correlation heatmap |
| `eda_time_trends.png` | Daily global trends across all features over time |
| `train_test_split.png` | Visual of training vs test period |
| `prophet_forecast.png` | Actuals vs forecast with 95% confidence interval |
| `prophet_components.png` | Prophet trend and yearly seasonality components |

---

## 🛠️ Dependencies
```
pandas
numpy
matplotlib
seaborn
scikit-learn
statsmodels
prophet
kaggle
```

---

## 👤 Author

**Chelsi** — Data Science Intern Applicant  
[GitHub](https://github.com/Chelsi08)
