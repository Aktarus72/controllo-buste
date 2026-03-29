import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Audit Buste Paga", layout="wide")
st.title("🛡️ Controllo Audit Buste Paga")

# Mappa delle tue colonne reali
COL_MESE = "Periodo Paga"
COL_NETTO = "Netto busta paga"
COL_FERIE_GODUTE = "Ferie Godute"
COL_FERIE_RESIDUE = "Ferie residue AC"
COL_PERMESSI_GODUTI = "Prem. ROL goduti ORE"

@st.cache_data
def load_data():
    try:
        df = pd.read_excel("Tracker_Buste_Paga.xlsx")
        # Pulizia nomi colonne
        df.columns = df.columns.astype(str).str.strip()
        # Convertiamo il periodo (es. Gennaio 2024) in data se possibile
        return df
    except:
        return None

df = load_data()

if df is not None:
    st.success("✅ Dati collegati con successo!")

    # --- BLOCCO 1: SOLDI ---
    st.header("💰 Analisi Stipendio Netto")
    fig_netto = px.line(df, x=COL_MESE, y=COL_NETTO, markers=True, title="Andamento Netto in Busta")
    st.plotly_chart(fig_netto, use_container_width=True)

    # --- BLOCCO 2: FERIE E PERMESSI ---
    st.header("🏖️ Ferie e ROL (Permessi)")
    c1, c2 = st.columns(2)
    
    with c1:
        # Grafico Ferie Godute vs Residue
        fig_ferie = px.bar(df, x=COL_MESE, y=[COL_FERIE_GODUTE, COL_FERIE_RESIDUE], 
                           title="Ferie: Godute vs Residue", barmode="group")
        st.plotly_chart(fig_ferie, use_container_width=True)
        
    with c2:
        # Grafico ROL (Permessi)
        fig_rol = px.area(df, x=COL_MESE, y=COL_PERMESSI_GODUTI, title="Permessi (ROL) Goduti")
        st.plotly_chart(fig_rol, use_container_width=True)

    # --- BLOCCO 3: TABELLA DI AUDIT ---
    st.header("🔍 Tabella di Controllo")
    st.dataframe(df[[COL_MESE, COL_NETTO, COL_FERIE_GODUTE, COL_FERIE_RESIDUE, COL_PERMESSI_GODUTI]])

else:
    st.error("Non riesco a leggere il file. Controlla che si chiami Tracker_Buste_Paga.xlsx")
