import os
import shutil
import streamlit as st
from TTS.api import TTS

# Setup
st.set_page_config(page_title="Custom Voice TTS", layout="centered")
TTS_MODEL = "tts_models/multilingual/multi-dataset/your_tts"
tts = TTS(model_name=TTS_MODEL)
VOICE_DIR = "saved_voices"
os.makedirs(VOICE_DIR, exist_ok=True)

def list_voices():
    return sorted([f.replace(".wav", "") for f in os.listdir(VOICE_DIR) if f.endswith(".wav")])

st.title("🎙️ Custom Voice TTS Generator")

# Voice upload
st.header("1️⃣ Upload & Save Voice")
uploaded_audio = st.file_uploader("Upload a reference voice (.wav)", type=["wav"])
voice_name = st.text_input("Name your voice")
if st.button("Save Voice") and uploaded_audio and voice_name.strip():
    path = os.path.join(VOICE_DIR, f"{voice_name.strip()}.wav")
    with open(path, "wb") as f:
        f.write(uploaded_audio.read())
    st.success(f"✅ Voice '{voice_name}' saved!")
elif st.button("Save Voice"):
    st.warning("Please upload a file and enter a voice name.")

# TTS
st.header("2️⃣ Generate Speech")
text = st.text_area("Enter text to convert to speech")
voice_choices = list_voices()
selected_voice = st.selectbox("Select a saved voice", voice_choices if voice_choices else ["No voices saved"])

if st.button("Generate"):
    if not text or selected_voice == "No voices saved":
        st.warning("Enter text and select a valid voice.")
    else:
        ref_path = os.path.join(VOICE_DIR, f"{selected_voice}.wav")
        output_path = "output.wav"
        tts.tts_to_file(text=text, speaker_wav=ref_path, language="en", file_path=output_path)
        st.audio(output_path)
        with open(output_path, "rb") as f:
            st.download_button("Download Audio", f, file_name="generated.wav")

st.caption("Built with 🐍 Python + 🗣️ Coqui TTS + 🚀 Streamlit")
