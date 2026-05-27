import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import io
import os
from datetime import datetime
from docx import Document
from docx.shared import Inches

st.set_page_config(page_title="CivilReport Pro", page_icon="📝", layout="centered")
st.title("📝 CivilReport Pro: Inspección Visual")
st.markdown("---")

st.subheader("📸 Registro y Edición Fotográfica")
st.write("Sube una foto de la obra y dibuja sobre ella para señalar observaciones (cangrejeras, fisuras, aceros mal dispuestos).")

# 1. Subida de la imagen
uploaded_file = st.file_uploader("Capturar o subir imagen", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file)
        
        # Ajuste automático del tamaño para la pantalla del celular
        canvas_width = 350
        ratio = canvas_width / image.width
        canvas_height = int(image.height * ratio)

        # 2. Herramientas de Marcaje
        st.markdown("### 🖍️ Herramientas de Marcaje")
        col1, col2 = st.columns(2)
        with col1:
            drawing_mode = st.radio("Herramienta:", ("Mano alzada", "Flecha / Línea", "Rectángulo", "Círculo"))
        with col2:
            stroke_color = st.color_picker("Color de la marca:", "#FF0000") # Rojo por defecto
        
        mode_map = {"Mano alzada": "freedraw", "Flecha / Línea": "line", "Rectángulo": "rect", "Círculo": "circle"}

        st.caption("Dibuja directamente sobre la imagen:")
        
        # 3. El Lienzo Interactivo
        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0)", # Fondo transparente
            stroke_width=3,
            stroke_color=stroke_color,
            background_image=image,
            update_streamlit=True,
            height=canvas_height,
            width=canvas_width,
            drawing_mode=mode_map[drawing_mode],
            key="canvas",
        )
        
        # 4. Datos de la Observación (Nueva sección)
        st.markdown("### 📋 Datos de la Observación")
        ubicacion = st.text_input("Ubicación del elemento (Ej. Losa Nivel 2, Columna C-4):")
        nota_foto = st.text_area("Descripción técnica de la observación:")
        
        # Tracking para saber si fue corregida
        estado_obs = st.selectbox("Estado de la observación:", ["🔴 Pendiente", "🟡 En proceso", "🟢 Corregida"])

        # 5. Generación de Archivos y Carpetas
        st.markdown("---")
        if st.button("📄 Generar, Guardar y Descargar Informe"):
            
            # Crear estructura de carpetas por fecha de hoy
            fecha_hoy = datetime.now().strftime("%Y-%m-%d")
            carpeta_destino = os.path.join("Reportes_Obra", fecha_hoy)
            
            if not os.path.exists(carpeta_destino):
                os.makedirs(carpeta_destino)

            # Ensamblamos el documento Word
            doc = Document()
            doc.add_heading('Reporte Técnico de Inspección en Sitio', 0)
            doc.add_paragraph(f"Fecha y hora: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            
            # Procesamos la imagen marcada con validación de seguridad
            if canvas_result.image_data is not None:
                marcada_img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
                imagen_final = Image.alpha_composite(image.convert("RGBA").resize((canvas_width, canvas_height)), marcada_img)
            else:
                imagen_final = image.convert("RGBA").resize((canvas_width, canvas_height))
            
            img_byte_arr = io.BytesIO()
            imagen_final.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            
            doc.add_heading('Registro Fotográfico', level=1)
            doc.add_picture(img_byte_arr, width=Inches(5.0))
            
            doc.add_heading('Detalles de la Inspección:', level=2)
            doc.add_paragraph(f"Ubicación: {ubicacion}")
            doc.add_paragraph(f"Descripción: {nota_foto}")
            doc.add_paragraph(f"Estado Actual: {estado_obs}")
            
            # Guardamos el archivo físicamente en la carpeta por fecha
            nombre_archivo = f"Reporte_{datetime.now().strftime('%H%M%S')}.docx"
            ruta_completa = os.path.join(carpeta_destino, nombre_archivo)
            doc.save(ruta_completa)
            
            # Preparamos el archivo para la descarga web desde el celular
            bio = io.BytesIO()
            doc.save(bio)
            
            st.success(f"¡Documento generado exitosamente! Guardado en: {ruta_completa}")
            st.download_button(
                label="⬇️ Descargar Archivo Word (.docx)",
                data=bio.getvalue(),
                file_name=nombre_archivo,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
            
    except Exception as e:
        st.error(f"Se encontró un error al procesar la imagen: {e}. Intenta con otra fotografía.")
