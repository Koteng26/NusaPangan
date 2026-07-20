"""
🚛 SmartDistrib — Mesin AI Logistik NusaPangan (flagship)
Route Optimization · Demand Forecasting · ETA Prediction · Cost Optimization · Delivery Monitoring
"""
import streamlit as st
import os, sys; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from utils import load_data
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="SmartDistrib", page_icon="🚛", layout="wide")

# ============ TEMA OPS GELAP (konsisten dgn Dashboard SPPG) ============
st.markdown("""
<style>
.stApp{background:radial-gradient(130% 110% at 75% -5%, #12261E 0%, #0B1713 48%, #070F0C 100%);}
.stApp, .stApp p, .stApp label, .stApp span{color:#D7E5DD;}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0D1B16,#0A1410);border-right:1px solid rgba(255,255,255,.07);}
[data-testid="stSidebar"] *{color:#C6DBD0 !important;}
[data-testid="stSidebarNav"] a{border-radius:8px;}
[data-testid="stSidebarNav"] a:hover{background:rgba(74,222,128,.10);}
[data-testid="stSidebarNav"] a[aria-current="page"]{background:rgba(74,222,128,.16);}
[data-testid="stSidebar"] img{filter:brightness(1.15);}

h1,h2,h3,h4{color:#F2F7F4 !important;}
.ops-live{display:inline-flex;align-items:center;gap:7px;font-family:ui-monospace,monospace;font-size:11px;
letter-spacing:.14em;color:#4ADE80;background:rgba(74,222,128,.08);border:1px solid rgba(74,222,128,.25);
padding:5px 12px;border-radius:999px;}
.ops-live i{width:7px;height:7px;border-radius:50%;background:#4ADE80;animation:blink 1.6s infinite;}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.2}}
.kpi{background:linear-gradient(160deg,rgba(255,255,255,.05),rgba(255,255,255,.015));
border:1px solid rgba(255,255,255,.08);border-radius:14px;padding:13px 15px;height:100%;}
.kpi .l{font-size:.66rem;letter-spacing:.08em;text-transform:uppercase;color:#8FA89C;}
.kpi .v{font-size:1.45rem;font-weight:900;color:#fff;margin-top:3px;font-family:ui-monospace,monospace;}
.kpi .s{font-size:.66rem;color:#8FA89C;margin-top:2px;}
.rt{background:linear-gradient(160deg,rgba(255,255,255,.045),rgba(255,255,255,.012));
border:1px solid rgba(255,255,255,.08);border-radius:14px;padding:13px 15px;margin-bottom:10px;}
.rt.best{border:1px solid rgba(74,222,128,.5);box-shadow:0 0 24px rgba(74,222,128,.08);}
.rt .top{display:flex;justify-content:space-between;align-items:center;gap:8px;}
.rt b{color:#fff;} .rt small{color:#8FA89C;font-size:.72rem;}
.badge-best{font-size:.64rem;font-weight:800;letter-spacing:.06em;color:#0B1713;background:#4ADE80;
padding:4px 10px;border-radius:999px;}
.mono{font-family:ui-monospace,monospace;}
.pbar{height:7px;background:rgba(255,255,255,.07);border-radius:4px;margin-top:8px;overflow:hidden;}
.pbar i{display:block;height:100%;border-radius:4px;background:linear-gradient(90deg,#39A96B,#4ADE80);}
.panel{background:linear-gradient(165deg,rgba(255,255,255,.05),rgba(255,255,255,.015));
border:1px solid rgba(255,255,255,.08);border-radius:16px;padding:16px;}
.note-ops{font-size:.72rem;color:#7E958A;border-left:3px solid rgba(231,178,76,.5);padding:6px 12px;margin-top:14px;}
.chip{font-size:.66rem;font-weight:800;letter-spacing:.05em;padding:4px 10px;border-radius:999px;}
.c-transit{background:rgba(231,178,76,.14);color:#E7B24C;border:1px solid rgba(231,178,76,.35);}
.c-done{background:rgba(74,222,128,.12);color:#4ADE80;border:1px solid rgba(74,222,128,.3);}
.c-wh{background:rgba(96,165,250,.12);color:#60A5FA;border:1px solid rgba(96,165,250,.3);}
</style>
""", unsafe_allow_html=True)

df = load_data("journeys.csv")

st.markdown("""
<div style="display:flex;align-items:center;gap:14px;flex-wrap:wrap;">
  <h2 style="margin:0;">🚛 SmartDistrib</h2>
  <span class="ops-live"><i></i>AI ENGINE</span>
</div>
<p style="color:#8FA89C;font-size:.85rem;margin-top:2px;">
Mesin logistik NusaPangan untuk koridor Banten → DKI: optimasi rute, prediksi permintaan &amp; ETA,
efisiensi biaya, dan pemantauan pengiriman.</p>
""", unsafe_allow_html=True)

k = st.columns(5)
for col,(l,v,s) in zip(k,[
    ("Koridor aktif","Banten → DKI","5 wilayah SPPG"),
    ("Batch dipantau",f"{len(df)}","musim ini"),
    ("Di perjalanan",f"{(df.status=='In Transit').sum()}","real-time board"),
    ("On-time rate","96%","30 hari terakhir"),
    ("Rata-rata rendemen",f"{df.rendemen_pct.mean():.0f}%","gabah → beras"),
]):
    col.markdown(f'<div class="kpi"><div class="l">{l}</div><div class="v">{v}</div><div class="s">{s}</div></div>', unsafe_allow_html=True)

st.markdown("")
t1,t2,t3,t4,t5 = st.tabs(["🗺️ Route Optimization","📈 Demand Forecasting","⏱️ ETA Prediction","💰 Cost Optimization","📡 Delivery Monitoring"])

# koordinat & konstanta
ORIGINS = {"Gudang Bulog Serang":(-6.115,106.163), "Penggilingan Mitra Tangerang":(-6.178,106.630)}
SPPGC = {"SPPG Jakarta Pusat":(-6.186,106.834),"SPPG Jakarta Barat":(-6.148,106.735),
         "SPPG Jakarta Timur":(-6.225,106.900),"SPPG Jakarta Selatan":(-6.266,106.813),
         "SPPG Jakarta Utara":(-6.121,106.774)}

# ============ TAB 1 — ROUTE OPTIMIZATION ============
with t1:
    ca, cb, cc, cd = st.columns([1.2,1.2,.8,1])
    o = ca.selectbox("Asal", list(ORIGINS.keys()))
    dsel = cb.selectbox("Tujuan", list(SPPGC.keys()))
    kg = cc.number_input("Kargo (kg)", 100, 8000, 500, 100)
    pri = cd.selectbox("Prioritas", ["⚡ Waktu tercepat","📏 Jarak terpendek","🛡️ Risiko terendah"])

    o_ll, d_ll = ORIGINS[o], SPPGC[dsel]
    jarak_dasar = 111.0*np.hypot(d_ll[0]-o_ll[0], (d_ll[1]-o_ll[1])*np.cos(np.radians(-6.2)))
    routes = [
        {"nama":"Tol Tangerang–Merak → Dalam Kota","f_km":1.28,"f_jam":0.0165,"risk":18,
         "wp":[o_ll,(-6.204,106.341),(-6.202,106.455),(-6.176,106.632),(-6.190,106.762),d_ll]},
        {"nama":"Tol JORR via BSD","f_km":1.42,"f_jam":0.0182,"risk":12,
         "wp":[o_ll,(-6.240,106.420),(-6.302,106.652),(-6.276,106.760),d_ll]},
        {"nama":"Arteri Daan Mogot","f_km":1.18,"f_jam":0.0235,"risk":34,
         "wp":[o_ll,(-6.190,106.470),(-6.176,106.632),(-6.160,106.706),d_ll]},
    ]
    for r in routes:
        r["km"] = round(jarak_dasar*r["f_km"])
        r["jam"] = round(jarak_dasar*r["f_jam"]+0.55, 1)
    if "tercepat" in pri: routes.sort(key=lambda r:r["jam"])
    elif "terpendek" in pri: routes.sort(key=lambda r:r["km"])
    else: routes.sort(key=lambda r:r["risk"])
    best = routes[0]

    mc, rc = st.columns([1.55,1])
    with mc:
        fig = go.Figure()
        warna = ["#4ADE80","#E7B24C","#5B7A6C"]
        for i,r in enumerate(routes):
            lats=[p[0] for p in r["wp"]]; lons=[p[1] for p in r["wp"]]
            fig.add_trace(go.Scattermapbox(lat=lats, lon=lons, mode="lines",
                line=dict(width=5 if i==0 else 3, color=warna[i]),
                name=r["nama"], opacity=1 if i==0 else .55))
        fig.add_trace(go.Scattermapbox(lat=[o_ll[0]], lon=[o_ll[1]], mode="markers+text",
            marker=dict(size=13,color="#E7B24C"), text=["ASAL"], textposition="top center",
            textfont=dict(color="#E7B24C",size=10), showlegend=False))
        fig.add_trace(go.Scattermapbox(lat=[d_ll[0]], lon=[d_ll[1]], mode="markers+text",
            marker=dict(size=13,color="#4ADE80"), text=["TUJUAN"], textposition="top center",
            textfont=dict(color="#4ADE80",size=10), showlegend=False))
        fig.update_layout(mapbox=dict(style="carto-darkmatter",
                          center=dict(lat=(o_ll[0]+d_ll[0])/2, lon=(o_ll[1]+d_ll[1])/2), zoom=8.6),
                          height=470, margin=dict(t=0,b=0,l=0,r=0),
                          paper_bgcolor="rgba(0,0,0,0)",
                          legend=dict(font=dict(color="#BFD4C9"), bgcolor="rgba(10,20,16,.6)"))
        st.plotly_chart(fig, use_container_width=True)
    with rc:
        for i,r in enumerate(routes):
            risk_lbl = "Rendah" if r["risk"]<20 else ("Sedang" if r["risk"]<30 else "Tinggi")
            st.markdown(f"""
            <div class="rt {'best' if i==0 else ''}">
              <div class="top"><b>{r['nama']}</b>{'<span class="badge-best">REKOMENDASI AI</span>' if i==0 else ''}</div>
              <small class="mono">📦 {r['km']} km · 🕐 {r['jam']} jam · 🛡️ Risiko: {risk_lbl}</small>
              <div class="pbar"><i style="width:{100-r['risk']*2}%"></i></div>
            </div>""", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="panel" style="border-left:4px solid #4ADE80;">
          <b style="color:#4ADE80;">⚡ Rencana muat</b><br>
          <span style="font-size:.82rem;">{kg:,} kg via <b>{best['nama']}</b> — berangkat 06:30,
          estimasi tiba {best['jam']} jam kemudian. Skor gabungan jarak, waktu tempuh &amp; risiko keterlambatan.</span>
        </div>""", unsafe_allow_html=True)

# ============ TAB 2 — DEMAND FORECASTING ============
with t2:
    st.markdown("#### 📈 Prakiraan Kebutuhan Beras — 14 Hari ke Depan")
    dsel2 = st.selectbox("SPPG", list(SPPGC.keys()), key="df_sppg")
    butuh = {"SPPG Jakarta Pusat":450,"SPPG Jakarta Barat":390,"SPPG Jakarta Timur":360,
             "SPPG Jakarta Selatan":300,"SPPG Jakarta Utara":240}[dsel2]
    tgl = pd.date_range("2026-07-20", periods=14, freq="D")
    need = [(butuh*(1+0.04*np.sin(i/2)) if t.weekday()<5 else 0) for i,t in enumerate(tgl)]
    pasok = butuh*0.92
    dfx = pd.DataFrame({"tanggal":tgl,"kebutuhan":need})
    dfx["hari"] = dfx.tanggal.dt.strftime("%a %d/%m")
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=dfx.hari, y=dfx.kebutuhan, name="Kebutuhan (kg)",
        marker_color=["#39A96B" if n>0 else "rgba(255,255,255,.10)" for n in dfx.kebutuhan]))
    fig2.add_hline(y=pasok, line_dash="dash", line_color="#E7B24C",
        annotation_text=f"Pasokan terkontrak {pasok:.0f} kg/hari", annotation_font_color="#E7B24C")
    fig2.update_layout(height=380, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#BFD4C9"), yaxis=dict(gridcolor="#1E2E27", title="kg"),
        xaxis=dict(gridcolor="#1E2E27"), showlegend=False, margin=dict(t=20,b=10))
    st.plotly_chart(fig2, use_container_width=True)
    gap_hari = int((dfx.kebutuhan>pasok).sum())
    total14 = dfx.kebutuhan.sum()
    c1,c2,c3 = st.columns(3)
    c1.markdown(f'<div class="kpi"><div class="l">Total 14 hari</div><div class="v">{total14:,.0f} kg</div><div class="s">hanya hari sekolah (Sen–Jum)</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="kpi"><div class="l">Hari berpotensi defisit</div><div class="v" style="color:{"#E7B24C" if gap_hari else "#4ADE80"};">{gap_hari}</div><div class="s">kebutuhan &gt; kontrak harian</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="kpi"><div class="l">Rekomendasi</div><div class="v" style="font-size:1rem;">+{max(0,(total14-pasok*10)):,.0f} kg</div><div class="s">tambahan via AgriMart pekan ini</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="note-ops">Model prakiraan: pola hari sekolah MBG (Sen–Jum) + variasi musiman — simulasi berlabel; siap dilatih ulang dengan data konsumsi aktual.</div>', unsafe_allow_html=True)

# ============ TAB 3 — ETA PREDICTION ============
with t3:
    st.markdown("#### ⏱️ Prediksi Waktu Tiba — Batch Aktif")
    aktif = df[df.status=="In Transit"].copy()
    for _,r in aktif.iterrows():
        conf = int(np.clip(97 - r.jarak_km*0.18, 72, 96))
        jam = round(r.jarak_km*0.0172 + 0.55, 1)
        st.markdown(f"""
        <div class="rt">
          <div class="top"><b>{r.qr_code} · {r.jumlah_kg_sekolah:,} kg → {r.sppg.replace('SPPG ','')}</b>
          <span class="chip c-transit">DI JALAN</span></div>
          <small class="mono">{r.petani_kab} → {r.sekolah_kota} · {r.jarak_km} km · estimasi tempuh {jam} jam</small>
          <div class="pbar"><i style="width:62%"></i></div>
          <small style="display:block;margin-top:6px;">Prediksi tiba <b style="color:#fff;">{r.tanggal_tiba} ± 25 menit</b>
          · keyakinan model <b style="color:#4ADE80;">{conf}%</b> · faktor: jam sibuk tol dalam kota, cuaca cerah, bongkar-muat gudang</small>
        </div>""", unsafe_allow_html=True)
    if aktif.empty:
        st.info("Tidak ada batch di perjalanan saat ini.")
    st.markdown('<div class="note-ops">ETA dihitung dari jarak koridor, profil jam berangkat, dan riwayat tempuh — GPS armada real-time: roadmap integrasi mitra transporter.</div>', unsafe_allow_html=True)

# ============ TAB 4 — COST OPTIMIZATION ============
with t4:
    st.markdown("#### 💰 Optimasi Biaya Angkut — Skenario Konsolidasi")
    sk = pd.DataFrame([
        {"Skenario":"Kirim terpisah (Pick Up, 500 kg)","kg":500,"biaya":150000},
        {"Skenario":"Konsolidasi 2 SPPG (Truk, 1.700 kg)","kg":1700,"biaya":350000},
        {"Skenario":"Full truck 1 rit (4.000 kg)","kg":4000,"biaya":520000},
    ])
    sk["per_kg"] = (sk.biaya/sk.kg).round(0)
    fig4 = go.Figure(go.Bar(x=sk.Skenario, y=sk.per_kg,
        marker_color=["rgba(255,255,255,.22)","#E7B24C","#4ADE80"],
        text=sk.per_kg, texttemplate="Rp %{text:,.0f}/kg", textposition="outside"))
    fig4.update_layout(height=360, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#BFD4C9"), yaxis=dict(gridcolor="#1E2E27", title="Biaya per kg (Rp)"),
        xaxis=dict(gridcolor="#1E2E27"), margin=dict(t=20,b=10))
    st.plotly_chart(fig4, use_container_width=True)
    hemat = 1 - sk.per_kg.iloc[2]/sk.per_kg.iloc[0]
    st.markdown(f"""
    <div class="panel" style="border-left:4px solid #4ADE80;">
      <b style="color:#4ADE80;">Konsolidasi penuh menghemat {hemat:.0%} biaya angkut per kg</b><br>
      <span style="font-size:.82rem;">AI menggabungkan order beberapa SPPG dalam satu koridor &amp; jadwal.
      Biaya transportasi tetap dibayar pembeli sekali di checkout — panel ini alat perencanaan, bukan biaya tambahan.</span>
    </div>""", unsafe_allow_html=True)

# ============ TAB 5 — DELIVERY MONITORING ============
with t5:
    st.markdown("#### 📡 Papan Pemantauan Pengiriman")
    cA,cB,cC = st.columns(3)
    for col,(lbl,val,cls) in zip([cA,cB,cC],[
        ("Di perjalanan",(df.status=="In Transit").sum(),"c-transit"),
        ("Di gudang asal",(df.status=="At Warehouse").sum(),"c-wh"),
        ("Terkirim ✓",(df.status=="Delivered").sum(),"c-done")]):
        col.markdown(f'<div class="kpi"><div class="l">{lbl}</div><div class="v">{val}</div></div>', unsafe_allow_html=True)
    st.markdown("")
    prog = {"Delivered":100,"In Transit":62,"At Warehouse":28}
    chip = {"Delivered":("c-done","TIBA ✓"),"In Transit":("c-transit","DI JALAN"),"At Warehouse":("c-wh","DI GUDANG")}
    for _,r in df.sort_values("status").iterrows():
        cls,lab = chip[r.status]
        st.markdown(f"""
        <div class="rt">
          <div class="top"><b>{r.qr_code}</b> <span class="chip {cls}">{lab}</span></div>
          <small class="mono">{r.petani_nama} ({r.petani_kab}) → {r.sppg} · {r.jumlah_kg_sekolah:,} kg · {r.jarak_km} km
          · gudang {r.suhu_gudang_c}°C / {r.kelembaban_pct}% RH</small>
          <div class="pbar"><i style="width:{prog[r.status]}%"></i></div>
        </div>""", unsafe_allow_html=True)
    st.markdown('<div class="note-ops">Suhu &amp; kelembaban dari catatan gudang pada tiap batch. Telemetri sensor real-time di armada: roadmap.</div>', unsafe_allow_html=True)

st.page_link("pages/5_🏢_Dashboard_SPPG.py", label="← Kembali ke Dashboard SPPG")
st.markdown('<div class="note-ops">Prototipe: seluruh modul berjalan di atas model heuristik + data simulasi berlabel; arsitektur siap menerima data operasional aktual.</div>', unsafe_allow_html=True)
