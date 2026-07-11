<div align="center">
  <img src="assets/hero_banner.jpg" alt="Aurea Estates valuation dashboard hero" width="100%">

  <br><br>

  <img src="https://readme-typing-svg.demolab.com?font=Playfair+Display&weight=700&size=34&duration=2800&pause=800&color=D4AF37&center=true&vCenter=true&width=900&lines=AUREA+ESTATES;Gurgaon+Real+Estate+Valuation+Engine;Premium+ML+Pricing+Intelligence" alt="Animated Aurea Estates title">

  <p>
    <strong>A luxury-styled Streamlit intelligence suite for Gurgaon property valuation, market exploration, and pricing confidence.</strong>
  </p>

  <p>
    <a href="https://house-prediction-77ywtbegrhhimdh3uvqqqf.streamlit.app/">
      <img src="https://img.shields.io/badge/Live_App-Launch_Aurea-D4AF37?style=for-the-badge&logo=streamlit&logoColor=white" alt="Live app">
    </a>
    <a href="https://streamlit.io/">
      <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
    </a>
    <a href="https://scikit-learn.org/">
      <img src="https://img.shields.io/badge/scikit--learn-1.7.2-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="scikit-learn">
    </a>
    <a href="https://plotly.com/">
      <img src="https://img.shields.io/badge/Plotly-Interactive_Charts-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" alt="Plotly">
    </a>
  </p>

  <h3>
    <a href="https://house-prediction-77ywtbegrhhimdh3uvqqqf.streamlit.app/">Open the deployed app</a>
  </h3>
</div>

---

## Preview

<div align="center">
  <table>
    <tr>
      <td align="center" width="33%">
        <img src="https://img.shields.io/badge/Valuation-Engine-111111?style=flat-square&labelColor=D4AF37" alt="Valuation engine">
        <br>
        Predicts defensible market value from core property signals.
      </td>
      <td align="center" width="33%">
        <img src="https://img.shields.io/badge/Market-Intelligence-111111?style=flat-square&labelColor=D4AF37" alt="Market intelligence">
        <br>
        Explores pricing patterns, sectors, distributions, and outliers.
      </td>
      <td align="center" width="33%">
        <img src="https://img.shields.io/badge/Luxury-Interface-111111?style=flat-square&labelColor=D4AF37" alt="Luxury interface">
        <br>
        Uses custom CSS, premium visuals, and interactive Plotly charts.
      </td>
    </tr>
  </table>
</div>

---

## What It Does

Aurea Estates turns curated Gurgaon housing data into an interactive valuation experience. The app combines a trained scikit-learn pipeline with a polished Streamlit interface so users can estimate property value, inspect market segments, and understand the variables behind price movement.

The experience is designed like a premium real-estate atelier: cinematic hero imagery, gold-accented controls, glass-style panels, animated sections, and dashboard views built for quick scanning.

---

## Core Signals

| Signal | Why It Matters |
|---|---|
| Sector | Captures location premium and neighborhood demand. |
| Property type | Separates flat and house behavior. |
| Bedrooms and bathrooms | Models configuration and livability. |
| Built-up area | Measures scale and usable footprint. |
| Balcony count | Adds amenity and layout context. |
| Age / possession | Reflects readiness, vintage, and construction phase. |
| Servant room / store room | Captures utility and premium inventory markers. |
| Furnishing type | Distinguishes furnished, semi-furnished, and unfurnished properties. |
| Luxury category | Encodes quality tier and finish level. |
| Floor category | Adds floor-position preference and elevation effect. |

---

## Tech Stack

<div align="center">

| Layer | Tools |
|---|---|
| App | Streamlit |
| Modeling | scikit-learn, category-encoders, XGBoost |
| Data | pandas, NumPy |
| Charts | Plotly, Matplotlib, Seaborn |
| Model storage | Git LFS |
| Styling | Custom CSS in Streamlit |

</div>

---

## Repository Map

```text
House Prediction/
├── app.py                         # Main Streamlit valuation dashboard
├── theme.py                       # Design system, styling, and shared UI helpers
├── pages/
│   ├── 1_◈_Market_Intelligence.py # Analytics and market exploration
│   └── 2_◈_The_Guide.py           # Methodology and user guide
├── assets/
│   └── hero_banner.jpg            # README and app hero visual
├── data/
│   ├── raw/                       # Original datasets
│   └── processed/                 # Cleaned datasets used by the app
├── models/
│   ├── df.pkl                     # Supporting serialized data
│   └── pipeline.pkl               # Git LFS model artifact
├── notebooks/                     # EDA, feature engineering, and model training
└── requirements.txt               # Python dependencies
```

---

## Run Locally

Clone the project:

```bash
git clone https://github.com/vyash0048-bit/House-Prediction.git
cd House-Prediction
```

Install Git LFS and fetch the model:

```bash
git lfs install
git lfs pull
```

Create or activate your Python environment, then install dependencies:

```bash
pip install -r requirements.txt
```

Launch the app:

```bash
streamlit run app.py
```

The local app opens at:

```text
http://localhost:8501/
```

---

## Deployment

The app is live here:

<div align="center">
  <a href="https://house-prediction-77ywtbegrhhimdh3uvqqqf.streamlit.app/">
    <img src="https://img.shields.io/badge/Launch_Deployed_App-Aurea_Estates-D4AF37?style=for-the-badge&logo=streamlit&logoColor=white" alt="Launch deployed app">
  </a>
</div>

`models/pipeline.pkl` is stored with Git LFS because the model is too large for normal GitHub file storage. For deployment, make sure the host pulls LFS files during build.

The app also supports a fallback `MODEL_URL` secret. If the deployed server does not receive the LFS model file, upload `pipeline.pkl` to a direct-download location and set:

```toml
MODEL_URL = "https://your-direct-download-link/pipeline.pkl"
```

---

## Project Flow

```mermaid
flowchart LR
    A["Raw Gurgaon listings"] --> B["Cleaning and preprocessing"]
    B --> C["Feature engineering"]
    C --> D["Model selection"]
    D --> E["Serialized pipeline.pkl"]
    E --> F["Streamlit valuation engine"]
    C --> G["Market intelligence dashboard"]
```

---

## Model Notes

The production model is a serialized scikit-learn pipeline. It expects the app inputs to match the training schema exactly, including categorical values such as `furnished`, `semifurnished`, and `unfurnished`.

`requirements.txt` pins `scikit-learn==1.7.2` so the deployed runtime matches the version used to create the model artifact.

---

<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&height=120&color=0:D4AF37,100:111111&section=footer&text=Aurea%20Estates&fontColor=ffffff&fontSize=28&animation=fadeIn" alt="Animated footer wave">
  <p><em>There is no single market price, only a defensible range. Aurea makes the range visible.</em></p>
</div>
