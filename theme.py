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
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Inter:wght@300;400;500;600;700&family=Montserrat:wght@300;400;500;600;700;800&display=swap');

        :root {{
            --bg: #0B0B0D;
            --text: #F5F1E6;
            --line: rgba(212, 175, 55, 0.2);
            --mute: #A8A8A8;
            --gold: #D4AF37;
            --gold-soft: #8C6E24;
            --glass-bg: rgba(18, 18, 22, 0.65);
            --glass-border: rgba(212, 175, 55, 0.15);
        }}

        /* ====== GLOBAL RESET ====== */
        html, body, [class*="css"] {{
            font-family: 'Montserrat', sans-serif !important;
        }}

        /* ====== SCROLLBAR ====== */
        ::-webkit-scrollbar {{ width: 6px; }}
        ::-webkit-scrollbar-track {{ background: #0B0B0D; }}
        ::-webkit-scrollbar-thumb {{
            background: linear-gradient(180deg, #8C6E24, #D4AF37);
            border-radius: 10px;
        }}
        ::-webkit-scrollbar-thumb:hover {{ background: #D4AF37; }}

        /* ====== KEYFRAME ANIMATIONS ====== */
        @keyframes fadeInUp {{
            0% {{ opacity: 0; transform: translateY(40px); filter: blur(4px); }}
            100% {{ opacity: 1; transform: translateY(0); filter: blur(0); }}
        }}

        @keyframes revealUp {{
            0% {{ opacity: 0; transform: translateY(50px) scale(0.98); filter: blur(6px); }}
            100% {{ opacity: 1; transform: translateY(0) scale(1); filter: blur(0); }}
        }}

        @keyframes shimmerText {{
            0% {{ background-position: -200% center; }}
            100% {{ background-position: 200% center; }}
        }}

        @keyframes auroraShift {{
            0% {{ opacity: 0.03; transform: scale(1) rotate(0deg); }}
            33% {{ opacity: 0.06; transform: scale(1.05) rotate(1deg); }}
            66% {{ opacity: 0.04; transform: scale(0.98) rotate(-1deg); }}
            100% {{ opacity: 0.03; transform: scale(1) rotate(0deg); }}
        }}

        @keyframes prismaticSweep {{
            0% {{ transform: translateX(-100%) skewX(-15deg); }}
            100% {{ transform: translateX(300%) skewX(-15deg); }}
        }}

        @keyframes glowPulse {{
            0%, 100% {{ box-shadow: 0 0 15px rgba(212,175,55,0.05), inset 0 0 20px rgba(212,175,55,0.02); }}
            50% {{ box-shadow: 0 0 25px rgba(212,175,55,0.12), inset 0 0 30px rgba(212,175,55,0.05); }}
        }}

        @keyframes navBorderSweep {{
            0% {{ background-position: -200% 0; }}
            100% {{ background-position: 200% 0; }}
        }}

        @keyframes activePulse {{
            0%, 100% {{ border-color: rgba(212,175,55,0.55); box-shadow: 0 0 8px rgba(212,175,55,0.1); }}
            50% {{ border-color: rgba(212,175,55,0.85); box-shadow: 0 0 20px rgba(212,175,55,0.2); }}
        }}

        @keyframes dividerPulse {{
            0%, 100% {{ opacity: 0.5; text-shadow: 0 0 8px rgba(212,175,55,0.3); }}
            50% {{ opacity: 1; text-shadow: 0 0 20px rgba(212,175,55,0.6); }}
        }}

        @keyframes focusRingPulse {{
            0%, 100% {{ box-shadow: 0 0 0 2px rgba(212,175,55,0.2); }}
            50% {{ box-shadow: 0 0 0 4px rgba(212,175,55,0.35); }}
        }}

        @keyframes tabUnderline {{
            0%, 100% {{ box-shadow: 0 2px 0 0 rgba(212,175,55,0.6); }}
            50% {{ box-shadow: 0 2px 0 0 rgba(212,175,55,1), 0 4px 12px rgba(212,175,55,0.2); }}
        }}

        /* ====== BACKGROUND: LUXURY DARK + AURORA ====== */
        [data-testid="stApp"] {{
            background: radial-gradient(ellipse at 50% -20%, #1a1a2e 0%, #0B0B0D 45%, #050505 100%) !important;
            background-attachment: fixed !important;
            overflow-x: hidden;
        }}

        /* Golden aurora radials */
        [data-testid="stApp"]::before {{
            content: '';
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background:
                radial-gradient(ellipse at 10% 0%, rgba(212,175,55,0.04) 0%, transparent 50%),
                radial-gradient(ellipse at 90% 0%, rgba(212,175,55,0.04) 0%, transparent 50%),
                radial-gradient(ellipse at 50% 100%, rgba(140,110,36,0.025) 0%, transparent 50%);
            pointer-events: none;
            z-index: 0;
            animation: auroraShift 12s ease-in-out infinite;
        }}


        /* ====== ANIMATED SECTIONS ====== */
        .animated-section {{
            animation: fadeInUp 1.2s cubic-bezier(0.22, 0.61, 0.36, 1) forwards;
        }}

        .stagger-1 {{ animation: revealUp 0.9s cubic-bezier(0.22,0.61,0.36,1) 0.1s both; }}
        .stagger-2 {{ animation: revealUp 0.9s cubic-bezier(0.22,0.61,0.36,1) 0.25s both; }}
        .stagger-3 {{ animation: revealUp 0.9s cubic-bezier(0.22,0.61,0.36,1) 0.4s both; }}
        .stagger-4 {{ animation: revealUp 0.9s cubic-bezier(0.22,0.61,0.36,1) 0.55s both; }}
        .stagger-5 {{ animation: revealUp 0.9s cubic-bezier(0.22,0.61,0.36,1) 0.7s both; }}

        /* ====== TYPOGRAPHY ====== */
        .section-eyebrow {{
            color: var(--gold);
            text-transform: uppercase;
            letter-spacing: 4px;
            font-size: 0.75rem;
            margin-bottom: 0.5rem;
            font-weight: 600;
            opacity: 0;
            animation: revealUp 0.8s cubic-bezier(0.22,0.61,0.36,1) 0.1s forwards;
        }}

        .section-title {{
            font-family: 'Cinzel', serif;
            font-size: 3.5rem;
            margin-bottom: 1rem;
            font-weight: 700;
            line-height: 1.1;
            letter-spacing: 0.02em;
            background: linear-gradient(90deg, #FFFFFF 0%, #D4AF37 25%, #FFF6DA 50%, #D4AF37 75%, #FFFFFF 100%);
            background-size: 200% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: shimmerText 6s linear infinite;
        }}

        .section-title em {{
            color: var(--gold);
            font-style: italic;
            -webkit-text-fill-color: var(--gold);
        }}

        .muted {{
            color: #B5B0A5;
            font-size: 1.05rem;
            line-height: 1.7;
            font-weight: 400;
            letter-spacing: 0.01em;
        }}

        /* ====== LUXURY METRIC CARDS ====== */
        .lux-metric {{
            position: relative;
            background: linear-gradient(145deg, rgba(22,22,28,0.85) 0%, rgba(12,12,16,0.9) 100%);
            border: 1px solid var(--glass-border);
            padding: 2.2rem 1.5rem;
            border-radius: 16px;
            text-align: center;
            backdrop-filter: blur(20px) saturate(150%);
            -webkit-backdrop-filter: blur(20px) saturate(150%);
            box-shadow:
                0 10px 40px rgba(0,0,0,0.6),
                inset 0 1px 0 rgba(255,255,255,0.03),
                inset 0 0 20px rgba(212,175,55,0.02);
            transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275),
                        box-shadow 0.4s ease,
                        border-color 0.4s ease;
            overflow: hidden;
            animation: glowPulse 5s ease-in-out infinite;
        }}

        .lux-metric::before {{
            content: '';
            position: absolute;
            top: 0; left: -100%;
            width: 60%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(212,175,55,0.06), transparent);
            transform: skewX(-15deg);
            transition: none;
            pointer-events: none;
        }}

        .lux-metric:hover::before {{
            animation: prismaticSweep 0.8s ease forwards;
        }}

        .lux-metric:hover {{
            transform: translateY(-8px) perspective(1000px) rotateX(2deg);
            box-shadow:
                0 20px 60px rgba(212,175,55,0.12),
                0 8px 30px rgba(0,0,0,0.5),
                inset 0 0 30px rgba(212,175,55,0.05);
            border-color: rgba(212,175,55,0.5);
        }}

        .lux-metric .lbl {{
            color: #B5B0A5;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 2.5px;
            margin-bottom: 0.75rem;
            font-weight: 500;
        }}

        .lux-metric .val {{
            font-family: 'Cinzel', serif;
            font-size: 2.4rem;
            color: var(--gold);
            margin: 0;
            text-shadow: 0 2px 15px rgba(212,175,55,0.25);
        }}

        /* ====== .metric CARDS (Market Intelligence) ====== */
        .metric {{
            position: relative;
            background: linear-gradient(145deg, rgba(22,22,28,0.85) 0%, rgba(12,12,16,0.9) 100%);
            border: 1px solid var(--glass-border);
            padding: 2rem 1.5rem;
            border-radius: 16px;
            text-align: center;
            backdrop-filter: blur(20px) saturate(150%);
            -webkit-backdrop-filter: blur(20px) saturate(150%);
            box-shadow:
                0 10px 40px rgba(0,0,0,0.6),
                inset 0 1px 0 rgba(255,255,255,0.03),
                inset 0 0 20px rgba(212,175,55,0.02);
            transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275),
                        box-shadow 0.4s ease,
                        border-color 0.4s ease;
            overflow: hidden;
            animation: glowPulse 5s ease-in-out infinite;
        }}

        .metric::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, rgba(212,175,55,0.6), transparent);
            border-radius: 2px;
        }}

        .metric::after {{
            content: '';
            position: absolute;
            top: 0; left: -100%;
            width: 60%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(212,175,55,0.06), transparent);
            transform: skewX(-15deg);
            pointer-events: none;
        }}

        .metric:hover::after {{
            animation: prismaticSweep 0.8s ease forwards;
        }}

        .metric:hover {{
            transform: translateY(-8px) perspective(1000px) rotateX(2deg);
            box-shadow:
                0 20px 60px rgba(212,175,55,0.12),
                0 8px 30px rgba(0,0,0,0.5),
                inset 0 0 30px rgba(212,175,55,0.05);
            border-color: rgba(212,175,55,0.5);
        }}

        .metric .lbl {{
            color: #B5B0A5;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 2.5px;
            margin-bottom: 0.6rem;
            font-weight: 500;
        }}

        .metric .val {{
            font-family: 'Cinzel', serif;
            font-size: 2rem;
            color: var(--gold);
            margin: 0;
            text-shadow: 0 2px 15px rgba(212,175,55,0.25);
        }}

        .metric .sub {{
            color: #999999;
            font-size: 0.74rem;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-top: 0.5rem;
        }}

        /* ====== SECTION DIVIDER ====== */
        .section-divider {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 16px;
            margin: 3rem 0;
            opacity: 0;
            animation: revealUp 0.8s 0.3s forwards;
        }}

        .section-divider::before,
        .section-divider::after {{
            content: '';
            flex: 1;
            max-width: 200px;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(212,175,55,0.4), transparent);
        }}

        .section-divider .diamond {{
            color: var(--gold);
            font-size: 1rem;
            animation: dividerPulse 4s ease-in-out infinite;
        }}

        /* ====== NAVIGATION ====== */
        .nav-wrap {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 1.5rem;
            border-bottom: 2px solid transparent;
            border-image: linear-gradient(90deg, transparent 5%, rgba(212,175,55,0.3) 30%, rgba(212,175,55,0.5) 50%, rgba(212,175,55,0.3) 70%, transparent 95%) 1;
            margin-bottom: 2.5rem;
            position: relative;
        }}

        .nav-brand {{
            font-family: 'Cinzel', serif;
            font-size: 1.7rem;
            color: var(--gold);
            letter-spacing: 3px;
            text-shadow: 0 0 30px rgba(212,175,55,0.2), 0 0 60px rgba(212,175,55,0.05);
        }}

        .nav-brand span {{
            color: var(--mute);
        }}

        .nav-tag {{
            color: var(--mute);
            font-size: 0.78rem;
            letter-spacing: 2.5px;
            text-transform: uppercase;
            font-weight: 400;
        }}

        /* ====== SIDEBAR ====== */
        section[data-testid="stSidebar"] {{
            background-color: #0A0A0A;
            border-right: 1px solid var(--line);
        }}

        /* ====== INPUT FIELDS: PREMIUM ====== */
        .stSelectbox > div > div,
        .stNumberInput > div > div {{
            background: rgba(18,18,24,0.7) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: 10px !important;
            color: #F5F1E6 !important;
            backdrop-filter: blur(8px) !important;
            transition: all 0.3s ease !important;
            min-height: 44px !important;
        }}

        .stSelectbox > div > div:hover,
        .stNumberInput > div > div:hover {{
            border-color: rgba(212,175,55,0.4) !important;
            box-shadow: 0 0 12px rgba(212,175,55,0.08) !important;
        }}

        .stSelectbox > div > div:focus-within,
        .stNumberInput > div > div:focus-within {{
            border-color: rgba(212,175,55,0.6) !important;
            animation: focusRingPulse 2s ease-in-out infinite !important;
        }}

        /* Input labels */
        .stSelectbox label,
        .stNumberInput label,
        .stSlider label {{
            color: #C5C0B5 !important;
            font-size: 0.8rem !important;
            text-transform: uppercase !important;
            letter-spacing: 1.5px !important;
            font-weight: 500 !important;
            min-height: 2.2rem !important;
            display: flex !important;
            align-items: flex-end !important;
            margin-bottom: 0.2rem !important;
        }}

        /* ====== SLIDER ====== */
        .stSlider > div > div > div > div {{
            background: linear-gradient(90deg, var(--gold-soft), var(--gold)) !important;
        }}
        .stSlider [data-testid="stThumbValue"] {{
            color: var(--gold) !important;
            font-family: 'Cinzel', serif !important;
        }}

        /* ====== TABS: PREMIUM SEGMENTED CONTROL ====== */
        .stTabs [data-baseweb="tab-list"] {{
            background: rgba(18,18,24,0.5);
            border-radius: 12px;
            padding: 4px;
            border: 1px solid var(--glass-border);
            backdrop-filter: blur(10px);
            gap: 4px;
        }}

        .stTabs [data-baseweb="tab"] {{
            background: transparent !important;
            border-radius: 8px !important;
            color: #B5B0A5 !important;
            font-family: 'Montserrat', sans-serif !important;
            font-weight: 600 !important;
            font-size: 0.78rem !important;
            letter-spacing: 1.5px !important;
            text-transform: uppercase !important;
            padding: 10px 24px !important;
            transition: all 0.3s ease !important;
            border: none !important;
        }}

        .stTabs [data-baseweb="tab"]:hover {{
            color: var(--gold) !important;
            background: rgba(212,175,55,0.06) !important;
        }}

        .stTabs [aria-selected="true"] {{
            color: var(--gold) !important;
            background: rgba(212,175,55,0.1) !important;
            animation: tabUnderline 3s ease-in-out infinite !important;
        }}

        .stTabs [data-baseweb="tab-highlight"] {{
            background-color: var(--gold) !important;
            height: 2px !important;
            border-radius: 2px !important;
        }}

        .stTabs [data-baseweb="tab-border"] {{
            display: none !important;
        }}

        /* ====== DATAFRAME / TABLE ====== */
        .stDataFrame {{
            border: 1px solid var(--glass-border) !important;
            border-radius: 12px !important;
            overflow: hidden !important;
        }}

        .stDataFrame [data-testid="stDataFrameResizable"] {{
            border-radius: 12px !important;
        }}

        /* Style the glideDataEditor cells */
        .stDataFrame div[class*="glideDataEditor"] {{
            background: rgba(10,10,14,0.9) !important;
        }}

        /* ====== STREAMLIT SCAFFOLD HIDING ====== */
        [data-testid="stMain"] {{ margin-left: 0 !important; }}
        [data-testid="stToolbar"],
        [data-testid="stAppToolbar"],
        .stAppToolbar,
        [data-testid="stExpandSidebarButton"] {{
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            width: 0 !important;
            height: 0 !important;
            pointer-events: none !important;
        }}

        /* ====== GLASS PANELS ====== */
        .glass-panel {{
            background: linear-gradient(145deg, rgba(20,20,26,0.7) 0%, rgba(10,10,14,0.8) 100%);
            border: 1px solid var(--glass-border);
            border-radius: 16px;
            padding: 2rem;
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.4);
            transition: border-color 0.4s ease, box-shadow 0.4s ease;
        }}

        .glass-panel:hover {{
            border-color: rgba(212,175,55,0.35);
            box-shadow: 0 12px 40px rgba(212,175,55,0.06), 0 8px 32px rgba(0,0,0,0.4);
        }}

        /* ====== FINAL VALUATION OVERRIDE ====== */
        .final-valuation {{
            position: relative;
            background: linear-gradient(180deg, rgba(22,22,28,0.95) 0%, rgba(8,8,12,0.95) 100%);
            border: 1px solid rgba(212,175,55,0.3);
            padding: 4rem 2rem;
            border-radius: 20px;
            text-align: center;
            margin-top: 2rem;
            backdrop-filter: blur(20px);
            box-shadow:
                inset 0 0 60px rgba(212,175,55,0.04),
                0 25px 60px rgba(0,0,0,0.7),
                0 0 0 1px rgba(212,175,55,0.1);
            animation: glowPulse 4s ease-in-out infinite;
            overflow: hidden;
        }}

        .final-valuation .lbl {{
            color: #B5B0A5;
            text-transform: uppercase;
            letter-spacing: 5px;
            font-size: 0.95rem;
            margin-bottom: 1.5rem;
            font-weight: 500;
        }}

        .final-valuation .val {{
            font-family: 'Cinzel', serif;
            font-size: 5.5rem;
            margin: 0;
            background: linear-gradient(90deg, #8C6E24, #D4AF37, #FFF6DA, #D4AF37, #8C6E24);
            background-size: 200% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: shimmerText 4s linear infinite;
            filter: drop-shadow(0 4px 20px rgba(212,175,55,0.3));
        }}

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
        padding: 10px 24px !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 999px !important;
        background: rgba(18,18,24,0.6) !important;
        backdrop-filter: blur(8px) !important;
        transition: all 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        text-decoration: none !important;
      }
      .aurea-links [data-testid="stPageLink"] a:hover,
      .aurea-links a[data-testid="stPageLink-NavLink"]:hover {
        color: var(--gold) !important;
        border-color: rgba(212,175,55,0.4) !important;
        background: rgba(212,175,55,0.08) !important;
        box-shadow: 0 0 15px rgba(212,175,55,0.1) !important;
        transform: translateY(-1px) !important;
      }
      .aurea-links [data-testid="stPageLink"] p { margin: 0 !important; color: inherit !important; }
      .aurea-links [data-testid="stPageLink"] svg { display: none !important; }
      /* Highlight active with pulse */
      .aurea-active a {
        color: var(--gold) !important;
        border-color: rgba(212,175,55,0.55) !important;
        background: rgba(212,175,55,0.10) !important;
        animation: activePulse 3s ease-in-out infinite !important;
      }
      /* Wrapper */
      .aurea-nav-row { display:flex; gap: 12px; justify-content:center; margin: -18px 0 40px; flex-wrap: wrap; }
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
