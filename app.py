import io
from datetime import datetime
from html import escape

import streamlit as st
from PIL import Image, ImageOps, UnidentifiedImageError

st.set_page_config(
    page_title="DermaFark AI | Araştırma Prototipi",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"], [data-testid="stApp"] {font-family:'DM Sans',sans-serif;}
[data-testid="stAppViewContainer"] {background:linear-gradient(180deg,#f6f7ff 0%,#fff 43%,#f9fbff 100%);}
.block-container {max-width:840px;padding-top:1.2rem;padding-bottom:5rem;}
#MainMenu,footer {visibility:hidden;}
h1,h2,h3 {letter-spacing:-.035em;color:#1d2445;}
.hero {background:linear-gradient(115deg,#6258d9,#8875e6 60%,#ad8fe7);color:white;
 border-radius:26px;padding:28px 26px;box-shadow:0 16px 34px #6a63b12c;margin-bottom:18px;}
.hero .tag {display:inline-block;background:#ffffff28;border:1px solid #ffffff44;border-radius:30px;
 font-size:12px;padding:6px 12px;margin-bottom:14px;}
.hero h1 {color:white;font-size:clamp(30px,5vw,43px);margin:0 0 8px;}
.hero p {color:#f7f3ff;font-size:15px;margin:0;line-height:1.7;}
.tile {background:#fff;border:1px solid #e9eafa;border-radius:18px;padding:18px;margin:8px 0;
 box-shadow:0 5px 18px #23295b09;}
.tile h3 {font-size:19px;margin:0 0 8px;}
.tile p {color:#66708c;font-size:14px;margin:0;}
.step {display:inline-block;border-radius:40px;background:#efedff;color:#554cc1;padding:6px 12px;
 font-weight:800;font-size:12px;margin:5px 0 12px;}
.info {background:#f1f5ff;border-left:4px solid #7565db;border-radius:12px;padding:13px 16px;
 color:#39476b;margin:14px 0;font-size:14px;}
.warning {background:#fff6ed;border:1px solid #ffdfc2;border-radius:13px;padding:14px;
 color:#85552a;margin:14px 0;font-size:14px;}
.mock {background:#f7f3ff;border:1px dashed #9c8bdf;border-radius:14px;padding:14px;
 color:#54479c;font-size:14px;margin:12px 0;}
.pill {display:inline-block;padding:6px 10px;background:#e8f7f2;color:#25765c;
 border-radius:30px;font-size:12px;font-weight:700;}
[data-testid="stButton"] button[kind="primary"] {background:#6658d7;border:0;border-radius:13px;
 padding:.75rem 1rem;font-weight:700;}
[data-testid="stButton"] button {border-radius:13px;font-weight:650;}
[data-testid="stTabs"] button {font-weight:700;}
[data-testid="stFileUploader"] {background:white;border-radius:16px;}
[data-testid="stMetric"] {background:#fff;border:1px solid #e9eafa;padding:15px;border-radius:15px;}
@media(max-width:640px){.block-container{padding:1rem .9rem 4rem;}
.hero{padding:22px 19px;border-radius:20px;}.hero h1{font-size:30px;}}
</style>
""", unsafe_allow_html=True)

STEPS = ["🏠 Ana sayfa", "📸 Fotoğraf", "🧠 Analiz", "📝 Belirti anketi",
         "📊 Sonuç", "📚 Hastalıklar", "🏥 Yönlendirme", "ℹ️ Proje"]
if "page" not in st.session_state:
    st.session_state.page = STEPS[0]
if "image_bytes" not in st.session_state:
    st.session_state.image_bytes = None
if "demo_requested" not in st.session_state:
    st.session_state.demo_requested = False

def navigate(page):
    st.session_state.page = page
    st.rerun()

def section(title, subtitle=None):
    st.markdown(f"## {title}")
    if subtitle:
        st.caption(subtitle)

def tile(title, description, icon="✨"):
    st.markdown(
        f'<div class="tile"><h3>{icon} {escape(title)}</h3><p>{escape(description)}</p></div>',
        unsafe_allow_html=True
    )

def load_photo(source):
    if source is None:
        return
    if len(source.getvalue()) > 8 * 1024 * 1024:
        st.error("En fazla 8 MB boyutunda fotoğraf yükleyin.")
        return
    try:
        data = source.getvalue()
        image = Image.open(io.BytesIO(data))
        image.verify()
        image = Image.open(io.BytesIO(data))
        image = ImageOps.exif_transpose(image).convert("RGB")
        if image.width * image.height > 24_000_000:
            st.error("Fotoğraf çözünürlüğü çok yüksek. Daha küçük bir fotoğraf seçin.")
            return
        st.session_state.image_bytes = data
        st.session_state.demo_requested = False
    except (UnidentifiedImageError, OSError, ValueError):
        st.error("Fotoğraf okunamadı. JPG veya PNG deneyin.")

def show_image():
    if st.session_state.image_bytes:
        image = Image.open(io.BytesIO(st.session_state.image_bytes))
        image = ImageOps.exif_transpose(image).convert("RGB")
        st.image(image, caption="Bu oturumda seçilen fotoğraf", use_container_width=True)
        return True
    return False

st.markdown(
    '<div class="hero"><div class="tag">🔬 TÜBİTAK 2204-B • Araştırma prototipi</div>'
    '<h1>DermaFark AI</h1>'
    '<p>Deri bulgularını anlamaya yönelik eğitim ve araştırma arayüzü.<br>'
    'Fotoğraf • Belirti soruları • Bilgilendirme • Uzman yönlendirmesi</p></div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="warning"><strong>⚠️ Tıbbi uyarı:</strong> Bu uygulama tanı koymaz, '
    'kanser taraması yapmaz ve bir hastalığı dışlayamaz. Şu anda yapay zekâ modeli bağlı değildir. '
    'Analiz ekranındaki gösterimler örnektir. Gerçek hasta fotoğrafı yüklemeyin.</div>',
    unsafe_allow_html=True
)
page = st.selectbox("📍 Bölüm seç", STEPS, index=STEPS.index(st.session_state.page))
if page != st.session_state.page:
    st.session_state.page = page
    st.rerun()

if page == STEPS[0]:
    section("Uygulamaya hoş geldiniz", "Araştırma akışını adım adım deneyin.")
    tile("1. Fotoğraf ekleyin", "Kamerayla fotoğraf çekin veya galeriden örnek görsel yükleyin.", "📸")
    tile("2. Analiz arayüzünü görün", "Henüz model bulunmadığından sadece tasarım demosunu inceleyin.", "🧠")
    tile("3. Belirti sorularını yanıtlayın", "Soruların kullanıcı deneyimini nasıl desteklediğini görün.", "📝")
    tile("4. Bilgi ve yönlendirme", "Hastalıkları tanıyın, dermatoloji başvuru yollarını görün.", "🏥")
    if st.button("Başlayalım →", type="primary", use_container_width=True):
        navigate(STEPS[1])

elif page == STEPS[1]:
    section("Fotoğraf ekle", "Yalnızca izinli, kişisel veri içermeyen eğitim görselleri kullanın.")
    st.markdown('<span class="step">ADIM 1 / 4</span>', unsafe_allow_html=True)
    method = st.radio("Fotoğraf kaynağı", ["📁 Galeriden / bilgisayardan yükle", "📷 Kamerayla çek"], horizontal=False)
    source = (st.file_uploader("JPG veya PNG seç", type=["jpg", "jpeg", "png"], key="upload")
              if method.startswith("📁") else st.camera_input("Kamerayı aç", key="camera"))
    if source is not None:
        # Only reprocess when the selected bytes have changed.
        if st.session_state.get("last_source") != (source.name, len(source.getvalue()), hash(source.getvalue())):
            load_photo(source)
            st.session_state.last_source = (source.name, len(source.getvalue()), hash(source.getvalue()))
    if show_image():
        st.success("Fotoğraf önizlemesi hazır.")
        if st.button("Analiz ekranına geç →", type="primary", use_container_width=True):
            navigate(STEPS[2])
        if st.button("Fotoğrafı oturumdan kaldır", use_container_width=True):
            st.session_state.image_bytes = None
            st.session_state.last_source = None
            st.rerun()
    else:
        st.info("Devam etmek için örnek bir görsel seçin veya kamerayı kullanın.")

elif page == STEPS[2]:
    section("Yapay zekâ analiz ekranı", "Görüntü sınıflandırma modelinin bağlanacağı bölüm.")
    st.markdown('<span class="step">ADIM 2 / 4</span>', unsafe_allow_html=True)
    if not show_image():
        st.info("Önce fotoğraf eklemeniz gerekiyor.")
        if st.button("← Fotoğraf ekle"):
            navigate(STEPS[1])
    else:
        st.markdown('<div class="mock"><strong>🧪 DEMO MODU</strong><br>'
                    'Bu sürüm fotoğrafı analiz etmez. Aşağıdaki ilerleme adımları '
                    'gelecekte geliştirilecek modelin arayüz taslağıdır.</div>',
                    unsafe_allow_html=True)
        st.progress(100, text="Arayüz demosu hazır • Yapay zekâ tahmini üretilmedi")
        st.write("**Gelecekteki araştırma modelinde karşılaştırılması planlanan sınıflar:**")
        st.write("Mikozis Fungoides · Egzama · Sedef · Tinea corporis · Pityriasis rosea")
        st.caption("Bu hastalıkların görsel benzerliği nedeniyle yalnızca fotoğrafa bakılarak tanı konulamaz.")
        if st.button("Belirti sorularına geç →", type="primary", use_container_width=True):
            navigate(STEPS[3])

elif page == STEPS[3]:
    section("Belirti anketi", "Bu sorular yalnızca eğitim demosu içindir; tanı üretmez.")
    st.markdown('<span class="step">ADIM 3 / 4</span>', unsafe_allow_html=True)
    with st.form("symptom_form"):
        duration = st.selectbox("Cilt bulgusu ne kadar süredir var?",
                                ["Seçiniz", "Birkaç gün", "1–4 hafta", "1–6 ay", "6 aydan uzun", "Bilmiyorum"])
        itch = st.radio("Kaşıntı var mı?", ["Seçiniz", "Yok", "Hafif", "Orta", "Şiddetli"])
        spread = st.radio("Görünüm zamanla değişti veya yayıldı mı?",
                          ["Seçiniz", "Evet", "Hayır", "Emin değilim"])
        location = st.selectbox("Hangi bölgede?", ["Seçiniz", "Gövde", "Kol", "Bacak", "Yüz / boyun", "Birden fazla bölge", "Diğer"])
        treatment = st.radio("Daha önce tedavi denendi mi?", ["Seçiniz", "Evet", "Hayır"])
        redflag = st.checkbox("Ateş, hızla kötüleşme veya ciddi ağrı gibi ek belirtiler var")
        consent = st.checkbox("Bu formun eğitim amaçlı olduğunu ve tanı sağlamadığını anladım.")
        submitted = st.form_submit_button("Yanıtları kaydet ve devam et →", type="primary", use_container_width=True)
    if submitted:
        if "Seçiniz" in [duration, itch, spread, location, treatment] or not consent:
            st.error("Lütfen soruları yanıtlayın ve bilgilendirme kutusunu işaretleyin.")
        else:
            st.session_state.answers = {
                "Süre": duration, "Kaşıntı": itch, "Değişim/yayılma": spread,
                "Bölge": location, "Önceki tedavi": treatment,
                "Ek uyarı belirtileri": "Evet" if redflag else "Hayır"
            }
            navigate(STEPS[4])

elif page == STEPS[4]:
    section("Sonuç ekranı", "Örnek ekran • Gerçek görüntü analizi değildir.")
    st.markdown('<span class="step">ADIM 4 / 4</span>', unsafe_allow_html=True)
    st.markdown('<div class="mock"><strong>Model sonucu: ÜRETİLMEDİ</strong><br>'
                'Eğitilmiş ve doğrulanmış bir model henüz uygulamaya bağlanmadı. '
                'Bu nedenle hastalık skorları veya olasılıkları gösterilmiyor.</div>',
                unsafe_allow_html=True)
    if "answers" in st.session_state:
        st.subheader("Anket yanıtları")
        for key, value in st.session_state.answers.items():
            st.write(f"**{key}:** {value}")
        if st.session_state.answers["Ek uyarı belirtileri"] == "Evet":
            st.error("Ateş, hızla kötüleşme veya ciddi ağrı gibi belirtilerde gecikmeden tıbbi değerlendirme alın.")
    else:
        st.info("Anket henüz doldurulmadı.")
    st.markdown('<div class="info"><strong>Uzman değerlendirmesi önemlidir.</strong><br>'
                'Devam eden, değişen veya açıklanamayan deri bulguları için dermatoloji uzmanına başvurun. '
                'Mikozis Fungoides tanısı gerektiğinde biyopsi ve klinik değerlendirme gerektirir.</div>',
                unsafe_allow_html=True)
    report = "DERMAFARK AI - EĞİTİM DEMOSU\nTıbbi tanı veya görüntü analizi içermez.\n"
    report += f"Oluşturulma: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
    for key, value in st.session_state.get("answers", {}).items():
        report += f"{key}: {value}\n"
    report += "\nBu rapor tıbbi karar için kullanılamaz. Dermatoloji uzmanına danışın.\n"
    st.download_button("📄 Demo özetini indir (TXT)", report, "dermafark_demo_ozet.txt",
                       mime="text/plain", use_container_width=True)
    if st.button("Uzman yönlendirmesine geç →", type="primary", use_container_width=True):
        navigate(STEPS[6])

elif page == STEPS[5]:
    section("Hastalıklar hakkında", "Görsel benzerlikler nedeniyle kesin tanı için uzman değerlendirmesi gerekir.")
    info = {
        "Mikozis Fungoides (MF)": ("Kutanöz T hücreli lenfoma türüdür. Erken dönemde egzama veya sedefe benzeyen lekeler/plaklar görülebilir.",
                                 "Tanı dermatoloji değerlendirmesi ve gerektiğinde biyopsiyle konur."),
        "Egzama": ("Kaşıntı, kuruluk ve kızarıklıkla seyreden iltihaplı deri hastalıklarını kapsar.",
                   "Benzer görünümde başka durumlar da olabilir."),
        "Sedef (Psoriasis)": ("Genellikle pullu ve belirgin sınırlı plaklarla seyreden kronik iltihaplı bir deri hastalığıdır.",
                              "Tanı klinik değerlendirmeyle yapılır."),
        "Tinea corporis": ("Deride mantar enfeksiyonudur; halka biçimli, pullu döküntülere neden olabilir.",
                           "Uygun tanı ve tedavi için sağlık uzmanına danışılmalıdır."),
        "Pityriasis rosea": ("Çoğu zaman gövdede görülen, kendini sınırlayabilen bir döküntüdür.",
                            "Başka döküntülerle karışabileceği için değerlendirme gerekebilir."),
    }
    for name, (description, note) in info.items():
        with st.expander(name):
            st.write(description)
            st.caption(note)
    st.info("Bu bilgiler genel eğitim amaçlıdır; kişisel tıbbi tavsiye değildir.")

elif page == STEPS[6]:
    section("Dermatolojiye yönlendirme", "Tıbbi kararları bir sağlık uzmanıyla birlikte verin.")
    tile("Dermatoloji (Cildiye)", "Devam eden, yayılan veya açıklanamayan deri bulguları için uygun uzmanlık alanıdır.", "🩺")
    st.link_button("🌐 MHRS üzerinden randevu sayfasını aç",
                   "https://www.mhrs.gov.tr/", use_container_width=True, type="primary")
    st.markdown("**ALO 182:** Telefonunuzdan `182` numarasını arayabilirsiniz.")
    st.markdown('<a href="tel:182" style="display:block;text-align:center;background:#eef0ff;'
                'border-radius:13px;padding:13px;color:#5044bb;text-decoration:none;font-weight:700">'
                '📞 182’yi ara</a>', unsafe_allow_html=True)
    st.warning("Hızla kötüleşen bulgular, ciddi ağrı, ateş veya genel durum bozukluğu varsa acil tıbbi değerlendirme alın.")
    st.caption("Uygulama sizin adınıza randevu oluşturmaz.")

else:
    section("Proje hakkında")
    tile("Araştırma amacı", "Benzer deri hastalıklarının görüntü sınıflandırma araştırması için kullanıcı arayüzü geliştirmek.", "🔬")
    tile("Kullanılan teknolojiler", "Python, Streamlit ve Pillow. Gelecekte uygun şekilde eğitilmiş model entegre edilebilir.", "💻")
    tile("Mevcut sürüm", "Tam arayüz prototipi: kamera, yükleme, anket, örnek sonuç, bilgi ve MHRS yönlendirmesi.", "🧩")
    st.markdown("### Sonraki araştırma adımları")
    st.write("1. Etik ve lisans açısından uygun veri setlerinin belirlenmesi.")
    st.write("2. Eğitim/test ayrımının kişi bazında yapılması.")
    st.write("3. Modelin bağımsız verilerde duyarlılık, özgüllük ve hata analiziyle değerlendirilmesi.")
    st.write("4. Klinik doğrulama olmadan gerçek hasta kullanımına sunulmaması.")
    st.info("Gizlilik: Bu demo fotoğrafı görüntülemek için işler; dosyayı ayrıca diske kaydetmez. "
            "Bununla birlikte barındırma hizmeti ve sunucu aktarımı nedeniyle gerçek hasta görüntüleri yüklenmemelidir.")

st.divider()
st.caption("DermaFark AI • TÜBİTAK eğitim ve araştırma prototipi • Tanı aracı değildir.")
