import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

st.set_page_config(page_title="Superstore Dashboard", layout="wide")

BASE_DIR = Path(__file__).parent.parent
df = pd.read_csv(BASE_DIR / 'data' / 'superstore.csv', encoding='latin-1')
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Year'] = df['Order Date'].dt.year


st.title("Dashboard de Ventas — Superstore")

st.sidebar.header("Filtros")
years = sorted(df['Year'].unique())
selected_years = st.sidebar.multiselect("Año", years, default=years)
categories = sorted(df['Category'].unique())
selected_cats = st.sidebar.multiselect("Categoría", categories, default=categories)

df_filtered = df[
    (df['Year'].isin(selected_years)) &
    (df['Category'].isin(selected_cats))
]

col1, col2, col3 = st.columns(3)
col1.metric("Ventas totales", f"${df_filtered['Sales'].sum():,.0f}")
col2.metric("Profit total", f"${df_filtered['Profit'].sum():,.0f}")
col3.metric("Nº transacciones", f"{len(df_filtered):,}")

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Profit por categoría")
    fig, ax = plt.subplots(figsize=(8, 4))
    profit_cat = df_filtered.groupby('Category')['Profit'].sum().sort_values()
    colors = ['red' if x < 0 else 'steelblue' for x in profit_cat]
    profit_cat.plot(kind='barh', ax=ax, color=colors)
    ax.axvline(x=0, color='black', linewidth=0.8)
    st.pyplot(fig)

with col_right:
    st.subheader("Relación descuento y profit")
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    ax2.scatter(df_filtered['Discount'], df_filtered['Profit'], alpha=0.3)
    ax2.axhline(y=0, color='red', linestyle='--')
    ax2.set_xlabel('Descuento')
    ax2.set_ylabel('Profit')
    st.pyplot(fig2)

st.subheader("Profit por subcategoría")
fig3, ax3 = plt.subplots(figsize=(10, 4))
profit_subcat = df_filtered.groupby('Sub-Category')['Profit'].sum().sort_values()
colors3 = ['red' if x < 0 else 'steelblue' for x in profit_subcat]
profit_subcat.plot(kind='barh', ax=ax3, color=colors3)
ax3.axvline(x=0, color='black', linewidth=0.8)
st.pyplot(fig3)