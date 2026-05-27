import streamlit as st
# --- PARCHE DE COMPATIBILIDAD (Arregla el error de image_to_url) ---
import streamlit.elements.image as st_image
if not hasattr(st_image, 'image_to_url'):
    st_image.image_to_url = lambda img, width, clamp, channels, format, image_id: "" 
# -----------------------------------------------------------------

from PIL import Image
from streamlit_drawable_canvas import st_canvas
import io
import os
from datetime import datetime
from docx import Document
from docx.shared import Inches

# Configuración estética de la página
st.set_page_config(page_title="CivilReport Pro", page_icon="🏗️", layout="centered")

# Estilo personalizado para mejorar la visibilidad de las pestañas
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] { background-color: #0e1117; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏗️ CivilReport Pro: Control de Obra")
st.info("Plataforma integral de inspección y reportes técnicos.")

# 1. ORGANIZACIÓN POR PESTAÑAS (Esto dividirá tu app como secciones)
tab_inspeccion, tab_calculos, tab_logistica, tab_formalizacion = st.tabs([
    "📸 Inspección y Marcaje", 
    "📐 Calculadoras", 
    "🚁 Control Drone", 
    "✍️ Firma y Envío"
])

# --- PESTAÑA 1: INSPECCIÓN ---
with tab_inspeccion:
    st.subheader("Registro de Observaciones")
    uploaded_file = st.file_uploader("Subir foto de la inspección", type=["png", "jpg", "jpeg"], key="inspeccion_main")

    if uploaded_file:
        image = Image.open(uploaded_file)
        # Ajuste de tamaño para móviles
        canvas_width = 320 
        ratio = canvas_width / image.width
        canvas_height = int(image.height * ratio)

        st.markdown("#### 🖍️ Herramientas de Marcaje")
        drawing_mode = st.radio("Herramienta:", ("Mano alzada", "Flecha / Línea", "Rectángulo", "Círculo"), horizontal=True)
        stroke_color = st.color_picker("Color de marca:", "#FF0000")
        
        mode_map = {"Mano alzada": "freedraw", "Flecha / Línea": "line", "Rectángulo": "rect", "Círculo": "circle"}

        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0)",
            stroke_width=3,
            stroke_color=stroke_color,
            background_image=image.resize((canvas_width, canvas_height)),
            height=canvas_height,
            width=canvas_width,
            drawing_mode=mode_map[drawing_mode],
            key="canvas_site",
        )
        
        st.markdown("---")
        st.subheader("📝 Detalles Técnicos")
        ubicacion = st.text_input("Ubicación exacta (Ej: Eje 4-B, Nivel 5):")
        nota_tecnica = st.text_area("Observaciones encontradas:")
        estado = st.select_slider("Estado de la falla:", options=["🔴 Crítico", "🟡 Observado", "🟢 Subsanado"])
        
        # Guardar en memoria para usarlo en la pestaña de Firma
        st.session_state['report_data'] = {
            "ubicacion": ubicacion,
            "nota": nota_tecnica,
            "estado": estado,
            "canvas": canvas_result.image_data if canvas_result else None,
            "img_orig": image,
            "dims": (canvas_width, canvas_height)
        }

# --- PESTAÑA 2: CALCULADORAS ---
with tab_calculos:
    st.subheader("Ingeniería de Campo")
    calc_type = st.selectbox("Tipo de cálculo:", ["Volumen de Concreto", "Peso de Acero"])
    
    if calc_type == "Volumen de Concreto":
        c1, c2, c3 = st.columns(3)
        l = c1.number_input("Largo (m)", value=1.0)
        a = c2.number_input("Ancho (m)", value=1.0)
        h = c3.number_input("Espesor (m)", value=0.2)
        total = l * a * h
        st.metric("Volumen Total", f"{total:.2f} m³")
        
    elif calc_type == "Peso de Acero":
        diam = st.selectbox("Diámetro (pulg)", ["1/4", "3/8", "1/2", "5/8", "3/4", "1"])
        metros = st.number_input("Metros lineales", value=1.0)
        pesos = {"1/4": 0.25, "3/8": 0.56, "1/2": 0.99, "5/8": 1.55, "3/4": 2.24, "1": 3.97}
        st.metric("Peso Estimado", f"{metros * pesos[diam]:.2f} kg")

# --- PESTAÑA 3: DRONE ---
with tab_logistica:
    st.subheader("Visor de Ortomosaicos")
    st.write("Carga vistas aéreas para control de logística y acopios.")
    drone_file = st.file_uploader("Subir imagen de drone", type=["jpg", "jpeg"], key="drone_view")
    if drone_file:
        st.image(drone_file, use_column_width=True)

# --- PESTAÑA 4: FIRMA Y CIERRE ---
with tab_formalizacion:
    st.subheader("Cierre de Reporte")
    st.write("Firma digital del responsable:")
    
    firma_canvas = st_canvas(
        stroke_width=2,
        stroke_color="#000000",
        background_color="#eeeeee",
        height=150,
        width=320,
        drawing_mode="freedraw",
        key="canvas_firma",
    )
    
    if st.button("💾 Finalizar Reporte Diario"):
        if 'report_data' in st.session_state:
            st.success("¡Datos consolidados! Procediendo a generar PDF/Word...")
            # Aquí se activará la conexión a Google Sheets en el siguiente paso
        else:
            st.warning("Primero debes completar la pestaña de Inspección.")
