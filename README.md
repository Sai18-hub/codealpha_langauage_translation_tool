# 🌍 AI Language Translation Tool

An intelligent, web-based language translation application developed as part of the **CodeAlpha Artificial Intelligence Internship**. The application provides real-time neural translation between multiple languages using the **MyMemory Translation API**, optimized with a serverless Python Flask backend and an Edge CDN frontend configured for deployment on **Vercel**.

---

## 📌 Project Overview

The **AI Language Translation Tool** provides a responsive interface for translating text across 20+ languages.

Users can:
* Select or swap source and target languages (with flag indicators and quick popular chips)
* Enter or paste text with a live 500-byte boundary tracking meter
* Translate text instantly using the MyMemory Translation API
* Listen to native pronunciations with integrated **Text-to-Speech (Web Speech API)**
* Copy translated text to clipboard with a single click
* Browse and reload recent translation history stored locally
* Run seamlessly on **Vercel** with near-instant cold-start times or run locally via Flask or Streamlit

---

## ✨ Key Features

* **🌐 20+ Languages Supported**: English, Telugu, Hindi, Tamil, Kannada, Malayalam, Spanish, French, German, Italian, Portuguese, Russian, Japanese, Chinese, Arabic, Bengali, Korean, Turkish, Dutch, and Indonesian.
* **⚡ Serverless Vercel Architecture**: Built using Python Flask serverless functions (`api/index.py`) and Edge CDN static files for fast global delivery.
* **🔊 Text-to-Speech Pronunciation**: Listen to translated results in the target language.
* **🔁 One-Click Language Swapping**: Instantly reverse source and target languages with fluid micro-animations.
* **📋 Clipboard Integration**: One-click paste from clipboard and copy translation.
* **⏱️ Recent History Drawer**: Automatically stores recent translations in browser local storage.
* **🛡️ Smart Input Validation**: Guards against empty input, identical source/target languages, and exceeds 500 bytes.
* **🔄 Dual Compatibility**: Deployable to Vercel via Flask (`app.py`), with Streamlit app preserved in `streamlit_app.py`.

---

## 🛠️ Technologies Used

* **Backend**: Python 3.14, Flask, Requests
* **Frontend**: HTML5, Vanilla CSS (Glassmorphism & modern design tokens), JavaScript (ES6+, Web Speech API)
* **API**: MyMemory Translation REST API
* **Cloud Platform**: Vercel (Edge CDN & Serverless Python Functions)
* **Legacy UI**: Streamlit (`streamlit_app.py`)

---

## 🏗️ Project Structure

```text
codealpha_langauage_translation_tool/
│
├── api/
│   └── index.py            # Vercel serverless Python entrypoint
├── public/                 # Static CDN files for Vercel
│   ├── index.html
│   └── static/
│       ├── style.css
│       └── script.js
├── templates/
│   └── index.html          # Jinja2 HTML template
├── static/
│   ├── style.css           # Glassmorphism styling and design system
│   └── script.js           # Client-side engine, TTS & history
├── app.py                  # Flask web application & REST API
├── streamlit_app.py        # Streamlit version of the translator
├── index.html              # Root entrypoint for Vercel CDN
├── requirements.txt        # Lightweight dependencies for Vercel
├── requirements-streamlit.txt # Streamlit dependencies
├── vercel.json             # Vercel function & rewrite configuration
├── .vercelignore           # Excluded files from Vercel deployment
├── .gitignore
└── README.md
```

---

## 🚀 Deployment to Vercel

1. Log in to your [Vercel Dashboard](https://vercel.com/sai18-hub).
2. Click **Add New...** > **Project** (or import `https://github.com/Sai18-hub/codealpha_langauage_translation_tool`).
3. Select **`codealpha_langauage_translation_tool`** from your repository list.
4. Keep the default settings:
   * **Framework Preset**: `Other`
   * **Root Directory**: `./`
5. Click **Deploy**. Vercel will install dependencies from `requirements.txt` and serve the application globally.

---

## 💻 Running Locally

### Option 1: Flask Web App (Same as Vercel)
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run Flask server
python app.py
```
Open your browser at `http://127.0.0.1:5000`.

### Option 2: Streamlit App
```bash
# 1. Install Streamlit dependencies
pip install -r requirements-streamlit.txt

# 2. Run Streamlit
streamlit run streamlit_app.py
```
Open your browser at `http://localhost:8501`.

---

## 👨‍💻 Author

Developed by **B Sai Charan** as part of the **CodeAlpha Artificial Intelligence Internship**.
* GitHub: [@Sai18-hub](https://github.com/Sai18-hub)
