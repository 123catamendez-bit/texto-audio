import streamlit as st
import os
import time
import glob
from gtts import gTTS
# from PIL import Image   # ← Descomenta cuando tengas una imagen
import base64

# --- CONFIGURACIÓN GENERAL ---
st.set_page_config(page_title="🌌 Voz Estelar | IA Galáctica", layout="centered")

# --- FONDO GALÁCTICO ---
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #0b0f1a;
    background-image: radial-gradient(circle at 20% 20%, #16213e, #0b0f1a);
    color: #e0e0e0;
}
[data-testid="stSidebar"] {
    background-color: #1a1f2e;
    color: #ffffff;
}
h1, h2, h3, p, label {
    color: #e0e0e0;
    font-family: 'Trebuchet MS', sans-serif;
}
textarea {
    background-color: #141b2d !important;
    color: #e0e0e0 !important;
}
a, a:visited, a:hover {
    text-decoration: none;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# --- TÍTULO ---
st.title("🪐 Voz Estelar")
st.markdown("Convierte tus pensamientos en **ondas sonoras cósmicas** y deja que la galaxia te escuche 🌠")

# --- IMAGEN DE PORTADA ---
# image = Image.open("voz_estelar.jpg")
# st.image(image, caption="🎧 Transmisión desde la Nebulosa de Orión", use_column_width=True)

# --- SIDEBAR ---
with st.sidebar:
    st.subheader("⚙️ Panel de Comando")
    st.write("Configura tu idioma interestelar y envía tu mensaje para ser transmitido por voz a través del cosmos.")

# --- CREAR CARPETA TEMPORAL ---
os.makedirs("temp", exist_ok=True)

# --- TEXTO DE DEMO ---
st.subheader("🛰️ Mensaje Intergaláctico de Prueba")
st.write(
    "\"Capitán, los sensores detectan una nueva forma de comunicación. "
    "Parece provenir de una inteligencia artificial de voz. "
    "Procedemos a traducir la transmisión...\""
)

# --- INPUT DE TEXTO ---
st.markdown("💬 **Escribe tu mensaje estelar para convertirlo en voz:**")
text = st.text_area("📡 Ingrese el texto aquí", placeholder="Ejemplo: 'Bienvenido al universo de la Inteligencia Artificial Galáctica'")

# --- SELECTOR DE IDIOMA ---
option_lang = st.selectbox(
    "🌍 Selecciona el idioma de transmisión",
    ("🇪🇸 Español - Canal Solar", "🇬🇧 English - Galactic Channel"),
)

lg = "es" if option_lang.startswith("🇪🇸") else "en"

# --- FUNCIÓN DE CONVERSIÓN ---
def text_to_speech(text, lg):
    tts = gTTS(text, lang=lg)
    my_file_name = text[0:20].replace(" ", "_") if text else "audio"
    file_path = f"temp/{my_file_name}.mp3"
    tts.save(file_path)
    return file_path

# --- BOTÓN DE CONVERSIÓN ---
if st.button("🚀 Transmitir Mensaje por Voz"):
    if text.strip() == "":
        st.warning("⚠️ Ingresa un texto antes de transmitir tu mensaje interestelar.")
    else:
        with st.spinner("🛰️ Transmitiendo señal de voz a través del espacio..."):
            file_path = text_to_speech(text, lg)
            st.success("✅ Señal recibida: ¡audio generado con éxito!")

            # Reproducir
            with open(file_path, "rb") as audio_file:
                audio_bytes = audio_file.read()
            st.markdown("### 🎧 Escucha tu transmisión:")
            st.audio(audio_bytes, format="audio/mp3")

            # Descargar
            with open(file_path, "rb") as f:
                data = f.read()

            bin_str = base64.b64encode(data).decode()
            href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(file_path)}">📥 Descargar archivo de audio</a>'
            st.markdown(href, unsafe_allow_html=True)

# --- LIMPIAR ARCHIVOS ANTIGUOS ---
def remove_files(n):
    mp3_files = glob.glob("temp/*.mp3")
    if mp3_files:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)

remove_files(7)

# --- PIE ---
st.markdown("---")
st.markdown("<p style='text-align:center; color:#8f9bb3;'>🌌 Proyecto IA Galáctica · Transmisión de voz por gTTS · 2025</p>", unsafe_allow_html=True)
