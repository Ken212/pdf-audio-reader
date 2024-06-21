import tkinter as tk
from tkinter import filedialog
import PyPDF2
import pyttsx3
import threading

class PDFToAudioApp:
    def __init__(self, root):
        self.root = root
        self.text_extracted = ""
        self.rate = tk.IntVar(value=200)
        self.voice_choice = tk.StringVar(value='male')
        self.setup_ui()

        self.speaking_thread = None
        self.stop_event = threading.Event()

    def extract_text(self):
        file = filedialog.askopenfile(parent=self.root, mode="rb", title="Choose a PDF File")
        if file:
            pdf_reader = PyPDF2.PdfReader(file)
            self.text_extracted = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                self.text_extracted += page.extract_text()
            file.close()

    def speak_text(self):
        engine = pyttsx3.init()
        engine.setProperty("rate", self.rate.get())
        all_voices = engine.getProperty("voices")
        voice_id = all_voices[0].id if self.voice_choice.get() == 'male' else all_voices[1].id
        engine.setProperty("voice", voice_id)

        self.stop_event.clear()
        for text in self.text_extracted.split('\n'):
            if self.stop_event.is_set():
                break
            engine.say(text)
            engine.runAndWait()

    def start_speaking(self):
        if self.speaking_thread and self.speaking_thread.is_alive():
            self.stop_speaking()
        self.speaking_thread = threading.Thread(target=self.speak_text)
        self.speaking_thread.start()

    def stop_speaking(self):
        self.stop_event.set()
        if self.speaking_thread and self.speaking_thread.is_alive():
            self.speaking_thread.join()

    def setup_ui(self):
        self.root.geometry("700x600")
        self.root.resizable(width=False, height=False)
        self.root.title("PDF to AUDIO")
        self.root.configure(background="#2e2e2e")

        # Frame 1
        frame1 = tk.Frame(self.root, width=500, height=200, bg="#4e4e4e")
        frame1.pack(side="top", fill="both")

        name1 = tk.Label(frame1, text="PDF to AUDIO", fg="#ffffff", bg="#4e4e4e", font=("Arial", 28, "bold"))
        name1.pack(pady=10)

        name2 = tk.Label(frame1, text="Listen to your PDF File", fg="#ffffff", bg="#4e4e4e", font=("Calibre", 25, "bold"))
        name2.pack(pady=10)

        # Frame 2
        frame2 = tk.Frame(self.root, width=500, height=450, bg="#2e2e2e")
        frame2.pack(side="top", fill="y")

        btn = tk.Button(frame2, text="Select PDF File", activeforeground="#ff0000", command=self.extract_text, padx=70, pady=10, fg="#ffffff", bg="#4e4e4e", font=("Arial", 12))
        btn.grid(row=0, pady=20, columnspan=2)

        rate_text = tk.Label(frame2, text="Enter Rate of Speech", fg="#ffffff", bg="#2e2e2e", font=("Arial", 12))
        rate_text.grid(row=1, column=0, pady=15, padx=0, sticky=tk.E)

        rate_entry = tk.Entry(frame2, textvariable=self.rate, fg="#000000", bg="#ffffff", font=("Arial", 12))
        rate_entry.grid(row=1, column=1, padx=30, pady=15, sticky=tk.W)

        voice_text = tk.Label(frame2, text="Select Voice:", fg="#ffffff", bg="#2e2e2e", font=("Arial", 12))
        voice_text.grid(row=2, column=0, pady=15, padx=0, sticky=tk.E)

        male_rb = tk.Radiobutton(frame2, text="Male", variable=self.voice_choice, value='male', fg="#ffffff", bg="#2e2e2e", font=("Arial", 12), selectcolor="#4e4e4e")
        male_rb.grid(row=2, column=1, pady=5, padx=30, sticky=tk.W)

        female_rb = tk.Radiobutton(frame2, text="Female", variable=self.voice_choice, value='female', fg="#ffffff", bg="#2e2e2e", font=("Arial", 12), selectcolor="#4e4e4e")
        female_rb.grid(row=3, column=1, pady=5, padx=30, sticky=tk.W)

        submit_btn = tk.Button(frame2, text="Play PDF File", command=self.start_speaking, activeforeground="#ff0000", padx=60, pady=10, fg="#ffffff", bg="#4e4e4e", font=("Arial", 12))
        submit_btn.grid(row=4, column=0, pady=65)

        stop_btn = tk.Button(frame2, text="Stop Playing", command=self.stop_speaking, activeforeground="#ff0000", padx=60, pady=10, fg="#ffffff", bg="#4e4e4e", font=("Arial", 12))
        stop_btn.grid(row=4, column=1, pady=65)


if __name__ == "__main__":
    root = tk.Tk()
    app = PDFToAudioApp(root)
    root.mainloop()
