"""
🗺️ LahanMap — Lahan Sawah Dilindungi Banten (Pilar 3: Data Intelligence)
Peta LSD resmi ATR/BPN (2021) 5 wilayah di atas citra satelit,
dengan petani terverifikasi ditautkan ke atasnya.
"""
import streamlit as st
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from utils import load_data, COMMON_CSS, get_data_path
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="LahanMap", page_icon="🗺️", layout="wide")
st.markdown(COMMON_CSS, unsafe_allow_html=True)

with st.sidebar:
    c = st.columns([1, 3, 1])
    with c[1]:
        st.image("assets/logo.png", use_container_width=True)

# ---------- HEADER ----------
st.markdown("""
<div class="np-header" style="background:linear-gradient(135deg,#0E3A2C,#166534 45%,#1C6E8C);">
    <p style="font-size:0.75rem;opacity:0.7;margin-bottom:6px;">PILAR 3 · DATA INTELLIGENCE — Moat Spasial NusaPangan</p>
    <h2 style="font-size:1.7rem;font-weight:800;">🗺️ LahanMap — Sawah Dilindungi Banten</h2>
    <p style="font-size:1.02rem;line-height:1.55;margin-top:8px;font-weight:500;">
        Data <strong>Lahan Sawah Dilindungi (LSD) resmi ATR/BPN 2021</strong> untuk 5 wilayah,
        di atas citra satelit — dengan petani terverifikasi ditautkan ke atasnya.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------- LOAD DATA ----------
@st.cache_data
def load_lsd():
    with open(get_data_path("lsd_banten.geojson"), encoding="utf-8") as f:
        gj = json.load(f)
    rows = [{"KABUPATEN": ft["properties"]["KABUPATEN"],
             "LUAS": ft["properties"]["LUAS"],
             "BIDANG": ft["properties"]["BIDANG"]} for ft in gj["features"]]
    return gj, pd.DataFrame(rows)

gj_lsd, df_lsd = load_lsd()
df_farmers = load_data("farmers.csv")

TOTAL_HA = df_lsd["LUAS"].sum()
TOTAL_BIDANG = int(df_lsd["BIDANG"].sum())

# 3 petani tervalidasi lapangan (data nyata)
VERIFIED = pd.DataFrame([
    {"nama": "Petani 1", "lat": -6.18, "lon": 106.08, "varietas": "Inpari 32", "luas": "1,5 ha", "wil": "Kab. Serang", "harga": "Rp 6.000–6.500/kg"},
    {"nama": "Petani 2", "lat": -6.55, "lon": 105.95, "varietas": "Ciherang", "luas": "2 ha", "wil": "Kab. Pandeglang", "harga": "Rp 6.200–6.800/kg"},
    {"nama": "Petani 3", "lat": -6.60, "lon": 106.20, "varietas": "Inpari 42", "luas": "0,8 ha", "wil": "Kab. Lebak", "harga": "Rp 6.000/kg"},
])

# ---------- METRICS ----------
m1, m2, m3, m4 = st.columns(4)
m1.metric("🌾 Sawah Dilindungi", f"{TOTAL_HA:,.0f} ha", "SK ATR/BPN 2021")
m2.metric("📐 Jumlah Bidang", f"{TOTAL_BIDANG:,}", "5 wilayah")
m3.metric("✅ Petani Tervalidasi", "3", "wawancara lapangan")
m4.metric("📍 Titik Jaringan", f"{len(df_farmers)}", "koordinat nyata")

# ---------- PANEL LAPISAN (gaya GIS) ----------
st.markdown('<div style="font-family:monospace;font-size:.72rem;letter-spacing:.1em;color:#166534;font-weight:700;margin-bottom:4px;">⬒ PANEL LAPISAN</div>', unsafe_allow_html=True)
pc1, pc2, pc3 = st.columns([1.15, 1.5, 1.1])
with pc1:
    basemap = st.radio("Base map", ["Citra Satelit", "OSM", "Tanpa Latar"], index=0)
with pc2:
    st.caption("Lapisan data")
    show_lsd = st.checkbox("Lahan Sawah Dilindungi (ATR/BPN)", value=True)
    show_farmers = st.checkbox("Titik jaringan petani (156)", value=True)
    show_verified = st.checkbox("Petani tervalidasi lapangan (3)", value=True)
with pc3:
    FOKUS = {"Banten (semua)": (-6.75, 106.15, 8.1)}
    for _k in sorted(df_lsd["KABUPATEN"]):
        _lab = _k if str(_k).startswith("Kota") else "Kab. " + str(_k)
        FOKUS[_lab] = None
    _FZ = {"Kab. Serang": (-6.20, 106.05, 9.6), "Kab. Pandeglang": (-6.63, 105.93, 9.2),
           "Kab. Lebak": (-6.65, 106.25, 9.1), "Kab. Tangerang": (-6.20, 106.47, 9.8),
           "Kota Serang": (-6.11, 106.16, 11.0), "Kota Cilegon": (-6.00, 106.02, 11.0)}
    fokus = st.selectbox("Fokus wilayah", list(FOKUS.keys()))
    ctr_lat, ctr_lon, zm = FOKUS["Banten (semua)"] if FOKUS.get(fokus) else _FZ.get(fokus, (-6.75, 106.15, 8.1))
    if FOKUS.get(fokus): ctr_lat, ctr_lon, zm = FOKUS[fokus]

STCOL = {"Siap Panen": "#39A96B", "Pasca Panen": "#8AA79A", "Masa Tanam": "#59B3D6", "Masa Tumbuh": "#3E9E8E"}

# ---------- PETA ----------
fig = go.Figure()

# Layer 1: polygon LSD (choropleth by luas)
if show_lsd:
    fig.add_trace(go.Choroplethmapbox(
    geojson=gj_lsd, locations=df_lsd["KABUPATEN"], featureidkey="properties.KABUPATEN",
    z=df_lsd["LUAS"], colorscale="Greens", marker_opacity=0.5, marker_line_width=1,
    marker_line_color="#1B5E20",
    colorbar=dict(title="Luas LSD (ha)", thickness=12, len=0.5, x=0.99),
    customdata=df_lsd[["BIDANG"]].values,
    hovertemplate="<b>%{location}</b><br>Sawah dilindungi: %{z:,.0f} ha<br>Bidang: %{customdata[0]:,}<extra>LSD resmi</extra>",
    name="Sawah Dilindungi"
    ))

# Layer 2: 156 titik jaringan (per status, koordinat nyata / atribut sintetis)
if show_farmers:
    for status, col in STCOL.items():
        d = df_farmers[df_farmers["status"] == status]
        if len(d) == 0:
            continue
        fig.add_trace(go.Scattermapbox(
            lat=d["latitude"], lon=d["longitude"], mode="markers",
            marker=dict(size=8, color=col),
            text=d["desa"] + " · " + d["kabupaten"] + "<br>" + d["varietas"] + " · " + d["luas_lahan_ha"].astype(str) + " ha",
            hovertemplate="%{text}<br>Status: " + status + "<extra>titik jaringan (sintetis)</extra>",
            name=status
        ))

# Layer 3: 3 petani tervalidasi (emas, di atas)
if show_verified:
    fig.add_trace(go.Scattermapbox(
    lat=VERIFIED["lat"], lon=VERIFIED["lon"], mode="markers",
    marker=dict(size=17, color="#E7B24C"),
    text=VERIFIED["nama"] + " · " + VERIFIED["varietas"] + "<br>" + VERIFIED["wil"] + " · " + VERIFIED["luas"] + "<br>Harga: " + VERIFIED["harga"],
    hovertemplate="%{text}<extra>✓ tervalidasi lapangan</extra>",
    name="✓ Petani tervalidasi (3)"
    ))

# Basemap
if basemap == "Citra Satelit":
    mapbox = dict(
        style="white-bg",
        layers=[dict(below="traces", sourcetype="raster", sourceattribution="Esri, Maxar, Earthstar Geographics",
                     source=["https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"])],
        center=dict(lat=ctr_lat, lon=ctr_lon), zoom=zm
    )
elif basemap == "OSM":
    mapbox = dict(style="open-street-map", center=dict(lat=ctr_lat, lon=ctr_lon), zoom=zm)
else:
    mapbox = dict(style="white-bg", center=dict(lat=ctr_lat, lon=ctr_lon), zoom=zm)

fig.update_layout(
    mapbox=mapbox, margin=dict(l=0, r=0, t=0, b=0), height=560,
    legend=dict(orientation="h", yanchor="bottom", y=0.01, xanchor="left", x=0.01,
                bgcolor="rgba(255,255,255,0.85)", font=dict(size=11)),
    paper_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(fig, use_container_width=True)

# ---------- RINCIAN PER WILAYAH ----------
st.markdown("### 📊 Sawah Dilindungi per Wilayah")
df_show = df_lsd.sort_values("LUAS", ascending=False).copy()
def _count_titik(k):
    target = k if k.startswith("Kota") else "Kab. " + k
    return int((df_farmers["kabupaten"] == target).sum())
df_show["Titik jaringan"] = df_show["KABUPATEN"].map(_count_titik)
df_show = df_show.rename(columns={"KABUPATEN": "Wilayah", "LUAS": "Luas LSD (ha)", "BIDANG": "Bidang"})
df_show["Luas LSD (ha)"] = df_show["Luas LSD (ha)"].round(0).astype(int)
st.dataframe(df_show, use_container_width=True, hide_index=True)

# ---------- MOAT + KEJUJURAN ----------
cA, cB = st.columns(2)
with cA:
    st.markdown("""
    <div class="np-alert np-alert-green">
        <b>🛡️ Kenapa ini moat.</b> Layer LSD publik bisa diunduh siapa saja — itu fondasi.
        Yang tidak bisa ditiru adalah <b>petani terverifikasi lapangan</b> yang ditautkan ke atasnya,
        dan riwayat panennya yang menebal tiap musim.
    </div>""", unsafe_allow_html=True)
with cB:
    st.markdown("""
    <div class="np-alert np-alert-orange">
        <b>📋 Kejujuran data.</b> Polygon = LSD resmi ATR/BPN 2021 (disederhanakan untuk web; 149.163 ha,
        47.937 bidang — angka utuh). <b>3 titik = petani nyata</b> hasil wawancara.
        156 titik jaringan berkoordinat nyata namun beratribut sintetis — diganti petani nyata tiap musim.
    </div>""", unsafe_allow_html=True)

st.markdown('<p class="np-source">Sumber: Kementerian ATR/BPN — Lahan Sawah Dilindungi (SK 2021) · farmers.csv (jaringan). Citra: Esri World Imagery.</p>', unsafe_allow_html=True)
