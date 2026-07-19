"""
🌾 NusaPangan — Farm-to-Fork Traceability for MBG
"""
import streamlit as st
import pandas as pd
import os, sys

st.set_page_config(page_title="NusaPangan", page_icon="🌾", layout="wide", initial_sidebar_state="expanded")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import load_data, COMMON_CSS

st.markdown(COMMON_CSS, unsafe_allow_html=True)

# Sidebar - logo only
with st.sidebar:
    col_logo = st.columns([1, 3, 1])
    with col_logo[1]:
        st.image("assets/logo.png", use_container_width=True)
    st.markdown("""
    <p style="text-align:center;font-size:1.05rem;color:#1B5E20;font-weight:700;margin-top:0;line-height:1.4;">
        "From Farm Data to<br>Indonesia's Food Security"
    </p>
    """, unsafe_allow_html=True)

# Load data
df_farmers = load_data("farmers.csv")
df_journeys = load_data("journeys.csv")
df_harga = load_data("harga_beras_pihps.csv")
df_produksi = load_data("produksi_padi_bps.csv")
df_mbg = load_data("mbg_satpen.csv")

# Stats
total_farmers = len(df_farmers)
total_journeys = len(df_journeys)
total_mbg_dki = df_mbg[df_mbg["provinsi"]=="DKI Jakarta"]["jumlah_satpen"].sum()
total_mbg_banten = df_mbg[df_mbg["provinsi"]=="Banten"]["jumlah_satpen"].sum()
avg_harga_dki = df_harga[df_harga["provinsi"]=="DKI Jakarta"]["harga_beras_medium_kg"].mean()
avg_harga_banten = df_harga[df_harga["provinsi"]=="Banten"]["harga_beras_medium_kg"].mean()
gap_harga = avg_harga_dki - avg_harga_banten

# HERO
st.markdown("""
<div class="np-header" style="background: linear-gradient(135deg, #14532d 0%, #166534 40%, #15803d 100%); box-shadow: 0 8px 32px rgba(20,83,45,0.3);">
    <p style="font-size: 0.75rem; opacity: 0.6; margin-bottom: 8px;">Platform Traceability MBG · Data Real PIHPS + BPS</p>
    <h2 style="font-size: 1.8rem; font-weight: 800;">🌾 NusaPangan</h2>
    <p style="font-size: 1.1rem; line-height: 1.6; margin-top: 10px; font-weight: 500;">
        <em>"Setiap porsi makan bergizi gratis yang diterima anak Indonesia<br>
        dapat ditelusuri kembali hingga petani yang menanamnya."</em>
    </p>
</div>
""", unsafe_allow_html=True)

# WELCOME + ALUR
if st.session_state.get("petani"):
    _p = st.session_state["petani"]
    st.markdown(f'<div class="np-alert np-alert-green">👋 Selamat datang kembali, <b>{_p["nama"]}</b> · <span style="font-family:monospace;">{_p["rice_id"]}</span> — paket <b>{_p["paket"]}</b>.</div>', unsafe_allow_html=True)

st.markdown("### 🧭 Alur NusaPangan — dari daftar sampai tersalur")
st.markdown("""
<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px;">
  <div class="np-card" style="flex:1;min-width:110px;text-align:center;padding:12px;"><b style="color:#15803d;">1 · Daftar</b><br><small style="color:#666;">petani + Rice ID</small></div>
  <div class="np-card" style="flex:1;min-width:110px;text-align:center;padding:12px;"><b style="color:#15803d;">2 · Dashboard</b><br><small style="color:#666;">profil &amp; panen</small></div>
  <div class="np-card" style="flex:1;min-width:110px;text-align:center;padding:12px;"><b style="color:#E65100;">3 · AgriMart</b><br><small style="color:#666;">jual ke SPPG</small></div>
  <div class="np-card" style="flex:1;min-width:110px;text-align:center;padding:12px;"><b style="color:#2196F3;">4 · QR Trace</b><br><small style="color:#666;">sawah → piring</small></div>
  <div class="np-card" style="flex:1;min-width:110px;text-align:center;padding:12px;"><b style="color:#1A237E;">5 · Gov Dashboard</b><br><small style="color:#666;">intelijen pangan</small></div>
</div>
""", unsafe_allow_html=True)
_c1, _c2 = st.columns(2)
with _c1:
    st.page_link("pages/0_📝_Pendaftaran.py", label="🌱 Mulai — Daftar sebagai Petani")
with _c2:
    st.page_link("pages/9_💳_Paket_Program.py", label="💳 Lihat Paket & Program")
st.markdown("---")

# STATS
st.markdown("### 📊 Data Real — Banten vs DKI Jakarta")
c1, c2, c3, c4 = st.columns(4)
c1.metric("👨‍🌾 Petani Banten", f"{total_farmers}", "Terverifikasi lapangan")
c2.metric("🔍 Journey Tracked", f"{total_journeys}", "Banten → DKI")
c3.metric("🏫 Satpen MBG", f"{total_mbg_dki + total_mbg_banten:,}", "DKI + Banten")
c4.metric("💰 Gap Harga", f"+Rp {gap_harga:,.0f}", "DKI lebih mahal/kg")
st.markdown('<p class="np-source">Sumber: SP2KP Kemendag, BPS, Kemendikdasmen 2026</p>', unsafe_allow_html=True)

# MASALAH
st.markdown("---")
st.markdown("### ❓ Mengapa NusaPangan Dibutuhkan?")
st.markdown(f"Program MBG mengalirkan **Rp 268 triliun (UU APBN 2026)** untuk **62 juta anak** di **280.023 sekolah**. Namun supply chain-nya masih gelap:")

p1, p2, p3 = st.columns(3)
with p1:
    st.markdown("""
    <div class="np-card" style="border-top:4px solid #F44336;text-align:center;padding:20px;">
        <div style="font-size:2.5rem;">🔍</div>
        <div style="font-size:1rem;font-weight:700;color:#333;margin-top:8px;">Tidak Ada Traceability</div>
        <div style="font-size:0.82rem;color:#666;margin-top:6px;line-height:1.6;">Dari mana bahan makanan MBG? Melewati tangan siapa? Tidak ada yang tahu.</div>
    </div>""", unsafe_allow_html=True)
with p2:
    st.markdown("""
    <div class="np-card" style="border-top:4px solid #FF9800;text-align:center;padding:20px;">
        <div style="font-size:2.5rem;">💸</div>
        <div style="font-size:1rem;font-weight:700;color:#333;margin-top:8px;">Potensi Kebocoran Subsidi</div>
        <div style="font-size:0.82rem;color:#666;margin-top:6px;line-height:1.6;">Riset IPB: 32% petani tak tercatat, 68% penerima subsidi bukan petani aktif.</div>
    </div>""", unsafe_allow_html=True)
with p3:
    st.markdown("""
    <div class="np-card" style="border-top:4px solid #2196F3;text-align:center;padding:20px;">
        <div style="font-size:2.5rem;">🗑️</div>
        <div style="font-size:1rem;font-weight:700;color:#333;margin-top:8px;">Food Loss Masif</div>
        <div style="font-size:0.82rem;color:#666;margin-top:6px;line-height:1.6;">Bappenas: 23-48 juta ton pangan terbuang per tahun senilai ratusan triliun rupiah.</div>
    </div>""", unsafe_allow_html=True)

# BANTEN vs DKI
st.markdown("---")
st.markdown("### 🗺️ Studi Kasus: Banten → DKI Jakarta")

prod_banten = df_produksi[df_produksi["provinsi"]=="Banten"]["produksi_ton"].sum()
prod_dki = df_produksi[df_produksi["provinsi"]=="DKI Jakarta"]["produksi_ton"].sum()

col_a, col_b = st.columns(2)
with col_a:
    st.markdown(f"""
    <div class="np-card" style="border-left:5px solid #4CAF50;padding:20px;">
        <div style="font-size:1.1rem;font-weight:800;color:#1B5E20;">🟢 Banten — Surplus Beras</div>
        <div style="font-size:0.88rem;color:#444;margin-top:10px;line-height:2;">
            📊 Produksi Jan-Jun: <strong>{prod_banten:,.0f} ton</strong><br>
            💰 Harga rata-rata: <strong>Rp {avg_harga_banten:,.0f}/kg</strong><br>
            🏫 Satpen MBG: <strong>{total_mbg_banten:,}</strong><br>
            👨‍🌾 Petani terdaftar: <strong>{total_farmers}</strong>
        </div>
    </div>""", unsafe_allow_html=True)
with col_b:
    st.markdown(f"""
    <div class="np-card" style="border-left:5px solid #F44336;padding:20px;">
        <div style="font-size:1.1rem;font-weight:800;color:#C62828;">🔴 DKI Jakarta — Defisit Total</div>
        <div style="font-size:0.88rem;color:#444;margin-top:10px;line-height:2;">
            📊 Produksi Jan-Jun: <strong>{prod_dki:,.1f} ton</strong> (hampir nol)<br>
            💰 Harga rata-rata: <strong>Rp {avg_harga_dki:,.0f}/kg</strong><br>
            🏫 Satpen MBG: <strong>{total_mbg_dki:,}</strong><br>
            🔴 <strong>Butuh supply dari provinsi tetangga</strong>
        </div>
    </div>""", unsafe_allow_html=True)

# KAPABILITAS — clickable cards with page links
st.markdown("---")
st.markdown("### 🧩 Satu Platform Traceability, Lima Kapabilitas")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <a href="/Farmer_Dashboard" target="_self" style="text-decoration:none;">
    <div class="np-card" style="text-align:center;min-height:170px;padding:20px;cursor:pointer;border-top:4px solid #4CAF50;">
        <div style="font-size:2.5rem;">👨‍🌾</div>
        <div style="font-size:1rem;font-weight:700;color:#1B5E20;margin-top:6px;">Identitas Petani</div>
        <div style="font-size:0.82rem;color:#666;margin-top:4px;">Verifikasi Dukcapil, credit scoring, akses KUR digital</div>
    </div></a>""", unsafe_allow_html=True)
with col2:
    st.markdown("""
    <a href="/QR_Trace" target="_self" style="text-decoration:none;">
    <div class="np-card" style="text-align:center;min-height:170px;padding:20px;cursor:pointer;border-top:4px solid #2196F3;">
        <div style="font-size:2.5rem;">🔍</div>
        <div style="font-size:1rem;font-weight:700;color:#0D47A1;margin-top:6px;">QR Traceability</div>
        <div style="font-size:0.82rem;color:#666;margin-top:4px;">Lacak beras dari sawah ke piring siswa + audit trail</div>
    </div></a>""", unsafe_allow_html=True)
with col3:
    st.markdown("""
    <a href="/Command_Center" target="_self" style="text-decoration:none;">
    <div class="np-card" style="text-align:center;min-height:170px;padding:20px;cursor:pointer;border-top:4px solid #1A237E;">
        <div style="font-size:2.5rem;">🏛️</div>
        <div style="font-size:1rem;font-weight:700;color:#1A237E;margin-top:6px;">Dashboard Pemerintah</div>
        <div style="font-size:0.82rem;color:#666;margin-top:4px;">Price Radar, MBG Monitor, early warning inflasi</div>
    </div></a>""", unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)
with col4:
    st.markdown("""
    <a href="/AgriMart" target="_self" style="text-decoration:none;">
    <div class="np-card" style="text-align:center;min-height:170px;padding:20px;cursor:pointer;border-top:4px solid #E65100;">
        <div style="font-size:2.5rem;">🛒</div>
        <div style="font-size:1rem;font-weight:700;color:#E65100;margin-top:6px;">Marketplace F2C</div>
        <div style="font-size:0.82rem;color:#666;margin-top:4px;">Petani jual langsung ke SPPG, memangkas rantai distribusi</div>
    </div></a>""", unsafe_allow_html=True)
with col5:
    st.markdown("""
    <a href="/PanganLink" target="_self" style="text-decoration:none;">
    <div class="np-card" style="text-align:center;min-height:170px;padding:20px;cursor:pointer;border-top:4px solid #7C3AED;">
        <div style="font-size:2.5rem;">🔗</div>
        <div style="font-size:1rem;font-weight:700;color:#7C3AED;margin-top:6px;">AI Matching</div>
        <div style="font-size:0.82rem;color:#666;margin-top:4px;">LSTM prediksi + matching surplus Banten → defisit DKI</div>
    </div></a>""", unsafe_allow_html=True)
with col6:
    st.markdown("""
    <a href="/SmartDistrib" target="_self" style="text-decoration:none;">
    <div class="np-card" style="text-align:center;min-height:170px;padding:20px;cursor:pointer;border-top:4px solid #00897B;">
        <div style="font-size:2.5rem;">🚛</div>
        <div style="font-size:1rem;font-weight:700;color:#00897B;margin-top:6px;">IoT Cold-Chain</div>
        <div style="font-size:0.82rem;color:#666;margin-top:4px;">Pantau suhu dan lokasi armada, cari rute terbaik otomatis</div>
    </div></a>""", unsafe_allow_html=True)

# MBG CONTEXT
st.markdown("---")
st.markdown("### 📖 Program MBG 2026")
st.markdown("""
| Indikator | Nilai |
|---|---|
| 💰 Anggaran | **Rp 268 triliun** (UU APBN 2026) |
| 👥 Penerima | **61,96 juta jiwa** |
| 🏭 SPPG | **27.735 dapur** |
| 🏫 Satuan pendidikan | **280.023 sekolah** |
""")

st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#888;padding:1rem 0;font-size:0.8rem;">
    <strong style="color:#1B5E20;">🌾 NusaPangan</strong> · Tim We Are Solution · PIDI DIGDAYA × HACKATHON 2026<br>
    Data: SP2KP Kemendag · BPS · Kemendikdasmen · Kementan · Bank Indonesia
</div>
""", unsafe_allow_html=True)
