import tkinter as tk
from tkinter import filedialog


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Image Tools")
        self.geometry("500x600")
        self.configure(padx=20, pady=20, bg="#c2d6d6")

        self.work_mode = tk.IntVar(value=1)
        self.last_mode = None

        self.selected_path = tk.StringVar(value="No path selected...")

        self.setup_ui()

    def setup_ui(self):
        title_label = tk.Label(
            self,
            text="Image Tools",
            font=("Helvetica", 24, "bold"),
            fg="#2c3e50",
            bg="#c2d6d6"
        )
        title_label.pack(pady=(0, 20))

        mode_frame = tk.LabelFrame(
            self,
            text="  Operation Mode  ",
            labelanchor="n",
            padx=15,
            pady=10,
        )
        mode_frame.pack(
            fill="x",
            pady=10
        )

        tk.Radiobutton(
            mode_frame,
            text="Single Image File",
            variable=self.work_mode,
            value=1,
            command=self.change_mode
        ).pack(anchor="w")

        tk.Radiobutton(
            mode_frame,
            text="Entire Folder (Batch)",
            variable=self.work_mode,
            value=2,
            command=self.change_mode
        ).pack(anchor="w")

        path_frame = tk.Frame(self)
        path_frame.pack(fill="x", pady=20)

        path_entry = tk.Entry(path_frame, textvariable=self.selected_path, state="readonly", width=40)
        path_entry.pack(side="left", padx=(0, 10), expand=True, fill="x")

        browse_btn = tk.Button(path_frame, text="Browse", command=self.browse_path)
        browse_btn.pack(side="right")

    def update_ui(self, new_path=None):
        if new_path:
            self.selected_path.set(new_path)
        else:
            self.selected_path.set("No path selected...")

        print(self.work_mode.get(), self.selected_path.get())

    def browse_path(self):
        if self.work_mode.get() == 1:
            path = filedialog.askopenfilename(
                filetypes=[("Images", "*.jpg *.png *.webp *.jpeg")]
            )
        else:
            path = filedialog.askdirectory()

        if path:
            self.update_ui(new_path=path)

    def change_mode(self):
        current_mode = self.work_mode.get()
        if current_mode == self.last_mode:
            return

        self.last_mode = current_mode
        self.update_ui()


if __name__ == "__main__":
    app = App()
    app.mainloop()
