import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import os
import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlretrieve
from theme import inject_theme, render_nav, format_inr, GOLD

FURNISHING_OPTIONS = {
    "Unfurnished": "unfurnished",
    "Semi-furnished": "semifurnished",
    "Furnished": "furnished",
}

st.set_page_config(
    page_title="Aurea · Valuation Engine",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_theme()
render_nav(active="valuation")

# Component Styles — Hyper-luxury overhaul
st.markdown("""
<style>
    /* ====== BUTTON: PREMIUM GOLD ====== */
    .stButton>button {
        position: relative;
        background: transparent;
        color: #D4AF37;
        border: 1px solid rgba(212,175,55,0.5);
        border-radius: 10px;
        text-transform: uppercase;
        letter-spacing: 3px;
        font-family: 'Montserrat', sans-serif;
        font-weight: 600;
        font-size: 0.9rem;
        padding: 1.1rem 2.5rem;
        transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        width: 100%;
        overflow: hidden;
        backdrop-filter: blur(8px);
    }
    .stButton>button::before {
        content: '';
        position: absolute;
        top: 0; left: -100%;
        width: 100%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(212,175,55,0.15), rgba(255,246,218,0.1), transparent);
        transition: left 0.6s ease;
    }
    .stButton>button:hover::before {
        left: 100%;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #D4AF37 0%, #FFF6DA 50%, #D4AF37 100%);
        color: #050505;
        border-color: #D4AF37;
        box-shadow: 0 0 30px rgba(212,175,55,0.3), 0 0 60px rgba(212,175,55,0.1), inset 0 0 20px rgba(255,246,218,0.1);
        transform: translateY(-2px);
        letter-spacing: 4px;
    }
    .stButton>button:active {
        transform: translateY(1px) scale(0.98);
        box-shadow: 0 0 15px rgba(212,175,55,0.2);
    }

    /* ====== FINAL VALUATION: ULTRA PREMIUM ====== */
    @keyframes borderBreath {
        0%, 100% { border-color: rgba(212,175,55,0.25); }
        50% { border-color: rgba(212,175,55,0.6); }
    }
    @keyframes innerAurora {
        0%, 100% { box-shadow: inset 0 0 40px rgba(212,175,55,0.03), 0 20px 60px rgba(0,0,0,0.7); }
        50% { box-shadow: inset 0 0 80px rgba(212,175,55,0.07), 0 25px 70px rgba(0,0,0,0.6); }
    }
    @keyframes goldTextShift {
        0% { background-position: 0% center; }
        100% { background-position: 200% center; }
    }
    @keyframes valReveal {
        0% { opacity: 0; transform: scale(0.8) translateY(20px); filter: blur(10px); }
        100% { opacity: 1; transform: scale(1) translateY(0); filter: blur(0); }
    }

    .final-valuation {
        position: relative;
        background: linear-gradient(180deg, rgba(22,22,28,0.95) 0%, rgba(8,8,12,0.97) 100%);
        border: 1px solid rgba(212,175,55,0.3);
        padding: 5rem 2rem;
        border-radius: 24px;
        text-align: center;
        margin-top: 2.5rem;
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        overflow: hidden;
        animation: borderBreath 4s ease-in-out infinite, innerAurora 6s ease-in-out infinite, valReveal 1s cubic-bezier(0.22,0.61,0.36,1) forwards;
    }
    .final-valuation::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent 10%, rgba(212,175,55,0.5) 50%, transparent 90%);
    }
    .final-valuation::after {
        content: '';
        position: absolute;
        top: -50%; left: -50%;
        width: 200%; height: 200%;
        background: radial-gradient(circle at 50% 50%, rgba(212,175,55,0.03) 0%, transparent 50%);
        pointer-events: none;
    }
    .final-valuation .ornament {
        color: rgba(212,175,55,0.4);
        font-size: 1.2rem;
        letter-spacing: 12px;
        margin: 0.8rem 0;
    }
    .final-valuation .lbl {
        color: #B5B0A5;
        text-transform: uppercase;
        letter-spacing: 5px;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    .final-valuation .val {
        font-family: 'Cinzel', serif;
        font-size: 5.5rem;
        margin: 0.5rem 0;
        background: linear-gradient(90deg, #8C6E24, #D4AF37, #FFF6DA, #D4AF37, #8C6E24);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: goldTextShift 4s linear infinite;
        filter: drop-shadow(0 4px 25px rgba(212,175,55,0.3));
    }
    .final-valuation .val-sub {
        color: #A8A8A8;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-top: 1rem;
    }

    /* ====== SECTION DIVIDER ====== */
    @keyframes dividerGlow {
        0%, 100% { opacity: 0.5; text-shadow: 0 0 8px rgba(212,175,55,0.3); }
        50% { opacity: 1; text-shadow: 0 0 20px rgba(212,175,55,0.6), 0 0 40px rgba(212,175,55,0.2); }
    }
    .section-divider {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 16px;
        margin: 2.5rem 0;
    }
    .section-divider::before,
    .section-divider::after {
        content: '';
        flex: 1;
        max-width: 200px;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(212,175,55,0.4), transparent);
    }
    .section-divider .diamond {
        color: #D4AF37;
        font-size: 0.9rem;
        animation: dividerGlow 4s ease-in-out infinite;
    }

    /* ====== HERO OVERLAY ====== */
    .hero-overlay {
        position: relative;
        margin-top: -6px;
        padding: 1.5rem 2rem;
        background: linear-gradient(180deg, rgba(11,11,13,0) 0%, rgba(11,11,13,0.95) 100%);
        text-align: center;
    }
    .hero-overlay .watermark {
        font-family: 'Cinzel', serif;
        font-size: 0.7rem;
        letter-spacing: 8px;
        text-transform: uppercase;
        color: rgba(212,175,55,2);
    }

    /* ====== CHART GLASS PANEL ====== */
    .chart-glass-panel {
        background: linear-gradient(145deg, rgba(18,18,24,0.5) 0%, rgba(10,10,14,0.6) 100%);
        border: 1px solid rgba(212,175,55,0.1);
        border-radius: 16px;
        padding: 1.5rem;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        transition: border-color 0.4s ease, box-shadow 0.4s ease;
    }
    .chart-glass-panel:hover {
        border-color: rgba(212,175,55,0.25);
        box-shadow: 0 12px 40px rgba(212,175,55,0.05), 0 8px 32px rgba(0,0,0,0.4);
    }
    
    /* ====== PLOTLY CHART GLASS CARD ====== */
    div[data-testid="stPlotlyChart"] {background: linear-gradient(145deg,rgba(18,18,24,0.55) 0%,rgba(10,10,14,0.65) 100%);
        border: 1px solid rgba(212,175,55,0.15);
        border-radius: 10px;
        padding: 5px;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        box-shadow:0 10px 35px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.03);
    }

    div[data-testid="stPlotlyChart"]:hover {
        border-color: rgba(212,175,55,0.35);
        box-shadow:0 15px 45px rgba(212,175,55,0.08),0 10px 35px rgba(0,0,0,0.45);
    }

    /* ====== ANIMATED FOOTER ====== */
    @keyframes footerLineGlow {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    .lux-footer {
        margin-top: 100px;
        padding-top: 40px;
        border-top: 1px solid transparent;
        border-image: linear-gradient(90deg, transparent, rgba(212,175,55,0.4), rgba(212,175,55,0.6), rgba(212,175,55,0.4), transparent) 1;
        display: flex;
        justify-content: space-between;
        color: var(--mute);
        font-size: 0.75rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        position: relative;
    }
    .lux-footer::before {
        content: '';
        position: absolute;
        top: -1px; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, #D4AF37, transparent);
        background-size: 200% 100%;
        animation: footerLineGlow 6s linear infinite;
        opacity: 0.5;
    }

    /* ====== STAGGER METRIC COLUMNS ====== */
    [data-testid="stHorizontalBlock"] > div:nth-child(1) .lux-metric {
        animation-delay: 0.1s;
    }
    [data-testid="stHorizontalBlock"] > div:nth-child(2) .lux-metric {
        animation-delay: 0.3s;
    }
    [data-testid="stHorizontalBlock"] > div:nth-child(3) .lux-metric {
        animation-delay: 0.5s;
    }
</style>
""", unsafe_allow_html=True)

# Display Hero Image
try:
    from PIL import Image
    img = Image.open('assets/hero_banner.jpg')
    st.image(img, use_container_width=True)
    # Hero overlay
    st.markdown("""
    <div class="hero-overlay">
        <div class="watermark">AUREA ESTATES · PRIVATE VALUATION ATELIER</div>
    </div>
    """, unsafe_allow_html=True)
except Exception:
    pass

st.markdown('<div class="animated-section">', unsafe_allow_html=True)

# ---- DASHBOARD SECTION ----
st.markdown('<div style="height: 40px"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-eyebrow">Market Overview</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">The <em>Portfolio</em>.</div>', unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv('data/processed/gurgaon_properties_post_feature_selection_v2.csv')

@st.cache_resource
def load_model():
    model_path = Path('models/pipeline.pkl')

    if not model_path.exists():
        model_url = os.getenv('MODEL_URL')
        if not model_url:
            try:
                model_url = st.secrets.get('MODEL_URL')
            except Exception:
                model_url = None

        if not model_url:
            st.error(
                "Model file is missing. Add MODEL_URL in your deployment secrets "
                "or place models/pipeline.pkl in the models folder."
            )
            st.stop()

        model_path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = model_path.with_suffix('.pkl.download')
        with st.spinner('Downloading valuation model...'):
            urlretrieve(model_url, temp_path)
            temp_path.replace(model_path)

    with model_path.open('rb') as f:
        return pickle.load(f)

try:
    df = load_data()
    pipeline = load_model()
    
    # KPIs
    median_price = df['price'].median()
    total_listings = len(df)
    avg_area = df['built_up_area'].median()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="lux-metric">
            <div class="lbl">Median Portfolio Value</div>
            <div class="val">{format_inr(median_price)}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="lux-metric">
            <div class="lbl">Curated Properties</div>
            <div class="val">{total_listings:,}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="lux-metric">
            <div class="lbl">Average Footprint</div>
            <div class="val">{avg_area:,.0f} <span style="font-size: 1.2rem; color: #888;">sq.ft</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div style="height: 50px"></div>', unsafe_allow_html=True)
    
    # Chart inside glass panel
    # st.markdown('<div class="chart-glass-panel">', unsafe_allow_html=True)
   #fig = px.scatter(
   #    df.sample(min(800, len(df)), random_state=42), 
   #    x="built_up_area", y="price", 
   #    color_discrete_sequence=[GOLD],
   #    opacity=0.6
   #)
   #fig.update_layout(
   #    height = 300,
   #    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
   #    font=dict(family="Inter", color="#888888"),
   #    margin=dict(l=0, r=0, t=10, b=0),
   #    xaxis=dict(title="Built-up Area (sq.ft)", gridcolor="rgba(212,175,55,0.05)", zeroline=False),
   #    yaxis=dict(title="Price (Cr)", gridcolor="rgba(212,175,55,0.05)", zeroline=False),
   #    title=dict(text="Market Distribution", font=dict(family="Cinzel", color="#D4AF37", size=24))
   #)
   #fig.update_traces(marker=dict(size=8, line=dict(width=0)))
   #st.plotly_chart(fig,use_container_width=True,config={"displayModeBar": False})
    # st.markdown('</div>', unsafe_allow_html=True)"""
    
    # Ornamental divider
    st.markdown("""
    <div class="section-divider">
        <span class="diamond">◈</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div style="height: 30px"></div>', unsafe_allow_html=True)
    
    # ---- VALUATION ENGINE SECTION ----
    st.markdown('<div class="section-eyebrow">Valuation Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Determine <em>Value</em>.</div>', unsafe_allow_html=True)
    st.markdown('<p class="muted" style="margin-top:-10px; max-width:720px; margin-bottom: 40px;">'
                'Specify the exact parameters of the asset. Our algorithmic engine will benchmark it against the portfolio to determine the most defensible market price.</p>',
                unsafe_allow_html=True)
    
    # Form inside glass panel
    st.markdown('<div class="glass-form-panel">', unsafe_allow_html=True)
    with st.container():
        c1, c2, c3 = st.columns(3, gap="large")
        
        with c1:
            property_type = st.selectbox('Property Type', sorted(df['property_type'].unique()))
            sector = st.selectbox('Sector Location', sorted(df['sector'].unique()))
            bedRoom = st.selectbox('Bedrooms', sorted(df['bedRoom'].unique()))
            bathroom = st.selectbox('Bathrooms', sorted(df['bathroom'].unique()))
            
        with c2:
            balcony = st.selectbox('Balconies', sorted(df['balcony'].unique()))
            agePossession = st.selectbox('Age / Possession', sorted(df['agePossession'].unique()))
            built_up_area = st.number_input('Built-up Area (sq. ft.)', min_value=100.0, max_value=20000.0, value=1500.0, step=50.0)
            servant_room = st.selectbox('Servant Room', [0.0, 1.0], format_func=lambda x: "Available" if x == 1.0 else "None")
            
        with c3:
            store_room = st.selectbox('Store Room', [0.0, 1.0], format_func=lambda x: "Available" if x == 1.0 else "None")
            furnishing_label = st.selectbox('Furnishing Type', list(FURNISHING_OPTIONS.keys()))
            furnishing_type = FURNISHING_OPTIONS[furnishing_label]
            luxury_category = st.selectbox('Luxury Category', sorted(df['luxury_category'].unique()))
            floor_category = st.selectbox('Floor Category', sorted(df['floor_category'].unique()))
    st.markdown('</div>', unsafe_allow_html=True)
            
    st.markdown('<div style="height: 30px"></div>', unsafe_allow_html=True)
    
    _, btn_col, _ = st.columns([1, 1, 1])
    with btn_col:
        predict_clicked = st.button('Execute Valuation')
    
    if predict_clicked:
        input_data = pd.DataFrame([[
            property_type, sector, bedRoom, bathroom, balcony, agePossession, 
            built_up_area, servant_room, store_room, furnishing_type, 
            luxury_category, floor_category
        ]], columns=[
            'property_type', 'sector', 'bedRoom', 'bathroom', 'balcony', 'agePossession', 
            'built_up_area', 'servant room', 'store room', 'furnishing_type', 
            'luxury_category', 'floor_category'
        ])
        
        with st.spinner("Consulting the oracle..."):
            import time
            time.sleep(1) # Add a slight delay for dramatic effect
            predicted_price = pipeline.predict(input_data)[0]
            formatted_price = format_inr(predicted_price)
            
            st.markdown(f"""
            <div class="final-valuation">
                <div class="ornament">◈ ◈ ◈</div>
                <div class="lbl">Estimated Market Value</div>
                <div class="val">{formatted_price}</div>
                <div class="ornament">◈ ◈ ◈</div>
                <div class="val-sub">Algorithmically Benchmarked · Aurea Engine</div>
            </div>
            """, unsafe_allow_html=True)
            
except Exception as e:
    st.error(f"Error loading model or data: {e}")

st.markdown("""
<div class="lux-footer">
  <div>© AUREA ESTATES · 2026</div>
  <div>Strictly Confidential Valuation</div>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
