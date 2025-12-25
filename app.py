import streamlit as st
import pandas as pd
from groq import Groq

# ==========================================
# 🛑 AREA KONFIGURASI API KEY GROQ
# Tempel API Key Groq Anda di sini:
GROQ_API_KEY = "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"
# ==========================================

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Enigma Laptop AI",
    page_icon="💻",
    layout="wide" # Layout wide agar chat lebih luas
)

# --- 2. LOAD DATA (DI BELAKANG LAYAR) ---
# Data tetap di-load agar bot pintar, tapi tidak ditampilkan di sidebar
try:
    df = pd.read_csv("data_laptop.csv")
except FileNotFoundError:
    st.error("⚠️ File data_laptop.csv tidak ditemukan!")
    st.stop()

# --- 3. SIDEBAR YANG BARU & KEREN ---
with st.sidebar:
    # Header Profil
    st.title("💻 Enigma Zone")
    st.caption("AI Assistant Toko Laptop Enigma")
    st.markdown("---")

    # Fitur Reset Chat
    st.subheader("🛠️ Kontrol")
    if st.button("🗑️ Hapus Riwayat Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.messages.append({"role": "assistant", "content": "Halo! Riwayat chat sudah dibersihkan. Ada yang bisa saya bantu?"})
        st.rerun()

    # Pengaturan Parameter AI
    st.subheader("🎛️ Pengaturan AI")
    
    # Pilihan Model (Bonus Fitur)
    model_option = st.selectbox(
        "Pilih Model:",
        ("llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768"),
        index=0,
        help="70b lebih pintar, 8b lebih cepat."
    )
    
    # Slider Kreativitas (Temperature)
    creativity = st.slider(
        "Tingkat Kreativitas:", 
        min_value=0.0, 
        max_value=1.0, 
        value=0.5, 
        step=0.1,
        help="0.0 = Jawaban kaku/tepat data. 1.0 = Jawaban lebih variatif."
    )

    st.markdown("---")
    
    # Footer / About
    with st.expander("ℹ️ Tentang Sistem Ini"):
        st.markdown("""
        **Teknologi:**
        - UI: Streamlit
        - LLM: Meta Llama 3
        - API: Groq Cloud
        
        **Fitur:**
        - Cek Stok Real-time
        - Rekomendasi Cerdas
        """)
        st.caption("© 2025 UAS Project")

# --- 4. AREA UTAMA (CHAT) ---
st.header("🤖 Tanya Stok & Rekomendasi Laptop")
st.write("Selamat datang! Silakan tanya spesifikasi, harga, atau minta saran laptop.")

# Inisialisasi History jika belum ada
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Halo! Saya AI Enigma. Mau cari laptop gaming, kantor, atau kuliah?"}
    ]

# Tampilkan Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. FUNGSI OTAK AI ---
def get_groq_response(user_query, data, temp, model_id):
    client = Groq(api_key=GROQ_API_KEY)
    
    data_str = data.to_string(index=False)
    
    system_prompt = f"""
    Kamu adalah Sales Assistant profesional untuk 'Toko Laptop Enigma'.
    
    DATABASE PRODUK:
    {data_str}
    
    INSTRUKSI:
    1. Jawab ramah dan persuasif (seperti sales asli).
    2. Wajib merujuk ke DATABASE PRODUK di atas.
    3. Jika user tanya laptop yang tidak ada di list, tawarkan alternatif yang mirip dari list.
    4. Format jawaban gunakan Markdown (bold untuk Nama Laptop dan Harga).
    5. Jangan sebutkan ID produk.
    """
    
    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            model=model_id,
            temperature=temp, # Mengikuti slider di sidebar
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error API: {e}"

# --- 6. INPUT USER & PROSES ---
if prompt := st.chat_input("Contoh: Laptop 5 jutaan buat skripsi..."):
    # Cek API Key
    if "GANTI_TULISAN" in GROQ_API_KEY:
        st.error("⚠️ API Key belum diisi di kodingan!")
        st.stop()

    # Tampilkan input user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Proses AI
    with st.chat_message("assistant"):
        with st.spinner("Sedang mengetik..."):
            # Mengirim parameter dari sidebar (creativity & model_option) ke fungsi
            response = get_groq_response(prompt, df, creativity, model_option)
            st.markdown(response)
            
    st.session_state.messages.append({"role": "assistant", "content": response})
