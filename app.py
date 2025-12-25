import streamlit as st
import pandas as pd
import google.generativeai as genai

# ==========================================
# 🛑 AREA KONFIGURASI API KEY (HARDCODE)
# Tempel API Key Anda di dalam tanda kutip di bawah ini:
GOOGLE_API_KEY = "AIzaSyD0dyAVo9-4Osl3VSR6MUdgOb_tF0wFmQE"
# ==========================================

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Enigma Laptop Chatbot",
    page_icon="💻",
    layout="centered"
)

# --- JUDUL & SIDEBAR ---
st.title("🤖 CS Toko Laptop Enigma")
st.write("Langsung tanya saja, tidak perlu input Key lagi!")


# --- FUNGSI AI ---
def get_response(user_query, data):
    # Menggunakan API Key yang sudah di-hardcode di atas
    genai.configure(api_key=AIzaSyD0dyAVo9-4Osl3VSR6MUdgOb_tF0wFmQE)
    
    # Pilih Model
    # Jika 'gemini-1.5-flash' masih error 404, ubah teks di bawah menjadi 'gemini-pro'
    model_name = 'gemini-1.5-flash' 
    
    try:
        model = genai.GenerativeModel(model_name)
    except:
        # Fallback jika model flash bermasalah
        model = genai.GenerativeModel('gemini-pro')

    # Siapkan Data
    data_str = data.to_string(index=False)
    
    # Instruksi Utama (System Prompt)
    system_prompt = f"""
    Kamu adalah asisten Customer Service untuk 'Toko Laptop Enigma'.
    Tugasmu adalah menjawab pertanyaan pelanggan berdasarkan DATA STOK berikut:
    
    {data_str}
    
    Aturan menjawab:
    1. Jawab dengan sopan, santai, tapi tetap profesional.
    2. HANYA rekomendasikan laptop yang ada di data stok di atas.
    3. Jika user tanya laptop yang tidak ada di data, katakan stok kosong.
    4. Jika user tanya rekomendasi (misal: budget 10 juta), cari yang harganya mendekati di data.
    5. Jika user menawar harga, tolak dengan halus.
    
    Pertanyaan User: {user_query}
    """
    
    try:
        response = model.generate_content(system_prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}. Cek apakah API Key sudah benar disalin."

# --- LOGIKA CHATBOT ---

# 1. Inisialisasi History Chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Halo! Saya bot Enigma. Cari laptop spek apa kak?"}
    ]

# 2. Tampilkan Chat Terdahulu
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Input User
if prompt := st.chat_input("Ketik pesan Anda di sini..."):
    
    # Cek apakah user lupa mengganti tulisan API Key
    if GOOGLE_API_KEY == "AIzaSyD0dyAVo9-4Osl3VSR6MUdgOb_tF0wFmQE":
        st.error("⚠️ Kamu belum memasukkan API Key di baris 8 file app.py!")
        st.stop()

    # Tampilkan pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Proses jawaban AI
    with st.chat_message("assistant"):
        with st.spinner("Sedang mengecek stok..."):
            response = get_response(prompt, df)
            st.markdown(response)
            
    # Simpan jawaban AI ke history
    st.session_state.messages.append({"role": "assistant", "content": response})
