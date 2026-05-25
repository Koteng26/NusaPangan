"""
🌾 NusaPangan — Farm-to-Fork Traceability System
Banten → DKI Jakarta | Beras Medium | Data Real PIHPS + BPS
"""
import streamlit as st
import pandas as pd
import os, sys

st.set_page_config(page_title="NusaPangan — Farm to Fork", page_icon="🌾", layout="wide", initial_sidebar_state="expanded")

# Add parent dir to path for utils
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import load_data, COMMON_CSS

st.markdown(COMMON_CSS, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🌾 NusaPangan")
    st.markdown("**Farm-to-Fork Traceability**")
    st.markdown("---")
    st.markdown("##### Tim We Are Solution")
    st.markdown("PIDI DIGDAYA × HACKATHON 2026")
    st.markdown("---")
    st.markdown("""
    **Sumber Data Real:**
    - PIHPS (SP2KP Kemendag 2026)
    - BPS Produksi Padi 2026
    - Kemendikdasmen MBG
    - Kementan Ekspor 2025
    - Bank Indonesia Inflasi
    """)

# Load real data
df_farmers = load_data("farmers.csv")
df_journeys = load_data("journeys.csv")
df_harga = load_data("harga_beras_pihps.csv")
df_produksi = load_data("produksi_padi_bps.csv")
df_mbg = load_data("mbg_satpen.csv")

# Header
st.markdown("""
<div class="np-header" style="background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 50%, #43A047 100%); box-shadow: 0 8px 32px rgba(27,94,32,0.3);">
    <div style="display:flex;gap:8px;margin-bottom:8px;">
        <span class="np-badge np-badge-orange">🍽️ MBG Integration</span>
        <span class="np-badge np-badge-green">📊 Data Real PIHPS + BPS</span>
    </div>
    <h2>🌾 NusaPangan</h2>
    <p>Farm-to-Fork Traceability System — Beras Banten → Piring Siswa DKI Jakarta</p>
    <p style="font-size: 0.8rem; opacity: 0.6;">Platform Digital Ketahanan Pangan × Program Makan Bergizi Gratis</p>
</div>
""", unsafe_allow_html=True)

# Key Stats from REAL data
total_farmers = len(df_farmers)
total_journeys = len(df_journeys)
total_mbg_dki = df_mbg[df_mbg["provinsi"]=="DKI Jakarta"]["jumlah_satpen"].sum()
total_mbg_banten = df_mbg[df_mbg["provinsi"]=="Banten"]["jumlah_satpen"].sum()
avg_harga_dki = df_harga[df_harga["provinsi"]=="DKI Jakarta"]["harga_beras_medium_kg"].mean()
avg_harga_banten = df_harga[df_harga["provinsi"]=="Banten"]["harga_beras_medium_kg"].mean()
gap_harga = avg_harga_dki - avg_harga_banten

st.markdown("### 📊 Dashboard Ringkasan — Data Real")
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("👨‍🌾 Petani Banten", f"{total_farmers}", "Verified Dukcapil")
c2.metric("🔍 Journey Tracked", f"{total_journeys}", "Banten → DKI")
c3.metric("🏫 Satpen MBG DKI", f"{total_mbg_dki:,}", "SD+SMP+SMA")
c4.metric("🏫 Satpen MBG Banten", f"{total_mbg_banten:,}", "SD+SMP+SMA")
c5.metric("💰 Gap Harga Beras", f"Rp {gap_harga:,.0f}/kg", "DKI vs Banten")

st.markdown('<p class="np-source">Sumber: SP2KP Kemendag, BPS, Kemendikdasmen 2026</p>', unsafe_allow_html=True)

st.markdown("---")

# Highlight: kenapa Banten → DKI
col_a, col_b = st.columns(2)
with col_a:
    st.markdown("#### 🟢 Banten — Surplus Beras")
    prod_banten = df_produksi[df_produksi["provinsi"]=="Banten"]["produksi_ton"].sum()
    st.markdown(f"""
    - Produksi Jan-Jun 2026: **{prod_banten:,.0f} ton**
    - Harga rata-rata: **Rp {avg_harga_banten:,.0f}/kg**
    - Satpen MBG: **{total_mbg_banten:,}** sekolah
    - Petani terdaftar: **{total_farmers}** verified
    """)

with col_b:
    st.markdown("#### 🔴 DKI Jakarta — Defisit Total")
    prod_dki = df_produksi[df_produksi["provinsi"]=="DKI Jakarta"]["produksi_ton"].sum()
    st.markdown(f"""
    - Produksi Jan-Jun 2026: **{prod_dki:,.1f} ton** (hampir nol!)
    - Harga rata-rata: **Rp {avg_harga_dki:,.0f}/kg**
    - Satpen MBG: **{total_mbg_dki:,}** sekolah
    - **Butuh supply dari luar** → NusaPangan!
    """)

st.markdown("---")

# Module Cards
st.markdown("### 🧩 Modul NusaPangan")
st.markdown("*Gunakan sidebar navigation untuk membuka setiap modul →*")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="np-card" style="text-align:center;min-height:160px;">
        <div style="font-size:2.5rem;">👨‍🌾</div>
        <div style="font-size:1.1rem;font-weight:700;color:#1B5E20;">Farmer Dashboard</div>
        <div style="font-size:0.8rem;color:#666;">Identitas digital, credit score, KUR, income tracking</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="np-card" style="text-align:center;min-height:160px;">
        <div style="font-size:2.5rem;">🔍</div>
        <div style="font-size:1.1rem;font-weight:700;color:#1B5E20;">QR Trace</div>
        <div style="font-size:0.8rem;color:#666;">Journey beras Banten → DKI + blockchain verification</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="np-card" style="text-align:center;min-height:160px;">
        <div style="font-size:2.5rem;">🏛️</div>
        <div style="font-size:1.1rem;font-weight:700;color:#1B5E20;">Command Center</div>
        <div style="font-size:0.8rem;color:#666;">Price Radar PIHPS real, MBG Monitor, Alerts</div>
    </div>""", unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)
with col4:
    st.markdown("""
    <div class="np-card" style="text-align:center;min-height:160px;">
        <div style="font-size:2.5rem;">🛒</div>
        <div style="font-size:1.1rem;font-weight:700;color:#1B5E20;">AgriMart</div>
        <div style="font-size:0.8rem;color:#666;">Marketplace F2C, escrow, eliminasi tengkulak</div>
    </div>""", unsafe_allow_html=True)
with col5:
    st.markdown("""
    <div class="np-card" style="text-align:center;min-height:160px;">
        <div style="font-size:2.5rem;">🔗</div>
        <div style="font-size:1.1rem;font-weight:700;color:#1B5E20;">PanganLink</div>
        <div style="font-size:0.8rem;color:#666;">AI matching Banten surplus → DKI defisit</div>
    </div>""", unsafe_allow_html=True)
with col6:
    st.markdown("""
    <div class="np-card" style="text-align:center;min-height:160px;">
        <div style="font-size:2.5rem;">🚛</div>
        <div style="font-size:1.1rem;font-weight:700;color:#1B5E20;">SmartDistrib</div>
        <div style="font-size:0.8rem;color:#666;">IoT cold-chain, fleet monitor, route AI</div>
    </div>""", unsafe_allow_html=True)

st.markdown("---")

# Context MBG
st.markdown("### 📖 Konteks Program MBG 2026")
st.markdown("""
| Indikator | Nilai |
|---|---|
| 💰 Anggaran 2026 | **Rp 335 triliun** |
| 👥 Penerima manfaat | **61,96 juta jiwa** |
| 🏭 Jumlah SPPG | **27.735 dapur** |
| 🏫 Satuan pendidikan | **280.023 sekolah** |
""")

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #999; padding: 1rem 0;">
    <p><strong>🌾 NusaPangan</strong> — Tim We Are Solution</p>
    <p>PIDI DIGDAYA × HACKATHON 2026 · Digitalisasi Ketahanan Pangan</p>
    <p style="font-size: 0.75rem;">Data real: SP2KP Kemendag, BPS, Kemendikdasmen, Kementan, Bank Indonesia</p>
</div>
""", unsafe_allow_html=True)
