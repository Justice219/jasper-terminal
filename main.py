import os
import subprocess
import sys

# run desktop_app.py in a subprocess from the desktop directory
# this is necessary to ensure that the desktop app runs in the correct directory
subprocess.run([sys.executable, 'desktop_app.py'], cwd=os.path.join(os.path.dirname(__file__), 'desktop'))