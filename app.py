import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Audit Buste Paga", layout="wide")
st.title("🛡️ Controllo Totale Buste Paga")

# Caricamento dati
@st.cache_data
def load_data():
    nome_file = "Tracker_Buste_Paga.xlsx"
    try:
        # Prova Excel
        df = pd.read_excel(nome_file)
    except:
        # Prova CSV
        df = pd.read_csv(nome_file)
    
    # PULIZIA COLONNE: toglie spazi e rende tutto minuscolo per sicurezza
    df.columns = df.columns.astype(str).str.strip()
    return df

df = load_data()

if df is not None:
    # Cerchiamo la colonna 'Mese' anche se ha nomi leggermente diversi
    colonna_mese = [c for c in df.columns if 'Mese' in c][0]
    
    # Conversione Data
    df['Data_Convertita'] = pd.to_datetime(df[colonna_mese], format='%m/%Y', errors='coerce')
    df['Anno'] = df['Data_Convertita'].dt.year
    
    st.success("✅ Dati caricati correttamente!")

    # --- FILTRO ANNO ---
    annali = sorted(df['Anno'].dropna().unique(), reverse=True)
    if annali:
        anno_sel = st.sidebar.selectbox("Seleziona l'Anno", annali)
        df_anno = df[df['Anno'] == anno_sel].sort_values('Data_Convertita')
        
        # MOSTRA TABELLA
        st.write(f"### 📋 Riepilogo {anno_sel}")
        # Selezioniamo solo le colonne che esistono davvero nel tuo file
        cols_da_mostrare = [c for c in ['Mese', 'Netto in Busta', 'Ferie Godute (gg)', 'Permessi Goduti (ore)'] if c in df.columns]
        st.dataframe(df_anno[cols_da_mostrare])
    else:
        st.warning("Formato data non riconosciuto. Assicurati che in 'Mese' ci sia scritto tipo 01/2024")
else:
    st.error("File non trovato o leggibile.")
