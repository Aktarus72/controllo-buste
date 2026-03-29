import streamlit as st
import pandas as pd

st.set_page_config(page_title="Diagnosi File", layout="wide")
st.title("🔍 Diagnosi del File Caricato")

nome_file = "Tracker_Buste_Paga.xlsx"

try:
    # Proviamo a leggere il file saltando eventuali righe vuote all'inizio
    df = pd.read_excel(nome_file)
    st.success(f"File '{nome_file}' trovato!")
    
    st.write("### Ecco cosa vede l'app nelle tue colonne:")
    st.write(list(df.columns))
    
    st.write("### Anteprima dei primi dati:")
    st.dataframe(df.head())

except Exception as e:
    try:
        df = pd.read_csv(nome_file)
        st.success(f"File '{nome_file}' trovato (letto come CSV)!")
        st.write("### Colonne trovate:")
        st.write(list(df.columns))
        st.dataframe(df.head())
    except Exception as e2:
        st.error(f"Impossibile leggere il file. Errore: {e2}")
