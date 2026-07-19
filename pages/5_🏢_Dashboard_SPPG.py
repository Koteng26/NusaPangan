"""
🏢 Dashboard SPPG / Institutional Buyer — Ops Center
Order, inventory, pengiriman, QR trace, dan analytics dalam satu layar.
"""
import streamlit as st
import os, sys; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from utils import load_data
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard SPPG", page_icon="🏢", layout="wide")

# ============ TEMA OPS CENTER (gelap, khusus halaman ini) ============
st.markdown("""
<style>
.stApp{background:radial-gradient(130% 110% at 75% -5%, #12261E 0%, #0B1713 48%, #070F0C 100%);}
.stApp, .stApp p, .stApp label, .stApp span{color:#D7E5DD;}
h1,h2,h3,h4{color:#F2F7F4 !important;}
[data-testid="stMetricValue"]{color:#fff;}
.ops-head{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin-bottom:4px;}
.ops-live{display:inline-flex;align-items:center;gap:7px;font-family:ui-monospace,monospace;font-size:11px;
letter-spacing:.14em;color:#4ADE80;background:rgba(74,222,128,.08);border:1px solid rgba(74,222,128,.25);
padding:5px 12px;border-radius:999px;}
.ops-live i{width:7px;height:7px;border-radius:50%;background:#4ADE80;animation:blink 1.6s infinite;}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.2}}
.ops-sub{font-family:ui-monospace,monospace;font-size:11px;letter-spacing:.08em;color:#E7B24C;
background:rgba(231,178,76,.08);border:1px solid rgba(231,178,76,.3);padding:5px 12px;border-radius:999px;}
.kpi{background:linear-gradient(160deg,rgba(255,255,255,.05),rgba(255,255,255,.015));
border:1px solid rgba(255,255,255,.08);border-radius:14px;padding:14px 16px;height:100%;}
.kpi .l{font-size:.68rem;letter-spacing:.08em;text-transform:uppercase;color:#8FA89C;}
.kpi .v{font-size:1.55rem;font-weight:900;color:#fff;margin-top:3px;font-family:ui-monospace,monospace;}
.kpi .s{font-size:.68rem;color:#8FA89C;margin-top:2px;}
.ship{background:linear-gradient(160deg,rgba(255,255,255,.045),rgba(255,255,255,.012));
border:1px solid rgba(255,255,255,.08);border-radius:14px;padding:13px 15px;margin-bottom:10px;}
.ship .top{display:flex;justify-content:space-between;gap:8px;align-items:center;flex-wrap:wrap;}
.ship b{color:#fff;font-size:.9rem;}
.ship small{color:#8FA89C;font-size:.72rem;}
.chip{font-size:.66rem;font-weight:800;letter-spacing:.05em;padding:4px 10px;border-radius:999px;}
.c-transit{background:rgba(231,178,76,.14);color:#E7B24C;border:1px solid rgba(231,178,76,.35);}
.c-done{background:rgba(74,222,128,.12);color:#4ADE80;border:1px solid rgba(74,222,128,.3);}
.c-wh{background:rgba(96,165,250,.12);color:#60A5FA;border:1px solid rgba(96,165,250,.3);}
.pbar{height:7px;background:rgba(255,255,255,.07);border-radius:4px;margin-top:9px;overflow:hidden;}
.pbar i{display:block;height:100%;border-radius:4px;background:linear-gradient(90deg,#39A96B,#4ADE80);}
.qr{font-family:ui-monospace,monospace;font-size:.7rem;color:#9FC2B2;}
.panel{background:linear-gradient(165deg,rgba(255,255,255,.05),rgba(255,255,255,.015));
border:1px solid rgba(255,255,255,.08);border-radius:16px;padding:16px;}
.list-row{display:flex;justify-content:space-between;gap:8px;padding:8px 0;
border-bottom:1px solid rgba(255,255,255,.06);font-size:.8rem;}
.list-row:last-child{border:0;}
.note-ops{font-size:.72rem;color:#7E958A;border-left:3px solid rgba(231,178,76,.5);padding:6px 12px;margin-top:14px;}
</style>
""", unsafe_allow_html=True)

df = load_data("journeys.csv")

# ============ HEADER ============
st.markdown("""
<div class="ops-head">
  <h2 style="margin:0;">🏢 Institutional Buyer — Ops Center</h2>
  <span class="ops-live"><i></i>LIVE</span>
  <span class="ops-sub">LANGGANAN DASHBOARD · Rp 5 jt/bln</span>
</div>
<p style="color:#8FA89C;font-size:.85rem;margin-top:2px;">
Pantau order, pengiriman, inventory, traceability, dan pasokan — satu layar untuk SPPG &amp; pembeli institusi.</p>
""", unsafe_allow_html=True)

# ============ PILIH SPPG ============
OPS = {
    "SPPG Jakarta Pusat":  {"porsi":3000,"butuh":450,"stok_kg": 900,"ontime":96},
    "SPPG Jakarta Barat":  {"porsi":2600,"butuh":390,"stok_kg":2340,"ontime":98},
    "SPPG Jakarta Timur":  {"porsi":2400,"butuh":360,"stok_kg":1800,"ontime":95},
    "SPPG Jakarta Selatan":{"porsi":2000,"butuh":300,"stok_kg":2400,"ontime":97},
    "SPPG Jakarta Utara":  {"porsi":1600,"butuh":240,"stok_kg":1680,"ontime":94},
}
sel = st.selectbox("Masuk sebagai", list(OPS.keys()), index=0)
ops = OPS[sel]
d = df[df["sppg"]==sel].copy()

stok_hari = ops["stok_kg"]/ops["butuh"]
warna_stok = "#E5484D" if stok_hari<=3 else ("#E7B24C" if stok_hari<=5 else "#4ADE80")
in_transit = (d["status"]=="In Transit").sum()
at_wh = (d["status"]=="At Warehouse").sum()
delivered_kg = int(d.loc[d["status"]=="Delivered","jumlah_kg_sekolah"].sum())
incoming_kg = int(d.loc[d["status"]!="Delivered","jumlah_kg_sekolah"].sum())

# ============ KPI STRIP ============
k = st.columns(6)
kpis = [
    ("Porsi / hari", f"{ops['porsi']:,}", "kapasitas dapur", "#fff"),
    ("Kebutuhan beras", f"{ops['butuh']} kg", "per hari", "#fff"),
    ("Stok tersisa", f"{stok_hari:.1f} hari", f"{ops['stok_kg']:,} kg di gudang", warna_stok),
    ("Batch masuk", f"{in_transit+at_wh}", f"{in_transit} di jalan · {at_wh} di gudang", "#60A5FA"),
    ("Diterima (musim ini)", f"{delivered_kg:,} kg", "terverifikasi QR", "#4ADE80"),
    ("On-time rate", f"{ops['ontime']}%", "30 hari terakhir", "#4ADE80"),
]
for col,(l,v,s,c) in zip(k,kpis):
    col.markdown(f'<div class="kpi"><div class="l">{l}</div><div class="v" style="color:{c};">{v}</div><div class="s">{s}</div></div>', unsafe_allow_html=True)

st.markdown("")

# ============ GRID UTAMA ============
kiri, kanan = st.columns([1.9, 1])

with kiri:
    st.markdown("#### 🚛 Order & Pengiriman")
    if d.empty:
        st.info("Belum ada order aktif untuk SPPG ini.")
    prog = {"Delivered":100, "In Transit":62, "At Warehouse":28}
    chip = {"Delivered":("c-done","TIBA ✓"), "In Transit":("c-transit","DI JALAN"), "At Warehouse":("c-wh","DI GUDANG ASAL")}
    for _,r in d.sort_values("status").iterrows():
        cls,lab = chip[r["status"]]
        eta = r["tanggal_tiba"] if r["status"]!="Delivered" else f"tiba {r['tanggal_tiba']}"
        st.markdown(f"""
        <div class="ship">
          <div class="top">
            <div><b>{r['jumlah_kg_sekolah']:,} kg {r['komoditas']}</b> · <span class="qr">{r['qr_code']}</span><br>
            <small>{r['petani_nama']} — {r['petani_desa']}, {r['petani_kab']} → {r['sekolah']} · {r['jarak_km']} km</small></div>
            <span class="chip {cls}">{lab}</span>
          </div>
          <div class="pbar"><i style="width:{prog[r['status']]}%"></i></div>
          <small style="display:block;margin-top:5px;">ETA {eta} · rendemen {r['rendemen_pct']}% · gudang {r['gudang']}</small>
        </div>
        """, unsafe_allow_html=True)

with kanan:
    st.markdown("#### 📦 Inventory")
    pct = min(100, stok_hari/10*100)
    st.markdown(f"""
    <div class="panel">
      <div style="display:flex;justify-content:space-between;font-size:.8rem;">
        <span>Beras di gudang</span><b style="color:#fff;">{ops['stok_kg']:,} kg</b></div>
      <div class="pbar"><i style="width:{pct:.0f}%;background:linear-gradient(90deg,{warna_stok},{warna_stok});"></i></div>
      <div style="display:flex;justify-content:space-between;font-size:.72rem;color:#8FA89C;margin-top:6px;">
        <span>≈ {stok_hari:.1f} hari operasi</span><span>ambang aman: 5 hari</span></div>
      <div class="list-row" style="margin-top:10px;"><span>Dalam perjalanan</span><b style="color:#E7B24C;">{incoming_kg:,} kg</b></div>
      <div class="list-row"><span>Konsumsi / hari</span><b>{ops['butuh']} kg</b></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 🔍 QR Terverifikasi")
    rows = "".join(
        f'<div class="list-row"><span class="qr">{r["qr_code"]}</span><span style="color:#4ADE80;">✓ {r["petani_nama"].split()[0]}</span></div>'
        for _,r in d.head(5).iterrows())
    st.markdown(f'<div class="panel">{rows if rows else "<small>—</small>"}</div>', unsafe_allow_html=True)
    st.page_link("pages/2_🔍_QR_Trace.py", label="Buka QR Traceability →")

# ============ AGRIMART LISTING ============
st.markdown("#### 🛒 AgriMart — Listing Terbuka dari Petani")
la, lb, lc, ld = st.columns([1,1,1,.9])
listing = [
    ("Gabah Inpari 32 — Pak Budi","Serang · stok 2.000 kg","Rp 6.800/kg"),
    ("Ciherang — KT Maju","Serang · stok 1.200 kg","Rp 6.500/kg"),
    ("GKG Inpari 42 — Bu Siti","Pandeglang · stok 800 kg","Rp 7.600/kg"),
]
for col,(n,s,p) in zip([la,lb,lc],listing):
    col.markdown(f"""
    <div class="panel" style="padding:13px;">
      <b style="color:#fff;font-size:.85rem;">{n}</b><br><small style="color:#8FA89C;">{s} · ✓ terverifikasi lapangan</small>
      <div style="margin-top:8px;font-family:ui-monospace,monospace;font-weight:800;color:#E7B24C;">{p}</div>
    </div>""", unsafe_allow_html=True)
with ld:
    st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
    st.page_link("pages/4_🛒_AgriMart.py", label="🛒 Buka AgriMart →")
    st.page_link("pages/6_🚛_SmartDistrib.py", label="🚛 Jadwalkan via SmartDistrib →")

# ============ ANALYTICS ============
st.markdown("#### 📊 Analytics")
a1, a2 = st.columns(2)
dark = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#BFD4C9"), margin=dict(t=36,b=10,l=10,r=10), height=310)

with a1:
    agg = df.groupby("sppg")["jumlah_kg_sekolah"].sum().reset_index()
    agg["warna"] = ["#39A96B" if s==sel else "rgba(255,255,255,.18)" for s in agg["sppg"]]
    fig1 = go.Figure(go.Bar(x=agg["sppg"].str.replace("SPPG ",""), y=agg["jumlah_kg_sekolah"],
                            marker_color=agg["warna"], text=agg["jumlah_kg_sekolah"],
                            texttemplate="%{text:,} kg", textposition="outside"))
    fig1.update_layout(title="Volume per SPPG (kg)", yaxis=dict(gridcolor="#1E2E27"),
                       xaxis=dict(gridcolor="#1E2E27"), **dark)
    st.plotly_chart(fig1, use_container_width=True)

with a2:
    src = d.groupby("petani_kab")["jumlah_kg_sekolah"].sum().reset_index() if not d.empty \
          else pd.DataFrame({"petani_kab":["—"],"jumlah_kg_sekolah":[1]})
    fig2 = px.pie(src, values="jumlah_kg_sekolah", names="petani_kab", hole=.55,
                  color_discrete_sequence=["#39A96B","#E7B24C","#60A5FA","#9F7AEA"])
    fig2.update_layout(title=f"Sumber pasokan — {sel.replace('SPPG ','')}", **dark)
    st.plotly_chart(fig2, use_container_width=True)

# ============ REKOMENDASI ============
st.markdown(f"""
<div class="panel" style="border-left:4px solid #E7B24C;">
  <b style="color:#E7B24C;">⚡ Rekomendasi hari ini</b><br>
  <span style="font-size:.85rem;">Stok {sel.replace('SPPG ','')} {'kritis' if stok_hari<=3 else 'terpantau'} ({stok_hari:.1f} hari).
  {('Buka permintaan di AgriMart — 3 pemasok Banten siap kirim, rute tercepat 92 km / ±2,2 jam via SmartDistrib.' if stok_hari<=3 else 'Pasokan terkontrak berjalan normal; jadwal berikutnya sudah di SmartDistrib.')}</span>
</div>
<div class="note-ops">Simulasi berlabel — pola operasional demo dari data journey terlacak.
Pembayaran memakai escrow yang diselenggarakan <b>mitra penyedia jasa pembayaran berizin</b> — bukan oleh NusaPangan.</div>
""", unsafe_allow_html=True)
