import streamlit as st
import pandas as pd
from groq import Groq

# ==========================================
# 🛑 AREA KONFIGURASI API KEY GROQ
GROQ_API_KEY = "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"
# ==========================================

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Enigma Laptop Zone",
    page_icon="🏢",
    layout="wide"
)

# --- 2. LOAD DATA ---
try:
    df = pd.read_csv("data_laptop.csv")
except FileNotFoundError:
    st.error("⚠️ File data_laptop.csv tidak ditemukan!")
    st.stop()

# --- 3. SIDEBAR (INFORMASI TOKO) ---
with st.sidebar:
    st.title("🏢 Enigma Laptop")
    st.caption("Solusi Laptop Terlengkap & Termurah")
    
    st.markdown("---")
    
    # Informasi Jam Operasional
    st.subheader("🕒 Jam Operasional")
    st.markdown("""
    **Senin - Jumat:** 09:00 - 20:00 WIB  
    
    **Sabtu - Minggu:** 10:00 - 18:00 WIB
    """)
    
    st.markdown("---")
    
    # Informasi Kontak & Lokasi
    st.subheader("📍 Lokasi & Kontak")
    st.markdown("""
    **Alamat:** Jl. Raya Banaran, Sekaran, Kec. Gn. Pati, Kota Semarang, Jawa Tengah 50229
    
    **WhatsApp Admin:** 0812-2946-7136
    """)
    
    st.markdown("---")
    
    # Tombol Reset Chat (Tetap penting agar bisa demo ulang)
    if st.button("🔄 Mulai Chat Baru", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.info("💡 Tips: Tanyakan laptop berdasarkan budget atau kebutuhan (coding/gaming/desain).")

# --- 4. AREA CHAT UTAMA ---
st.header("👋 Selamat Datang di Enigma Laptop Zone")
st.write("Saya Joko asisten virtual toko. Silakan tanya stok atau minta rekomendasi laptop!")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Halo! Ada yang bisa saya bantu carikan hari ini? Kami punya promo menarik untuk laptop Gaming dan Ultrabook."}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. FUNGSI OTAK AI ---
def get_groq_response(user_query, data):
    client = Groq(api_key=GROQ_API_KEY)
    
    data_str = data.to_string(index=False)
    
    system_prompt = f"""
    Kamu adalah Customer Service profesional untuk 'Toko Laptop Enigma'.
    
    DATABASE STOK HARI INI:
    {data_str}
    
    PANDUAN MENJAWAB:
    1. Gaya bahasa: Ramah, membantu, dan persuasif (Sales).
    2. WAJIB merujuk ke DATABASE STOK di atas.
    3. Jika user bertanya "Rekomendasi laptop budget X", cari harga yang mendekati di database.
    4. Jika stok habis atau tidak ada di data, katakan dengan sopan dan tawarkan alternatif.
    5. Jangan mengarang spesifikasi yang tidak ada di data.
    """
    
    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            # Saya kunci menggunakan model terbaik & stabil saat ini
            model="llama-3.3-70b-versatile", 
            temperature=0.6, # Kreativitas seimbang (tidak terlalu kaku, tidak ngawur)
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error API: {e}. Cek koneksi internet atau API Key Anda."

# --- 6. INPUT USER ---
if prompt := st.chat_input("Misal: Laptop gaming budget 15 juta..."):
    # Cek API Key
    if "GANTI_TULISAN" in GROQ_API_KEY:
        st.error("⚠️ API Key belum diisi di baris 8!")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Mengecek ketersediaan stok..."):
            response = get_groq_response(prompt, df)
            st.markdown(response)
            
    st.session_state.messages.append({"role": "assistant", "content": response})
