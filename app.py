import json
from pathlib import Path
import pandas as pd
import streamlit as st

# Configurazione della pagina
st.set_page_config(
    page_title="Drug-Disease Link Predictor",
    page_icon="🧬",
    layout="wide",
)

# Titolo dell'applicazione e descrizione iniziale
st.title("🧬 Drug-Disease Link Predictor")
st.caption("Predictions were generated based on Probabilistic Network Inference.")


# 1. Caricamento dati JSON con cache per prestazioni ottimali
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


# Caricamento in memoria
drugs_data, diseases_data = load_data()

# 2. Barra Laterale (Sidebar) - Totalmente sicura e nativa
st.sidebar.title("About fab-app")
st.sidebar.info(
    "**Drug-Disease Link Predictor** is an interactive tool for drug repurposing based on Probabilistic Network Inference. "
    "Predictions are inferred using 300 MCMC steps of a nested Degree-Corrected "
    "Stochastic Block Model (nDCSBM) on a bipartite network."
)

# 3. Selezione modalità di ricerca
search_mode = st.radio(
    "Select search mode:",
    options=["Search by Disease", "Search by Drug"],
    horizontal=True,
)

# 4. Ricerca e visualizzazione dati
if search_mode == "Search by Disease":
    if not diseases_data:
        st.error("File 'diseases.json' was not found or is empty in the current directory.")
    else:
        disease_list = ["-- Select a Disease --"] + sorted(list(diseases_data.keys()))
        selected_disease = st.selectbox(
            "Select a Disease from the dropdown menu:",
            options=disease_list,
        )

        if selected_disease and selected_disease != "-- Select a Disease --":
            predictions = diseases_data.get(selected_disease, [])
            st.subheader(f"Predicted Candidate Drugs for: **{selected_disease}**")

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
        st.error("File 'drugs.json' was not found or is empty in the current directory.")
    else:
        drug_list = ["-- Select a Drug --"] + sorted(list(drugs_data.keys()))
        selected_drug = st.selectbox(
            "Select a Drug from the dropdown menu:",
            options=drug_list,
        )

        if selected_drug and selected_drug != "-- Select a Drug --":
            predictions = drugs_data.get(selected_drug, [])
            st.subheader(f"Predicted Candidate Diseases for: **{selected_drug}**")

            if predictions:
                df = pd.DataFrame(predictions)
                if "score" in df.columns:
                    df = df.drop(columns=["score"])

                df.index = [f"#{i+1}" for i in range(len(df))]
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No predictions found for the selected drug.")

# 5. Footer a fine pagina (HTML semplice e isolato)
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