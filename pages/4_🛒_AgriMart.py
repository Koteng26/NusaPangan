"""
🛒 AgriMart — Marketplace Beras & Gabah (MVP)
Alur sederhana: Browse → Detail → Request Order. Tanpa checkout/escrow di prototipe.
"""
import streamlit as st
import os, sys; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from utils import COMMON_CSS

st.set_page_config(page_title="AgriMart", page_icon="🛒", layout="wide")
st.markdown(COMMON_CSS, unsafe_allow_html=True)
ss = st.session_state

st.markdown("""
<div class="np-header" style="background:linear-gradient(135deg,#9F1239,#C2274E,#E11D48);">
    <h2>🛒 AgriMart</h2>
    <p>Marketplace gabah &amp; beras dari petani terverifikasi — untuk SPPG dan pembeli institusi.</p>
</div>
""", unsafe_allow_html=True)

if ss.get("petani"):
    p = ss["petani"]
    st.markdown(f'<div class="np-alert np-alert-green">🌾 Listing Anda aktif: <b>{p["varietas"]}</b> · {p["luas"]} ha · {p["kabupaten"]} ({p["rice_id"]}) — tampil untuk semua pembeli institusi.</div>', unsafe_allow_html=True)

LISTINGS = [
    {"id":"L1","nama":"Gabah Kering Panen — Inpari 32","penjual":"Pak Budi Santoso","tipe":"GKP","kab":"Kab. Serang","stok":2000,"harga":6800,"panen":"Juli 2026","musim":4,"rendemen":"63–65%","riceid":"NP-BTN-2026-0847"},
    {"id":"L2","nama":"Gabah Kering Panen — Ciherang","penjual":"KT Maju Bersama","tipe":"GKP","kab":"Kab. Serang","stok":1200,"harga":6500,"panen":"Juli 2026","musim":6,"rendemen":"62–64%","riceid":"NP-BTN-2026-0812"},
    {"id":"L3","nama":"Gabah Kering Giling — Inpari 42","penjual":"Bu Siti Aminah","tipe":"GKG","kab":"Kab. Pandeglang","stok":800,"harga":7600,"panen":"Juni 2026","musim":5,"rendemen":"64–66%","riceid":"NP-BTN-2026-0793"},
    {"id":"L4","nama":"Beras Medium — Situ Bagendit","penjual":"KT Sejahtera","tipe":"Beras","kab":"Kab. Lebak","stok":600,"harga":12980,"panen":"Juni 2026","musim":7,"rendemen":"—","riceid":"NP-BTN-2026-0761"},
    {"id":"L5","nama":"Beras Organik — Mentik Wangi","penjual":"Pak Rahmat","tipe":"Beras","kab":"Kab. Serang","stok":300,"harga":15500,"panen":"Juli 2026","musim":3,"rendemen":"—","riceid":"NP-BTN-2026-0888"},
    {"id":"L6","nama":"Gabah Kering Panen — Situ Bagendit","penjual":"Hasan Kurniawan","tipe":"GKP","kab":"Kab. Serang","stok":1500,"harga":6600,"panen":"Juli 2026","musim":4,"rendemen":"63%","riceid":"NP-2001"},
]

# ============ DETAIL VIEW ============
if ss.get("am_sel"):
    it = next((l for l in LISTINGS if l["id"]==ss["am_sel"]), None)
    if it is None:
        ss["am_sel"] = None; st.rerun()
    if st.button("← Kembali ke listing"):
        ss["am_sel"] = None; st.rerun()

    ka, kb = st.columns([1.4, 1])
    with ka:
        st.markdown(f"""
        <div class="np-card">
          <div style="font-size:1.25rem;font-weight:800;color:#1B5E20;">{it['nama']}</div>
          <div style="color:#666;font-size:.9rem;margin-top:2px;">{it['penjual']} · {it['kab']} · panen {it['panen']}</div>
          <div style="margin-top:10px;">
            <span style="background:#DCF5E6;color:#166534;font-size:.75rem;font-weight:700;padding:4px 12px;border-radius:999px;">✓ Terverifikasi Petugas Lapangan</span>
            <span style="background:#EEF2FF;color:#3730A3;font-size:.75rem;font-weight:700;padding:4px 12px;border-radius:999px;margin-left:6px;">Rice ID {it['riceid']}</span>
          </div>
          <div style="display:flex;gap:26px;margin-top:16px;">
            <div><b style="font-size:1.15rem;">{it['stok']:,} kg</b><br><small style="color:#888;">stok tersedia</small></div>
            <div><b style="font-size:1.15rem;">{it['musim']}</b><br><small style="color:#888;">musim tercatat</small></div>
            <div><b style="font-size:1.15rem;">{it['rendemen']}</b><br><small style="color:#888;">rendemen historis</small></div>
          </div>
        </div>""", unsafe_allow_html=True)
        st.markdown('<div class="np-alert np-alert-green" style="margin-top:10px;">Riwayat panen & transaksi penjual tercatat di platform dan dapat diaudit pembeli institusi sebelum konfirmasi.</div>', unsafe_allow_html=True)

    with kb:
        st.markdown(f'<div class="np-card" style="text-align:center;"><div style="font-size:.8rem;color:#888;">Harga ditawarkan</div><div style="font-size:1.9rem;font-weight:900;color:#9F1239;">Rp {it["harga"]:,}/kg</div></div>', unsafe_allow_html=True)
        qty = st.number_input("Jumlah diminta (kg)", 100, it["stok"], min(500, it["stok"]), 100)
        st.markdown(f"""
        <div class="np-card" style="font-size:.9rem;">
          <div style="display:flex;justify-content:space-between;"><span>Perkiraan nilai</span><b>Rp {qty*it['harga']:,}</b></div>
          <div style="display:flex;justify-content:space-between;color:#888;"><span>Komisi platform 5%</span><span>ditanggung pembeli institusi</span></div>
        </div>""", unsafe_allow_html=True)
        if st.button("📨 Request Order", type="primary", use_container_width=True):
            st.success(f"Permintaan {qty:,} kg terkirim ke {it['penjual']}. Penjual akan mengonfirmasi ketersediaan & jadwal. Pembayaran (escrow oleh mitra PJP berizin — bukan NusaPangan) dilakukan setelah konfirmasi.")
            st.balloons()
        st.page_link("pages/6_🚛_SmartDistrib.py", label="🚛 Rencanakan pengiriman di SmartDistrib →")
    st.stop()

# ============ BROWSE VIEW ============
f1, f2, f3 = st.columns([1,1,1])
tipe = f1.selectbox("Jenis", ["Semua","GKP","GKG","Beras"])
kab = f2.selectbox("Wilayah", ["Semua"]+sorted({l["kab"] for l in LISTINGS}))
urut = f3.selectbox("Urutkan", ["Harga terendah","Harga tertinggi","Stok terbanyak"])

items = [l for l in LISTINGS if (tipe=="Semua" or l["tipe"]==tipe) and (kab=="Semua" or l["kab"]==kab)]
items.sort(key=lambda l: l["harga"] if urut=="Harga terendah" else (-l["harga"] if urut=="Harga tertinggi" else -l["stok"]))

st.markdown(f"**{len(items)} penawaran aktif** · semua penjual terverifikasi lapangan")
cols = st.columns(3)
for i,it in enumerate(items):
    with cols[i%3]:
        st.markdown(f"""
        <div class="np-card" style="margin-bottom:4px;">
          <div style="display:flex;justify-content:space-between;align-items:start;">
            <b style="font-size:.95rem;color:#1B5E20;">{it['nama']}</b>
            <span style="background:#FCE7EF;color:#9F1239;font-size:.66rem;font-weight:800;padding:3px 9px;border-radius:999px;">{it['tipe']}</span>
          </div>
          <div style="font-size:.78rem;color:#777;margin-top:3px;">{it['penjual']} · {it['kab']}</div>
          <div style="font-size:.72rem;color:#166534;margin-top:5px;">✓ terverifikasi · stok {it['stok']:,} kg</div>
          <div style="font-size:1.25rem;font-weight:900;color:#9F1239;margin-top:8px;">Rp {it['harga']:,}<span style="font-size:.75rem;color:#888;font-weight:600;">/kg</span></div>
        </div>""", unsafe_allow_html=True)
        if st.button("Lihat Detail →", key="btn_"+it["id"], use_container_width=True):
            ss["am_sel"] = it["id"]; st.rerun()

st.markdown('<div class="np-alert np-alert-orange" style="margin-top:16px;"><b>MVP demo.</b> Alur prototipe berhenti di Request Order — tanpa checkout. Pembayaran produksi memakai escrow yang diselenggarakan <b>mitra penyedia jasa pembayaran berizin</b>, bukan NusaPangan. Listing merupakan simulasi berlabel berbasis pola petani jaringan.</div>', unsafe_allow_html=True)
