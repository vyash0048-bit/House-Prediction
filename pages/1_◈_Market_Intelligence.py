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
render_nav(active="intelligence")

df = load_df()

# ---- Header -------------------------------------------------------------
st.markdown('<div class="section-eyebrow">Market Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">A quiet read on <em>Gurgaon</em>.</div>', unsafe_allow_html=True)
st.markdown('<p class="muted" style="margin-top:-20px; max-width:720px;">'
            'A curated view of the 5,000 comparables in our model — segmented by sector, luxury tier and possession, so you can benchmark like a buyer with better information than the room.</p>',
            unsafe_allow_html=True)

# ---- KPI strip ----------------------------------------------------------
c1, c2, c3, c4 = st.columns(4, gap="medium")
median_cr = df["price"].median()
avg_psf = ((df["price"] * 1e7) / df["built_up_area"]).median()
top_sector_row = df.groupby("sector")["price"].median().sort_values(ascending=False).head(1)
top_sector, top_val = top_sector_row.index[0], top_sector_row.iloc[0]
n_luxury = int((df["luxury_category"] == "high").sum())

def metric_card(col, label, value, sub=""):
    col.markdown(f"""
    <div class="metric">
      <div class="lbl">{label}</div>
      <div class="val">{value}</div>
      <div class="sub">{sub}</div>
    </div>
    """, unsafe_allow_html=True)

metric_card(c1, "Median Price", format_inr(median_cr), "All comparables")
metric_card(c2, "Median ₹/sq.ft.", f"₹ {avg_psf:,.0f}", "Blended, city-wide")
metric_card(c3, "Priciest Sector", top_sector.title(), f"Median · {format_inr(top_val)}")
metric_card(c4, "High-luxury stock", f"{n_luxury:,}", f"{n_luxury/len(df)*100:.1f}% of dataset")

st.markdown('<div style="height: 40px"></div>', unsafe_allow_html=True)

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
tab1, tab2, tab3 = st.tabs(["Sector Ranking", "Distribution", "Sector Deep-Dive"])

with tab1:
    top_n = st.slider("Number of sectors", 10, 40, 20, key="topn")
    ranked = df.groupby("sector")["price"].median().sort_values(ascending=True).tail(top_n)
    ranked_df = ranked.reset_index()
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

with tab2:
    left, right = st.columns([1, 1], gap="large")

    with left:
        fig = px.histogram(df, x="price", nbins=50,
                           color_discrete_sequence=[GOLD])
        fig.update_traces(marker_line_color="rgba(11,11,13,0.4)", marker_line_width=1, opacity=0.9)
        dark_layout(fig, "Price distribution (Cr)", height=380)
        fig.update_xaxes(title="Price (Cr)"); fig.update_yaxes(title="Listings")
        st.plotly_chart(fig, use_container_width=True)

    with right:
        fig = px.scatter(df.sample(min(1500, len(df)), random_state=1),
                         x="built_up_area", y="price", color="luxury_category",
                         color_discrete_map={"low": "#8C6E24", "medium": GOLD_SOFT, "high": GOLD},
                         opacity=0.75, hover_data=["sector", "bedRoom"])
        fig.update_traces(marker=dict(size=7, line=dict(width=0)))
        dark_layout(fig, "Area vs. price · by luxury tier", height=380)
        fig.update_xaxes(title="Built-up area (sq. ft.)"); fig.update_yaxes(title="Price (Cr)")
        st.plotly_chart(fig, use_container_width=True)

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

    st.markdown('<div style="height: 24px"></div>', unsafe_allow_html=True)
    lc, rc = st.columns([1, 1], gap="large")
    with lc:
        by_bhk = sub.groupby("bedRoom")["price"].median().reset_index()
        fig = px.bar(by_bhk, x="bedRoom", y="price",
                     color="price", color_continuous_scale=GOLD_SCALE)
        fig.update_coloraxes(showscale=False)
        dark_layout(fig, f"{sector.title()} · median price by BHK", height=360)
        fig.update_xaxes(title="Bedrooms"); fig.update_yaxes(title="Median price (Cr)")
        st.plotly_chart(fig, use_container_width=True)
    with rc:
        fig = px.box(sub, x="luxury_category", y="price",
                     category_orders={"luxury_category": ["low", "medium", "high"]},
                     color="luxury_category",
                     color_discrete_map={"low": "#8C6E24", "medium": GOLD_SOFT, "high": GOLD})
        fig.update_traces(marker=dict(line=dict(color="rgba(212,175,55,0.35)")))
        dark_layout(fig, f"{sector.title()} · price by luxury tier", height=360)
        fig.update_xaxes(title=""); fig.update_yaxes(title="Price (Cr)")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div style="height: 24px"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-eyebrow">Comparables</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title" style="font-size:1.5rem">Sample transactions · <em>{sector.title()}</em></div>', unsafe_allow_html=True)
    show = sub.sample(min(12, len(sub)), random_state=3).copy()
    show["price"] = show["price"].apply(format_inr)
    show = show[["property_type", "bedRoom", "bathroom", "built_up_area",
                 "furnishing_type", "luxury_category", "agePossession", "price"]]
    show.columns = ["Type", "BHK", "Baths", "Area (sqft)", "Furnishing", "Luxury", "Possession", "Price"]
    st.dataframe(show, use_container_width=True, hide_index=True)

# ---- Footer -------------------------------------------------------------
st.markdown("""
<div style="margin-top:70px; padding-top:30px; border-top:1px solid var(--line);
     display:flex; justify-content:space-between; color:var(--mute); font-size:0.82rem; letter-spacing:.14em; text-transform:uppercase;">
  <div>© Aurea Estates · Est. 2026</div>
  <div>Analytics derived from the modelled comparable set.</div>
</div>
""", unsafe_allow_html=True)