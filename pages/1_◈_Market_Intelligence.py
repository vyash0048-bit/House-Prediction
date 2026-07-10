"""" 
Aurea Estates — Market Intelligence Dashboard
Sector-wise analytics, trends & comparisons.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from theme import inject_theme, render_nav, load_df, format_inr, GOLD, GOLD_SOFT

st.set_page_config(
    page_title="Aurea · Market Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)
inject_theme()

# ---- Page-Specific Luxe CSS --------------------------------------------
st.markdown("""
<style>
/* ═══════════════════════════════════════════════════════════
   MARKET INTELLIGENCE — HYPER-LUXURY OVERRIDES
   ═══════════════════════════════════════════════════════════ */

/* ── Animated section entrance with staggered delays ────── */
@keyframes mi-revealUp {
  0%   { opacity: 0; transform: translateY(48px) scale(0.97); filter: blur(6px); }
  60%  { filter: blur(0); }
  100% { opacity: 1; transform: translateY(0) scale(1); filter: blur(0); }
}

.mi-animated-section {
  opacity: 0;
  animation: mi-revealUp 1.1s cubic-bezier(0.19, 1, 0.22, 1) forwards;
}

/* ── Title shimmer animation ──────────────────────────────── */
@keyframes mi-shimmer {
  0%   { background-position: -200% center; }
  100% { background-position: 200% center; }
}

.mi-shimmer-title {
  font-family: 'Cinzel', serif;
  font-size: 3.5rem;
  font-weight: 700;
  line-height: 1.1;
  margin-bottom: 1rem;
  background: linear-gradient(
    105deg,
    #FFFFFF 0%, #FFFFFF 35%,
    #D4AF37 42%, #FFF6DA 50%, #D4AF37 58%,
    #FFFFFF 65%, #FFFFFF 100%
  );
  background-size: 200% auto;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: mi-shimmer 6s ease-in-out infinite;
}

.mi-shimmer-title em {
  -webkit-text-fill-color: #D4AF37;
  font-style: italic;
}

/* ── Enhanced metric card ─────────────────────────────────── */
@keyframes mi-goldLineGrow {
  0%   { width: 0; opacity: 0; }
  100% { width: 36px; opacity: 1; }
}

.mi-metric {
  position: relative;
  background: linear-gradient(160deg,
    rgba(20,20,24,0.85) 0%,
    rgba(10,10,13,0.92) 100%
  );
  border: 1px solid rgba(212,175,55,0.12);
  border-radius: 14px;
  padding: 2rem 1.6rem 1.6rem;
  text-align: center;
  backdrop-filter: blur(18px) saturate(1.4);
  -webkit-backdrop-filter: blur(18px) saturate(1.4);
  box-shadow:
    0 8px 32px rgba(0,0,0,0.45),
    inset 0 1px 0 rgba(212,175,55,0.06);
  transition: all 0.4s cubic-bezier(0.19, 1, 0.22, 1);
  overflow: hidden;
}

/* Gold accent ornament line above each card */
.mi-metric::before {
  content: '';
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  height: 2px;
  width: 0;
  background: linear-gradient(90deg, transparent, #D4AF37, #FFF6DA, #D4AF37, transparent);
  border-radius: 2px;
  animation: mi-goldLineGrow 1s 0.6s cubic-bezier(0.19, 1, 0.22, 1) forwards;
}

/* Subtle corner glow */
.mi-metric::after {
  content: '';
  position: absolute;
  top: -1px;
  left: -1px;
  right: -1px;
  bottom: -1px;
  border-radius: 14px;
  background: linear-gradient(135deg,
    rgba(212,175,55,0.08) 0%,
    transparent 30%,
    transparent 70%,
    rgba(212,175,55,0.04) 100%
  );
  pointer-events: none;
  z-index: 0;
}

.mi-metric:hover {
  transform: translateY(-6px);
  border-color: rgba(212,175,55,0.4);
  box-shadow:
    0 16px 48px rgba(0,0,0,0.5),
    0 0 24px rgba(212,175,55,0.06),
    inset 0 1px 0 rgba(212,175,55,0.12);
}

.mi-metric .lbl {
  position: relative;
  z-index: 1;
  color: #B5B0A5;
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 2.5px;
  margin-bottom: 0.6rem;
  font-weight: 600;
}

.mi-metric .val {
  position: relative;
  z-index: 1;
  font-family: 'Cinzel', serif;
  font-size: 2rem;
  color: #D4AF37;
  margin: 0;
  text-shadow: 0 2px 12px rgba(212,175,55,0.18);
  line-height: 1.3;
}

.mi-metric .sub {
  position: relative;
  z-index: 1;
  color: #999999;
  font-size: 0.74rem;
  margin-top: 0.4rem;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

/* ── Glass-panel chart container ──────────────────────────── */
@keyframes mi-borderPulse {
  0%, 100% { border-color: rgba(212,175,55,0.10); }
  50%      { border-color: rgba(212,175,55,0.25); }
}

.mi-glass-panel {
  background: linear-gradient(145deg,
    rgba(18,18,22,0.7) 0%,
    rgba(8,8,11,0.85) 100%
  );
  border: 1px solid rgba(212,175,55,0.10);
  border-radius: 16px;
  padding: 1.8rem 1.4rem;
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  box-shadow:
    0 12px 40px rgba(0,0,0,0.4),
    inset 0 1px 0 rgba(255,255,255,0.02);
  animation: mi-borderPulse 5s ease-in-out infinite;
  position: relative;
  overflow: hidden;
}

/* Glass sheen highlight */
.mi-glass-panel::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg,
    transparent 0%,
    rgba(212,175,55,0.15) 20%,
    rgba(255,246,218,0.10) 50%,
    rgba(212,175,55,0.15) 80%,
    transparent 100%
  );
  pointer-events: none;
}

.mi-glass-panel:hover {
  border-color: rgba(212,175,55,0.30);
  box-shadow:
    0 16px 48px rgba(0,0,0,0.5),
    0 0 30px rgba(212,175,55,0.04);
}

/* ── Ornamental divider ──────────────────────────────────── */
@keyframes mi-dividerFadeIn {
  0%   { opacity: 0; transform: scaleX(0.3); }
  100% { opacity: 1; transform: scaleX(1); }
}

.mi-ornament {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin: 2.5rem auto;
  max-width: 320px;
  opacity: 0;
  animation: mi-dividerFadeIn 1.2s 0.4s cubic-bezier(0.19, 1, 0.22, 1) forwards;
}

.mi-ornament .line {
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(212,175,55,0.35), transparent);
}

.mi-ornament .diamond {
  color: #D4AF37;
  font-size: 0.65rem;
  opacity: 0.6;
  text-shadow: 0 0 8px rgba(212,175,55,0.3);
}

/* ── Luxe footer ─────────────────────────────────────────── */
@keyframes mi-footerLineShimmer {
  0%   { background-position: -300% center; }
  100% { background-position: 300% center; }
}

.mi-footer {
  margin-top: 80px;
  padding-top: 32px;
  position: relative;
}

.mi-footer::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(212,175,55,0.1) 15%,
    rgba(212,175,55,0.5) 35%,
    #D4AF37 50%,
    rgba(212,175,55,0.5) 65%,
    rgba(212,175,55,0.1) 85%,
    transparent 100%
  );
  background-size: 300% 100%;
  animation: mi-footerLineShimmer 8s ease-in-out infinite;
}

.mi-footer-inner {
  display: flex;
  justify-content: space-between;
  color: #888888;
  font-size: 0.78rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  font-weight: 500;
}

.mi-footer-inner span {
  transition: color 0.3s ease;
}

.mi-footer-inner span:hover {
  color: #D4AF37;
}

/* ── Stacked tab refinements ─────────────────────────────── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
  gap: 4px;
  border-bottom: 1px solid rgba(212,175,55,0.10) !important;
}

[data-testid="stTabs"] [data-baseweb="tab"] {
  color: #888888 !important;
  font-size: 0.82rem !important;
  letter-spacing: 0.15em !important;
  text-transform: uppercase !important;
  font-weight: 600 !important;
  padding: 12px 24px !important;
  border-radius: 8px 8px 0 0 !important;
  transition: all 0.3s ease !important;
}

[data-testid="stTabs"] [data-baseweb="tab"]:hover {
  color: #D4AF37 !important;
  background: rgba(212,175,55,0.04) !important;
}

[data-testid="stTabs"] [aria-selected="true"] {
  color: #D4AF37 !important;
  background: rgba(212,175,55,0.06) !important;
  border-bottom: 2px solid #D4AF37 !important;
}

[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
  background-color: #D4AF37 !important;
}

/* ── Dataframe styling ───────────────────────────────────── */
[data-testid="stDataFrame"] {
  border: 1px solid rgba(212,175,55,0.12) !important;
  border-radius: 12px !important;
  overflow: hidden;
}
</style>
""", unsafe_allow_html=True)

render_nav(active="intelligence")

df = load_df()

# ---- Header -------------------------------------------------------------
st.markdown('<div class="mi-animated-section" style="animation-delay: 0s">', unsafe_allow_html=True)
st.markdown('<div class="section-eyebrow">Market Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="mi-shimmer-title">A quiet read on <em>Gurgaon</em>.</div>', unsafe_allow_html=True)
st.markdown('<p class="muted" style="margin-top:-20px; max-width:720px;">'
            'A curated view of the 5,000 comparables in our model — segmented by sector, luxury tier and possession, so you can benchmark like a buyer with better information than the room.</p>',
            unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---- Ornamental divider --------------------------------------------------
st.markdown("""
<div class="mi-ornament">
  <div class="line"></div>
  <div class="diamond">◈</div>
  <div class="line"></div>
</div>
""", unsafe_allow_html=True)

# ---- KPI strip ----------------------------------------------------------
st.markdown('<div class="mi-animated-section" style="animation-delay: 0.15s">', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4, gap="medium")
median_cr = df["price"].median()
avg_psf = ((df["price"] * 1e7) / df["built_up_area"]).median()
top_sector_row = df.groupby("sector")["price"].median().sort_values(ascending=False).head(1)
top_sector, top_val = top_sector_row.index[0], top_sector_row.iloc[0]
n_luxury = int((df["luxury_category"] == "high").sum())

def metric_card(col, label, value, sub=""):
    col.markdown(f"""
    <div class="mi-metric">
      <div class="lbl">{label}</div>
      <div class="val">{value}</div>
      <div class="sub">{sub}</div>
    </div>
    """, unsafe_allow_html=True)

metric_card(c1, "Median Price", format_inr(median_cr), "All comparables")
metric_card(c2, "Median ₹/sq.ft.", f"₹ {avg_psf:,.0f}", "Blended, city-wide")
metric_card(c3, "Priciest Sector", top_sector.title(), f"Median · {format_inr(top_val)}")
metric_card(c4, "High-luxury stock", f"{n_luxury:,}", f"{n_luxury/len(df)*100:.1f}% of dataset")
st.markdown('</div>', unsafe_allow_html=True)

# ---- Ornamental divider --------------------------------------------------
st.markdown("""
<div class="mi-ornament">
  <div class="line"></div>
  <div class="diamond">◈</div>
  <div class="line"></div>
</div>
""", unsafe_allow_html=True)

# ---- Plotly theme -------------------------------------------------------
GOLD_SCALE = [(0.0, "#3B2E10"), (0.35, "#8C6E24"), (0.7, "#D4AF37"), (1.0, "#FFF6DA")]
PLOT_BG = "rgba(0,0,0,0)"

def dark_layout(fig, title=None, height=420):
    fig.update_layout(
        title=dict(text=title, font=dict(family="Fraunces", color="#F5F1E6", size=20)) if title else None,
        paper_bgcolor=PLOT_BG, plot_bgcolor=PLOT_BG,
        font=dict(family="Inter Tight", color="#A9A196", size=12),
        margin=dict(l=20, r=20, t=50 if title else 20, b=20),
        height=height,
        xaxis=dict(gridcolor="rgba(212,175,55,0.08)", zeroline=False, linecolor="rgba(212,175,55,0.15)"),
        yaxis=dict(gridcolor="rgba(212,175,55,0.08)", zeroline=False, linecolor="rgba(212,175,55,0.15)"),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#F5F1E6")),
        hoverlabel=dict(bgcolor="#141418", bordercolor=GOLD, font=dict(family="Inter Tight", color="#F5F1E6")),
    )
    return fig

# ---- Tabs ---------------------------------------------------------------
st.markdown('<div class="mi-animated-section" style="animation-delay: 0.3s">', unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs(["Sector Ranking", "Distribution", "Sector Deep-Dive"])

with tab1:
    top_n = st.slider("Number of sectors", 10, 40, 20, key="topn")
    ranked = df.groupby("sector")["price"].median().sort_values(ascending=True).tail(top_n)
    ranked_df = ranked.reset_index()
  # st.markdown('<div class="mi-glass-panel">', unsafe_allow_html=True)
    fig = go.Figure(go.Bar(
        x=ranked_df["price"], y=ranked_df["sector"].str.title(), orientation="h",
        marker=dict(
            color=ranked_df["price"], colorscale=GOLD_SCALE, showscale=False,
            line=dict(color="rgba(212,175,55,0.35)", width=0.5),
        ),
        hovertemplate="<b>%{y}</b><br>Median · ₹ %{x:.2f} Cr<extra></extra>",
    ))
    dark_layout(fig, "Median valuation by sector (Cr)", height=560)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    left, right = st.columns([1, 1], gap="large")

    with left:
   #    st.markdown('<div class="mi-glass-panel">', unsafe_allow_html=True)
        fig = px.histogram(df, x="price", nbins=50,
                           color_discrete_sequence=[GOLD])
        fig.update_traces(marker_line_color="rgba(11,11,13,0.4)", marker_line_width=1, opacity=0.9)
        dark_layout(fig, "Price distribution (Cr)", height=380)
        fig.update_xaxes(title="Price (Cr)"); fig.update_yaxes(title="Listings")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
    #   st.markdown('<div class="mi-glass-panel">', unsafe_allow_html=True)
        fig = px.scatter(df.sample(min(1500, len(df)), random_state=1),
                         x="built_up_area", y="price", color="luxury_category",
                         color_discrete_map={"low": "#8C6E24", "medium": GOLD_SOFT, "high": GOLD},
                         opacity=0.75, hover_data=["sector", "bedRoom"])
        fig.update_traces(marker=dict(size=7, line=dict(width=0)))
        dark_layout(fig, "Area vs. price · by luxury tier", height=380)
        fig.update_xaxes(title="Built-up area (sq. ft.)"); fig.update_yaxes(title="Price (Cr)")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    sectors = sorted(df["sector"].unique())
    default_ix = sectors.index("golf course road") if "golf course road" in sectors else 0
    sector = st.selectbox("Choose sector", sectors, index=default_ix, key="deepdive")
    sub = df[df["sector"] == sector]

    a, b, c, d = st.columns(4, gap="medium")
    metric_card(a, "Listings", f"{len(sub):,}")
    metric_card(b, "Median price", format_inr(sub["price"].median()))
    metric_card(c, "Median ₹/sq.ft.", f"₹ {((sub['price']*1e7)/sub['built_up_area']).median():,.0f}")
    metric_card(d, "Median size", f"{sub['built_up_area'].median():,.0f} sq.ft.")

    st.markdown("""
    <div class="mi-ornament" style="margin: 1.5rem auto;">
      <div class="line"></div>
      <div class="diamond">◈</div>
      <div class="line"></div>
    </div>
    """, unsafe_allow_html=True)

    lc, rc = st.columns([1, 1], gap="large")
    with lc:
    #   st.markdown('<div class="mi-glass-panel">', unsafe_allow_html=True)
        by_bhk = sub.groupby("bedRoom")["price"].median().reset_index()
        fig = px.bar(by_bhk, x="bedRoom", y="price",
                     color="price", color_continuous_scale=GOLD_SCALE)
        fig.update_coloraxes(showscale=False)
        dark_layout(fig, f"{sector.title()} · median price by BHK", height=360)
        fig.update_xaxes(title="Bedrooms"); fig.update_yaxes(title="Median price (Cr)")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with rc:
    #   st.markdown('<div class="mi-glass-panel">', unsafe_allow_html=True)
        fig = px.box(sub, x="luxury_category", y="price",
                     category_orders={"luxury_category": ["low", "medium", "high"]},
                     color="luxury_category",
                     color_discrete_map={"low": "#8C6E24", "medium": GOLD_SOFT, "high": GOLD})
        fig.update_traces(marker=dict(line=dict(color="rgba(212,175,55,0.35)")))
        dark_layout(fig, f"{sector.title()} · price by luxury tier", height=360)
        fig.update_xaxes(title=""); fig.update_yaxes(title="Price (Cr)")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="mi-ornament" style="margin: 1.5rem auto;">
      <div class="line"></div>
      <div class="diamond">◈</div>
      <div class="line"></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-eyebrow">Comparables</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title" style="font-size:1.5rem">Sample transactions · <em>{sector.title()}</em></div>', unsafe_allow_html=True)
    show = sub.sample(min(12, len(sub)), random_state=3).copy()
    show["price"] = show["price"].apply(format_inr)
    show = show[["property_type", "bedRoom", "bathroom", "built_up_area",
                 "furnishing_type", "luxury_category", "agePossession", "price"]]
    show.columns = ["Type", "BHK", "Baths", "Area (sqft)", "Furnishing", "Luxury", "Possession", "Price"]
    st.dataframe(show, use_container_width=True, hide_index=True)

st.markdown('</div>', unsafe_allow_html=True)

# ---- Footer -------------------------------------------------------------
st.markdown("""
<div class="mi-animated-section" style="animation-delay: 0.5s">
  <div class="mi-footer">
    <div class="mi-footer-inner">
      <span>© Aurea Estates · Est. 2026</span>
      <span>Analytics derived from the modelled comparable set.</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)