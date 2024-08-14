import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

class ChangeHandler(FileSystemEventHandler):
    """Restart the script when there's a change."""
    
    def __init__(self, script_name):
        self.script_name = script_name
        self.process = None
        self.start_script()
        
    def on_modified(self, event):
        """Restart the script if the file is modified."""
        if event.src_path == self.script_name or event.src_path in other_scripts:
            self.restart_script()
            
    def start_script(self):
        """Start the script."""
        self.process = subprocess.Popen(['python', self.script_name], stdout=subprocess.PIPE)
        print(f'Started {self.script_name}')
        
    def restart_script(self):
        """Restart the script."""
        if self.process:
            self.process.kill()
            self.process.wait()
        self.start_script()
        print(f'Restarted {self.script_name}')

curr_dir = os.getcwd()
script_name = f'{curr_dir}/bot.py'
other_scripts = [f'{curr_dir}/openRouter.py', f'{curr_dir}/weather.py']

event_handler = ChangeHandler(script_name)
observer = Observer()
observer.schedule(event_handler, path='.', recursive=False)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()