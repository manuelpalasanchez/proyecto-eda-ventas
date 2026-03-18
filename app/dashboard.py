import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from tabs import tab_resumen, tab_problemas, tab_evolucion
st.set_page_config(
    page_title="Superstore Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

@st.cache_data
def load_data():
    BASE_DIR = Path(__file__).parent.parent
    df = pd.read_csv(BASE_DIR / 'data' / 'superstore.csv', encoding='latin-1')
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Year'] = df['Order Date'].dt.year
    df['Month'] = df['Order Date'].dt.month
    return df

df = load_data()

st.title("📊 Superstore Sales Dashboard")
st.markdown("""
Análisis exploratorio de ventas de una gran superficie estadounidense (2014–2017).  
Identifica qué categorías, productos y prácticas comerciales generan beneficios y cuáles generan pérdidas.""")

st.sidebar.title("Filtros")
st.sidebar.markdown("Filtra los datos para explorar segmentos específicos.")

years = sorted(df['Year'].unique())
selected_years = st.sidebar.multiselect("Año", years, default=years)

categories = sorted(df['Category'].unique())
selected_cats = st.sidebar.multiselect("Categoría", categories, default=categories)

regions = sorted(df['Region'].unique())
selected_regions = st.sidebar.multiselect("Región", regions, default=regions)


df_filtrado = df[
    (df['Year'].isin(selected_years)) &
    (df['Category'].isin(selected_cats)) &
    (df['Region'].isin(selected_regions))
]


if df_filtrado.empty:
    st.warning("No hay datos para los filtros seleccionados.")
    st.stop()


k1, k2, k3, k4 = st.columns(4)
k1.metric("Ventas totales", f"${df_filtrado['Sales'].sum():,.0f}")
k2.metric("Profit total", f"${df_filtrado['Profit'].sum():,.0f}")
k3.metric("Transacciones", f"{len(df_filtrado):,}")
k4.metric("Profit medio", f"${df_filtrado['Profit'].mean():,.1f}")


tab1, tab2, tab3 = st.tabs(["Resumen general", "Problemas detectados", "Evolución temporal"])

with tab1:
    tab_resumen.render(df_filtrado)
with tab2:
    tab_problemas.render(df_filtrado)
with tab3:
    tab_evolucion.render(df_filtrado)