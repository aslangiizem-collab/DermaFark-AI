import streamlit as st
from PIL import Image
import io

st.set_page_config(page_title="DermaFark AI | Araştırma Prototipi", page_icon="🔬", layout="centered")

st.markdown("""
<style>
.block-container {max-width: 800px; padding-top: 1.8rem}
.hero {background:linear-gradient(120deg,#ede9fe,#fce7f3);padding:22px;border-radius:18px;margin-bottom:18px}
.hero h1 {color:#4338ca;margin:0;font-size:2rem}
.hero p {color:#475569;margin:8px 0 0}
.note {padding:14px;border-radius:12px;background:#eff6ff;color:#1e40af}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>🔬 DermaFark AI</h1><p>Deri Hastalıkları Görüntü Analizi · Araştırma ve Eğitim Prototipi</p></div>', unsafe_allow_html=True)
st.warning("Bu demo tıbbi tanı veya kanser taraması yapmaz. Görsel analiz sonucu üretmez; tüm örnek skorlar kurgusaldır.")

tab1, tab2, tab3 = st.tabs(["📷 Görüntü yükle", "📖 Hastalıklar", "ℹ️ Proje hakkında"])

with tab1:
    st.subheader("Deri fotoğrafı yükleyin")
    st.write("Arayüzü denemek için JPG veya PNG formatında bir görsel seçebilirsiniz. Görsel, yalnızca bu oturumda önizlenir.")
    uploaded = st.file_uploader("Görsel seçin", type=["jpg", "jpeg", "png"], accept_multiple_files=False)
    if uploaded is not None:
        if uploaded.size > 10 * 1024 * 1024:
            st.error("Dosya 10 MB'tan küçük olmalı.")
        else:
            try:
                photo = Image.open(io.BytesIO(uploaded.getvalue()))
                photo.verify()
                photo = Image.open(io.BytesIO(uploaded.getvalue())).convert("RGB")
                st.image(photo, caption="Yüklenen görüntü", use_container_width=True)
                if st.button("✨ Demo ekranını göster", type="primary", use_container_width=True):
                    st.session_state["demo"] = True
            except Exception:
                st.error("Görsel okunamadı. Başka bir dosya deneyin.")
    else:
        st.session_state["demo"] = False

    if uploaded is not None and st.session_state.get("demo"):
        st.subheader("Örnek sonuç ekranı")
        st.info("Aşağıdaki değerler yalnızca tasarım demosudur; yüklediğiniz görüntüden hesaplanmamıştır.")
        for name, value in [("Mikozis Fungoides", 0.52), ("Egzama", 0.31), ("Sedef", 0.17)]:
            st.write(f"**{name}** — temsili skor: %{value*100:.0f}")
            st.progress(value)
        st.error("Bu skorlar tanı veya gerçek hastalık olasılığı değildir. Şüpheli ya da devam eden deri bulguları için dermatoloji uzmanına başvurun.")
        st.download_button(
            "📄 Demo raporunu indir (TXT)",
            data=("DermaFark AI — DEMO\nBu belge gerçek analiz içermez.\n"
                  "Temsili skorlar: MF %52, Egzama %31, Sedef %17.\n"
                  "Tıbbi karar vermek için kullanmayın.\n"),
            file_name="dermafark_demo_raporu.txt",
            mime="text/plain",
            use_container_width=True
        )

with tab2:
    st.markdown("**Mikozis Fungoides (MF):** Deride lekeler veya plaklarla başlayabilen bir kutanöz T hücreli lenfoma türüdür.")
    st.markdown("**Egzama:** Kaşıntı, kuruluk ve kızarıklıkla seyreden çeşitli iltihaplı deri durumlarını kapsar.")
    st.markdown("**Sedef (Psoriasis):** Genellikle pullu, belirgin sınırlı plaklara yol açabilen kronik iltihaplı deri hastalığıdır.")
    st.info("Bu hastalıklar görsel olarak birbirine benzeyebilir. MF tanısı klinik değerlendirme ve gerektiğinde biyopsi gerektirir.")

with tab3:
    st.write("**Amaç:** Üç deri hastalığına yönelik bir görüntü sınıflandırma araştırmasının kullanıcı arayüzünü göstermek.")
    st.write("**Teknoloji:** Python + Streamlit. Gelecekte doğrulanmış veri setiyle eğitilmiş bir model bağlanabilir.")
    st.write("**Sınır:** Bu sürümde yapay zekâ modeli bulunmuyor; hiçbir görüntüden tıbbi tahmin yapılmıyor.")
    st.write("**Gizlilik:** Hassas hasta fotoğraflarını bu demo gibi kamuya açık servislere yüklemeyin. Gerçek veriler için izin, güvenlik ve uygun barındırma gerekir.")
