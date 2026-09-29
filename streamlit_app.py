import streamlit as st
import requests
import streamlit.components.v1 as components


# =========================================
# PAGE CONFIGURATION
# =========================================

st.set_page_config(
    page_title="AI Language Translator",
    page_icon="🌍",
    layout="centered"
)


# =========================================
# CUSTOM CSS
# =========================================

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        margin-bottom: 25px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================
# LANGUAGE LIST
# =========================================

languages = {
    "English": "en",
    "Telugu": "te",
    "Hindi": "hi",
    "Tamil": "ta",
    "Kannada": "kn",
    "Malayalam": "ml",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Japanese": "ja",
    "Chinese": "zh",
    "Arabic": "ar"
}


# =========================================
# INITIALIZE SESSION STATE
# =========================================

if "source_language" not in st.session_state:
    st.session_state.source_language = "English"

if "target_language" not in st.session_state:
    st.session_state.target_language = "Telugu"

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""


# =========================================
# SWAP LANGUAGES FUNCTION
# =========================================

def swap_languages():

    current_source = st.session_state.source_language
    current_target = st.session_state.target_language

    st.session_state.source_language = current_target
    st.session_state.target_language = current_source


# =========================================
# CLEAR TEXT FUNCTION
# =========================================

def clear_text():

    st.session_state.input_text = ""
    st.session_state.translated_text = ""


# =========================================
# TRANSLATION FUNCTION
# =========================================

def translate_text(text, source_language, target_language):

    url = "https://api.mymemory.translated.net/get"

    params = {
        "q": text,
        "langpair": f"{source_language}|{target_language}"
    }

    response = requests.get(
        url,
        params=params,
        timeout=15
    )

    response.raise_for_status()

    data = response.json()

    # Check API response status
    if data.get("responseStatus") != 200:
        raise Exception(
            data.get(
                "responseDetails",
                "Translation failed."
            )
        )

    # Get main translation
    translated_text = (
        data.get("responseData", {})
        .get("translatedText", "")
        .strip()
    )

    # If main translation is empty,
    # check other available matches
    if not translated_text:

        for match in data.get("matches", []):

            translation = (
                match.get("translation", "")
                .strip()
            )

            if translation:

                translated_text = translation
                break

    # If no translation was found
    if not translated_text:

        raise Exception(
            "No translation was returned by the translation service."
        )

    return translated_text


# =========================================
# TITLE
# =========================================

st.markdown(
    '<div class="main-title">🌍 AI Language Translation Tool</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Translate text quickly between multiple languages'
    '</div>',
    unsafe_allow_html=True
)


# =========================================
# LANGUAGE SELECTION
# =========================================

st.subheader("🌐 Language Selection")

col1, col2 = st.columns(2)

with col1:

    source_language = st.selectbox(
        "Source Language",
        list(languages.keys()),
        key="source_language"
    )

with col2:

    target_language = st.selectbox(
        "Target Language",
        list(languages.keys()),
        key="target_language"
    )


# =========================================
# SWAP BUTTON
# =========================================

st.button(
    "🔁 Swap Languages",
    use_container_width=True,
    on_click=swap_languages
)


# =========================================
# TEXT INPUT
# =========================================

st.subheader("📝 Enter Text")

text = st.text_area(
    "Text to translate",
    height=160,
    placeholder="Type your text here...",
    key="input_text"
)


# =========================================
# TRANSLATE AND CLEAR BUTTONS
# =========================================

col3, col4 = st.columns(2)

with col3:

    translate_button = st.button(
        "🔄 Translate",
        use_container_width=True
    )

with col4:

    st.button(
        "🗑️ Clear",
        use_container_width=True,
        on_click=clear_text
    )


# =========================================
# TRANSLATION PROCESS
# =========================================

if translate_button:

    # Check for empty text
    if not text.strip():

        st.warning(
            "⚠️ Please enter some text to translate."
        )

    # Check same languages
    elif source_language == target_language:

        st.warning(
            "⚠️ Please select different source "
            "and target languages."
        )

    # Check 500-byte limit
    elif len(text.encode("utf-8")) > 500:

        st.warning(
            "⚠️ Please keep the text within 500 bytes."
        )

    else:

        source_code = languages[source_language]
        target_code = languages[target_language]

        try:

            with st.spinner("Translating..."):

                result = translate_text(
                    text,
                    source_code,
                    target_code
                )

            # Save translation
            st.session_state.translated_text = result

        except requests.exceptions.RequestException:

            st.error(
                "❌ Could not connect to the translation service. "
                "Please check your internet connection and try again."
            )

        except Exception as error:

            st.error(
                f"❌ Translation failed: {error}"
            )


# =========================================
# DISPLAY TRANSLATION
# =========================================

if st.session_state.translated_text:

    st.subheader("✨ Translation")

    st.text_area(
        "Translated Text",
        value=st.session_state.translated_text,
        height=160,
        disabled=True
    )

    # =====================================
    # COPY TRANSLATION BUTTON
    # =====================================

    safe_text = (
        st.session_state.translated_text
        .replace("\\", "\\\\")
        .replace("`", "\\`")
        .replace("${", "\\${")
    )

    copy_html = f"""
    <button
        onclick="copyTranslation()"
        style="
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 8px;
            border: 1px solid #cccccc;
            background-color: white;
            cursor: pointer;
        "
    >
        📋 Copy Translation
    </button>

    <script>

    function copyTranslation() {{

        const text = `{safe_text}`;

        navigator.clipboard.writeText(text);

        alert("Translation copied!");

    }}

    </script>
    """

    components.html(
        copy_html,
        height=60
    )

    st.success(
        f"✅ Translated from {source_language} "
        f"to {target_language}."
    )


# =========================================
# ABOUT PROJECT
# =========================================

st.markdown("---")

st.subheader("ℹ️ About This Project")

st.write(
    "AI Language Translation Tool is a web-based application "
    "that translates text between multiple languages using "
    "a translation API."
)

st.write("**Technologies Used:**")

st.markdown(
    """
    - Python
    - Streamlit
    - REST API
    - MyMemory Translation API
    """
)

st.write("**Features:**")

st.markdown(
    """
    - Multiple language support
    - Real-time translation
    - Language swapping
    - Copy translated text
    - Clear input
    - Input validation
    - Error handling
    """
)
