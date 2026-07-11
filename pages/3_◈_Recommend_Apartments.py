"""Aurea Estates — Recommend Apartments"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pickle
import pandas as pd
import numpy as np
from theme import inject_theme, render_nav

st.set_page_config(
    page_title="Aurea · Recommend Apartments",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_theme()
render_nav(active="recommend")

# ── Page-specific luxury CSS ─────────────────────────────────────────
st.markdown("""
<style>
    /* ═══════════════════════════════════════════════════════════════
       RECOMMEND PAGE — HYPER-LUXURY ANIMATIONS & PREMIUM UI
       ═══════════════════════════════════════════════════════════════ */

    /* ── Keyframes ─────────────────────────────────────────────── */
    @keyframes recRevealUp {
        0%   { opacity: 0; transform: translateY(44px) scale(0.97); filter: blur(6px); }
        100% { opacity: 1; transform: translateY(0) scale(1);       filter: blur(0);   }
    }

    @keyframes recCardSlideIn {
        0%   { opacity: 0; transform: translateY(30px) scale(0.96); }
        100% { opacity: 1; transform: translateY(0) scale(1);       }
    }

    @keyframes recBorderGlow {
        0%, 100% { border-color: rgba(212, 175, 55, 0.15); box-shadow: 0 0 25px rgba(212, 175, 55, 0.02); }
        50%      { border-color: rgba(212, 175, 55, 0.40); box-shadow: 0 0 50px rgba(212, 175, 55, 0.08); }
    }

    @keyframes recScoreShimmer {
        0%   { background-position: -200% center; }
        100% { background-position: 200% center;  }
    }

    @keyframes recDiamondPulse {
        0%, 100% { opacity: 0.5; transform: scale(1);   }
        50%      { opacity: 1;   transform: scale(1.15); }
    }

    @keyframes recGlowPulse {
        0%, 100% { box-shadow: 0 0 15px rgba(212,175,55,0.05), inset 0 0 20px rgba(212,175,55,0.02); }
        50%      { box-shadow: 0 0 25px rgba(212,175,55,0.12), inset 0 0 30px rgba(212,175,55,0.05); }
    }

    @keyframes recPrismaticSweep {
        0%   { transform: translateX(-100%) skewX(-15deg); }
        100% { transform: translateX(300%) skewX(-15deg);  }
    }

    @keyframes recPinDrop {
        0%   { opacity: 0; transform: translateY(-12px) scale(0.8); }
        60%  { transform: translateY(2px) scale(1.05); }
        100% { opacity: 1; transform: translateY(0) scale(1); }
    }

    @keyframes recFooterLineExpand {
        0%   { width: 0%;   opacity: 0; }
        100% { width: 100%; opacity: 1; }
    }

    /* ── Animated entrance wrapper ─────────────────────────────── */
    .rec-animated {
        animation: recRevealUp 1.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        opacity: 0;
    }
    .rec-animated.delay-1 { animation-delay: 0.10s; }
    .rec-animated.delay-2 { animation-delay: 0.30s; }
    .rec-animated.delay-3 { animation-delay: 0.50s; }
    .rec-animated.delay-4 { animation-delay: 0.70s; }

    /* ── Ornamental diamond divider ────────────────────────────── */
    .rec-ornament {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 18px;
        margin: 30px 0 44px 0;
        animation: recRevealUp 1.2s 0.25s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        opacity: 0;
    }
    .rec-ornament .orn-line {
        flex: 1;
        max-width: 180px;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.45), transparent);
    }
    .rec-ornament .orn-diamond {
        color: #D4AF37;
        font-size: 0.92rem;
        animation: recDiamondPulse 4s ease-in-out infinite;
        text-shadow: 0 0 12px rgba(212, 175, 55, 0.30);
    }

    /* ── Glass section panels ─────────────────────────────────── */
    .rec-glass-panel {
        background: linear-gradient(165deg,
            rgba(212, 175, 55, 0.025) 0%,
            rgba(15, 15, 18, 0.75)   35%,
            rgba(10, 10, 12, 0.85)   100%);
        backdrop-filter: blur(24px) saturate(1.2);
        -webkit-backdrop-filter: blur(24px) saturate(1.2);
        border: 1px solid rgba(212, 175, 55, 0.18);
        border-radius: 18px;
        padding: 44px 48px 40px;
        position: relative;
        overflow: hidden;
        animation: recBorderGlow 6s ease-in-out infinite;
        box-shadow:
            0 20px 60px rgba(0, 0, 0, 0.50),
            inset 0 1px 0 rgba(212, 175, 55, 0.08);
        margin-bottom: 2rem;
    }
    .rec-glass-panel::before {
        content: '';
        position: absolute;
        top: 0; left: 10%; right: 10%;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.5), transparent);
    }
    .rec-glass-panel::after {
        content: '';
        position: absolute;
        top: -60px; right: -60px;
        width: 200px; height: 200px;
        background: radial-gradient(circle, rgba(212, 175, 55, 0.04) 0%, transparent 70%);
        pointer-events: none;
    }

    /* ── Section subtitle ──────────────────────────────────────── */
    .rec-subtitle {
        font-family: 'Cinzel', serif;
        font-size: 1.35rem;
        font-weight: 700;
        color: #F5F1E6;
        letter-spacing: 0.08em;
        margin-bottom: 0.6rem;
        position: relative;
        padding-left: 20px;
        border-left: 3px solid #D4AF37;
    }

    .rec-desc {
        color: #B5B0A5;
        font-size: 1rem;
        line-height: 1.7;
        margin-bottom: 1.8rem;
    }

    /* ── Result cards for radius search ─────────────────────────── */
    .rec-result-card {
        position: relative;
        background: linear-gradient(145deg, rgba(22,22,28,0.85) 0%, rgba(12,12,16,0.9) 100%);
        border: 1px solid rgba(212, 175, 55, 0.15);
        padding: 1.3rem 1.6rem;
        border-radius: 14px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        box-shadow: 0 8px 28px rgba(0,0,0,0.4);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        overflow: hidden;
        opacity: 0;
        animation: recCardSlideIn 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    .rec-result-card::before {
        content: '';
        position: absolute;
        top: 0; left: -100%;
        width: 60%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(212,175,55,0.06), transparent);
        transform: skewX(-15deg);
        pointer-events: none;
    }
    .rec-result-card:hover::before {
        animation: recPrismaticSweep 0.8s ease forwards;
    }
    .rec-result-card:hover {
        transform: translateY(-4px);
        border-color: rgba(212, 175, 55, 0.45);
        box-shadow: 0 16px 48px rgba(212,175,55,0.08), 0 8px 28px rgba(0,0,0,0.5);
    }
    .rec-result-card .rec-name {
        font-family: 'Cinzel', serif;
        font-size: 1.05rem;
        color: #F5F1E6;
        letter-spacing: 0.04em;
    }
    .rec-result-card .rec-distance {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.85rem;
        color: #D4AF37;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-shadow: 0 0 8px rgba(212,175,55,0.2);
    }
    .rec-result-card .rec-pin {
        font-size: 1rem;
        margin-right: 10px;
        opacity: 0;
        animation: recPinDrop 0.5s ease forwards;
    }

    /* ── Recommendation cards ──────────────────────────────────── */
    .rec-recommend-card {
        position: relative;
        background: linear-gradient(145deg, rgba(22,22,28,0.85) 0%, rgba(12,12,16,0.9) 100%);
        border: 1px solid rgba(212, 175, 55, 0.15);
        padding: 1.8rem 2rem;
        border-radius: 16px;
        text-align: center;
        backdrop-filter: blur(20px) saturate(150%);
        -webkit-backdrop-filter: blur(20px) saturate(150%);
        box-shadow:
            0 10px 40px rgba(0,0,0,0.6),
            inset 0 1px 0 rgba(255,255,255,0.03);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        overflow: hidden;
        animation: recGlowPulse 5s ease-in-out infinite;
        opacity: 0;
        animation: recCardSlideIn 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    .rec-recommend-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(212,175,55,0.5), transparent);
        border-radius: 2px;
    }
    .rec-recommend-card::after {
        content: '';
        position: absolute;
        top: 0; left: -100%;
        width: 60%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(212,175,55,0.06), transparent);
        transform: skewX(-15deg);
        pointer-events: none;
    }
    .rec-recommend-card:hover::after {
        animation: recPrismaticSweep 0.8s ease forwards;
    }
    .rec-recommend-card:hover {
        transform: translateY(-8px) perspective(1000px) rotateX(2deg);
        box-shadow:
            0 20px 60px rgba(212,175,55,0.12),
            0 8px 30px rgba(0,0,0,0.5),
            inset 0 0 30px rgba(212,175,55,0.05);
        border-color: rgba(212,175,55,0.5);
    }
    .rec-recommend-card .rec-rank {
        font-family: 'Cinzel', serif;
        font-size: 0.8rem;
        font-weight: 700;
        color: #D4AF37;
        width: 32px; height: 32px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        border: 1px solid rgba(212,175,55,0.30);
        border-radius: 50%;
        background: rgba(212,175,55,0.06);
        margin-bottom: 0.8rem;
    }
    .rec-recommend-card .rec-prop-name {
        font-family: 'Cinzel', serif;
        font-size: 1.1rem;
        color: #F5F1E6;
        margin-bottom: 0.6rem;
        letter-spacing: 0.03em;
        line-height: 1.4;
    }
    .rec-recommend-card .rec-score {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.82rem;
        font-weight: 600;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        background: linear-gradient(90deg, #8C6E24, #D4AF37, #FFF6DA, #D4AF37, #8C6E24);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: recScoreShimmer 4s linear infinite;
    }
    .rec-recommend-card .rec-score-bar-bg {
        width: 100%;
        height: 4px;
        background: rgba(212,175,55,0.1);
        border-radius: 2px;
        margin-top: 0.8rem;
        overflow: hidden;
    }
    .rec-recommend-card .rec-score-bar {
        height: 100%;
        background: linear-gradient(90deg, #8C6E24, #D4AF37);
        border-radius: 2px;
        transition: width 0.8s cubic-bezier(0.22, 1, 0.36, 1);
    }

    /* ── Empty state ──────────────────────────────────────────── */
    .rec-empty {
        text-align: center;
        padding: 3rem 1rem;
        color: #B5B0A5;
        font-size: 1.05rem;
        letter-spacing: 0.05em;
    }
    .rec-empty .rec-empty-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        opacity: 0.4;
    }

    /* ── Animated footer ──────────────────────────────────────── */
    .rec-footer {
        margin-top: 80px;
        padding-top: 30px;
        position: relative;
        display: flex;
        justify-content: space-between;
        color: var(--mute);
        font-size: 0.82rem;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        opacity: 0;
        animation: recRevealUp 1.0s 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    .rec-footer::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        height: 1px;
        background: linear-gradient(90deg,
            rgba(212, 175, 55, 0.05),
            rgba(212, 175, 55, 0.50) 50%,
            rgba(212, 175, 55, 0.05));
        animation: recFooterLineExpand 1.8s 0.6s cubic-bezier(0.22, 1, 0.36, 1) forwards;
        width: 0;
        opacity: 0;
    }
</style>
""", unsafe_allow_html=True)


# ── Compat loader for old-pandas pickles ─────────────────────────────
def _compat_pickle_load(filepath):
    """Load a pickle that may have been created with an older pandas version."""
    try:
        with open(filepath, 'rb') as f:
            return pickle.load(f)
    except TypeError:
        # Handle pandas BlockPlacement slice incompatibility (pandas 1.x → 2.x)
        from pandas._libs.internals import BlockPlacement
        import pandas.core.internals.blocks as blocks

        def compat_new_block(values, placement=None, *, ndim=2, refs=None):
            if isinstance(placement, slice):
                placement = BlockPlacement(placement)
            klass = blocks.get_block_type(values.dtype)
            return klass(values, ndim=ndim, placement=placement, refs=refs)

        class CompatUnpickler(pickle.Unpickler):
            def find_class(self, module, name):
                if module == 'pandas.core.internals.blocks' and name == 'new_block':
                    return compat_new_block
                return super().find_class(module, name)

        with open(filepath, 'rb') as f:
            return CompatUnpickler(f).load()


# ── Load models ──────────────────────────────────────────────────────
@st.cache_resource
def load_recommendation_models():
    location_df = _compat_pickle_load('models/location_distance.pkl')
    cosine_sim1 = _compat_pickle_load('models/cosine_sim1.pkl')
    cosine_sim2 = _compat_pickle_load('models/cosine_sim2.pkl')
    cosine_sim3 = _compat_pickle_load('models/cosine_sim3.pkl')
    return location_df, cosine_sim1, cosine_sim2, cosine_sim3


def recommend_properties_with_scores(property_name, location_df, cosine_sim1, cosine_sim2, cosine_sim3, top_n=5):
    cosine_sim_matrix = 0.5 * cosine_sim1 + 0.8 * cosine_sim2 + 1 * cosine_sim3

    sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]

    top_properties = location_df.index[top_indices].tolist()

    recommendations_df = pd.DataFrame({
        'PropertyName': top_properties,
        'SimilarityScore': top_scores
    })

    return recommendations_df


try:
    location_df, cosine_sim1, cosine_sim2, cosine_sim3 = load_recommendation_models()

    # ── Header ────────────────────────────────────────────────────
    st.markdown('<div class="rec-animated delay-1">', unsafe_allow_html=True)
    st.markdown('<div class="section-eyebrow">Discovery Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Recommend <em>Apartments</em>.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Ornamental divider ────────────────────────────────────────
    st.markdown("""
    <div class="rec-ornament">
      <div class="orn-line"></div>
      <div class="orn-diamond">◈</div>
      <div class="orn-line"></div>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════
    # SECTION 1 — Location Radius Search
    # ══════════════════════════════════════════════════════════════
    st.markdown('<div class="rec-animated delay-2">', unsafe_allow_html=True)
    # st.markdown('<div class="rec-glass-panel">', unsafe_allow_html=True)
    st.markdown('<div class="rec-subtitle">Proximity Search</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="rec-desc">Discover residences within your chosen radius. '
        'Select a landmark location and define your perimeter — Aurea will surface '
        'every property within reach.</div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)  # close rec-glass-panel

    col1, col2 = st.columns([3, 1], gap="large")
    with col1:
        selected_location = st.selectbox(
            'Select Location',
            sorted(location_df.columns.to_list()),
            key="loc_search"
        )
    with col2:
        radius = st.number_input(
            'Radius (km)',
            min_value=0.5,
            max_value=50.0,
            value=5.0,
            step=0.5,
            key="radius_input"
        )

    st.markdown('<div style="height: 16px"></div>', unsafe_allow_html=True)

    _, btn_col1, _ = st.columns([1, 1, 1])
    with btn_col1:
        search_clicked = st.button('Search Nearby', key="btn_search", use_container_width=True)

    if search_clicked:
        result_ser = location_df[
            location_df[selected_location] < radius * 1000
        ][selected_location].sort_values()

        if len(result_ser) == 0:
            st.markdown("""
            <div class="rec-empty">
                <div class="rec-empty-icon">◈</div>
                <div>No properties found within this radius. Try expanding your search perimeter.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<div style="height: 20px"></div>', unsafe_allow_html=True)
            for idx, (key, value) in enumerate(result_ser.items()):
                dist_km = round(value / 1000, 1)
                delay = 0.1 + idx * 0.06
                st.markdown(f"""
                <div class="rec-result-card" style="animation-delay: {delay}s;">
                    <div style="display: flex; align-items: center;">
                        <span class="rec-pin" style="animation-delay: {delay + 0.2}s;">📍</span>
                        <span class="rec-name">{key}</span>
                    </div>
                    <span class="rec-distance">{dist_km} km</span>
                </div>
                """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # close rec-animated delay-2

    # ── Divider ───────────────────────────────────────────────────
    st.markdown("""
    <div class="rec-ornament">
      <div class="orn-line"></div>
      <div class="orn-diamond">◈</div>
      <div class="orn-line"></div>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════
    # SECTION 2 — Apartment Recommendations
    # ══════════════════════════════════════════════════════════════
    st.markdown('<div class="rec-animated delay-3">', unsafe_allow_html=True)
    # st.markdown('<div class="rec-glass-panel">', unsafe_allow_html=True)
    st.markdown('<div class="rec-subtitle">Similar Residences</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="rec-desc">Select an apartment you admire. Aurea\'s multi-signal '
        'similarity engine will surface five residences that share its DNA — matched on '
        'amenities, location proximity, and luxury profile.</div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)  # close rec-glass-panel

    selected_apartment = st.selectbox(
        'Select an Apartment',
        sorted(location_df.index.to_list()),
        key="apt_recommend"
    )

    st.markdown('<div style="height: 16px"></div>', unsafe_allow_html=True)

    _, btn_col2, _ = st.columns([1, 1, 1])
    with btn_col2:
        recommend_clicked = st.button('Discover Similar', key="btn_recommend", use_container_width=True)

    if recommend_clicked:
        recommendation_df = recommend_properties_with_scores(
            selected_apartment, location_df, cosine_sim1, cosine_sim2, cosine_sim3
        )

        st.markdown('<div style="height: 24px"></div>', unsafe_allow_html=True)

        cols = st.columns(len(recommendation_df), gap="medium")
        max_score = recommendation_df['SimilarityScore'].max() if len(recommendation_df) > 0 else 1

        for idx, (col, (_, row)) in enumerate(zip(cols, recommendation_df.iterrows())):
            with col:
                score_pct = (row['SimilarityScore'] / max_score) * 100 if max_score > 0 else 0
                delay = 0.15 + idx * 0.12
                st.markdown(f"""
                <div class="rec-recommend-card" style="animation-delay: {delay}s;">
                    <div class="rec-rank">{idx + 1}</div>
                    <div class="rec-prop-name">{row['PropertyName']}</div>
                    <div class="rec-score">Match: {row['SimilarityScore']:.2%}</div>
                    <div class="rec-score-bar-bg">
                        <div class="rec-score-bar" style="width: {score_pct:.0f}%;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # close rec-animated delay-3

    # ── Footer ────────────────────────────────────────────────────
    st.markdown("""
    <div class="rec-footer">
      <div>© Aurea Estates · Est. 2026</div>
      <div>Discovery powered by multi-signal similarity.</div>
    </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error loading recommendation models: {e}")
