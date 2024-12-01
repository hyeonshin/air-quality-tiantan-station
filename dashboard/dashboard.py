import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

all_df = pd.read_csv("./main_data.csv")

st.header('Air Quality Tiantan Station Dashboard:sparkles:')

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Select Year', list(all_df['year'].unique()))
selected_month = st.sidebar.selectbox('Select Month', list(all_df['month'].unique()))

data_filtered = all_df[(all_df['year'] == selected_year) & (all_df['month'] == selected_month)].copy()

# Displaying data statistics
st.subheader('Data Overview for Selected Period')
st.write(data_filtered.describe())

# Corellation Matrix
data = all_df 
st.subheader("Correlation Heatmap")

# Select numeric columns, excluding "No" if it exists
numeric_columns = data.select_dtypes(include='number').drop(columns="No", errors='ignore')

# Compute the correlation matrix
correlation_matrix = numeric_columns.corr()

st.write("#### Correlation Matrix")
st.dataframe(correlation_matrix)

# Create and display the heatmap using Matplotlib and Seaborn
st.write("#### Heatmap of Correlations")
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(
    correlation_matrix,
    annot=True,          # Show correlation values
    cmap='coolwarm',     # Colormap
    fmt=".2f",           # Decimal format
    linewidths=0.5       # Line width between cells
)
plt.title('Heatmap of Correlations')
st.pyplot(fig)


# yearly
st.subheader("Yearly Air Pollution Levels at Tiantan")

# Group data by year and calculate the mean for numeric columns
yearly_tiantan_df = all_df.groupby("year").mean(numeric_only=True)

# Display the yearly data in Streamlit
st.write("#### Yearly Average Data")
st.dataframe(yearly_tiantan_df)

# Create and display the line plot
st.write("#### Air Pollution Levels Over the Years")
fig, ax = plt.subplots(figsize=(10, 5))

# Plot each pollutant
ax.plot(
    yearly_tiantan_df.index, yearly_tiantan_df["PM2.5"], label="PM2.5",
    marker='o'
)
ax.plot(
    yearly_tiantan_df.index, yearly_tiantan_df["PM10"], label="PM10",
    marker='o'
)
ax.plot(
    yearly_tiantan_df.index, yearly_tiantan_df["SO2"], label="SO2",
    marker='o'
)
ax.plot(
    yearly_tiantan_df.index, yearly_tiantan_df["NO2"], label="NO2",
    marker='o'
)
ax.plot(
    yearly_tiantan_df.index, yearly_tiantan_df["O3"], label="O3",
    marker='o'
)

# Customize the plot
ax.set_title("Angka Polutan Udara di Tiantan per Tahun", loc="center", fontsize=16)
ax.set_xlabel("Tahun")
ax.set_ylabel("mg/m³")
ax.tick_params(axis='x', labelsize=10)
ax.tick_params(axis='y', labelsize=10)
ax.legend()

# Display the plot in Streamlit
st.pyplot(fig)

# Create and display the line plot CO
st.write("#### CO Pollution Levels Over the Years")
fig2, ax2 = plt.subplots(figsize=(10, 5))

# Plot CO pollutant
ax2.plot(
    yearly_tiantan_df.index, yearly_tiantan_df["CO"], label="CO",
    marker='o'
)

# Customize the plot
ax2.set_title("Angka Polutan CO di Tiantan per Tahun", loc="center", fontsize=16)
ax2.set_xlabel("Tahun")
ax2.set_ylabel("mg/m³")
ax2.tick_params(axis='x', labelsize=10)
ax2.tick_params(axis='y', labelsize=10)
ax2.legend()

# Display the plot in Streamlit
st.pyplot(fig2)

# hourly
st.subheader("Hourly Air Pollution Levels at Tiantan")

# Group data by hour and calculate the mean for numeric columns
hourly_pm25 = all_df.groupby("hour")['PM2.5'].mean(numeric_only=True)

max_hour = hourly_pm25.idxmax()
max_value = hourly_pm25.max()

colors = ['red' if hour == max_hour else 'gray' for hour in hourly_pm25.index]

# Display the hourly data in Streamlit
st.write("#### Hourly Average Data")
st.dataframe(hourly_pm25)

# Create and display the line plot
st.write("#### Average PM2.5 Levels by Hour Over the Years")
fig, ax = plt.subplots(figsize=(10, 5))

# Plot bar
ax.bar(
    hourly_pm25.index, hourly_pm25.values, label="PM2.5",
    color=colors, edgecolor='black'
)

# Customize the plot
ax.set_title("Average PM2.5 Levels by Hour", loc="center", fontsize=16)
ax.set_xlabel("Hour of the Day")
ax.set_ylabel("PM2.5 Concentration")
ax.tick_params(axis='x', labelsize=10)
ax.tick_params(axis='y', labelsize=10)
ax.grid(axis='y', linestyle='--', alpha=0.7)
ax.text(max_hour, max_value + 2, f'{max_value:.2f}', ha='center', va='bottom', fontsize=12, color='black')
ax.legend()

# Display the plot in Streamlit
st.pyplot(fig)

# Clustering based on PM2.5 levels
st.subheader("Clustering Air Pollution Levels at Tiantan by PM2.5 Levels")

def assign_cluster(pm25):
    if pm25 <= 15:
        return 'Good'
    elif pm25 <= 65:
        return 'Moderate'
    elif pm25 <= 150:
        return 'Unhealthy for Sensitive Groups'
    elif pm25 <= 250:
        return 'Unhealthy'
    elif pm25 <= 300:
        return 'Very Unhealthy'
    else:
        return 'Hazardous'

all_df['Cluster'] = all_df['PM2.5'].apply(assign_cluster)


# Display the sample data in Streamlit
st.write("#### Sample of Clustered Data")
st.dataframe(all_df[["PM2.5","Cluster"]].sample(25))

cluster_counts = all_df.groupby('Cluster')['PM2.5'].count()

# Identify the highest value and its index
max_value = cluster_counts.max()
max_index = cluster_counts.idxmax()

# Assign colors: red for the highest, gray for the rest
colors = ['red' if value == max_value else 'gray' for value in cluster_counts.values]

# Create a horizontal bar chart
fig, ax = plt.subplots(figsize=(8, 6))
ax.barh(cluster_counts.index, cluster_counts.values, color=colors, edgecolor='black')

# Add labels and title
ax.set_xlabel('PM2.5 Count')
ax.set_ylabel('Cluster')
ax.set_title('PM2.5 Count by Cluster')

# Annotate the highest bar
ax.text(max_value, max_index, f'{max_value}', 
        va='center', ha='left', fontsize=10, color='black')

# Adjust layout
plt.tight_layout()

# Display the plot in Streamlit
st.pyplot(fig)


st.caption('Copyright © Mohammad Nashrullah 2024')