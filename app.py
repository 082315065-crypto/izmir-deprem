import streamlit as st
import math

st.title("🏗️ İzmir Deprem Erken Uyarı Sistemi")
st.write("Akkar & Çağnan (2010) Algoritması")

mag = st.sidebar.slider("Deprem Büyüklüğü (Mw)", 4.0, 8.0, 6.6)
dist = st.sidebar.number_input("Uzaklık (km)", value=15)

def hesapla_pga(M, R):
    A1, A2, A3, A7, C1 = 8.92418, -0.513, -0.695, 7.33617, 6.5
    G_SABITI = 9810.0 
    ln_y = A1 + (A2 * (M - C1)) + (A3 * math.log(math.sqrt(R**2 + A7**2)))
    return round(math.exp(ln_y) / G_SABITI, 4)

pga = hesapla_pga(mag, dist)
st.metric("Tahmini Sarsıntı (PGA)", f"{pga} g")

if pga >= 0.25:
    st.error("🚨 KRİTİK: Vanalar Kapatıldı!")
elif pga >= 0.15:
    st.warning("⚠️ UYARI: Metro Durduruldu!")
else:
    st.success("📱 BİLGİ: SMS Gönderildi.")
import streamlit as st
import math
import pandas as pd

# Sayfa ayarları
st.set_page_config(page_title="İzmir Deprem Uyarı", page_icon="🏗️", layout="wide")

st.title("🏗️ İzmir Deprem Erken Uyarı Sistemi")
st.markdown("---")

# Yan Menü (Inputlar)
st.sidebar.header("🎛️ Parametreler")
mag = st.sidebar.slider("Deprem Büyüklüğü (Mw)", 4.0, 8.0, 6.6, step=0.1)
dist = st.sidebar.number_input("Uzaklık (km)", value=15, min_value=1)

# Hesaplama Fonksiyonu
def hesapla_pga(M, R):
    A1, A2, A3, A7, C1 = 8.92418, -0.513, -0.695, 7.33617, 6.5
    G_SABITI = 9810.0 
    ln_y = A1 + (A2 * (M - C1)) + (A3 * math.log(math.sqrt(R**2 + A7**2)))
    return round(math.exp(ln_y) / G_SABITI, 4)

pga = hesapla_pga(mag, dist)

# Üst Bilgi Kartları
col1, col2 = st.columns(2)
with col1:
    st.metric("Tahmini Sarsıntı (PGA)", f"{pga} g")
with col2:
    if pga >= 0.25:
        st.error("🚨 DURUM: KRİTİK! Vanalar Kapatıldı.")
    elif pga >= 0.15:
        st.warning("⚠️ DURUM: UYARI! Metro Durduruldu.")
    else:
        st.success("📱 DURUM: GÜVENLİ. SMS Gönderildi.")

st.markdown("---")

# GRAFİK BÖLÜMÜ
st.subheader("📈 Mesafeye Göre Sarsıntı Analizi")
st.write(f"{mag} büyüklüğündeki bir depremin mesafeye göre sönümlenme grafiği:")

# Grafik verisi oluşturma
dist_list = list(range(1, 101))
pga_list = [hesapla_pga(mag, d) for d in dist_list]
chart_data = pd.DataFrame({
    'Mesafe (km)': dist_list,
    'Sarsıntı (g)': pga_list
})

st.line_chart(chart_data.set_index('Mesafe (km)'))

st.info("💡 Not: Uzaklık arttıkça sarsıntı şiddetinin (g) nasıl azaldığını grafikten inceleyebilirsiniz.")