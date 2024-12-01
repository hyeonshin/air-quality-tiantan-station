import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

all_df = pd.read_csv("main_data.csv")

def corr_aq(tiantan_df):
    data = tiantan_df

    numeric_columns = data.select_dtypes(include='number').drop(columns="No", errors='ignore')

    correlation_matrix = numeric_columns.corr()

    plt.figure(figsize=(10, 8)) 
    sns.heatmap(
        correlation_matrix,
        annot=True,          
        cmap='coolwarm',      
        fmt=".2f",            
        linewidths=0.5         
    )
    plt.title('Heatmap of Correlations')
    plt.show()

def yearly_aq(tiantan_df):
    yearly_tiantan_df = tiantan_df.groupby("year").mean(numeric_only=True)

    plt.figure(figsize=(10, 5))
    plt.plot(
        yearly_tiantan_df.index, yearly_tiantan_df["PM2.5"], label="PM2.5",
        marker='o', 
    )
    plt.plot(
        yearly_tiantan_df.index, yearly_tiantan_df["PM10"], label="PM10",
        marker='o', 
    )
    plt.plot(
        yearly_tiantan_df.index, yearly_tiantan_df["SO2"], label="SO2",
        marker='o', 
    )
    plt.plot(
        yearly_tiantan_df.index, yearly_tiantan_df["NO2"], label="NO2",
        marker='o', 
    )
    plt.plot(
        yearly_tiantan_df.index, yearly_tiantan_df["O3"], label="O3",
        marker='o', 
    )
    plt.title("Angka Polutan Udara di Tiantan per Tahun", loc="center", fontsize=16)
    plt.xlabel("Tahun")
    plt.ylabel("mg/m³")
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.legend()
    plt.show()

    #CO

    plt.plot(
        yearly_tiantan_df.index, yearly_tiantan_df["CO"], label="CO",
        marker='o', 
    )
    plt.title("Angka Polutan CO di Tiantan per Tahun", loc="center", fontsize=10)
    plt.xlabel("Tahun")
    plt.ylabel("mg/m³")
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.legend()
    plt.show()

def best_worst_aq(tiantan_df):
    yearly_tiantan_df = tiantan_df.groupby("year").mean(numeric_only=True)

    plt.plot(
        yearly_tiantan_df.index, yearly_tiantan_df["PM2.5"], label="PM2.5",
        marker='o', 
    )
    plt.title("Angka Polutan PM2.5 di Tiantan per Tahun", loc="center", fontsize=10)
    plt.xlabel("Tahun")
    plt.ylabel("mg/m³")
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.legend()
    plt.show()

def hourly_aq(tiantan_df):
    data = tiantan_df

    hourly_pm25 = data.groupby('hour')['PM2.5'].mean()

    max_hour = hourly_pm25.idxmax()
    max_value = hourly_pm25.max()

    colors = ['red' if hour == max_hour else 'gray' for hour in hourly_pm25.index]

    plt.figure(figsize=(10, 6))
    hourly_pm25.plot(kind='bar', color=colors, edgecolor='black')
    plt.title('Average PM2.5 Levels by Hour', fontsize=16)
    plt.xlabel('Hour of the Day', fontsize=14)
    plt.ylabel('PM2.5 Concentration', fontsize=14)
    plt.xticks(rotation=0)  
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.text(max_hour, max_value + 2, f'{max_value:.2f}', ha='center', va='bottom', fontsize=12, color='black')

    plt.tight_layout()
    plt.show()

st.header('Air Quality Analyst Dashboard Tiantan Station :sparkles:')

st.subheader("Correlation Table Air Quality")
st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Select Year', list(all_df['year'].unique()))
selected_month = st.sidebar.selectbox('Select Month', list(all_df['month'].unique()))

data_filtered = all_df[(all_df['year'] == selected_year) & (all_df['month'] == selected_month)].copy()

# Displaying data statistics
st.subheader('Data Overview for Selected Period')
st.write(data_filtered.describe())

# Line chart for PM2.5 levels over selected month
st.subheader('Daily PM2.5 Levels')
fig, ax = plt.subplots()
ax.plot(data_filtered['day'], data_filtered['PM2.5'])
plt.xlabel('Day of the Month')
plt.ylabel('PM2.5 Concentration')
st.pyplot(fig)

# corr_aq(all_df)

st.caption('Copyright © Mohammad Nashrullah 2024')