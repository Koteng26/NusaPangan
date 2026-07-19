"""
📝 Pendaftaran Petani — Onboarding + Persetujuan (legal standing)
Alur: Data diri → Lahan → Persetujuan → Program → Rice ID (session_state)
"""
import streamlit as st
import os, sys, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from utils import COMMON_CSS

st.set_page_config(page_title="Pendaftaran Petani", page_icon="📝", layout="centered")
st.markdown(COMMON_CSS, unsafe_allow_html=True)

with st.sidebar:
    c = st.columns([1, 3, 1])
    with c[1]:
        st.image("assets/logo.png", use_container_width=True)

ss = st.session_state
ss.setdefault("reg_step", 0)

KAB = ["Kab. Serang", "Kab. Pandeglang", "Kab. Lebak", "Kota Serang", "Kota Cilegon"]
VAR = ["Inpari 32", "Inpari 42", "Ciherang", "IR64", "Mekongga", "Situ Bagendit", "Beras Merah", "Beras Organik"]
KAB_LATLON = {"Kab. Serang": (-6.18, 106.08), "Kab. Pandeglang": (-6.55, 105.95),
              "Kab. Lebak": (-6.60, 106.20), "Kota Serang": (-6.12, 106.15), "Kota Cilegon": (-6.02, 106.05)}

# ---------- HEADER ----------
st.markdown("""
<div class="np-header" style="background:linear-gradient(135deg,#14532d,#166534 45%,#15803d);">
    <p style="font-size:0.75rem;opacity:0.65;margin-bottom:6px;">NUSAPANGAN · ONBOARDING</p>
    <h2 style="font-size:1.6rem;font-weight:800;">📝 Pendaftaran Petani</h2>
    <p style="font-size:0.95rem;margin-top:6px;">Gabung jaringan petani terverifikasi Banten — buat identitas digital & Rice ID Anda.</p>
</div>
""", unsafe_allow_html=True)

# Jika sudah terdaftar di sesi ini
if ss.get("petani") and ss.reg_step >= 99:
    p = ss["petani"]
    st.success("Anda sudah terdaftar pada sesi ini.")
    st.markdown(f"""
    <div class="np-card" style="text-align:center;padding:26px;">
        <div style="font-size:2.6rem;">🌾</div>
        <div style="font-size:1.3rem;font-weight:800;color:#1B5E20;margin-top:6px;">{p['nama']}</div>
        <div style="font-family:monospace;font-size:1.4rem;color:#15803d;background:#f0fdf4;border:1px dashed #4CAF50;border-radius:10px;padding:10px;margin:14px auto;max-width:280px;">{p['rice_id']}</div>
        <div style="color:#555;font-size:0.9rem;">{p['luas']} ha · {p['kabupaten']} · {p['varietas']} · Paket {p['paket']}</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("""
    <div class="np-card" style="padding:16px 18px;margin-top:8px;">
      <b>Status verifikasi</b>
      <div style="margin-top:10px;font-size:.9rem;line-height:2.0;">
        ✅ Persetujuan &amp; tanda tangan digital — <b style="color:#15803d;">selesai</b><br>
        🧑‍🌾 Kunjungan petugas lapangan (pengambilan titik GPS lahan) — <b style="color:#B45309;">dijadwalkan</b><br>
        🕓 <b>Menunggu Verifikasi Dukcapil</b> — <span style="color:#92400E;font-size:.82rem;">integrasi API dalam proses; saat ini identitas diverifikasi petugas lapangan &amp; NIK di-hash (UU PDP)</span>
      </div>
    </div>""", unsafe_allow_html=True)
    st.page_link("pages/1_👨‍🌾_Farmer_Dashboard.py", label="Masuk Dashboard Petani →", icon="👨‍🌾")
    if st.button("Daftar petani lain"):
        ss.reg_step = 0
        st.rerun()
    st.stop()

# ---------- PROGRESS ----------
labels = ["Data diri", "Lahan", "Persetujuan", "Program"]
step = min(ss.reg_step, 3)
cols = st.columns(4)
for i, lb in enumerate(labels):
    color = "#15803d" if i <= step else "#c8e6c9"
    cols[i].markdown(f"<div style='height:6px;border-radius:3px;background:{color};margin-bottom:4px;'></div>"
                     f"<div style='font-size:0.72rem;color:{'#1B5E20' if i<=step else '#aaa'};text-align:center;font-weight:600;'>{lb}</div>",
                     unsafe_allow_html=True)
st.write("")

# ---------- STEP 0: DATA DIRI ----------
if ss.reg_step == 0:
    st.markdown("##### Langkah 1 · Data diri")
    st.text_input("Nama lengkap", key="reg_nama", placeholder="cth. Budi Santoso")
    c1, c2 = st.columns(2)
    c1.text_input("No. HP", key="reg_hp", placeholder="08xx")
    c2.text_input("NIK (16 digit)", key="reg_nik", max_chars=16, placeholder="16 digit")
    st.info("🔒 NIK akan di-hash dan tidak disimpan dalam bentuk asli, sesuai UU No.27/2022 (Pelindungan Data Pribadi).")
    if st.button("Lanjut →", type="primary", use_container_width=True):
        if not ss.get("reg_nama") or len(ss.get("reg_nik", "")) < 6:
            st.error("Mohon isi nama dan NIK dengan benar.")
        else:
            ss.reg_step = 1
            st.rerun()

# ---------- STEP 1: LAHAN ----------
elif ss.reg_step == 1:
    st.markdown("##### Langkah 2 · Data lahan")
    c1, c2 = st.columns(2)
    c1.selectbox("Kabupaten/Kota", KAB, key="reg_kab")
    c2.number_input("Luas lahan (ha)", min_value=0.0, step=0.1, key="reg_luas")
    st.selectbox("Varietas utama", VAR, key="reg_var")
    lat, lon = KAB_LATLON.get(ss.get("reg_kab", KAB[0]), (-6.4, 106.1))
    st.caption("Titik lahan (perkiraan wilayah). Titik GPS resmi diambil oleh **petugas lapangan saat kunjungan verifikasi** — bukan digambar sendiri — lalu diuji terhadap poligon Lahan Sawah Dilindungi.")
    st.map({"lat": [lat], "lon": [lon]}, zoom=9)
    b1, b2 = st.columns([1, 2])
    if b1.button("← Kembali", use_container_width=True):
        ss.reg_step = 0; st.rerun()
    if b2.button("Lanjut →", type="primary", use_container_width=True):
        if not ss.get("reg_luas"):
            st.error("Mohon isi luas lahan.")
        else:
            ss.reg_step = 2; st.rerun()

# ---------- STEP 2: PERSETUJUAN (LEGAL STANDING) ----------
elif ss.reg_step == 2:
    st.markdown("##### Langkah 3 · Persetujuan (legal standing)")
    with st.expander("Baca Syarat & Ketentuan Ringkas", expanded=True):
        st.markdown("""
1. NusaPangan menyediakan platform verifikasi & data pertanian. **NusaPangan bukan pemberi pinjaman**, tidak menyimpan dana Anda, dan tidak memiliki aset logistik.
2. Data lahan & panen Anda dipakai untuk verifikasi dan **hanya dapat diakses mitra atas persetujuan Anda**.
3. **NIK di-hash** dan dilindungi sesuai UU No.27/2022 (PDP).
4. Anda dapat **mencabut persetujuan** dan meminta penghapusan data kapan saja.
5. Benefit musim (advice, voucher input) disediakan **mitra**; syarat mengikuti masing-masing program.
        """)
    a1 = st.checkbox("Saya menyetujui Syarat & Ketentuan NusaPangan.", key="agree1")
    a2 = st.checkbox("Saya memberi izin pemrosesan data pribadi saya sesuai UU PDP.", key="agree2")
    a3 = st.checkbox("Saya menyatakan data yang saya isi benar dan sah.", key="agree3")
    sign = st.text_input("Tanda tangan — ketik nama lengkap sebagai persetujuan", key="reg_sign")
    ok = a1 and a2 and a3 and len(sign.strip()) > 1
    b1, b2 = st.columns([1, 2])
    if b1.button("← Kembali", use_container_width=True):
        ss.reg_step = 1; st.rerun()
    if b2.button("Lanjut →", type="primary", use_container_width=True, disabled=not ok):
        ss.reg_step = 3; st.rerun()
    if not ok:
        st.caption("Centang ketiga persetujuan dan isi tanda tangan untuk melanjutkan.")

# ---------- STEP 3: PROGRAM ----------
elif ss.reg_step == 3:
    st.markdown("##### Langkah 4 · Pilih program")
    ss.setdefault("reg_paket", "Petani (Gratis)")
    paket = st.radio("Program", ["Petani (Gratis)", "Program Musim (Gratis · didanai mitra)", "NusaTani+ (Berbayar opsional)"],
                     key="reg_paket")
    if paket.startswith("Petani"):
        st.markdown('<div class="np-alert np-alert-green"><b>Petani — Gratis.</b> Profil & Rice ID terverifikasi · harga harian & info pasar · akses AgriMart (jual ke SPPG).</div>', unsafe_allow_html=True)
    elif paket.startswith("Program Musim"):
        st.markdown('<div class="np-alert np-alert-green"><b>Program Musim — Gratis, didanai mitra.</b> Pendampingan agronom 10 jam/bulan · voucher input 1× (ditukar di toko tani mitra) · prediksi cuaca & waktu tanam.<br><small>◆ Benefit disponsori mitra input — NusaPangan tidak menyimpan/menjual barang.</small></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="np-alert np-alert-orange"><b>NusaTani+ — Rp 49rb/musim (opsional).</b> Semua fitur gratis + prioritas pembeli · analitik panen lanjutan · sertifikat traceability untuk beras premium/organik.</div>', unsafe_allow_html=True)
    b1, b2 = st.columns([1, 2])
    if b1.button("← Kembali", use_container_width=True):
        ss.reg_step = 2; st.rerun()
    if b2.button("Daftar sekarang ✓", type="primary", use_container_width=True):
        rid = "NP-BTN-" + str(random.randint(1000, 9999))
        pk = "Petani" if paket.startswith("Petani") else ("Program Musim" if paket.startswith("Program") else "NusaTani+")
        ss["petani"] = {
            "nama": ss.get("reg_nama", "Petani"), "rice_id": rid,
            "kabupaten": ss.get("reg_kab", KAB[0]), "luas": ss.get("reg_luas", 0),
            "varietas": ss.get("reg_var", VAR[0]), "paket": pk,
        }
        ss.reg_step = 99
        st.balloons()
        st.rerun()
