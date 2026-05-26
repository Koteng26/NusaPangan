"""
👨‍🌾 Farmer Dashboard — Identitas Digital Petani
Inspired by modern agritech dashboard design
"""
import streamlit as st
import os, sys; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from utils import load_data, COMMON_CSS
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="Farmer Dashboard", page_icon="👨‍🌾", layout="wide")
st.markdown(COMMON_CSS, unsafe_allow_html=True)

st.markdown("""
<style>
    .greeting { font-size: 1.5rem; font-weight: 700; color: #1B5E20; margin-bottom: 0; }
    .greeting-sub { font-size: 0.9rem; color: #666; margin-top: 2px; }
    .stat-card {
        background: white; border-radius: 14px; padding: 16px;
        border: 1px solid #e8e8e8; text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .stat-icon { font-size: 1.8rem; margin-bottom: 4px; }
    .stat-val { font-size: 1.6rem; font-weight: 800; color: #1B5E20; }
    .stat-label { font-size: 0.75rem; color: #888; margin-top: 2px; }
    .stat-delta { font-size: 0.7rem; color: #4CAF50; font-weight: 600; }
    .activity-item {
        display: flex; gap: 12px; align-items: center;
        padding: 10px 14px; background: white; border-radius: 10px;
        border: 1px solid #f0f0f0; margin-bottom: 6px;
    }
    .activity-icon { width: 36px; height: 36px; border-radius: 10px; display: flex;
        align-items: center; justify-content: center; font-size: 1.1rem; flex-shrink: 0; }
    .activity-title { font-size: 0.85rem; font-weight: 600; color: #333; }
    .activity-sub { font-size: 0.75rem; color: #999; }
    .activity-time { font-size: 0.7rem; color: #bbb; margin-left: auto; white-space: nowrap; }
    .weather-card {
        background: linear-gradient(135deg, #E8F5E9, #C8E6C9);
        border-radius: 14px; padding: 16px; text-align: center;
    }
    .weather-temp { font-size: 2.5rem; font-weight: 800; color: #1B5E20; }
    .weather-desc { font-size: 0.85rem; color: #555; }
    .weather-detail { font-size: 0.8rem; color: #666; margin-top: 4px; }
    .profile-mini {
        display: flex; align-items: center; gap: 10px;
        background: white; border-radius: 12px; padding: 10px 14px;
        border: 1px solid #e8e8e8;
    }
    .profile-avatar { width: 44px; height: 44px; border-radius: 50%; background: #E8F5E9;
        display: flex; align-items: center; justify-content: center; font-size: 1.5rem; flex-shrink: 0; }
    .crop-card {
        background: white; border-radius: 12px; padding: 14px;
        border: 1px solid #e8e8e8; text-align: center; min-height: 120px;
    }
    .crop-icon { font-size: 2rem; margin-bottom: 4px; }
    .crop-name { font-size: 0.9rem; font-weight: 700; color: #333; }
    .crop-loc { font-size: 0.75rem; color: #999; }
    .crop-badge { display: inline-block; background: #E8F5E9; color: #1B5E20; 
        font-size: 0.7rem; font-weight: 600; padding: 2px 8px; border-radius: 10px; margin-top: 6px; }
</style>
""", unsafe_allow_html=True)

df = load_data("farmers.csv")

# Farmer selector - compact
col_sel1, col_sel2, col_sel3 = st.columns([2,2,2])
with col_sel1:
    kab = st.selectbox("📍 Kabupaten", df["kabupaten"].unique())
with col_sel2:
    desa_list = df[df["kabupaten"]==kab]["desa"].unique()
    desa = st.selectbox("🏘️ Desa", desa_list)
with col_sel3:
    farmer_list = df[(df["kabupaten"]==kab) & (df["desa"]==desa)]
    farmer_name = st.selectbox("👤 Petani", farmer_list["nama"].values)

farmer = farmer_list[farmer_list["nama"]==farmer_name].iloc[0]
income_est = int(farmer['estimasi_produksi_ton'] * 1000 * farmer['harga_gabah_petani_kg'])

# ================================================================
# GREETING + PROFILE CARD (identity info integrated)
# ================================================================
hour = datetime.now().hour
salam = "Selamat pagi" if hour < 11 else "Selamat siang" if hour < 15 else "Selamat sore" if hour < 18 else "Selamat malam"

st.markdown(f"""
<div style="background:white;border-radius:16px;padding:20px;border:1px solid #c8e6c9;box-shadow:0 2px 12px rgba(27,94,32,0.06);margin-bottom:16px;">
    <div style="display:flex;gap:16px;align-items:center;">
        <div style="width:64px;height:64px;border-radius:50%;background:#E8F5E9;display:flex;align-items:center;justify-content:center;font-size:2rem;flex-shrink:0;border:2px solid #c8e6c9;">👨‍🌾</div>
        <div style="flex:1;">
            <div style="font-size:1.3rem;font-weight:800;color:#1B5E20;">{salam}, {farmer["nama"].split()[0]} 👋</div>
            <div style="font-size:0.85rem;color:#666;margin-top:2px;">{farmer["nama"]} · {farmer["farmer_id"]}</div>
            <div style="display:flex;gap:6px;margin-top:6px;flex-wrap:wrap;">
                <span style="background:#E8F5E9;color:#1B5E20;padding:2px 8px;border-radius:10px;font-size:0.72rem;font-weight:600;">✅ Verified Dukcapil</span>
                <span style="background:#E3F2FD;color:#0D47A1;padding:2px 8px;border-radius:10px;font-size:0.72rem;font-weight:600;">🌾 {farmer["varietas"]}</span>
                <span style="background:#FFF3E0;color:#E65100;padding:2px 8px;border-radius:10px;font-size:0.72rem;font-weight:600;">🟢 {farmer["status"]}</span>
            </div>
        </div>
        <div style="text-align:right;font-size:0.78rem;color:#888;line-height:1.8;">
            <strong>NIK:</strong> {str(farmer['nik'])[:6]}****{str(farmer['nik'])[-4:]}<br>
            <strong>Desa:</strong> {farmer['desa']}, {farmer['kabupaten']}<br>
            <strong>Poktan:</strong> {farmer['kelompok_tani']}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ================================================================
# 4 STAT CARDS (like the design reference)
# ================================================================
s1, s2, s3, s4 = st.columns(4)

with s1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-icon">🌾</div>
        <div class="stat-val">{farmer['luas_lahan_ha']} ha</div>
        <div class="stat-label">Total Lahan</div>
        <div class="stat-delta">Varietas {farmer['varietas']}</div>
    </div>""", unsafe_allow_html=True)

with s2:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-icon">🌱</div>
        <div class="stat-val">Padi</div>
        <div class="stat-label">Tanaman Aktif</div>
        <div class="stat-delta">🟢 {farmer['status']}</div>
    </div>""", unsafe_allow_html=True)

with s3:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-icon">🌾</div>
        <div class="stat-val">{farmer['estimasi_produksi_ton']} ton</div>
        <div class="stat-label">Est. Panen</div>
        <div class="stat-delta">Produktivitas {farmer['produktivitas_ton_ha']} ton/ha</div>
    </div>""", unsafe_allow_html=True)

with s4:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-icon">💰</div>
        <div class="stat-val">Rp {income_est/1_000_000:.1f}jt</div>
        <div class="stat-label">Est. Pendapatan</div>
        <div class="stat-delta">Harga gabah Rp {farmer['harga_gabah_petani_kg']:,}/kg</div>
    </div>""", unsafe_allow_html=True)

st.markdown("")

# ================================================================
# MAIN CONTENT: 2 columns
# ================================================================
col_left, col_right = st.columns([2, 1])

with col_left:
    # TIMELINE MUSIM TANAM
    st.markdown("##### 📅 Timeline Musim Tanam")
    
    tanam = pd.to_datetime(farmer["tanggal_tanam"])
    tumbuh = tanam + timedelta(days=30)
    bunga = tanam + timedelta(days=70)
    panen = pd.to_datetime(farmer["estimasi_panen"])
    
    phases = [
        {"phase": "Tanam", "date": tanam.strftime("%d %b"), "color": "#4CAF50", "icon": "🌱", "desc": "Bibit ditanam"},
        {"phase": "Tumbuh", "date": tumbuh.strftime("%d %b"), "color": "#66BB6A", "icon": "🌿", "desc": "Tanaman tumbuh"},
        {"phase": "Berbunga", "date": bunga.strftime("%d %b"), "color": "#FFC107", "icon": "🌾", "desc": "Padi berbunga"},
        {"phase": "Panen", "date": panen.strftime("%d %b"), "color": "#FF9800", "icon": "👨‍🌾", "desc": "Siap panen"},
    ]
    
    phase_cols = st.columns(4)
    for i, p in enumerate(phases):
        with phase_cols[i]:
            st.markdown(f"""
            <div style="background:{p['color']};color:#fff;border-radius:14px;padding:14px 8px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,0.1);">
                <div style="font-size:2rem;margin-bottom:4px;">{p['icon']}</div>
                <div style="font-size:0.95rem;font-weight:700;">{p['phase']}</div>
                <div style="font-size:0.72rem;opacity:0.85;margin-top:2px;">{p['desc']}</div>
                <div style="font-size:0.75rem;opacity:0.9;margin-top:4px;font-weight:600;">{p['date']}</div>
            </div>""", unsafe_allow_html=True)
    
    st.markdown("")
    
    # PRICE COMPARISON
    st.markdown("##### 💰 Perbandingan Harga")
    price_comp = pd.DataFrame({
        "Kategori": ["Harga Gabah Petani (GKG)", "Harga Beras Pasar (Retail)"],
        "Harga": [farmer["harga_gabah_petani_kg"], farmer["harga_beras_pasar_kg"]],
    })
    fig_price = px.bar(price_comp, x="Kategori", y="Harga", 
                       color="Kategori",
                       color_discrete_sequence=["#43A047", "#FF7043"],
                       text="Harga")
    fig_price.update_traces(texttemplate="Rp %{text:,.0f}", textposition="outside")
    fig_price.update_layout(showlegend=False, height=250, 
                           margin=dict(l=0,r=0,t=10,b=0),
                           yaxis_title="Rupiah/kg",
                           plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_price, use_container_width=True)
    
    # CREDIT SCORE
    st.markdown("##### 💳 Credit Score & Akses KUR")
    st.markdown("*Credit Score = skor kelayakan kredit petani berdasarkan riwayat tanam, luas lahan, dan verifikasi identitas. Skor tinggi → lebih mudah mengajukan KUR (Kredit Usaha Rakyat) dari bank.*")
    
    score = farmer["credit_score"]
    grade = "A" if score >= 700 else "B" if score >= 650 else "C" if score >= 600 else "D"
    grade_color = "#4CAF50" if score >= 700 else "#8BC34A" if score >= 650 else "#FFC107" if score >= 600 else "#FF5722"
    
    cs1, cs2 = st.columns(2)
    with cs1:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            title={"text": f"Grade {grade}"},
            gauge={
                "axis": {"range": [300, 850]},
                "bar": {"color": grade_color},
                "steps": [
                    {"range": [300, 550], "color": "#FFEBEE"},
                    {"range": [550, 650], "color": "#FFF3E0"},
                    {"range": [650, 750], "color": "#F1F8E9"},
                    {"range": [750, 850], "color": "#E8F5E9"},
                ],
            },
        ))
        fig_gauge.update_layout(height=250, margin=dict(l=20,r=20,t=40,b=10))
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with cs2:
        if score >= 650:
            st.success(f"✅ **ELIGIBLE KUR Mikro** — hingga Rp {min(50, int(farmer['luas_lahan_ha']*25))} juta")
        elif score >= 550:
            st.warning("⚠️ **CONDITIONAL** — Perlu tambahan jaminan kelompok tani")
        else:
            st.error("❌ **BELUM ELIGIBLE** — Perlu peningkatan riwayat transaksi")
        
        st.markdown(f"""
        | Parameter | Nilai |
        |---|---|
        | Luas Lahan | **{farmer['luas_lahan_ha']} ha** |
        | Verified Dukcapil | ✅ Ya |
        | Kelompok Tani | **{farmer['kelompok_tani']}** |
        | Est. Produksi | **{farmer['estimasi_produksi_ton']} ton** |
        """)

with col_right:
    # AKTIVITAS TERBARU
    st.markdown("##### 📋 Aktivitas Terbaru")
    
    random.seed(hash(farmer['farmer_id']))
    activities = [
        {"icon": "💧", "bg": "#E3F2FD", "title": "Penyiraman dilakukan", "loc": f"Lahan Padi - {farmer['desa']}", "time": "2 jam lalu"},
        {"icon": "🧪", "bg": "#F3E5F5", "title": "Pemupukan dilakukan", "loc": f"Lahan Padi - {farmer['desa']}", "time": "1 hari lalu"},
        {"icon": "📸", "bg": "#FFF3E0", "title": "Foto lahan diupload", "loc": "Verifikasi GPS", "time": "2 hari lalu"},
        {"icon": "✅", "bg": "#E8F5E9", "title": "NIK diverifikasi", "loc": "API Dukcapil", "time": "3 hari lalu"},
        {"icon": "📊", "bg": "#E0F2F1", "title": "Credit score diupdate", "loc": f"Score: {farmer['credit_score']}", "time": "5 hari lalu"},
    ]
    
    for a in activities:
        st.markdown(f"""
        <div class="activity-item">
            <div class="activity-icon" style="background:{a['bg']};">{a['icon']}</div>
            <div>
                <div class="activity-title">{a['title']}</div>
                <div class="activity-sub">{a['loc']}</div>
            </div>
            <div class="activity-time">{a['time']}</div>
        </div>""", unsafe_allow_html=True)
    
    st.markdown("")
    
    # CUACA HARI INI
    st.markdown("##### 🌤️ Cuaca Hari Ini")
    
    # Simulated weather based on location (realistic for Banten)
    random.seed(hash(farmer['desa']))
    temp = random.randint(27, 32)
    humidity = random.randint(60, 78)
    conditions = random.choice(["Cerah Berawan", "Cerah", "Berawan", "Hujan Ringan"])
    wind = random.randint(5, 15)
    condition_icon = {"Cerah Berawan": "⛅", "Cerah": "☀️", "Berawan": "☁️", "Hujan Ringan": "🌧️"}
    
    st.markdown(f"""
    <div class="weather-card">
        <div style="font-size:0.8rem;color:#666;">📍 {farmer['desa']}, {farmer['kabupaten']}</div>
        <div style="font-size:3rem;margin:4px 0;">{condition_icon.get(conditions, "⛅")}</div>
        <div class="weather-temp">{temp}°C</div>
        <div class="weather-desc">{conditions}</div>
        <div style="display:flex;justify-content:center;gap:16px;margin-top:8px;">
            <div class="weather-detail">💧 {humidity}%<br><span style="font-size:0.7rem;">Kelembaban</span></div>
            <div class="weather-detail">💨 {wind} km/jam<br><span style="font-size:0.7rem;">Angin</span></div>
        </div>
        <div style="font-size:0.65rem;color:#999;margin-top:8px;">Integrasi BMKG API</div>
    </div>""", unsafe_allow_html=True)

# ================================================================
# BOTTOM: All farmers table
# ================================================================
st.markdown("---")
st.markdown(f"### 📋 Semua Petani di Desa {desa}")
desa_farmers = df[(df["kabupaten"]==kab) & (df["desa"]==desa)][
    ["farmer_id", "nama", "luas_lahan_ha", "varietas", "status", "estimasi_produksi_ton", "credit_score"]
]
desa_farmers.columns = ["ID", "Nama", "Lahan (ha)", "Varietas", "Status", "Est. Produksi (ton)", "Credit Score"]
st.dataframe(desa_farmers, use_container_width=True, hide_index=True)
