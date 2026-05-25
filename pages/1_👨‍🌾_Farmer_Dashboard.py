"""
👨‍🌾 Farmer Dashboard — Identitas Digital Petani
"""
import streamlit as st
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from utils import load_data, COMMON_CSS
import pandas as pd
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from utils import load_data, COMMON_CSS
import plotly.express as px
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from utils import load_data, COMMON_CSS
import plotly.graph_objects as go
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from utils import load_data, COMMON_CSS

st.set_page_config(page_title="Farmer Dashboard", page_icon="👨‍🌾", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif; }
    .farmer-header {
        background: linear-gradient(135deg, #1B5E20, #2E7D32);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 1.5rem;
    }
    .profile-card {
        background: white;
        border: 2px solid #E8F5E9;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }
    .verified-badge {
        background: #E8F5E9;
        color: #1B5E20;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .metric-highlight {
        background: linear-gradient(135deg, #E8F5E9, #C8E6C9);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
    }
    .metric-highlight .number { font-size: 1.8rem; font-weight: 800; color: #1B5E20; }
    .metric-highlight .label { font-size: 0.8rem; color: #555; }
</style>
""", unsafe_allow_html=True)

# Load data
df = load_data("farmers.csv")
df_journeys = load_data("journeys.csv")

st.markdown("""
<div class="farmer-header">
    <h2 style="margin:0;">👨‍🌾 Farmer Dashboard</h2>
    <p style="margin:0.3rem 0 0 0; opacity:0.8;">Identitas Digital Petani — Verifikasi NIK Dukcapil</p>
</div>
""", unsafe_allow_html=True)

# Farmer selector
col_sel1, col_sel2, col_sel3 = st.columns([2,2,2])
with col_sel1:
    kab = st.selectbox("📍 Kabupaten", df["kabupaten"].unique())
with col_sel2:
    desa_list = df[df["kabupaten"]==kab]["desa"].unique()
    desa = st.selectbox("🏘️ Desa", desa_list)
with col_sel3:
    farmer_list = df[(df["kabupaten"]==kab) & (df["desa"]==desa)]
    farmer_name = st.selectbox("👤 Pilih Petani", farmer_list["nama"].values)

farmer = farmer_list[farmer_list["nama"]==farmer_name].iloc[0]

st.markdown("---")

# Profile Card
col_profile, col_stats = st.columns([1, 2])

with col_profile:
    st.markdown(f"""
    <div class="profile-card">
        <div style="text-align:center; margin-bottom:1rem;">
            <div style="width:80px;height:80px;background:#E8F5E9;border-radius:50%;margin:0 auto;display:flex;align-items:center;justify-content:center;font-size:2.5rem;">👨‍🌾</div>
        </div>
        <h3 style="text-align:center;margin:0;color:#1B5E20;">{farmer['nama']}</h3>
        <p style="text-align:center;color:#666;margin:0.3rem 0;">ID: {farmer['farmer_id']}</p>
        <p style="text-align:center;"><span class="verified-badge">✅ Verified Dukcapil</span></p>
        <hr>
        <p><strong>NIK:</strong> {farmer['nik'][:6]}****{farmer['nik'][-4:]}</p>
        <p><strong>Desa:</strong> {farmer['desa']}</p>
        <p><strong>Kabupaten:</strong> {farmer['kabupaten']}</p>
        <p><strong>Kelompok Tani:</strong> {farmer['kelompok_tani']}</p>
        <p><strong>Luas Lahan:</strong> {farmer['luas_lahan_ha']} ha</p>
        <p><strong>Varietas:</strong> {farmer['varietas']}</p>
        <p><strong>Status:</strong> 🟢 {farmer['status']}</p>
    </div>
    """, unsafe_allow_html=True)

with col_stats:
    # Key metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="metric-highlight">
            <div class="number">{farmer['luas_lahan_ha']}</div>
            <div class="label">Hektar Lahan</div>
        </div>""", unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-highlight">
            <div class="number">{farmer['estimasi_produksi_ton']}</div>
            <div class="label">Ton Est. Produksi</div>
        </div>""", unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-highlight">
            <div class="number">{farmer['credit_score']}</div>
            <div class="label">Credit Score</div>
        </div>""", unsafe_allow_html=True)
    with m4:
        income_est = int(farmer['estimasi_produksi_ton'] * 1000 * farmer['harga_gabah_petani_kg'])
        st.markdown(f"""
        <div class="metric-highlight">
            <div class="number">Rp {income_est/1_000_000:.0f}jt</div>
            <div class="label">Est. Pendapatan</div>
        </div>""", unsafe_allow_html=True)
    
    st.markdown("")
    
    # Farming timeline
    st.markdown("##### 📅 Timeline Musim Tanam")
    timeline_data = pd.DataFrame([
        {"Tahap": "Tanam", "Mulai": farmer["tanggal_tanam"], "Status": "✅ Selesai"},
        {"Tahap": "Tumbuh", "Mulai": pd.to_datetime(farmer["tanggal_tanam"]) + pd.Timedelta(days=30), "Status": "✅ Selesai"},
        {"Tahap": "Berbunga", "Mulai": pd.to_datetime(farmer["tanggal_tanam"]) + pd.Timedelta(days=70), "Status": "🔄 Berjalan"},
        {"Tahap": "Panen", "Mulai": farmer["estimasi_panen"], "Status": "⏳ Estimasi"},
    ])
    
    fig_timeline = go.Figure()
    colors = ["#4CAF50", "#66BB6A", "#FFC107", "#FF9800"]
    for i, row in timeline_data.iterrows():
        fig_timeline.add_trace(go.Bar(
            x=[1], y=[row["Tahap"]], orientation='h',
            marker_color=colors[i],
            text=f"{row['Tahap']} — {row['Status']}",
            textposition="inside",
            hoverinfo="text",
        ))
    fig_timeline.update_layout(
        showlegend=False, height=200,
        margin=dict(l=0,r=0,t=10,b=0),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Price comparison
    st.markdown("##### 💰 Perbandingan Harga")
    price_comp = pd.DataFrame({
        "Kategori": ["Harga Gabah Petani\n(per kg GKG)", "Harga Beras Pasar\n(per kg retail)"],
        "Harga": [farmer["harga_gabah_petani_kg"], farmer["harga_beras_pasar_kg"]],
    })
    fig_price = px.bar(price_comp, x="Kategori", y="Harga", 
                       color="Kategori",
                       color_discrete_sequence=["#43A047", "#FF7043"],
                       text="Harga")
    fig_price.update_traces(texttemplate="Rp %{text:,.0f}", textposition="outside")
    fig_price.update_layout(showlegend=False, height=280, 
                           margin=dict(l=0,r=0,t=10,b=0),
                           yaxis_title="Rupiah/kg",
                           plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_price, use_container_width=True)

st.markdown("---")

# Credit Score & KUR Access
st.markdown("### 💳 AgriFinance — Credit Score & Akses KUR")
col_cs, col_kur = st.columns(2)

with col_cs:
    score = farmer["credit_score"]
    if score >= 700:
        grade, color = "A — Excellent", "#4CAF50"
    elif score >= 650:
        grade, color = "B — Good", "#8BC34A"
    elif score >= 600:
        grade, color = "C — Fair", "#FFC107"
    else:
        grade, color = "D — Needs Improvement", "#FF5722"
    
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={"text": f"Credit Score: {grade}"},
        gauge={
            "axis": {"range": [300, 850]},
            "bar": {"color": color},
            "steps": [
                {"range": [300, 550], "color": "#FFEBEE"},
                {"range": [550, 650], "color": "#FFF3E0"},
                {"range": [650, 750], "color": "#F1F8E9"},
                {"range": [750, 850], "color": "#E8F5E9"},
            ],
        },
    ))
    fig_gauge.update_layout(height=300, margin=dict(l=20,r=20,t=50,b=20))
    st.plotly_chart(fig_gauge, use_container_width=True)

with col_kur:
    st.markdown(f"""
    #### Simulasi Akses KUR
    
    Berdasarkan profil petani **{farmer['nama']}**:
    
    | Parameter | Nilai |
    |---|---|
    | Credit Score | **{score}** ({grade.split(' — ')[0]}) |
    | Luas Lahan | **{farmer['luas_lahan_ha']} ha** |
    | Est. Produksi | **{farmer['estimasi_produksi_ton']} ton** |
    | Verified Dukcapil | ✅ **Ya** |
    | Kelompok Tani | **{farmer['kelompok_tani']}** |
    
    **Rekomendasi KUR:**
    """)
    
    if score >= 650:
        st.success(f"✅ **ELIGIBLE** — Petani memenuhi syarat KUR Mikro hingga Rp {min(50, int(farmer['luas_lahan_ha']*25))} juta")
    elif score >= 550:
        st.warning("⚠️ **CONDITIONAL** — Perlu tambahan jaminan kelompok tani")
    else:
        st.error("❌ **BELUM ELIGIBLE** — Perlu peningkatan riwayat transaksi")

st.markdown("---")

# Summary table all farmers in desa
st.markdown(f"### 📋 Semua Petani di Desa {desa}")
desa_farmers = df[(df["kabupaten"]==kab) & (df["desa"]==desa)][
    ["farmer_id", "nama", "luas_lahan_ha", "varietas", "status", "estimasi_produksi_ton", "credit_score"]
]
desa_farmers.columns = ["ID", "Nama", "Lahan (ha)", "Varietas", "Status", "Est. Produksi (ton)", "Credit Score"]
st.dataframe(desa_farmers, use_container_width=True, hide_index=True)
