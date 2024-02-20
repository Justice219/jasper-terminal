import os
import subprocess
import sys

# add root directory to this current folder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


# run desktop_app.py in a subprocess from the desktop directory
# this is necessary to ensure that the desktop app runs in the correct directory
subprocess.Popen([sys.executable, 'desktop_app.py'], cwd='desktop')

# run web_app.py in a subprocess from the web directory
# this is necessary to ensure that the web app runs in the correct directory
subprocess.Popen([sys.executable, 'web_app.py'], cwd='web')