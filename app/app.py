import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from collections import defaultdict, Counter
import random

# Set Streamlit page config
st.set_page_config(page_title="Interactive Word Cloud", layout="wide")
st.title("Exploration of Firts Survey)")

# File uploader for Excel files
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

# If a file is uploaded
if uploaded_file:
    # Load Excel data into a DataFrame
    df = pd.read_excel(uploaded_file)

    # Check if the required "Name" column exists
    if "Name" not in df.columns:
        st.error("The dataset must contain a column named 'Name'.")
    else:
        # User selects the column containing text to analyze
        column = st.selectbox("Select the column to analyze", [col for col in df.columns if col != "Name"])

        # UI input to allow excluding words (semicolon-separated)
        st.markdown("### ❌ Exclude Words")
        exclusions = st.text_input("Enter words to exclude (separated by semicolons `;`)", value="")

        if st.button("Generate Word Cloud"):
            # Process exclusion list (case-insensitive)
            exclusion_list = [word.strip().lower() for word in exclusions.split(";") if word.strip()]

            # Count word frequency and collect names per word
            word_freq = Counter()
            word_to_names = defaultdict(set)

            for _, row in df[[column, "Name"]].dropna().iterrows():
                raw_text = str(row[column])
                name = str(row["Name"])

                # Split by lines, semicolons, commas
                for line in raw_text.splitlines():
                    for part in line.split(";"):
                        for word in part.split(","):
                            clean = word.strip()
                            if clean and clean.lower() not in exclusion_list:
                                word_freq[clean] += 1
                                word_to_names[clean].add(name)

            if not word_freq:
                st.warning("⚠️ Nothing to plot. All words may have been excluded.")
            else:
                # Get top 100 frequent words
                top_words = word_freq.most_common(100)

                x_vals, y_vals, texts, sizes, colors, tooltips = [], [], [], [], [], []

                # Frequency range for color normalization
                freqs = [freq for _, freq in top_words]
                max_freq = max(freqs)
                min_freq = min(freqs)
                range_freq = max_freq - min_freq if max_freq != min_freq else 1

                # Helper: map freq to RGB using a 'jet'-like scale
                def freq_to_rgb(freq):
                    normalized = (freq - min_freq) / range_freq
                    return jet_colormap(normalized)

                # Jet-style color map (simplified RGB steps)
                def jet_colormap(value):
                    """Maps a value [0,1] to a jet-style RGB color."""
                    if value < 0.25:
                        r, g, b = 0, 4 * value, 1
                    elif value < 0.5:
                        r, g, b = 0, 1, 1 - 4 * (value - 0.25)
                    elif value < 0.75:
                        r, g, b = 4 * (value - 0.5), 1, 0
                    else:
                        r, g, b = 1, 1 - 4 * (value - 0.75), 0
                    return f"rgb({int(r*255)}, {int(g*255)}, {int(b*255)})"

                for word, freq in top_words:
                    x_vals.append(random.uniform(-1, 1))
                    y_vals.append(random.uniform(-1, 1))
                    texts.append(word)
                    sizes.append(10 + freq * 3)
                    colors.append(freq_to_rgb(freq))
                    people = ", ".join(word_to_names[word])
                    tooltips.append(f"{word}<br>Freq: {freq}<br>Used by: {people}")

                # Create plotly figure
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=x_vals,
                    y=y_vals,
                    text=texts,
                    mode="text",
                    textfont={"size": sizes, "color": colors},
                    hoverinfo="text",
                    hovertext=tooltips,
                ))

                fig.update_layout(
                    title="Interactive Word Cloud (Temperature-Colored)",
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    margin=dict(l=0, r=0, t=30, b=0),
                    height=700
                )

                st.plotly_chart(fig, use_container_width=True)
