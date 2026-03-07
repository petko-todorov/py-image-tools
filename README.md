# 🖼️ Image Tools

**Image Tools** is a lightweight and intuitive Python desktop application designed for fast image processing. It allows users to resize, convert formats, and optimize quality for single images or entire folders (Batch Processing) through a clean Graphical User Interface (GUI).

---

## ✨ Key Features

* **Dual Operation Modes:** Process a single file or perform batch processing on an entire folder.
* **Supported Formats:** Input and output support for `JPG`, `JPEG`, `PNG`, `WEBP`, `BMP`, `TIFF`.
* **Smart Resizing:** Scaling options (25%, 33.3%, 50%, 100%, 200%, 400%) using the high-quality `LANCZOS` resampling filter.
* **Quality Control:** Adjustable compression slider (0-100) to balance file size and visual clarity.
* **Live Preview:** A detailed `Treeview` table showing pending changes (Resolution, Format, Size) before you even hit start.
* **Multithreaded Execution:** The UI remains responsive and does not "freeze" during heavy processing tasks.
* **Automatic Organization:** Processed files are neatly saved in a generated `/output` subfolder.

---

## 🚀 Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/petko-todorov/py-image-tools.git
    cd py-image-tools
    ```

2.  **Install requirements:**
    The project relies on the `Pillow` library for image manipulation.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    python main.py
    ```

---

## 🛠️ How to Use

1.  **Select Mode:** Choose between "Single Image File" or "Entire Folder (Batch)" at the top.
2.  **Browse Path:** Click the **Browse** button to select your source.
3.  **Configure Settings:**
    * Select the **Target Format** from the dropdown.
    * Choose a **Resize** percentage.
    * Adjust the **Quality** slider (ideal for reducing `.webp` or `.jpg` file sizes).
4.  **Process:** Click **Start**. You can track the progress via the progress bar.
5.  **View Results:** Once finished, click **Open Output Folder** to access your optimized files immediately.

---

## 📝 Tech Stack

* **Python 3.x**
* **Tkinter:** For the graphical user interface.
* **Pillow (PIL):** For high-performance image processing.
* **Threading:** To handle background tasks without locking the UI.

---

## 🤝 Contributing

Contributions are welcome! If you have ideas for new features or find a bug, feel free to open an **Issue** or submit a **Pull Request**.

---

## 📄 License

This project is licensed under the MIT License.