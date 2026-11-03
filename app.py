import io
from html import escape
from datetime import datetime
import streamlit as st
from PIL import Image, ImageOps

st.set_page_config(page_title="DermaFark AI", page_icon="🔬", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap');
html,body,[data-testid="stApp"]{font-family:'Nunito',sans-serif}
[data-testid="stAppViewContainer"]{background:linear-gradient(180deg,#f9f6ff 0%,#ffffff 65%)}
.block-container{max-width:490px;padding:0.7rem 1rem 5rem}
#MainMenu,footer,[data-testid="stDecoration"]{display:none}
h1,h2,h3{color:#351276;letter-spacing:-.035em}
h2{font-size:1.65rem;text-align:center;margin:0.6rem 0 0.2rem}
p{line-height:1.5}
.brand{display:flex;align-items:center;gap:10px;padding:10px 2px 13px;
border-bottom:1px solid #eee7fa;font-weight:900;color:#351276;font-size:19px}
.logo{width:42px;height:42px;display:grid;place-items:center;border-radius:50%;
background:#e9d8ff;color:#661dc5;font-size:25px}
.hero{background:radial-gradient(circle at 70% 20%,#e4d2ff 0%,transparent 42%),linear-gradient(145deg,#f5ecff,#fff);
border-radius:22px;text-align:center;padding:22px 14px 20px;margin:12px 0 15px}
.illustration{font-size:70px;line-height:1.25;margin:8px auto 15px}
.hero h1{font-size:35px;margin:0 0 10px;color:#351276;font-weight:900}
.hero p{color:#342a54;font-size:16px;margin:0 auto 12px;max-width:300px}
.card{border:1px solid #e8dff5;background:white;border-radius:17px;padding:15px;
box-shadow:0 5px 14px #4b277410;margin:8px 0}
.card-title{font-size:17px;font-weight:900;color:#351276}
.card-desc{font-size:13px;color:#4e4c62;margin-top:5px}
.step{display:flex;justify-content:center;align-items:center;gap:11px;margin:20px auto}
.dot{width:31px;height:31px;border:1px solid #bcb1d2;border-radius:50%;display:grid;
place-items:center;color:#706382;font-weight:900}
.dot.active{background:#6b24c7;color:white;border-color:#6b24c7}
.divider{height:2px;background:#ddd2eb;width:24px}
.notice{background:#f1edff;border-radius:14px;padding:13px;color:#493279;font-size:13px;margin:12px 0}
.alert{background:#fff5e8;border:1px solid #ffdfb7;border-radius:14px;padding:12px;color:#7b532b;font-size:13px;margin:10px 0}
.stButton>button[kind="primary"],.stDownloadButton>button[kind="primary"]{
background:linear-gradient(100deg,#5c16b5,#7824d2);color:white;border:0;
border-radius:11px;font-weight:900;min-height:46px;box-shadow:0 4px 9px #651cb526}
.stButton>button{border-radius:11px;font-weight:800;min-height:44px}
[data-testid="stFileUploader"]{background:#fff;border:2px dashed #c7a4f1;border-radius:16px;padding:9px}
[data-testid="stRadio"] label,[data-testid="stCheckbox"] label{font-size:14px}
.caption{color:#81768f;font-size:12px;text-align:center}
@media(max-width:500px){.block-container{padding:0.5rem .8rem 4rem}.hero h1{font-size:32px}}
</style>
""",unsafe_allow_html=True)

PAGES=["Ana Sayfa","Fotoğraf Yükleme / Çekme","Belirti Anketi","Analiz Ekranı",
       "Sonuç ve Rapor","Hastalık Bilgileri","Randevu ve Destek","Proje Hakkında"]
if "page" not in st.session_state: st.session_state.page=PAGES[0]
if "photo" not in st.session_state: st.session_state.photo=None
if "answers" not in st.session_state: st.session_state.answers={}

def go(name):
    st.session_state.page=name
    st.rerun()

def button(label,destination,primary=False,key=None):
    if st.button(label,type="primary" if primary else "secondary",use_container_width=True,key=key):
        go(destination)

def steps(current):
    parts=[]
    for i in range(1,5):
        parts.append(f'<span class="dot {"active" if i==current else ""}">{i}</span>')
        if i<4: parts.append('<span class="divider"></span>')
    st.markdown('<div class="step">{"".join(parts)}</div>'.replace('{"".join(parts)}',''.join(parts)),unsafe_allow_html=True)

def card(icon,title,desc):
    st.markdown(f'<div class="card"><div class="card-title">{icon} {escape(title)}</div>'
                f'<div class="card-desc">{escape(desc)}</div></div>',unsafe_allow_html=True)

def title(text,subtitle=""):
    st.markdown(f"<h2>{escape(text)}</h2>",unsafe_allow_html=True)
    if subtitle: st.markdown(f'<p style="text-align:center;color:#574e67;font-size:14px">{escape(subtitle)}</p>',unsafe_allow_html=True)

def show_photo():
    if st.session_state.photo:
        st.image(st.session_state.photo,caption="Yüklenen örnek fotoğraf",use_container_width=True)
        return True
    return False

st.markdown('<div class="brand"><span class="logo">⚕</span> DermaFark AI</div>',unsafe_allow_html=True)
with st.sidebar:
    st.subheader("☰ Menü")
    for item in PAGES:
        if st.button(item,key="nav_"+item,use_container_width=True):
            go(item)
    st.caption("TÜBİTAK 2204-B araştırma prototipi")

if st.session_state.page==PAGES[0]:
    st.markdown('<div class="hero"><div class="illustration">🔎🧬</div>'
                '<h1>DermaFark AI</h1><p>Deri Hastalıkları İçin Yapay Zekâ Destekli '
                'Ön Değerlendirme Sistemi</p></div>',unsafe_allow_html=True)
    button("▶ Analize Başla",PAGES[1],True)
    a,b=st.columns(2)
    with a:
        card("📷","Görüntü Analizi","Fotoğraf yükleme")
        button("Fotoğraf Ekle",PAGES[1],key="home_photo")
        card("📖","Hastalık Bilgileri","Bilgi kartları")
        button("Bilgileri Aç",PAGES[5],key="home_info")
    with b:
        card("📋","Belirti Anketi","Kısa sorular")
        button("Anketi Aç",PAGES[2],key="home_survey")
        card("ⓘ","Proje Hakkında","Araştırma amacı")
        button("Projeyi Gör",PAGES[7],key="home_about")

elif st.session_state.page==PAGES[1]:
    steps(1)
    title("Görüntü Yükle / Çek","Analiz etmek istediğiniz deri bölgesinin net bir fotoğrafını seçin.")
    upload=st.file_uploader("📁 Fotoğraf yükle (JPG, PNG)",type=["jpg","jpeg","png"])
    camera=st.camera_input("📷 Kamerayla çek")
    file=camera or upload
    if file is not None:
        try:
            if len(file.getvalue())>8_000_000: raise ValueError("8 MB sınırı aşıldı")
            im=Image.open(io.BytesIO(file.getvalue()))
            im=ImageOps.exif_transpose(im).convert("RGB")
            if im.width*im.height>24_000_000: raise ValueError("Görüntü çok büyük")
            st.session_state.photo=im
        except Exception:
            st.error("Görsel okunamadı. Daha küçük JPG/PNG yükleyin.")
    show_photo()
    st.markdown('<div class="notice">ℹ️ İyi fotoğraf için: Yeterli ışık kullanın, '
                'görüntüyü net çekin, yalnızca gerekli bölgeyi kadraja alın.</div>',unsafe_allow_html=True)
    if st.session_state.photo:
        button("Devam Et →",PAGES[2],True)
    st.caption("Yalnızca izinli eğitim görselleri yükleyin; gerçek hasta fotoğrafları kullanmayın.")

elif st.session_state.page==PAGES[2]:
    steps(2)
    title("Belirti Anketi","Deri bölgenizle ilgili aşağıdaki soruları yanıtlayın.")
    with st.form("form"):
        duration=st.radio("1. Lezyonunuz ne kadar süredir var?",["1 haftadan kısa","1 hafta – 1 ay","1 ay – 6 ay","6 aydan uzun"],index=None)
        symptoms=st.multiselect("2. Hangi belirtileri gözlemliyorsunuz?",["Kaşıntı","Kızarıklık","Pullanma","Kuruluk","Ağrı / hassasiyet"])
        spread=st.radio("3. Görünüm zamanla yayıldı veya değişti mi?",["Evet","Hayır","Emin değilim"],index=None)
        treatment=st.radio("4. Daha önce tedavi denendi mi?",["Evet","Hayır"],index=None)
        red=st.checkbox("Ateş, hızla kötüleşme veya ciddi ağrı gibi ek belirtiler var")
        ok=st.form_submit_button("Anketi Kaydet →",type="primary",use_container_width=True)
    if ok:
        if duration is None or spread is None or treatment is None: st.error("Lütfen zorunlu soruları yanıtlayın.")
        else:
            st.session_state.answers={"Süre":duration,"Belirtiler":", ".join(symptoms) or "Belirtilmedi",
                                      "Yayılma":spread,"Tedavi":treatment,"Ek uyarı belirtileri":"Evet" if red else "Hayır"}
            go(PAGES[3])

elif st.session_state.page==PAGES[3]:
    steps(3)
    title("Analiz Ekranı","Yapay zekâ modelinin bağlanacağı bölüm.")
    st.markdown('<div class="hero"><div class="illustration">🧠</div>'
                '<h1 style="font-size:25px">Analiz Taslağı</h1>'
                '<p>Henüz eğitilmiş bir görüntü sınıflandırma modeli bağlı değil.</p></div>',unsafe_allow_html=True)
    st.progress(100,text="Arayüz hazır — gerçek analiz yapılmadı")
    st.markdown('<div class="notice">Bu ekranda sahte sonuç veya hastalık olasılığı '
                'üretilmez. Model eğitimi ve doğrulaması tamamlandığında bu bölüme eklenecektir.</div>',
                unsafe_allow_html=True)
    button("Sonuç Ekranına Geç →",PAGES[4],True)

elif st.session_state.page==PAGES[4]:
    steps(4)
    title("Ön Değerlendirme Sonucu")
    st.markdown('<div class="alert"><b>🧪 DEMO — Tanı sonucu yok</b><br>'
                'Görseldeki örnek tasarımın aksine, şu anda %82 gibi bir hastalık olasılığı '
                'hesaplanmamaktadır. Gerçek model eklenince doğrulanmış çıktılar gösterilebilir.</div>',
                unsafe_allow_html=True)
    if st.session_state.answers:
        st.subheader("📋 Anket özeti")
        for k,v in st.session_state.answers.items(): st.write(f"**{k}:** {v}")
        if st.session_state.answers.get("Ek uyarı belirtileri")=="Evet":
            st.error("Ateş, ciddi ağrı veya hızla kötüleşmede gecikmeden sağlık kuruluşuna başvurun.")
    st.markdown('<div class="notice">ℹ️ Kesin tanı için dermatoloji uzmanına başvurunuz. '
                'Fotoğraf tek başına Mikozis Fungoides veya diğer hastalıkları doğrulamaz ya da dışlamaz.</div>',
                unsafe_allow_html=True)
    report="DERMAFARK AI - EĞİTİM DEMOSU\nGerçek görüntü analizi yapılmadı.\n"
    report+=f"Tarih: {datetime.now():%d.%m.%Y %H:%M}\n"
    report+="\n".join(f"{k}: {v}" for k,v in st.session_state.answers.items())
    report+="\nTıbbi tanı yerine geçmez."
    st.download_button("⬇ Demo Raporunu İndir (TXT)",report,"dermafark_ozet.txt",
                       "text/plain",use_container_width=True)
    button("📅 MHRS / ALO 182",PAGES[6],True)

elif st.session_state.page==PAGES[5]:
    title("Hastalık Bilgileri")
    diseases=[
      ("Mikozis Fungoides","Erken evrede egzama ve sedefle karışabilen, deriyi tutan bir T hücreli lenfoma türüdür."),
      ("Egzama","Ciltte kuruluk, kızarıklık ve kaşıntıyla seyreden yaygın iltihaplı deri durumlarıdır."),
      ("Sedef (Psoriasis)","Ciltte kırmızı, pullu plaklarla seyreden kronik iltihaplı hastalıktır."),
      ("Tinea corporis","Halka biçimli pullu döküntülere neden olabilen mantar enfeksiyonudur."),
      ("Pityriasis rosea","Genellikle gövdede ortaya çıkan ve zamanla kendiliğinden düzelebilen döküntüdür.")
    ]
    for name,desc in diseases:
        with st.expander("🩺 "+name):
            st.write(desc)
            st.caption("Bu bilgiler eğitim amaçlıdır; tanı için dermatoloji uzmanına danışın.")

elif st.session_state.page==PAGES[6]:
    title("Randevu ve Destek")
    card("🗓️","MHRS ile Randevu Al","Resmî MHRS sitesinden dermatoloji randevusu araştırabilirsiniz.")
    st.link_button("Randevu Al ↗","https://www.mhrs.gov.tr/",type="primary",use_container_width=True)
    card("☎️","ALO 182","Türkiye'de MHRS çağrı merkezi numarası.")
    st.markdown('<a href="tel:182" style="display:block;text-align:center;background:#eee0ff;'
                'color:#4e159c;padding:13px;border-radius:12px;font-weight:900;text-decoration:none">'
                '📞 182’yi Ara</a>',unsafe_allow_html=True)
    st.warning("Hızla kötüleşme, ciddi ağrı veya ateş gibi belirtilerde gecikmeden tıbbi değerlendirme alın.")
    st.caption("Bu uygulama sizin adınıza randevu oluşturmaz.")

else:
    title("Proje Hakkında")
    st.markdown('<div class="hero"><div class="illustration">⚗️</div>'
                '<h1 style="font-size:27px">DermaFark AI</h1>'
                '<p>TÜBİTAK 2204-B • Ortaokul Öğrencileri Araştırma Projesi</p></div>',
                unsafe_allow_html=True)
    card("🎯","Projenin Amacı","Görsel olarak benzer deri hastalıklarının yapay zekâ ile araştırılmasına yönelik bir prototip geliştirmek.")
    card("⌨️","Kullanılan Teknolojiler","Python, Streamlit, Pillow; ileride eğitilecek görüntü sınıflandırma modeli.")
    card("🔬","Araştırma Aşaması","Şu anda arayüz tamamlandı. Model eğitimi, bilimsel test ve klinik doğrulama yapılmadı.")

st.markdown('<div class="caption" style="margin-top:22px">DermaFark AI • Eğitim ve araştırma prototipi<br>'
            'Tıbbi tanı veya tarama aracı değildir.</div>',unsafe_allow_html=True)
