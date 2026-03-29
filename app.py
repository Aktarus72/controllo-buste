import streamlit as st
import pandas as pd
import plotly.express as px

# Configurazione iniziale
st.set_page_config(page_title="Audit Buste Paga", layout="wide")
st.title("🛡️ Controllo Totale Buste Paga")

# Caricamento dati dal tuo file Excel
try:
    # Carichiamo il file (che caricheremo su GitHub tra poco)
    df = pd.read_excel("Tracker_Buste_Paga.xlsx")
    
    # Trasformiamo la tua data MM/AAAA in una data leggibile dal computer
    df['Data_Convertita'] = pd.to_datetime(df['Mese'], format='%m/%Y')
    df['Anno'] = df['Data_Convertita'].dt.year
    
    st.success("Dati caricati correttamente!")

except Exception as e:
    st.error("In attesa del file Excel... Carica 'Tracker_Buste_Paga.xlsx' per iniziare.")
    st.stop()

# --- FILTRO PER ANNO ---
anno_sel = st.sidebar.selectbox("Seleziona l'Anno da controllare", sorted(df['Anno'].unique(), reverse=True))
df_anno = df[df['Anno'] == anno_sel].sort_values('Data_Convertita')

# Mostriamo un'anteprima veloce
st.write(f"Analisi per l'anno: {anno_sel}")
st.dataframe(df_anno[['Mese', 'Netto in Busta', 'Ferie Godute (gg)', 'Permessi Goduti (ore)']])
