import streamlit as st
import pickle
import pandas as pd

GOLD = "#D4AF37"
GOLD_SOFT = "#8C6E24"
DARK = "#050505"
CARD_BG = "rgba(255, 255, 255, 0.02)"

def inject_theme():
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Montserrat:wght@400;500;600;700;800&display=swap');
        
        :root {{
            --bg: #0B0B0D;
            --text: #F5F1E6;
            --line: rgba(212, 175, 55, 0.2);
            --mute: #888888;
            --gold: #D4AF37;
        }}
        
        /* Global Reset */
        html, body, [class*="css"] {{
            font-family: 'Montserrat', sans-serif !important;
        }}
        
        /* Smooth Animations */
        @keyframes fadeInUp {{
            0% {{ opacity: 0; transform: translateY(30px); }}
            100% {{ opacity: 1; transform: translateY(0); }}
        }}
        
        /* Aesthetic Luxury Background */
        [data-testid="stApp"] {{
            background: radial-gradient(circle at 50% -20%, #1a1a24 0%, #0B0B0D 50%, #050505 100%) !important;
            background-attachment: fixed !important;
        }}
        
        [data-testid="stApp"]::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; height: 800px;
            background: radial-gradient(circle at 15% 0%, rgba(212,175,55,0.035) 0%, transparent 40%),
                        radial-gradient(circle at 85% 0%, rgba(212,175,55,0.035) 0%, transparent 40%);
            pointer-events: none;
            z-index: 0;
        }}
        
        .animated-section {{
            animation: fadeInUp 1.2s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
        }}
        
        /* Typography */
        .section-eyebrow {{
            color: var(--gold);
            text-transform: uppercase;
            letter-spacing: 3px;
            font-size: 0.75rem;
            margin-bottom: 0.5rem;
            font-weight: 600;
        }}
        
        .section-title {{
            font-family: 'Cinzel', serif;
            font-size: 3.5rem;
            color: #FFFFFF;
            margin-bottom: 1rem;
            font-weight: 700;
            line-height: 1.1;
        }}
        
        .section-title em {{
            color: var(--gold);
            font-style: italic;
        }}
        
        .muted {{
            color: var(--mute);
            font-size: 1.1rem;
            line-height: 1.6;
            font-weight: 300;
        }}
        
        /* Luxury Dashboard Metrics */
        .lux-metric {{
            background: linear-gradient(145deg, rgba(20,20,20,0.8) 0%, rgba(10,10,10,0.8) 100%);
            border: 1px solid var(--line);
            padding: 2rem;
            border-radius: 12px;
            text-align: center;
            backdrop-filter: blur(10px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .lux-metric:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(212, 175, 55, 0.1);
            border-color: rgba(212, 175, 55, 0.5);
        }}
        
        .lux-metric .lbl {{
            color: var(--mute);
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 0.5rem;
        }}
        
        .lux-metric .val {{
            font-family: 'Cinzel', serif;
            font-size: 2.5rem;
            color: var(--gold);
            margin: 0;
            text-shadow: 0 2px 10px rgba(212, 175, 55, 0.2);
        }}
        
        /* Navigation Wrap */
        .nav-wrap {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 1.5rem;
            border-bottom: 1px solid var(--line);
            margin-bottom: 2.5rem;
        }}
        
        .nav-brand {{
            font-family: 'Cinzel', serif;
            font-size: 1.6rem;
            color: var(--gold);
            letter-spacing: 2px;
        }}
        
        .nav-brand span {{
            color: var(--mute);
        }}
        
        .nav-tag {{
            color: var(--mute);
            font-size: 0.8rem;
            letter-spacing: 2px;
            text-transform: uppercase;
        }}

        /* Sidebar styling */
        section[data-testid="stSidebar"] {{
            background-color: #0A0A0A;
            border-right: 1px solid var(--line);
        }}
        
        /* Base Streamlit overrides */
        .stSelectbox > div > div, .stNumberInput > div > div {{
            background-color: rgba(255,255,255,0.02) !important;
            border: 1px solid var(--line) !important;
            border-radius: 8px !important;
            color: #FFFFFF !important;
        }}
        /* Streamlit Scaffold Hiding */
        [data-testid="stMain"] { margin-left: 0 !important; }
        /* Kill the top-left sidebar toggle toolbar */
        [data-testid="stToolbar"],
        [data-testid="stAppToolbar"],
        .stAppToolbar,
        [data-testid="stExpandSidebarButton"] {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            width: 0 !important;
            height: 0 !important;
            pointer-events: none !important;
        }
    </style>
    """, unsafe_allow_html=True)

def render_nav(active: str = "valuation"):
    """Top nav bar with real multi-page routing via st.page_link."""
    st.markdown("""
    <div class="nav-wrap" id="aurea-nav">
      <div class="nav-brand">AUREA<span> · </span>ESTATES</div>
      <div class="nav-tag">Gurgaon · 2026</div>
    </div>
    """, unsafe_allow_html=True)
    # Native page links styled to sit under the brand as a chip row
    st.markdown("""
    <style>
      /* Chip-style page links */
      .aurea-links [data-testid="stPageLink"] a,
      .aurea-links a[data-testid="stPageLink-NavLink"] {
        color: var(--mute) !important;
        font-size: 0.78rem !important;
        letter-spacing: 0.22em !important;
        text-transform: uppercase !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
        border: 1px solid var(--line) !important;
        border-radius: 999px !important;
        background: rgba(20,20,24,0.6) !important;
        transition: all .25s ease;
        text-decoration: none !important;
      }
      .aurea-links [data-testid="stPageLink"] a:hover,
      .aurea-links a[data-testid="stPageLink-NavLink"]:hover {
        color: var(--gold) !important;
        border-color: rgba(212,175,55,0.4) !important;
        background: rgba(212,175,55,0.06) !important;
      }
      .aurea-links [data-testid="stPageLink"] p { margin: 0 !important; color: inherit !important; }
      .aurea-links [data-testid="stPageLink"] svg { display: none !important; }
      /* Highlight active */
      .aurea-active a { color: var(--gold) !important; border-color: rgba(212,175,55,0.55) !important;
                       background: rgba(212,175,55,0.10) !important; }
      /* Wrapper */
      .aurea-nav-row { display:flex; gap: 10px; justify-content:center; margin: -18px 0 40px; flex-wrap: wrap; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="aurea-nav-row aurea-links">', unsafe_allow_html=True)
    cols = st.columns([1, 1, 1, 1, 1])
    with cols[1]:
        st.markdown(f'<div class="{"aurea-active" if active=="valuation" else ""} ">', unsafe_allow_html=True)
        st.page_link("app.py", label="Valuation")
        st.markdown('</div>', unsafe_allow_html=True)
    with cols[2]:
        st.markdown(f'<div class="{"aurea-active" if active=="intelligence" else ""} ">', unsafe_allow_html=True)
        st.page_link("pages/1_◈_Market_Intelligence.py", label="Market Intelligence")
        st.markdown('</div>', unsafe_allow_html=True)
    with cols[3]:
        st.markdown(f'<div class="{"aurea-active" if active=="guide" else ""} ">', unsafe_allow_html=True)
        st.page_link("pages/2_◈_The_Guide.py", label="The Guide")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

@st.cache_data
def load_df():
    return pd.read_csv('data/processed/gurgaon_properties_post_feature_selection_v2.csv')

def format_inr(val):
    if val >= 100:
        return f"₹ {val:,.0f}"
    return f"₹ {val:.2f} Cr"
