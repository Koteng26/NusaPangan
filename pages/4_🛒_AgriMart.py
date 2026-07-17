"""
🛒 AgriMart — Marketplace Farm-to-Consumer
Petani jual langsung ke SPPG/konsumen — memangkas rantai distribusi
"""
import streamlit as st
import os, sys; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from utils import load_data, COMMON_CSS
import pandas as pd

st.set_page_config(page_title="AgriMart", page_icon="🛒", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif; }
    .mart-header {
        background: linear-gradient(135deg, #E65100, #F57C00, #FF9800);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 1.5rem;
    }
    .product-card {
        background: white;
        border: 1px solid #E8F5E9;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        height: 100%;
    }
    .product-card:hover {
        border-color: #43A047;
        box-shadow: 0 4px 16px rgba(67,160,71,0.15);
    }
    .price-tag {
        background: #E8F5E9;
        color: #1B5E20;
        font-size: 1.3rem;
        font-weight: 800;
        padding: 0.3rem 0.8rem;
        border-radius: 8px;
        display: inline-block;
    }
    .old-price {
        text-decoration: line-through;
        color: #999;
        font-size: 0.85rem;
    }
    .savings-badge {
        background: #FFF3E0;
        color: #E65100;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 0.2rem 0.5rem;
        border-radius: 12px;
    }
    .verified-seller {
        background: #E8F5E9;
        color: #1B5E20;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 0.15rem 0.5rem;
        border-radius: 10px;
    }
    .escrow-step {
        text-align: center;
        padding: 0.8rem;
    }
    .escrow-icon { font-size: 2rem; }
    .escrow-label { font-size: 0.8rem; color: #555; margin-top: 0.3rem; }
    .escrow-active { background: #E8F5E9; border-radius: 12px; }
    .order-card {
        background: white;
        border: 1px solid #eee;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

df_farmers = load_data("farmers.csv")

st.markdown("""
<div class="mart-header">
    <h2 style="margin:0;">🛒 AgriMart — Farm to Consumer</h2>
    <p style="margin:0.3rem 0 0 0; opacity:0.8;">Petani jual langsung ke sekolah MBG — tanpa perantara, harga lebih adil.</p>
</div>
""", unsafe_allow_html=True)

ss = st.session_state
ss.setdefault("my_listings", [])
if ss.get("petani"):
    _p = ss["petani"]
    st.markdown(f'<div style="background:#E8F5E9;border-left:4px solid #43A047;border-radius:12px;padding:0.9rem 1.1rem;margin-bottom:1rem;font-size:0.9rem;">👋 Halo <b>{_p["nama"]}</b> · <span style="font-family:monospace;">{_p["rice_id"]}</span> — {_p["luas"]} ha {_p["varietas"]} di {_p["kabupaten"]}. Terbitkan lapak hasil panen Anda di tab <b>Browse Produk</b>.</div>', unsafe_allow_html=True)
else:
    st.info("Belum mendaftar? Buka menu **📝 Pendaftaran** untuk membuat Rice ID dan menjual hasil panen Anda di sini.")

# Metrics
st.markdown(f"""
<div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:20px;">
    <div style="flex:1;min-width:140px;background:linear-gradient(135deg,#E65100,#FF8F00);border-radius:14px;padding:18px;color:#fff;box-shadow:0 4px 16px rgba(230,81,0,0.2);">
        <div style="font-size:0.75rem;opacity:0.8;">🌾 Produk Aktif</div>
        <div style="font-size:1.8rem;font-weight:900;margin-top:4px;">48</div>
        <div style="font-size:0.7rem;opacity:0.7;">listing tersedia</div>
    </div>
    <div style="flex:1;min-width:140px;background:linear-gradient(135deg,#1B5E20,#2E7D32);border-radius:14px;padding:18px;color:#fff;box-shadow:0 4px 16px rgba(27,94,32,0.2);">
        <div style="font-size:0.75rem;opacity:0.8;">👨‍🌾 Petani Seller</div>
        <div style="font-size:1.8rem;font-weight:900;margin-top:4px;">125</div>
        <div style="font-size:0.7rem;opacity:0.7;">verified Dukcapil</div>
    </div>
    <div style="flex:1;min-width:140px;background:linear-gradient(135deg,#0D47A1,#1565C0);border-radius:14px;padding:18px;color:#fff;box-shadow:0 4px 16px rgba(13,71,161,0.2);">
        <div style="font-size:0.75rem;opacity:0.8;">🏫 Buyer Institusi</div>
        <div style="font-size:1.8rem;font-weight:900;margin-top:4px;">12</div>
        <div style="font-size:0.7rem;opacity:0.7;">SPPG terhubung</div>
    </div>
    <div style="flex:1;min-width:140px;background:linear-gradient(135deg,#880E4F,#AD1457);border-radius:14px;padding:18px;color:#fff;box-shadow:0 4px 16px rgba(136,14,79,0.2);">
        <div style="font-size:0.75rem;opacity:0.8;">💰 Hemat vs Pasar</div>
        <div style="font-size:1.8rem;font-weight:900;margin-top:4px;">~18%</div>
        <div style="font-size:0.7rem;opacity:0.7;">rata-rata penghematan</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Tab system
tab_browse, tab_order, tab_escrow = st.tabs(["🛍️ Browse Produk", "📋 Simulasi Order", "🔐 Escrow & Pembayaran"])

with tab_browse:
    st.markdown("### 🌾 Produk Tersedia dari Petani Terverifikasi")

    if ss.get("petani"):
        _p = ss["petani"]
        with st.expander("🌾 Terbitkan lapak Anda (jual hasil panen)", expanded=not ss["my_listings"]):
            with st.form("jual_form", clear_on_submit=True):
                cca, ccb = st.columns(2)
                _harga = cca.number_input("Harga jual (Rp/kg)", min_value=5000, max_value=20000, value=11000, step=100)
                _stok = ccb.number_input("Stok (kg)", min_value=50, max_value=50000, value=500, step=50)
                if st.form_submit_button("Terbitkan lapak ✓", type="primary", use_container_width=True):
                    ss["my_listings"].insert(0, {
                        "nama_produk": f"Beras {_p['varietas']} — panen {_p['nama']}",
                        "petani": _p["nama"], "rice_id": _p["rice_id"], "kab": _p["kabupaten"],
                        "harga": int(_harga), "stok": int(_stok),
                    })
                    st.success("Lapak Anda terbit dan tampil paling atas!")
        if ss["my_listings"]:
            st.markdown("#### 🌟 Lapak Anda")
            _mc = st.columns(3)
            for _i, _l in enumerate(ss["my_listings"][:3]):
                with _mc[_i % 3]:
                    st.markdown(f'<div class="product-card" style="border:2px solid #43A047;"><div style="display:flex;justify-content:space-between;"><span style="font-size:0.75rem;color:#888;">🌾 {_l["kab"]}</span><span class="verified-seller">✅ Lapak Anda</span></div><h4 style="margin:0.3rem 0;font-size:1rem;">{_l["nama_produk"]}</h4><p style="font-size:0.8rem;color:#666;margin:0.2rem 0;">👨‍🌾 {_l["petani"]} · {_l["rice_id"]}</p><div style="margin:0.5rem 0;"><span class="price-tag">Rp {_l["harga"]:,}/kg</span></div><p style="font-size:0.75rem;color:#888;">Stok: {_l["stok"]:,} kg</p></div>', unsafe_allow_html=True)
            st.markdown("---")
    
    # Filter
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        kat_filter = st.selectbox("Kategori", ["Semua", "Beras", "Gabah", "Benih"])
    with col_f2:
        kab_filter = st.selectbox("Asal Kabupaten", ["Semua"] + list(df_farmers["kabupaten"].unique()))
    with col_f3:
        sort_by = st.selectbox("Urutkan", ["Harga Terendah", "Rating Tertinggi", "Stok Terbanyak"])
    
    st.markdown("")
    
    # Product listings - simulated from farmer data
    products = []
    for _, f in df_farmers.head(30).iterrows():
        beras_kg = int(f["estimasi_produksi_ton"] * 1000 * 0.63)
        harga_f2c = int(f["harga_beras_pasar_kg"] * 0.82)  # 18% cheaper
        products.append({
            "nama_produk": f"Beras {f['varietas']} Premium",
            "petani": f["nama"],
            "farmer_id": f["farmer_id"],
            "desa": f["desa"],
            "kab": f["kabupaten"],
            "stok_kg": beras_kg,
            "harga_f2c": harga_f2c,
            "harga_pasar": f["harga_beras_pasar_kg"],
            "rating": round(4.2 + (f["credit_score"] - 550) / 1000, 1),
            "terjual": int(beras_kg * 0.3),
        })
    
    df_products = pd.DataFrame(products)
    if kab_filter != "Semua":
        df_products = df_products[df_products["kab"] == kab_filter]
    
    # Display as cards
    rows = [df_products.iloc[i:i+3] for i in range(0, min(12, len(df_products)), 3)]
    for row_data in rows:
        cols = st.columns(3)
        for idx, (_, prod) in enumerate(row_data.iterrows()):
            with cols[idx]:
                savings_pct = int((1 - prod["harga_f2c"] / prod["harga_pasar"]) * 100)
                st.markdown(f"""
                <div class="product-card">
                    <div style="display:flex;justify-content:space-between;align-items:start;margin-bottom:0.5rem;">
                        <span style="font-size:0.75rem;color:#888;">🌾 {prod['kab']}</span>
                        <span class="verified-seller">✅ Verified</span>
                    </div>
                    <h4 style="margin:0.3rem 0;font-size:1rem;">{prod['nama_produk']}</h4>
                    <p style="font-size:0.8rem;color:#666;margin:0.2rem 0;">
                        👨‍🌾 {prod['petani']} — Desa {prod['desa']}<br>
                        ⭐ {prod['rating']} · {prod['terjual']} kg terjual
                    </p>
                    <div style="margin:0.5rem 0;">
                        <span class="price-tag">Rp {prod['harga_f2c']:,}/kg</span>
                        <span class="old-price">Rp {int(prod['harga_pasar']):,}</span>
                        <span class="savings-badge">Hemat {savings_pct}%</span>
                    </div>
                    <p style="font-size:0.75rem;color:#888;margin:0.3rem 0;">Stok: {prod['stok_kg']:,} kg tersedia</p>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("")

with tab_order:
    st.markdown("### 📋 Simulasi Order — SPPG Membeli Beras dari Petani")
    
    st.markdown("""
    > **Skenario:** SPPG Surabaya Utara membutuhkan 500 kg beras premium untuk menu MBG minggu depan.
    > Sistem AgriMart otomatis mencarikan petani terdekat dengan stok tersedia dan harga terbaik.
    """)
    
    st.markdown("---")
    
    # Order form
    col_order1, col_order2 = st.columns(2)
    
    with col_order1:
        st.markdown("##### 🏫 Detail Pembeli")
        buyer = st.selectbox("Institusi Pembeli", [
            "SPPG Surabaya Utara — SMPN 3 Surabaya",
            "SPPG Bandung Tengah — SDN 1 Bandung", 
            "SPPG Jakarta Selatan — SMPN 7 Jakarta",
        ])
        komoditas = st.selectbox("Komoditas", ["Beras Premium", "Beras Medium"])
        jumlah = st.number_input("Jumlah (kg)", min_value=50, max_value=5000, value=500, step=50)
        tgl_kirim = st.date_input("Tanggal Kirim Dibutuhkan")
    
    with col_order2:
        st.markdown("##### 🤖 Rekomendasi AgriMart AI")
        
        # Matching
        matched = df_products.head(3)
        if len(matched) == 0:
            st.warning("Belum ada produk tersedia untuk filter ini")
        else:
            total_cost_f2c = jumlah * matched.iloc[0]["harga_f2c"]
            total_cost_pasar = jumlah * matched.iloc[0]["harga_pasar"]
            savings = total_cost_pasar - total_cost_f2c
            
            st.success(f"""
            **✅ Match ditemukan!** {len(matched)} petani terverifikasi
            
            **Total biaya F2C:** Rp {total_cost_f2c:,.0f}  
            **Harga pasar normal:** Rp {total_cost_pasar:,.0f}  
            **💰 Penghematan:** Rp {savings:,.0f} ({int(savings/max(total_cost_pasar,1)*100)}%)
            """)
        
        for i, (_, m) in enumerate(matched.iterrows()):
            alloc = [250, 150, 100][i] if i < 3 else 0
            st.markdown(f"""
            **Petani {i+1}:** {m['petani']} ({m['farmer_id']})  
            Desa {m['desa']}, {m['kab']} — Alokasi: {alloc} kg @ Rp {m['harga_f2c']:,}/kg  
            ⭐ {m['rating']} · ✅ Dukcapil Verified · Credit Score {int(m['rating']*165)}
            """)
    
    if st.button("🛒 Buat Order", type="primary", use_container_width=True):
        st.balloons()
        st.success("✅ Order #ORD-2026-0847 berhasil dibuat! Petani akan menerima notifikasi WhatsApp dalam 30 detik.")

with tab_escrow:
    st.markdown("### 🔐 Sistem Escrow — Pembayaran Aman & Transparan")
    
    st.markdown("""
    AgriMart menggunakan **sistem escrow** untuk melindungi kedua pihak.
    Dana ditahan di rekening escrow sampai barang diterima dan diverifikasi.
    """)
    
    st.markdown("---")
    
    # Escrow flow visualization
    st.markdown("##### 🔄 Alur Escrow AgriMart")
    
    e1, e2, e3, e4, e5 = st.columns(5)
    
    with e1:
        st.markdown("""
        <div class="escrow-step escrow-active">
            <div class="escrow-icon">🏫</div>
            <div style="font-weight:700;font-size:0.85rem;color:#1B5E20;">1. Order</div>
            <div class="escrow-label">SPPG buat pesanan 500 kg beras</div>
        </div>
        """, unsafe_allow_html=True)
    with e2:
        st.markdown("""
        <div class="escrow-step escrow-active">
            <div class="escrow-icon">💰</div>
            <div style="font-weight:700;font-size:0.85rem;color:#1B5E20;">2. Escrow</div>
            <div class="escrow-label">Dana Rp 5,7jt ditahan di escrow</div>
        </div>
        """, unsafe_allow_html=True)
    with e3:
        st.markdown("""
        <div class="escrow-step escrow-active">
            <div class="escrow-icon">🚛</div>
            <div style="font-weight:700;font-size:0.85rem;color:#E65100;">3. Kirim</div>
            <div class="escrow-label">Petani kirim, GPS & IoT terlacak</div>
        </div>
        """, unsafe_allow_html=True)
    with e4:
        st.markdown("""
        <div class="escrow-step">
            <div class="escrow-icon">✅</div>
            <div style="font-weight:700;font-size:0.85rem;color:#888;">4. Terima</div>
            <div class="escrow-label">SPPG konfirmasi kualitas OK</div>
        </div>
        """, unsafe_allow_html=True)
    with e5:
        st.markdown("""
        <div class="escrow-step">
            <div class="escrow-icon">💸</div>
            <div style="font-weight:700;font-size:0.85rem;color:#888;">5. Bayar</div>
            <div class="escrow-label">Dana cair ke e-wallet petani</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Active orders
    st.markdown("##### 📦 Order Aktif")
    
    orders = pd.DataFrame([
        {"Order ID": "ORD-2026-0845", "Pembeli": "SPPG Surabaya Utara", "Petani": "Budi Santoso", "Komoditas": "Beras Ciherang", "Jumlah": "500 kg", "Total": "Rp 5.740.000", "Status": "🚛 Dalam Pengiriman", "Escrow": "💰 Ditahan"},
        {"Order ID": "ORD-2026-0843", "Pembeli": "SPPG Bandung Tengah", "Petani": "Hasan Hidayat", "Komoditas": "Beras IR64", "Jumlah": "300 kg", "Total": "Rp 3.420.000", "Status": "✅ Diterima", "Escrow": "💸 Dicairkan"},
        {"Order ID": "ORD-2026-0841", "Pembeli": "SPPG Jakarta Selatan", "Petani": "Dedi Supriatna", "Komoditas": "Beras Inpari 32", "Jumlah": "750 kg", "Total": "Rp 8.625.000", "Status": "✅ Diterima", "Escrow": "💸 Dicairkan"},
        {"Order ID": "ORD-2026-0839", "Pembeli": "SPPG Semarang Barat", "Petani": "Ahmad Mulyadi", "Komoditas": "Beras Ciherang", "Jumlah": "200 kg", "Total": "Rp 2.280.000", "Status": "📦 Disiapkan", "Escrow": "💰 Ditahan"},
    ])
    st.dataframe(orders, use_container_width=True, hide_index=True)
    
    # Impact summary
    st.markdown("---")
    st.markdown("##### 📊 Dampak AgriMart")
    
    st.markdown("""
    <div style="display:flex;gap:12px;flex-wrap:wrap;">
        <div style="flex:1;min-width:130px;background:linear-gradient(135deg,#1B5E20,#388E3C);border-radius:12px;padding:14px;color:#fff;text-align:center;">
            <div style="font-size:0.7rem;opacity:0.8;">Total Transaksi</div>
            <div style="font-size:1.4rem;font-weight:900;">Rp 847 jt</div>
            <div style="font-size:0.65rem;opacity:0.7;">+23% bulan ini</div>
        </div>
        <div style="flex:1;min-width:130px;background:linear-gradient(135deg,#0D47A1,#1976D2);border-radius:12px;padding:14px;color:#fff;text-align:center;">
            <div style="font-size:0.7rem;opacity:0.8;">Avg Savings</div>
            <div style="font-size:1.4rem;font-weight:900;">18%</div>
            <div style="font-size:0.65rem;opacity:0.7;">konsumen hemat</div>
        </div>
        <div style="flex:1;min-width:130px;background:linear-gradient(135deg,#E65100,#F57C00);border-radius:12px;padding:14px;color:#fff;text-align:center;">
            <div style="font-size:0.7rem;opacity:0.8;">Income Petani</div>
            <div style="font-size:1.4rem;font-weight:900;">+32%</div>
            <div style="font-size:0.65rem;opacity:0.7;">vs jual ke tengkulak</div>
        </div>
        <div style="flex:1;min-width:130px;background:linear-gradient(135deg,#4A148C,#7B1FA2);border-radius:12px;padding:14px;color:#fff;text-align:center;">
            <div style="font-size:0.7rem;opacity:0.8;">Rantai Distribusi</div>
            <div style="font-size:1.4rem;font-weight:900;">Dipangkas</div>
            <div style="font-size:0.65rem;opacity:0.7;">petani → SPPG</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
