import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import subprocess
import os

from file_reader import read_text_file
from tts_engine import TTSEngine

tts = TTSEngine()

def run_ollama(prompt: str) -> str:
    try:
        process = subprocess.Popen(
            ["ollama", "run", "mistral"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        output, _ = process.communicate(prompt, timeout=120)
        return output.strip()
    except Exception as e:
        return f"Error: {e}"

def open_ai_assistant():
    win = tk.Toplevel()
    win.title("AI Assistant – Document Summarizer")
    win.geometry("800x600")

    text_area = scrolledtext.ScrolledText(win, wrap=tk.WORD)
    text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    summary_area = scrolledtext.ScrolledText(win, wrap=tk.WORD, height=8)
    summary_area.pack(fill=tk.X, padx=10, pady=10)

    loaded_text = {"content": ""}

    def upload_file():
        path = filedialog.askopenfilename(
            filetypes=[("Text Files","*.txt"),("All Files","*.*")]
        )
        if not path:
            return

        try:
            content = read_text_file(path)
            loaded_text["content"] = content
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, content)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def summarize():
        if not loaded_text["content"]:
            messagebox.showinfo("Info", "Upload a file first")
            return

        prompt = (
            "Summarize the following text in simple English, short and clear:\n\n"
            + loaded_text["content"]
        )

        summary = run_ollama(prompt)
        summary_area.delete(1.0, tk.END)
        summary_area.insert(tk.END, summary)

    def speak_summary():
        text = summary_area.get(1.0, tk.END).strip()
        if text:
            tts.speak(text)

    btn_frame = ttk.Frame(win)
    btn_frame.pack(pady=10)

    ttk.Button(btn_frame, text="Upload File", command=upload_file).pack(side=tk.LEFT, padx=5)
    ttk.Button(btn_frame, text="Summarize", command=summarize).pack(side=tk.LEFT, padx=5)
    ttk.Button(btn_frame, text="Speak Summary", command=speak_summary).pack(side=tk.LEFT, padx=5)
    ttk.Button(btn_frame, text="Close", command=win.destroy).pack(side=tk.LEFT, padx=5)

# Allow standalone testing
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    open_ai_assistant()
    root.mainloop()
