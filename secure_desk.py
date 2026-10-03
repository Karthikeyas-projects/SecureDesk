import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import re


LYNIS_COMMAND = ["./lynis", "audit", "system"]


class SecureDesk(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("SECURE DESK")
        self.geometry("900x620")
        self.minsize(760, 500)
        self.configure(bg="#f5f5f5")

        self.scan_button = None
        self.status_label = None
        self.progress = None
        self.score_label = None
        self.problems_text = None

        self.build_ui()

    def build_ui(self):
        # Fixed top bar
        top_bar = tk.Frame(self, bg="#202020", height=64)
        top_bar.pack(side="top", fill="x")
        top_bar.pack_propagate(False)

        title = tk.Label(
            top_bar,
            text="SECURE DESK",
            bg="#202020",
            fg="white",
            font=("Arial", 20, "bold"),
        )
        title.pack(side="left", padx=22)

        # Main content
        content = tk.Frame(self, bg="#f5f5f5")
        content.pack(fill="both", expand=True, padx=28, pady=28)

        intro = tk.Label(
            content,
            text="Linux Security Scanner",
            bg="#f5f5f5",
            fg="#222222",
            font=("Arial", 22, "bold"),
        )
        intro.pack(anchor="w")

        self.status_label = tk.Label(
            content,
            text="Ready to scan",
            bg="#f5f5f5",
            fg="#666666",
            font=("Arial", 11),
        )
        self.status_label.pack(anchor="w", pady=(5, 18))

        self.scan_button = tk.Button(
            content,
            text="SCAN NOW",
            command=self.start_scan,
            bg="#d62828",
            fg="white",
            activebackground="#b91f1f",
            activeforeground="white",
            font=("Arial", 13, "bold"),
            relief="flat",
            padx=28,
            pady=12,
            cursor="hand2",
        )
        self.scan_button.pack(anchor="w")

        # Indeterminate progress bar shown only during scan
        self.progress = ttk.Progressbar(
            content,
            mode="indeterminate",
            length=420,
        )
        self.progress.pack(anchor="w", pady=(15, 24))
        self.progress.stop()
        self.progress.pack_forget()

        # Results area
        results = tk.Frame(content, bg="white", bd=1, relief="solid")
        results.pack(fill="both", expand=True, pady=(5, 0))

        score_box = tk.Frame(results, bg="white")
        score_box.pack(fill="x", padx=18, pady=18)

        tk.Label(
            score_box,
            text="SECURITY SCORE",
            bg="white",
            fg="#666666",
            font=("Arial", 10, "bold"),
        ).pack(anchor="w")

        self.score_label = tk.Label(
            score_box,
            text="—",
            bg="white",
            fg="#222222",
            font=("Arial", 34, "bold"),
        )
        self.score_label.pack(anchor="w", pady=(2, 0))

        tk.Label(
            results,
            text="PROBLEMS",
            bg="white",
            fg="#666666",
            font=("Arial", 10, "bold"),
        ).pack(anchor="w", padx=18, pady=(0, 8))

        text_frame = tk.Frame(results, bg="white")
        text_frame.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")

        self.problems_text = tk.Text(
            text_frame,
            wrap="word",
            font=("Consolas", 10),
            bg="#fafafa",
            fg="#222222",
            relief="flat",
            yscrollcommand=scrollbar.set,
        )
        self.problems_text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.problems_text.yview)

        self.problems_text.insert(
            "1.0",
            "No scan has been run yet."
        )
        self.problems_text.config(state="disabled")

    def start_scan(self):
        self.scan_button.config(state="disabled")
        self.status_label.config(
            text="Running Lynis audit... Please wait."
        )

        self.score_label.config(text="Scanning...")
        self.set_problems("Lynis is scanning the system...\n")

        self.progress.pack(anchor="w", pady=(15, 24))
        self.progress.start(10)

        # Run in a background thread so the GUI does not freeze.
        thread = threading.Thread(
            target=self.run_lynis,
            daemon=True
        )
        thread.start()

    def run_lynis(self):
        try:
            process = subprocess.Popen(
                LYNIS_COMMAND,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )

            output_lines = []

            for line in process.stdout:
                output_lines.append(line)

            return_code = process.wait()
            output = "".join(output_lines)

            self.after(
                0,
                self.scan_finished,
                return_code,
                output
            )

        except FileNotFoundError:
            self.after(
                0,
                self.scan_failed,
                "Could not find ./lynis.\n\n"
                "Make sure the Lynis script is in the same folder "
                "as this Python file and is executable."
            )
        except Exception as exc:
            self.after(
                0,
                self.scan_failed,
                str(exc)
            )

    def scan_finished(self, return_code, output):
        self.progress.stop()
        self.progress.pack_forget()
        self.scan_button.config(state="normal")

        if return_code != 0:
            self.status_label.config(
                text="Lynis finished with an error."
            )
            self.score_label.config(text="—")
            self.set_problems(
                output.strip()
                or "Lynis did not return any output."
            )

            messagebox.showerror(
                "Lynis Error",
                "Lynis returned an error.\n\n"
                "Check the output in the Problems box."
            )
            return

        score = self.extract_score(output)
        problems = self.extract_problems(output)

        self.status_label.config(
            text="Scan complete."
        )

        self.score_label.config(
            text=score if score is not None else "Not found"
        )

        if problems:
            self.set_problems("\n\n".join(problems))
        else:
            self.set_problems(
                "No warning/suggestion lines were found in "
                "the Lynis terminal output."
            )

    def scan_failed(self, error):
        self.progress.stop()
        self.progress.pack_forget()
        self.scan_button.config(state="normal")
        self.status_label.config(text="Scan failed.")
        self.score_label.config(text="—")
        self.set_problems(error)

        messagebox.showerror(
            "Scan Failed",
            error
        )

    @staticmethod
    def clean_ansi(text):
        # Remove terminal color/control sequences.
        return re.sub(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])", "", text)

    def extract_score(self, output):
        cleaned = self.clean_ansi(output)

        # Typical Lynis output:
        # Hardening index : 64
        match = re.search(
            r"Hardening\s+index\s*:\s*(\d+)",
            cleaned,
            re.IGNORECASE
        )

        if match:
            return match.group(1) + " / 100"

        # Fallback for slightly different formatting.
        match = re.search(
            r"Hardening\s+index.*?(\d{1,3})",
            cleaned,
            re.IGNORECASE | re.DOTALL
        )

        if match:
            return match.group(1) + " / 100"

        return None

    def extract_problems(self, output):
        cleaned = self.clean_ansi(output)
        problems = []

        # Prefer the actual warning/suggestion lines printed by Lynis.
        for raw_line in cleaned.splitlines():
            line = raw_line.strip()

            if "[WARNING]" in line.upper() or "[SUGGESTION]" in line.upper():
                line = re.sub(r"^\s*[-*]\s*", "", line)
                problems.append(line)

        # Remove duplicates while keeping order.
        unique = []
        seen = set()

        for item in problems:
            if item not in seen:
                seen.add(item)
                unique.append(item)

        return unique

    def set_problems(self, text):
        self.problems_text.config(state="normal")
        self.problems_text.delete("1.0", "end")
        self.problems_text.insert("1.0", text)
        self.problems_text.config(state="disabled")


if __name__ == "__main__":
    app = SecureDesk()
    app.mainloop()
