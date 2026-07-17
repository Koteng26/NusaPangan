"""
💳 Paket & Program — Model bisnis: freemium + berbayar opsional
Petani: gratis/freemium + benefit didanai mitra + NusaTani+ opsional.
Institusi: langganan dashboard & layanan data (sisi pendapatan utama).
"""
import streamlit as st
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from utils import COMMON_CSS

st.set_page_config(page_title="Paket & Program", page_icon="💳", layout="wide")
st.markdown(COMMON_CSS, unsafe_allow_html=True)

with st.sidebar:
    c = st.columns([1, 3, 1])
    with c[1]:
        st.image("assets/logo.png", use_container_width=True)

ss = st.session_state

st.markdown("""
<div class="np-header" style="background:linear-gradient(135deg,#14532d,#166534 45%,#1C6E8C);">
    <p style="font-size:0.75rem;opacity:0.65;margin-bottom:6px;">MODEL BISNIS · FREEMIUM + BERBAYAR OPSIONAL</p>
    <h2 style="font-size:1.6rem;font-weight:800;">💳 Paket & Program</h2>
    <p style="font-size:0.95rem;margin-top:6px;">Petani nyaris gratis — pendapatan utama dari sisi institusi. Benefit petani didanai mitra, bukan stok NusaPangan.</p>
</div>
""", unsafe_allow_html=True)

if ss.get("petani"):
    p = ss["petani"]
    st.markdown(f'<div class="np-alert np-alert-green">👋 Halo <b>{p["nama"]}</b> ({p["rice_id"]}) — paket aktif Anda: <b>{p["paket"]}</b>.</div>', unsafe_allow_html=True)

st.markdown("### 👨‍🌾 Untuk Petani")
c1, c2, c3 = st.columns(3)
def tier(col, name, price, color, items, tag=""):
    lis = "".join([f'<li style="font-size:0.85rem;color:#555;padding:4px 0 4px 18px;position:relative;"><span style="position:absolute;left:0;color:#4CAF50;">✓</span>{it}</li>' for it in items])
    col.markdown(f"""
    <div class="np-card" style="border-top:4px solid {color};min-height:320px;">
        <div style="font-size:1.15rem;font-weight:800;color:{color};">{name}</div>
        <div style="font-family:monospace;font-size:1.1rem;color:#1B5E20;margin:4px 0 10px;">{price}</div>
        {f'<span class="np-badge np-badge-green">{tag}</span>' if tag else ''}
        <ul style="list-style:none;margin-top:10px;">{lis}</ul>
    </div>""", unsafe_allow_html=True)

tier(c1, "Petani", "Gratis", "#4CAF50",
     ["Profil & Rice ID terverifikasi", "Harga harian & info pasar", "Akses AgriMart (jual ke SPPG)", "QR traceability dasar"],
     "Freemium")
tier(c2, "Program Musim", "Gratis · didanai mitra", "#15803d",
     ["Semua fitur Petani", "Pendampingan agronom 20 jam / musim", "Voucher input 1× di toko tani mitra", "Prediksi cuaca & waktu tanam"],
     "Benefit mitra")
tier(c3, "NusaTani+", "Rp 49rb / musim", "#E65100",
     ["Semua fitur di atas", "Prioritas pembeli & harga terbaik", "Analitik panen lanjutan", "Sertifikat traceability (premium/organik)"],
     "Opsional")

st.markdown('<div class="np-alert np-alert-orange" style="margin-top:10px;"><b>◆ Prinsip tata kelola:</b> benefit fisik (voucher input) <b>didanai & disalurkan mitra</b> — NusaPangan tidak membeli, menyimpan, atau menjual barang. Kami memonetisasi <b>akses ke data petani terverifikasi</b>, bukan stok.</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("### 🏛️ Untuk Institusi — sumber pendapatan utama")
i1, i2, i3 = st.columns(3)
i1.markdown('<div class="np-card"><b style="color:#0D47A1;">Langganan Dashboard</b><br><span style="font-family:monospace;color:#1B5E20;">Rp 5–15 jt/bln</span><br><small style="color:#666;">SPPG, Bulog, Pemda — Command Center, MBG Monitor, Price Radar.</small></div>', unsafe_allow_html=True)
i2.markdown('<div class="np-card"><b style="color:#7C3AED;">Verifikasi & Prediksi</b><br><span style="font-family:monospace;color:#1B5E20;">Rp 25–50 rb/verifikasi</span><br><small style="color:#666;">Bank & asuransi — verifikasi petani; prediksi panen untuk BGN/Bulog.</small></div>', unsafe_allow_html=True)
i3.markdown('<div class="np-card"><b style="color:#00897B;">Akses Mitra Input</b><br><span style="font-family:monospace;color:#1B5E20;">Sponsorship / lead</span><br><small style="color:#666;">Perusahaan input mensponsori benefit musim untuk akses jaringan petani.</small></div>', unsafe_allow_html=True)

st.markdown("---")
if ss.get("petani"):
    st.page_link("pages/1_👨‍🌾_Farmer_Dashboard.py", label="Ke Dashboard Petani →", icon="👨‍🌾")
else:
    st.page_link("pages/0_📝_Pendaftaran.py", label="Daftar sebagai petani dulu →", icon="📝")

st.markdown('<p class="np-source">Model ilustratif untuk prototype. Angka paket dapat disesuaikan; benefit fisik selalu via mitra (asset-light).</p>', unsafe_allow_html=True)
