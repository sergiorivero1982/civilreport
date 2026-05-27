import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import io
from docx import Document
from docx.shared import Inches

# Configuración estética de la página
st.set_page_config(page_title="CivilReport Pro", page_icon="🏗️", layout="centered")

st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #f0f2f6; border-radius: 4px 4px 0px 0px; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background-color: #0e1117; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏗️ CivilReport Pro: Control de Obra")
st.info("Plataforma integral de inspección y reportes técnicos.")

tab_inspeccion, tab_calculos, tab_logistica, tab_formalizacion = st.tabs([
    "📸 Inspección y Marcaje", "📐 Calculadoras", "🚁 Control Drone", "✍️ Firma y Envío"
])

# --- PESTAÑA 1: INSPECCIÓN ---
with tab_inspeccion:
    st.subheader("Registro de Observaciones")
    uploaded_file = st.file_uploader("Subir foto de la inspección", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        
        # Ajuste de tamaño
        canvas_width = 350 
        ratio = canvas_width / image.width
        canvas_height = int(image.height * ratio)

        st.markdown("#### 🖍️ Herramientas de Marcaje")
        drawing_mode = st.radio("Herramienta:", ("Mano alzada", "Flecha / Línea", "Rectángulo", "Círculo"), horizontal=True)
        stroke_color = st.color_picker("Color de marca:", "#FF0000")
        mode_map = {"Mano alzada": "freedraw", "Flecha / Línea": "line", "Rectángulo": "rect", "Círculo": "circle"}

        # EL LIENZO - Aquí se carga la imagen de fondo directamente
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
