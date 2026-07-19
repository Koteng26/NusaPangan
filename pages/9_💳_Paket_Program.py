"""
💳 Paket & Program — dua lapis yang saling menghidupi:
petani (akuisisi & data, gratis) · institusi (monetisasi).
"""
import streamlit as st
import os, sys; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from utils import COMMON_CSS

st.set_page_config(page_title="Paket & Program", page_icon="💳", layout="wide")
st.markdown(COMMON_CSS, unsafe_allow_html=True)
ss = st.session_state

st.markdown("""
<div class="np-header" style="background:linear-gradient(135deg,#0E3A2C,#166534,#15803d);">
    <h2>💳 Paket &amp; Program</h2>
    <p><b>Petani tidak pernah menjadi sumber pendapatan — mereka sumber data.</b>
    Yang membayar adalah pihak yang membutuhkan kepastian: pembeli institusi dan lembaga.</p>
</div>
""", unsafe_allow_html=True)

if ss.get("petani"):
    p = ss["petani"]
    st.markdown(f'<div class="np-alert np-alert-green">👋 Halo <b>{p["nama"]}</b> ({p["rice_id"]}) — paket aktif Anda: <b>{p["paket"]}</b>.</div>', unsafe_allow_html=True)

# ============ LAPIS 1 — PETANI ============
st.markdown("### 👨‍🌾 Lapis 1 · Petani — akuisisi & mesin data")
def tier(col, name, price, color, items, tag=""):
    lis = "".join(f"<li style='margin:6px 0;font-size:.88rem;'>{x}</li>" for x in items)
    col.markdown(f"""
    <div class="np-card" style="border-top:5px solid {color};height:100%;">
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <b style="font-size:1.05rem;">{name}</b>
        {f"<span style='background:{color};color:#fff;font-size:.62rem;font-weight:800;padding:3px 10px;border-radius:999px;'>{tag}</span>" if tag else ""}
      </div>
      <div style="font-weight:900;color:{color};margin:4px 0 8px;">{price}</div>
      <ul style="padding-left:18px;margin:0;">{lis}</ul>
    </div>""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
tier(c1, "Petani", "Gratis selamanya", "#4CAF50",
     ["Profil & Rice ID terverifikasi", "Harga harian & informasi pasar", "Listing di AgriMart (jual ke SPPG/institusi)", "QR traceability untuk tiap batch"])
tier(c2, "Program Musim", "Gratis · didanai mitra", "#15803d",
     ["Semua fitur Petani", "Konsultasi ahli 10 jam / bulan", "Voucher input 1× (ditukar di toko tani mitra)", "Prediksi cuaca & waktu tanam"], tag="DIDANAI MITRA")
tier(c3, "NusaTani+", "Rp 49rb / musim (opsional)", "#C9902E",
     ["Semua fitur di atas", "Prioritas tampil ke pembeli", "Analitik panen lanjutan", "Sertifikat traceability beras premium/organik"])

st.markdown('<div class="np-alert np-alert-orange" style="margin-top:6px;">◆ Benefit Program Musim disponsori mitra input & pembiayaan — NusaPangan tidak menyimpan/menjual barang, dan lapis petani <b>bukan pusat laba</b>: tujuannya jumlah petani dan ketebalan data.</div>', unsafe_allow_html=True)

# ============ LAPIS 2 — INSTITUSI ============
st.markdown("### 🏢 Lapis 2 · Institusi — yang membayar")
k1, k2 = st.columns(2)
k1.markdown("""
<div class="np-card" style="border-top:5px solid #9F1239;height:100%;">
  <b style="font-size:1.05rem;">Pembeli Institusi</b>
  <div style="font-size:.8rem;color:#777;">SPPG · Bulog · katering & pembeli korporat</div>
  <ul style="padding-left:18px;margin-top:8px;">
    <li style="margin:6px 0;font-size:.88rem;"><b>Komisi transaksi 5%</b> per pembelian di AgriMart</li>
    <li style="margin:6px 0;font-size:.88rem;"><b>Langganan Dashboard Ops</b> — order, inventory, pengiriman, QR, analytics</li>
    <li style="margin:6px 0;font-size:.88rem;">SmartDistrib: optimasi rute & prakiraan kebutuhan</li>
  </ul>
</div>""", unsafe_allow_html=True)
k2.markdown("""
<div class="np-card" style="border-top:5px solid #1C6E8C;height:100%;">
  <b style="font-size:1.05rem;">Lembaga — Data &amp; Verifikasi</b>
  <div style="font-size:.8rem;color:#777;">Bank · asuransi · Pemda · Bulog (margin tertinggi)</div>
  <ul style="padding-left:18px;margin-top:8px;">
    <li style="margin:6px 0;font-size:.88rem;"><b>Laporan verifikasi petani</b> — profil + skor dari data lapangan</li>
    <li style="margin:6px 0;font-size:.88rem;"><b>Feed data wilayah</b> — prediksi panen & peta pasokan (LahanMap/LSD)</li>
    <li style="margin:6px 0;font-size:.88rem;">Akses hanya dengan <b>izin eksplisit petani</b> (UU PDP)</li>
  </ul>
</div>""", unsafe_allow_html=True)

# ============ MENGAPA BERLAPIS ============
st.markdown("""
<div class="np-card" style="margin-top:14px;background:#F0FDF4;">
  <b>Mengapa dua lapis ini saling menghidupi:</b>
  <span style="font-size:.9rem;">petani gratis → jumlah petani & catatan panen bertambah → data makin tebal
  → verifikasi & prediksi makin akurat → institusi membayar lebih → pendapatan itu membiayai layanan gratis petani. ↺</span>
</div>
<div class="np-alert np-alert-red" style="margin-top:10px;">
  <b>⚠️ NusaPangan TIDAK menyalurkan pinjaman.</b> Kami menjual data verifikasi — keputusan kredit,
  besaran, dan risikonya sepenuhnya pada lembaga keuangan. Petani tidak dipungut biaya verifikasi.
  Rincian harga final institusi ada pada dokumen proposal.
</div>
""", unsafe_allow_html=True)
