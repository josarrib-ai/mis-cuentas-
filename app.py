import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="App Control Personal & Finanzas", page_icon="📱", layout="wide")

st.markdown("""
<style>
    .main-title { font-size: 26px; font-weight: bold; color: #1B4D3E; margin-bottom: 15px; }
    .kpi-card-green { background-color: #E6F4EA; padding: 15px; border-radius: 12px; text-align: center; border: 1px solid #C6DAFC; }
    .kpi-card-red { background-color: #FCE8E6; padding: 15px; border-radius: 12px; text-align: center; border: 1px solid #FAD2CF; }
    .kpi-card-blue { background-color: #E8F0FE; padding: 15px; border-radius: 12px; text-align: center; border: 1px solid #D2E3FC; }
    .kpi-title { font-size: 13px; font-weight: bold; color: #5F6368; }
    .kpi-num { font-size: 22px; font-weight: bold; margin-top: 5px; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.sidebar.title("📲 Control Personal")
seccion = st.sidebar.radio("Selecciona una opción:", ["💳 Control de Finanzas", "🧾 Tickets y Garantías", "🏃 Carreras & Strava", "🪴 Plantas & Jardín", "📐 Medidas del Hogar", "🎄 Planificador Navidad"])

if seccion == "💳 Control de Finanzas":
    st.markdown("<div class='main-title'>💳 Balance Mensual, Gastos e Ingresos</div>", unsafe_allow_html=True)
    if 'ingresos' not in st.session_state:
        st.session_state.ingresos = pd.DataFrame([
            {"Fuente": "Nómina Principal", "Tipo": "Fijo", "Monto (€)": 1800.0, "Notas": "Cobro fin de mes"},
            {"Fuente": "Incentivos / Bonos", "Tipo": "Variable", "Monto (€)": 150.0, "Notas": "Comisiones"}
        ])
    if 'gastos' not in st.session_state:
        st.session_state.gastos = pd.DataFrame([
            {"Categoría": "Hipotecas / Alquiler", "Tipo": "Fijo", "Presupuesto (€)": 800.0, "Gasto Real (€)": 800.0},
            {"Categoría": "Luz, Agua y Gas", "Tipo": "Fijo", "Presupuesto (€)": 150.0, "Gasto Real (€)": 135.0},
            {"Categoría": "Supermercado", "Tipo": "Variable", "Presupuesto (€)": 450.0, "Gasto Real (€)": 520.0},
            {"Categoría": "Restauración y Ocio", "Tipo": "Variable", "Presupuesto (€)": 200.0, "Gasto Real (€)": 310.0},
            {"Categoría": "Combustible / Transporte", "Tipo": "Variable", "Presupuesto (€)": 120.0, "Gasto Real (€)": 140.0}
        ])

    tot_ingresos = st.session_state.ingresos["Monto (€)"].sum()
    tot_gastos = st.session_state.gastos["Gasto Real (€)"].sum()
    balance_neto = tot_ingresos - tot_gastos

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"<div class='kpi-card-blue'><div class='kpi-title'>INGRESOS MES</div><div class='kpi-num' style='color:#1A73E8;'>{tot_ingresos:,.2f} €</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='kpi-card-red'><div class='kpi-title'>GASTOS MES</div><div class='kpi-num' style='color:#C5221F;'>{tot_gastos:,.2f} €</div></div>", unsafe_allow_html=True)
    with c3:
        color_bal = "#137333" if balance_neto >= 0 else "#C5221F"
        st.markdown(f"<div class='kpi-card-green'><div class='kpi-title'>AHORRO NETO</div><div class='kpi-num' style='color:{color_bal};'>{balance_neto:,.2f} €</div></div>", unsafe_allow_html=True)

    st.write("---")
    with st.expander("➕ **Añadir Nuevo Gasto Rápidamente**", expanded=False):
        with st.form("form_gasto"):
            cat = st.text_input("Categoría / Concepto", "Ej: Supermercado Mercadona")
            tipo = st.selectbox("Tipo de Gasto", ["Variable", "Fijo"])
            pres = st.number_input("Presupuesto Estimado (€)", min_value=0.0, value=100.0)
            real = st.number_input("Gasto Real Pagado (€)", min_value=0.0, value=0.0)
            btn_save = st.form_submit_button("💾 Guardar Gasto")
            if btn_save:
                nuevo_g = pd.DataFrame([{"Categoría": cat, "Tipo": tipo, "Presupuesto (€)": pres, "Gasto Real (€)": real}])
                st.session_state.gastos = pd.concat([st.session_state.gastos, nuevo_g], ignore_index=True)
                st.success("¡Gasto guardado correctamente!")
                st.rerun()

    tab_g, tab_i = st.tabs(["📊 Presupuesto & Gastos", "💵 Ingresos"])
    with tab_g:
        df_g = st.session_state.gastos.copy()
        df_g["Diferencia (€)"] = df_g["Presupuesto (€)"] - df_g["Gasto Real (€)"]
        df_g["Estado"] = df_g["Diferencia (€)"].apply(lambda x: "⚠️ Excedido" if x < 0 else "✅ Ok")
        st.dataframe(df_g, use_container_width=True)
        
        col_chart1, col_chart2 = st.columns(2)
        with col_chart1:
            fig_bar = px.bar(df_g, x="Categoría", y=["Presupuesto (€)", "Gasto Real (€)"], barmode="group",
                             title="Presupuesto vs Gasto Real", color_discrete_sequence=["#1B4D3E", "#9A031E"])
            st.plotly_chart(fig_bar, use_container_width=True)
        with col_chart2:
            fig_pie = px.pie(df_g, names="Categoría", values="Gasto Real (€)", title="Distribución del Gasto",
                             color_discrete_sequence=px.colors.sequential.Darkmint)
            st.plotly_chart(fig_pie, use_container_width=True)

    with tab_i:
        st.dataframe(st.session_state.ingresos, use_container_width=True)

elif seccion == "🧾 Tickets y Garantías":
    st.markdown("<div class='main-title'>🧾 Gestor de Tickets & Vencimiento de Garantías</div>", unsafe_allow_html=True)
    if 'tickets' not in st.session_state:
        st.session_state.tickets = [
            {"Producto": "Televisor Salón 55''", "Tienda": "MediaMarkt", "Precio (€)": 499.0, "Fecha Compra": "2024-11-15", "Fecha Vencimiento": "2027-11-15", "Días Restantes": 394, "Estado": "✅ En Garantía"},
            {"Producto": "Zapatillas Running", "Tienda": "Decathlon", "Precio (€)": 89.9, "Fecha Compra": "2024-10-01", "Fecha Vencimiento": "2026-10-31", "Días Restantes": 14, "Estado": "⚠️ Próximo a Vencer"}
        ]
    with st.expander("➕ **Subir / Registrar Nuevo Ticket**", expanded=True):
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            prod = st.text_input("Producto / Compras", "Ej: Frigorífico Bosch")
            tienda = st.text_input("Establecimiento / Tienda", "Ej: El Corte Inglés")
            precio = st.number_input("Precio (€)", value=650.0)
        with col_t2:
            f_compra = st.date_input("Fecha de Compra", datetime.now())
            anios_g = st.selectbox("Años de Garantía", [1, 2, 3, 5], index=2)
            archivo_ticket = st.file_uploader("Adjuntar foto del ticket (JPG, PNG o PDF)", type=["jpg", "png", "pdf"])
            
        if st.button("💾 Guardar Ticket & Generar Alerta"):
            f_venc = f_compra + timedelta(days=365 * anios_g)
            dias_r = (f_venc - datetime.now().date()).days
            est = "⚠️ Próximo a Vencer" if dias_r < 30 else ("🔴 Vencida" if dias_r < 0 else "✅ En Garantía")
            nuevo_ticket = {"Producto": prod, "Tienda": tienda, "Precio (€)": precio, "Fecha Compra": f_compra.strftime("%Y-%m-%d"), "Fecha Vencimiento": f_venc.strftime("%Y-%m-%d"), "Días Restantes": dias_r, "Estado": est}
            st.session_state.tickets.append(nuevo_ticket)
            st.success(f"¡Ticket para '{prod}' guardado!")
            st.rerun()

    st.write("---")
    st.subheader("📋 Mis Garantías Registradas")
    st.dataframe(pd.DataFrame(st.session_state.tickets), use_container_width=True)

elif seccion == "🏃 Carreras & Strava":
    st.markdown("<div class='main-title'>🏃 Registro de Carreras & Conexión Strava</div>", unsafe_allow_html=True)
    col_s1, col_s2 = st.columns([1, 2])
    with col_s1:
        st.subheader("📡 Sincronizar Strava")
        if st.button("🔄 Conectar Cuenta de Strava (API)"):
            st.success("¡Sincronización automática con Strava activada!")
        uploaded_gpx = st.file_uploader("Subir archivo .GPX o .CSV de Strava", type=["gpx", "csv"])
    with col_s2:
        st.subheader("📊 Historial de Kilómetros vs Objetivo")
        df_strava = pd.DataFrame({"Año": [2022, 2023, 2024, 2025, 2026], "KM Recorridos": [105.4, 126.8, 117.3, 30.4, 18.5], "Objetivo KM": [230.0, 230.0, 230.0, 230.0, 230.0]})
        fig_st = px.bar(df_strava, x="Año", y=["KM Recorridos", "Objetivo KM"], barmode="group", color_discrete_sequence=["#1B4D3E", "#E9C46A"], title="Progresión Anual de Carrera (KM)")
        st.plotly_chart(fig_st, use_container_width=True)

elif seccion == "🪴 Plantas & Jardín":
    st.markdown("<div class='main-title'>🪴 Catálogo de Plantas y Jardín</div>", unsafe_allow_html=True)
    st.dataframe(pd.DataFrame([
        {"Planta": "Jazmín", "Precio (€)": 9.75, "Fecha Plantado": "2024-07-15", "Estado / Foto": "Floración activa"},
        {"Planta": "Esqueje Buganvilla", "Precio (€)": 0.0, "Fecha Plantado": "2024-07-15", "Estado / Foto": "En crecimiento"},
        {"Planta": "Esqueje Jade", "Precio (€)": 0.0, "Fecha Plantado": "2024-08-15", "Estado / Foto": "Sano"}
    ]), use_container_width=True)

elif seccion == "📐 Medidas del Hogar":
    st.markdown("<div class='main-title'>📐 Medidas y Reformas del Hogar</div>", unsafe_allow_html=True)
    st.dataframe(pd.DataFrame([
        {"Elemento / Zona": "Salón", "Ancho (m)": "-", "Largo (m)": "-", "Observaciones": "Ver plano principal"},
        {"Elemento / Zona": "Valla Mogro", "Ancho (m)": "0.80", "Largo (m)": "1.00", "Observaciones": "Restauración de madera"},
        {"Elemento / Zona": "Suelo Barbacoa", "Ancho (m)": "-", "Largo (m)": "-", "Observaciones": "Azulejo exterior"}
    ]), use_container_width=True)

elif seccion == "🎄 Planificador Navidad":
    st.markdown("<div class='main-title'>🎄 Planificador de Menús y Eventos</div>", unsafe_allow_html=True)
    st.dataframe(pd.DataFrame([
        {"Categoría": "Aperitivos", "Plato / Menú": "Langostinos cocidos, Hojaldritos variados", "Notas": "Salmón, queso, sobrasada"},
        {"Categoría": "Principal", "Plato / Menú": "Merluza en salsa verde con almejas", "Notas": "Encargar en pescadería"},
        {"Categoría": "Postre", "Plato / Menú": "Tronco de Navidad", "Notas": "Chocolate o Tiramisú"}
    ]), use_container_width=True)
