""""Aurea Estates — The Guide"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
from theme import inject_theme, render_nav

st.set_page_config(page_title="Aurea · The Guide", page_icon="◈",
                   layout="wide", initial_sidebar_state="collapsed")
inject_theme()
render_nav(active="guide")

st.markdown('<div class="section-eyebrow">The Guide</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">How Aurea reads a <em>home</em>.</div>', unsafe_allow_html=True)

st.markdown("""
<div style="max-width: 780px; color: var(--text); line-height: 1.7; font-size: 1.02rem;">
<p class="muted" style="font-size: 1.05rem;">There is no single "market price" for a Gurgaon home — only a defensible range, shaped by twelve quiet variables. Aurea makes those variables visible.</p>

<h3 style="margin-top: 34px;">The twelve signals</h3>
<ol style="padding-left: 20px; margin-top: 12px;">
  <li><b>Sector.</b> The single strongest predictor. Golf Course Road and the older DLF phases command a persistent premium.</li>
  <li><b>Property type.</b> Independent floors and villas carry a modest premium over apartments of the same footprint.</li>
  <li><b>Configuration.</b> Bedroom and bathroom counts anchor buyer expectations more than raw square footage.</li>
  <li><b>Built-up area.</b> The lever of scale — but with diminishing returns above ~4,000 sq. ft. in most sectors.</li>
  <li><b>Balconies.</b> Small in isolation, meaningful in aggregate — particularly at the mid & high floors.</li>
  <li><b>Possession age.</b> New and under-construction stock commands a premium; the 8–15 year band is the buyer's sweet spot.</li>
  <li><b>Furnishing.</b> Full furnishing typically adds 8–12%.</li>
  <li><b>Luxury tier.</b> The most volatile signal. The "high" tier can add 40–50% over comparable "low" stock.</li>
  <li><b>Floor position.</b> High floors command 4–8% over ground/low floors in most towers.</li>
  <li><b>Servant room.</b> A defining feature for the 4BHK+ segment; adds 2–4%.</li>
  <li><b>Store room.</b> A subtle differentiator that quietly buys forgiveness on other trade-offs.</li>
  <li><b>Micro-orientation.</b> Not modelled directly, but reflected in the negotiation band we return.</li>
</ol>

<h3 style="margin-top: 40px;">How to read the valuation</h3>
<p>Our point estimate is the model's <em>most defensible</em> number. The band around it is the range within which a well-briefed buyer and a well-briefed seller would credibly settle. If your target price sits outside the band, the market is telling you something.</p>

<h3 style="margin-top: 40px;">A note on discretion</h3>
<p class="muted">Aurea does not list, broker, or share your inputs. This is a tool for you — a second opinion, delivered without a commission attached.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="margin-top:80px; padding-top:30px; border-top:1px solid var(--line);
     display:flex; justify-content:space-between; color:var(--mute); font-size:0.82rem; letter-spacing:.14em; text-transform:uppercase;">
  <div>© Aurea Estates · Est. 2026</div>
  <div>A private valuation atelier.</div>
</div>
""", unsafe_allow_html=True)