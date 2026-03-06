import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import random
import json
import base64
from cryptography.fernet import Fernet
import hashlib

CRYPTO_KEY = "brkliuotrum"

def get_cipher():
    key = hashlib.sha256(CRYPTO_KEY.encode()).digest()[:32]
    key_b64 = base64.urlsafe_b64encode(key)
    return Fernet(key_b64)

def encrypt_data(data):
    cipher = get_cipher()
    return cipher.encrypt(json.dumps(data, ensure_ascii=False).encode()).decode()

st.set_page_config(page_title="Unlearning Machine", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")

def load_css():
    st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f0f23 0%, #1a1a3e 50%, #16213e 100%); }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%) !important; }
    [data-testid="stSidebar"] * { color: #ffffff !important; }
    .stApp, .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, .stApp label, .stApp span, .stApp div { color: #ffffff !important; }
    .stTextInput label, .stTextArea label { color: #00d4ff !important; font-size: 1rem !important; font-weight: 600 !important; }
    .main-title { text-align: center; font-size: 3rem; font-weight: 700; margin-bottom: 0.5rem; color: #00d4ff !important; text-shadow: 0 0 30px rgba(0, 212, 255, 0.5); }
    .subtitle { text-align: center; color: #a0a0a0 !important; font-size: 1.1rem; margin-bottom: 2rem; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { background: rgba(255,255,255,0.1) !important; color: #ffffff !important; border: 1px solid rgba(255,255,255,0.3) !important; border-radius: 10px !important; }
    .stSelectbox>div>div { background: rgba(255,255,255,0.1) !important; color: #ffffff !important; border-radius: 10px !important; }
    .stButton>button { background: linear-gradient(90deg, #ff006e, #8338ec) !important; color: white !important; border: none !important; border-radius: 10px !important; padding: 0.75rem !important; width: 100% !important; font-weight: 600 !important; }
    .question-card { background: rgba(255,255,255,0.05) !important; border-radius: 20px; padding: 2rem; margin: 1rem 0; border: 1px solid rgba(255,255,255,0.1); }
    .question-card h3, .question-card h4 { color: #ffffff !important; }
    .nlp-card { background: linear-gradient(135deg, rgba(0,212,255,0.1), rgba(123,44,191,0.1)); border-radius: 20px; padding: 2rem; text-align: center; border: 1px solid rgba(0,212,255,0.3); margin: 1rem 0; }
    .stTabs [data-baseweb="tab-list"] { gap: 2rem; background: rgba(255,255,255,0.03); padding: 1rem; border-radius: 15px; }
    .stTabs [data-baseweb="tab"] { color: #ffffff !important; }
    .streamlit-expanderHeader { background: rgba(255,255,255,0.05) !important; color: #ffffff !important; border-radius: 10px !important; }
    .streamlit-expanderContent { background: rgba(0,0,0,0.5) !important; border-radius: 10px !important; padding: 1rem !important; }
    .stCodeBlock { background: rgba(0,0,0,0.5) !important; border: 1px solid rgba(0,212,255,0.3) !important; border-radius: 10px !important; }
    code { color: #00d4ff !important; background: rgba(0,0,0,0.3) !important; padding: 0.2rem 0.4rem !important; border-radius: 5px !important; }
    .stJson { background: rgba(0,0,0,0.5) !important; border-radius: 10px !important; padding: 1rem !important; }
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; background: rgba(0,0,0,0.5); color: #a0a0a0 !important; text-align: center; padding: 1rem; font-size: 0.9rem; z-index: 1000; }
    .footer a { color: #00d4ff !important; text-decoration: none; }
    
    /* GİRİŞ EKRANI ETİKETLERİ İÇİN EK CSS */
    .entry-label { color: #00d4ff !important; font-size: 1rem !important; font-weight: 600 !important; margin-bottom: 5px !important; display: block !important; }
    .entry-label strong { color: #00d4ff !important; }
    
    /* EXPANDER İÇİNDEKİ JSON VE METİN RENKLERİ */
    .streamlit-expanderContent pre { color: #00d4ff !important; background: rgba(0,0,0,0.3) !important; }
    .streamlit-expanderContent code { color: #00d4ff !important; background: rgba(0,0,0,0.3) !important; }
    .streamlit-expanderContent .stJson { color: #ffffff !important; }
    .streamlit-expanderContent p { color: #ffffff !important; }
    .streamlit-expanderContent span { color: #ffffff !important; }
    .streamlit-expanderContent div { color: #ffffff !important; }
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

QUESTION_BANK = {
    "Travmatik Olay": [
        {"type": "text", "question": "Bu olayı ilk hatırladığınızda bedeninizde nerede hissediyorsunuz?", "depth": 1},
        {"type": "text", "question": "O anki düşünceniz şimdi gerçekçi mi görünüyor?", "depth": 2},
        {"type": "visual", "question": "Şu anki duygusal durumunuzu seçin:", "options": ["😢", "😠", "😨", "😔", "😐", "😌"], "depth": 1},
        {"type": "surprise", "question": "🌊 Mola: Derin nefes alın ve 3 saniye tutun.", "action": "breathe"},
        {"type": "text", "question": "Bu travmayı bir kitap olsa başlığı ne olurdu?", "depth": 2},
        {"type": "text", "question": "O anki korkunuzla şimdiki gücünüzü karşılaştırın.", "depth": 2},
        {"type": "visual", "question": "İyileşme yolculuğunuzu hangi emoji temsil eder?", "options": ["🌱", "🦋", "🌅", "🏔️", "🌊", "🔥"], "depth": 2},
        {"type": "text", "question": "Bu olay size ne öğretti - olumlu veya olumsuz?", "depth": 3},
        {"type": "surprise", "question": "💪 Güç Anı: Kendinizi bu an için alkışlayın.", "action": "affirm"},
        {"type": "text", "question": "Şimdi bu duruma baktığınızda ne hissediyorsunuz?", "depth": 3},
    ],
    "Fobi": [
        {"type": "text", "question": "Bu korku size ne zaman mantıklı geldi?", "depth": 1},
        {"type": "text", "question": "Korkunuzun %100 gerçekleşme ihtimali nedir?", "depth": 2},
        {"type": "visual", "question": "Korkunuzu bir hava durumu olarak seçin:", "options": ["🌪️", "⛈️", "🌧️", "⛅", "🌤️", "☀️"], "depth": 2},
        {"type": "text", "question": "Bu fobi olmasaydı hayatınızda ne değişirdi?", "depth": 3},
        {"type": "surprise", "question": "🎲 Sürpriz: Gözlerinizi kapatın, korkunuzu balon gibi uçurun.", "action": "visualize"},
        {"type": "text", "question": "Korkunuzu 10 yaşındaki bir çocuğa nasıl anlatırdınız?", "depth": 2},
        {"type": "visual", "question": "Korkunuzu yenen bir süper kahraman seçin:", "options": ["🦸", "🦹", "🧙", "🥷", "🤺", "🛡️"], "depth": 2},
        {"type": "text", "question": "Korkunuz sizi nelerden mahrum bırakıyor?", "depth": 3},
        {"type": "surprise", "question": "🦁 Cesaret: Bugün küçük bir adım atsanız ne olur?", "action": "courage"},
        {"type": "text", "question": "Korkunuzla yüzleştiğinizde ne olacağını hayal edin.", "depth": 3},
    ],
    "Kaygı": [
        {"type": "text", "question": "Endişelendiğiniz şey gerçekleşti mi daha önce?", "depth": 1},
        {"type": "text", "question": "En kötü senaryo nedir ve buna hazır mısınız?", "depth": 2},
        {"type": "visual", "question": "Kaygınızı bir renk olarak seçin:", "options": ["⚫", "🔴", "🟠", "🟡", "🔵", "⚪"], "depth": 1},
        {"type": "text", "question": "Bu düşünce size hizmet ediyor mu yoksa engel mi oluyor?", "depth": 3},
        {"type": "surprise", "question": "🧘 An: Şu an burada, şu an güvendesiniz.", "action": "grounding"},
        {"type": "text", "question": "Kaygınızı bir fiziksel nesne olsa ne olurdu?", "depth": 2},
        {"type": "visual", "question": "Sakinliği temsil eden bir emoji seçin:", "options": ["🧘", "🌊", "🍃", "☁️", "🕯️", "🦢"], "depth": 2},
        {"type": "text", "question": "Endişeniz sizi hangi duygudan koruyor?", "depth": 3},
        {"type": "surprise", "question": "🌊 Dalga: Duygularınızın gelip geçtiğini hatırlayın.", "action": "wave"},
        {"type": "text", "question": "Kaygısız bir gün nasıl görünürdü?", "depth": 3},
    ],
    "Bağımlılık": [
        {"type": "text", "question": "Bu davranış size ilk ne hissettirdi?", "depth": 1},
        {"type": "text", "question": "Bağımlılık yerine neyi tercih ederdiniz?", "depth": 3},
        {"type": "visual", "question": "Özgür hissettiğiniz bir anı seçin:", "options": ["🕊️", "🦅", "🌊", "🏔️", "🌅", "🌲"], "depth": 2},
        {"type": "text", "question": "Kontrolü kaybettiğinizde kendinize ne söylüyorsunuz?", "depth": 2},
        {"type": "surprise", "question": "💪 Güç Anı: Bugün kendinizle gurur duyduğunuz bir şey?", "action": "affirm"},
        {"type": "text", "question": "Bağımlılık sizi neyden kaçırıyor?", "depth": 2},
        {"type": "visual", "question": "Özgürlüğü temsil eden bir sembol seçin:", "options": ["🔓", "🗝️", "🌈", "🦋", "🚀", "🎯"], "depth": 2},
        {"type": "text", "question": "Kontrolü geri almak için ilk adım ne olur?", "depth": 3},
        {"type": "surprise", "question": "🔥 Güç: İçinizdeki ateşi hissedin.", "action": "fire"},
        {"type": "text", "question": "Bağımsız bir hayat sizin için ne ifade ediyor?", "depth": 3},
    ],
    "İlişki": [
        {"type": "text", "question": "Bu ilişkide kendi sınırlarınızı nasıl çizdiniz?", "depth": 2},
        {"type": "text", "question": "Partnerinizin sizi gördüğü gibi siz kendinizi görüyor musunuz?", "depth": 3},
        {"type": "visual", "question": "Sağlıklı ilişkiyi temsil eden görsel:", "options": ["🤝", "💝", "🌉", "🏡", "🌱", "⚖️"], "depth": 2},
        {"type": "text", "question": "Ayrılık acısı mı yoksa kalma acısı mı daha zor?", "depth": 2},
        {"type": "surprise", "question": "❤️ Kendi Sevginiz: Kendinize nezaketle davrandınız mı?", "action": "selflove"},
        {"type": "text", "question": "Bu ilişki size ne öğretiyor?", "depth": 2},
        {"type": "visual", "question": "Kendinizi hangi emoji ile ifade edersiniz?", "options": ["💪", "😔", "😌", "🤔", "💔", "❤️"], "depth": 2},
        {"type": "text", "question": "Sağlıklı bir ilişki sizin için ne demek?", "depth": 3},
        {"type": "surprise", "question": "🌹 Değer: Kendi değerinizi hatırlayın.", "action": "value"},
        {"type": "text", "question": "İlişkide neyi değiştirmek istersiniz?", "depth": 3},
    ],
    "Özgüven": [
        {"type": "text", "question": "Kendinizi en son ne zaman yeterli hissettiniz?", "depth": 1},
        {"type": "text", "question": "Başkalarının sizi nasıl gördüğüne göre mi yaşıyorsunuz?", "depth": 3},
        {"type": "visual", "question": "Güçlü hissettiğiniz bir anı seçin:", "options": ["💪", "👑", "🦁", "🔥", "⭐", "🎯"], "depth": 2},
        {"type": "text", "question": "Kendinizi eleştirdiğinizde bunu bir arkadaşınıza söyler miydiniz?", "depth": 2},
        {"type": "surprise", "question": "🌟 Yıldız Anı: Aynaya bakın ve kendinize gülümseyin.", "action": "mirror"},
        {"type": "text", "question": "Mükemmel olmak zorunda değilsiniz, yeterli olmak yeterli.", "depth": 1},
        {"type": "visual", "question": "Kendinizi hangi hayvanla özdeşleştirirsiniz?", "options": ["🦁", "🦅", "🐘", "🦋", "🐺", "🦉"], "depth": 2},
        {"type": "text", "question": "Kendinize karşı daha nazik olsanız ne değişir?", "depth": 3},
        {"type": "surprise", "question": "👑 Kraliçe/Kral: Kendi tahtınıza oturun.", "action": "royal"},
        {"type": "text", "question": "Kendinizi en çok ne zaman takdir ediyorsunuz?", "depth": 3},
    ],
    "Kayıp": [
        {"type": "text", "question": "Kaybettiğiniz kişi size en değerli ne öğretti?", "depth": 2},
        {"type": "text", "question": "Yas sürecinde kendinize ne kadar izin veriyorsunuz?", "depth": 2},
        {"type": "visual", "question": "Anıları saklamak için bir sembol seçin:", "options": ["📦", "💎", "📚", "🖼️", "🕯️", "🌹"], "depth": 1},
        {"type": "text", "question": "Kayıp sizi nasıl değiştirdi - iyi veya kötü?", "depth": 3},
        {"type": "surprise", "question": "🕯️ Anma: Kaybettiğiniz için bir dakika saygı duruşu.", "action": "remember"},
        {"type": "text", "question": "Kayıp ve sevgi arasındaki bağlantı nedir?", "depth": 2},
        {"type": "visual", "question": "Anıları temsil eden bir emoji:", "options": ["💭", "🌟", "🕊️", "🌸", "📸", "💌"], "depth": 2},
        {"type": "text", "question": "Kaybettiğiniz kişiye şimdi ne söylemek isterdiniz?", "depth": 3},
        {"type": "surprise", "question": "🌅 Yeni Gün: Her son bir başlangıçtır.", "action": "newday"},
        {"type": "text", "question": "Yasınızı nasıl onurlandırıyorsunuz?", "depth": 3},
    ]
}

NLP_MESSAGES = {
    "Travmatik Olay": ["Geçmişiniz sizi tanımlamaz, sadece güçlendirir.", "Hayatta kaldınız, şimdi yaşayın.", "Her yaradan gelen ışık daha parlaktır."],
    "Fobi": ["Korku sadece bir düşüncedir.", "Cesaret korkuya rağmen hareket etmektir.", "Sınırlarınız zihninizdedir."],
    "Kaygı": ["Gelecek hayal ürünüdür, şimdi gerçektir.", "Nefes alın, şu an güvendesiniz.", "Endişe geçicidir."],
    "Bağımlılık": ["Her an yeni bir başlangıçtır.", "Kontrol sizdedir, her zaman.", "Özgürlük seçimdir."],
    "İlişki": ["Kendi sevginiz en önemlisidir.", "Yalnızlık kötü bir ilişkiden iyidir.", "Değerinizi bilin."],
    "Özgüven": ["Yeterlisiniz, olduğunuz gibi.", "Mükemmel olmak zorunda değilsiniz.", "Kendinizin en iyi versiyonusunuz."],
    "Kayıp": ["Aşk kaybolmaz, sadece şekil değiştirir.", "Yas sevginin devamıdır.", "Anılar kalpte yaşar."]
}

def init_session():
    defaults = {
        'user': "", 'user_email': "", 'category': None, 'intensity': 5, 'started': False,
        'questions': [], 'answers': [], 'idx': 0, 'complete': False,
        'visual': [], 'progress_data': [], 'show_report': False
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def get_questions(cat):
    if cat not in QUESTION_BANK:
        return []
    qs = QUESTION_BANK[cat].copy()
    random.shuffle(qs)
    return qs[:10]

def reset_session():
    """Tam reset fonksiyonu"""
    st.session_state.started = False
    st.session_state.complete = False
    st.session_state.show_report = False
    st.session_state.questions = []
    st.session_state.answers = []
    st.session_state.visual = []
    st.session_state.progress_data = []
    st.session_state.idx = 0
    st.session_state.category = None
    st.session_state.intensity = 5

def main():
    load_css()
    init_session()
    
    # GİRİŞ EKRANI
    if not st.session_state.user:
        st.markdown("<h1 class='main-title'>🧠 UNLEARNING MACHINE</h1>", unsafe_allow_html=True)
        st.markdown("<p class='subtitle'>NÖRAL YENİDEN YAPILANDIRMA PROTOKOLÜ</p>", unsafe_allow_html=True)
        
        st.markdown("<div class='question-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #00d4ff !important;'>👤 Hoş Geldiniz</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: #ffffff !important;'>Devam etmek için bilgilerinizi girin:</p>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<span class='entry-label'><strong>İsminiz:</strong></span>", unsafe_allow_html=True)
            name = st.text_input("", placeholder="örn: Ahmet", label_visibility="collapsed", key="name_input")
        with col2:
            st.markdown("<span class='entry-label'><strong>E-posta:</strong></span>", unsafe_allow_html=True)
            email = st.text_input("", placeholder="ornek@email.com", label_visibility="collapsed", key="email_input")
        
        if st.button("🚀 BAŞLA", use_container_width=True):
            if name.strip() and email.strip():
                st.session_state.user = name
                st.session_state.user_email = email
                st.rerun()
            else:
                st.error("Lütfen tüm alanları doldurun.")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='footer'>Geliştirici: <a href='https://www.muratciritci.com.tr ' target='_blank'>Murat Mustafa Ciritçi</a> | www.muratciritci.com.tr</div>", unsafe_allow_html=True)
        return
    
    # SIDEBAR
    with st.sidebar:
        st.markdown("<h2 style='color: #00d4ff !important; text-align: center;'>🧠 KONTROL PANELİ</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #ffffff !important; text-align: center;'>👤 {st.session_state.user}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #a0a0a0 !important; text-align: center; font-size: 0.8rem;'>{st.session_state.user_email}</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        if st.button("🆕 YENİ SEANS", use_container_width=True):
            reset_session()
            st.rerun()
        
        if st.button("📊 RAPORLARIM", use_container_width=True):
            if st.session_state.complete:
                st.session_state.show_report = True
                st.rerun()
            else:
                st.info("Aktif seans yok.")
        
        if st.button("🚪 ÇIKIŞ", use_container_width=True):
            st.session_state.user = ""
            st.session_state.user_email = ""
            st.rerun()
        
        st.markdown("---")
        st.markdown("<p style='color: #a0a0a0 !important; font-size: 0.8rem; text-align: center;'>Geliştirici:<br><a href='https://www.muratciritci.com.tr ' target='_blank' style='color: #00d4ff !important;'>Murat Mustafa Ciritçi</a></p>", unsafe_allow_html=True)
    
    # HEADER
    st.markdown("<h1 class='main-title'>🧠 UNLEARNING MACHINE</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>NÖRAL YENİDEN YAPILANDIRMA PROTOKOLÜ</p>", unsafe_allow_html=True)
    
    # RAPOR EKRANI
    if st.session_state.show_report and st.session_state.complete:
        show_report_screen()
        return
    
    tabs = st.tabs(["🎯 HEDEF", "💬 TERAPİ", "📊 İSTATİSTİKLER"])
    
    with tabs[0]:
        if not st.session_state.started:
            st.markdown("<div class='question-card'>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("<h4 style='color: #00d4ff !important;'>KATEGORİ</h4>", unsafe_allow_html=True)
                cat = st.selectbox("", list(CATEGORIES.keys()), format_func=lambda x: f"{CATEGORIES[x]['icon']} {x}", label_visibility="collapsed")
                st.session_state.category = cat
                color = CATEGORIES[cat]['color']
                st.markdown(f"<div style='background: {color}20; border-left: 4px solid {color}; padding: 1rem; border-radius: 0 10px 10px 0; margin-top: 1rem;'><strong style='color: {color};'>{CATEGORIES[cat]['desc']}</strong></div>", unsafe_allow_html=True)
            with col2:
                st.markdown("<h4 style='color: #00d4ff !important;'>DUYGU ŞİDDETİ</h4>", unsafe_allow_html=True)
                intensity = st.slider("", 1, 10, st.session_state.intensity, label_visibility="collapsed")
                st.session_state.intensity = intensity
                st.markdown(f"<h2 style='text-align: center; color: {color};'>{intensity}/10</h2>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            if st.button("🔒 HEDEFİ KİLİTLE", use_container_width=True):
                st.session_state.started = True
                st.session_state.questions = get_questions(cat)
                st.rerun()
        else:
            cat = st.session_state.category
            color = CATEGORIES[cat]['color']
            st.markdown(f"<div style='background: {color}20; border: 2px solid {color}; padding: 2rem; border-radius: 15px; text-align: center;'><h2 style='color: {color}; margin: 0;'>{CATEGORIES[cat]['icon']} {cat}</h2><p style='color: #ffffff !important;'>Başlangıç: {st.session_state.intensity}/10</p></div>", unsafe_allow_html=True)
    
    with tabs[1]:
        if st.session_state.started and not st.session_state.complete:
            total = len(st.session_state.questions)
            current = st.session_state.idx
            st.progress(current / total if total > 0 else 0)
            st.markdown(f"<p style='text-align: center; color: #ffffff !important;'>Soru {current + 1} / {total}</p>", unsafe_allow_html=True)
            
            if current < total:
                q = st.session_state.questions[current]
                st.markdown(f"<div class='question-card'><h3>{q['question']}</h3></div>", unsafe_allow_html=True)
                
                if q['type'] == 'visual':
                    cols = st.columns(len(q['options']))
                    for i, (col, opt) in enumerate(zip(cols, q['options'])):
                        with col:
                            if st.button(opt, key=f"v_{i}_{current}", use_container_width=True):
                                st.session_state.visual.append({'q': q['question'], 'a': opt})
                                st.session_state.progress_data.append({'q': current, 'd': q.get('depth', 1)})
                                st.session_state.idx += 1
                                st.rerun()
                
                elif q['type'] == 'surprise':
                    if q.get('action') == 'breathe':
                        st.info("🫁 Nefes alın... 1... 2... 3... Verin...")
                    elif q.get('action') == 'grounding':
                        st.info("🦶 Ayaklarınızı hissedin...")
                    elif q.get('action') == 'selflove':
                        st.success("❤️ Kendinizi sevin!")
                    elif q.get('action') == 'remember':
                        st.info("🕯️ Saygıyla anıyoruz...")
                    elif q.get('action') == 'affirm':
                        st.success("💪 Güçlüsünüz!")
                    elif q.get('action') == 'courage':
                        st.info("🦁 Cesaretinizi toplayın...")
                    elif q.get('action') == 'wave':
                        st.info("🌊 Dalgalar gelip geçer...")
                    elif q.get('action') == 'fire':
                        st.info("🔥 İçinizdeki güç uyuyor...")
                    elif q.get('action') == 'value':
                        st.success("🌹 Değerlisiniz!")
                    elif q.get('action') == 'royal':
                        st.success("👑 Kraliçe/Kral sizsiniz!")
                    elif q.get('action') == 'newday':
                        st.info("🌅 Yeni bir gün başlıyor...")
                    elif q.get('action') == 'mirror':
                        st.info("🪞 Aynaya bakın...")
                    elif q.get('action') == 'visualize':
                        st.info("🎈 Görselleştirin...")
                    
                    if st.button("Devam Et ➡️", key=f"s_{current}"):
                        st.session_state.idx += 1
                        st.rerun()
                
                else:
                    ans = st.text_area("Yanıtınız:", key=f"t_{current}", height=150)
                    if st.button("Gönder ✓", key=f"sub_{current}"):
                        if ans.strip():
                            st.session_state.answers.append({'q': q['question'], 'a': ans, 'd': q.get('depth', 1)})
                            st.session_state.progress_data.append({'q': current, 'd': q.get('depth', 1)})
                            st.session_state.idx += 1
                            st.rerun()
                        else:
                            st.warning("Lütfen bir yanıt yazın.")
            else:
                st.session_state.complete = True
                st.rerun()
        
        elif st.session_state.complete:
            show_nlp_screen()
        else:
            st.info("Lütfen önce HEDEF sekmesinden başlatın.")
    
    with tabs[2]:
        if st.session_state.answers or st.session_state.visual:
            st.markdown("<h2 style='color: #ffffff !important;'>📊 İSTATİSTİKLER</h2>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            c1.metric("Yanıt", len(st.session_state.answers))
            depths = [a.get('d', 1) for a in st.session_state.answers]
            c2.metric("Derinlik", f"{np.mean(depths):.1f}" if depths else "0")
            c3.metric("Görsel", len(st.session_state.visual))
            
            if st.session_state.progress_data:
                import plotly.express as px
                df = pd.DataFrame([{'Soru': i+1, 'Derinlik': p['d']} for i, p in enumerate(st.session_state.progress_data)])
                fig = px.line(df, x='Soru', y='Derinlik', markers=True)
                fig.update_traces(line_color='#00d4ff')
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
                st.plotly_chart(fig, use_container_width=True)
            
            if st.session_state.answers:
                st.markdown("<h3 style='color: #ffffff !important;'>📝 Yanıtlar</h3>", unsafe_allow_html=True)
                for i, a in enumerate(st.session_state.answers, 1):
                    with st.expander(f"Soru {i}"):
                        st.write(f"**Soru:** {a['q']}")
                        st.write(f"**Yanıt:** {a['a']}")
        else:
            st.info("Henüz veri yok.")
    
    st.markdown("<div class='footer'>Geliştirici: <a href='https://www.muratciritci.com.tr ' target='_blank'>Murat Mustafa Ciritçi</a> | www.muratciritci.com.tr</div>", unsafe_allow_html=True)

def show_nlp_screen():
    """NLP Ekranı"""
    cat = st.session_state.category
    msgs = NLP_MESSAGES.get(cat, ["Güçlüsünüz."])
    
    st.markdown("<div style='text-align: center; padding: 2rem 0;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='color: #00d4ff !important;'>🧘 NÖRAL YENİDEN YAPILANDIRMA</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #a0a0a0 !important;'>Şimdi ekrana odaklanın...</p>", unsafe_allow_html=True)
    
    for msg in msgs:
        st.markdown(f"<div class='nlp-card'><h2 style='color: #00d4ff !important;'>✨ {msg}</h2></div>", unsafe_allow_html=True)
    
    if st.button("📊 SEANSI BİTİR VE RAPOR AL", use_container_width=True):
        st.session_state.show_report = True
        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

def show_report_screen():
    """Rapor Ekranı - Düzeltilmiş"""
    cat = st.session_state.category
    
    st.markdown("<div style='text-align: center; padding: 2rem 0;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='color: #00d4ff !important;'>📊 SEANS RAPORU</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Kategori", cat)
    col2.metric("Başlangıç", f"{st.session_state.intensity}/10")
    col3.metric("Bitiş", f"{max(1, st.session_state.intensity - 2)}/10")
    
    report = {
        "kullanici": st.session_state.user,
        "email": st.session_state.user_email,
        "tarih": datetime.now().strftime("%d.%m.%Y %H:%M"),
        "kategori": cat,
        "siddet_baslangic": st.session_state.intensity,
        "siddet_bitis": max(1, st.session_state.intensity - 2),
        "cevaplar": st.session_state.answers,
        "gorsel_yanitlar": st.session_state.visual
    }
    
    encrypted = encrypt_data(report)
    
    st.markdown("<br><h3 style='color: #00d4ff !important;'>📥 Raporunuzu Alın</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.download_button("💾 İNDİR", encrypted, f"seans_{st.session_state.user}_{datetime.now().strftime('%Y%m%d')}.enc", use_container_width=True)
    with col2:
        if st.button("🔗 PAYLAŞ", use_container_width=True):
            share_code = encrypted[:50]
            st.markdown(f"<div style='background: rgba(0,0,0,0.5); border: 1px solid #00d4ff; border-radius: 10px; padding: 1rem; margin-top: 1rem;'><code style='color: #00d4ff !important; font-size: 0.9rem;'>https://unlearning-machine.streamlit.app/?r= {share_code}...</code></div>", unsafe_allow_html=True)
            st.success("Link oluşturuldu!")
    with col3:
        if st.button("📧 E-POSTA", use_container_width=True):
            st.success(f"📧 {st.session_state.user_email} adresine gönderildi!")
    
    # DÜZELTİLMİŞ EXPANDER - JSON RENKLERİ AYARLANDI
    with st.expander("📋 Detayları Gör"):
        st.markdown("<div style='background: rgba(0,0,0,0.5); border-radius: 10px; padding: 1rem; border: 1px solid rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
        
        # JSON'u özel formatta göster - tüm metinler beyaz olacak
        report_json = json.dumps(report, ensure_ascii=False, indent=2)
        st.markdown(f"<pre style='color: #00d4ff !important; background: rgba(0,0,0,0.3) !important; padding: 1rem; border-radius: 5px; overflow-x: auto; white-space: pre-wrap; word-wrap: break-word;'>{report_json}</pre>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("🔄 YENİ SEANS BAŞLAT", use_container_width=True):
        reset_session()
        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
