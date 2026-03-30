import streamlit as st
import pandas as pd

st.set_page_config(page_title="Audit Ferie/ROL", layout="wide")
st.title("🕵️ Controllo Anomalie Ferie e Permessi")
st.subheader("Verifica se i conti dell'azienda tornano con i tuoi")

@st.cache_data
def load_data():
    try:
        df = pd.read_excel("Tracker_Buste_Paga.xlsx")
        df.columns = df.columns.astype(str).str.strip()
        return df
    except:
        return None

df = load_data()

if df is not None:
    # 1. Pulizia e Preparazione
    col_mese = "Periodo Paga"
    col_ferie_god = "Ferie Godute"
    col_ferie_res = "Ferie residue AC"
    col_rol_god = "Prem. ROL goduti ORE"
    col_rol_res = "Perm ROL residui AC"

    # 2. CALCOLO DISCREPANZE (Il cuore dell'Audit)
    # Calcoliamo quanto dovrebbe essere il residuo teorico
    df['Ferie_Teoriche'] = df[col_ferie_res].shift(1) - df[col_ferie_god]
    df['ROL_Teorico'] = df[col_rol_res].shift(1) - df[col_rol_god]
    
    st.info("💡 Consiglio: Se vedi ore godute in mesi dove non sei stato in ferie, qualcuno le sta scalando d'ufficio.")

    # 3. TABELLA FOCUS FERIE
    st.header("🏖️ Analisi Ferie (Giorni)")
    audit_ferie = df[[col_mese, col_ferie_god, col_ferie_res]].copy()
    st.dataframe(audit_ferie, use_container_width=True)

    # 4. TABELLA FOCUS PERMESSI (ROL)
    st.header("⏳ Analisi Permessi/ROL (Ore)")
    audit_rol = df[[col_mese, col_rol_god, col_rol_res]].copy()
    st.dataframe(audit_rol, use_container_width=True)

    # 5. ALERT AUTOMATICO
    st.header("🚨 Segnalazioni Sospette")
    # Cerchiamo mesi con godimento > 0
    sospetti = df[(df[col_ferie_god] > 0) | (df[col_rol_god] > 0)]
    if not sospetti.empty:
        st.warning("In questi mesi risultano scalati dei permessi o ferie. Controlla se corrispondono alla realtà:")
        st.table(sospetti[[col_mese, col_ferie_god, col_rol_god]])
    else:
        st.success("Nessun permesso scalato rilevato nei dati caricati.")

else:
    st.error("File non trovato.")
