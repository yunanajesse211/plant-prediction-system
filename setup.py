import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
build_exe_options = {"packages": ["os","pyttsx3.drivers","pyttsx3.drivers.dummy","pyttsx3.drivers.espeak","pyttsx3.drivers.nsss","pyttsx3.drivers.sapi5","pyttsx3.drivers._espeak"],"include_files":[ "dataset","plant.ico","dataset/power_plant.csv"]}

# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="CCPP Prediction System",
    version="1.0",
    description="Hourly output Energy prediction",
    options={"build_exe": build_exe_options},
    author="Mr. Joshua",
    executables=[Executable("power_plant_pred.py", base=base,icon='plant.ico')],
)