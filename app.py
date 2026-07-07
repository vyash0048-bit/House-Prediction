import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import plotly.graph_objects as go
from theme import inject_theme, render_nav, format_inr, GOLD

st.set_page_config(
    page_title="Aurea · Valuation Engine",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_theme()
render_nav(active="valuation")

# Component Styles
st.markdown("""
<style>
    .stButton>button {
        background: transparent;
        color: #D4AF37;
        border: 1px solid #D4AF37;
        border-radius: 6px;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 1rem;
        padding: 1rem 2rem;
        transition: all 0.4s ease;
        width: 100%;
    }
    .stButton>button:hover {
        background: #D4AF37;
        color: #050505;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.3);
    }
    .final-valuation {
        background: linear-gradient(180deg, rgba(20,20,20,0.9) 0%, rgba(5,5,5,0.9) 100%);
        border: 1px solid rgba(212, 175, 55, 0.3);
        padding: 4rem 2rem;
        border-radius: 12px;
        text-align: center;
        margin-top: 2rem;
        box-shadow: inset 0 0 40px rgba(212, 175, 55, 0.05), 0 20px 50px rgba(0,0,0,0.8);
    }
    .final-valuation .lbl {
        color: #888888;
        text-transform: uppercase;
        letter-spacing: 4px;
        font-size: 1rem;
        margin-bottom: 1rem;
    }
    .final-valuation .val {
        font-family: 'Cinzel', serif;
        font-size: 5.5rem;
        color: #D4AF37;
        margin: 0;
        text-shadow: 0 4px 20px rgba(212, 175, 55, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Display Hero Image
try:
    from PIL import Image
    img = Image.open('assets/hero_banner.jpg')
    st.image(img, use_container_width=True)
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
    with open('models/pipeline.pkl', 'rb') as f:
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
    
    # Beautiful Plotly Chart
    fig = px.scatter(
        df.sample(min(800, len(df)), random_state=42), 
        x="built_up_area", y="price", 
        color_discrete_sequence=[GOLD],
        opacity=0.6
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#888888"),
        margin=dict(l=0, r=0, t=30, b=0),
        xaxis=dict(title="Built-up Area (sq.ft)", gridcolor="rgba(212,175,55,0.05)", zeroline=False),
        yaxis=dict(title="Price (Cr)", gridcolor="rgba(212,175,55,0.05)", zeroline=False),
        title=dict(text="Market Distribution", font=dict(family="Cinzel", color="#D4AF37", size=24))
    )
    fig.update_traces(marker=dict(size=8, line=dict(width=0)))
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('<div style="height: 60px"></div>', unsafe_allow_html=True)
    
    # ---- VALUATION ENGINE SECTION ----
    st.markdown('<div class="section-eyebrow">Valuation Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Determine <em>Value</em>.</div>', unsafe_allow_html=True)
    st.markdown('<p class="muted" style="margin-top:-10px; max-width:720px; margin-bottom: 40px;">'
                'Specify the exact parameters of the asset. Our algorithmic engine will benchmark it against the portfolio to determine the most defensible market price.</p>',
                unsafe_allow_html=True)
    
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
            furnishing_type = st.selectbox('Furnishing Type', sorted(df['furnishing_type'].unique()))
            luxury_category = st.selectbox('Luxury Category', sorted(df['luxury_category'].unique()))
            floor_category = st.selectbox('Floor Category', sorted(df['floor_category'].unique()))
            
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
                <div class="lbl">Estimated Market Value</div>
                <div class="val">{formatted_price}</div>
            </div>
            """, unsafe_allow_html=True)
            
except Exception as e:
    st.error(f"Error loading model or data: {e}")

st.markdown("""
<div style="margin-top:100px; padding-top:40px; border-top:1px solid var(--line);
     display:flex; justify-content:space-between; color:var(--mute); font-size:0.75rem; letter-spacing:2px; text-transform:uppercase;">
  <div>© AUREA ESTATES · 2026</div>
  <div>Strictly Confidential Valuation</div>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)