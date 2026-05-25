"""
🚛 SmartDistrib — IoT Cold-Chain & Logistik Cerdas
Sensor IoT real-time (suhu/kelembaban/GPS) + AI routing optimization
"""
import streamlit as st
import os, sys; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from utils import load_data, COMMON_CSS
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(page_title="SmartDistrib", page_icon="🚛", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif; }
    .distrib-header {
        background: linear-gradient(135deg, #004D40, #00695C, #00897B);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 1.5rem;
    }
    .fleet-card {
        background: white;
        border: 1px solid #E0F2F1;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .fleet-card.alert { border-color: #F44336; background: #FFF8F7; }
    .sensor-gauge {
        text-align: center;
        background: linear-gradient(135deg, #E0F2F1, #B2DFDB);
        border-radius: 12px;
        padding: 1rem;
    }
    .sensor-gauge .val { font-size: 2rem; font-weight: 800; }
    .sensor-gauge .lbl { font-size: 0.75rem; color: #555; }
    .sensor-gauge.danger { background: linear-gradient(135deg, #FFEBEE, #FFCDD2); }
    .sensor-gauge.danger .val { color: #C62828; }
    .route-step {
        display: flex; gap: 0.5rem; align-items: center;
        padding: 0.5rem 0;
        border-bottom: 1px dashed #eee;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="distrib-header">
    <h2 style="margin:0;">🚛 SmartDistrib — IoT Cold-Chain & Logistik Cerdas</h2>
    <p style="margin:0.3rem 0 0 0; opacity:0.8;">Sensor suhu/kelembaban/GPS real-time + Algoritma Genetika routing optimization</p>
</div>
""", unsafe_allow_html=True)

# Top metrics
c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("🚛 Armada Aktif", "10", "unit")
c2.metric("📦 Kargo Hari Ini", "8.4 ton")
c3.metric("🌡️ Avg Suhu", "25.3°C", "✅ Normal")
c4.metric("⚠️ Alert Suhu", "1", "armada")
c5.metric("📍 On-Route", "7/10")
c6.metric("📉 FLW Ditekan", "-22%", "vs konvensional")

st.markdown("---")

tab_fleet, tab_iot, tab_route = st.tabs(["🚛 Fleet Monitor", "🌡️ IoT Sensor Live", "🗺️ Route Optimization"])

with tab_fleet:
    st.markdown("### 🚛 Fleet Monitor — Status Armada Real-time")
    
    np.random.seed(42)
    fleet_data = []
    routes = [
        ("Karawang", "Jakarta", 150), ("Subang", "Bandung", 85),
        ("Indramayu", "Semarang", 220), ("Karawang", "Surabaya", 780),
        ("Subang", "Yogyakarta", 350), ("Karawang", "Bandung", 120),
        ("Indramayu", "Jakarta", 200), ("Subang", "Surabaya", 820),
        ("Karawang", "Semarang", 450), ("Indramayu", "Bandung", 180),
    ]
    statuses = ["🟢 On Route", "🟢 On Route", "🟢 On Route", "🟢 On Route",
                "🟢 On Route", "🟢 On Route", "🟢 On Route",
                "📦 Loading", "📦 Loading", "🔴 Alert"]
    
    for i in range(10):
        origin, dest, dist = routes[i]
        suhu = round(np.random.uniform(23, 27) if i != 9 else 32.1, 1)
        kelembaban = round(np.random.uniform(55, 68), 1)
        progress = np.random.randint(20, 95) if i < 7 else (0 if i < 9 else 65)
        
        fleet_data.append({
            "id": f"KRW-{i+1:03d}",
            "origin": origin,
            "dest": dest,
            "kargo": f"{np.random.randint(5, 12) * 100} kg beras",
            "suhu": suhu,
            "kelembaban": kelembaban,
            "dist_km": dist,
            "progress": progress,
            "status": statuses[i],
            "eta": f"{np.random.randint(1, 8)} jam",
            "driver": ["Agus S.", "Rina M.", "Bambang K.", "Doni P.", "Eko W.", 
                       "Fajar H.", "Gilang R.", "Hadi T.", "Irfan A.", "Joko S."][i],
        })
    
    df_fleet = pd.DataFrame(fleet_data)
    
    # Alert card first
    alert_truck = df_fleet[df_fleet["status"] == "🔴 Alert"].iloc[0]
    st.markdown(f"""
    <div class="fleet-card alert" style="margin-bottom:1rem;">
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <div>
                <span style="font-size:1.2rem;">🔴</span>
                <strong style="color:#C62828;">ALERT — Armada {alert_truck['id']}</strong>
            </div>
            <span style="background:#FFEBEE;color:#C62828;padding:0.2rem 0.6rem;border-radius:12px;font-size:0.75rem;font-weight:700;">SUHU KRITIS: {alert_truck['suhu']}°C</span>
        </div>
        <p style="font-size:0.85rem;color:#555;margin:0.5rem 0;">
            <strong>Rute:</strong> {alert_truck['origin']} → {alert_truck['dest']} · 
            <strong>Kargo:</strong> {alert_truck['kargo']} · 
            <strong>Driver:</strong> {alert_truck['driver']}<br>
            <strong>⚡ Aksi Otomatis:</strong> SmartDistrib mengalihkan ke depot pendingin terdekat (Depot Cirebon, 35 km). 
            Notifikasi dikirim ke driver via WhatsApp.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Fleet table
    display_fleet = df_fleet[["id", "driver", "origin", "dest", "kargo", "suhu", "kelembaban", "progress", "status", "eta"]].copy()
    display_fleet.columns = ["Armada", "Driver", "Asal", "Tujuan", "Kargo", "Suhu (°C)", "Kelembaban (%)", "Progress (%)", "Status", "ETA"]
    st.dataframe(display_fleet, use_container_width=True, hide_index=True)

with tab_iot:
    st.markdown("### 🌡️ IoT Sensor Dashboard — Live Monitoring")
    
    # Select truck
    truck_sel = st.selectbox("Pilih Armada", [f"{d['id']} — {d['origin']}→{d['dest']}" for d in fleet_data])
    truck_idx = int(truck_sel.split("-")[1][:3]) - 1
    truck = fleet_data[truck_idx]
    
    st.markdown("---")
    
    # Sensor gauges
    g1, g2, g3, g4 = st.columns(4)
    
    is_danger_temp = truck["suhu"] > 28
    
    with g1:
        st.markdown(f"""
        <div class="sensor-gauge {'danger' if is_danger_temp else ''}">
            <div class="val">🌡️ {truck['suhu']}°C</div>
            <div class="lbl">Suhu Kargo</div>
            <div style="font-size:0.7rem;margin-top:0.3rem;">{'🔴 MELEBIHI BATAS' if is_danger_temp else '✅ Normal (< 28°C)'}</div>
        </div>
        """, unsafe_allow_html=True)
    with g2:
        st.markdown(f"""
        <div class="sensor-gauge">
            <div class="val">💧 {truck['kelembaban']}%</div>
            <div class="lbl">Kelembaban</div>
            <div style="font-size:0.7rem;margin-top:0.3rem;">✅ Normal (55-70%)</div>
        </div>
        """, unsafe_allow_html=True)
    with g3:
        st.markdown(f"""
        <div class="sensor-gauge">
            <div class="val">📍 {truck['progress']}%</div>
            <div class="lbl">Progress Rute</div>
            <div style="font-size:0.7rem;margin-top:0.3rem;">ETA: {truck['eta']}</div>
        </div>
        """, unsafe_allow_html=True)
    with g4:
        speed = np.random.randint(40, 80)
        st.markdown(f"""
        <div class="sensor-gauge">
            <div class="val">🏎️ {speed} km/h</div>
            <div class="lbl">Kecepatan</div>
            <div style="font-size:0.7rem;margin-top:0.3rem;">✅ Dalam batas aman</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")
    
    # Temperature history chart
    st.markdown("##### 📊 Riwayat Suhu Kargo (24 Jam Terakhir)")
    
    hours = pd.date_range(datetime(2026, 5, 14, 0, 0), periods=24, freq="h")
    np.random.seed(truck_idx)
    
    if is_danger_temp:
        temps = list(np.random.uniform(24, 26, 18)) + list(np.linspace(26, 32.1, 6))
    else:
        temps = list(np.random.uniform(23.5, 27, 24))
    
    humidity = list(np.random.uniform(55, 68, 24))
    
    fig_temp = go.Figure()
    fig_temp.add_trace(go.Scatter(
        x=hours, y=temps, mode="lines+markers",
        name="Suhu (°C)", line=dict(color="#FF5722", width=2),
        marker=dict(size=4),
    ))
    fig_temp.add_trace(go.Scatter(
        x=hours, y=humidity, mode="lines",
        name="Kelembaban (%)", line=dict(color="#2196F3", width=1.5, dash="dot"),
        yaxis="y2",
    ))
    
    # Threshold line
    fig_temp.add_hline(y=28, line_dash="dash", line_color="#F44336",
                       annotation_text="Batas suhu aman (28°C)", annotation_position="top left")
    
    fig_temp.update_layout(
        height=300,
        yaxis=dict(title="Suhu (°C)", gridcolor="#eee"),
        yaxis2=dict(title="Kelembaban (%)", overlaying="y", side="right"),
        xaxis=dict(title="Waktu"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.3),
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=20, b=0),
    )
    st.plotly_chart(fig_temp, use_container_width=True)
    
    # MQTT data simulation
    st.markdown("##### 📡 Raw Telemetry (MQTT Protocol)")
    telemetry = pd.DataFrame({
        "Timestamp": [f"2026-05-14 {h:02d}:{np.random.randint(0,59):02d}:{np.random.randint(0,59):02d}" for h in range(10, 15)],
        "Topic": [f"nusapangan/fleet/{truck['id']}/sensors"] * 5,
        "Suhu (°C)": [round(t, 1) for t in temps[10:15]],
        "Kelembaban (%)": [round(h, 1) for h in humidity[10:15]],
        "GPS Lat": [round(-6.32 + np.random.uniform(-0.5, 0.5), 4) for _ in range(5)],
        "GPS Lon": [round(107.3 + np.random.uniform(0, 3), 4) for _ in range(5)],
        "Speed (km/h)": [np.random.randint(40, 75) for _ in range(5)],
    })
    st.dataframe(telemetry, use_container_width=True, hide_index=True)

with tab_route:
    st.markdown("### 🗺️ AI Route Optimization — Algoritma Genetika")
    st.markdown("*Mensimulasikan ribuan probabilitas rute untuk menekan BBM & waktu tempuh berdasarkan data IoT real-time.*")
    
    st.markdown("---")
    
    col_route, col_result = st.columns([1, 1])
    
    with col_route:
        st.markdown("##### 📍 Parameter Rute")
        r_origin = st.selectbox("Asal", ["Gudang Bulog Karawang", "Gudang Bulog Cirebon", "Gudang Agregator Bekasi"])
        r_dest = st.selectbox("Tujuan", ["SPPG Surabaya Utara", "SPPG Bandung Tengah", "SPPG Jakarta Selatan", "SPPG Semarang Barat"])
        r_cargo = st.number_input("Kargo (kg)", 100, 5000, 500, 100)
        r_priority = st.selectbox("Prioritas", ["⚡ Waktu tercepat", "💰 Biaya terendah", "🌡️ Cold-chain optimal"])
    
    with col_result:
        st.markdown("##### 🤖 Hasil Optimasi AI")
        
        # Simulated GA results
        routes_result = [
            {"rute": "Karawang → Tol Cikampek → Tol Trans Jawa → Surabaya", "jarak": "780 km", "waktu": "10.5 jam", "bbm": "Rp 1.248.000", "suhu_risk": "Rendah", "score": 94},
            {"rute": "Karawang → Pantura → Semarang → Surabaya", "jarak": "850 km", "waktu": "14 jam", "bbm": "Rp 1.105.000", "suhu_risk": "Sedang", "score": 78},
            {"rute": "Karawang → Tol Cipali → Tol Semarang → Surabaya", "jarak": "810 km", "waktu": "11.5 jam", "bbm": "Rp 1.296.000", "suhu_risk": "Rendah", "score": 87},
        ]
        
        for i, r in enumerate(routes_result):
            badge = "🏆 REKOMENDASI" if i == 0 else ""
            border = "#00897B" if i == 0 else "#eee"
            st.markdown(f"""
            <div style="border:2px solid {border};border-radius:10px;padding:0.8rem;margin-bottom:0.5rem;background:{'#E0F2F1' if i==0 else 'white'};">
                <div style="display:flex;justify-content:space-between;">
                    <strong style="font-size:0.85rem;">Rute {i+1} {badge}</strong>
                    <span style="background:#E0F2F1;color:#004D40;padding:0.1rem 0.4rem;border-radius:8px;font-size:0.75rem;font-weight:700;">Score: {r['score']}</span>
                </div>
                <p style="font-size:0.75rem;color:#555;margin:0.3rem 0;">📍 {r['rute']}</p>
                <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0.3rem;font-size:0.75rem;color:#666;">
                    <span>🛣️ {r['jarak']}</span>
                    <span>⏱️ {r['waktu']}</span>
                    <span>⛽ {r['bbm']}</span>
                    <span>🌡️ Risk: {r['suhu_risk']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # GA convergence chart
    st.markdown("##### 📈 Konvergensi Algoritma Genetika")
    
    np.random.seed(42)
    generations = list(range(1, 51))
    best_fitness = [1200]
    for g in range(49):
        delta = np.random.uniform(0, 30) * (1 - g/50)
        best_fitness.append(best_fitness[-1] - delta)
    avg_fitness = [b + np.random.uniform(50, 150) for b in best_fitness]
    
    fig_ga = go.Figure()
    fig_ga.add_trace(go.Scatter(x=generations, y=best_fitness, name="Best Fitness", 
                                line=dict(color="#00897B", width=2)))
    fig_ga.add_trace(go.Scatter(x=generations, y=avg_fitness, name="Avg Population",
                                line=dict(color="#B2DFDB", width=1.5, dash="dot")))
    fig_ga.update_layout(
        height=280,
        xaxis_title="Generasi", yaxis_title="Cost Function (BBM + Waktu + Risk)",
        plot_bgcolor="rgba(0,0,0,0)", yaxis=dict(gridcolor="#eee"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.3),
        margin=dict(l=0, r=0, t=10, b=0),
    )
    st.plotly_chart(fig_ga, use_container_width=True)
    
    st.markdown("""
    > **Algoritma Genetika (VRP):** Populasi 200 rute × 50 generasi. 
    > Fitness function: *minimize(BBM + waktu + risiko_suhu)*. 
    > Crossover: Ordered Crossover (OX). Mutation rate: 5%. 
    > Konvergen dalam ~30 generasi ke solusi optimal.
    """)
    
    # Impact
    st.markdown("---")
    st.markdown("##### 📊 Dampak SmartDistrib")
    d1, d2, d3, d4 = st.columns(4)
    d1.metric("📉 Food Loss", "Berkurang", "estimasi signifikan")
    d2.metric("⛽ Efisiensi BBM", "+18%", "vs rute manual")
    d3.metric("🌡️ Insiden Suhu", "1 dari 10", "tertangani otomatis")
    d4.metric("💰 Saving Logistik", "Rp 127 jt/bln", "estimasi")
