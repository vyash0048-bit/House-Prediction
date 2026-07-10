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

# ── Page-specific luxury CSS ─────────────────────────────────────────
st.markdown("""
<style>
    /* ═══════════════════════════════════════════════════════════════
       GUIDE PAGE — HYPER-LUXURY ANIMATIONS & PREMIUM UI
       ═══════════════════════════════════════════════════════════════ */

    /* ── Keyframes ─────────────────────────────────────────────── */
    @keyframes guideRevealUp {
        0%   { opacity: 0; transform: translateY(44px) scale(0.97); filter: blur(6px); }
        100% { opacity: 1; transform: translateY(0) scale(1);       filter: blur(0);   }
    }

    @keyframes goldUnderlineGrow {
        0%   { width: 0;    opacity: 0; }
        100% { width: 56px; opacity: 1; }
    }

    @keyframes listItemSlideIn {
        0%   { opacity: 0; transform: translateX(-28px); }
        100% { opacity: 1; transform: translateX(0);     }
    }

    @keyframes borderGlowPulse {
        0%, 100% { border-color: rgba(212, 175, 55, 0.18); box-shadow: 0 0 30px rgba(212, 175, 55, 0.03); }
        50%      { border-color: rgba(212, 175, 55, 0.40); box-shadow: 0 0 50px rgba(212, 175, 55, 0.08); }
    }

    @keyframes footerLineExpand {
        0%   { width: 0%;   opacity: 0; }
        100% { width: 100%; opacity: 1; }
    }

    @keyframes diamondPulse {
        0%, 100% { opacity: 0.5; transform: scale(1);   }
        50%      { opacity: 1;   transform: scale(1.15); }
    }

    @keyframes subtleGlow {
        0%, 100% { text-shadow: 0 0 6px rgba(212, 175, 55, 0.0); }
        50%      { text-shadow: 0 0 18px rgba(212, 175, 55, 0.18); }
    }

    /* ── Animated entrance wrapper ─────────────────────────────── */
    .guide-animated-section {
        animation: guideRevealUp 1.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        opacity: 0;
    }
    .guide-animated-section.delay-1 { animation-delay: 0.10s; }
    .guide-animated-section.delay-2 { animation-delay: 0.30s; }
    .guide-animated-section.delay-3 { animation-delay: 0.50s; }

    /* ── Ornamental diamond divider ────────────────────────────── */
    .guide-ornament {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 18px;
        margin: 30px 0 44px 0;
        animation: guideRevealUp 1.2s 0.25s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        opacity: 0;
    }
    .guide-ornament .orn-line {
        flex: 1;
        max-width: 180px;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.45), transparent);
    }
    .guide-ornament .orn-diamond {
        color: #D4AF37;
        font-size: 0.92rem;
        animation: diamondPulse 4s ease-in-out infinite;
        text-shadow: 0 0 12px rgba(212, 175, 55, 0.30);
    }

    /* ── Glass panel container with animated border glow ───────── */
    .guide-glass-panel {
        max-width: 820px;
        background: linear-gradient(165deg,
            rgba(212, 175, 55, 0.025) 0%,
            rgba(15, 15, 18, 0.75)   35%,
            rgba(10, 10, 12, 0.85)   100%);
        backdrop-filter: blur(24px) saturate(1.2);
        -webkit-backdrop-filter: blur(24px) saturate(1.2);
        border: 1px solid rgba(212, 175, 55, 0.18);
        border-radius: 18px;
        padding: 52px 56px 48px;
        position: relative;
        overflow: hidden;
        animation: borderGlowPulse 6s ease-in-out infinite;
        box-shadow:
            0 20px 60px rgba(0, 0, 0, 0.50),
            inset 0 1px 0 rgba(212, 175, 55, 0.08);
    }
    /* Top-edge gold gradient accent */
    .guide-glass-panel::before {
        content: '';
        position: absolute;
        top: 0; left: 10%; right: 10%;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.5), transparent);
    }
    /* Subtle corner glow */
    .guide-glass-panel::after {
        content: '';
        position: absolute;
        top: -60px; right: -60px;
        width: 200px; height: 200px;
        background: radial-gradient(circle, rgba(212, 175, 55, 0.04) 0%, transparent 70%);
        pointer-events: none;
    }

    /* ── Typography: h3 headings ───────────────────────────────── */
    .guide-glass-panel h3 {
        font-family: 'Cinzel', serif !important;
        font-size: 1.30rem !important;
        font-weight: 700 !important;
        color: #F5F1E6 !important;
        letter-spacing: 0.12em !important;
        text-transform: uppercase;
        margin-top: 44px !important;
        margin-bottom: 18px !important;
        padding-left: 20px;
        border-left: 3px solid #D4AF37;
        position: relative;
        line-height: 1.4 !important;
        animation: subtleGlow 5s ease-in-out infinite;
    }
    /* Gold underline that animates in */
    .guide-glass-panel h3::after {
        content: '';
        display: block;
        margin-top: 10px;
        height: 2px;
        background: linear-gradient(90deg, #D4AF37, rgba(212, 175, 55, 0.15));
        border-radius: 2px;
        animation: goldUnderlineGrow 1.0s 0.8s cubic-bezier(0.22, 1, 0.36, 1) forwards;
        width: 0;
        opacity: 0;
    }

    /* ── Styled ordered list with golden markers ───────────────── */
    .guide-glass-panel ol {
        list-style: none !important;
        counter-reset: guide-counter;
        padding-left: 0 !important;
        margin-top: 16px !important;
    }
    .guide-glass-panel ol li {
        counter-increment: guide-counter;
        position: relative;
        padding-left: 52px;
        margin-bottom: 18px;
        color: #E8E4D9;
        line-height: 1.75;
        font-size: 1.01rem;
        opacity: 0;
        animation: listItemSlideIn 0.7s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    /* Stagger each item */
    .guide-glass-panel ol li:nth-child(1)  { animation-delay: 0.55s; }
    .guide-glass-panel ol li:nth-child(2)  { animation-delay: 0.63s; }
    .guide-glass-panel ol li:nth-child(3)  { animation-delay: 0.71s; }
    .guide-glass-panel ol li:nth-child(4)  { animation-delay: 0.79s; }
    .guide-glass-panel ol li:nth-child(5)  { animation-delay: 0.87s; }
    .guide-glass-panel ol li:nth-child(6)  { animation-delay: 0.95s; }
    .guide-glass-panel ol li:nth-child(7)  { animation-delay: 1.03s; }
    .guide-glass-panel ol li:nth-child(8)  { animation-delay: 1.11s; }
    .guide-glass-panel ol li:nth-child(9)  { animation-delay: 1.19s; }
    .guide-glass-panel ol li:nth-child(10) { animation-delay: 1.27s; }
    .guide-glass-panel ol li:nth-child(11) { animation-delay: 1.35s; }
    .guide-glass-panel ol li:nth-child(12) { animation-delay: 1.43s; }

    /* Golden numbered counter marker */
    .guide-glass-panel ol li::before {
        content: counter(guide-counter, decimal-leading-zero);
        position: absolute;
        left: 0;
        top: 1px;
        font-family: 'Cinzel', serif;
        font-size: 0.88rem;
        font-weight: 700;
        color: #D4AF37;
        width: 36px;
        height: 36px;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 1px solid rgba(212, 175, 55, 0.30);
        border-radius: 8px;
        background: rgba(212, 175, 55, 0.05);
        text-shadow: 0 0 8px rgba(212, 175, 55, 0.15);
    }

    /* Bold text in gold */
    .guide-glass-panel b,
    .guide-glass-panel strong {
        color: #D4AF37 !important;
        font-weight: 700;
    }

    /* Emphasized text with subtle gold */
    .guide-glass-panel em {
        color: #D4AF37;
        font-style: italic;
    }

    /* Body paragraphs */
    .guide-glass-panel p {
        color: var(--text);
        line-height: 1.8;
        font-size: 1.03rem;
    }
    .guide-glass-panel p.muted {
        color: #B5B0A5;
        font-size: 1.06rem;
        line-height: 1.7;
        font-weight: 400;
    }

    /* ── Discretion note as elegant blockquote ──────────────────── */
    .guide-discretion-wrap {
        margin-top: 42px;
        padding: 26px 30px 26px 28px;
        border-left: 3px solid #D4AF37;
        border-radius: 0 12px 12px 0;
        background: linear-gradient(135deg,
            rgba(212, 175, 55, 0.035) 0%,
            rgba(10, 10, 12, 0.5) 100%);
        backdrop-filter: blur(8px);
        position: relative;
    }
    .guide-discretion-wrap::before {
        content: '';
        position: absolute;
        top: 8px; bottom: 8px; left: -1px;
        width: 3px;
        background: linear-gradient(180deg, #D4AF37, rgba(212, 175, 55, 0.15));
        border-radius: 2px;
    }
    .guide-discretion-wrap h3 {
        margin-top: 0 !important;
        border-left: none !important;
        padding-left: 0 !important;
    }
    .guide-discretion-wrap p.muted {
        margin-bottom: 0;
    }

    /* ── Animated footer ───────────────────────────────────────── */
    .guide-footer {
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
        animation: guideRevealUp 1.0s 1.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    .guide-footer::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        height: 1px;
        background: linear-gradient(90deg,
            rgba(212, 175, 55, 0.05),
            rgba(212, 175, 55, 0.50) 50%,
            rgba(212, 175, 55, 0.05));
        animation: footerLineExpand 1.8s 1.4s cubic-bezier(0.22, 1, 0.36, 1) forwards;
        width: 0;
        opacity: 0;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────
st.markdown('<div class="guide-animated-section delay-1">', unsafe_allow_html=True)
st.markdown('<div class="section-eyebrow">The Guide</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">How Aurea reads a <em>home</em>.</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── Ornamental divider ───────────────────────────────────────────────
st.markdown("""
<div class="guide-ornament">
  <div class="orn-line"></div>
  <div class="orn-diamond">◈</div>
  <div class="orn-line"></div>
</div>
""", unsafe_allow_html=True)

# ── Main content in glass panel ──────────────────────────────────────
st.markdown('<div class="guide-animated-section delay-2">', unsafe_allow_html=True)
st.markdown("""
<div class="guide-glass-panel">
<p class="muted" style="font-size: 1.05rem;">There is no single "market price" for a Gurgaon home — only a defensible range, shaped by twelve quiet variables. Aurea makes those variables visible.</p>

<h3>The twelve signals</h3>
<ol>
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

<h3>How to read the valuation</h3>
<p>Our point estimate is the model's <em>most defensible</em> number. The band around it is the range within which a well-briefed buyer and a well-briefed seller would credibly settle. If your target price sits outside the band, the market is telling you something.</p>

<div class="guide-discretion-wrap">
  <h3>A note on discretion</h3>
  <p class="muted">Aurea does not list, broker, or share your inputs. This is a tool for you — a second opinion, delivered without a commission attached.</p>
</div>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── Animated footer ──────────────────────────────────────────────────
st.markdown("""
<div class="guide-footer">
  <div>© Aurea Estates · Est. 2026</div>
  <div>A private valuation atelier.</div>
</div>
""", unsafe_allow_html=True)