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


def translate_text(text: str, source_code: str, target_code: str) -> str:
    """Translates text using MyMemory Translation API."""
    url = "https://api.mymemory.translated.net/get"
    params = {
        "q": text,
        "langpair": f"{source_code}|{target_code}"
    }

    response = requests.get(url, params=params, timeout=12)
    response.raise_for_status()
    data = response.json()

    if data.get("responseStatus") != 200:
        raise Exception(data.get("responseDetails", "Translation service error."))

    translated = (data.get("responseData", {}) or {}).get("translatedText", "").strip()

    if not translated:
        for match in data.get("matches", []):
            candidate = (match.get("translation", "") or "").strip()
            if candidate:
                translated = candidate
                break

    if not translated:
        raise Exception("No translation was returned by the translation service.")

    return translated


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