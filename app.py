import streamlit as st
import pandas as pd
import os
from groq import Groq

# ==========================================
# 🔐 API KEY GROQ — diambil dari st.secrets / environment variable
#    Jangan taruh key langsung di kode. Isi salah satu:
#    1) .streamlit/secrets.toml -> GROQ_API_KEY = "gsk_xxx"
#    2) environment variable GROQ_API_KEY
# ==========================================
GROQ_API_KEY = "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"
# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Laptop Zone",
    page_icon="💻",
    layout="wide"
)

# --- 2. TEMA VISUAL: GLASSMORPHISM DARK-PURPLE (samain dengan Churn Prediction Web) ---
GLASS_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

*, html, body, [class*="css"] { font-family: 'Sora', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 2.5rem 2rem 2.5rem !important; max-width: 1280px !important; }

.stApp {
    background: #0a0612 !important;
    background-image:
        radial-gradient(ellipse 80% 60% at 10% 0%,  #2d1b6944 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 90% 10%, #5b21b622 0%, transparent 55%),
        radial-gradient(ellipse 40% 40% at 50% 90%, #1e0b4422 0%, transparent 50%) !important;
    color: #e2d9f3 !important;
}

/* Header banner (pengganti topbar lama) */
.header-wrap {
    background: linear-gradient(135deg, rgba(109,40,217,.18) 0%, rgba(76,29,149,.10) 100%);
    border: 1px solid rgba(139,92,246,.25); border-radius: 16px;
    padding: 1.6rem 2rem; margin: 1.4rem 0 1.8rem 0;
    backdrop-filter: blur(12px);
    display: flex; align-items: center; justify-content: space-between;
    flex-wrap: wrap; gap: .8rem;
}
.brand-row { display: flex; align-items: center; gap: .9rem; }
.brand-icon {
    width: 42px; height: 42px; border-radius: 10px;
    background: linear-gradient(135deg, #7c3aed, #a855f7);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.3rem; box-shadow: 0 0 18px #7c3aed66;
}
.brand-name { font-size: 1.15rem; font-weight: 700; color: #f5f0ff; letter-spacing: -.02em; }
.brand-sub  { font-size: .7rem; color: #7c5bba; margin-top: .15rem; }
.badge {
    font-size: .68rem; font-weight: 600; letter-spacing: .07em; text-transform: uppercase;
    padding: .3rem .8rem; border-radius: 99px;
    background: rgba(124,58,237,.2); border: 1px solid rgba(139,92,246,.4); color: #c4b5fd;
}
.header-icons { display: flex; align-items: center; gap: 1rem; }
.hi-item { position: relative; font-size: 1.05rem; color: #c4b5fd; }
.hi-dot {
    position: absolute; top: -6px; right: -8px; width: 8px; height: 8px; border-radius: 50%;
}
.dot-blue  { background: #7c3aed; box-shadow: 0 0 6px #7c3aed; }
.dot-green { background: #22c55e; box-shadow: 0 0 6px #22c55e; }
.hi-user {
    display: flex; align-items: center; gap: .5rem; font-size: .8rem; font-weight: 600; color: #e9d5ff;
}
.hi-avatar {
    width: 28px; height: 28px; border-radius: 50%;
    background: rgba(124,58,237,.2); border: 1px solid rgba(139,92,246,.4);
    display: flex; align-items: center; justify-content: center; font-size: .9rem;
}

/* Headings */
h1, h2, h3, h4 { color: #f5f0ff !important; font-weight: 700 !important; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0d0818 !important;
    border-right: 1px solid rgba(139,92,246,.18) !important;
}
section[data-testid="stSidebar"] * { color: #e2d9f3 !important; }
section[data-testid="stSidebar"] h1 { color: #f5f0ff !important; font-weight: 700 !important; }
section[data-testid="stSidebar"] h3 {
    color: #c4b5fd !important; font-size: .82rem !important;
    text-transform: uppercase !important; letter-spacing: .07em !important;
    border-bottom: 1px solid rgba(139,92,246,.18); padding-bottom: .35rem;
}
section[data-testid="stSidebar"] hr { border-color: rgba(139,92,246,.18) !important; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #9333ea) !important;
    color: #fff !important; border: none !important; border-radius: 999px !important;
    font-size: .82rem !important; font-weight: 600 !important; padding: .55rem 1.4rem !important;
    box-shadow: 0 4px 15px rgba(124,58,237,.35) !important; transition: all .2s !important;
}
.stButton > button:hover { transform: translateY(-1px) !important; box-shadow: 0 6px 20px rgba(124,58,237,.5) !important; }

/* Alerts */
div[data-testid="stAlert"] {
    background: rgba(124,58,237,.10) !important;
    border-left: 4px solid #7c3aed !important;
    border-radius: 10px !important; color: #e2d9f3 !important;
    backdrop-filter: blur(8px) !important;
}

/* Chat bubbles */
div[data-testid="stChatMessage"] {
    background: rgba(255,255,255,.04) !important;
    border: 1px solid rgba(139,92,246,.18) !important;
    border-radius: 14px !important;
    padding: .3rem .4rem !important;
    backdrop-filter: blur(8px);
    box-shadow: 0 2px 10px rgba(0,0,0,.2);
}
div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarAssistant"]) {
    border-left: 3px solid #7c3aed !important;
}
div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) {
    background: rgba(124,58,237,.08) !important;
    border-right: 3px solid #a855f7 !important;
}
div[data-testid="stChatMessage"] p { color: #e2d9f3 !important; }

/* Chat input */
div[data-testid="stChatInput"] {
    background: rgba(30, 15, 60, 0.85) !important;
    border: 1px solid rgba(139,92,246,.35) !important;
    border-radius: 12px !important;
    box-shadow: 0 2px 12px rgba(124,58,237,.15);
}
div[data-testid="stChatInput"] textarea {
    color: #e2d9f3 !important;
    caret-color: #c4b5fd !important;
}
div[data-testid="stChatInput"] textarea::placeholder { color: #7c5bba !important; opacity: 1 !important; }

/* Caption & small text */
.stCaption, [data-testid="stCaptionContainer"] { color: #7c5bba !important; }

/* Section label (dipakai buat memisahkan info) */
.sec-label {
    font-size: .65rem; text-transform: uppercase; letter-spacing: .12em;
    color: #6b4fa0; border-bottom: 1px solid rgba(139,92,246,.18);
    padding-bottom: .35rem; margin: 1.2rem 0 .8rem 0;
    display: flex; align-items: center; gap: .5rem;
}
.sec-label::before {
    content: ''; display: inline-block; width: 3px; height: 12px; border-radius: 2px;
    background: linear-gradient(#7c3aed, #a855f7);
}

/* Glass info card (dipakai di sidebar utk jam operasional / lokasi) */
.gcard {
    background: rgba(255,255,255,.04); border: 1px solid rgba(139,92,246,.18);
    border-radius: 12px; padding: 1rem 1.2rem; margin-bottom: .7rem;
    backdrop-filter: blur(8px); transition: border-color .2s, transform .2s;
    font-size: .82rem; color: #c4b5fd; line-height: 1.7;
}
.gcard:hover { border-color: rgba(139,92,246,.4); }
.gcard b { color: #f5f0ff; }

/* Divider */
hr { border-color: rgba(139,92,246,.18) !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #3b1d7a; border-radius: 3px; }
</style>

<div class="header-wrap">
    <div class="brand-row">
        <div class="brand-icon">💻</div>
        <div>
            <div class="brand-name">Laptop Zone</div>
            <div class="brand-sub">Customer Service · AI Sales Assistant</div>
        </div>
    </div>
    <div class="header-icons">
        <span class="hi-item">🔔<span class="hi-dot dot-blue"></span></span>
        <span class="hi-item">💬<span class="hi-dot dot-green"></span></span>
        <div class="hi-user">
            <div class="hi-avatar">🙂</div>
            Tamu (guest)
        </div>
        <span class="badge">Groq · Llama 3.3 70B</span>
    </div>
</div>
"""
st.markdown(GLASS_CSS, unsafe_allow_html=True)

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

    st.subheader("🕒 Jam Operasional")
    st.markdown("""
    <div class="gcard">
        <b>Senin – Jumat:</b> 09:00 – 20:00 WIB<br><br>
        <b>Sabtu – Minggu:</b> 10:00 – 18:00 WIB
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📍 Lokasi & Kontak")
    st.markdown("""
    <div class="gcard">
        <b>Alamat:</b><br>Jl. Arjuna, Pendrikan Kidul, Kec. Semarang Tengah,
        Kota Semarang, Jawa Tengah 50229<br><br>
        <b>WhatsApp Admin:</b> 0812-2946-7136
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    if st.button("🔄 Mulai Chat Baru", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.info("💡 Tips: Tanyakan laptop berdasarkan budget atau kebutuhan (coding/gaming/desain).")

# --- 5. AREA CHAT UTAMA ---
st.markdown("<div class='sec-label'>👋 Selamat Datang di Enigma Laptop Zone</div>", unsafe_allow_html=True)
st.write("Saya Joko, asisten virtual toko. Silakan tanya stok atau minta rekomendasi laptop!")

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
            model="llama-3.3-70b-versatile",
            temperature=0.6,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error API: {e}. Cek koneksi internet atau API Key Anda."

# --- 7. INPUT USER ---
if prompt := st.chat_input("Misal: Laptop gaming budget 15 juta..."):
    if not GROQ_API_KEY:
        st.error("⚠️ API Key belum diatur! Tambahkan GROQ_API_KEY di .streamlit/secrets.toml atau environment variable.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Mengecek ketersediaan stok..."):
            response = get_groq_response(prompt, df)
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
