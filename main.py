import os
import subprocess
import sys

desktop_path = os.path.join(os.getcwd(), 'desktop')
web_path = os.path.join(os.getcwd(), 'web')

# run web app in a subprocess
subprocess.Popen([sys.executable, os.path.join(web_path, 'web_app.py')])
# run desktop app in a subprocess
subprocess.Popen([sys.executable, os.path.join(desktop_path, 'desktop_app.py')])
