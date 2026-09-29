// ========================================================
// AI LANGUAGE TRANSLATION TOOL - JAVASCRIPT ENGINE
// Dual-layer translation (Serverless Flask + Client Fallback)
// Speech Synthesis, History Storage, Byte Counter, & Toast System
// ========================================================

const LANGUAGES = {
    "English": { code: "en", flag: "🇬🇧", voice: "en-US" },
    "Telugu": { code: "te", flag: "🇮🇳", voice: "te-IN" },
    "Hindi": { code: "hi", flag: "🇮🇳", voice: "hi-IN" },
    "Tamil": { code: "ta", flag: "🇮🇳", voice: "ta-IN" },
    "Kannada": { code: "kn", flag: "🇮🇳", voice: "kn-IN" },
    "Malayalam": { code: "ml", flag: "🇮🇳", voice: "ml-IN" },
    "Spanish": { code: "es", flag: "🇪🇸", voice: "es-ES" },
    "French": { code: "fr", flag: "🇫🇷", voice: "fr-FR" },
    "German": { code: "de", flag: "🇩🇪", voice: "de-DE" },
    "Italian": { code: "it", flag: "🇮🇹", voice: "it-IT" },
    "Portuguese": { code: "pt", flag: "🇵🇹", voice: "pt-PT" },
    "Russian": { code: "ru", flag: "🇷🇺", voice: "ru-RU" },
    "Japanese": { code: "ja", flag: "🇯🇵", voice: "ja-JP" },
    "Chinese": { code: "zh", flag: "🇨🇳", voice: "zh-CN" },
    "Arabic": { code: "ar", flag: "🇸🇦", voice: "ar-SA" },
    "Bengali": { code: "bn", flag: "🇮🇳", voice: "bn-IN" },
    "Korean": { code: "ko", flag: "🇰🇷", voice: "ko-KR" },
    "Turkish": { code: "tr", flag: "🇹🇷", voice: "tr-TR" },
    "Dutch": { code: "nl", flag: "🇳🇱", voice: "nl-NL" },
    "Indonesian": { code: "id", flag: "🇮🇩", voice: "id-ID" }
};

const POPULAR_LANGUAGES = ["English", "Telugu", "Hindi", "Spanish", "French", "Japanese"];
const STORAGE_KEY = "ai_translator_history_v1";

// DOM Elements
const sourceSelect = document.getElementById("sourceLanguageSelect");
const targetSelect = document.getElementById("targetLanguageSelect");
const swapBtn = document.getElementById("swapLanguagesBtn");
const popularChipsContainer = document.getElementById("popularChips");
const inputText = document.getElementById("inputText");
const outputText = document.getElementById("outputText");
const translateBtn = document.getElementById("translateBtn");
const btnText = document.getElementById("btnText");
const btnSpinner = document.getElementById("btnSpinner");
const btnIcon = document.getElementById("btnIcon");
const clearBtn = document.getElementById("clearBtn");
const pasteBtn = document.getElementById("pasteBtn");
const copyBtn = document.getElementById("copyBtn");
const copyBtnText = document.getElementById("copyBtnText");
const listenBtn = document.getElementById("listenBtn");
const byteCounter = document.getElementById("byteCounter");
const byteBar = document.getElementById("byteBar");
const loadingShimmer = document.getElementById("loadingShimmer");
const statusBadge = document.getElementById("statusBadge");
const statusMessage = document.getElementById("statusMessage");
const sourceLangTag = document.getElementById("sourceLangTag");
const targetLangTag = document.getElementById("targetLangTag");
const toastContainer = document.getElementById("toastContainer");
const historyList = document.getElementById("historyList");
const historyCount = document.getElementById("historyCount");
const clearHistoryBtn = document.getElementById("clearHistoryBtn");

// State
let isTranslating = false;

// ========================================================
// INITIALIZATION
// ========================================================

document.addEventListener("DOMContentLoaded", () => {
    populateLanguageSelects();
    renderPopularChips();
    setupEventListeners();
    updateByteCount();
    loadHistory();
});

function populateLanguageSelects() {
    sourceSelect.innerHTML = "";
    targetSelect.innerHTML = "";

    Object.entries(LANGUAGES).forEach(([name, meta]) => {
        const opt1 = new Option(`${meta.flag} ${name}`, meta.code);
        const opt2 = new Option(`${meta.flag} ${name}`, meta.code);
        
        sourceSelect.add(opt1);
        targetSelect.add(opt2);
    });

    sourceSelect.value = "en"; // English
    targetSelect.value = "te"; // Telugu

    updateTags();
}

function renderPopularChips() {
    popularChipsContainer.innerHTML = "";
    POPULAR_LANGUAGES.forEach((name) => {
        const meta = LANGUAGES[name];
        if (!meta) return;

        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "chip-btn";
        btn.textContent = `${meta.flag} ${name}`;
        btn.addEventListener("click", () => {
            targetSelect.value = meta.code;
            updateTags();
            showToast(`Target set to ${name}`, "success");
        });
        popularChipsContainer.appendChild(btn);
    });
}

function updateTags() {
    const sourceName = getLanguageNameByCode(sourceSelect.value);
    const targetName = getLanguageNameByCode(targetSelect.value);

    sourceLangTag.textContent = `${LANGUAGES[sourceName]?.flag || "🌐"} ${sourceName}`;
    targetLangTag.textContent = `${LANGUAGES[targetName]?.flag || "✨"} ${targetName}`;
}

function getLanguageNameByCode(code) {
    const entry = Object.entries(LANGUAGES).find(([_, meta]) => meta.code === code);
    return entry ? entry[0] : code;
}

// ========================================================
// BYTE COUNTER & VALIDATION
// ========================================================

function getByteLength(str) {
    return new TextEncoder().encode(str).length;
}

function updateByteCount() {
    const text = inputText.value;
    const bytes = getByteLength(text);
    const maxBytes = 500;
    const percentage = Math.min((bytes / maxBytes) * 100, 100);

    byteCounter.textContent = `${bytes} / ${maxBytes} bytes`;
    byteBar.style.width = `${percentage}%`;

    byteBar.classList.remove("warn", "danger");
    if (bytes > maxBytes) {
        byteBar.classList.add("danger");
        byteCounter.style.color = "var(--accent-rose)";
    } else if (bytes > 400) {
        byteBar.classList.add("warn");
        byteCounter.style.color = "var(--accent-amber)";
    } else {
        byteCounter.style.color = "var(--text-muted)";
    }
}

// ========================================================
// EVENT LISTENERS
// ========================================================

function setupEventListeners() {
    inputText.addEventListener("input", updateByteCount);
    sourceSelect.addEventListener("change", updateTags);
    targetSelect.addEventListener("change", updateTags);

    // Swap Languages Button
    swapBtn.addEventListener("click", () => {
        const temp = sourceSelect.value;
        sourceSelect.value = targetSelect.value;
        targetSelect.value = temp;
        updateTags();

        // If translation already exists, swap text too!
        if (outputText.value.trim() && inputText.value.trim()) {
            const currentInput = inputText.value;
            inputText.value = outputText.value;
            outputText.value = currentInput;
            updateByteCount();
        }

        showToast("Languages swapped!", "success");
    });

    // Clear Button
    clearBtn.addEventListener("click", () => {
        inputText.value = "";
        outputText.value = "";
        updateByteCount();
        statusBadge.classList.add("hidden");
        inputText.focus();
        showToast("Text cleared", "success");
    });

    // Paste Button
    pasteBtn.addEventListener("click", async () => {
        try {
            const text = await navigator.clipboard.readText();
            if (text) {
                inputText.value = text;
                updateByteCount();
                showToast("Pasted from clipboard", "success");
            } else {
                showToast("Clipboard is empty", "error");
            }
        } catch (e) {
            showToast("Clipboard permission required to paste", "error");
        }
    });

    // Sample Text Chips
    document.querySelectorAll(".sample-chip").forEach((btn) => {
        btn.addEventListener("click", () => {
            inputText.value = btn.dataset.sample;
            updateByteCount();
            inputText.focus();
        });
    });

    // Copy Button
    copyBtn.addEventListener("click", async () => {
        const text = outputText.value.trim();
        if (!text) {
            showToast("Nothing to copy yet", "error");
            return;
        }

        try {
            await navigator.clipboard.writeText(text);
            copyBtnText.textContent = "Copied!";
            copyBtn.classList.add("highlight-btn");
            showToast("Translation copied to clipboard!", "success");
            setTimeout(() => {
                copyBtnText.textContent = "Copy";
            }, 2000);
        } catch (e) {
            showToast("Failed to copy to clipboard", "error");
        }
    });

    // Listen Button (Speech Synthesis)
    listenBtn.addEventListener("click", () => {
        const text = outputText.value.trim();
        if (!text) {
            showToast("Translate text first to listen", "error");
            return;
        }

        speakText(text, targetSelect.value);
    });

    // Main Translate Button
    translateBtn.addEventListener("click", performTranslation);

    // Keyboard Shortcut (Ctrl+Enter or Cmd+Enter)
    document.addEventListener("keydown", (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
            e.preventDefault();
            performTranslation();
        }
    });

    // Clear History Button
    clearHistoryBtn.addEventListener("click", () => {
        localStorage.removeItem(STORAGE_KEY);
        loadHistory();
        showToast("History cleared", "success");
    });
}

// ========================================================
// TRANSLATION LOGIC (Dual-Layer: Flask + Client Fallback)
// ========================================================

async function performTranslation() {
    if (isTranslating) return;

    const text = inputText.value.trim();
    const source = sourceSelect.value;
    const target = targetSelect.value;
    const bytes = getByteLength(text);

    // Validation 1: Empty text
    if (!text) {
        showToast("⚠️ Please enter some text to translate.", "error");
        inputText.focus();
        return;
    }

    // Validation 2: Same languages
    if (source === target) {
        showToast("⚠️ Please select different source and target languages.", "error");
        return;
    }

    // Validation 3: Byte limit
    if (bytes > 500) {
        showToast(`⚠️ Text exceeds 500-byte limit (${bytes} bytes). Please shorten.`, "error");
        return;
    }

    // Set Loading State
    setLoading(true);

    try {
        let translatedText = "";

        // First attempt: Serverless Flask Endpoint (/api/translate or /translate)
        try {
            const response = await fetch("/api/translate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text, source, target })
            });

            if (response.ok) {
                const data = await response.json();
                if (data.success && data.translated_text) {
                    translatedText = data.translated_text;
                }
            }
        } catch (serverErr) {
            console.warn("Server endpoint unreachable, attempting client-side fallback:", serverErr);
        }

        // Second attempt fallback: Direct MyMemory API call
        if (!translatedText) {
            const fallbackUrl = `https://api.mymemory.translated.net/get?q=${encodeURIComponent(text)}&langpair=${source}|${target}`;
            const fallbackRes = await fetch(fallbackUrl);
            if (!fallbackRes.ok) {
                throw new Error("Translation service returned an error status.");
            }
            const data = await fallbackRes.json();
            if (data.responseStatus !== 200 && data.responseStatus !== "200") {
                throw new Error(data.responseDetails || "Translation failed.");
            }
            translatedText = data.responseData?.translatedText?.trim();

            if (!translatedText && data.matches?.length) {
                for (const match of data.matches) {
                    if (match.translation?.trim()) {
                        translatedText = match.translation.trim();
                        break;
                    }
                }
            }
        }

        if (!translatedText) {
            throw new Error("No translation returned by the translation service.");
        }

        // Render result
        outputText.value = translatedText;

        const sourceName = getLanguageNameByCode(source);
        const targetName = getLanguageNameByCode(target);

        statusMessage.textContent = `Translated from ${sourceName} to ${targetName}`;
        statusBadge.classList.remove("hidden");

        // Save to History
        saveHistoryItem({
            sourceName,
            targetName,
            sourceCode: source,
            targetCode: target,
            originalText: text,
            translatedText,
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        });

        showToast("✅ Translation complete!", "success");

    } catch (err) {
        console.error("Translation Error:", err);
        showToast(`❌ Translation failed: ${err.message}`, "error");
    } finally {
        setLoading(false);
    }
}

function setLoading(loading) {
    isTranslating = loading;
    if (loading) {
        btnSpinner.classList.remove("hidden");
        btnIcon.classList.add("hidden");
        btnText.textContent = "Translating...";
        translateBtn.disabled = true;
        loadingShimmer.classList.remove("hidden");
        outputText.value = "";
    } else {
        btnSpinner.classList.add("hidden");
        btnIcon.classList.remove("hidden");
        btnText.textContent = "Translate Now";
        translateBtn.disabled = false;
        loadingShimmer.classList.add("hidden");
    }
}

// ========================================================
// TEXT-TO-SPEECH (Web Speech API)
// ========================================================

function speakText(text, langCode) {
    if (!('speechSynthesis' in window)) {
        showToast("Speech synthesis is not supported in this browser.", "error");
        return;
    }

    window.speechSynthesis.cancel(); // Cancel any ongoing speech

    const utterance = new SpeechSynthesisUtterance(text);
    const langName = getLanguageNameByCode(langCode);
    const voiceMeta = LANGUAGES[langName];

    if (voiceMeta && voiceMeta.voice) {
        utterance.lang = voiceMeta.voice;
    }

    utterance.rate = 0.95;
    utterance.pitch = 1.0;

    utterance.onstart = () => showToast(`Playing ${langName} audio...`, "success");
    utterance.onerror = () => showToast("Audio playback issue", "error");

    window.speechSynthesis.speak(utterance);
}

// ========================================================
// RECENT TRANSLATIONS HISTORY
// ========================================================

function getHistory() {
    try {
        return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
    } catch {
        return [];
    }
}

function saveHistoryItem(item) {
    let history = getHistory();
    // Prepend and filter duplicates
    history = [item, ...history.filter(h => h.originalText !== item.originalText)].slice(0, 10);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(history));
    loadHistory();
}

function loadHistory() {
    const history = getHistory();
    historyCount.textContent = `${history.length} items`;

    if (history.length === 0) {
        historyList.innerHTML = `<div class="history-empty">No recent translations yet. Enter text and translate to build your history!</div>`;
        return;
    }

    historyList.innerHTML = "";
    history.forEach((item) => {
        const card = document.createElement("div");
        card.className = "history-item";
        card.innerHTML = `
            <div class="history-item-header">
                <span>${item.sourceName} ➔ ${item.targetName}</span>
                <span style="color: var(--text-muted); font-size: 10px;">${item.timestamp || ""}</span>
            </div>
            <div class="history-item-source" title="${item.originalText}">${escapeHtml(item.originalText)}</div>
            <div class="history-item-target" title="${item.translatedText}">${escapeHtml(item.translatedText)}</div>
        `;

        card.addEventListener("click", () => {
            inputText.value = item.originalText;
            outputText.value = item.translatedText;
            sourceSelect.value = item.sourceCode;
            targetSelect.value = item.targetCode;
            updateTags();
            updateByteCount();
            statusMessage.textContent = `Restored from history (${item.sourceName} ➔ ${item.targetName})`;
            statusBadge.classList.remove("hidden");
            showToast("Restored from history", "success");
        });

        historyList.appendChild(card);
    });
}

function escapeHtml(str) {
    return str
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// ========================================================
// TOAST NOTIFICATIONS
// ========================================================

function showToast(message, type = "success") {
    const toast = document.createElement("div");
    toast.className = `toast toast-${type}`;
    toast.textContent = message;

    toastContainer.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = "0";
        toast.style.transform = "translateY(15px) scale(0.95)";
        setTimeout(() => toast.remove(), 300);
    }, 2800);
}
