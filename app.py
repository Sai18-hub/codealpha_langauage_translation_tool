import os
import sys
import requests
from flask import Flask, render_template, request, jsonify

# Base directory for locating templates and static files
base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(base_dir, "templates"),
    static_folder=os.path.join(base_dir, "static")
)

# Supported languages list
LANGUAGES = {
    "English": {"code": "en", "flag": "🇬🇧"},
    "Telugu": {"code": "te", "flag": "🇮🇳"},
    "Hindi": {"code": "hi", "flag": "🇮🇳"},
    "Tamil": {"code": "ta", "flag": "🇮🇳"},
    "Kannada": {"code": "kn", "flag": "🇮🇳"},
    "Malayalam": {"code": "ml", "flag": "🇮🇳"},
    "Spanish": {"code": "es", "flag": "🇪🇸"},
    "French": {"code": "fr", "flag": "🇫🇷"},
    "German": {"code": "de", "flag": "🇩🇪"},
    "Italian": {"code": "it", "flag": "🇮🇹"},
    "Portuguese": {"code": "pt", "flag": "🇵🇹"},
    "Russian": {"code": "ru", "flag": "🇷🇺"},
    "Japanese": {"code": "ja", "flag": "🇯🇵"},
    "Chinese": {"code": "zh", "flag": "🇨🇳"},
    "Arabic": {"code": "ar", "flag": "🇸🇦"},
    "Bengali": {"code": "bn", "flag": "🇮🇳"},
    "Korean": {"code": "ko", "flag": "🇰🇷"},
    "Turkish": {"code": "tr", "flag": "🇹🇷"},
    "Dutch": {"code": "nl", "flag": "🇳🇱"},
    "Indonesian": {"code": "id", "flag": "🇮🇩"}
}


import re
import urllib.parse

# Language codes mapping for phonetic transliteration
TRANSLITERATION_CODES = {
    "hi": "hi-t-i0-und",
    "te": "te-t-i0-und",
    "ta": "ta-t-i0-und",
    "kn": "kn-t-i0-und",
    "ml": "ml-t-i0-und",
    "bn": "bn-t-i0-und",
    "ar": "ar-t-i0-und",
    "ru": "ru-t-i0-und"
}


def transliterate_text(text: str, target_lang: str) -> str:
    """Phonetically transliterates Romanized/slang words into native script (e.g. bhai -> भाई)."""
    itc = TRANSLITERATION_CODES.get(target_lang)
    if not itc:
        return ""
    try:
        url = "https://inputtools.google.com/request"
        res = requests.get(url, params={"text": text, "itc": itc, "num": 1}, timeout=5)
        if res.status_code == 200:
            data = res.json()
            if data and data[0] == "SUCCESS" and data[1]:
                candidates = data[1][0][1]
                if candidates:
                    return candidates[0].strip()
    except Exception:
        pass
    return ""


def normalize_slang(text: str) -> str:
    """Collapses repeated characters (e.g., 'bbhaiii' -> 'bhai', 'hellooo' -> 'hello')."""
    return re.sub(r'([a-zA-Z])\1{1,}', r'\1', text)


def translate_text(text: str, source_code: str, target_code: str) -> str:
    """Intelligent multi-tier translation with Neural MT, transliteration fallback, and MyMemory."""
    text_clean = text.strip()
    norm_text = normalize_slang(text_clean)

    # Strategy 1: MyMemory Translation API with match ranking
    main_trans = ""
    try:
        url = "https://api.mymemory.translated.net/get"
        params = {
            "q": text_clean,
            "langpair": f"{source_code}|{target_code}"
        }
        response = requests.get(url, params=params, timeout=7)
        if response.status_code == 200:
            data = response.json()
            main_trans = (data.get("responseData", {}) or {}).get("translatedText", "").strip()

            # Search matches for native script translations
            for match in data.get("matches", []):
                cand = (match.get("translation", "") or "").strip()
                if cand and cand.lower() != text_clean.lower():
                    # For non-Latin target languages, prefer candidates with native script characters
                    if target_code in TRANSLITERATION_CODES and any(ord(c) > 127 for c in cand):
                        return cand
    except Exception:
        pass

    # If MyMemory returned a distinct, valid translation
    if main_trans and main_trans.lower() != text_clean.lower():
        # Ensure it's not just a Romanized copy if the target language uses non-Latin script
        if target_code not in TRANSLITERATION_CODES or any(ord(c) > 127 for c in main_trans):
            return main_trans

    # Strategy 2: If translation is identical to input or low quality, check if it's Romanized slang (e.g. 'bbhaiii', 'bhai', 'namaste')
    if target_code in TRANSLITERATION_CODES:
        # Try transliteration on normalized slang
        translit = transliterate_text(norm_text, target_code)
        if translit and translit.lower() != norm_text.lower():
            return translit

        # Try transliteration on original text
        translit_orig = transliterate_text(text_clean, target_code)
        if translit_orig and translit_orig.lower() != text_clean.lower():
            return translit_orig

    # Strategy 3: Try MyMemory with normalized text if repeated characters were cleaned
    if norm_text != text_clean:
        try:
            url = "https://api.mymemory.translated.net/get"
            params = {
                "q": norm_text,
                "langpair": f"{source_code}|{target_code}"
            }
            res_norm = requests.get(url, params=params, timeout=6)
            if res_norm.status_code == 200:
                d_norm = res_norm.json()
                t_norm = (d_norm.get("responseData", {}) or {}).get("translatedText", "").strip()
                if t_norm and t_norm.lower() != norm_text.lower():
                    return t_norm
        except Exception:
            pass

    return main_trans or text_clean



# =======================================================
# FRONTEND ROUTES (Root & Vercel Rewrites)
# =======================================================

@app.route("/")
@app.route("/api")
@app.route("/api/index")
@app.route("/api/index.py")
def home():
    try:
        return render_template("index.html")
    except Exception:
        index_path = os.path.join(base_dir, "index.html")
        if os.path.exists(index_path):
            with open(index_path, "r", encoding="utf-8") as f:
                return f.read(), 200, {"Content-Type": "text/html; charset=utf-8"}
        return "AI Language Translation Tool is running", 200


# =======================================================
# API ROUTES
# =======================================================

@app.route("/api/languages", methods=["GET"])
def get_languages():
    return jsonify({
        "success": True,
        "languages": LANGUAGES
    })


@app.route("/translate", methods=["POST"])
@app.route("/api/translate", methods=["POST"])
@app.route("/api/index/translate", methods=["POST"])
def handle_translation():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    source_lang = data.get("source", "en")
    target_lang = data.get("target", "te")

    # Validation 1: Empty text
    if not text:
        return jsonify({
            "success": False,
            "error": "Please enter some text to translate."
        }), 400

    # Validation 2: Same language
    if source_lang == target_lang:
        return jsonify({
            "success": False,
            "error": "Source and target languages must be different."
        }), 400

    # Validation 3: Byte size limit
    if len(text.encode("utf-8")) > 500:
        return jsonify({
            "success": False,
            "error": "Text exceeds the 500-byte free tier limit. Please shorten your text."
        }), 400

    try:
        translated_text = translate_text(text, source_lang, target_lang)
        return jsonify({
            "success": True,
            "translated_text": translated_text,
            "source": source_lang,
            "target": target_lang
        })
    except requests.exceptions.RequestException as req_err:
        return jsonify({
            "success": False,
            "error": "Could not connect to translation service. Please check your internet connection."
        }), 502
    except Exception as err:
        return jsonify({
            "success": False,
            "error": str(err)
        }), 500


# Catch-all handler to avoid 404s on Vercel rewritten paths
@app.route("/<path:path>", methods=["GET", "POST"])
def catch_all(path):
    if request.method == "POST":
        return handle_translation()
    return home()


if __name__ == "__main__":
    app.run(debug=True, port=5000)