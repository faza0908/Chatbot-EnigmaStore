import streamlit as st
import pandas as pd
import google.generativeai as genai

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Enigma Laptop Chatbot",
    page_icon="💻",
    layout="centered"
)

# --- JUDUL & SIDEBAR ---
st.title("🤖 CS Toko Laptop Enigma")
st.write("Tanyakan spesifikasi, rekomendasi, atau stok laptop di sini!")

with st.sidebar:
    st.header("⚙️ Konfigurasi")
    api_key = st.text_input("Masukkan Gemini API Key:", type="password")
    st.info("Dapatkan key di aistudio.google.com")
    st.divider()
    st.subheader("📦 Data Stok Toko")
    
    # Load Data
    try:
        df = pd.read_csv("data_laptop.csv")
        st.dataframe(df[['Merk', 'Model', 'Harga']], hide_index=True)
    except FileNotFoundError:
        st.error("File data_laptop.csv tidak ditemukan!")
        st.stop()

# --- FUNGSI AI ---
def get_response(user_query, api_key, data):
    # Konfigurasi API
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Prompt Engineering (Instruksi Utama untuk AI)
    # Kita menyuapkan data CSV sebagai string ke dalam prompt
    data_str = data.to_string(index=False)
    
    system_prompt = f"""
    Kamu adalah asisten Customer Service untuk 'Toko Laptop Enigma'.
    Tugasmu adalah menjawab pertanyaan pelanggan berdasarkan DATA STOK berikut:
    
    {data_str}
    
    Aturan menjawab:
    1. Jawab dengan sopan dan ramah.
    2. HANYA rekomendasikan laptop yang ada di data stok di atas.
    3. Jika user tanya laptop yang tidak ada di data, katakan stok kosong.
    4. Jika user tanya rekomendasi (misal: budget 10 juta), cari yang harganya mendekati di data.
    5. Jawab dalam Bahasa Indonesia yang baik.
    
    Pertanyaan User: {user_query}
    """
    
    try:
        response = model.generate_content(system_prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}. Cek API Key kamu."

# --- LOGIKA CHATBOT ---

# 1. Inisialisasi History Chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Halo! Selamat datang di Enigma Laptop Zone. Ada yang bisa saya bantu cari hari ini?"}
    ]

# 2. Tampilkan Chat Terdahulu
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Input User
if prompt := st.chat_input("Ketik pesan Anda di sini..."):
    
    # Cek apakah API Key sudah diisi
    if not api_key:
        st.warning("⚠️ Mohon masukkan API Key di menu sebelah kiri terlebih dahulu.")
        st.stop()
        
    # Tampilkan pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Proses jawaban AI
    with st.chat_message("assistant"):
        with st.spinner("Sedang mengecek stok..."):
            response = get_response(prompt, api_key, df)
            st.markdown(response)
            
    # Simpan jawaban AI ke history
    st.session_state.messages.append({"role": "assistant", "content": response})
