import streamlit as st
import google.generativeai as genai

# 1. Configuración de la página para que parezca tu News Hub
st.set_page_config(page_title="News Hub Energía Argentina", page_icon="⚡", layout="wide")

# Estilos para que se vea elegante como querías
st.markdown("""
<style>
    .title {font-size: 3em !important; font-family: 'Serif'; color: #2C3E50;}
    .subtitle {color: #7F8C8D; font-size: 1.2em;}
    .card {padding: 20px; border-radius: 10px; background-color: #f8f9fa; margin-bottom: 10px; border-left: 5px solid #FF4B4B;}
</style>
""", unsafe_allow_html=True)

# 2. Tu Título y Marca Personal
st.markdown('<p class="subtitle">INTELIGENCIA ARTIFICIAL APLICADA AL SECTOR ENERGÉTICO</p>', unsafe_allow_html=True)
st.markdown('<h1 class="title">News Hub Energía Argentina</h1>', unsafe_allow_html=True)
st.caption("by María Eugenia Schiaffino")

st.divider()

# 3. Conexión con el Cerebro (API Key)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("⚠️ Error: No encuentro la API Key. Asegurate de ponerla en los 'Secrets' de Streamlit.")
    st.stop()

# 4. El Cerebro (Configuración del Modelo)
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    system_instruction="""
    Actúas como un Analista Senior de Energía en Argentina (perfil 'News Hub').
    Tu objetivo es resumir, explicar y analizar noticias o temas sobre Vaca Muerta, GNL, YPF y Energía.
    Tu tono es periodístico, estratégico y profesional.
    Cuando el usuario busque un tema, generá un 'Boletín Ejecutivo' simulado con:
    1. Un titular impactante.
    2. El contexto estratégico (El 'Por qué importa').
    3. Los jugadores clave involucrados.
    4. Una conclusión tipo 'Visión de Futuro'.
    """
)

# 5. La Barra de Búsqueda (Como en tu diseño original)
query = st.text_input("🔍 Buscar sobre Vaca Muerta, GNL, YPF...", placeholder="Ej: Últimos avances del RIGI o Exportaciones de GNL")

# Sugerencias rápidas (Botones)
col1, col2, col3, col4 = st.columns(4)
if col1.button("Récord Vaca Muerta"): query = "Récord de producción en Vaca Muerta y su impacto"
if col2.button("Ley RIGI y GNL"): query = "Estado actual del RIGI y proyecto GNL YPF-Petronas"
if col3.button("Inversiones 2025"): query = "Proyección de inversiones en Oil & Gas para 2025"
if col4.button("Oleoducto Vaca Muerta Sur"): query = "Avances estratégicos del Oleoducto Vaca Muerta Sur"

# 6. Generar el Reporte cuando hay búsqueda
if query:
    with st.spinner(f"Analizando inteligencia sobre: {query}..."):
        try:
            response = model.generate_content(query)
            
            # Mostrar resultado con formato bonito
            st.markdown(f"""
            <div class="card">
                <h3>Resultados del Análisis: {query}</h3>
                {response.text}
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Ocurrió un error al procesar: {e}")

# Footer
st.markdown("---")
st.markdown("*News Hub Energía - Powered by Vitto el Erudito AI*")
