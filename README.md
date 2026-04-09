# AI-Assisted Image Text Reader and Voice Command System

## 📌 Project Overview

The **AI-Assisted Image Text Reader and Voice Command System** is an intelligent application that extracts text from images and documents using OCR (Optical Character Recognition), translates the extracted text, and converts it into speech output.

The system also supports voice commands, enabling hands-free operation. It is designed as an assistive tool for visually impaired users, students, and anyone who prefers listening over reading.

---

## 🚀 Features

* 🖼️ Image to Text Conversion using OCR (Tesseract / Vision OCR)
* 🌐 Multi-language Translation Support
* 🔊 Text-to-Speech Output (gTTS / pyttsx3)
* 🎙️ Voice Command Recognition (VOSK - offline)
* 📂 Support for Image and PDF File Upload
* 🤖 AI-based Text Summarization (Ollama + Mistral)
* 🖥️ User-friendly GUI using Tkinter

---

## 🛠️ Technologies Used

* Python
* OpenCV
* Tesseract OCR / Google Vision OCR
* Google Translate / deep-translator
* gTTS / pyttsx3
* VOSK (Speech Recognition)
* Tkinter (GUI)
* Ollama + Mistral (LLM)
* JSON (Configuration)

---

## 📁 Project Structure

```
├── app.py                # Main application (GUI)
├── ocr.py                # OCR processing
├── vision_ocr.py         # Google Vision OCR (optional)
├── translator.py         # Language translation
├── tts_engine.py         # Text-to-Speech
├── voice_commands.py     # Voice command handling
├── file_reader.py        # File input handling (PDF/Image)
├── preprocess.py         # Image preprocessing
├── ai_assistant.py       # AI assistant (summarization)
├── requirements.txt      # Dependencies
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```
git clone https://github.com/your-username/AI-Assisted-Image-Text-Reader-and-Voice-Command-System.git
cd AI-Assisted-Image-Text-Reader-and-Voice-Command-System
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Install Tesseract OCR

* Windows: Download and install from official site
* Mac:

```
brew install tesseract
```

---

## 📦 Additional Setup

### 🔊 VOSK Model (Required for Voice Commands)

Download VOSK speech model from:
https://alphacephei.com/vosk/models

Extract and place the folder inside the project directory as:

```
/vosk-model
```

---

## 🔑 Google Vision API Setup (Optional)

The file **"vision-voice.json"** has been removed from this repository for security reasons.

To use Google Vision OCR:

1. Go to Google Cloud Console
2. Create a new project
3. Enable **Vision API**
4. Generate and download the JSON key file
5. Place the file in the project folder
6. Update the file path in the code

👉 Note: Without this file, the system will still work using Tesseract OCR.

---

## ▶️ How to Run

```
python3 app.py
```

---

## 🎯 Use Cases

* Assistive technology for visually impaired users
* Reading printed text from images and documents
* Language translation with speech output
* Hands-free interaction using voice commands

---

## ⚠️ Limitations

* OCR accuracy depends on image quality
* Handwritten text recognition is limited
* Translation may require internet connectivity
* Voice recognition may be affected by background noise

---

## 🚀 Future Enhancements

* Mobile application development
* Real-time video text detection
* Handwritten text recognition
* Improved AI-based summarization
* Support for more languages

---

## 👩‍💻 Authors

This project was developed by a team of 4 members as part of an academic project.

**Lead Developer:**
Harshitha

---

## ⭐ Acknowledgement

This project was developed to demonstrate the integration of AI, computer vision, and speech technologies into a unified assistive system.

---
