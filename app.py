import streamlit as st
import google.generativeai as genai
import os

# 1. Configuración de la página (La "Fachada")
st.set_page_config(page_title="Vitto: Inteligencia Oil & Gas", page_icon="🛢️")

st.title("🛢️ Vitto el Erudito: Edición Vaca Muerta")
st.write("Preguntame sobre RIGI, GNL, Soft Skills o estrategias para el Upstream.")

# 2. Conexión con el Cerebro (La API Key)
# Esto busca la llave en los "secretos" de la nube para que nadie te la robe.
api_key = st.secrets["GOOGLE_API_KEY"]

if not api_key:
    st.error("¡Alerta! Falta la API Key. Configurala en los secretos de Streamlit.")
    st.stop()

genai.configure(api_key=api_key)

# 3. Configuración del Modelo (Tu creación de AI Studio)
# Acá podés cambiar las instrucciones del sistema si querés ajustar la personalidad.
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro", # O el modelo que hayas usado en AI Studio
    generation_config=generation_config,
    system_instruction="Sos un experto en Oil & Gas y estrategia en Vaca Muerta. Respondés con ironía inteligente y datos precisos."
)

# 4. El Chat (La Interacción)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Capturar input del usuario
if prompt := st.chat_input("¿Cuál es tu consulta estratégica?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generar respuesta
    with st.chat_message("assistant"):
        with st.spinner("Procesando datos del yacimiento..."):
            chat = model.start_chat(history=[
                {"role": m["role"], "parts": [m["content"]]} for m in st.session_state.messages[:-1]
            ])
            response = chat.send_message(prompt)
            st.markdown(response.text)
    
    st.session_state.messages.append({"role": "model", "content": response.text})
