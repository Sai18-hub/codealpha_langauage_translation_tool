# 🌍 AI Language Translation Tool

A simple web-based language translation application built using
Python and Streamlit. The application allows users to translate
text between multiple languages using the MyMemory Translation API.

---

## 📌 Project Overview

The AI Language Translation Tool provides an easy-to-use interface
for translating text from one language to another.

Users can:

- Select a source language
- Select a target language
- Enter text to translate
- Translate the text using an online translation API
- Swap source and target languages
- Copy the translated text
- Clear the input and translation

This project was developed as part of the **CodeAlpha AI Internship**.

---

## ✨ Features

### 🌐 Multiple Language Support

The application currently supports:

- English
- Telugu
- Hindi
- Tamil
- Kannada
- Malayalam
- French
- German
- Spanish
- Italian
- Portuguese
- Russian
- Japanese
- Chinese
- Arabic

### 🔄 Translation

Text is translated using the **MyMemory Translation API**.

### 🔁 Swap Languages

The Swap Languages button allows users to quickly switch the
source and target languages.

### 📋 Copy Translation

Users can copy the translated text using the Copy Translation
button.

### 🗑️ Clear

The Clear button removes the entered text and previous translation.

### ⚠️ Input Validation

The application checks:

- Empty text
- Same source and target languages
- Text exceeding the supported 500-byte limit

### ❌ Error Handling

The application handles:

- Internet connection errors
- Translation API errors
- Missing translation responses

---

## 🛠️ Technologies Used

- Python
- Streamlit
- Requests
- REST API
- MyMemory Translation API
- HTML
- JavaScript

---

## 🏗️ Project Structure

```text
language transalation tool/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── .venv/