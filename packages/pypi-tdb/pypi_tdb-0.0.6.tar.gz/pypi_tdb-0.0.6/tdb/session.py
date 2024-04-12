import os
import platform
import time
import tempfile
import tdb.cli
import tdb.tags
import tdb.config
import tdb.records
import signal
import sys

_last_text = ""
_start_text = ""

def start(name, content="", ext=".txt", update_cb=None):
    global _last_text
    global _start_text
    _start_text = content
    name += "-"
    temp_file = tempfile.NamedTemporaryFile(mode="w+", prefix=name, suffix=ext, delete=False)
    temp_file.write(content)
    temp_file.close()
    proc = tdb.cli.popen(f"{tdb.config.get('editor')} {temp_file.name}")
    modtime = os.path.getmtime(temp_file.name)
    try:
        while proc.poll() == None:
            if modtime < os.path.getmtime(temp_file.name):
                time.sleep(0.1)
                modtime = os.path.getmtime(temp_file.name)
                text = open(temp_file.name).read()
                text = tdb.tags.parse_cmds("update", text)
                _last_text = text
                if update_cb:
                    text = update_cb(content, text)
                    content = text
                open(temp_file.name, "w").write(text)
                modtime = os.path.getmtime(temp_file.name)
            time.sleep(0.1)
    except KeyboardInterrupt as e:
        print("\nInterrupt detected!")
    
    text = ""
    if os.path.exists(temp_file.name):
        text = open(temp_file.name).read()
        os.remove(temp_file.name)
    return text

 
def signal_term_handler(signal, frame):
    if _last_text != _start_text:
        tdb.records.add_record(_last_text)
    sys.exit(1)
 
signal.signal(signal.SIGTERM, signal_term_handler)
if platform.system() == "Linux": signal.signal(signal.SIGQUIT, signal_term_handler)