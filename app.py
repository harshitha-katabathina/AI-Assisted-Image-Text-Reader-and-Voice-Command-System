from ai_assistant import open_ai_assistant
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading, os
import cv2
from PIL import Image, ImageTk
import pytesseract
import numpy as np

from preprocess import clean_image
from file_reader import read_image_file, read_pdf_first_page, read_text_file
from translator import MyTranslator
from tts_engine import TTSEngine
from voice_commands import VoiceControl

# ---------------- INIT ----------------
translator = MyTranslator()
tts = TTSEngine()
vc = VoiceControl()

#  Languages (SAFE & STABLE)
lang_map = {
    "English":"en",
    "Telugu":"te",
    "Hindi":"hi",
    "Tamil":"ta",
    "Kannada":"kn",
    "Malayalam":"ml",
    "Bengali":"bn",
    "Marathi":"mr",
    "Gujarati":"gu",
    "Punjabi":"pa",
    "Urdu":"ur",
    "Spanish":"es",
    "French":"fr",
    "German":"de",
    "Italian":"it",
    "Portuguese":"pt",
    "Chinese":"zh-cn",
    "Japanese":"ja",
    "Korean":"ko",
    "Arabic":"ar"
}

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Vision2Voice")
root.geometry("1000x650")

left = ttk.Frame(root, width=260)
left.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

right = ttk.Frame(root)
right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

preview = tk.Label(right)
preview.pack()

text_output = scrolledtext.ScrolledText(right, height=10, wrap=tk.WORD)
text_output.pack(fill=tk.X, pady=10)

languages = list(lang_map.keys())
lang_var = tk.StringVar(value="English")

ttk.Label(left, text="Select Language").pack()
ttk.Combobox(
    left,
    values=languages,
    textvariable=lang_var,
    state="readonly"
).pack(fill=tk.X)

# ---------------- CAMERA ----------------
current_frame = None
cap = cv2.VideoCapture(0)

def update_camera():

    global current_frame

    ret, frame = cap.read()

    if ret:
        current_frame = frame.copy()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        img = Image.fromarray(frame)
        img = img.resize((640,360))

        imgtk = ImageTk.PhotoImage(image=img)

        preview.imgtk = imgtk
        preview.configure(image=imgtk)

    root.after(10, update_camera)

# ---------------- OCR ----------------

def do_ocr(pil_img):
    gray = cv2.cvtColor(np.array(pil_img), cv2.COLOR_BGR2GRAY)
    
    gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

    text = pytesseract.image_to_string(
    gray,
    lang="eng+tel+hin+mal+urd+deu+chi_sim+jpn+kor+ara+tam"
    )

    print("Detected text:", text)

    return text

# ---------------- CORE ----------------
def extract_translate_speak(text):
    if not text.strip():
        messagebox.showinfo("Info", "No text detected")
        return

    text_output.delete(1.0, tk.END)
    text_output.insert(tk.END, text)

    target_lang = lang_var.get()
    translated = translator.translate(text, target_lang)

    if translated:
        text_output.insert(tk.END, "\n\n--- TRANSLATED ---\n" + translated)
        tts.speak(translated, lang_map[target_lang])
    else:
        tts.speak(text, lang_map[target_lang])

# ---------------- ACTIONS ----------------
def capture_action():

    global current_frame

    if current_frame is None:
        messagebox.showwarning("Warning","Camera not ready")
        return

    frame = current_frame.copy()


    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(5,5),0)
    gray = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

    pil = Image.fromarray(gray)

    text = pytesseract.image_to_string(
        pil,
        lang="eng+tel+hin+mal+urd+deu+chi_sim+jpn+kor+ara+tam",
        config="--psm 6"
    )

    print("Detected:", text)

    extract_translate_speak(text)

def upload_action():
    path = filedialog.askopenfilename()

    if not path:
        return

    ext = os.path.splitext(path)[1].lower()

    if ext in [".png", ".jpg", ".jpeg"]:
        pil = read_image_file(path)

        if pil is None:
            messagebox.showerror("Error", "Image not loaded")
            return

        text = do_ocr(pil)

    elif ext == ".pdf":
        pil = read_pdf_first_page(path)

        if pil is None:
            messagebox.showerror("Error", "PDF not loaded")
            return

        text = do_ocr(pil)

    elif ext == ".txt":
        text = read_text_file(path)

    else:
        messagebox.showerror("Error", "Unsupported file")
        return

    extract_translate_speak(text)

# 🎙 MULTI-LANGUAGE VOICE COMMANDS
def voice_command_action():
    spoken = vc.listen_once(4)
    if not spoken:
        return

    # Convert ANY language → English for command understanding
    cmd = translator.translate(spoken, "English") or spoken
    cmd = cmd.lower()
    print("Command:", cmd)

    if any(word in cmd for word in ["capture","photo","click","take picture"]):
        capture_action()

    elif any(word in cmd for word in ["upload","file","open file"]):
        upload_action()

    elif any(word in cmd for word in ["translate","speak","read"]):
        voice_translate_speak()

    elif any(word in cmd for word in ["quit","exit","close"]):
        quit_action()

# 🎤 Translate & Speak (Voice → Voice)
import speech_recognition as sr

def voice_translate_speak():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Speak now...")
        audio = r.listen(source)

    try:
        spoken = r.recognize_google(audio)
        print("Detected speech:", spoken)

    except Exception as e:
        messagebox.showerror("Error","Could not understand speech")
        return

    target_lang_name = lang_var.get()
    target_lang_code = lang_map[target_lang_name]

    translated = translator.translate(spoken, target_lang_name)

    if not translated:
        messagebox.showwarning("Translation","Translation failed")
        return

    print("Translated:", translated)

    text_output.delete(1.0, tk.END)
    text_output.insert(tk.END, translated)

    tts.speak(translated, target_lang_code)

def clear_action():
    text_output.delete(1.0, tk.END)

def quit_action():
    cap.release()
    root.destroy()

# ---------------- BUTTONS ----------------
ttk.Button(left, text="Capture", command=lambda: threading.Thread(target=capture_action, daemon=True).start()).pack(fill=tk.X, pady=5)
ttk.Button(left, text="Upload File", command=lambda: threading.Thread(target=upload_action, daemon=True).start()).pack(fill=tk.X, pady=5)
ttk.Button(left, text="Voice Command", command=lambda: threading.Thread(target=voice_command_action, daemon=True).start()).pack(fill=tk.X, pady=5)
ttk.Button(left, text="AI Assistant", command=open_ai_assistant).pack(fill=tk.X, pady=5)
ttk.Button(left, text="Translate & Speak", command=lambda: threading.Thread(target=voice_translate_speak, daemon=True).start()).pack(fill=tk.X, pady=5)
ttk.Button(left, text="Clear", command=clear_action).pack(fill=tk.X, pady=5)
ttk.Button(left, text="Quit", command=quit_action).pack(fill=tk.X, pady=5)


update_camera()
root.mainloop()