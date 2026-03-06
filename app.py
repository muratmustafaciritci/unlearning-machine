def load_css():
    st.markdown("""
    <style>
    /* TEMEL ARKAPLAN */
    .stApp { 
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a3e 50%, #16213e 100%); 
    }
    
    /* SIDEBAR */
    [data-testid="stSidebar"] { 
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%) !important; 
    }
    [data-testid="stSidebar"] * { 
        color: #ffffff !important; 
    }
    
    /* TÜM YAZILAR */
    .stApp, .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
    .stApp span, .stApp div {
        color: #ffffff !important;
    }
    
    /* LABEL'LAR - EN ÖNEMLİ KISIM */
    label, .stTextInput label, .stTextArea label, 
    [data-testid="stWidgetLabel"], [data-baseweb="label"],
    .css-1n76uvr, .css-81oif8, .css-16huue1, .css-qrbaxs {
        color: #00d4ff !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
    }
    
    /* BAŞLIK */
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: #00d4ff !important;
        text-shadow: 0 0 30px rgba(0, 212, 255, 0.5);
    }
    .subtitle {
        text-align: center;
        color: #a0a0a0 !important;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* INPUT ALANLARI */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background: rgba(0,0,0,0.3) !important;
        color: #ffffff !important;
        border: 1px solid rgba(0,212,255,0.3) !important;
        border-radius: 10px !important;
    }
    ::placeholder {
        color: rgba(255,255,255,0.4) !important;
    }
    
    /* SELECTBOX */
    .stSelectbox>div>div {
        background: rgba(0,0,0,0.3) !important;
        color: #ffffff !important;
        border-radius: 10px !important;
    }
    
    /* BUTONLAR */
    .stButton>button {
        background: linear-gradient(90deg, #ff006e, #8338ec) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem !important;
        width: 100% !important;
        font-weight: 600 !important;
    }
    
    /* KARTLAR */
    .question-card {
        background: rgba(0,0,0,0.3) !important;
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(0,212,255,0.2);
    }
    .question-card h3, .question-card h4 {
        color: #ffffff !important;
    }
    
    /* NLP KART */
    .nlp-card {
        background: linear-gradient(135deg, rgba(0,212,255,0.1), rgba(123,44,191,0.1));
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        border: 1px solid rgba(0,212,255,0.3);
        margin: 1rem 0;
    }
    
    /* SEKMELER */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background: rgba(0,0,0,0.2);
        padding: 1rem;
        border-radius: 15px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #ffffff !important;
    }
    
    /* EXPANDER - DÜZELTİLMİŞ */
    [data-testid="stExpander"] {
        border: none !important;
    }
    [data-testid="stExpander"] summary {
        background: rgba(0,0,0,0.3) !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        padding: 0.75rem 1rem !important;
        border: 1px solid rgba(0,212,255,0.2) !important;
    }
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] {
        background: rgba(0,0,0,0.5) !important;
        border-radius: 0 0 10px 10px !important;
        padding: 1rem !important;
        border: 1px solid rgba(0,212,255,0.2) !important;
        border-top: none !important;
    }
    [data-testid="stExpanderDetails"] * {
        color: #ffffff !important;
    }
    
    /* JSON */
    [data-testid="stJson"], .stJson {
        background: rgba(0,0,0,0.5) !important;
        color: #00d4ff !important;
    }
    
    /* CODE BLOK */
    code {
        color: #00d4ff !important;
        background: rgba(0,0,0,0.5) !important;
        padding: 0.2rem 0.4rem !important;
        border-radius: 5px !important;
    }
    
    /* FOOTER */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: rgba(0,0,0,0.7);
        color: #a0a0a0 !important;
        text-align: center;
        padding: 1rem;
        font-size: 0.9rem;
        z-index: 1000;
    }
    .footer a {
        color: #00d4ff !important;
        text-decoration: none;
    }
    </style>
    """, unsafe_allow_html=True)
