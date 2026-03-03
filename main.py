import os
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, ttk

from PIL import Image


class App(tk.Tk):
    RESIZE_OPTIONS = ["25%", "33.3%", "50%", "100%", "200%", "400%"]

    def __init__(self):
        super().__init__()

        self.title("Image Tools")
        self.geometry("500x600")
        self.configure(padx=20, pady=20, bg="#c2d6d6")

        self.work_mode = tk.IntVar(value=1)
        self.last_mode = None

        self.selected_path = tk.StringVar(value="No image selected...")

        self.images_count = 0

        self.images_count_label = tk.Label(
            self,
            text=self.images_count,
        )

        self.settings_frame = tk.LabelFrame(
            self,
            text="  Settings  ",
            labelanchor="n",
            padx=15,
            pady=15,
        )

        self.tree_frame = tk.LabelFrame(
            self,
            text="  Images List & Info  ",
            labelanchor="n",
            padx=10,
            pady=10
        )

        columns = ("name", "resolution", "type", "target") # TODO: change
        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=columns,
            show="headings",
        )

        self.resize_percent = tk.StringVar(value="100%")

        self.setup_ui()

    def setup_ui(self):
        title_label = tk.Label(
            self,
            text="Image Tools",
            font=("Helvetica", 24, "bold"),
            fg="#2c3e50",
            bg="#c2d6d6"
        )
        title_label.pack(pady=(0, 5))

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

        path_frame = tk.LabelFrame(
            self,
            text="  Path  ",
            labelanchor="n",
            padx=15,
            pady=10
        )
        path_frame.pack(fill="x", pady=(0, 5))

        path_entry = tk.Entry(
            path_frame,
            textvariable=self.selected_path,
            state="readonly",
        )
        path_entry.pack(
            side="left",
            padx=(0, 10),
            expand=True,
            fill="x"
        )

        browse_button = tk.Button(path_frame, text="Browse", command=self.browse_path)
        browse_button.pack(side="right")

        resize_frame = tk.Frame(self.settings_frame)
        resize_frame.pack(fill="x", pady=(0, 5))
        tk.Label(
            resize_frame,
            text="Resize"
        ).pack(side="left")
        tk.OptionMenu(
            resize_frame,
            self.resize_percent,
            *self.RESIZE_OPTIONS
        ).pack(side="left", padx=(10, 0))
        tk.Button(
            resize_frame,
            text="Apply",
            command=lambda: self.start_processing(self.selected_path.get())
        ).pack(
            side="bottom",
            padx=(0, 10)
        )

        self.tree.heading("name", text="Name")
        self.tree.heading("resolution", text="Resolution")
        self.tree.heading("type", text="From")
        self.tree.heading("target", text="To")

        self.tree.column("name", width=150)
        self.tree.column("resolution", width=100)
        self.tree.column("type", width=60)
        self.tree.column("target", width=60)

        self.tree.pack(side="left", fill="both", expand=True)

        scroller = ttk.Scrollbar(
            self.tree_frame,
            orient="vertical",
            command=self.tree.yview,
        )
        self.tree.configure(yscrollcommand=scroller.set)
        scroller.pack(side="right", fill="y")

    def update_ui(self, new_path=None):
        if new_path:
            self.selected_path.set(new_path)
            if self.work_mode.get() == 2:
                self.images_count_label.pack()
        else:
            if self.work_mode.get() == 1:
                self.selected_path.set("No image selected...")
            else:
                self.selected_path.set("No path selected...")
            self.images_count_label.pack_forget()
            self.settings_frame.pack_forget()
            self.tree_frame.pack_forget()

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
            self.settings_frame.pack(fill="both", expand=True, pady=10)

            self.tree_frame.pack(fill="both", expand=True, pady=10)
            self.populate_tree(path)
            if self.work_mode.get() == 2:
                self.imgs_count()

    def change_mode(self):
        current_mode = self.work_mode.get()
        if current_mode == self.last_mode:
            return

        self.last_mode = current_mode
        self.update_ui()

    def imgs_count(self):
        folder_path = self.selected_path.get()
        if folder_path == "No path selected...":
            return

        self.images_count = len([x for x in os.listdir(folder_path) if x.endswith((".jpg", ".png", ".webp", ".jpeg"))])
        self.images_count_label.config(text=f"Images found: {self.images_count}")

    def populate_tree(self, path):
        for item in self.tree.get_children():
            self.tree.delete(item)

        valid_extensions = (".jpg", ".png", ".webp", ".jpeg")
        files = []

        if os.path.isfile(path):
            files.append(path)
        elif os.path.isdir(path):
            files = [os.path.join(path, f) for f in os.listdir(path)
                     if f.lower().endswith(valid_extensions)]

        for image_path in files:
            with Image.open(image_path) as image:
                name = os.path.basename(image_path)
                res = f"{image.width}x{image.height}"
                fmt = image.format
                target = "WEBP"  # TODO: change
                self.tree.insert("", "end", values=(name, res, fmt, target))

    def start_processing(self, path):
        percent_str = self.resize_percent.get()
        scale_factor = float(percent_str.replace('%', '')) / 100

        files_to_process = []

        if os.path.isfile(path):
            files_to_process.append(path)
            output_dir = os.path.join(os.path.dirname(path), "output")
        else:  # os.path.isdir(path):
            valid_extensions = (".jpg", ".png", ".webp", ".jpeg")
            files_to_process = [os.path.join(path, f) for f in os.listdir(path)
                                if f.lower().endswith(valid_extensions)]
            output_dir = os.path.join(path, "output")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for file_path in files_to_process:
            with Image.open(file_path) as image:
                new_w = int(image.width * scale_factor)
                new_h = int(image.height * scale_factor)

                resized_img = image.resize((new_w, new_h), Image.Resampling.LANCZOS)

                save_path = Path(output_dir) / Path(file_path).with_suffix('.webp').name
                # TODO: add quality option
                resized_img.save(save_path, "webp")


if __name__ == "__main__":
    app = App()
    app.mainloop()
