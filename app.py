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
