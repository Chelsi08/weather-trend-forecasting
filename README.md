# 🌦️ Weather Trend Forecasting

Analyzing 130,978 global weather readings across 211 countries to forecast temperature trends using time series modeling.

---

## 📌 Project Overview

An end-to-end data science project covering data cleaning, exploratory analysis, time series forecasting, hyperparameter tuning, and model evaluation using Facebook Prophet.

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
├── weather_trend_forecast.ipynb  # Main notebook (all code)
├── daily_global.csv              # Aggregated daily global averages
├── forecast.csv                  # Prophet forecast output
├── test_results.csv              # Model evaluation results
├── metrics.json                  # MAE, RMSE, MAPE scores
├── requirements.txt              # Dependencies
└── README.md                     # This file
```

---

## ⚙️ How to Run

### Option 1 — Google Colab (recommended)
1. Open `weather_trend_forecast.ipynb` in Google Colab
2. Run Cell 1 — it will prompt you to upload your `kaggle.json` API key
3. Run all remaining cells in order

### Option 2 — Local
```bash
git clone https://github.com/Chelsi08/weather-trend-forecasting
cd weather-trend-forecasting
pip install -r requirements.txt
jupyter notebook weather_trend_forecast.ipynb
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
- Strong positive correlation between temperature and UV index (+0.49)
- Humidity negatively correlated with UV index (-0.55)
- Clear annual seasonal cycle visible in global daily averages

### 3. Forecasting — Three Models Tested

#### Model 1: Original Prophet (Baseline)
- Aggregated 130K+ rows into **674 daily global averages**
- Train/test split: 614 days training, 60 days holdout test
- Yearly seasonality, changepoint_prior_scale = 0.05

#### Model 2: Tuned Prophet
- Systematically tested 8 values of `changepoint_prior_scale` (0.005 → 0.05)
- Optimal value found: **0.03**
- Tested additive vs multiplicative seasonality — additive won

#### Model 3: Tuned Prophet + Weather Regressors
- Added humidity, pressure, UV index, cloud cover, wind as inputs
- Result: performance degraded — regressors are seasonally collinear with
  temperature. Prophet's built-in seasonality already captures this information.
  More features did not mean a better model.

### 4. Model Evaluation

| Model | MAE | RMSE | MAPE |
|-------|-----|------|------|
| Original Prophet | 0.81°C | 1.05°C | 4.97% |
| Tuned Prophet | 0.63°C | 0.78°C | 3.81% |
| Tuned + Regressors | 1.02°C | 1.20°C | 6.22% |

**Best model: Tuned Prophet — 22.7% improvement over baseline**

Forecast extends 90 days beyond the test period to June 2026.

### 5. Key Findings
- Global temperatures follow a clear annual cycle: peak July–September
  (+4°C above trend), trough in January (−4°C below trend)
- Hyperparameter tuning reduced MAE from 0.81°C to 0.63°C
- Adding weather regressors degraded performance — collinear features
  add noise, not signal

---

## 📈 Key Visualizations

| Plot | Description |
|------|-------------|
| EDA global patterns | Temperature, humidity, precipitation distributions + correlation heatmap |
| EDA time trends | Daily global trends across all features over time |
| Train/test split | Visual of training vs test period |
| Prophet forecast | Actuals vs forecast with 95% confidence interval |
| Prophet components | Trend and yearly seasonality components |
| Changepoint tuning | Changepoint prior scale tuning curve |
| Model comparison | Original vs tuned model on test period |

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
