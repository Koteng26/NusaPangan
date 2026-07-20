"""
📋 About — transparansi prototipe: apa yang nyata, apa yang simulasi,
batasan, arsitektur, roadmap, dan tim.
"""
import streamlit as st
import os, sys; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from utils import COMMON_CSS
import pandas as pd

st.set_page_config(page_title="About", page_icon="📋", layout="wide")
st.markdown(COMMON_CSS, unsafe_allow_html=True)

st.markdown("""
<div class="np-header" style="background:linear-gradient(135deg,#0E3A2C,#166534 55%,#1C6E8C);">
    <p style="font-size:.75rem;opacity:.75;margin-bottom:6px;">TRANSPARANSI PROTOTIPE</p>
    <h2>📋 Sejauh mana ini nyata?</h2>
    <p style="margin-top:8px;">Halaman ini memetakan batas prototipe NusaPangan secara terbuka —
    data mana yang resmi, mana yang simulasi, dan apa yang belum kami bangun.</p>
</div>
""", unsafe_allow_html=True)

# ============ 1. NYATA vs SIMULASI ============
st.markdown("### 🔍 Apa yang Nyata, Apa yang Simulasi")

df = pd.DataFrame([
    ["Inflasi nasional bulanan", "✅ Data resmi", "Bank Indonesia — 283 bulan (Des 2002 – Jun 2026)"],
    ["Lahan Sawah Dilindungi Banten", "✅ Data resmi", "Kementerian ATR/BPN, SK 2021 — 149.163 ha · 47.937 bidang · 5 wilayah"],
    ["Harga beras & gabah", "✅ Data resmi", "SP2KP Kementerian Perdagangan (PIHPS) 2026"],
    ["Produksi padi per provinsi", "✅ Data resmi", "Badan Pusat Statistik 2026"],
    ["Satuan pendidikan program MBG", "✅ Data resmi", "Kemendikdasmen — 134.674 satpen DKI + Banten"],
    ["Inflasi umum & volatile food", "✅ Data resmi", "Badan Pusat Statistik 2026"],
    ["3 petani tervalidasi", "✅ Nyata", "Hasil wawancara lapangan langsung di Banten"],
    ["156 titik jaringan petani", "🟡 Campuran", "Koordinat wilayah nyata; atribut (nama, panen, harga) sintetis berlabel"],
    ["Listing AgriMart", "🟠 Simulasi berlabel", "Pola penawaran realistis berbasis harga PIHPS aktual"],
    ["Journey pengiriman & QR", "🟠 Simulasi berlabel", "15 batch contoh untuk memperagakan alur keterlacakan"],
    ["Skor kelayakan petani", "🟠 Simulasi berlabel", "Formula demonstratif dari komponen data lapangan"],
    ["Rute & ETA SmartDistrib", "🟠 Simulasi berlabel", "Heuristik jarak-waktu-risiko; koordinat koridor nyata"],
], columns=["Komponen", "Status", "Keterangan"])
st.dataframe(df, use_container_width=True, hide_index=True)

st.markdown("""
<div class="np-alert np-alert-green">
<b>Mengapa kami menampilkan ini.</b> Prototipe hackathon selalu mengandung simulasi — yang membedakan
adalah apakah batasnya dinyatakan. Setiap angka simulasi di platform ini diberi label pada halamannya masing-masing.
</div>
""", unsafe_allow_html=True)

# ============ 2. BATASAN ============
st.markdown("### ⚠️ Batasan Prototipe — yang BELUM kami bangun")
b1, b2 = st.columns(2)
b1.markdown("""
<div class="np-card" style="border-left:5px solid #DC2626;height:100%;">
<b>Belum berjalan</b>
<ul style="padding-left:18px;margin-top:8px;font-size:.88rem;line-height:1.9;">
<li>Pembayaran sungguhan — <b>escrow diselenggarakan mitra PJP berizin</b>, belum terpasang</li>
<li>Integrasi <b>API Dukcapil</b> — verifikasi kini oleh petugas lapangan, NIK di-hash (UU PDP)</li>
<li><b>Hash-chain</b> belum berjalan sebagai ledger produksi — arsitektur, bukan sistem aktif</li>
<li>GPS armada real-time — ETA dihitung dari jarak & profil koridor</li>
<li>Tidak ada perangkat <b>IoT</b>; suhu/kelembaban berasal dari catatan gudang</li>
</ul></div>""", unsafe_allow_html=True)
b2.markdown("""
<div class="np-card" style="border-left:5px solid #15803d;height:100%;">
<b>Yang sudah berjalan</b>
<ul style="padding-left:18px;margin-top:8px;font-size:.88rem;line-height:1.9;">
<li>Aplikasi petani <b>14 layar</b> berfungsi penuh (web app)</li>
<li>Pendaftaran → consent → <b>Rice ID</b> lintas halaman (session)</li>
<li>Peta <b>LSD resmi</b> di atas citra satelit + panel lapisan</li>
<li>Dashboard institusi &amp; Command Center dari data terpasang</li>
<li>Optimasi rute, prakiraan kebutuhan, dan papan pengiriman</li>
</ul></div>""", unsafe_allow_html=True)

st.markdown("""
<div class="np-alert np-alert-red">
<b>⚠️ NusaPangan TIDAK menyalurkan pinjaman dan tidak menyimpan dana pengguna.</b>
Kami menyediakan data verifikasi; keputusan kredit sepenuhnya pada lembaga keuangan.
Dana transaksi ditahan escrow oleh mitra penyedia jasa pembayaran berizin — bukan oleh NusaPangan.
</div>
""", unsafe_allow_html=True)

# ============ 3. ARSITEKTUR ============
st.markdown("### 🧩 Bagaimana Potongannya Menyatu")
a = st.columns(4)
arch = [
    ("📱", "Aplikasi Petani", "Rice ID, catat lahan & panen, jual, QR, skor kelayakan"),
    ("🗄️", "Lapisan Data", "LSD ATR/BPN, harga PIHPS, produksi BPS, inflasi BI, catatan panen"),
    ("🏢", "Dashboard Institusi", "SPPG & pembeli: order, inventory, pengiriman, analytics"),
    ("🏛️", "Pemerintah & Lembaga", "Command Center, laporan verifikasi, peta pasokan wilayah"),
]
ARCH_C = ["#15803d", "#0E9488", "#E11D48", "#1A237E"]
for c, (ic, t, d), warna in zip(a, arch, ARCH_C):
    c.markdown(f"""<div class="np-card" style="height:100%;text-align:center;
    border:1.5px solid {warna}30;border-top:4px solid {warna};background:linear-gradient(160deg,{warna}0A,#fff);">
    <div style="font-size:1.9rem;">{ic}</div>
    <b style="font-size:.95rem;color:{warna};">{t}</b>
    <div style="font-size:.78rem;color:#666;margin-top:6px;line-height:1.6;">{d}</div></div>""",
    unsafe_allow_html=True)

st.markdown("""
<div class="np-card" style="margin-top:10px;background:#F0FDF4;">
<b>Alur nilainya:</b> <span style="font-size:.9rem;">petani memakai platform gratis → data lapangan terkumpul dan
terverifikasi → institusi membayar untuk kepastian pasokan → lembaga membayar untuk verifikasi &amp; prediksi →
pendapatan itu membiayai layanan gratis petani. ↺</span>
</div>
""", unsafe_allow_html=True)

# ============ 4. ROADMAP ============
st.markdown("### 🛣️ Roadmap")
r1, r2, r3 = st.columns(3)
for col, (fase, judul, warna, items) in zip([r1, r2, r3], [
    ("FASE 1", "Fondasi kepercayaan", "#15803d",
     ["Integrasi API Dukcapil", "Escrow via mitra PJP berizin", "Hash-chain sebagai ledger aktif"]),
    ("FASE 2", "Kedalaman data lahan", "#C9902E",
     ["Lapisan Lahan Baku Sawah (LBS)", "Poligon lahan mandiri divalidasi petugas", "Analisis risiko alih fungsi (LBS−LSD)"]),
    ("FASE 3", "Perluasan koridor", "#1C6E8C",
     ["Koridor di luar Banten–DKI", "Produk verifikasi untuk bank & asuransi", "Kemitraan Bulog & pemerintah daerah"]),
]):
    lis = "".join(f"<li style='margin:6px 0;font-size:.86rem;'>{x}</li>" for x in items)
    col.markdown(f"""<div class="np-card" style="border-top:5px solid {warna};height:100%;">
    <div style="font-family:monospace;font-size:.7rem;letter-spacing:.1em;color:{warna};font-weight:700;">{fase}</div>
    <b style="font-size:1rem;">{judul}</b>
    <ul style="padding-left:18px;margin-top:8px;">{lis}</ul></div>""", unsafe_allow_html=True)

st.markdown('<p class="np-source">Sumber data: Bank Indonesia · Badan Pusat Statistik · SP2KP Kementerian Perdagangan · Kemendikdasmen · Kementerian ATR/BPN (Lahan Sawah Dilindungi, 2021).</p>', unsafe_allow_html=True)
