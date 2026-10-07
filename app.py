import json
from pathlib import Path
import pandas as pd
import streamlit as st

# --- STREAMLIT PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Drug-Disease Link Predictor", page_icon="🧬", layout="wide"
)
# --- AUMENTO DIMENSIONE FONT GLOBALE E TITOLO (CSS CORRETTO) ---
st.markdown(
    """
    <style>
    /* 1. Font generale di base per i testi normali */
    html, body, p, label, span {
        font-size: 1.1rem;
    }

    /* 2. Dimensione specifica per le caption */
    [data-testid="stCaptionContainer"] p {
        font-size: 1.15rem !important;
    }

    /* 3. Riduzione specifica per il menu a tendina (selectbox) */
    div[data-testid="stSelectbox"] label,
    div[data-testid="stSelectbox"] label p,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] *,
    div[data-baseweb="popover"] *,
    ul[role="listbox"] li * {
        font-size: 0.85rem !important;
    }

    /* 4. Titolo principale (posizionato alla fine per prevalere su tutto) */
    h1, h1 *, [data-testid="stHeader"] h1, [data-testid="stHeadingWithTitle"] * {
        font-size: 2.25rem !important;
        line-height: 1.2 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
# --- APPLICATION TITLE ---
st.title("🧬 Drug-Disease Link Predictor")

# 1. RIASSUNTO BREVE DELLA CAPTION (SOPRA LA BARRA DI RICERCA)
st.caption(
    "Predictions were generated based on Probabilistic Network Inference for drug repurposing."
)


# --- LOAD DATA WITH CACHING ---
@st.cache_data
def load_data():
    drugs_file = Path("drugs.json")
    diseases_file = Path("diseases.json")

    drugs_data = {}
    diseases_data = {}

    if drugs_file.exists():
        with open(drugs_file, "r", encoding="utf-8") as f:
            drugs_data = json.load(f)

    if diseases_file.exists():
        with open(diseases_file, "r", encoding="utf-8") as f:
            diseases_data = json.load(f)

    return drugs_data, diseases_data


drugs_data, diseases_data = load_data()


# 2. BARRA DI RICERCA (ST.RADIO)
search_mode = st.radio(
    "Select search mode:",
    options=["Search by Disease", "Search by Drug"],
    horizontal=True,
)



# --- 4. DROPDOWN SEARCH & TABLE DISPLAY ---
if search_mode == "Search by Disease":
    if not diseases_data:
        st.error(
            "File 'diseases.json' was not found or is empty in the current directory."
        )
    else:
        disease_list = sorted(list(diseases_data.keys()))

        selected_disease = st.selectbox(
            "Select a Disease from the dropdown menu:",
            options=disease_list,
            index=None,
            placeholder="Type or select a disease to search...",
        )

        if selected_disease:
            predictions = diseases_data.get(selected_disease, [])
            st.subheader(
                f"Predicted Candidate Drugs for:  **{selected_disease}** "
            )

            if predictions:
                df = pd.DataFrame(predictions)
                if "score" in df.columns:
                    df = df.drop(columns=["score"])

                df.index = [f"#{i+1}" for i in range(len(df))]
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No predictions found for the selected disease.")

else:
    if not drugs_data:
        st.error(
            "File 'drugs.json' was not found or is empty in the current directory."
        )
    else:
        drug_list = sorted(list(drugs_data.keys()))

        selected_drug = st.selectbox(
            "Select a Drug from the dropdown menu:",
            options=drug_list,
            index=None,
            placeholder="Type or select a drug to search...",
        )

        if selected_drug:
            predictions = drugs_data.get(selected_drug, [])
            st.subheader(
                f"Predicted Candidate Diseases for:  **{selected_drug}** "
            )

            if predictions:
                df = pd.DataFrame(predictions)
                if "score" in df.columns:
                    df = df.drop(columns=["score"])

                df.index = [f"#{i+1}" for i in range(len(df))]
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No predictions found for the selected drug.")

# 3. CAPTION DETTAGLIATA (SOTTO LA BARRA DI RICERCA)
st.caption(
    """
    **About the Data & Predictions**  

    Link prediction is a mathematical method that analyzes known connections within a network to estimate the likelihood of undiscovered links.  
    This application uses the verified database of therapeutic associations curated by **Newman and Polanco** to suggest potential candidates for **drug repurposing**.
    
    
    **Key Limitations & Disclaimer:**

    Predictions are**Topology-Based:** they rely strictly on network structure and observed interactions. **The model does not account for side effects, drug-drug interactions, or patient comorbidities.**
    Predictions were generated using stochastic algorithms, therefore these predictions are preliminary research suggestions for early-stage screening and **must be validated by medical and pharmacological experts**.
    """
)


# --- SIDEBAR (TECHNICAL DETAILS & THESIS INFO) ---
st.sidebar.title("About fab-app")
st.sidebar.info(
    """
    **Drug-Disease Link Predictor**

    Developed as part of a **Master's Thesis project** on *Deterministic and Stochastic Network Inference*.
    
    - **Goal:** Link prediction for drug repurposing on a bipartite network.
    - **Model:** Nested Degree-Corrected Stochastic Block Model (**nDCSBM**).
    - **Inference:** **300 MCMC sweeps** performed using `graph-tool`.
    """
)


# --- MAIN PAGE FOOTER ---
st.markdown("---")
st.markdown(
    """
    <div style="
    background-color: #f5dfc6;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #EAE6DF;
    text-align: center;
    margin-top: 30px;
    ">
        <p style="color: #31333F; margin: 0; font-size: 1rem; font-weight: 500;">
            Developed by <b>Federica</b> | Master's Thesis Project
        </p>
        <p style="margin: 8px 0 0 0; font-size: 0.95rem;">
            🔗 <a href="https://github.com/federica13700" target="_blank" style="color: #0066cc; text-decoration: none;">GitHub Profile</a>
            &nbsp;•&nbsp;
            📁 <a href="https://github.com/federica13700/fab-app" target="_blank" style="color: #0066cc; text-decoration: none;">Project Repository</a>
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)