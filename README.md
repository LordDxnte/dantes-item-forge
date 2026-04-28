# 🗡️ Dante's Item Forge

A lightweight, local desktop application that leverages Groq's high-speed AI API to find the optimal weapons, armor, and items for any game. 

Built entirely with standard Python libraries and PyWebView for a zero-bloat, native desktop experience.

## ✨ Features
* **Lightning Fast:** Uses Groq's LPU inference engine (`llama3-70b`) to instantly analyze gaming knowledge bases and tier lists.
* **Native Desktop UI:** Uses `pywebview` to create a sleek, responsive dark-mode application window—no browser tabs required.
* **Secure Architecture:** The backend proxy runs on Python's native `http.server` bound strictly to `localhost`, keeping your API keys completely safe.

## 🚀 How to Run

1. Clone the repository:
   ```bash
   git clone [https://github.com/yourusername/dantes-item-forge.git](https://github.com/yourusername/dantes-item-forge.git)
   cd dantes-item-forge
## 🚀 How to Make it an Executable on Windows.

1. Install Python on the Windows PC.

2. pip install pywebview PyQt6 PyInstaller.

3. Run the same command: pyinstaller --onefile --windowed item_finder.py.

4.It will produce an item_finder.exe in the dist/ folder.

## 🚀 How to Make it an Executable on Linux.

1. Open Terminal:
   ```bash
   pip install pyinstaller
   pyinstaller --onefile --windowed item_finder.py
   
****YOU ONLY NEED TO PUT YOUR API ONCE, IT WILL SAVE IT IN A CONFIG AFTER THAT.****
