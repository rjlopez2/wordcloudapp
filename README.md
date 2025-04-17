# 📊 Streamlit Word Cloud App (Apptainer/Singularity)

This project is a lightweight Streamlit application that reads an Excel file, selects a column, and generates a word cloud.

## 🧱 Project Structure

├── app/ # Streamlit app and requirements ├── data/ # Input Excel files ├── singularity/ # Singularity/Apptainer definition file


## 🚀 Run with Apptainer

1. Build the container:
   ```bash
   apptainer build wordcloud.sif singularity/Singularity.def
