import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import io

# 1. Configuración de la página
st.set_page_config(page_title="CivilReport Pro", page_icon="🏗️", layout="centered")

st.title("🏗️ CivilReport Pro: Control de Obra")
st.info("Plataforma integral de inspección y reportes técnicos.")

# 2. Creación de las Pestañas
tab_inspeccion, tab_calculos, tab_logistica, tab_firma = st.tabs([
    "📸 Inspección", "📐 Calculadoras", "🚁 Vistas Aéreas", "✍️ Firma y Cierre"
])

# ==========================================
# PESTAÑA 1: INSPECCIÓN
# ==========================================
with tab_inspeccion:
    st.subheader("Registro Fotográfico y Marcaje")
    uploaded_file = st.file_uploader("Subir foto de la inspección", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        # SOLUCIÓN CLAVE: Convertir la imagen a RGBA para garantizar compatibilidad con fotos de WhatsApp
        image = Image.open(uploaded_file).convert("RGBA")
        
        # Ajustamos el tamaño para la pantalla
        canvas_width = 350
        ratio = canvas_width / image.width
        canvas_height = int(image.height * ratio)

        # Redimensionar la imagen de fondo
        bg_image = image.resize((canvas_width, canvas_height))

        st.markdown("#### 🖍️ Herramientas de Marcaje")
        col1, col2 = st.columns(2)
        with col1:
            drawing_mode = st.radio("Herramienta:", ("Mano alzada", "Línea", "Rectángulo", "Círculo"))
        with col2:
            stroke_color = st.color_picker("Color de la marca:", "#FF0000")
            
        mode_map = {"Mano alzada": "freedraw", "Línea": "line", "Rectángulo": "rect", "Círculo": "circle"}

        st.caption("Dibuja directamente sobre la imagen:")
        
        # El lienzo interactivo
        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0)", # Transparente para ver la foto de fondo
            stroke_width=3,
            stroke_color=stroke_color,
            background_image=bg_image,
            update_streamlit=True,
            height=canvas_height,
            width=canvas_width,
            drawing_mode=mode_map[drawing_mode],
            key="canvas_inspeccion",
        )
        
        st.markdown("### 📋 Datos de la Observación")
        ubicacion = st.text_input("Ubicación del elemento (Ej. Losa Nivel 2):")
        nota_foto = st.text_area("Descripción técnica:")
        estado_obs = st.selectbox("Estado:", ["🔴 Pendiente", "🟡 En proceso", "🟢 Corregida"])

# ==========================================
# PESTAÑA 2: CALCULADORAS
# ==========================================
with tab_calculos:
    st.subheader("Cálculo Rápido de Hormigón")
    col_l, col_a, col_h = st.columns(3)
    largo = col_l.number_input("Largo (m)", value=0.0)
    ancho = col_a.number_input("Ancho (m)", value=0.0)
    alto = col_h.number_input("Espesor (m)", value=0.0)
    
    vol_neto = largo * ancho * alto
    st.success(f"**Volumen Neto:** {vol_neto:.2f} m³")

    st.markdown("---")
    st.subheader("Estimador de Peso de Acero")
    diametro = st.selectbox("Diámetro (mm)", [6, 8, 10, 12, 16, 20, 25])
    longitud = st.number_input("Longitud total (m)", value=0.0)
    pesos_acero = {6: 0.222, 8: 0.395, 10: 0.617, 12: 0.888, 16: 1.578, 20: 2.466, 25: 3.853}
    st.info(f"**Peso estimado:** {(longitud * pesos_acero[diametro]):.2f} kg")

# ==========================================
# PESTAÑA 3: VISTAS AÉREAS
# ==========================================
with tab_logistica:
    st.subheader("Control Logístico Aéreo")
    vuelo_file = st.file_uploader("Subir ortomosaico o vista drone", type=["jpg", "jpeg"], key="drone")
    if vuelo_file is not None:
        st.image(Image.open(vuelo_file), caption="Vista del terreno", use_column_width=True)

# ==========================================
# PESTAÑA 4: FIRMA
# ==========================================
with tab_firma:
    st.subheader("Firma del Responsable")
    firma_result = st_canvas(
        fill_color="rgba(255, 255, 255, 1)",
        stroke_width=2,
        stroke_color="#000000",
        background_color="#FFFFFF",
        height=150,
        width=350,
        drawing_mode="freedraw",
        key="canvas_firma",
    )
    if st.button("Finalizar Reporte"):
        st.success("¡Datos guardados en memoria correctamente!")
