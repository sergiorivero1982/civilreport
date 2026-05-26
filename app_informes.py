import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import io
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
    image = Image.open(uploaded_file)
    
    # Ajuste automático del tamaño para la pantalla del celular
    canvas_width = 350
    ratio = canvas_width / image.width
    canvas_height = int(image.height * ratio)

    # 2. Herramientas estilo "ConstruccionPro"
    st.markdown("### 🖍️ Herramientas de Marcaje")
    drawing_mode = st.radio("Herramienta:", ("Mano alzada", "Flecha / Línea", "Rectángulo", "Círculo"), horizontal=True)
    stroke_color = st.color_picker("Color de la marca:", "#FF0000") # Rojo por defecto para resaltar
    
    mode_map = {"Mano alzada": "freedraw", "Flecha / Línea": "line", "Rectángulo": "rect", "Círculo": "circle"}

    st.caption("Dibuja directamente sobre la imagen:")
    
    # 3. El Lienzo Interactivo
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0)", # Fondo transparente para ver la foto
        stroke_width=3,
        stroke_color=stroke_color,
        background_image=image,
        update_streamlit=True,
        height=canvas_height,
        width=canvas_width,
        drawing_mode=mode_map[drawing_mode],
        key="canvas",
    )
    
    nota_foto = st.text_area("Descripción técnica de la observación:")

    # 4. Generación Real de Archivos (No solo impresión web)
    st.markdown("---")
    if st.button("📄 Generar y Descargar Informe en Word"):
        # Ensamblamos el documento
        doc = Document()
        doc.add_heading('Reporte Técnico de Inspección en Sitio', 0)
        
        # Procesamos la imagen marcada
        if canvas_result.image_data is not None:
            # Convertimos el array del canvas a imagen png
            marcada_img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
            
            # Combinamos la foto original con las marcas
            imagen_final = Image.alpha_composite(image.convert("RGBA").resize((canvas_width, canvas_height)), marcada_img)
            
            img_byte_arr = io.BytesIO()
            imagen_final.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            
            doc.add_heading('Registro Fotográfico', level=1)
            doc.add_picture(img_byte_arr, width=Inches(5.0))
        
        doc.add_heading('Observaciones e Instrucciones:', level=2)
        doc.add_paragraph(nota_foto)
        
        # Preparamos la descarga
        bio = io.BytesIO()
        doc.save(bio)
        
        st.success("¡Documento generado exitosamente!")
        st.download_button(
            label="⬇️ Guardar Archivo Word (.docx)",
            data=bio.getvalue(),
            file_name="Reporte_Inspeccion_Diaria.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
