import streamlit as st
st.title("Mi Dashboard")
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title="Dashboard de Ventas",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard de Análisis de Ventas")
st.markdown("---")

st.sidebar.header("🔍 Filtros")

@st.cache_data
def generar_datos():
    np.random.seed(42)
    fechas = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')

    productos = ['Laptop', 'Mouse', 'Teclado', 'Monitor', 'Webcam']
    regiones = ['Norte', 'Sur', 'Este', 'Oeste', 'Centro']

    datos = []
    for fecha in fechas:
        for _ in range(np.random.randint(5, 15)):
            datos.append({
                'Fecha': fecha,
                'Producto': np.random.choice(productos),
                'Región': np.random.choice(regiones),
                'Cantidad': np.random.randint(1, 10),
                'Precio_Unitario': np.random.randint(20, 500),
            })

    df = pd.DataFrame(datos)
    df['Total'] = df['Cantidad'] * df['Precio_Unitario']
    return df

df = generar_datos()

productos_sel = st.sidebar.multiselect(
    "Productos",
    df['Producto'].unique(),
    default=df['Producto'].unique()
)

regiones_sel = st.sidebar.multiselect(
    "Regiones",
    df['Región'].unique(),
    default=df['Región'].unique()
)

df_f = df[
    df['Producto'].isin(productos_sel) &
    df['Región'].isin(regiones_sel)
]

st.header("📈 Métricas")

col1, col2, col3 = st.columns(3)

col1.metric("Ventas Totales", f"${df_f['Total'].sum():,.0f}")
col2.metric("Ticket Promedio", f"${df_f['Total'].mean():,.0f}")
col3.metric("Productos Vendidos", int(df_f['Cantidad'].sum()))

st.markdown("---")

st.subheader("📊 Ventas por Producto")
ventas_prod = df_f.groupby('Producto')['Total'].sum().reset_index()
fig = px.bar(ventas_prod, x='Producto', y='Total')
st.plotly_chart(fig, use_container_width=True)

st.subheader("📋 Datos")
st.dataframe(df_f.head(50), use_container_width=True)

