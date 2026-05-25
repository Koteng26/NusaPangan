"""
🏛️ Government Command Center — Data Real PIHPS + BPS + Inflasi
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from utils import load_data, COMMON_CSS

st.set_page_config(page_title="Command Center", page_icon="🏛️", layout="wide")
st.markdown(COMMON_CSS, unsafe_allow_html=True)

df_harga = load_data("harga_beras_pihps.csv")
df_produksi = load_data("produksi_padi_bps.csv")
df_mbg = load_data("mbg_satpen.csv")
df_inflasi = load_data("inflasi_bps.csv")
df_farmers = load_data("farmers.csv")
df_journeys = load_data("journeys.csv")

st.markdown("""
<div class="np-header" style="background: linear-gradient(135deg, #1A237E, #283593, #3949AB);">
    <h2>🏛️ Government Command Center</h2>
    <p>Data Real — PIHPS Kemendag · BPS Produksi · Inflasi BI · MBG Kemendikdasmen</p>
</div>
""", unsafe_allow_html=True)

# Top metrics
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("👨‍🌾 Petani Verified", f"{len(df_farmers)}")
c2.metric("📦 Journey Active", f"{len(df_journeys)}")
mbg_total = df_mbg["jumlah_satpen"].sum()
c3.metric("🏫 Satpen MBG", f"{mbg_total:,}")
avg_dki = df_harga[df_harga["provinsi"]=="DKI Jakarta"]["harga_beras_medium_kg"].mean()
c4.metric("💰 Avg Beras DKI", f"Rp {avg_dki:,.0f}")
avg_btn = df_harga[df_harga["provinsi"]=="Banten"]["harga_beras_medium_kg"].mean()
c5.metric("💰 Avg Beras Banten", f"Rp {avg_btn:,.0f}")

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["📊 Price Radar PIHPS", "🌾 Produksi BPS", "🍽️ MBG Monitor", "📈 Inflasi & Alerts"])

with tab1:
    st.markdown("### 📊 Price Radar — Harga Beras Medium Real (PIHPS 2026)")
    st.markdown("*Sumber: SP2KP Kementerian Perdagangan 2026*")
    
    # Line chart per wilayah
    col_prov = st.selectbox("Pilih Provinsi", ["Semua", "DKI Jakarta", "Banten"])
    
    if col_prov == "Semua":
        filtered = df_harga.copy()
    else:
        filtered = df_harga[df_harga["provinsi"] == col_prov]
    
    fig = px.line(filtered, x="bulan", y="harga_beras_medium_kg", 
                  color="wilayah", line_group="wilayah",
                  markers=True,
                  labels={"harga_beras_medium_kg": "Harga (Rp/kg)", "bulan": "Bulan"},
                  title="Harga Beras Medium per Wilayah (Jan-Mei 2026)")
    fig.update_layout(height=450, plot_bgcolor="rgba(0,0,0,0)", 
                     yaxis=dict(gridcolor="#eee"),
                     legend=dict(orientation="h", yanchor="bottom", y=-0.4))
    st.plotly_chart(fig, use_container_width=True)
    
    # Comparison DKI vs Banten average
    st.markdown("##### 📊 Perbandingan Harga Rata-rata: DKI Jakarta vs Banten")
    df_avg = df_harga.groupby(["provinsi", "bulan"])["harga_beras_medium_kg"].mean().round(0).reset_index()
    fig_comp = px.bar(df_avg, x="bulan", y="harga_beras_medium_kg", color="provinsi",
                     barmode="group",
                     color_discrete_map={"DKI Jakarta": "#F44336", "Banten": "#4CAF50"},
                     labels={"harga_beras_medium_kg": "Harga Rata-rata (Rp/kg)"},
                     text="harga_beras_medium_kg")
    fig_comp.update_traces(texttemplate="Rp %{text:,.0f}", textposition="outside")
    fig_comp.update_layout(height=400, plot_bgcolor="rgba(0,0,0,0)", yaxis=dict(gridcolor="#eee"))
    st.plotly_chart(fig_comp, use_container_width=True)
    
    # Raw data table
    with st.expander("📋 Lihat Data Lengkap PIHPS"):
        st.dataframe(df_harga, use_container_width=True, hide_index=True)

with tab2:
    st.markdown("### 🌾 Produksi Padi per Provinsi (BPS 2026)")
    st.markdown("*Sumber: BPS — Produksi Padi Menurut Provinsi (Bulanan) 2026*")
    
    fig_prod = px.bar(df_produksi, x="bulan", y="produksi_ton", color="provinsi",
                     barmode="group",
                     labels={"produksi_ton": "Produksi (Ton)", "bulan": "Bulan"},
                     title="Produksi Padi Bulanan 2026 (Ton)")
    fig_prod.update_layout(height=450, plot_bgcolor="rgba(0,0,0,0)", yaxis=dict(gridcolor="#eee"))
    st.plotly_chart(fig_prod, use_container_width=True)
    
    # Highlight DKI vs Banten
    st.markdown("##### 🔴 DKI Jakarta vs 🟢 Banten — Gap Produksi Ekstrem")
    col_d, col_b = st.columns(2)
    
    prod_dki = df_produksi[df_produksi["provinsi"]=="DKI Jakarta"]
    prod_btn = df_produksi[df_produksi["provinsi"]=="Banten"]
    
    with col_d:
        st.markdown("**DKI Jakarta** (defisit total)")
        st.dataframe(prod_dki[["bulan", "produksi_ton"]].rename(columns={"produksi_ton": "Produksi (Ton)"}), 
                     use_container_width=True, hide_index=True)
        st.metric("Total Jan-Jun", f"{prod_dki['produksi_ton'].sum():,.1f} ton")
    
    with col_b:
        st.markdown("**Banten** (surplus)")
        st.dataframe(prod_btn[["bulan", "produksi_ton"]].rename(columns={"produksi_ton": "Produksi (Ton)"}),
                     use_container_width=True, hide_index=True)
        st.metric("Total Jan-Jun", f"{prod_btn['produksi_ton'].sum():,.0f} ton")
    
    ratio = prod_btn['produksi_ton'].sum() / max(prod_dki['produksi_ton'].sum(), 1)
    st.success(f"📊 **Banten memproduksi {ratio:,.0f}× lebih banyak dari DKI Jakarta** — ini peluang PanganLink untuk matching supply langsung ke SPPG Jakarta.")

with tab3:
    st.markdown("### 🍽️ MBG Monitor — Data Satuan Pendidikan")
    st.markdown("*Sumber: mbg.pdm.kemendikdasmen.go.id*")
    
    col_mbg1, col_mbg2 = st.columns(2)
    
    with col_mbg1:
        fig_mbg = px.bar(df_mbg, x="jenjang", y="jumlah_satpen", color="provinsi",
                        barmode="group",
                        color_discrete_map={"DKI Jakarta": "#2196F3", "Banten": "#4CAF50"},
                        text="jumlah_satpen",
                        labels={"jumlah_satpen": "Jumlah Satpen"})
        fig_mbg.update_traces(texttemplate="%{text:,}", textposition="outside")
        fig_mbg.update_layout(height=350, plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_mbg, use_container_width=True)
    
    with col_mbg2:
        # Pie chart total
        mbg_total_df = df_mbg.groupby("provinsi")["jumlah_satpen"].sum().reset_index()
        fig_pie = px.pie(mbg_total_df, values="jumlah_satpen", names="provinsi",
                        color_discrete_sequence=["#2196F3", "#4CAF50"],
                        hole=0.4, title="Distribusi Satpen MBG")
        fig_pie.update_layout(height=350)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    st.markdown(f"""
    > **Insight:** DKI Jakarta memiliki **{df_mbg[df_mbg['provinsi']=='DKI Jakarta']['jumlah_satpen'].sum():,}** satuan pendidikan MBG 
    > tapi produksi beras hampir nol. Banten memiliki **{df_mbg[df_mbg['provinsi']=='Banten']['jumlah_satpen'].sum():,}** satpen 
    > dengan surplus beras signifikan. NusaPangan menghubungkan keduanya.
    """)

with tab4:
    st.markdown("### 📈 Data Inflasi — BPS + Bank Indonesia")
    st.markdown("*Sumber: BPS rilis bulanan + Bank Indonesia*")
    
    # Inflasi chart
    fig_inf = go.Figure()
    fig_inf.add_trace(go.Bar(
        x=df_inflasi["bulan"] + " " + df_inflasi["tahun"].astype(str),
        y=df_inflasi["inflasi_umum_yoy"],
        name="Inflasi Umum (YoY %)",
        marker_color="#2196F3",
    ))
    fig_inf.add_trace(go.Scatter(
        x=df_inflasi["bulan"] + " " + df_inflasi["tahun"].astype(str),
        y=df_inflasi["volatile_food_yoy"],
        name="Volatile Food (YoY %)",
        line=dict(color="#F44336", width=3),
        mode="lines+markers",
    ))
    fig_inf.add_hline(y=5, line_dash="dash", line_color="#FF9800",
                     annotation_text="Target BI: <5%")
    fig_inf.update_layout(height=400, plot_bgcolor="rgba(0,0,0,0)", 
                         yaxis=dict(gridcolor="#eee", title="Persen (%)"),
                         legend=dict(orientation="h", yanchor="bottom", y=-0.2))
    st.plotly_chart(fig_inf, use_container_width=True)
    
    # Alerts
    st.markdown("##### ⚠️ Alert Center")
    st.markdown("""
    <div class="np-alert np-alert-red">
        <strong>🔴 Inflasi Volatile Food Feb 2026: 4.64% YoY</strong><br>
        Mendekati batas BI 5%. Komoditas penyumbang: cabai rawit, daging ayam, bawang merah, telur ayam, beras.<br>
        <em>Rekomendasi Price Radar: aktivasi operasi pasar + PanganLink matching dari surplus Banten.</em>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="np-alert np-alert-green">
        <strong>🟢 Inflasi Apr 2026 Melandai: 2.42% YoY</strong><br>
        Volatile food deflasi -0.88% MtM. Stabilitas harga pangan membaik.<br>
        <em>Efek GPIPS, operasi pasar Bapanas, dan KAD antarwilayah berhasil.</em>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("📋 Tabel Data Inflasi Lengkap"):
        st.dataframe(df_inflasi, use_container_width=True, hide_index=True)
