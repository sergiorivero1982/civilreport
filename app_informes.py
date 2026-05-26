import streamlit as st
from datetime import date
from PIL import Image

st.set_page_config(page_title="CivilReport Pro", page_icon="📝", layout="centered")

st.title("📝 CivilReport Pro: Informes Técnicos de Obra")
st.caption("Sistema de Registro para Residencia y Supervisión de Obra")
st.markdown("---")

# Selección de Rol en la Barra Lateral
st.sidebar.header("⚙️ Configuración del Informe")
rol = st.sidebar.selectbox("Seleccione su Rol en Obra", ["Ingeniero Residente / Encargado", "Supervisor / Fiscal"])

# Información General del Proyecto
st.subheader("🏢 Datos Generales")
col1, col2 = st.columns(2)
with col1:
    proyecto = st.text_input("Nombre del Proyecto / Edificación", value="Condominio Residencial")
    ingeniero = st.text_input("Nombre del Profesional", value="Ing. Sergio Rivero")
with col2:
    fecha_informe = st.date_input("Fecha del Reporte", date.today())
    periodo = st.text_input("Período / Fase del Reporte", value="Semana 12 - Obra Gruesa")

st.markdown("---")

# Secciones dinámicas según el rol seleccionado
if rol == "Ingeniero Residente / Encargado":
    st.subheader("👷 Registro de Actividades y Avances (Residencia)")
    
    actividades = st.text_area("Actividades Realizadas en el Período", 
                               placeholder="- Vaciado de losa reticular en el nivel 3.\n- Armado de columnas del eje B.\n- Encofrado de vigas de borde.")
    
    col_av1, col_av2 = st.columns(2)
    with col_av1:
        avance_fisico = st.number_input("Porcentaje de avance programado (%)", min_value=0.0, max_value=100.0, value=45.0)
    with col_av2:
        avance_real = st.number_input("Porcentaje de avance real ejecutado (%)", min_value=0.0, max_value=100.0, value=43.5)
        
    materiales_log = st.text_area("Control de Materiales / Vaciados del periodo", 
                                  placeholder="Ej: Ingreso de 300 bolsas de cemento IP-40, vaciado de 15 m3 de hormigón f'c=210 kg/cm2 en columnas.")

else:
    st.subheader("🔍 Fiscalización y Control de Calidad (Supervisión)")
    
    estado_obra = st.selectbox("Estado General de la Obra", ["Conforme al Cronograma", "Con Retraso Leve", "Crítico / Obra Paralizada"])
    
    observaciones_tecnicas = st.text_area("Observaciones e Instrucciones de Supervisión", 
                                          placeholder="- Se solicita corregir la separación de estribos en los nudos antes del vaciado.\n- Verificar la estanqueidad del encofrado en vigas de borde.")
    
    aprobacion = st.radio("¿Se aprueba el avance del periodo para planilla?", ["Sí, aprobado", "Aprobado con observaciones", "Rechazado hasta subsanar"])

st.markdown("---")

# Módulo de Registro Fotográfico (Común para ambos roles)
st.subheader("📸 Registro Fotográfico e Inspección Visual")
st.write("Cargue las fotografías tomadas en campo (inspecciones en sitio, seguimiento de vaciados o monitoreo aéreo).")

uploaded_files = st.file_uploader("Subir imágenes de la obra", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

fotos_registro = []

if uploaded_files:
    for i, file in enumerate(uploaded_files):
        st.markdown(f"#### 🖼️ Fotografía N° {i+1}")
        image = Image.open(file)
        st.image(image, caption=file.name, use_container_width=True)
        
        # Anotación específica para cada foto cargada
        nota_foto = st.text_input(f"Anotación / Descripción técnica para la Fotografía N° {i+1}", 
                                  key=f"nota_{i}",
                                  placeholder="Ej: Detalle del armado de fierro en viga banda. Se constata correcto espaciamiento.")
        fotos_registro.append({"imagen": image, "nombre": file.name, "nota": nota_foto})

st.markdown("---")

# Botón para compilar y exportar el informe
if st.button("🚀 Generar Vista de Impresión del Informe"):
    st.success("¡Informe compilado con éxito! Para guardarlo en PDF, presione Ctrl+P (o Compartir > Imprimir en su celular) y seleccione 'Guardar como PDF'.")
    
    # Maquetación del documento final en pantalla
    st.markdown(f"""
    <div style="border: 2px solid #333; padding: 20px; background-color: #fafafa; color: #111; border-radius: 5px;">
        <h2 style="text-align: center; margin-bottom: 0;">REPORTE TÉCNICO DE OBRA</h2>
        <p style="text-align: center; margin-top: 5px; font-weight: bold; color: #555;">Documento de Verificación en Campo</p>
        <hr style="border: 1px solid #333;">
        <table style="width:100%; border-collapse: collapse; margin-bottom: 20px;">
            <tr><td><b>Proyecto:</b> {proyecto}</td><td><b>Fecha:</b> {fecha_informe}</td></tr>
            <tr><td><b>Profesional:</b> {ingeniero}</td><td><b>Rol:</b> {rol}</td></tr>
            <tr><td colspan="2"><b>Período Evaluado:</b> {periodo}</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
    
    if rol == "Ingeniero Residente / Encargado":
        st.markdown(f"""
        <div style="color: #111; background-color: #fafafa; padding: 0 20px 20px 20px; border-left: 2px solid #333; border-right: 2px solid #333;">
            <h3>1. Actividades Ejecutadas</h3>
            <p style="white-space: pre-wrap;">{actividades if actividades else 'No se registraron textos.'}</p>
            <h3>2. Estado del Avance Físico</h3>
            <ul>
                <li>Avance Programado: {avance_fisico}%</li>
                <li>Avance Real Ejecutado: {avance_real}%</li>
            </ul>
            <h3>3. Logística y Materiales</h3>
            <p style="white-space: pre-wrap;">{materiales_log if materiales_log else 'No se registraron datos.'}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="color: #111; background-color: #fafafa; padding: 0 20px 20px 20px; border-left: 2px solid #333; border-right: 2px solid #333;">
            <h3>1. Estado General del Proyecto</h3>
            <p><b>Condición:</b> {estado_obra}</p>
            <h3>2. Observaciones Técnicas e Instrucciones emitidas</h3>
            <p style="white-space: pre-wrap;">{observaciones_tecnicas if observaciones_tecnicas else 'Sin observaciones registradas.'}</p>
            <h3>3. Dictamen del Período</h3>
            <p><b>Estado de Planilla:</b> {aprobacion}</p>
        </div>
        """, unsafe_allow_html=True)
        
    if fotos_registro:
        st.markdown("<div style='color: #111; background-color: #fafafa; padding: 0 20px; border-left: 2px solid #333; border-right: 2px solid #333;'><h3>4. Anexo Fotográfico</h3></div>", unsafe_allow_html=True)
        for idx, f in enumerate(fotos_registro):
            st.image(f["imagen"], use_container_width=True)
            st.markdown(f"<div style='color: #111; background-color: #fafafa; padding: 0 20px 10px 20px; border-left: 2px solid #333; border-right: 2px solid #333;'><p><b>Foto N° {idx+1}:</b> {f['nota'] if f['nota'] else 'Sin descripción.'}</p><hr></div>", unsafe_allow_html=True)
            
    st.markdown("<div style='background-color: #fafafa; padding: 10px 20px; border-bottom: 2px solid #333; border-left: 2px solid #333; border-right: 2px solid #333; text-align: center;'><p style='font-size: 12px; color: #666;'>Generado de forma digital mediante CivilReport Pro.</p></div>", unsafe_allow_html=True)

# Firma de la aplicación en el pie del menú lateral
st.sidebar.markdown("---")
st.sidebar.caption("CivilReport Pro v1.0 - Sucre, Bolivia")
