import os
import threading
import tkinter as tk
import webbrowser
from pathlib import Path
from tkinter import filedialog, ttk

from PIL import Image


class App(tk.Tk):
    RESIZE_OPTIONS = ["25%", "33.3%", "50%", "100%", "200%", "400%"]
    FILES_TYPES = ["JPG", "PNG", "WEBP", "JPEG"]

    def __init__(self):
        super().__init__()

        self.title("Image Tools")
        self.geometry("700x900")
        self.configure(padx=20, pady=2, bg="#c2d6d6")

        self.work_mode = tk.IntVar(value=1)
        self.last_mode = None

        self.selected_path = tk.StringVar(value="No image selected...")

        self.single_image_mode = None
        self.batch_folder_mode = None

        self.browse_button = None
        self.images_count = 0

        self.no_images_label = tk.Label(
            self,
            text="No images found in the selected folder.",
            font=("Arial", 15),
            bg="#c2d6d6",
            fg="#800020"
        )

        self.settings_frame = tk.LabelFrame(
            self,
            text="  Settings  ",
            labelanchor="n",
            padx=15,
            pady=15,
        )

        self.target_format = tk.StringVar(value="WEBP")
        self.target_format.trace_add("write", lambda name, index, mode: self.populate_tree(self.selected_path.get()))
        self.target_format_types = self.FILES_TYPES

        self.quality = tk.IntVar(value=75)
        self.quality.trace_add("write", lambda name, index, mode: self.populate_tree(self.selected_path.get()))

        self.buttons_frame = tk.Frame(
            self.settings_frame,
            padx=15,
            pady=15,
        )
        self.start_button = tk.Button(
            self.buttons_frame,
            text="Start",
            command=self.run_processing_thread,
            width=10,
            height=2
        )

        self.are_images_done = False
        self.open_output_folder_button = tk.Button(
            self.buttons_frame,
            text="Open Output Folder",
            command=lambda: self.open_output_folder(self.selected_path.get()),
            width=15,
            height=2
        )

        self.tree_frame = tk.LabelFrame(
            self,
            text="  Images List & Info  ",
            labelanchor="n",
            padx=10,
            pady=10
        )

        columns = ("name", "resolution", "type", "old_size", "new_size")

        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=columns,
            show="headings",
        )

        self.resize_percent = tk.StringVar(value="100%")
        self.resize_percent.trace_add("write", lambda name, index, mode: self.populate_tree(self.selected_path.get()))

        self.progress = ttk.Progressbar(
            self.settings_frame,
            orient="horizontal",
            length=400,
        )

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
            pady=(0, 5)
        )

        self.single_image_mode = tk.Radiobutton(
            mode_frame,
            text="Single Image File",
            variable=self.work_mode,
            value=1,
            command=self.change_mode,
            font=("Arial", 10)
        )
        self.single_image_mode.pack(anchor="w")

        self.batch_folder_mode = tk.Radiobutton(
            mode_frame,
            text="Entire Folder (Batch)",
            variable=self.work_mode,
            value=2,
            command=self.change_mode,
            font=("Arial", 10)
        )
        self.batch_folder_mode.pack(anchor="w")

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
            width=40,
            font=("Arial", 11)
        )
        path_entry.pack(
            side="left",
            padx=(0, 10),
            expand=True,
            fill="x"
        )

        self.browse_button = tk.Button(
            path_frame,
            text="Browse",
            command=self.browse_path,
            width=10,
            height=2
        )
        self.browse_button.pack(side="right")

        format_frame = tk.Frame(self.settings_frame)
        format_frame.pack(fill="x", pady=(0, 10), padx=30)
        # inner_container_format = tk.Frame(format_frame)
        # inner_container_format.pack(anchor="center")
        tk.Label(
            format_frame,
            text="Target Format",
            font=("Arial", 14)
        ).pack(side="left", padx=(20, 0))
        format_options = ttk.Combobox(
            format_frame,
            textvariable=self.target_format,
            values=self.target_format_types,
            state="readonly",
            font=("Arial", 18),
            width=15
        )
        format_options.bind("<<ComboboxSelected>>", lambda e: format_frame.focus())
        format_options.pack(side="right")

        resize_frame = tk.Frame(self.settings_frame)
        resize_frame.pack(fill="x", pady=(0, 5), padx=30)
        # inner_container_resize = tk.Frame(resize_frame)
        # inner_container_resize.pack(anchor="center")
        tk.Label(
            resize_frame,
            text="Resize",
            font=("Arial", 14)
        ).pack(side="left", padx=(20, 0))
        resize_options = ttk.Combobox(
            resize_frame,
            textvariable=self.resize_percent,
            values=self.RESIZE_OPTIONS,
            state="readonly",
            font=("Arial", 18),
            width=15,
        )
        resize_options.bind("<<ComboboxSelected>>", lambda e: resize_frame.focus())
        resize_options.pack(side="right")

        quality_frame = tk.Frame(self.settings_frame)
        quality_frame.pack(fill="x", pady=5, padx=30)
        # inner_container_quality = tk.Frame(quality_frame)
        # inner_container_quality.pack(anchor="center")
        tk.Label(
            quality_frame,
            text="Quality",
            font=("Arial", 14),
        ).pack(side="left", padx=20)
        tk.Scale(
            quality_frame,
            from_=0,
            to=100,
            orient="horizontal",
            variable=self.quality,
            width=30,
            length=450,
            tickinterval=10,
            font=("Arial", 13),
        ).pack(pady=(0, 5), side="right")

        self.buttons_frame.pack(pady=5)
        self.start_button.pack(side="left", padx=(10, 0))

        self.progress.pack(
            fill="x",
            padx=50,
            pady=10,
        )

        self.tree.heading("name", text="Name")
        self.tree.heading("resolution", text="Resolution (Old -> New)")
        self.tree.heading("type", text="Type (Old -> New)")
        self.tree.heading("old_size", text="Original Size")
        self.tree.heading("new_size", text="New Size")

        self.tree.column("name", width=150)
        self.tree.column("resolution", width=180)
        self.tree.column("type", width=100)
        self.tree.column("old_size", width=70)
        self.tree.column("new_size", width=70)

        self.tree.pack(side="left", fill="both", expand=True)

        scroller = ttk.Scrollbar(
            self.tree_frame,
            orient="vertical",
            command=self.tree.yview,
        )
        self.tree.configure(yscrollcommand=scroller.set)
        scroller.pack(side="right", fill="y")

    def update_ui(self, new_path=None):
        self.no_images_label.pack_forget()
        self.settings_frame.pack_forget()
        self.target_format.set("WEBP")
        self.resize_percent.set("100%")
        self.quality.set(75)
        self.open_output_folder_button.pack_forget()
        self.tree_frame.pack_forget()
        self.progress["value"] = 0
        if new_path:
            self.selected_path.set(new_path)
        else:
            if self.work_mode.get() == 1:
                self.selected_path.set("No image selected...")
            else:
                self.selected_path.set("No path selected...")

    def browse_path(self):
        self.start_button.config(state="normal")
        self.browse_button.config(state="normal")
        if self.work_mode.get() == 1:
            path = filedialog.askopenfilename(
                filetypes=[("Images", "*.jpg *.png *.webp *.jpeg")]
            )
        else:
            path = filedialog.askdirectory()

        if path:
            self.update_ui(new_path=path)
            valid_extensions = (".jpg", ".png", ".webp", ".jpeg")
            if os.path.isdir(path):
                files = [f for f in os.listdir(path) if f.lower().endswith(valid_extensions)]
                count = len(files)
            else:
                count = 1 if path.lower().endswith(valid_extensions) else 0

            if count > 0:
                self.settings_frame.pack(fill="both", expand=True, pady=(0, 5))
                self.tree_frame.pack(fill="both", expand=True, pady=(0, 5))
                self.populate_tree(path)
                if self.work_mode.get() == 2:
                    self.images_count = count
                    self.settings_frame.config(text=f"  Settings (Images found: {self.images_count})  ")
            else:
                self.no_images_label.pack(pady=50)

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
        self.settings_frame.config(text=f"  Settings (Images found: {self.images_count})  ")

    def populate_tree(self, path):
        for item in self.tree.get_children():
            self.tree.delete(item)

        scale = float(self.resize_percent.get().replace('%', '')) / 100
        target_format = self.target_format.get()

        valid_extensions = {f".{ext.lower()}" for ext in self.FILES_TYPES}
        if Path(path).is_dir():
            files = [str(p) for p in Path(path).iterdir() if p.suffix.lower() in valid_extensions]
        elif Path(path).is_file():
            files = [path]
        else:
            files = []

        for image_path in files:
            with Image.open(image_path) as image:
                name = os.path.basename(image_path)
                source_fmt = image.format

                new_w, new_h = int(image.width * scale), int(image.height * scale)
                res_display = f"{image.width}x{image.height} -> {new_w}x{new_h}"

                type_display = f"{source_fmt} -> {target_format.upper()}"

                orig_bytes = os.path.getsize(image_path)
                orig_kb = orig_bytes / 1024

                if orig_kb < 1024:
                    size_display = f"{orig_kb:.1f} KB"
                else:
                    size_display = f"{orig_kb / 1024:.2f} MB"

                self.tree.insert("", "end", values=(name, res_display, type_display, size_display))

    def run_processing_thread(self):
        path = self.selected_path.get()
        if not path or path.startswith("No"):
            return

        self.start_button.config(state="disabled")
        self.browse_button.config(state="disabled")

        thread = threading.Thread(target=self.start_processing, args=(path,))
        thread.daemon = True
        thread.start()

    def start_processing(self, path):
        self.open_output_folder_button.pack_forget()
        percent_str = self.resize_percent.get()
        scale_factor = float(percent_str.replace('%', '')) / 100

        files_to_process = []

        if os.path.isfile(path):
            files_to_process.append(path)
            output_dir = os.path.join(os.path.dirname(path), "output")
        else:
            valid_extensions = (".jpg", ".png", ".webp", ".jpeg")
            files_to_process = [
                os.path.join(path, f)
                for f in os.listdir(path)
                if f.lower().endswith(valid_extensions)
            ]
            output_dir = os.path.join(path, "output")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        total_files = len(files_to_process)

        self.progress["maximum"] = total_files
        self.progress["value"] = 0

        target_ext = self.target_format.get().lower()

        for item in self.tree.get_children():
            self.tree.delete(item)

        for index, file_path in enumerate(files_to_process, start=1):
            with Image.open(file_path) as image:
                new_w = int(image.width * scale_factor)
                new_h = int(image.height * scale_factor)

                new_img = image.resize((new_w, new_h), Image.Resampling.LANCZOS)

                save_format = "JPEG" if target_ext in ["jpg", "jpeg"] else target_ext.upper()
                if save_format == "JPEG" and new_img.mode in ("RGBA", "P", "LA"):
                    new_img = new_img.convert("RGB")

                save_path = Path(output_dir) / Path(file_path).with_suffix(f".{target_ext}").name
                new_img.save(
                    save_path,
                    save_format,
                    quality=self.quality.get()
                )

                new_size = os.path.getsize(save_path)

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        os.path.basename(file_path),
                        f"{image.width}x{image.height} -> {new_w}x{new_h}",
                        f"{image.format} -> {target_ext.upper()}",
                        self.format_size(os.path.getsize(file_path)),
                        self.format_size(new_size)
                    )
                )
                self.tree.see(self.tree.get_children()[-1])

                self.progress["value"] = index
                self.update_idletasks()

        self.start_button.config(state="normal")
        self.browse_button.config(state="normal")

        self.open_output_folder_button.pack(side="left", padx=10)

    @staticmethod
    def open_output_folder(path):
        if os.path.isfile(path):
            base_dir = os.path.dirname(path)
        else:
            base_dir = path

        output_dir = os.path.join(base_dir, "output")
        webbrowser.open(f"file://{output_dir}")

    @staticmethod
    def format_size(bytes_size):
        kb = bytes_size / 1024
        if kb < 1024:
            return f"{kb:.1f} KB"
        return f"{kb / 1024:.2f} MB"


if __name__ == "__main__":
    app = App()
    app.mainloop()
