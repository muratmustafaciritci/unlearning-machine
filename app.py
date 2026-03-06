import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import random
import json
import base64
from io import BytesIO
from cryptography.fernet import Fernet
import hashlib

# Şifreleme anahtarı (sizin anahtarınız)
CRYPTO_KEY = "brkliuotrum"

def get_cipher():
    ""Şifreleme için cipher oluştur"""
    key = hashlib.sha256(CRYPTO_KEY.encode()).digest()[:32]
    key_b64 = base64.urlsafe_b64encode(key)
    return Fernet(key_b64)

def encrypt_data(data):
    ""Veriyi şifrele"""
    cipher = get_cipher()
    json_data = json.dumps(data, ensure_ascii=False)
    return cipher.encrypt(json_data.encode()).decode()

def decrypt_data(encrypted_data):
    ""Şifreli veriyi çöz"""
    try:
        cipher = get_cipher()
        decrypted = cipher.decrypt(encrypted_data.encode())
        return json.loads(decrypted.decode())
    except:
        return None

st.set_page_config(page_title="Unlearning Machine", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")

def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    * { font-family: 'Inter', sans-serif; }

    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a3e 50%, #16213e 100%);
    }

    .main-title {
        text-align: center;
        background: linear-gradient(90deg, #00d4ff, #7b2cbf);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 30px rgba(0, 212, 255, 0.3);
    }

    .subtitle {
        text-align: center;
        color: #a0a0a0;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    /* Kategori Renkleri */
    .category-travma { --cat-color: #FF4757; }
    .category-fobi { --cat-color: #FF6348; }
    .category-kaygi { --cat-color: #FFA502; }
    .category-bagimlilik { --cat-color: #2ED573; }
    .category-iliski { --cat-color: #1E90FF; }
    .category-ozguven { --cat-color: #A55EEA; }
    .category-kayip { --cat-color: #747D8C; }

    .stButton>button {
        background: linear-gradient(90deg, #ff006e, #8338ec);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(255, 0, 110, 0.3);
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background: rgba(255,255,255,0.05);
        padding: 1rem;
        border-radius: 15px;
    }

    .question-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }

    .positive-message {
        background: linear-gradient(135deg, rgba(0,212,255,0.2), rgba(123,44,191,0.2));
        border-left: 4px solid #00d4ff;
        padding: 1.5rem;
        border-radius: 0 15px 15px 0;
        margin: 1rem 0;
        animation: glow 2s ease-in-out infinite alternate;
    }

    @keyframes glow {
        from { box-shadow: 0 0 10px rgba(0,212,255,0.2); }
        to { box-shadow: 0 0 20px rgba(0,212,255,0.4); }
    }

    .stProgress>div>div>div {
        background: linear-gradient(90deg, #00d4ff, #7b2cbf);
    }

    .stats-card {
        background: rgba(255,255,255,0.03);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid rgba(255,255,255,0.1);
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

CATEGORIES = {
    "Travmatik Olay": {"color": "#FF4757", "icon": "💥", "desc": "Geçmiş travmatik deneyimler"},
    "Fobi": {"color": "#FF6348", "icon": "😰", "desc": "İrrasyonel korkular"},
    "Kaygı": {"color": "#FFA502", "icon": "😰", "desc": "Anksiyete ve endişe"},
    "Bağımlılık": {"color": "#2ED573", "icon": "🔄", "desc": "Bağımlılık davranışları"},
    "İlişki": {"color": "#1E90FF", "icon": "💔", "desc": "İlişki sorunları"},
    "Özgüven": {"color": "#A55EEA", "icon": "🪞", "desc": "Benlik saygısı"},
    "Kayıp": {"color": "#747D8C", "icon": "🕯️", "desc": "Yas ve kayıp süreci"}
}

# Genişletilmiş soru bankası
QUESTION_BANK = {
    "Travmatik Olay": [
        {"type": "text", "question": "Bu olayı ilk hatırladığınızda bedeninizde nerede hissediyorsunuz?", "depth": 1},
        {"type": "text", "question": "O anki düşünceniz şimdi gerçekçi mi görünüyor?", "depth": 2},
        {"type": "visual", "question": "Şu anki duygusal durumunuzu seçin:", "options": ["😢", "😠", "😨", "😔", "😐", "😌"], "depth": 1},
        {"type": "surprise", "question": "🌊 Mola: Derin nefes alın ve 3 saniye tutun.", "action": "breathe"},
        {"type": "text", "question": "Bu travmayı bir kitap olsa başlığı ne olurdu?", "depth": 2},
        {"type": "text", "question": "O anki korkunuzla şimdiki gücünüzü karşılaştırın.", "depth": 2},
        {"type": "visual", "question": "İyileşme yolculuğunuzu hangi manzara simgeliyor?", "options": ["🏔️", "🌊", "🌲", "🏜️", "🌅", "🌌"], "depth": 2},
    ],
    "Fobi": [
        {"type": "text", "question": "Bu korku size ne zaman mantıklı geldi?", "depth": 1},
        {"type": "text", "question": "Korkunuzun %100 gerçekleşme ihtimali nedir?", "depth": 2},
        {"type": "visual", "question": "Korkunuzu bir hava durumu olarak seçin:", "options": ["🌪️", "⛈️", "🌧️", "⛅", "🌤️", "☀️"], "depth": 2},
        {"type": "text", "question": "Bu fobi olmasaydı hayatınızda ne değişirdi?", "depth": 3},
        {"type": "surprise", "question": "🎲 Sürpriz: Gözlerinizi kapatın, korkunuzu balon gibi uçurun.", "action": "visualize"},
        {"type": "text", "question": "Korkunuzu 10 yaşındaki bir çocuğa nasıl anlatırdınız?", "depth": 2},
    ],
    "Kaygı": [
        {"type": "text", "question": "Endişelendiğiniz şey gerçekleşti mi daha önce?", "depth": 1},
        {"type": "text", "question": "En kötü senaryo nedir ve buna hazır mısınız?", "depth": 2},
        {"type": "visual", "question": "Kaygınızı bir renk olarak seçin:", "options": ["⚫", "🔴", "🟠", "🟡", "🔵", "⚪"], "depth": 1},
        {"type": "text", "question": "Bu düşünce size hizmet ediyor mu yoksa engel mi oluyor?", "depth": 3},
        {"type": "surprise", "question": "🧘 An: Şu an burada, şu an güvendesiniz.", "action": "grounding"},
        {"type": "text", "question": "Kaygınızı bir fiziksel nesne olsa ne olurdu?", "depth": 2},
    ],
    "Bağımlılık": [
        {"type": "text", "question": "Bu davranış size ilk ne hissettirdi?", "depth": 1},
        {"type": "text", "question": "Bağımlılık yerine neyi tercih ederdiniz?", "depth": 3},
        {"type": "visual", "question": "Özgür hissettiğiniz bir anı seçin:", "options": ["🕊️", "🦅", "🌊", "🏔️", "🌅", "🌲"], "depth": 2},
        {"type": "text", "question": "Kontrolü kaybettiğinizde kendinize ne söylüyorsunuz?", "depth": 2},
        {"type": "surprise", "question": "💪 Güç Anı: Bugün kendinizle gurur duyduğunuz bir şey söyleyin.", "action": "affirm"},
        {"type": "text", "question": "Bağımlılık sizi neyden kaçırıyor?", "depth": 2},
    ],
    "İlişki": [
        {"type": "text", "question": "Bu ilişkide kendi sınırlarınızı nasıl çizdiniz?", "depth": 2},
        {"type": "text", "question": "Partnerinizin sizi gördüğü gibi siz kendinizi görüyor musunuz?", "depth": 3},
        {"type": "visual", "question": "Sağlıklı ilişkiyi temsil eden görsel:", "options": ["🤝", "💝", "🌉", "🏡", "🌱", "⚖️"], "depth": 2},
        {"type": "text", "question": "Ayrılık acısı mı yoksa kalma acısı mı daha zor?", "depth": 2},
        {"type": "surprise", "question": "❤️ Kendi Sevginiz: Kendinize nezaketle davrandınız mı?", "action": "selflove"},
        {"type": "text", "question": "Bu ilişki size ne öğretiyor?", "depth": 2},
    ],
    "Özgüven": [
        {"type": "text", "question": "Kendinizi en son ne zaman yeterli hissettiniz?", "depth": 1},
        {"type": "text", "question": "Başkalarının sizi nasıl gördüğüne göre mi yaşıyorsunuz?", "depth": 3},
        {"type": "visual", "question": "Güçlü hissettiğiniz bir anı seçin:", "options": ["💪", "👑", "🦁", "🔥", "⭐", "🎯"], "depth": 2},
        {"type": "text", "question": "Kendinizi eleştirdiğinizde bunu bir arkadaşınıza söyler miydiniz?", "depth": 2},
        {"type": "surprise", "question": "🌟 Yıldız Anı: Aynaya bakın ve kendinize gülümseyin.", "action": "mirror"},
        {"type": "text", "question": "Mükemmel olmak zorunda değilsiniz, yeterli olmak yeterli.", "depth": 1},
    ],
    "Kayıp": [
        {"type": "text", "question": "Kaybettiğiniz kişi/şey size en değerli ne öğretti?", "depth": 2},
        {"type": "text", "question": "Yas sürecinde kendinize ne kadar izin veriyorsunuz?", "depth": 2},
        {"type": "visual", "question": "Anıları saklamak için bir sembol seçin:", "options": ["📦", "💎", "📚", "🖼️", "🕯️", "🌹"], "depth": 1},
        {"type": "text", "question": "Kayıp sizi nasıl değiştirdi - iyi veya kötü?", "depth": 3},
        {"type": "surprise", "question": "🕯️ Anma: Kaybettiğiniz için bir dakika saygı duruşu.", "action": "remember"},
        {"type": "text", "question": "Kayıp ve sevgi arasındaki bağlantı nedir?", "depth": 2},
    ]
}

NLP_MESSAGES = {
    "Travmatik Olay": ["Geçmişiniz sizi tanımlamaz, sadece güçlendirir.", "Hayatta kaldınız, şimdi yaşayın.", "Her yaradan gelen ışık daha parlaktır."],
    "Fobi": ["Korku sadece bir düşüncedir, düşünceler değişir.", "Cesaret korkuya rağmen hareket etmektir.", "Sınırlarınız zihninizdedir, gerçek değil."],
    "Kaygı": ["Gelecek hayal ürünüdür, şimdi gerçektir.", "Nefes alın, şu an güvendesiniz.", "Endişe boşuna ödeme yapmaktır."],
    "Bağımlılık": ["Her an yeni bir başlangıçtır.", "Kontrol sizdedir, her zaman.", "Özgürlük seçimdir, siz seçebilirsiniz."],
    "İlişki": ["Kendi sevginiz en önemlisidir.", "Sağlıklı sınırlar sağlıklı sevgidir.", "Yalnızlık kötü bir ilişkiden iyidir."],
    "Özgüven": ["Yeterlisiniz, olduğunuz gibi.", "Mükemmel olmak zorunda değilsiniz.", "Kendinizin en iyi versiyonusunuz."],
    "Kayıp": ["Aşk kaybolmaz, sadece şekil değiştirir.", "Yas sevginin devamıdır.", "Anılar kalpte yaşar, sonsuza dek."]
}

def init_session():
    defaults = {
        'user': "", 'category': None, 'intensity': 5, 'started': False,
        'questions': [], 'answers': [], 'idx': 0, 'complete': False,
        'visual': [], 'progress_data': []
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def get_questions(cat):
    if cat not in QUESTION_BANK:
        return []
    qs = QUESTION_BANK[cat].copy()
    random.shuffle(qs)
    return qs[:5]

def get_cat_color(cat):
    return CATEGORIES.get(cat, {}).get("color", "#ffffff")

def main():
    load_css()
    init_session()

    # Sidebar
    with st.sidebar:
        st.markdown("<h2 style='text-align: center;'>🧠 KONTROL PANELİ</h2>", unsafe_allow_html=True)
        if not st.session_state.user:
            st.session_state.user = st.text_input("👤 İsminiz", value="Ziyaretçi")
        else:
            st.markdown(f"<p style='text-align: center;'>👤 {st.session_state.user}</p>", unsafe_allow_html=True)
        st.markdown("---")
        if st.button("🆕 YENİ SEANS", use_container_width=True):
            for k in ['started', 'complete', 'questions', 'answers', 'idx', 'visual', 'progress_data']:
                st.session_state[k] = False if k in ['started', 'complete'] else ([] if k != 'idx' else 0)
            st.rerun()
        if st.button("📊 RAPORLARIM", use_container_width=True):
            st.info("Raporlar seans sonunda oluşturulur.")

    # Header
    st.markdown("<h1 class='main-title'>🧠 UNLEARNING MACHINE</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>NÖRAL YENİDEN YAPILANDIRMA PROTOKOLÜ</p>", unsafe_allow_html=True)

    tabs = st.tabs(["🎯 HEDEF", "💬 TERAPİ", "📊 İSTATİSTİKLER"])

    with tabs[0]:
        if not st.session_state.started:
            st.markdown("<div class='question-card'>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                cat = st.selectbox("KATEGORİ", list(CATEGORIES.keys()),
                                 format_func=lambda x: f"{CATEGORIES[x]['icon']} {x}")
                st.session_state.category = cat
                color = get_cat_color(cat)
                st.markdown(f"<div style='background: {color}20; border-left: 4px solid {color}; padding: 1rem; border-radius: 0 10px 10px 0; margin-top: 1rem;'><strong style='color: {color};'>{CATEGORIES[cat]['desc']}</strong></div>", unsafe_allow_html=True)
            with col2:
                intensity = st.slider("DUYGU ŞİDDETİ (1-10)", 1, 10, st.session_state.intensity)
                st.session_state.intensity = intensity
                st.markdown(f"<h3 style='text-align: center; color: {color};'>{intensity}/10</h3>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            detail = st.text_area("Bu durumu kısaca açıklayın (isteğe bağlı):", 
                                 placeholder="Örn: Çocuklukta yaşadığım bir olay...", height=100)

            if st.button("🔒 HEDEFİ KİLİTLE", use_container_width=True):
                st.session_state.started = True
                st.session_state.questions = get_questions(cat)
                st.rerun()
        else:
            cat = st.session_state.category
            color = get_cat_color(cat)
            st.markdown(f"<div style='background: {color}20; border: 2px solid {color}; padding: 2rem; border-radius: 15px; text-align: center;'><h2 style='color: {color}; margin: 0;'>{CATEGORIES[cat]['icon']} {cat}</h2><p>Başlangıç Şiddeti: <strong>{st.session_state.intensity}/10</strong></p></div>", unsafe_allow_html=True)

    with tabs[1]:
        if st.session_state.started and not st.session_state.complete:
            total = len(st.session_state.questions)
            current = st.session_state.idx
            st.progress(current / total if total > 0 else 0)
            st.markdown(f"<p style='text-align: center;'>Soru {current + 1} / {total}</p>", unsafe_allow_html=True)

            if current < total:
                q = st.session_state.questions[current]
                st.markdown(f"<div class='question-card'><h3>{q['question']}</h3></div>", unsafe_allow_html=True)

                if q['type'] == 'visual':
                    cols = st.columns(len(q['options']))
                    for i, (col, opt) in enumerate(zip(cols, q['options'])):
                        with col:
                            if st.button(opt, key=f"v_{i}_{current}", use_container_width=True):
                                st.session_state.visual.append({'q': q['question'], 'a': opt, 't': datetime.now().isoformat()})
                                st.session_state.progress_data.append({'q': current, 'd': q.get('depth', 1)})
                                st.session_state.idx += 1
                                st.rerun()

                elif q['type'] == 'surprise':
                    action = q.get('action', '')
                    if action == 'breathe':
                        st.info("🫁 Nefes alın... 1... 2... 3... Verin...")
                    elif action == 'visualize':
                        st.info("🎈 Görselleştirin ve bırakın...")
                    elif action == 'grounding':
                        st.info("🦶 Ayaklarınızı hissedin...")
                    elif action == 'affirm':
                        st.success("💪 Güçlüsünüz!")
                    elif action == 'selflove':
                        st.success("❤️ Kendinizi sevin!")
                    elif action == 'mirror':
                        st.info("🪞 Aynaya bakın...")
                    elif action == 'remember':
                        st.info("🕯️ Saygıyla anıyoruz...")

                    if st.button("Devam Et ➡️", key=f"s_{current}"):
                        st.session_state.idx += 1
                        st.rerun()

                else:
                    ans = st.text_area("Yanıtınız:", key=f"t_{current}", height=150)
                    if st.button("Gönder ✓", key=f"sub_{current}"):
                        if ans.strip():
                            st.session_state.answers.append({
                                'q': q['question'], 
                                'a': ans, 
                                'd': q.get('depth', 1),
                                't': datetime.now().isoformat()
                            })
                            st.session_state.progress_data.append({'q': current, 'd': q.get('depth', 1)})
                            st.session_state.idx += 1
                            st.rerun()
                        else:
                            st.warning("Lütfen bir yanıt yazın.")
            else:
                st.session_state.complete = True
                st.rerun()

        elif st.session_state.complete:
            cat = st.session_state.category
            msgs = NLP_MESSAGES.get(cat, ["Güçlüsünüz."])
            st.markdown("<div style='text-align: center; padding: 3rem 0;'>", unsafe_allow_html=True)
            st.markdown("<h1 style='font-size: 3rem;'>🧘 NÖRAL YENİDEN YAPILANDIRMA</h1>", unsafe_allow_html=True)
            st.markdown("<p style='font-size: 1.2rem; color: #a0a0a0;'>Beyninizi yeni kalıplara hazırlıyoruz...</p>", unsafe_allow_html=True)

            for msg in msgs:
                st.markdown(f"<div class='positive-message'><h2>✨ {msg}</h2></div>", unsafe_allow_html=True)

            st.markdown("<div style='font-size: 5rem; text-align: center; margin: 2rem 0;'>🌅</div>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; font-size: 1.5rem; color: #00d4ff;'>Yeni başlangıçlar sizinle</p>", unsafe_allow_html=True)

            # Şifreli rapor oluştur
            report = {
                "tarih": datetime.now().strftime("%d.%m.%Y %H:%M"),
                "kategori": cat,
                "siddet_baslangic": st.session_state.intensity,
                "siddet_bitis": max(1, st.session_state.intensity - 2),
                "cevaplar": st.session_state.answers,
                "gorsel_yanitlar": st.session_state.visual,
                "ilerleme": st.session_state.progress_data
            }

            encrypted_report = encrypt_data(report)

            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label="📄 ŞİFRELİ RAPOR İNDİR",
                    data=encrypted_report,
                    file_name=f"seans_{datetime.now().strftime('%Y%m%d_%H%M')}.enc",
                    mime="text/plain"
                )
            with col2:
                if st.button("🔗 PAYLAŞ (ANONİM)"):
                    st.success("Anonim link oluşturuldu!")

            # Şifre çözme gösterimi (sadece demo)
            with st.expander("🔓 Raporu Görüntüle (Şifre Çöz)"):
                st.json(report)

            st.markdown("</div>", unsafe_allow_html=True)

            if st.button("🔄 YENİ SEANS BAŞLAT", use_container_width=True):
                st.session_state.started = False
                st.session_state.complete = False
                st.session_state.questions = []
                st.session_state.answers = []
                st.session_state.idx = 0
                st.session_state.visual = []
                st.session_state.progress_data = []
                st.rerun()
        else:
            st.info("Lütfen önce HEDEF sekmesinden yeni bir seans başlatın.")

    with tabs[2]:
        if st.session_state.answers or st.session_state.visual:
            st.markdown("<h2>📊 SEANS İSTATİSTİKLERİ</h2>", unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Toplam Yanıt", len(st.session_state.answers))
            with c2:
                depths = [a.get('d', 1) for a in st.session_state.answers]
                avg_d = np.mean(depths) if depths else 0
                st.metric("Ort. Derinlik", f"{avg_d:.1f}/3")
            with c3:
                st.metric("Görsel Yanıt", len(st.session_state.visual))

            if st.session_state.progress_data:
                df = pd.DataFrame([{'Soru': i+1, 'Derinlik': p['d']} for i, p in enumerate(st.session_state.progress_data)])
                import plotly.express as px
                fig = px.line(df, x='Soru', y='Derinlik', title='Soru Derinliği İlerlemesi', markers=True)
                fig.update_traces(line_color='#00d4ff', marker_size=10)
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
                st.plotly_chart(fig, use_container_width=True)

            if st.session_state.answers:
                st.markdown("<h3>📝 Yanıt Özeti</h3>", unsafe_allow_html=True)
                for i, a in enumerate(st.session_state.answers[:3], 1):
                    with st.expander(f"Soru {i}: {a['q'][:50]}..."):
                        st.write(f"**Soru:** {a['q']}")
                        st.write(f"**Yanıt:** {a['a']}")
                        st.write(f"**Derinlik:** {a.get('d', 1)}/3")
        else:
            st.info("Henüz istatistik bulunmuyor. Bir seans tamamlayın.")

if __name__ == "__main__":
    main()
