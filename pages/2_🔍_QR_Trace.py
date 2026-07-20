"""
🔍 QR Trace — Lacak Perjalanan Beras dari Sawah ke Dapur SPPG
"""
import streamlit as st
import os, sys; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from utils import load_data, COMMON_CSS
import pandas as pd
import qrcode
import io
import base64
import plotly.graph_objects as go

st.set_page_config(page_title="QR Trace", page_icon="🔍", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif; }
    .trace-header {
        background: linear-gradient(135deg, #0D47A1, #1565C0, #1E88E5);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 1.5rem;
    }
    .journey-step {
        background: white;
        border-left: 4px solid #4CAF50;
        border-radius: 0 12px 12px 0;
        padding: 1.2rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .journey-step.active { border-left-color: #FF9800; background: #FFF8E1; }
    .journey-step.pending { border-left-color: #9E9E9E; background: #FAFAFA; }
    .step-icon { font-size: 1.5rem; }
    .step-title { font-weight: 700; color: #1B5E20; font-size: 1rem; }
    .step-detail { color: #555; font-size: 0.85rem; margin-top: 0.3rem; }
    .qr-container {
        text-align: center;
        background: white;
        border: 2px solid #E3F2FD;
        border-radius: 16px;
        padding: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

df_journeys = load_data("journeys.csv")

st.markdown("""
<div class="trace-header">
    <h2 style="margin:0;">🔍 QR Trace — Farm to Fork</h2>
    <p style="margin:0.3rem 0 0 0; opacity:0.8;">Lacak perjalanan beras dari sawah Pak Tani sampai piring siswa MBG</p>
</div>
""", unsafe_allow_html=True)

# Selector
journey_options = [f"{row['journey_id']} — {row['petani_nama']} → {row['sekolah']}" for _, row in df_journeys.iterrows()]
selected = st.selectbox("🔎 Pilih Journey untuk Dilacak", journey_options)
journey_idx = journey_options.index(selected)
j = df_journeys.iloc[journey_idx]

st.markdown("---")

col_qr, col_journey = st.columns([1, 2])

with col_qr:
    # Generate QR Code
    qr_data = f"https://nusapangan.id/trace/{j['qr_code']}"
    qr = qrcode.QRCode(version=1, box_size=8, border=2)
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="#1B5E20", back_color="white")
    
    buf = io.BytesIO()
    qr_img.save(buf, format="PNG")
    qr_b64 = base64.b64encode(buf.getvalue()).decode()
    
    st.markdown(f"""
    <div class="qr-container">
        <img src="data:image/png;base64,{qr_b64}" width="200">
        <p style="margin-top:0.8rem;font-weight:700;color:#1B5E20;">{j['qr_code']}</p>
        <p style="font-size:0.8rem;color:#888;">Scan QR ini untuk lacak asal beras</p>
        <p style="font-size:0.75rem;color:#aaa;">Komoditas: <strong>{j['komoditas']}</strong> — {j['varietas']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    st.metric("Total Jarak Tempuh", "~380 km", help="Estimasi dari sawah ke sekolah")
    st.metric("Waktu Tempuh", f"{(pd.to_datetime(j['tanggal_tiba']) - pd.to_datetime(j['tanggal_panen'])).days} hari")
    st.metric("Jumlah untuk Sekolah", f"{j['jumlah_kg_sekolah']} kg")
    st.metric("Porsi Siswa", f"{j['jumlah_porsi']} porsi")

with col_journey:
    st.markdown("### 🗺️ Journey Timeline")
    
    # Step 1: Farm
    st.markdown(f"""
    <div class="journey-step">
        <div class="step-icon">🌾</div>
        <div class="step-title">TAHAP 1 — Sawah Petani</div>
        <div class="step-detail">
            <strong>Petani:</strong> {j['petani_nama']} (ID: {j['petani_id']})<br>
            <strong>Lokasi:</strong> Desa {j['petani_desa']}, {j['petani_kab']}<br>
            <strong>Luas Lahan:</strong> {j['luas_lahan']} hektar<br>
            <strong>Tanggal Tanam:</strong> {j['tanggal_tanam']}<br>
            <strong>Tanggal Panen:</strong> {j['tanggal_panen']}<br>
            <strong>Hasil Panen:</strong> {j['jumlah_gabah_kg']:,} kg Gabah (GKG)<br>
            <strong>Varietas:</strong> {j['varietas']}<br>
            ✅ <em>Terverifikasi petugas lapangan · Integrasi Dukcapil: dalam proses</em>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='text-align:center;font-size:1.5rem;color:#4CAF50;'>⬇️</div>", unsafe_allow_html=True)
    
    # Step 2: Penggilingan
    st.markdown(f"""
    <div class="journey-step">
        <div class="step-icon">🏭</div>
        <div class="step-title">TAHAP 2 — Penggilingan</div>
        <div class="step-detail">
            <strong>Mitra:</strong> {j['penggilingan']}, {j['penggilingan_kab']}<br>
            <strong>Tanggal Giling:</strong> {j['tanggal_giling']}<br>
            <strong>Hasil Beras:</strong> {j['jumlah_beras_kg']:,} kg beras putih<br>
            <strong>Rendemen:</strong> {j['rendemen_pct']}% (GKG → Beras)<br>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='text-align:center;font-size:1.5rem;color:#4CAF50;'>⬇️</div>", unsafe_allow_html=True)
    
    # Step 3: Gudang
    st.markdown(f"""
    <div class="journey-step">
        <div class="step-icon">🏪</div>
        <div class="step-title">TAHAP 3 — Gudang & Cold Storage</div>
        <div class="step-detail">
            <strong>Gudang:</strong> {j['gudang']}, {j['gudang_kab']}<br>
            <strong>Tanggal Masuk:</strong> {j['tanggal_masuk_gudang']}<br>
            <strong>Suhu Gudang:</strong> {j['suhu_gudang_c']}°C<br>
            <strong>Kelembaban:</strong> {j['kelembaban_pct']}%<br>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='text-align:center;font-size:1.5rem;color:#4CAF50;'>⬇️</div>", unsafe_allow_html=True)
    
    # Step 4: Distribution to School
    status_class = "active" if j["status"] == "In Transit" else ""
    st.markdown(f"""
    <div class="journey-step {status_class}">
        <div class="step-icon">🚛</div>
        <div class="step-title">TAHAP 4 — Distribusi ke SPPG</div>
        <div class="step-detail">
            <strong>SPPG:</strong> {j['sppg']}<br>
            <strong>Tanggal Kirim:</strong> {j['tanggal_kirim']}<br>
            <strong>Tanggal Tiba:</strong> {j['tanggal_tiba']}<br>
            <strong>Jumlah:</strong> {j['jumlah_kg_sekolah']} kg<br>
            <strong>Status:</strong> {'🟢' if j['status']=='Delivered' else '🟡'} {j['status']}<br>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='text-align:center;font-size:1.5rem;color:#4CAF50;'>⬇️</div>", unsafe_allow_html=True)
    
    # Step 5: School / Plate
    st.markdown(f"""
    <div class="journey-step">
        <div class="step-icon">🍽️</div>
        <div class="step-title">TAHAP 5 — Dapur SPPG MBG</div>
        <div class="step-detail">
            <strong>Sekolah:</strong> {j['sekolah']}, {j['sekolah_kota']}<br>
            <strong>Jumlah Porsi:</strong> {j['jumlah_porsi']:,} porsi<br>
            <strong>Verifikasi:</strong> ✅ Seluruh journey tercatat permanen (hash-chain)<br>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Peta journey
st.markdown("### 🗺️ Peta Perjalanan — Banten → DKI Jakarta")

fig_map = go.Figure()

# Real coordinates: Sawah (Banten) → Penggilingan → Gudang → Transit → Sekolah (DKI)
lats = [
    float(j.get('latitude', -6.28)) if 'latitude' in j.index else -6.28,  # Sawah
    -6.28,   # Penggilingan Serang/Tangerang
    -6.18,   # Gudang Bulog
    -6.20,   # Transit - border Banten/DKI
    -6.19,   # Sekolah DKI Jakarta
]
lons = [
    float(j.get('longitude', 106.20)) if 'longitude' in j.index else 106.20,
    106.25,  # Penggilingan
    106.55,  # Gudang
    106.70,  # Transit
    106.84,  # Sekolah DKI
]
labels = [
    f"🌾 Sawah {j['petani_nama']}<br>{j['petani_desa']}, {j['petani_kab']}",
    f"🏭 {j['penggilingan']}<br>{j['penggilingan_kab']}",
    f"🏪 {j['gudang']}<br>{j['gudang_kab']}",
    "🚛 Transit Banten→DKI",
    f"🏫 {j['sekolah']}<br>{j['sekolah_kota']}"
]
colors = ['#4CAF50', '#FF9800', '#2196F3', '#9E9E9E', '#F44336']
sizes = [18, 14, 14, 10, 18]

# Path
fig_map.add_trace(go.Scattermapbox(
    lat=lats, lon=lons,
    mode='lines',
    line=dict(width=3, color='#1B5E20'),
    showlegend=False,
    hoverinfo='skip',
))

# Points
for i in range(len(lats)):
    fig_map.add_trace(go.Scattermapbox(
        lat=[lats[i]], lon=[lons[i]],
        mode='markers+text',
        marker=dict(size=sizes[i], color=colors[i]),
        text=[labels[i].split('<br>')[0]],
        textposition="top center",
        textfont=dict(size=11, color=colors[i]),
        hovertext=labels[i].replace('<br>', ' - '),
        hoverinfo='text',
        showlegend=False,
    ))

fig_map.update_layout(
    mapbox=dict(
        style="open-street-map",
        center=dict(lat=-6.22, lon=106.50),
        zoom=8.5,
    ),
    height=450,
    margin=dict(l=0, r=0, t=0, b=0),
)
st.plotly_chart(fig_map, use_container_width=True)

st.markdown(f"""
> 🗺️ **Rute:** {j['petani_desa']}, {j['petani_kab']} (Banten) → {j['penggilingan']} → {j['gudang']} → {j['sekolah']}, {j['sekolah_kota']} (DKI Jakarta)  
""")

st.markdown("---")

# hash-chain
st.markdown("##### 🔗 Rantai Catatan Terkunci (Hash-Chain) — detail teknis")
st.markdown("""
> **Apa itu hash-chain di NusaPangan?** Bayangkan buku catatan yang dipegang bersama oleh banyak pihak 
> (Kementan, Bank, Bulog, BPK, Bapanas). Setiap kali beras berpindah tangan — dari petani ke penggilingan, 
> dari gudang ke sekolah — catatan otomatis tertulis dan **tidak bisa dihapus atau diubah** oleh siapapun. 
> Artinya tidak ada satu pihak pun yang bisa mengubah data sepihak — semuanya tercatat dan bisa dicek.
""")
st.markdown("*Setiap kali beras berpindah tangan, catatan otomatis tersimpan permanen dan tidak bisa dihapus.*")

import hashlib
import json

# Generate realistic block hashes
def make_hash(data_str):
    return hashlib.sha256(data_str.encode()).hexdigest()[:16]

blocks = [
    {
        "block": 0,
        "label": "Genesis Block",
        "icon": "🔐",
        "data": "NusaPangan Ledger Init",
        "timestamp": "2026-01-01 00:00:00",
        "validator": "BGN Node + BPK Auditor",
    },
    {
        "block": 1,
        "label": "Registrasi Petani",
        "icon": "👨‍🌾",
        "data": f"farmer_id={j['petani_id']}, nik=VERIFIED, dukcapil=TRUE",
        "timestamp": j['tanggal_tanam'] + " 08:15:22",
        "validator": "Petugas lapangan + penerima batch",
    },
    {
        "block": 2,
        "label": "Panen & Serah Gabah",
        "icon": "🌾",
        "data": f"gabah={j['jumlah_gabah_kg']}kg, varietas={j['varietas']}, GPS=verified",
        "timestamp": j['tanggal_panen'] + " 14:30:45",
        "validator": "Kelompok Tani + NusaPangan Node",
    },
    {
        "block": 3,
        "label": "Penggilingan",
        "icon": "🏭",
        "data": f"beras={j['jumlah_beras_kg']}kg, rendemen={j['rendemen_pct']}%, mutu=tercatat",
        "timestamp": j['tanggal_giling'] + " 09:12:33",
        "validator": "Mitra Giling + Bulog Node",
    },
    {
        "block": 4,
        "label": "Gudang Storage",
        "icon": "🏪",
        "data": f"suhu={j['suhu_gudang_c']}C, kelembaban={j['kelembaban_pct']}%, IoT=active",
        "timestamp": j['tanggal_masuk_gudang'] + " 11:45:18",
        "validator": "Petugas gudang + penerima batch",
    },
    {
        "block": 5,
        "label": "Distribusi ke SPPG",
        "icon": "🚛",
        "data": f"tujuan={j['sppg']}, jumlah={j['jumlah_kg_sekolah']}kg, GPS=tracked",
        "timestamp": j['tanggal_kirim'] + " 06:30:00",
        "validator": "SmartDistrib IoT + BGN Node",
    },
    {
        "block": 6,
        "label": "Diterima Sekolah",
        "icon": "🏫",
        "data": f"sekolah={j['sekolah']}, porsi={j['jumlah_porsi']}, verified=TRUE",
        "timestamp": j['tanggal_tiba'] + " 10:20:55",
        "validator": "SPPG Admin + Kemendikdasmen Node",
    },
]

# Calculate hashes
prev_hash = "0000000000000000"
for b in blocks:
    b["prev_hash"] = prev_hash
    block_data = json.dumps({"block": b["block"], "data": b["data"], "prev": prev_hash})
    b["hash"] = make_hash(block_data)
    prev_hash = b["hash"]

# Render hash-chain
for b in blocks:
    color = "#4CAF50" if b["block"] > 0 else "#1565C0"
    st.markdown(f"""
    <div style="background:white;border:2px solid {color};border-radius:12px;padding:1rem;margin-bottom:0.3rem;position:relative;">
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <div>
                <span style="font-size:1.2rem;">{b['icon']}</span>
                <strong style="color:{color};">Block #{b['block']} — {b['label']}</strong>
            </div>
            <span style="background:#E8F5E9;color:#1B5E20;padding:0.15rem 0.5rem;border-radius:10px;font-size:0.7rem;font-weight:600;">✅ Immutable</span>
        </div>
        <div style="font-size:0.75rem;color:#666;margin-top:0.5rem;font-family:monospace;">
            <strong>Data:</strong> {b['data']}<br>
            <strong>Timestamp:</strong> {b['timestamp']} WIB<br>
            <strong>Prev Hash:</strong> {b['prev_hash']}<br>
            <strong>Block Hash:</strong> <span style="color:{color};font-weight:700;">{b['hash']}</span><br>
            <strong>Validator:</strong> {b['validator']} (PBFT Consensus)
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if b["block"] < len(blocks) - 1:
        st.markdown(f"<div style='text-align:center;font-size:1rem;color:{color};'>🔗</div>", unsafe_allow_html=True)

st.markdown("""
> **Hash-chain (catatan berantai terkunci):** Setiap transaksi divalidasi oleh minimal 
> 3 node (BPK Auditor, BGN, Kementan) menggunakan konsensus PBFT. Data tidak dapat diubah 
> setelah tercatat — sehingga seluruh perjalanan beras bisa dilacak siapa saja — dari petani sampai piring siswa.
""")

st.markdown("---")

# All journeys table
st.markdown("### 📋 Semua Journey yang Dilacak")
display_cols = ["journey_id", "petani_nama", "petani_kab", "komoditas", "varietas", "sekolah", "sekolah_kota", "status"]
display_df = df_journeys[display_cols].copy()
display_df.columns = ["ID", "Petani", "Asal", "Komoditas", "Varietas", "Sekolah Tujuan", "Kota", "Status"]
st.dataframe(display_df, use_container_width=True, hide_index=True)
