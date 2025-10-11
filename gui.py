import json
import requests
import operator
import tkinter as tk
from tkinter import scrolledtext
from input_parser import InputParser
from musicrecs import run_recommendations
import threading

class MusicRecsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Recommender")
        self.root.geometry("600x500")

        # Input Frame
        input_frame = tk.Frame(root, padx=10, pady=10)
        input_frame.pack(fill=tk.X)

        tk.Label(input_frame, text="Enter your favorite artists (Artist%Weight):").pack(anchor=tk.W)
        self.input_text = scrolledtext.ScrolledText(input_frame, width=60, height=10)
        self.input_text.pack(fill=tk.X, expand=True)
        self.input_text.insert(tk.INSERT, "The Beatles%3\nRadiohead%2\nPink Floyd%2.5")

        # Control Frame
        control_frame = tk.Frame(root)
        control_frame.pack(pady=5)

        self.run_button = tk.Button(control_frame, text="Get Recommendations", command=self.start_recommendation_thread)
        self.run_button.pack()

        # Output Frame
        output_frame = tk.Frame(root, padx=10, pady=10)
        output_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(output_frame, text="Recommendations:").pack(anchor=tk.W)
        self.output_text = scrolledtext.ScrolledText(output_frame, width=80, height=15)
        self.output_text.pack(fill=tk.BOTH, expand=True)

    def start_recommendation_thread(self):
        self.run_button.config(state=tk.DISABLED)
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert(tk.INSERT, "Working on it... this may take a moment.\n")
        self.root.update_idletasks()
        
        thread = threading.Thread(target=self.compute_recommendations)
        thread.daemon = True
        thread.start()

    def compute_recommendations(self):
        input_data = self.input_text.get("1.0", tk.END)
        
        parser = InputParser()
        try:
            startup_weights, max_weight = parser.parse_from_text(input_data)
        except Exception as e:
            self.update_output(f"Error parsing input: {e}\nPlease use the format: Artist Name%Weight\n")
            self.enable_button()
            return

        if not startup_weights:
            self.update_output("Please enter at least one artist.\n")
            self.enable_button()
            return

        try:
            recommendations, _ = run_recommendations(startup_weights, max_weight)
            
            output_content = ""
            if recommendations:
                for artist, weight in recommendations:
                    output_content += f"{artist}: {weight:.4f}\n"
            else:
                output_content = "Could not generate recommendations. Check your API key and network connection.\n"
            
            self.update_output(output_content, clear=True)

        except Exception as e:
            self.update_output(f"An error occurred: {e}\n")
        finally:
            self.enable_button()

    def update_output(self, text, clear=False):
        def task():
            if clear:
                self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, text)
        self.root.after(0, task)

    def enable_button(self):
        self.root.after(0, lambda: self.run_button.config(state=tk.NORMAL))


if __name__ == "__main__":
    root = tk.Tk()
    app = MusicRecsGUI(root)
    root.mainloop()