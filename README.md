# House Price Prediction

A machine learning project designed to clean, preprocess, and model house/flat data for price prediction.

## Directory Structure

The project has been structured as a standard data science project to keep data and analysis files organized:

```text
House Prediction/
├── data/
│   ├── raw/                      # Original, unmodified data files
│   │   ├── flats.csv             # Raw flat listings dataset
│   │   └── independent-house.csv # Raw independent houses dataset
│   └── processed/                # Cleaned and processed data files ready for modeling
│       └── flats_cleaned.csv     # Cleaned flat listings dataset
├── notebooks/                    # Jupyter Notebooks for analysis and preprocessing
│   └── data-preprocessing-flats.ipynb
├── requirements.txt              # Required python dependencies
└── README.md                     # Project documentation
```

## Setup Instructions

1. **Create/Activate Virtual Environment**:
   If not already activated, activate the virtual environment at the root folder:
   - On Windows (PowerShell):
     ```powershell
     .venv\Scripts\Activate.ps1
     ```
   - On Linux/macOS:
     ```bash
     source .venv/bin/activate
     ```

2. **Install Dependencies**:
   Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Preprocessing**:
   Open and execute the cells in [data-preprocessing-flats.ipynb](file:///C:/Projects/House%20Prediction/notebooks/data-preprocessing-flats.ipynb) to load the raw flat listings from `data/raw/flats.csv`, perform cleaning, and save the result to `data/processed/flats_cleaned.csv`.
