# Streamlit app to analyze words

This is a **Streamlit-based application** that generates an interactive **word cloud** from a column in an uploaded Excel file. It uses **Plotly** for interactivity and color-codes words by frequency (like a heatmap from blue to red). Tooltips on hover display each word’s frequency and who mentioned it.

> The app is designed to run inside a **Singularity/Apptainer container**, bootstrapped from a Docker image.

---

## Features

- 📂 Upload an `.xlsx` Excel file
- 🔍 Choose a column to analyze
- 🙋 The column `"Name"` is automatically used to track who used each word
- 🧹 Exclude unwanted terms (case-insensitive)
- 🌡️ Color-coded words by frequency (Jet colormap: blue → red)
- 🖱️ Tooltips showing frequency + contributors on hover
- 📱 Fully interactive visualization powered by **Plotly**

---

## Project Structure

```
wordcloud-app/
├── README.md
├── app
│   ├── app.py
│   ├── entrypoint.sh
│   └── requirements.txt
├── data
│   └── VIBE User Questionnaire(1-9).xlsx
├── singularity
│   └── app.def
└── wordcloud.sif

```


## Installation (Singularity / Apptainer)

First, ensure you have **Apptainer** or **Singularity** installed on your system.

### 1. Clone repo
Download this repo.
```bash
git clone git@github.com:rjlopez2/wordcloudapp.git
```

### 2. Build the container image
The container image is not included in this repository. To build the Streamlit container image use the following commands:
```bash
cd singularity
apptainer build --fakeroot wordcloud.sif app.def 
````

## How to Run the App

### 1. Run the container interactively
```bash
apptainer run --bind ./app:/app wordcloud.sif
```

This mounts the app/ and data/ folders into the container.

## How to Use the App

1. Upload your Excel file (.xlsx)

2. Select the column you want to analyze (e.g., "Software")

3. The app automatically uses the `'Name'` column to associate entries with contributors

4. Optionally exclude words (separate by ;, case-insensitive)

5. Click “Generate Word Cloud”

6. Interact with the colorful Plotly word cloud.

7. Hover over a word to see:
   - Frequency of use.
   - Who used the word.


## Notes

- Your Excel file must include a column named Name to track user mentions.

- Only the top 100 words (by frequency) are shown for clarity.

- Words are color-coded using a Jet-style colormap (low = blue, high = red).

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create a new Pull Request

## License

Code is licensed under MIT (see LICENSE.txt)
