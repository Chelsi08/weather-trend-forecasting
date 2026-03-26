import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import json
from datetime import datetime

# ── Page Config
st.set_page_config(
    page_title="Weather Trend Forecasting",
    page_icon="🌦️",
    layout="wide"
)


# ── Load Data 
@st.cache_data
def load_data():
    daily    = pd.read_csv('daily_global.csv', parse_dates=['last_updated'])
    forecast = pd.read_csv('forecast.csv',     parse_dates=['ds'])
    test     = pd.read_csv('test_results.csv', parse_dates=['ds'])
    with open('metrics.json') as f:
        metrics = json.load(f)
    return daily, forecast, test, metrics

daily, forecast, test, metrics = load_data()

# ── Header 
st.title("🌦️ Global Weather Trend Forecasting")
st.markdown("Analyzing **130,978 weather readings** across **211 countries** to forecast global temperature trends.")
st.markdown("---")

# ── Metric Cards 
st.subheader("📊 Model Performance")
col1, col2, col3, col4 = st.columns(4)

col1.metric("MAE",  f"{metrics['mae']}°C",  "Mean Absolute Error")
col2.metric("RMSE", f"{metrics['rmse']}°C", "Root Mean Squared Error")
col3.metric("MAPE", f"{metrics['mape']}%",  "Mean Abs % Error")
col4.metric("Improvement", "22.7%", "vs baseline model")

st.markdown("---")

# ── Forecast Plot 
st.subheader("📈 Temperature Forecast — Global Daily Average")

# Split forecast into historical and future
last_actual_date = daily['last_updated'].max()
forecast_future  = forecast[forecast['ds'] > last_actual_date]
forecast_hist    = forecast[forecast['ds'] <= last_actual_date]

fig = go.Figure()

# Actual historical temperatures
fig.add_trace(go.Scatter(
    x=daily['last_updated'],
    y=daily['avg_temp'],
    mode='lines',
    name='Actual Temperature',
    line=dict(color='#2196F3', width=1.5),
    opacity=0.8
))

# Prophet fit on historical
fig.add_trace(go.Scatter(
    x=forecast_hist['ds'],
    y=forecast_hist['yhat'],
    mode='lines',
    name='Model Fit',
    line=dict(color='#FF9800', width=1.5, dash='dot'),
    opacity=0.7
))

# Future forecast
fig.add_trace(go.Scatter(
    x=forecast_future['ds'],
    y=forecast_future['yhat'],
    mode='lines',
    name='Future Forecast',
    line=dict(color='#F44336', width=2.5)
))

# Confidence interval
fig.add_trace(go.Scatter(
    x=pd.concat([forecast_future['ds'], forecast_future['ds'][::-1]]),
    y=pd.concat([forecast_future['yhat_upper'], forecast_future['yhat_lower'][::-1]]),
    fill='toself',
    fillcolor='rgba(244,67,54,0.15)',
    line=dict(color='rgba(255,255,255,0)'),
    name='95% Confidence Interval'
))

fig.update_layout(
    xaxis_title='Date',
    yaxis_title='Average Temperature (°C)',
    hovermode='x unified',
    legend=dict(orientation='h', yanchor='bottom', y=1.02),
    height=450,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)
fig.update_xaxes(showgrid=True, gridcolor='rgba(128,128,128,0.2)')
fig.update_yaxes(showgrid=True, gridcolor='rgba(128,128,128,0.2)')

st.plotly_chart(fig, use_container_width=True)

# ── Test Period Zoom 
st.subheader("🔍 Test Period — Actual vs Predicted")

fig2 = go.Figure()

fig2.add_trace(go.Scatter(
    x=test['ds'], y=test['y'],
    mode='lines',
    name='Actual',
    line=dict(color='#2196F3', width=2)
))

fig2.add_trace(go.Scatter(
    x=test['ds'], y=test['yhat'],
    mode='lines',
    name='Predicted',
    line=dict(color='#F44336', width=2, dash='dash')
))

fig2.add_trace(go.Scatter(
    x=pd.concat([test['ds'], test['ds'][::-1]]),
    y=pd.concat([test['yhat_upper'], test['yhat_lower'][::-1]]),
    fill='toself',
    fillcolor='rgba(244,67,54,0.1)',
    line=dict(color='rgba(255,255,255,0)'),
    name='95% CI'
))

fig2.update_layout(
    xaxis_title='Date',
    yaxis_title='Avg Temperature (°C)',
    hovermode='x unified',
    height=350,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)
fig2.update_xaxes(showgrid=True, gridcolor='rgba(128,128,128,0.2)')
fig2.update_yaxes(showgrid=True, gridcolor='rgba(128,128,128,0.2)')

st.plotly_chart(fig2, use_container_width=True)

# ── EDA Section ────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("🔎 Exploratory Data Analysis")

tab1, tab2, tab3 = st.tabs(["Temperature", "Humidity & Precipitation", "Model Comparison"])

with tab1:
    fig3 = px.histogram(
        daily, x='avg_temp', nbins=50,
        title='Global Daily Average Temperature Distribution',
        color_discrete_sequence=['#2196F3']
    )
    fig3.update_layout(
        xaxis_title='Temperature (°C)',
        yaxis_title='Frequency',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig3, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        fig4 = px.line(
            daily, x='last_updated', y='avg_humidity',
            title='Global Average Humidity Over Time',
            color_discrete_sequence=['#4CAF50']
        )
        fig4.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig4, use_container_width=True)
    with col2:
        fig5 = px.line(
            daily, x='last_updated', y='total_precip',
            title='Global Total Precipitation Over Time',
            color_discrete_sequence=['#9C27B0']
        )
        fig5.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig5, use_container_width=True)

with tab3:
    comparison_data = {
        'Model': ['Original Prophet', 'Tuned Prophet', 'Tuned + Regressors'],
        'MAE':   [0.81, 0.63, 1.02],
        'RMSE':  [1.05, 0.78, 1.20],
        'MAPE':  [4.97, 3.81, 6.22]
    }
    df_comp = pd.DataFrame(comparison_data)

    fig6 = go.Figure()
    fig6.add_trace(go.Bar(name='MAE',  x=df_comp['Model'], y=df_comp['MAE'],  marker_color='#2196F3'))
    fig6.add_trace(go.Bar(name='RMSE', x=df_comp['Model'], y=df_comp['RMSE'], marker_color='#F44336'))
    fig6.add_trace(go.Bar(name='MAPE', x=df_comp['Model'], y=df_comp['MAPE'], marker_color='#FF9800'))

    fig6.update_layout(
        barmode='group',
        title='Model Comparison — Lower is Better',
        yaxis_title='Error',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig6, use_container_width=True)

    st.dataframe(df_comp, use_container_width=True)

# ── Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
Built by <b>Chelsi</b> | 
Facebook Prophet | pandas | Streamlit | 
<a href='https://github.com/Chelsi08/weather-trend-forecasting'>GitHub</a>
</div>
""", unsafe_allow_html=True)