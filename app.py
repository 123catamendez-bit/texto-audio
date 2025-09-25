import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

# Título con emoji
st.title("🗣️ Conversión de Texto a Audio 🎧")

# Imagen portada
image = Image.open("gato_raton.png")
st.image(image, caption="🐭 Una fábula entre gato y ratón 🐱", use_column_width=True)

with st.sidebar:
    st.subheader("⚙️ Configuración")
    st.write("Escribe o selecciona un texto para escucharlo convertido en audio.")

# Crear carpeta temporal
try:
    os.mkdir("temp")
except:
    pass

# Texto de ejemplo
st.subheader("📖 Una pequeña Fábula")
st.write(
    "¡Ay! -dijo el ratón-. El mundo se hace cada día más pequeño. "
    "Al principio era tan grande que le tenía miedo. Corría y corría y "
    "me alegraba ver esos muros a lo lejos. Pero esas paredes se estrechan "
    "tan rápido que me encuentro en el último cuarto y ahí en el rincón "
    "está la trampa sobre la cual debo pasar. "
    "—Todo lo que debes hacer es cambiar de rumbo —dijo el gato… y se lo comió. "
    " *(Franz Kafka)*"
)

# Input de texto
st.markdown("✍️ **Escribe el texto que quieras escuchar en audio:**")
text = st.text_area("Ingrese el texto aquí")

# Selector de idioma con banderas
option_lang = st.selectbox(
    "🌍 Selecciona el idioma",
    ("🇪🇸 Español", "🇬🇧 English"),
)

if option_lang.startswith("🇪🇸"):
    lg = "es"
else:
    lg = "en"

# Conversor de texto a voz
def text_to_speech(text, lg):
    tts = gTTS(text, lang=lg)
    try:
        my_file_name = text[0:20].replace(" ", "_")
    except:
        my_file_name = "audio"
    file_path = f"temp/{my_file_name}.mp3"
    tts.save(file_path)
    return file_path

# Botón de conversión
if st.button("🎙️ Convertir a Audio"):
    if text.strip() == "":
        st.warning("⚠️ Por favor escribe un texto para convertirlo.")
    else:
        with st.spinner("🔊 Generando tu audio..."):
            file_path = text_to_speech(text, lg)
            st.success("✅ Audio generado con éxito!")

            # Reproducir
            audio_file = open(file_path, "rb")
            audio_bytes = audio_file.read()
            st.markdown("### ▶️ Escucha tu audio:")
            st.audio(audio_bytes, format="audio/mp3")

            # Descargar
            with open(file_path, "rb") as f:
                data = f.read()

            bin_str = base64.b64encode(data).decode()
            href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(file_path)}">📥 Descargar archivo de audio</a>'
            st.markdown(href, unsafe_allow_html=True)

# Función para limpiar archivos viejos
def remove_files(n):
    mp3_files = glob.glob("temp/*.mp3")
    if mp3_files:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)

# Limpiar archivos de más de 7 días
remove_files(7)
