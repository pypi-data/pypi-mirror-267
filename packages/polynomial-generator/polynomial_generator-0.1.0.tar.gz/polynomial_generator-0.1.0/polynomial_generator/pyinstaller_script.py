import PyInstaller.__main__
from pathlib import Path

path_to_main = str(Path(__file__).parent.absolute() / "generate_polynomial_app.py")

def install():
    PyInstaller.__main__.run([
        path_to_main,
        '--onefile',
        '--windowed',
        # other pyinstaller options... 
    ])

if __name__ == "__main__":
    install()
