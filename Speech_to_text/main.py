import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
from textblob import TextBlob
import threading
import time

class SpeechNLPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Speech to Text NLP Analyzer")
        self.root.geometry("500x600")
        self.root.configure(bg="#f0f4f8")
        self.root.resizable(False, False)

        # UI Constants
        self.primary_color = "#2c3e50"
        self.accent_color = "#3498db"
        self.bg_color = "#f0f4f8"
        self.text_color = "#34495e"
        self.button_color = "#27ae60"

        self.is_recording = False
        self.setup_ui()

    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg=self.primary_color, pady=20)
        header_frame.pack(fill="x")
        
        header_label = tk.Label(
            header_frame, 
            text="Speech to Text NLP Analyzer", 
            font=("Helvetica", 18, "bold"), 
            fg="white", 
            bg=self.primary_color
        )
        header_label.pack()

        # Main Content Frame
        content_frame = tk.Frame(self.root, bg=self.bg_color, padx=30, pady=20)
        content_frame.pack(fill="both", expand=True)

        # Start Button
        self.record_btn = tk.Button(
            content_frame,
            text="🎤 Start Recording",
            font=("Helvetica", 12, "bold"),
            bg=self.button_color,
            fg="white",
            padx=20,
            pady=10,
            relief="flat",
            command=self.start_recording_thread,
            activebackground="#219150",
            activeforeground="white"
        )
        self.record_btn.pack(pady=20)

        # Status Label
        self.status_label = tk.Label(
            content_frame,
            text="Click the button to start",
            font=("Helvetica", 10, "italic"),
            bg=self.bg_color,
            fg="#7f8c8d"
        )
        self.status_label.pack()

        # Recognized Text Area
        tk.Label(
            content_frame, 
            text="Recognized Text:", 
            font=("Helvetica", 11, "bold"), 
            bg=self.bg_color, 
            fg=self.text_color
        ).pack(anchor="w", pady=(20, 5))

        self.text_display = tk.Text(
            content_frame,
            height=6,
            font=("Helvetica", 11),
            padx=10,
            pady=10,
            wrap="word",
            bg="white",
            relief="solid",
            borderwidth=1
        )
        self.text_display.pack(fill="x")
        self.text_display.config(state="disabled")

        # Results Frame
        results_frame = tk.Frame(content_frame, bg=self.bg_color, pady=20)
        results_frame.pack(fill="x")

        # Sentiment Label
        tk.Label(
            results_frame, 
            text="Sentiment:", 
            font=("Helvetica", 12, "bold"), 
            bg=self.bg_color, 
            fg=self.text_color
        ).grid(row=0, column=0, sticky="w")

        self.sentiment_val = tk.Label(
            results_frame, 
            text="---", 
            font=("Helvetica", 12), 
            bg=self.bg_color, 
            fg=self.accent_color
        )
        self.sentiment_val.grid(row=0, column=1, padx=10, sticky="w")

        # Confidence Label
        tk.Label(
            results_frame, 
            text="Confidence:", 
            font=("Helvetica", 12, "bold"), 
            bg=self.bg_color, 
            fg=self.text_color
        ).grid(row=1, column=0, sticky="w", pady=10)

        self.confidence_val = tk.Label(
            results_frame, 
            text="---", 
            font=("Helvetica", 12), 
            bg=self.bg_color, 
            fg=self.accent_color
        )
        self.confidence_val.grid(row=1, column=1, padx=10, sticky="w", pady=10)

    def update_status(self, text, color="#7f8c8d"):
        self.status_label.config(text=text, fg=color)

    def update_text(self, text):
        self.text_display.config(state="normal")
        self.text_display.delete("1.0", tk.END)
        self.text_display.insert(tk.END, text)
        self.text_display.config(state="disabled")

    def analyze_sentiment(self, text):
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        if polarity > 0.1:
            sentiment = "Positive 😊"
            color = "#27ae60"
        elif polarity < -0.1:
            sentiment = "Negative 😡"
            color = "#c0392b"
        else:
            sentiment = "Neutral 😐"
            color = "#f39c12"

        # Confidence calculation: using absolute polarity + some base value, capped at 99%
        # Or more realistically, use subjectivity as well
        confidence = min(99, int((abs(polarity) * 50) + 50))
        
        return sentiment, color, f"{confidence}%"

    def start_recording_thread(self):
        if self.is_recording:
            return
        
        self.is_recording = True
        self.record_btn.config(state="disabled", bg="#95a5a6")
        self.update_status("🎤 Listening...", "#e74c3c")
        self.update_text("")
        self.sentiment_val.config(text="---", fg=self.accent_color)
        self.confidence_val.config(text="---", fg=self.accent_color)
        
        threading.Thread(target=self.record_and_process, daemon=True).start()

    def record_and_process(self):
        recognizer = sr.Recognizer()
        
        # Debug: List microphones to console
        try:
            mic_list = sr.Microphone.list_microphone_names()
            print("\n--- Available Microphones ---")
            for i, name in enumerate(mic_list):
                print(f"Index {i}: {name}")
            print("-----------------------------\n")
        except Exception as e:
            print(f"Could not list microphones: {e}")

        try:
            # Using default microphone
            with sr.Microphone() as source:
                self.root.after(0, lambda: self.update_status("🎤 Calibrating noise...", "#f39c12"))
                recognizer.adjust_for_ambient_noise(source, duration=1.5)
                recognizer.energy_threshold += 50  # Slight boost to avoid picking up tiny noises
                
                self.root.after(0, lambda: self.update_status("🎤 Listening (Start speaking now)...", "#e74c3c"))
                # Increased timeout to 10 and phrase limit to 15
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
                
            self.root.after(0, lambda: self.update_status("⚙️ Processing...", self.accent_color))
            
            # Convert speech to text
            text = recognizer.recognize_google(audio)
            
            # Analyze sentiment
            sentiment, color, confidence = self.analyze_sentiment(text)
            
            # Update UI
            self.root.after(0, lambda: self.update_text(text))
            self.root.after(0, lambda: self.sentiment_val.config(text=sentiment, fg=color))
            self.root.after(0, lambda: self.confidence_val.config(text=confidence, fg=color))
            self.root.after(0, lambda: self.update_status("✅ Done!", "#27ae60"))

        except sr.WaitTimeoutError:
            self.root.after(0, lambda: self.update_status("❌ No speech detected.", "#c0392b"))
        except sr.UnknownValueError:
            self.root.after(0, lambda: self.update_status("❌ Could not understand speech.", "#c0392b"))
        except sr.RequestError as e:
            self.root.after(0, lambda: messagebox.showerror("API Error", f"Could not request results; {e}"))
            self.root.after(0, lambda: self.update_status("❌ API Error.", "#c0392b"))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"An error occurred: {e}"))
            self.root.after(0, lambda: self.update_status("❌ Error occurred.", "#c0392b"))
        finally:
            self.is_recording = False
            self.root.after(0, lambda: self.record_btn.config(state="normal", bg=self.button_color))

if __name__ == "__main__":
    root = tk.Tk()
    app = SpeechNLPApp(root)
    root.mainloop()
