"""
🌾 NusaPangan — Farm-to-Fork Traceability for MBG
"Setiap porsi makan bergizi gratis dapat ditelusuri hingga petani yang menanamnya"
"""
import streamlit as st
import pandas as pd
import os, sys

st.set_page_config(page_title="NusaPangan — Farm to Fork", page_icon="🌾", layout="wide", initial_sidebar_state="expanded")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import load_data, COMMON_CSS

st.markdown(COMMON_CSS, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("assets/logo.png", width=150)
    st.markdown("**Dari Sawah ke Piring Anak Indonesia**")
    st.markdown("---")
    st.markdown("##### Tim We Are Solution")
    st.markdown("PIDI DIGDAYA × HACKATHON 2026")
    st.markdown("---")
    st.markdown("""
    **Sumber Data:**
    - SP2KP Kemendag 2026 (PIHPS)
    - BPS Produksi Padi 2026
    - Kemendikdasmen MBG
    - Kementan/BPS Ekspor 2025
    - Bank Indonesia Inflasi
    """)

# Load real data
df_farmers = load_data("farmers.csv")
df_journeys = load_data("journeys.csv")
df_harga = load_data("harga_beras_pihps.csv")
df_produksi = load_data("produksi_padi_bps.csv")
df_mbg = load_data("mbg_satpen.csv")

# ================================================================
# HERO HEADER — Narasi utama
# ================================================================
st.markdown("""
<div class="np-header" style="background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 50%, #43A047 100%); box-shadow: 0 8px 32px rgba(27,94,32,0.3);">
    <p style="font-size: 0.8rem; opacity: 0.7; margin-bottom: 8px;">Platform Traceability MBG · Data Real PIHPS + BPS</p>
    <h2 style="font-size: 1.6rem;">🌾 NusaPangan</h2>
    <p style="font-size: 1.05rem; line-height: 1.6; margin-top: 8px;">
        <em>"Setiap porsi makan bergizi gratis yang diterima anak Indonesia<br>
        dapat ditelusuri kembali hingga petani yang menanamnya."</em>
    </p>
    <p style="font-size: 0.75rem; opacity: 0.5; margin-top: 8px;">Dari Sawah Banten ke Piring Siswa DKI Jakarta</p>
</div>
""", unsafe_allow_html=True)

# ================================================================
# KEY STATS dari data real
# ================================================================
total_farmers = len(df_farmers)
total_journeys = len(df_journeys)
total_mbg_dki = df_mbg[df_mbg["provinsi"]=="DKI Jakarta"]["jumlah_satpen"].sum()
total_mbg_banten = df_mbg[df_mbg["provinsi"]=="Banten"]["jumlah_satpen"].sum()
avg_harga_dki = df_harga[df_harga["provinsi"]=="DKI Jakarta"]["harga_beras_medium_kg"].mean()
avg_harga_banten = df_harga[df_harga["provinsi"]=="Banten"]["harga_beras_medium_kg"].mean()
gap_harga = avg_harga_dki - avg_harga_banten

st.markdown("### 📊 Data Real — Banten vs DKI Jakarta")
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("👨‍🌾 Petani Banten", f"{total_farmers}", "Verified Dukcapil")
c2.metric("🔍 Journey Tracked", f"{total_journeys}", "Banten → DKI")
c3.metric("🏫 Satpen MBG DKI", f"{total_mbg_dki:,}", "SD+SMP+SMA")
c4.metric("🏫 Satpen MBG Banten", f"{total_mbg_banten:,}", "SD+SMP+SMA")
c5.metric("💰 Gap Harga Beras", f"Rp {gap_harga:,.0f}/kg", "DKI vs Banten")

st.markdown('<p class="np-source">Sumber: SP2KP Kemendag, BPS, Kemendikdasmen 2026</p>', unsafe_allow_html=True)

# ================================================================
# MASALAH — kenapa NusaPangan dibutuhkan
# ================================================================
st.markdown("---")
st.markdown("### ❓ Mengapa NusaPangan Dibutuhkan?")

st.markdown("""
Program MBG mengalirkan **Rp 335 triliun per tahun** untuk memberi makan **62 juta anak** 
di **280.023 sekolah**. Namun supply chain-nya masih gelap:
""")

p1, p2, p3 = st.columns(3)
with p1:
    st.markdown("""
    <div class="np-card" style="padding:16px;">
        <div style="font-size:1.5rem;margin-bottom:4px;">🔍</div>
        <div style="font-size:0.9rem;font-weight:700;">Tidak Ada Traceability</div>
        <div style="font-size:0.8rem;color:#666;margin-top:4px;">Dari mana bahan makanan MBG? Melewati tangan siapa? Tidak ada yang tahu.</div>
    </div>""", unsafe_allow_html=True)
with p2:
    st.markdown("""
    <div class="np-card" style="padding:16px;">
        <div style="font-size:1.5rem;margin-bottom:4px;">💸</div>
        <div style="font-size:0.9rem;font-weight:700;">Potensi Kebocoran Subsidi</div>
        <div style="font-size:0.8rem;color:#666;margin-top:4px;">Riset IPB: 32% petani tak tercatat, 68% penerima subsidi bukan petani aktif.</div>
    </div>""", unsafe_allow_html=True)
with p3:
    st.markdown("""
    <div class="np-card" style="padding:16px;">
        <div style="font-size:1.5rem;margin-bottom:4px;">🗑️</div>
        <div style="font-size:0.9rem;font-weight:700;">Food Loss Masif</div>
        <div style="font-size:0.8rem;color:#666;margin-top:4px;">Bappenas: 23-48 juta ton pangan terbuang per tahun. Senilai ratusan triliun rupiah.</div>
    </div>""", unsafe_allow_html=True)

# ================================================================
# BANTEN vs DKI — the story
# ================================================================
st.markdown("---")
st.markdown("### 🗺️ Studi Kasus: Banten → DKI Jakarta")

col_a, col_b = st.columns(2)

prod_banten = df_produksi[df_produksi["provinsi"]=="Banten"]["produksi_ton"].sum()
prod_dki = df_produksi[df_produksi["provinsi"]=="DKI Jakarta"]["produksi_ton"].sum()

with col_a:
    st.markdown(f"""
    <div class="np-card" style="border-left: 4px solid #4CAF50; padding:16px;">
        <div style="font-size:1rem;font-weight:700;color:#1B5E20;">🟢 Banten — Surplus Beras</div>
        <div style="font-size:0.85rem;color:#555;margin-top:8px;line-height:1.8;">
            Produksi Jan-Jun 2026: <strong>{prod_banten:,.0f} ton</strong><br>
            Harga rata-rata: <strong>Rp {avg_harga_banten:,.0f}/kg</strong><br>
            Satpen MBG: <strong>{total_mbg_banten:,}</strong> sekolah<br>
            Petani terdaftar: <strong>{total_farmers}</strong> verified
        </div>
    </div>""", unsafe_allow_html=True)

with col_b:
    st.markdown(f"""
    <div class="np-card" style="border-left: 4px solid #F44336; padding:16px;">
        <div style="font-size:1rem;font-weight:700;color:#C62828;">🔴 DKI Jakarta — Defisit Total</div>
        <div style="font-size:0.85rem;color:#555;margin-top:8px;line-height:1.8;">
            Produksi Jan-Jun 2026: <strong>{prod_dki:,.1f} ton</strong> (hampir nol)<br>
            Harga rata-rata: <strong>Rp {avg_harga_dki:,.0f}/kg</strong><br>
            Satpen MBG: <strong>{total_mbg_dki:,}</strong> sekolah<br>
            <strong>Butuh supply dari provinsi tetangga</strong>
        </div>
    </div>""", unsafe_allow_html=True)

st.markdown(f"""
> **Gap harga Rp {gap_harga:,.0f}/kg** antara Banten dan DKI Jakarta menunjukkan inefisiensi rantai pasok. 
> NusaPangan menghubungkan petani Banten langsung ke SPPG Jakarta — memangkas rantai distribusi, 
> menekan harga untuk konsumen, dan meningkatkan pendapatan petani.
""")

# ================================================================
# KAPABILITAS — bukan "5 modul terpisah" tapi "1 platform, 5 kapabilitas"
# ================================================================
st.markdown("---")
st.markdown("### 🧩 Satu Platform Traceability, Lima Kapabilitas")
st.markdown("*NusaPangan bukan 5 produk terpisah — melainkan satu ekosistem terintegrasi yang menjawab seluruh rantai pasok MBG.*")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="np-card" style="text-align:center;min-height:160px;">
        <div style="font-size:2.5rem;">👨‍🌾</div>
        <div style="font-size:1rem;font-weight:700;color:#1B5E20;">Identitas Petani</div>
        <div style="font-size:0.8rem;color:#666;">Verifikasi Dukcapil, credit scoring, akses KUR digital</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="np-card" style="text-align:center;min-height:160px;">
        <div style="font-size:2.5rem;">🔍</div>
        <div style="font-size:1rem;font-weight:700;color:#1B5E20;">QR Traceability</div>
        <div style="font-size:0.8rem;color:#666;">Lacak beras dari sawah ke piring siswa + audit trail</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="np-card" style="text-align:center;min-height:160px;">
        <div style="font-size:2.5rem;">🏛️</div>
        <div style="font-size:1rem;font-weight:700;color:#1B5E20;">Dashboard Pemerintah</div>
        <div style="font-size:0.8rem;color:#666;">Price Radar, MBG Monitor, early warning inflasi</div>
    </div>""", unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)
with col4:
    st.markdown("""
    <div class="np-card" style="text-align:center;min-height:160px;">
        <div style="font-size:2.5rem;">🛒</div>
        <div style="font-size:1rem;font-weight:700;color:#1B5E20;">Marketplace F2C</div>
        <div style="font-size:0.8rem;color:#666;">Petani jual langsung ke SPPG, memangkas rantai distribusi</div>
    </div>""", unsafe_allow_html=True)
with col5:
    st.markdown("""
    <div class="np-card" style="text-align:center;min-height:160px;">
        <div style="font-size:2.5rem;">🔗</div>
        <div style="font-size:1rem;font-weight:700;color:#1B5E20;">AI Matching Supply-Demand</div>
        <div style="font-size:0.8rem;color:#666;">LSTM prediksi + matching surplus Banten → defisit DKI</div>
    </div>""", unsafe_allow_html=True)
with col6:
    st.markdown("""
    <div class="np-card" style="text-align:center;min-height:160px;">
        <div style="font-size:2.5rem;">🚛</div>
        <div style="font-size:1rem;font-weight:700;color:#1B5E20;">IoT Cold-Chain</div>
        <div style="font-size:0.8rem;color:#666;">Sensor suhu/GPS real-time, optimasi rute distribusi</div>
    </div>""", unsafe_allow_html=True)

# ================================================================
# KONTEKS MBG
# ================================================================
st.markdown("---")
st.markdown("### 📖 Konteks Program MBG 2026")
st.markdown("""
| Indikator | Nilai |
|---|---|
| 💰 Anggaran 2026 | **Rp 335 triliun** |
| 👥 Penerima manfaat | **61,96 juta jiwa** |
| 🏭 Jumlah SPPG | **27.735 dapur** |
| 🏫 Satuan pendidikan | **280.023 sekolah** |

> NusaPangan tidak menciptakan pasar baru — melainkan memperkuat transparansi 
> dan efisiensi supply chain MBG yang sudah pasti ada.
""")

# ================================================================
# FOOTER
# ================================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #999; padding: 1rem 0;">
    <p><strong>🌾 NusaPangan</strong> — Tim We Are Solution</p>
    <p>PIDI DIGDAYA × HACKATHON 2026</p>
    <p style="font-size: 0.75rem;">Data: SP2KP Kemendag · BPS · Kemendikdasmen · Kementan · Bank Indonesia</p>
</div>
""", unsafe_allow_html=True)
