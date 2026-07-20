"""
🏛️ Government Command Center — Inflasi BI (real) + SPPG Monitoring + PIHPS + BPS
"""
import streamlit as st
import os, sys; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from utils import load_data, COMMON_CSS
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Command Center", page_icon="🏛️", layout="wide", initial_sidebar_state="collapsed")
st.markdown(COMMON_CSS, unsafe_allow_html=True)

df_harga = load_data("harga_beras_pihps.csv")
df_produksi = load_data("produksi_padi_bps.csv")
df_mbg = load_data("mbg_satpen.csv")
df_inflasi = load_data("inflasi_bps.csv")
df_bi = load_data("inflasi_bi.csv")
df_farmers = load_data("farmers.csv")
df_journeys = load_data("journeys.csv")

df_bi["tanggal"] = pd.to_datetime(df_bi["ym"] + "-01")
df_bi["tahun"] = df_bi["tanggal"].dt.year

st.markdown("""
<div class="np-header" style="background: linear-gradient(135deg, #1A237E, #283593, #3949AB);">
    <h2>🏛️ Government Command Center</h2>
    <p>Inflasi nasional, pasokan SPPG, harga pangan, dan produksi beras — satu dashboard.</p>
</div>
""", unsafe_allow_html=True)

# ===== Metrik puncak =====
avg_dki = df_harga[df_harga["provinsi"]=="DKI Jakarta"]["harga_beras_medium_kg"].mean()
avg_btn = df_harga[df_harga["provinsi"]=="Banten"]["harga_beras_medium_kg"].mean()
mbg_total = df_mbg["jumlah_satpen"].sum()
inf_now = df_bi.iloc[-1]; inf_prev = df_bi.iloc[-2]

st.markdown(f"""
<div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:20px;">
    <div style="flex:1;min-width:140px;background:linear-gradient(135deg,#1A237E,#3949AB);border-radius:14px;padding:18px;color:#fff;">
        <div style="font-size:0.75rem;opacity:0.8;">📈 Inflasi {inf_now['periode']}</div>
        <div style="font-size:1.8rem;font-weight:900;margin-top:4px;">{inf_now['inflasi']:.2f}%</div>
        <div style="font-size:0.7rem;opacity:0.85;">{'▲' if inf_now['inflasi']>=inf_prev['inflasi'] else '▼'} {abs(inf_now['inflasi']-inf_prev['inflasi']):.2f} pp vs bulan lalu</div>
    </div>
    <div style="flex:1;min-width:140px;background:linear-gradient(135deg,#1B5E20,#2E7D32);border-radius:14px;padding:18px;color:#fff;">
        <div style="font-size:0.75rem;opacity:0.8;">👨‍🌾 Petani Jaringan</div>
        <div style="font-size:1.8rem;font-weight:900;margin-top:4px;">{len(df_farmers)}</div>
        <div style="font-size:0.7rem;opacity:0.85;">3 tervalidasi lapangan</div>
    </div>
    <div style="flex:1;min-width:140px;background:linear-gradient(135deg,#0D47A1,#1565C0);border-radius:14px;padding:18px;color:#fff;">
        <div style="font-size:0.75rem;opacity:0.8;">📦 Journey Aktif</div>
        <div style="font-size:1.8rem;font-weight:900;margin-top:4px;">{len(df_journeys)}</div>
    </div>
    <div style="flex:1;min-width:140px;background:linear-gradient(135deg,#4A148C,#6A1B9A);border-radius:14px;padding:18px;color:#fff;">
        <div style="font-size:0.75rem;opacity:0.8;">🏫 Satpen MBG</div>
        <div style="font-size:1.8rem;font-weight:900;margin-top:4px;">{mbg_total:,}</div>
    </div>
    <div style="flex:1;min-width:140px;background:linear-gradient(135deg,#BF360C,#E65100);border-radius:14px;padding:18px;color:#fff;">
        <div style="font-size:0.75rem;opacity:0.8;">💰 Beras DKI vs Banten</div>
        <div style="font-size:1.35rem;font-weight:900;margin-top:6px;">Rp {avg_dki:,.0f} / {avg_btn:,.0f}</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["📈 Inflasi BI", "🍽️ SPPG Monitoring", "📊 Price Radar PIHPS", "🌾 Produksi BPS"])

# ============ TAB 1 — INFLASI BANK INDONESIA (DATA REAL) ============
with tab1:
    st.markdown("### 📈 Inflasi Nasional — Bank Indonesia")
    st.markdown(f"*Data resmi Bank Indonesia · **{len(df_bi)} bulan** ({df_bi['periode'].iloc[0]} – {df_bi['periode'].iloc[-1]})*")

    c1, c2, c3, c4 = st.columns(4)
    last12 = df_bi.tail(12)["inflasi"].mean()
    hi = df_bi.loc[df_bi["inflasi"].idxmax()]; lo = df_bi.loc[df_bi["inflasi"].idxmin()]
    c1.metric(f"Terkini · {inf_now['periode']}", f"{inf_now['inflasi']:.2f}%",
              f"{inf_now['inflasi']-inf_prev['inflasi']:+.2f} pp", delta_color="inverse")
    c2.metric("Rata-rata 12 bulan", f"{last12:.2f}%")
    c3.metric(f"Tertinggi · {hi['periode']}", f"{hi['inflasi']:.2f}%")
    c4.metric(f"Terendah · {lo['periode']}", f"{lo['inflasi']:.2f}%")

    yr_min, yr_max = int(df_bi["tahun"].min()), int(df_bi["tahun"].max())
    yr = st.slider("Rentang tahun", yr_min, yr_max, (2018, yr_max))
    dfv = df_bi[(df_bi["tahun"]>=yr[0]) & (df_bi["tahun"]<=yr[1])]

    fig = go.Figure()
    fig.add_hrect(y0=1.5, y1=3.5, fillcolor="#4CAF50", opacity=0.10, line_width=0,
                  annotation_text="Kisaran sasaran BI 2,5% ± 1", annotation_position="top left")
    fig.add_trace(go.Scatter(x=dfv["tanggal"], y=dfv["inflasi"], mode="lines",
                             name="Inflasi YoY (%)", line=dict(color="#283593", width=2.4),
                             fill="tozeroy", fillcolor="rgba(40,53,147,0.08)"))
    fig.update_layout(height=430, plot_bgcolor="rgba(0,0,0,0)",
                      yaxis=dict(gridcolor="#eee", title="Inflasi YoY (%)"),
                      xaxis=dict(title=""), showlegend=False,
                      margin=dict(t=20, b=10))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    > **Episode penting dalam data:** lonjakan **2005** & **2008** (kenaikan harga BBM & krisis global,
    > inflasi menembus dua digit), **2013** (penyesuaian BBM), lalu era stabil **2015–2021**, tekanan
    > pangan-energi **2022**, dan kembali ke kisaran sasaran hingga **{}** ({:.2f}%).
    """.format(inf_now["periode"], inf_now["inflasi"]))

    st.markdown("""
    <div class="np-alert np-alert-green">
        <strong>Mengapa ini panel utama NusaPangan?</strong><br>
        Beras adalah penyumbang bobot terbesar kelompok <em>volatile food</em> — penggerak utama gejolak inflasi.
        Transparansi harga gabah→beras dan kepastian pasokan Banten→DKI yang dibangun NusaPangan
        adalah instrumen langsung pengendalian inflasi pangan di tingkat daerah.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("##### Detail 2026 — Umum vs Volatile Food (BPS)")
    fig_inf = go.Figure()
    fig_inf.add_trace(go.Bar(x=df_inflasi["bulan"] + " " + df_inflasi["tahun"].astype(str),
                             y=df_inflasi["inflasi_umum_yoy"], name="Inflasi Umum (YoY %)",
                             marker_color="#2196F3"))
    fig_inf.add_trace(go.Scatter(x=df_inflasi["bulan"] + " " + df_inflasi["tahun"].astype(str),
                                 y=df_inflasi["volatile_food_yoy"], name="Volatile Food (YoY %)",
                                 line=dict(color="#F44336", width=3), mode="lines+markers"))
    fig_inf.update_layout(height=360, plot_bgcolor="rgba(0,0,0,0)",
                          yaxis=dict(gridcolor="#eee", title="Persen (%)"),
                          legend=dict(orientation="h", yanchor="bottom", y=-0.3))
    st.plotly_chart(fig_inf, use_container_width=True)

    with st.expander("📋 Tabel inflasi BI lengkap (283 bulan)"):
        st.dataframe(df_bi[["periode","inflasi"]].iloc[::-1], use_container_width=True, hide_index=True)

# ============ TAB 2 — SPPG MONITORING ============
with tab2:
    st.markdown("### 🍽️ SPPG Monitoring — Operasional Dapur MBG")
    st.markdown("*Simulasi berlabel — pola operasional; data satpen dari Kemendikdasmen.*")

    sppg = [
        {"nama":"SPPG SDN 03 Menteng","wil":"Jakarta Pusat","porsi":3000,"butuh":450,"stok_hari":2,"pasok":300},
        {"nama":"SPPG Tanah Abang","wil":"Jakarta Pusat","porsi":2400,"butuh":360,"stok_hari":6,"pasok":360},
        {"nama":"SPPG Serang Kota","wil":"Banten","porsi":1800,"butuh":270,"stok_hari":9,"pasok":270},
    ]
    cols = st.columns(3)
    for c,s in zip(cols,sppg):
        warna = "#C62828" if s["stok_hari"]<=3 else ("#EF6C00" if s["stok_hari"]<=5 else "#2E7D32")
        status = "KRITIS" if s["stok_hari"]<=3 else ("WASPADA" if s["stok_hari"]<=5 else "AMAN")
        c.markdown(f"""
        <div style="background:#fff;border:1px solid #E0E6E2;border-left:6px solid {warna};border-radius:12px;padding:14px;">
            <div style="font-weight:800;font-size:0.95rem;">{s['nama']}</div>
            <div style="font-size:0.75rem;color:#777;">{s['wil']} · {s['porsi']:,} porsi/hari</div>
            <div style="display:flex;gap:14px;margin-top:10px;font-size:0.8rem;">
                <div><b>{s['butuh']} kg</b><br><span style="color:#888;">butuh/hari</span></div>
                <div><b style="color:{warna};">{s['stok_hari']} hari</b><br><span style="color:#888;">stok tersisa</span></div>
                <div><b>{s['pasok']} kg</b><br><span style="color:#888;">terkontrak/hari</span></div>
            </div>
            <div style="margin-top:8px;font-size:0.7rem;font-weight:800;color:{warna};">● {status}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")
    dfs = pd.DataFrame(sppg)
    fig_s = go.Figure()
    fig_s.add_trace(go.Bar(x=dfs["nama"], y=dfs["butuh"], name="Kebutuhan/hari (kg)", marker_color="#283593"))
    fig_s.add_trace(go.Bar(x=dfs["nama"], y=dfs["pasok"], name="Pasokan terkontrak (kg)", marker_color="#2E7D32"))
    fig_s.update_layout(barmode="group", height=340, plot_bgcolor="rgba(0,0,0,0)",
                        yaxis=dict(gridcolor="#eee", title="kg / hari"),
                        legend=dict(orientation="h", yanchor="bottom", y=-0.3))
    st.plotly_chart(fig_s, use_container_width=True)

    st.markdown("##### 🚛 Pengiriman Aktif")
    st.dataframe(pd.DataFrame([
        {"Batch":"NP-BTN-2026-0847","Pemasok":"Pak Budi (Serang)","Tujuan":"SPPG Menteng","Qty":"500 kg","Status":"🚛 Dalam pengiriman","ETA":"10:00 hari ini"},
        {"Batch":"NP-BTN-2026-0851","Pemasok":"KT Maju (Serang)","Tujuan":"SPPG Tanah Abang","Qty":"1.200 kg","Status":"⏳ Menunggu konfirmasi","ETA":"—"},
        {"Batch":"NP-BTN-2026-0855","Pemasok":"Bu Siti (Pandeglang)","Tujuan":"SPPG Serang Kota","Qty":"300 kg","Status":"📦 Dijadwalkan","ETA":"besok 07:00"},
    ]), use_container_width=True, hide_index=True)

    st.markdown("""
    <div class="np-alert np-alert-red">
        <strong>🔴 SPPG Menteng — stok 2 hari, pasokan terkontrak 300/450 kg (gap 150 kg/hari)</strong><br>
        5 pemasok terverifikasi di Banten siap kirim (total 4.100 kg tersedia).<br>
        <em>Rekomendasi: buka permintaan di AgriMart + jadwalkan via SmartDistrib (rute 92 km, ±2,2 jam).</em>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("🏫 Cakupan Program — Satuan Pendidikan MBG (konteks pasar)"):
      col_mbg1, col_mbg2 = st.columns(2)
      with col_mbg1:
          fig_mbg = px.bar(df_mbg, x="jenjang", y="jumlah_satpen", color="provinsi", barmode="group",
                           color_discrete_map={"DKI Jakarta":"#2196F3","Banten":"#4CAF50"},
                           text="jumlah_satpen", labels={"jumlah_satpen":"Jumlah Satpen"})
          fig_mbg.update_traces(texttemplate="%{text:,}", textposition="outside")
          fig_mbg.update_layout(height=330, plot_bgcolor="rgba(0,0,0,0)")
          st.plotly_chart(fig_mbg, use_container_width=True)
      with col_mbg2:
          mbg_total_df = df_mbg.groupby("provinsi")["jumlah_satpen"].sum().reset_index()
          fig_pie = px.pie(mbg_total_df, values="jumlah_satpen", names="provinsi",
                           color_discrete_sequence=["#2196F3","#4CAF50"], hole=0.4,
                           title="Distribusi Satpen MBG")
          fig_pie.update_layout(height=330)
          st.plotly_chart(fig_pie, use_container_width=True)

# ============ TAB 3 — PRICE RADAR PIHPS ============
with tab3:
    st.markdown("### 📊 Price Radar — Harga Beras Medium Real (PIHPS 2026)")
    st.markdown("*Sumber: SP2KP Kementerian Perdagangan 2026*")
    col_prov = st.selectbox("Pilih Provinsi", ["Semua", "DKI Jakarta", "Banten"])
    filtered = df_harga if col_prov=="Semua" else df_harga[df_harga["provinsi"]==col_prov]
    fig = px.line(filtered, x="bulan", y="harga_beras_medium_kg", color="wilayah",
                  line_group="wilayah", markers=True,
                  labels={"harga_beras_medium_kg":"Harga (Rp/kg)","bulan":"Bulan"},
                  title="Harga Beras Medium per Wilayah (Jan-Mei 2026)")
    fig.update_layout(height=440, plot_bgcolor="rgba(0,0,0,0)", yaxis=dict(gridcolor="#eee"),
                      legend=dict(orientation="h", yanchor="bottom", y=-0.4))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("##### 📊 Perbandingan Harga Rata-rata: DKI Jakarta vs Banten")
    df_avg = df_harga.groupby(["provinsi","bulan"])["harga_beras_medium_kg"].mean().round(0).reset_index()
    fig_comp = px.bar(df_avg, x="bulan", y="harga_beras_medium_kg", color="provinsi", barmode="group",
                      color_discrete_map={"DKI Jakarta":"#F44336","Banten":"#4CAF50"},
                      labels={"harga_beras_medium_kg":"Harga Rata-rata (Rp/kg)"}, text="harga_beras_medium_kg")
    fig_comp.update_traces(texttemplate="Rp %{text:,.0f}", textposition="outside")
    fig_comp.update_layout(height=400, plot_bgcolor="rgba(0,0,0,0)", yaxis=dict(gridcolor="#eee"))
    st.plotly_chart(fig_comp, use_container_width=True)
    with st.expander("📋 Lihat Data Lengkap PIHPS"):
        st.dataframe(df_harga, use_container_width=True, hide_index=True)

# ============ TAB 4 — PRODUKSI BPS ============
with tab4:
    st.markdown("### 🌾 Produksi Padi per Provinsi (BPS 2026)")
    st.markdown("*Sumber: BPS — Produksi Padi Menurut Provinsi (Bulanan) 2026*")
    fig_prod = px.bar(df_produksi, x="bulan", y="produksi_ton", color="provinsi", barmode="group",
                      labels={"produksi_ton":"Produksi (Ton)","bulan":"Bulan"},
                      title="Produksi Padi Bulanan 2026 (Ton)")
    fig_prod.update_layout(height=440, plot_bgcolor="rgba(0,0,0,0)", yaxis=dict(gridcolor="#eee"))
    st.plotly_chart(fig_prod, use_container_width=True)

    st.markdown("##### 🔴 DKI Jakarta vs 🟢 Banten — Gap Produksi Ekstrem")
    col_d, col_b = st.columns(2)
    prod_dki = df_produksi[df_produksi["provinsi"]=="DKI Jakarta"]
    prod_btn = df_produksi[df_produksi["provinsi"]=="Banten"]
    with col_d:
        st.markdown("**DKI Jakarta** (defisit total)")
        st.dataframe(prod_dki[["bulan","produksi_ton"]].rename(columns={"produksi_ton":"Produksi (Ton)"}),
                     use_container_width=True, hide_index=True)
        st.metric("Total Jan-Jun", f"{prod_dki['produksi_ton'].sum():,.1f} ton")
    with col_b:
        st.markdown("**Banten** (surplus)")
        st.dataframe(prod_btn[["bulan","produksi_ton"]].rename(columns={"produksi_ton":"Produksi (Ton)"}),
                     use_container_width=True, hide_index=True)
        st.metric("Total Jan-Jun", f"{prod_btn['produksi_ton'].sum():,.0f} ton")
    ratio = prod_btn['produksi_ton'].sum() / max(prod_dki['produksi_ton'].sum(), 1)
    st.success(f"📊 **Banten memproduksi {ratio:,.0f}× lebih banyak dari DKI Jakarta** — koridor pasokan yang diverifikasi dan dihubungkan NusaPangan langsung ke SPPG Jakarta.")
