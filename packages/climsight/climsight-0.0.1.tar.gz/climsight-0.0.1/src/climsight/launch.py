import subprocess

def launch_streamlit_app():
    subprocess.run(["streamlit", "run", "climsight.py"])