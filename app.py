import streamlit as st
import pandas as pd
from groq import Groq

# ==========================================
# 🛑 AREA KONFIGURASI API KEY GROQ
GROQ_API_KEY = "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"
# ==========================================

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Laptop Zone",
    page_icon="💻",
    layout="wide"
)

# --- 2. TEMA VISUAL LIGHT: NAVY + CYAN (ALA DASHBOARD) ---
CI4_CSS = """
<style>
    :root{
        --navy: #1B3B6D;
        --navy-dark: #14294F;
        --accent-blue: #116BFF;
        --cyan: #17C3E0;
        --cyan-dark: #0FA8C4;
        --bg-page: #F5F7FC;
        --bg-card: #FFFFFF;
        --border: #E7ECF5;
        --sidebar-active-bg: #EFF4FF;
        --badge-green: #178755;
        --text-muted: #8A93A6;
    }

    /* Latar utama */
    .stApp {
        background-color: var(--bg-page);
        color: var(--navy);
        font-family: "Segoe UI", "Helvetica Neue", sans-serif;
    }

    /* Top bar custom ala dashboard */
    .topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background-color: var(--bg-card);
        border-bottom: 1px solid var(--border);
        border-top: 3px solid var(--navy-dark);
        padding: 12px 24px;
        margin: -1rem -1rem 1.2rem -1rem;
        border-radius: 0 0 10px 10px;
        box-shadow: 0 2px 6px rgba(20,41,79,0.05);
    }
    .topbar-left { display:flex; align-items:center; gap:14px; }
    .topbar-logo { display:flex; align-items:center; gap:10px; font-weight:800; font-size:22px; color: var(--navy); }
    .topbar-logo span.icon { font-size: 22px; }
    .topbar-right { display:flex; align-items:center; gap:18px; }
    .topbar-icon { position:relative; font-size:18px; color: var(--navy); }
    .topbar-badge {
        position:absolute; top:-8px; right:-10px; font-size:10px; color:#fff;
        border-radius: 999px; padding: 1px 5px; font-weight:700;
    }
    .badge-blue { background-color: var(--accent-blue); }
    .badge-green { background-color: var(--badge-green); }
    .topbar-user { display:flex; align-items:center; gap:8px; font-weight:600; color: var(--navy); font-size: 14px; }
    .topbar-avatar {
        width:30px; height:30px; border-radius:50%; background: var(--sidebar-active-bg);
        display:flex; align-items:center; justify-content:center; font-size:16px;
    }

    /* Judul & heading */
    h1, h2, h3 {
        color: var(--navy) !important;
        font-weight: 800 !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: var(--bg-card);
        border-right: 1px solid var(--border);
    }
    section[data-testid="stSidebar"] * {
        color: var(--navy) !important;
    }
    section[data-testid="stSidebar"] h1 {
        color: var(--navy) !important;
        font-weight: 800 !important;
    }
    section[data-testid="stSidebar"] h3 {
        color: var(--navy) !important;
        border-bottom: 1px solid var(--border);
        padding-bottom: 4px;
    }

    /* Tombol ala pill cyan */
    .stButton > button {
        background-color: var(--cyan) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 20px !important;
        font-weight: 600 !important;
        padding: 6px 18px !important;
        transition: background-color 0.2s ease-in-out;
        box-shadow: 0 2px 6px rgba(23,195,224,0.35);
    }
    .stButton > button:hover {
        background-color: var(--cyan-dark) !important;
        color: #FFFFFF !important;
    }

    /* Info box */
    div[data-testid="stAlert"] {
        background-color: var(--sidebar-active-bg) !important;
        border-left: 4px solid var(--accent-blue) !important;
        color: var(--navy) !important;
        border-radius: 8px;
    }

    /* Chat bubble - assistant */
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarAssistant"]) {
        background-color: var(--bg-card);
        border: 1px solid var(--border);
        border-left: 4px solid var(--navy);
        border-radius: 12px;
        padding: 10px 14px;
        box-shadow: 0 1px 4px rgba(20,41,79,0.05);
    }

    /* Chat bubble - user */
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) {
        background-color: var(--sidebar-active-bg);
        border: 1px solid var(--border);
        border-right: 4px solid var(--cyan);
        border-radius: 12px;
        padding: 10px 14px;
    }

    /* Input chat di bawah */
    div[data-testid="stChatInput"] {
        border: 1.5px solid var(--border) !important;
        border-radius: 10px !important;
        background-color: var(--bg-card) !important;
        box-shadow: 0 1px 4px rgba(20,41,79,0.06);
    }
    div[data-testid="stChatInput"] textarea {
        color: var(--navy) !important;
    }

    /* Caption & teks kecil */
    .stCaption, [data-testid="stCaptionContainer"] {
        color: var(--text-muted) !important;
    }

    /* Divider */
    hr {
        border-color: var(--border) !important;
    }
</style>

<div class="topbar">
    <div class="topbar-left">
        <div class="topbar-logo"><span class="icon">💻</span> Laptop Zone</div>
    </div>
    <div class="topbar-right">
        <div class="topbar-icon">🔔<span class="topbar-badge badge-blue">•</span></div>
        <div class="topbar-icon">💬<span class="topbar-badge badge-green">•</span></div>
        <div class="topbar-user">
            <div class="topbar-avatar">🙂</div>
            Tamu (guest)
        </div>
    </div>
</div>
"""
st.markdown(CI4_CSS, unsafe_allow_html=True)

# --- 3. LOAD DATA ---
try:
    df = pd.read_csv("data_laptop.csv")
except FileNotFoundError:
    st.error("⚠️ File data_laptop.csv tidak ditemukan!")
    st.stop()

# --- 4. SIDEBAR (INFORMASI TOKO) ---
with st.sidebar:
    st.title("Laptop Zone")
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
    **Alamat:** Jl. Arjuna, Pendrikan Kidul, Kec. Semarang Tengah, Kota Semarang, Jawa Tengah 50229

    **WhatsApp Admin:** 0812-2946-7136
    """)

    st.markdown("---")

    # Tombol Reset Chat (Tetap penting agar bisa demo ulang)
    if st.button("🔄 Mulai Chat Baru", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.info("💡 Tips: Tanyakan laptop berdasarkan budget atau kebutuhan (coding/gaming/desain).")

# --- 5. AREA CHAT UTAMA ---
st.markdown("### Data Tables")
st.caption("Home")
st.markdown("#### 👋 Selamat Datang di Enigma Laptop Zone")
st.write("Saya Joko asisten virtual toko. Silakan tanya stok atau minta rekomendasi laptop!")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Halo! Ada yang bisa saya bantu carikan hari ini? Kami punya promo menarik untuk laptop Gaming dan Ultrabook."}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 6. FUNGSI OTAK AI ---
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
            temperature=0.6,  # Kreativitas seimbang (tidak terlalu kaku, tidak ngawur)
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error API: {e}. Cek koneksi internet atau API Key Anda."

# --- 7. INPUT USER ---
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
