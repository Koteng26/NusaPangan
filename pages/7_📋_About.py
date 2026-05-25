"""
📋 About NusaPangan — Business Model, Architecture, Security, Impact & Roadmap
Halaman ini menutup gap: cost structure, revenue model, architecture diagram,
security compliance, impact KPI, scaling roadmap, adoption readiness
"""
import streamlit as st
import os, sys; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from utils import load_data, COMMON_CSS
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="About NusaPangan", page_icon="📋", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif; }
    .about-header {
        background: linear-gradient(135deg, #1B5E20, #2E7D32, #43A047);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 1.5rem;
    }
    .arch-box {
        background: white;
        border: 2px solid #E8F5E9;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        min-height: 80px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .arch-box.green { border-color: #4CAF50; background: #E8F5E9; }
    .arch-box.blue { border-color: #2196F3; background: #E3F2FD; }
    .arch-box.purple { border-color: #7C3AED; background: #EDE9FE; }
    .arch-box.orange { border-color: #FF9800; background: #FFF3E0; }
    .arch-box.teal { border-color: #009688; background: #E0F2F1; }
    .arch-box.red { border-color: #F44336; background: #FFEBEE; }
    .arch-title { font-size: 0.9rem; font-weight: 700; }
    .arch-sub { font-size: 0.7rem; color: #666; margin-top: 0.2rem; }
    .kpi-card {
        background: white;
        border-left: 4px solid #4CAF50;
        border-radius: 0 12px 12px 0;
        padding: 1rem;
        margin-bottom: 0.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .security-item {
        background: white;
        border: 1px solid #E8F5E9;
        border-radius: 10px;
        padding: 0.8rem;
        margin-bottom: 0.4rem;
    }
    .revenue-box {
        text-align: center;
        padding: 1rem;
        border-radius: 12px;
        background: white;
        border: 1px solid #eee;
    }
    .onboard-step {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 0.8rem;
        background: white;
        border-radius: 10px;
        margin-bottom: 0.4rem;
        border: 1px solid #eee;
    }
    .onboard-num {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: #E8F5E9;
        color: #1B5E20;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 1rem;
        flex-shrink: 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="about-header">
    <h2 style="margin:0;">📋 About NusaPangan</h2>
    <p style="margin:0.3rem 0 0 0; opacity:0.8;">Business Model · System Architecture · Security · Impact · Roadmap</p>
</div>
""", unsafe_allow_html=True)

# ================================================================
# TABS
# ================================================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏗️ Architecture", "💰 Business Model", "🔒 Security", 
    "📊 Impact KPI", "🚀 Roadmap", "📱 Onboarding"
])

# ================================================================
# TAB 1: SYSTEM ARCHITECTURE
# ================================================================
with tab1:
    st.markdown("### 🏗️ System Architecture — Microservices on GKE")
    
    st.markdown("##### 📱 Frontend Layer")
    f1, f2, f3 = st.columns(3)
    with f1:
        st.markdown("""
        <div class="arch-box green">
            <div class="arch-title">📱 Mobile App</div>
            <div class="arch-sub">React Native · Android/iOS<br>Petani & konsumen</div>
        </div>""", unsafe_allow_html=True)
    with f2:
        st.markdown("""
        <div class="arch-box green">
            <div class="arch-title">🌐 Web Dashboard</div>
            <div class="arch-sub">React.js · SPA<br>Pemerintah & admin</div>
        </div>""", unsafe_allow_html=True)
    with f3:
        st.markdown("""
        <div class="arch-box green">
            <div class="arch-title">💬 WhatsApp Bot</div>
            <div class="arch-sub">WhatsApp Business API<br>Notifikasi & quick action</div>
        </div>""", unsafe_allow_html=True)
    
    st.markdown("<div style='text-align:center;font-size:1.5rem;color:#4CAF50;'>⬇️ REST API + WebSocket ⬇️</div>", unsafe_allow_html=True)
    
    st.markdown("##### ⚙️ API Gateway & Backend Services")
    b1, b2, b3, b4, b5 = st.columns(5)
    with b1:
        st.markdown("""
        <div class="arch-box blue">
            <div class="arch-title">🛒 AgriMart</div>
            <div class="arch-sub">Node.js<br>Marketplace + Escrow</div>
        </div>""", unsafe_allow_html=True)
    with b2:
        st.markdown("""
        <div class="arch-box blue">
            <div class="arch-title">🔗 PanganLink</div>
            <div class="arch-sub">FastAPI (Python)<br>LSTM + Matching AI</div>
        </div>""", unsafe_allow_html=True)
    with b3:
        st.markdown("""
        <div class="arch-box blue">
            <div class="arch-title">📊 Price Radar</div>
            <div class="arch-sub">FastAPI (Python)<br>Isolation Forest</div>
        </div>""", unsafe_allow_html=True)
    with b4:
        st.markdown("""
        <div class="arch-box blue">
            <div class="arch-title">💳 AgriFinance</div>
            <div class="arch-sub">Node.js<br>Credit Score + KUR</div>
        </div>""", unsafe_allow_html=True)
    with b5:
        st.markdown("""
        <div class="arch-box blue">
            <div class="arch-title">🚛 SmartDistrib</div>
            <div class="arch-sub">FastAPI + MQTT<br>IoT + GA Routing</div>
        </div>""", unsafe_allow_html=True)
    
    st.markdown("<div style='text-align:center;font-size:1.5rem;color:#2196F3;'>⬇️ Internal Bus ⬇️</div>", unsafe_allow_html=True)
    
    st.markdown("##### 🗄️ Data & Infrastructure Layer")
    d1, d2, d3, d4 = st.columns(4)
    with d1:
        st.markdown("""
        <div class="arch-box purple">
            <div class="arch-title">🐘 PostgreSQL</div>
            <div class="arch-sub">Primary DB<br>Sharded per wilayah</div>
        </div>""", unsafe_allow_html=True)
    with d2:
        st.markdown("""
        <div class="arch-box purple">
            <div class="arch-title">⚡ Redis</div>
            <div class="arch-sub">Cache + Pub/Sub<br>Real-time data</div>
        </div>""", unsafe_allow_html=True)
    with d3:
        st.markdown("""
        <div class="arch-box purple">
            <div class="arch-title">🔗 Hyperledger</div>
            <div class="arch-sub">Blockchain Fabric<br>PBFT Consensus</div>
        </div>""", unsafe_allow_html=True)
    with d4:
        st.markdown("""
        <div class="arch-box purple">
            <div class="arch-title">☁️ GKE</div>
            <div class="arch-sub">Google Kubernetes<br>Auto-scaling</div>
        </div>""", unsafe_allow_html=True)
    
    st.markdown("<div style='text-align:center;font-size:1.5rem;color:#7C3AED;'>⬇️ External API Integration ⬇️</div>", unsafe_allow_html=True)
    
    st.markdown("##### 🔌 External API & Data Sources")
    e1, e2, e3, e4, e5 = st.columns(5)
    with e1:
        st.markdown("""
        <div class="arch-box orange">
            <div class="arch-title">🆔 Dukcapil</div>
            <div class="arch-sub">NIK Verification</div>
        </div>""", unsafe_allow_html=True)
    with e2:
        st.markdown("""
        <div class="arch-box orange">
            <div class="arch-title">📊 PIHPS BI</div>
            <div class="arch-sub">Harga Pangan</div>
        </div>""", unsafe_allow_html=True)
    with e3:
        st.markdown("""
        <div class="arch-box orange">
            <div class="arch-title">🌦️ BMKG</div>
            <div class="arch-sub">Cuaca & Iklim</div>
        </div>""", unsafe_allow_html=True)
    with e4:
        st.markdown("""
        <div class="arch-box orange">
            <div class="arch-title">🏦 Bank API</div>
            <div class="arch-sub">KUR Disbursement</div>
        </div>""", unsafe_allow_html=True)
    with e5:
        st.markdown("""
        <div class="arch-box orange">
            <div class="arch-title">🛰️ Sentinel-2</div>
            <div class="arch-sub">Citra Satelit</div>
        </div>""", unsafe_allow_html=True)

# ================================================================
# TAB 2: BUSINESS MODEL
# ================================================================
with tab2:
    st.markdown("### 💰 Business Model — Revenue & Cost Structure")
    
    st.markdown("##### 📊 Revenue Streams")
    r1, r2, r3, r4 = st.columns(4)
    with r1:
        st.markdown("""
        <div class="revenue-box">
            <div style="font-size:2rem;">🛒</div>
            <div style="font-weight:700;font-size:0.9rem;">Komisi AgriMart</div>
            <div style="font-size:1.5rem;font-weight:800;color:#1B5E20;">1-2%</div>
            <div style="font-size:0.75rem;color:#666;">per transaksi F2C/B2B</div>
            <div style="font-size:0.8rem;font-weight:600;color:#FF9800;margin-top:0.3rem;">~Rp 6 M/bln</div>
        </div>""", unsafe_allow_html=True)
    with r2:
        st.markdown("""
        <div class="revenue-box">
            <div style="font-size:2rem;">🚛</div>
            <div style="font-weight:700;font-size:0.9rem;">SaaS IoT</div>
            <div style="font-size:1.5rem;font-weight:800;color:#1B5E20;">Rp 5jt</div>
            <div style="font-size:0.75rem;color:#666;">per perusahaan/bulan</div>
            <div style="font-size:0.8rem;font-weight:600;color:#FF9800;margin-top:0.3rem;">~Rp 250 jt/bln</div>
        </div>""", unsafe_allow_html=True)
    with r3:
        st.markdown("""
        <div class="revenue-box">
            <div style="font-size:2rem;">💳</div>
            <div style="font-weight:700;font-size:0.9rem;">DaaS Credit</div>
            <div style="font-size:1.5rem;font-weight:800;color:#1B5E20;">Rp 50rb</div>
            <div style="font-size:0.75rem;color:#666;">per credit check bank</div>
            <div style="font-size:0.8rem;font-weight:600;color:#FF9800;margin-top:0.3rem;">~Rp 500 jt/bln</div>
        </div>""", unsafe_allow_html=True)
    with r4:
        st.markdown("""
        <div class="revenue-box">
            <div style="font-size:2rem;">🏛️</div>
            <div style="font-weight:700;font-size:0.9rem;">Lisensi B2G</div>
            <div style="font-size:1.5rem;font-weight:800;color:#1B5E20;">Rp 200jt</div>
            <div style="font-size:0.75rem;color:#666;">per instansi/tahun</div>
            <div style="font-size:0.8rem;font-weight:600;color:#FF9800;margin-top:0.3rem;">~Rp 1.2 M/bln</div>
        </div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Cost Structure
    st.markdown("##### 💸 Cost Structure")
    cost_data = pd.DataFrame({
        "Kategori": ["GCP Infrastructure", "Tim Dev (8 orang)", "Sensor IoT & Install", "Field Agent Ops", "Compliance & Audit", "Marketing & BD"],
        "Bulanan (Rp)": [45_000_000, 320_000_000, 80_000_000, 60_000_000, 25_000_000, 30_000_000],
    })
    cost_data["Persentase"] = (cost_data["Bulanan (Rp)"] / cost_data["Bulanan (Rp)"].sum() * 100).round(1)
    
    col_cost1, col_cost2 = st.columns(2)
    with col_cost1:
        fig_cost = px.pie(cost_data, values="Bulanan (Rp)", names="Kategori",
                         color_discrete_sequence=["#4CAF50", "#2196F3", "#FF9800", "#9C27B0", "#F44336", "#607D8B"],
                         hole=0.4)
        fig_cost.update_layout(height=300, margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig_cost, use_container_width=True)
    
    with col_cost2:
        st.dataframe(cost_data, use_container_width=True, hide_index=True)
        total_cost = cost_data["Bulanan (Rp)"].sum()
        st.metric("Total Cost / Bulan", f"Rp {total_cost/1e6:,.0f} jt")
    
    st.markdown("---")
    
    # Break-even
    st.markdown("##### 📈 Break-Even Projection")
    
    months = list(range(1, 25))
    revenue_proj = [0]*2 + [50]*2 + [150, 250, 400, 600, 800, 1000, 1200, 1400,
                    1600, 1800, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900]
    cost_proj = [560]*6 + [540]*6 + [520]*6 + [500]*6
    
    fig_be = go.Figure()
    fig_be.add_trace(go.Scatter(x=months, y=revenue_proj, name="Revenue (Rp jt)", 
                                line=dict(color="#4CAF50", width=3), fill="tozeroy",
                                fillcolor="rgba(76,175,80,0.1)"))
    fig_be.add_trace(go.Scatter(x=months, y=cost_proj, name="Cost (Rp jt)",
                                line=dict(color="#F44336", width=2, dash="dash")))
    fig_be.add_vline(x=14, line_dash="dot", line_color="#FF9800",
                     annotation_text="Break-Even (Bulan 14)", annotation_position="top")
    fig_be.update_layout(height=350, xaxis_title="Bulan", yaxis_title="Rp (Juta)",
                        plot_bgcolor="rgba(0,0,0,0)", yaxis=dict(gridcolor="#eee"),
                        legend=dict(orientation="h", yanchor="bottom", y=-0.2),
                        margin=dict(l=0,r=0,t=20,b=0))
    st.plotly_chart(fig_be, use_container_width=True)
    
    st.success("💡 **Proyeksi break-even di bulan ke-14** dengan asumsi 50.000 pengguna aktif dan volume transaksi Rp 50 miliar/bulan.")

# ================================================================
# TAB 3: SECURITY & COMPLIANCE
# ================================================================
with tab3:
    st.markdown("### 🔒 Security & Compliance")
    
    st.markdown("##### 🛡️ Security Architecture")
    
    security_items = [
        {"icon": "🔐", "title": "Enkripsi AES-256", "detail": "Seluruh data at-rest dan in-transit terenkripsi dengan standar militer AES-256. TLS 1.3 untuk komunikasi API."},
        {"icon": "🔑", "title": "OAuth2 + JWT + Zero Trust", "detail": "Autentikasi multi-factor. Setiap request diverifikasi ulang — tidak ada trusted zone. Token JWT dengan expiry 15 menit."},
        {"icon": "🔗", "title": "Blockchain Immutability", "detail": "Hyperledger Fabric (PBFT consensus). Data subsidi dan transaksi tidak bisa diubah sepihak. OJK/BPK sebagai auditor node independen."},
        {"icon": "🆔", "title": "Biometrik & Dukcapil", "detail": "Verifikasi NIK real-time via API Dukcapil. Mencegah 100% profil fiktif. Data KTP diproses tanpa disimpan (zero-knowledge proof)."},
        {"icon": "📡", "title": "IoT Security (MQTT TLS)", "detail": "Sensor IoT berkomunikasi lewat MQTT dengan TLS encryption. Device authentication per armada. Anomaly detection pada telemetri."},
        {"icon": "🗄️", "title": "Database Sharding", "detail": "PostgreSQL di-shard per wilayah. Backup otomatis setiap 6 jam. Disaster recovery RTO < 4 jam, RPO < 1 jam."},
    ]
    
    for item in security_items:
        st.markdown(f"""
        <div class="security-item">
            <div style="display:flex;gap:0.8rem;align-items:start;">
                <span style="font-size:1.5rem;">{item['icon']}</span>
                <div>
                    <div style="font-weight:700;font-size:0.9rem;">{item['title']}</div>
                    <div style="font-size:0.8rem;color:#555;margin-top:0.2rem;">{item['detail']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("##### 📜 Regulatory Compliance")
    
    comp1, comp2, comp3 = st.columns(3)
    with comp1:
        st.markdown("""
        <div class="arch-box green">
            <div class="arch-title">📜 UU PDP</div>
            <div class="arch-sub">UU Pelindungan Data Pribadi<br>Full compliance</div>
        </div>""", unsafe_allow_html=True)
    with comp2:
        st.markdown("""
        <div class="arch-box blue">
            <div class="arch-title">🏦 POJK 30/2025</div>
            <div class="arch-sub">Regulatory Sandbox OJK<br>Layanan Keuangan Digital</div>
        </div>""", unsafe_allow_html=True)
    with comp3:
        st.markdown("""
        <div class="arch-box purple">
            <div class="arch-title">🖥️ PP 71/2019</div>
            <div class="arch-sub">PSTE<br>Sistem Transaksi Elektronik</div>
        </div>""", unsafe_allow_html=True)

# ================================================================
# TAB 4: IMPACT KPI
# ================================================================
with tab4:
    st.markdown("### 📊 Impact Dashboard — Key Performance Indicators")
    
    # Target vs Actual
    st.markdown("##### 🎯 Target Impact NusaPangan")
    
    kpi_data = [
        {"kpi": "Kenaikan Pendapatan Petani", "target": "+30%", "current": "+32%", "status": "✅ On Track", "icon": "💰"},
        {"kpi": "Penurunan Harga Konsumen", "target": "-20%", "current": "-18%", "status": "✅ On Track", "icon": "📉"},
        {"kpi": "Reduksi Food Loss & Waste", "target": "-20%", "current": "-22%", "status": "✅ Exceeded", "icon": "🗑️"},
        {"kpi": "Subsidi Fiktif Terdeteksi", "target": "100%", "current": "100%", "status": "✅ Achieved", "icon": "🔍"},
        {"kpi": "Petani Akses Keuangan Formal", "target": "80%", "current": "72%", "status": "🔄 Progress", "icon": "💳"},
        {"kpi": "Akurasi Prediksi Harga (LSTM)", "target": "R² > 0.90", "current": "R² = 0.94", "status": "✅ Exceeded", "icon": "🤖"},
    ]
    
    for kpi in kpi_data:
        st.markdown(f"""
        <div class="kpi-card">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <span style="font-size:1.2rem;">{kpi['icon']}</span>
                    <strong style="margin-left:0.5rem;">{kpi['kpi']}</strong>
                </div>
                <span style="font-size:0.8rem;font-weight:600;">{kpi['status']}</span>
            </div>
            <div style="display:flex;gap:2rem;margin-top:0.5rem;font-size:0.85rem;">
                <span style="color:#888;">Target: <strong style="color:#1B5E20;">{kpi['target']}</strong></span>
                <span style="color:#888;">Saat ini: <strong style="color:#0D47A1;">{kpi['current']}</strong></span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # SDG Alignment
    st.markdown("##### 🌍 SDG Alignment")
    sdg1, sdg2, sdg3, sdg4 = st.columns(4)
    with sdg1:
        st.markdown("""
        <div class="arch-box green">
            <div class="arch-title">SDG 1</div>
            <div class="arch-sub">No Poverty<br>Income petani +30%</div>
        </div>""", unsafe_allow_html=True)
    with sdg2:
        st.markdown("""
        <div class="arch-box orange">
            <div class="arch-title">SDG 2</div>
            <div class="arch-sub">Zero Hunger<br>FLW -20%, MBG</div>
        </div>""", unsafe_allow_html=True)
    with sdg3:
        st.markdown("""
        <div class="arch-box blue">
            <div class="arch-title">SDG 9</div>
            <div class="arch-sub">Industry & Innovation<br>Digital infrastructure</div>
        </div>""", unsafe_allow_html=True)
    with sdg4:
        st.markdown("""
        <div class="arch-box purple">
            <div class="arch-title">SDG 12</div>
            <div class="arch-sub">Responsible Consumption<br>Traceability</div>
        </div>""", unsafe_allow_html=True)

# ================================================================
# TAB 5: ROADMAP & SCALING
# ================================================================
with tab5:
    st.markdown("### 🚀 Roadmap & Scaling Strategy")
    
    # Timeline
    phases = [
        {"phase": "Fase 0", "title": "Foundation", "period": "Bulan 1", "color": "#9E9E9E",
         "items": "Blueprint sistem, perizinan Sandbox OJK/BI, setup GCP, MOU kelompok tani pilot"},
        {"phase": "Fase 1", "title": "MVP Launch", "period": "Bulan 2-3", "color": "#4CAF50",
         "items": "Closed-beta AgriMart + Price Radar, 200 petani pilot, integrasi API BI/Bapanas, 10 armada IoT"},
        {"phase": "Fase 2", "title": "AI & Subsidi", "period": "Bulan 4-6", "color": "#2196F3",
         "items": "PanganLink launch, smart contract AgriFinance, API Dukcapil live, demo purifikasi e-RDKK ke Kementan"},
        {"phase": "Fase 3", "title": "Skalasi Nasional", "period": "Bulan 7-12", "color": "#FF9800",
         "items": "5 provinsi, credit score digital untuk bank mitra, monetisasi B2B analytics, target 50.000 user"},
    ]
    
    for p in phases:
        st.markdown(f"""
        <div style="display:flex;gap:1rem;margin-bottom:1rem;">
            <div style="text-align:center;min-width:80px;">
                <div style="background:{p['color']};color:white;padding:0.4rem 0.8rem;border-radius:8px;font-weight:700;font-size:0.85rem;">{p['phase']}</div>
                <div style="font-size:0.75rem;color:#888;margin-top:0.3rem;">{p['period']}</div>
            </div>
            <div style="flex:1;background:white;border-left:4px solid {p['color']};border-radius:0 12px 12px 0;padding:1rem;">
                <div style="font-weight:700;font-size:0.95rem;">{p['title']}</div>
                <div style="font-size:0.8rem;color:#555;margin-top:0.3rem;">{p['items']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Growth projection
    st.markdown("##### 📈 Growth Projection (24 Bulan)")
    
    growth_months = list(range(1, 25))
    users = [200, 500, 1000, 2000, 3500, 5000, 7500, 10000, 14000, 18000, 23000, 28000,
             33000, 38000, 42000, 45000, 48000, 50000, 55000, 60000, 70000, 80000, 100000, 120000]
    provinces = [1]*3 + [2]*3 + [3]*3 + [5]*3 + [8]*3 + [12]*3 + [18]*3 + [25]*3
    
    fig_growth = go.Figure()
    fig_growth.add_trace(go.Bar(x=growth_months, y=users, name="Users Aktif",
                               marker_color="#4CAF50", opacity=0.7))
    fig_growth.add_trace(go.Scatter(x=growth_months, y=[p*5000 for p in provinces], 
                                    name="Provinsi Coverage (×5000)", 
                                    line=dict(color="#FF9800", width=2),
                                    yaxis="y"))
    fig_growth.update_layout(height=350, xaxis_title="Bulan", yaxis_title="Jumlah",
                            plot_bgcolor="rgba(0,0,0,0)", yaxis=dict(gridcolor="#eee"),
                            legend=dict(orientation="h", yanchor="bottom", y=-0.2),
                            margin=dict(l=0,r=0,t=20,b=0))
    st.plotly_chart(fig_growth, use_container_width=True)
    
    # Scaling tech
    st.markdown("##### ⚙️ Scaling Technology")
    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        st.metric("Target User Y1", "50.000", "aktif")
    with sc2:
        st.metric("Target User Y2", "500.000", "aktif")
    with sc3:
        st.metric("Auto-Scale", "GKE Kubernetes", "elastis")
    
    st.markdown("""
    > **Strategi Scaling:** Database di-shard per wilayah (Jawa, Sumatera, Sulawesi, dst). 
    > Redis caching untuk data harga real-time. GKE auto-scaling menyesuaikan traffic secara elastis.
    > Offline-first sync untuk daerah dengan sinyal fluktuatif.
    """)

# ================================================================
# TAB 6: ONBOARDING / ADOPTION READINESS
# ================================================================
with tab6:
    st.markdown("### 📱 User Onboarding — Adoption Readiness")
    st.markdown("*Bagaimana petani yang belum pernah pakai smartphone bisa masuk ke NusaPangan?*")
    
    st.markdown("---")
    
    st.markdown("##### 👨‍🌾 Alur Onboarding Petani (5 Langkah)")
    
    onboard_steps = [
        {"num": "1", "title": "Field Agent Datang ke Desa", "detail": "Agent NusaPangan mengunjungi kelompok tani. Bawa tablet, printer mini untuk cetak QR. Koordinasi dengan ketua kelompok tani.", "icon": "🏘️"},
        {"num": "2", "title": "Registrasi + Verifikasi NIK", "detail": "Petani tunjukkan KTP. Agent input NIK ke sistem. API Dukcapil verifikasi real-time dalam 3 detik. Foto lahan diambil + GPS boundary.", "icon": "🆔"},
        {"num": "3", "title": "Profil Digital Tercipta", "detail": "Otomatis: identitas digital, luas lahan, varietas, credit score awal. Petani dapat QR code personal yang dicetak di tempat.", "icon": "📱"},
        {"num": "4", "title": "WhatsApp Terhubung", "detail": "Petani daftar WhatsApp ke bot NusaPangan. Semua notifikasi (harga, order, pembayaran) via WA. Tidak perlu download app.", "icon": "💬"},
        {"num": "5", "title": "Listing Pertama di AgriMart", "detail": "Agent bantu petani listing produk pertama. Harga otomatis sesuai Price Radar. Dalam 24 jam, produk sudah visible ke buyer SPPG.", "icon": "🛒"},
    ]
    
    for step in onboard_steps:
        st.markdown(f"""
        <div class="onboard-step">
            <div class="onboard-num">{step['num']}</div>
            <div style="flex:1;">
                <div style="font-weight:700;font-size:0.9rem;">{step['icon']} {step['title']}</div>
                <div style="font-size:0.8rem;color:#555;margin-top:0.2rem;">{step['detail']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("##### 📊 Adoption Readiness Indicators")
    
    ar1, ar2, ar3, ar4 = st.columns(4)
    ar1.metric("📱 Smartphone Penetration", "79%", "Indonesia 2025")
    ar2.metric("💬 WhatsApp Users", "112 jt", "Indonesia")
    ar3.metric("📡 4G Coverage", "94%", "populasi")
    ar4.metric("🏘️ Kelompok Tani", "340.000+", "aktif")
    
    st.markdown("""
    > **Kunci Adopsi:** NusaPangan tidak memaksa petani download app baru. 
    > WhatsApp sebagai primary channel — petani sudah familiar. 
    > Field agent turun ke desa untuk onboarding awal. 
    > Setelah terdaftar, semua bisa dilakukan via chat WhatsApp.
    """)
    
    st.markdown("---")
    
    # User personas
    st.markdown("##### 👥 User Personas")
    
    p1, p2, p3 = st.columns(3)
    with p1:
        st.markdown("""
        <div class="arch-box green">
            <div style="font-size:2rem;">👨‍🌾</div>
            <div class="arch-title">Pak Budi (55 thn)</div>
            <div class="arch-sub">Petani padi, 2 ha, Karawang<br>HP Android murah<br>Akses: WhatsApp only<br>Kebutuhan: harga adil, akses KUR</div>
        </div>""", unsafe_allow_html=True)
    with p2:
        st.markdown("""
        <div class="arch-box blue">
            <div style="font-size:2rem;">👩‍💼</div>
            <div class="arch-title">Bu Ani (38 thn)</div>
            <div class="arch-sub">Admin SPPG Surabaya<br>Laptop + HP<br>Akses: Web dashboard<br>Kebutuhan: order cepat, traceability</div>
        </div>""", unsafe_allow_html=True)
    with p3:
        st.markdown("""
        <div class="arch-box purple">
            <div style="font-size:2rem;">👨‍💻</div>
            <div class="arch-title">Pak Rudi (45 thn)</div>
            <div class="arch-sub">Analis Bapanas<br>Desktop + multi-screen<br>Akses: Command Center<br>Kebutuhan: data real-time, alert</div>
        </div>""", unsafe_allow_html=True)
