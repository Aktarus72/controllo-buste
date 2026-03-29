import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Audit Buste Paga", layout="wide")
st.title("🛡️ Controllo Totale Buste Paga")

# Funzione magica per caricare il file in ogni caso
def load_data():
    nome_file = "Tracker_Buste_Paga.xlsx"
    try:
        # Prova 1: Leggi come Excel
        return pd.read_excel(nome_file)
    except:
        try:
            # Prova 2: Leggi come CSV (spesso i file scaricati cambiano formato)
            return pd.read_csv(nome_file)
        except:
            return None

df = load_data()

if df is not None:
    # Pulizia nomi colonne (toglie spazi extra)
    df.columns = df.columns.str.strip()
    
    # Trasformazione Data
    df['Data_Convertita'] = pd.to_datetime(df['Mese'], format='%m/%Y', errors='coerce')
    df['Anno'] = df['Data_Convertita'].dt.year
    
    st.success("✅ Dati caricati! Ora puoi controllare i furbetti.")

    # --- FILTRO ANNO ---
    annali = sorted(df['Anno'].dropna().unique(), reverse=True)
    if annali:
        anno_sel = st.sidebar.selectbox("Seleziona l'Anno", annali)
        df_anno = df[df['Anno'] == anno_sel].sort_values('Data_Convertita')
        
        # MOSTRA TABELLA DI CONTROLLO
        st.write(f"### 📋 Riepilogo {anno_sel}")
        st.dataframe(df_anno[['Mese', 'Netto in Busta', 'Ferie Godute (gg)', 'Permessi Goduti (ore)']])
    else:
        st.warning("Controlla il formato della colonna Mese (deve essere MM/AAAA)")
else:
    st.error("❌ Errore: Non trovo il file 'Tracker_Buste_Paga.xlsx' su GitHub o il formato è errato.")
    st.info("Assicurati che il file caricato su GitHub si chiami esattamente: Tracker_Buste_Paga.xlsx")
