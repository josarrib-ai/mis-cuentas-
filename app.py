import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# Configuración de página móvil
st.set_page_config(page_title="Mi App Personal", page_icon="📱", layout="centered")

# Estilos CSS personalizados para apariencia de App Móvil
st.markdown("""
<style>
    /* Estilos globales */
    .stApp { background-color: #F8F9FA; }
    
    /* Header principal */
    .app-header {
        background: linear-gradient(135deg, #1B4D3E 0%, #2D6A4F 100%);
        padding: 20px 15px;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    .app-title { font-size: 22px; font-weight: 700; margin: 0; }
    .app-subtitle { font-size: 13px; opacity: 0.9; margin-top: 4px; }
    
    /* Tarjetas KPI elegantes */
    .kpi-container { display: flex; gap: 10px; margin-bottom: 20px; }
    .kpi-card {
        flex: 1;
        background: white;
        padding: 14px 10px;
        border-radius: 14px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        border: 1px solid #E9ECEF;
    }
    .kpi-label { font-size: 11px; font-weight: 600; color: #6C757D; text-transform: uppercase; letter-spacing: 0.5px; }
    .kpi-value { font-size: 18px; font-weight: 700; margin-top: 4px; }
    
    /* Botones y formularios */
    .stButton>button {
        width: 100%;
        background-color: #1B4D3E;
        color: white;
        border-radius: 12px;
        padding: 10px 16px;
        font-weight: 600;
        border: none;
        box-shadow: 0 2px 6px rgba(27,77,62,0.2);
    }
    .stButton>button:hover { background-color: #2D6A4F; color: white; }
    
    /* Tarjeta de elemento de lista */
    .list-card {
        background: white;
        padding: 12px 16px;
        border-radius: 12px;
        margin-bottom: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.03);
        border-left: 4px solid #1B4D3E;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
</style>
""", unsafe_allow_html=True)

# Encabezado móvil
st.markdown("""
<div class='app-header'>
    <div class='app-title'>📲 Mi Panel de Control</div>
    <div class='app-subtitle'>Finanzas, Garantías, Deporte y Gestión</div>
</div>
""", unsafe_allow_html=True)

# Navegación principal en la parte superior (Pestañas estilo App)
seccion = st.option_menu = st.selectbox(
    "Navega por tus módulos:",
    ["💳 Finanzas & Gastos", "🧾 Tickets y Garantías", "🏃 Carreras & Strava", "🪴 Plantas & Jardín", "📐 Medidas del Hogar", "🎄 Planificador Navidad"],
    index=0
)

st.write("")

if "Finanzas" in seccion:
    if 'ingresos' not in st.session_state:
        st.session_state.ingresos = pd.DataFrame([
            {"Fuente": "Nómina Principal", "Monto (€)": 1800.0},
            {"Fuente": "Incentivos / Bonos", "Monto (€)": 150.0}
        ])
    if 'gastos' not in st.session_state:
        st.session_state.gastos = pd.DataFrame([
            {"Categoría": "Hipotecas / Alquiler", "Presupuesto (€)": 800.0, "Gasto Real (€)": 800.0},
            {"Categoría": "Luz, Agua y Gas", "Presupuesto (€)": 150.0, "Gasto Real (€)": 135.0},
            {"Categoría": "Supermercado", "Presupuesto (€)": 450.0, "Gasto Real (€)": 520.0},
            {"Categoría": "Restauración y Ocio", "Presupuesto (€)": 200.0, "Gasto Real (€)": 310.0},
            {"Categoría": "Combustible / Transporte", "Presupuesto (€)": 120.0, "Gasto Real (€)": 140.0}
        ])

    tot_ingresos = st.session_state.ingresos["Monto (€)"].sum()
    tot_gastos = st.session_state.gastos["Gasto Real (€)"].sum()
    balance_neto = tot_ingresos - tot_gastos

    # KPIs superiores
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Ingresos</div><div class='kpi-value' style='color:#2A9D8F;'>{tot_ingresos:,.0f} €</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Gastos</div><div class='kpi-value' style='color:#E76F51;'>{tot_gastos:,.0f} €</div></div>", unsafe_allow_html=True)
    with col3:
        color_b = "#2A9D8F" if balance_neto >= 0 else "#E76F51"
        st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Ahorro</div><div class='kpi-value' style='color:{color_b};'>{balance_neto:,.0f} €</div></div>", unsafe_allow_html=True)

    st.write("")
    
    # Formulario desplegable
    with st.expander("➕ **Añadir un gasto rápido**"):
        with st.form("form_gasto_movil"):
            cat = st.text_input("Categoría / Concepto", placeholder="Ej: Compra supermercado")
            pres = st.number_input("Presupuesto (€)", value=50.0, step=10.0)
            real = st.number_input("Gasto Real (€)", value=0.0, step=5.0)
            if st.form_submit_button("Guardar Gasto"):
                nuevo = pd.DataFrame([{"Categoría": cat, "Presupuesto (€)": pres, "Gasto Real (€)": real}])
                st.session_state.gastos = pd.concat([st.session_state.gastos, nuevo], ignore_index=True)
                st.success("¡Gasto registrado!")
                st.rerun()

    # Pestañas de detalle
    tab1, tab2 = st.tabs(["📊 Distribución de Gastos", "📋 Desglose Detallado"])
    with tab1:
        fig = px.pie(st.session_state.gastos, names="Categoría", values="Gasto Real (€)", hole=0.5,
                     color_discrete_sequence=px.colors.qualitative.Bold)
        fig.update_layout(margin=dict(t=10, b=10, l=10, r=10), showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
        
    with tab2:
        for idx, row in st.session_state.gastos.iterrows():
            st.markdown(f"""
            <div class='list-card'>
                <div>
                    <strong>{row['Categoría']}</strong><br>
                    <small style='color:#6C757D;'>Presupuesto: {row['Presupuesto (€)']} €</small>
                </div>
                <div style='text-align:right; font-weight:bold; font-size:16px; color:#1B4D3E;'>
                    {row['Gasto Real (€)']} €
                </div>
            </div>
            """, unsafe_allow_html=True)

elif "Tickets" in seccion:
    st.subheader("🧾 Tickets & Garantías Activas")
    with st.expander("➕ **Registrar nuevo ticket**"):
        prod = st.text_input("Producto", "Ej: Televisor")
        tienda = st.text_input("Tienda", "Ej: MediaMarkt")
        precio = st.number_input("Importe (€)", value=100.0)
        f_compra = st.date_input("Fecha de compra", datetime.now())
        anios = st.selectbox("Años de garantía", [1, 2, 3, 5], index=2)
        if st.button("Guardar Ticket"):
            st.success("¡Ticket guardado correctamente!")

    st.markdown("""
    <div class='list-card' style='border-left-color: #2A9D8F;'>
        <div>
            <strong>Televisor Salón 55''</strong><br>
            <small style='color:#6C757D;'>MediaMarkt • Vence: 15/11/2027</small>
        </div>
        <div><span style='background:#E6F4EA; color:#137333; padding:4px 8px; border-radius:8px; font-size:12px; font-weight:bold;'>En Garantía</span></div>
    </div>
    <div class='list-card' style='border-left-color: #E76F51;'>
        <div>
            <strong>Zapatillas Running</strong><br>
            <small style='color:#6C757D;'>Decathlon • Vence: 31/10/2026</small>
        </div>
        <div><span style='background:#FCE8E6; color:#C5221F; padding:4px 8px; border-radius:8px; font-size:12px; font-weight:bold;'>Próximo Vencimiento</span></div>
    </div>
    """, unsafe_allow_html=True)

elif "Strava" in seccion:
    st.subheader("🏃 Deporte & Carreras")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total KM 2026", "18.5 km", "+4.2 km")
    with col2:
        st.metric("Objetivo Anual", "230 km", "8% conseguido")
        
    df_st = pd.DataFrame({"Año": [2022, 2023, 2024, 2025, 2026], "KM": [105.4, 126.8, 117.3, 30.4, 18.5]})
    fig_st = px.bar(df_st, x="Año", y="KM", title="Evolución de Kilómetros Anuales", color_discrete_sequence=["#1B4D3E"])
    st.plotly_chart(fig_st, use_container_width=True)

elif "Plantas" in seccion:
    st.subheader("🪴 Jardín & Plantas")
    st.markdown("""
    <div class='list-card'>
        <div><strong>Jazmín</strong><br><small style='color:#6C757D;'>Plantado: 15/07/2024</small></div>
        <div style='font-weight:bold;'>9.75 €</div>
    </div>
    <div class='list-card'>
        <div><strong>Esqueje Buganvilla</strong><br><small style='color:#6C757D;'>Plantado: 15/07/2024</small></div>
        <div style='font-weight:bold;'>0.00 €</div>
    </div>
    """, unsafe_allow_html=True)

elif "Medidas" in seccion:
    st.subheader("📐 Medidas del Hogar")
    st.markdown("""
    <div class='list-card'>
        <div><strong>Valla Mogro</strong><br><small style='color:#6C757D;'>Dimensiones: 0.80 x 1.00 m</small></div>
    </div>
    <div class='list-card'>
        <div><strong>Cajeado Trasera Sofá</strong><br><small style='color:#6C757D;'>Dimensiones: 2.05 x 0.65 x 0.15 m</small></div>
    </div>
    """, unsafe_allow_html=True)

elif "Navidad" in seccion:
    st.subheader("🎄 Planificador Nochebuena")
    st.markdown("""
    <div class='list-card'>
        <div><strong>Entrantes</strong><br><small style='color:#6C757D;'>Langostinos cocidos, Hojaldritos variados</small></div>
    </div>
    <div class='list-card'>
        <div><strong>Plato Principal</strong><br><small style='color:#6C757D;'>Merluza en salsa verde con almejas</small></div>
    </div>
    <div class='list-card'>
        <div><strong>Postre</strong><br><small style='color:#6C757D;'>Tronco de Navidad (Chocolate/Tiramisú)</small></div>
    </div>
    """, unsafe_allow_html=True)
