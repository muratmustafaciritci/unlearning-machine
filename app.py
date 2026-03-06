import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import random
import json
import base64
from io import BytesIO

st.set_page_config(page_title="Unlearning Machine", page_icon="🧠", layout="wide")

# CSS
def load_css():
    st.markdown("""
    <style>
    .main-title { text-align: center; background: linear-gradient(90deg, #00d4ff, #7b2cbf); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3rem; font-weight: 700; }
    .stButton>button { background: linear-gradient(90deg, #ff006e, #8338ec); color: white; border-radius: 10px; border: none; padding: 0.75rem; width: 100%; }
    .question-card { background: rgba(255,255,255,0.05); border-radius: 15px; padding: 2rem; border: 1px solid rgba(255,255,255,0.1); }
    .positive-message { background: linear-gradient(135deg, rgba(0,212,255,0.2), rgba(123,44,191,0.2)); border-left: 4px solid #00d4ff; padding: 1.5rem; border-radius: 0 15px 15px 0; }
    </style>
    """, unsafe_allow_html=True)

CATEGORIES = {
    "Travmatik Olay": {"color": "#FF4757", "icon": "💥"},
    "Fobi": {"color": "#FF6348", "icon": "😰"},
    "Kaygı": {"color": "#FFA502", "icon": "😰"},
    "Bağımlılık": {"color": "#2ED573", "icon": "🔄"},
    "İlişki": {"color": "#1E90FF", "icon": "💔"},
    "Özgüven": {"color": "#A55EEA", "icon": "🪞"},
    "Kayıp": {"color": "#747D8C", "icon": "🕯️"}
}

QUESTIONS = {
    "Travmatik Olay": [
        {"q": "Bu olayı ilk hatırladığınızda bedeninizde nerede hissediyorsunuz?", "type": "text", "depth": 1},
        {"q": "O anki düşünceniz şimdi gerçekçi mi görünüyor?", "type": "text", "depth": 2},
        {"q": "Şu anki duygusal durumunuzu seçin:", "type": "visual", "options": ["😢", "😠", "😨", "😔", "😐", "😌"], "depth": 1},
        {"q": "🌊 Mola: Derin nefes alın ve 3 saniye tutun.", "type": "surprise", "action": "breathe"},
        {"q": "Bu travmayı bir kitap olsa başlığı ne olurdu?", "type": "text", "depth": 2},
    ],
    "Fobi": [
        {"q": "Bu korku size ne zaman mantıklı geldi?", "type": "text", "depth": 1},
        {"q": "Korkunuzu bir hava durumu olarak seçin:", "type": "visual", "options": ["🌪️", "⛈️", "🌧️", "⛅", "🌤️", "☀️"], "depth": 2},
        {"q": "🎲 Sürpriz: Gözlerinizi kapatın, korkunuzu balon gibi uçurun.", "type": "surprise", "action": "visualize"},
        {"q": "Bu fobi olmasaydı hayatınızda ne değişirdi?", "type": "text", "depth": 3},
    ],
    "Kaygı": [
        {"q": "Endişelendiğiniz şey gerçekleşti mi daha önce?", "type": "text", "depth": 1},
        {"q": "Kaygınızı bir renk olarak seçin:", "type": "visual", "options": ["⚫", "🔴", "🟠", "🟡", "🔵", "⚪"], "depth": 1},
        {"q": "🧘 An: Şu an burada, şu an güvendesiniz.", "type": "surprise", "action": "grounding"},
        {"q": "Bu düşünce size hizmet ediyor mu?", "type": "text", "depth": 3},
    ],
    "Bağımlılık": [
        {"q": "Bu davranış size ilk ne hissettirdi?", "type": "text", "depth": 1},
        {"q": "Özgür hissettiğiniz bir anı seçin:", "type": "visual", "options": ["🕊️", "🦅", "🌊", "🏔️", "🌅", "🌲"], "depth": 2},
        {"q": "💪 Güç Anı: Bugün kendinizle gurur duyduğunuz bir şey?", "type": "surprise", "action": "affirm"},
        {"q": "Kontrolü kaybettiğinizde kendinize ne söylüyorsunuz?", "type": "text", "depth": 2},
    ],
    "İlişki": [
        {"q": "Bu ilişkide kendi sınırlarınızı nasıl çizdiniz?", "type": "text", "depth": 2},
        {"q": "Sağlıklı ilişkiyi temsil eden görsel:", "type": "visual", "options": ["🤝", "💝", "🌉", "🏡", "🌱", "⚖️"], "depth": 2},
        {"q": "❤️ Kendi Sevginiz: Kendinize nezaketle davrandınız mı?", "type": "surprise", "action": "selflove"},
        {"q": "Ayrılık acısı mı yoksa kalma acısı mı daha zor?", "type": "text", "depth": 2},
    ],
    "Özgüven": [
        {"q": "Kendinizi en son ne zaman yeterli hissettiniz?", "type": "text", "depth": 1},
        {"q": "Güçlü hissettiğiniz bir anı seçin:", "type": "visual", "options": ["💪", "👑", "🦁", "🔥", "⭐", "🎯"], "depth": 2},
        {"q": "🌟 Yıldız Anı: Aynaya bakın ve kendinize gülümseyin.", "type": "surprise", "action": "mirror"},
        {"q": "Kendinizi eleştirdiğinizde bunu arkadaşınıza söyler miydiniz?", "type": "text", "depth": 2},
    ],
    "Kayıp": [
        {"q": "Kaybettiğiniz kişi size en değerli ne öğretti?", "type": "text", "depth": 2},
        {"q": "Anıları saklamak için bir sembol seçin:", "type": "visual", "options": ["📦", "💎", "📚", "🖼️", "🕯️", "🌹"], "depth": 1},
        {"q": "🕯️ Anma: Kaybettiğiniz için bir dakika saygı duruşu.", "type": "surprise", "action": "remember"},
        {"q": "Kayıp sizi nasıl değiştirdi?", "type": "text", "depth": 3},
    ]
}

NLP_MSG = {
    "Travmatik Olay": ["Geçmişiniz sizi tanımlamaz, sadece güçlendirir.", "Hayatta kaldınız, şimdi yaşayın."],
    "Fobi": ["Korku sadece bir düşüncedir.", "Cesaret korkuya rağmen hareket etmektir."],
    "Kaygı": ["Gelecek hayal ürünüdür, şimdi gerçektir.", "Nefes alın, şu an güvendesiniz."],
    "Bağımlılık": ["Her an yeni bir başlangıçtır.", "Kontrol sizdedir, her zaman."],
    "İlişki": ["Kendi sevginiz en önemlisidir.", "Yalnızlık kötü bir ilişkiden iyidir."],
    "Özgüven": ["Yeterlisiniz, olduğunuz gibi.", "Mükemmel olmak zorunda değilsiniz."],
    "Kayıp": ["Aşk kaybolmaz, sadece şekil değiştirir.", "Anılar kalpte yaşar."]
}

def init_session():
    defaults = {
        'user': "", 'category': None, 'intensity': 5, 'started': False,
        'questions': [], 'answers': [], 'idx': 0, 'complete': False,
        'visual': []
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def get_questions(cat):
    if cat not in QUESTIONS:
        return []
    qs = QUESTIONS[cat].copy()
    random.shuffle(qs)
    return qs[:4]

def main():
    load_css()
    init_session()

    # Sidebar
    with st.sidebar:
        st.markdown("<h2>🧠 KONTROL PANELİ</h2>", unsafe_allow_html=True)
        if not st.session_state.user:
            st.session_state.user = st.text_input("👤 İsim", value="Ziyaretçi")
        else:
            st.write(f"👤 {st.session_state.user}")
        st.markdown("---")
        if st.button("🆕 YENİ SEANS", use_container_width=True):
            for k in ['started', 'complete', 'questions', 'answers', 'idx', 'visual']:
                st.session_state[k] = False if k in ['started', 'complete'] else ([] if k != 'idx' else 0)
            st.rerun()
        if st.button("📊 RAPORLARIM", use_container_width=True):
            st.info("Seans sonunda rapor oluşturulur.")

    # Header
    st.markdown("<h1 class='main-title'>🧠 UNLEARNING MACHINE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #a0a0a0;'>NÖRAL YENİDEN YAPILANDIRMA PROTOKOLÜ</p>", unsafe_allow_html=True)

    tabs = st.tabs(["🎯 HEDEF", "💬 TERAPİ", "📊 İSTATİSTİKLER"])

    with tabs[0]:
        if not st.session_state.started:
            st.markdown("<div class='question-card'>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                cat = st.selectbox("KATEGORİ", list(CATEGORIES.keys()),
                                 format_func=lambda x: f"{CATEGORIES[x]['icon']} {x}")
                st.session_state.category = cat
                color = CATEGORIES[cat]['color']
                st.markdown(f"<div style='color: {color}; font-weight: bold; padding: 10px; border-left: 4px solid {color};'>{cat}</div>", unsafe_allow_html=True)
            with col2:
                intensity = st.slider("DUYGU ŞİDDETİ (1-10)", 1, 10, st.session_state.intensity)
                st.session_state.intensity = intensity
                st.markdown(f"<h3 style='text-align: center; color: {color};'>{intensity}/10</h3>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            if st.button("🔒 HEDEFİ KİLİTLE", use_container_width=True):
                st.session_state.started = True
                st.session_state.questions = get_questions(cat)
                st.rerun()
        else:
            cat = st.session_state.category
            color = CATEGORIES[cat]['color']
            st.markdown(f"<div style='background: {color}20; border: 2px solid {color}; padding: 2rem; border-radius: 15px; text-align: center;'><h2 style='color: {color};'>{CATEGORIES[cat]['icon']} {cat}</h2><p>Başlangıç: {st.session_state.intensity}/10</p></div>", unsafe_allow_html=True)

    with tabs[1]:
        if st.session_state.started and not st.session_state.complete:
            total = len(st.session_state.questions)
            current = st.session_state.idx
            st.progress(current / total if total > 0 else 0)
            st.write(f"Soru {current + 1} / {total}")

            if current < total:
                q = st.session_state.questions[current]
                st.markdown(f"<div class='question-card'><h3>{q['q']}</h3></div>", unsafe_allow_html=True)

                if q['type'] == 'visual':
                    cols = st.columns(len(q['options']))
                    for i, (col, opt) in enumerate(zip(cols, q['options'])):
                        with col:
                            if st.button(opt, key=f"v_{i}_{current}", use_container_width=True):
                                st.session_state.visual.append({'q': q['q'], 'a': opt})
                                st.session_state.idx += 1
                                st.rerun()

                elif q['type'] == 'surprise':
                    st.info(f"🎯 Eylem: {q.get('action', 'nefes')}")
                    if st.button("Devam Et ➡️", key=f"s_{current}"):
                        st.session_state.idx += 1
                        st.rerun()

                else:
                    ans = st.text_area("Yanıtınız:", key=f"t_{current}", height=100)
                    if st.button("Gönder ✓", key=f"sub_{current}"):
                        if ans.strip():
                            st.session_state.answers.append({'q': q['q'], 'a': ans, 'd': q.get('depth', 1)})
                            st.session_state.idx += 1
                            st.rerun()
                        else:
                            st.warning("Yanıt yazın.")
            else:
                st.session_state.complete = True
                st.rerun()

        elif st.session_state.complete:
            cat = st.session_state.category
            msgs = NLP_MSG.get(cat, ["Güçlüsünüz."])
            st.markdown("<h1 style='text-align: center;'>🧘 NÖRAL YENİDEN YAPILANDIRMA</h1>", unsafe_allow_html=True)
            for msg in msgs:
                st.markdown(f"<div class='positive-message'><h3>✨ {msg}</h3></div>", unsafe_allow_html=True)
            st.markdown("<div style='text-align: center; font-size: 4rem; margin: 2rem 0;'>🌅</div>", unsafe_allow_html=True)

            # Rapor indirme
            report = {
                "tarih": datetime.now().strftime("%d.%m.%Y %H:%M"),
                "kategori": cat,
                "siddet": st.session_state.intensity,
                "cevaplar": st.session_state.answers,
                "gorsel": st.session_state.visual
            }
            col1, col2 = st.columns(2)
            with col1:
                st.download_button("📄 JSON İndir", json.dumps(report, ensure_ascii=False), 
                                 f"seans_{datetime.now().strftime('%Y%m%d')}.json")
            with col2:
                if st.button("🔗 Paylaş"):
                    st.success("Anonim link oluşturuldu!")

            if st.button("🔄 Yeni Seans", use_container_width=True):
                st.session_state.started = False
                st.session_state.complete = False
                st.session_state.questions = []
                st.session_state.answers = []
                st.session_state.idx = 0
                st.rerun()
        else:
            st.info("HEDEF sekmesinden başlatın.")

    with tabs[2]:
        if st.session_state.answers or st.session_state.visual:
            st.markdown("<h2>📊 İSTATİSTİKLER</h2>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            c1.metric("Yanıt Sayısı", len(st.session_state.answers))
            depths = [a.get('d', 1) for a in st.session_state.answers]
            c2.metric("Ort. Derinlik", f"{np.mean(depths):.1f}" if depths else "0")
            c3.metric("Görsel Yanıt", len(st.session_state.visual))

            if st.session_state.answers:
                df = pd.DataFrame([{'Soru': i+1, 'Derinlik': a.get('d', 1)} for i, a in enumerate(st.session_state.answers)])
                import plotly.express as px
                fig = px.bar(df, x='Soru', y='Derinlik', title='Soru Derinliği', color='Derinlik')
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
                st.plotly_chart(fig, use_container_width=True)

            st.markdown("<h3>📝 Yanıtlar</h3>", unsafe_allow_html=True)
            for i, a in enumerate(st.session_state.answers[:3], 1):
                with st.expander(f"Soru {i}"):
                    st.write(f"**{a['q']}**")
                    st.write(a['a'])
        else:
            st.info("Henüz veri yok.")

if __name__ == "__main__":
    main()
