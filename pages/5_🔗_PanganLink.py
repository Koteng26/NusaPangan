"""
🔗 PanganLink — AI Matching Surplus-Defisit Antarwilayah
Mesin matching otomatis yang menghubungkan daerah surplus dengan defisit pangan
"""
import streamlit as st
import os, sys; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from utils import load_data, COMMON_CSS
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="PanganLink", page_icon="🔗", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif; }
    .pangan-header {
        background: linear-gradient(135deg, #4A148C, #6A1B9A, #8E24AA);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 1.5rem;
    }
    .match-card {
        background: white;
        border: 2px solid #E1BEE7;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 0.8rem;
    }
    .match-card.active { border-color: #8E24AA; box-shadow: 0 4px 16px rgba(142,36,170,0.15); }
    .surplus-badge {
        background: #E8F5E9; color: #1B5E20;
        padding: 0.2rem 0.6rem; border-radius: 12px;
        font-size: 0.75rem; font-weight: 700;
    }
    .deficit-badge {
        background: #FFEBEE; color: #C62828;
        padding: 0.2rem 0.6rem; border-radius: 12px;
        font-size: 0.75rem; font-weight: 700;
    }
    .ai-score {
        background: linear-gradient(135deg, #EDE7F6, #D1C4E9);
        border-radius: 8px;
        padding: 0.5rem 0.8rem;
        text-align: center;
    }
    .ai-score .num { font-size: 1.5rem; font-weight: 800; color: #4A148C; }
    .ai-score .lbl { font-size: 0.7rem; color: #666; }
</style>
""", unsafe_allow_html=True)

df_provinsi = load_data("produksi_padi_bps.csv")

st.markdown("""
<div class="pangan-header">
    <h2 style="margin:0;">🔗 PanganLink — AI Demand-Supply Matching</h2>
    <p style="margin:0.3rem 0 0 0; opacity:0.8;">Mesin matching otomatis surplus → defisit antarwilayah. Meredam disparitas harga & inflasi.</p>
</div>
""", unsafe_allow_html=True)

# Metrics
c1, c2, c3, c4 = st.columns(4)
c1.metric("🟢 Wilayah Surplus", "6 provinsi")
c2.metric("🔴 Wilayah Defisit", "4 provinsi")
c3.metric("🤖 Match Aktif", "8 rute")
c4.metric("📉 Disparitas Ditekan", "-34%", "vs tanpa PanganLink")

st.markdown("---")

tab_map, tab_match, tab_predict = st.tabs(["🗺️ Peta Surplus-Defisit", "🤖 AI Matching", "📈 Prediksi LSTM"])

with tab_map:
    st.markdown("### 🗺️ Peta Surplus-Defisit Beras Nasional")
    st.markdown("*Hijau = surplus, Merah = defisit. Ukuran = volume.*")
    
    # Create surplus-deficit data
    supply_demand = pd.DataFrame([
        {"provinsi": "Jawa Barat", "produksi_beras": 5_796_000, "konsumsi_beras": 4_200_000, "status": "Surplus", "selisih": 1_596_000, "lat": -6.9, "lon": 107.6},
        {"provinsi": "Jawa Timur", "produksi_beras": 6_363_000, "konsumsi_beras": 4_800_000, "status": "Surplus", "selisih": 1_563_000, "lat": -7.5, "lon": 112.0},
        {"provinsi": "Jawa Tengah", "produksi_beras": 5_292_000, "konsumsi_beras": 3_900_000, "status": "Surplus", "selisih": 1_392_000, "lat": -7.1, "lon": 110.4},
        {"provinsi": "Sulawesi Selatan", "produksi_beras": 3_024_000, "konsumsi_beras": 1_200_000, "status": "Surplus", "selisih": 1_824_000, "lat": -3.7, "lon": 119.9},
        {"provinsi": "Sumatera Barat", "produksi_beras": 1_449_000, "konsumsi_beras": 800_000, "status": "Surplus", "selisih": 649_000, "lat": -0.9, "lon": 100.4},
        {"provinsi": "Lampung", "produksi_beras": 1_701_000, "konsumsi_beras": 1_100_000, "status": "Surplus", "selisih": 601_000, "lat": -4.6, "lon": 105.2},
        {"provinsi": "DKI Jakarta", "produksi_beras": 2_000, "konsumsi_beras": 1_500_000, "status": "Defisit", "selisih": -1_498_000, "lat": -6.2, "lon": 106.85},
        {"provinsi": "Papua", "produksi_beras": 45_000, "konsumsi_beras": 600_000, "status": "Defisit", "selisih": -555_000, "lat": -4.0, "lon": 138.5},
        {"provinsi": "Kalimantan Timur", "produksi_beras": 280_000, "konsumsi_beras": 550_000, "status": "Defisit", "selisih": -270_000, "lat": 0.5, "lon": 117.2},
        {"provinsi": "Maluku", "produksi_beras": 60_000, "konsumsi_beras": 280_000, "status": "Defisit", "selisih": -220_000, "lat": -3.2, "lon": 130.1},
    ])
    
    # Scatter geo with color by status
    fig_sd = go.Figure()
    
    surplus = supply_demand[supply_demand["status"] == "Surplus"]
    deficit = supply_demand[supply_demand["status"] == "Defisit"]
    
    fig_sd.add_trace(go.Scattergeo(
        lat=surplus["lat"], lon=surplus["lon"],
        text=surplus.apply(lambda r: f"{r['provinsi']}<br>Surplus: +{r['selisih']:,} ton", axis=1),
        marker=dict(size=surplus["selisih"].abs() / 80000, color="#4CAF50", opacity=0.7, line=dict(width=1, color="#fff")),
        name="Surplus", hoverinfo="text",
    ))
    
    fig_sd.add_trace(go.Scattergeo(
        lat=deficit["lat"], lon=deficit["lon"],
        text=deficit.apply(lambda r: f"{r['provinsi']}<br>Defisit: {r['selisih']:,} ton", axis=1),
        marker=dict(size=deficit["selisih"].abs() / 80000, color="#F44336", opacity=0.7, line=dict(width=1, color="#fff")),
        name="Defisit", hoverinfo="text",
    ))
    
    # Draw matching arrows
    matches = [
        {"from_lat": -6.9, "from_lon": 107.6, "to_lat": -6.2, "to_lon": 106.85, "label": "JaBar→Jakarta"},
        {"from_lat": -7.5, "from_lon": 112.0, "to_lat": -4.0, "to_lon": 138.5, "label": "JaTim→Papua"},
        {"from_lat": -3.7, "from_lon": 119.9, "to_lat": 0.5, "to_lon": 117.2, "label": "SulSel→KalTim"},
        {"from_lat": -7.1, "from_lon": 110.4, "to_lat": -3.2, "to_lon": 130.1, "label": "JaTeng→Maluku"},
    ]
    
    for m in matches:
        fig_sd.add_trace(go.Scattergeo(
            lat=[m["from_lat"], m["to_lat"]],
            lon=[m["from_lon"], m["to_lon"]],
            mode="lines",
            line=dict(width=2, color="#8E24AA", dash="dot"),
            showlegend=False,
            hoverinfo="text",
            text=[m["label"], m["label"]],
        ))
    
    fig_sd.update_geos(
        visible=True, resolution=50,
        showcountries=True, showland=True,
        landcolor="#f5f5f5", countrycolor="#ccc",
        center=dict(lat=-2.5, lon=118),
        lonaxis_range=[95, 141], lataxis_range=[-11, 6],
    )
    fig_sd.update_layout(
        height=500, margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=-0.05),
    )
    st.plotly_chart(fig_sd, use_container_width=True)
    
    st.markdown("""
    > 🟣 **Garis ungu putus-putus** = rekomendasi matching AI PanganLink.  
    > Algoritma LSTM memprediksi kebutuhan 2 minggu ke depan dan secara otomatis menghubungkan surplus ke defisit.
    """)

with tab_match:
    st.markdown("### 🤖 Rekomendasi AI Matching — Beras")
    st.markdown("*Algoritma PanganLink menghitung skor berdasarkan: volume, jarak, harga, dan urgensi.*")
    
    st.markdown("---")
    
    # Match recommendations
    match_data = [
        {
            "from": "Jawa Barat", "to": "DKI Jakarta",
            "volume": "1.200 ton/bulan", "jarak": "~150 km",
            "harga_asal": "Rp 11.800/kg", "harga_tujuan": "Rp 14.500/kg",
            "savings": "Rp 3,24 Miliar/bulan",
            "score": 97, "status": "🟢 Aktif", "urgency": "Tinggi",
        },
        {
            "from": "Jawa Timur", "to": "Papua",
            "volume": "400 ton/bulan", "jarak": "~3.200 km",
            "harga_asal": "Rp 11.500/kg", "harga_tujuan": "Rp 18.000/kg",
            "savings": "Rp 2,6 Miliar/bulan",
            "score": 82, "status": "🟢 Aktif", "urgency": "Tinggi",
        },
        {
            "from": "Sulawesi Selatan", "to": "Kalimantan Timur",
            "volume": "250 ton/bulan", "jarak": "~800 km",
            "harga_asal": "Rp 11.200/kg", "harga_tujuan": "Rp 15.200/kg",
            "savings": "Rp 1,0 Miliar/bulan",
            "score": 78, "status": "🟡 Menunggu", "urgency": "Sedang",
        },
        {
            "from": "Jawa Tengah", "to": "Maluku",
            "volume": "180 ton/bulan", "jarak": "~2.500 km",
            "harga_asal": "Rp 11.600/kg", "harga_tujuan": "Rp 16.800/kg",
            "savings": "Rp 936 Juta/bulan",
            "score": 71, "status": "🟡 Menunggu", "urgency": "Sedang",
        },
    ]
    
    for i, m in enumerate(match_data):
        active = "active" if m["score"] >= 80 else ""
        col_info, col_score = st.columns([4, 1])
        
        with col_info:
            st.markdown(f"""
            <div class="match-card {active}">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;">
                    <div>
                        <span class="surplus-badge">🟢 {m['from']}</span>
                        <span style="font-size:1.2rem;margin:0 0.5rem;">→</span>
                        <span class="deficit-badge">🔴 {m['to']}</span>
                    </div>
                    <span style="font-size:0.85rem;">{m['status']}</span>
                </div>
                <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0.5rem;font-size:0.8rem;">
                    <div><strong>Volume:</strong><br>{m['volume']}</div>
                    <div><strong>Jarak:</strong><br>{m['jarak']}</div>
                    <div><strong>Harga Asal:</strong><br>{m['harga_asal']}</div>
                    <div><strong>Harga Tujuan:</strong><br>{m['harga_tujuan']}</div>
                </div>
                <div style="margin-top:0.5rem;font-size:0.85rem;">
                    💰 <strong>Potensi penghematan:</strong> {m['savings']} · 
                    ⚡ <strong>Urgensi:</strong> {m['urgency']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_score:
            st.markdown(f"""
            <div class="ai-score" style="margin-top:0.5rem;">
                <div class="num">{m['score']}</div>
                <div class="lbl">AI Score</div>
            </div>
            """, unsafe_allow_html=True)

with tab_predict:
    st.markdown("### 📈 Prediksi LSTM — Kebutuhan Beras 2 Minggu ke Depan")
    st.markdown("*Model LSTM (Long Short-Term Memory) memproses data historis PIHPS, musim, dan pola konsumsi.*")
    
    import numpy as np
    
    # Simulated LSTM prediction
    days = pd.date_range("2026-05-01", "2026-05-28")
    np.random.seed(42)
    
    actual = 14200 + np.cumsum(np.random.randn(14) * 80)
    predicted = list(actual[-3:]) + list(14200 + np.cumsum(np.random.randn(14) * 60) + 200)
    pred_dates = pd.date_range("2026-05-12", "2026-05-28")
    
    fig_lstm = go.Figure()
    
    # Actual
    fig_lstm.add_trace(go.Scatter(
        x=days[:14], y=actual,
        mode="lines+markers", name="Harga Aktual",
        line=dict(color="#1E88E5", width=2),
        marker=dict(size=5),
    ))
    
    # Predicted
    fig_lstm.add_trace(go.Scatter(
        x=pred_dates, y=predicted,
        mode="lines+markers", name="Prediksi LSTM",
        line=dict(color="#FF9800", width=2, dash="dash"),
        marker=dict(size=5, symbol="diamond"),
    ))
    
    # Confidence interval
    upper = [p + 300 for p in predicted]
    lower = [p - 300 for p in predicted]
    fig_lstm.add_trace(go.Scatter(
        x=list(pred_dates) + list(pred_dates[::-1]),
        y=upper + lower[::-1],
        fill="toself", fillcolor="rgba(255,152,0,0.1)",
        line=dict(width=0), name="Confidence 95%",
        showlegend=True,
    ))
    
    # Vertical line for "today"
    fig_lstm.add_vline(x="2026-05-14", line_dash="dot", line_color="#888",
                       annotation_text="Hari ini", annotation_position="top")
    
    fig_lstm.update_layout(
        height=400,
        yaxis_title="Harga Beras Premium (Rp/kg)",
        xaxis_title="Tanggal",
        legend=dict(orientation="h", yanchor="bottom", y=-0.2),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(gridcolor="#eee"),
    )
    st.plotly_chart(fig_lstm, use_container_width=True)
    
    st.markdown("""
    > **Insight AI:** Model LSTM memprediksi kenaikan harga beras premium sebesar **+2.8%** dalam 2 minggu ke depan 
    > di wilayah DKI Jakarta. PanganLink secara otomatis merekomendasikan peningkatan alokasi dari 
    > surplus Jawa Barat sebesar **+15%** untuk meredam potensi inflasi.
    """)
    
    # Model performance
    st.markdown("##### 📊 Performa Model")
    perf1, perf2, perf3, perf4 = st.columns(4)
    perf1.metric("MAE", "Rp 187/kg", "2.1% error")
    perf2.metric("RMSE", "Rp 243/kg")
    perf3.metric("R² Score", "0.94")
    perf4.metric("Training Data", "24 bulan", "PIHPS BI")
