#!/usr/bin/env python3

import simple_http_server.server as server, os, sys, requests, shutil
from pathlib import Path
from ftfutils import log, Mode
from ftfutils.utilities import *
from episode import Episode
from line import Time
from simple_http_server import request_map, HttpError, StaticFile, PathValue, Parameter

CONFIG = load_json('./config/config.json')
log(Mode.INFO, "Loaded config: " + str(CONFIG))

# Bind the correct host: port
if(CONFIG['prod']):
    HOST = CONFIG['host']
    PORT = CONFIG['port']
else:
    HOST = CONFIG['dev_host']
    PORT = CONFIG['dev_port']

LOCAL_BASE="./cache/"
REMOTE_BASE="https://raw.githubusercontent.com/FoxtrotCore/misc/master/subtitles/ass/"

def prepare_script(file_path):
    local = Path(LOCAL_BASE + file_path)
    remote = REMOTE_BASE + file_path

    if(not local.exists()):
        log(Mode.DEBUG, "File not cached: " + str(local) + "\n\tMaking request to repo: " + str(remote))
        raw_script = requests.get(remote).text
        file = open(str(local), 'w+')
        file.write(raw_script)
        file.close()
    else: log(Mode.INFO, "File cached: " + str(local))

    return str(local)


# If all is well, this returns None, else it returns a dictionary
def validate_arg(arg):
    # Check int type
    try: int(arg)
    except ValueError: return {"code": 406, "message": "episode number must be alphanumeric"}

    # Check ep_num range
    if(int(arg) < 0 or int(arg) > 95): return {"code": 406, "message": "episode range must be between 0-95"}

    return None

@request_map("/", method="GET")
def root_handle(): return StaticFile('./index.html', 'utf-8'), {"code": 200, "message": "success!"}

@request_map("/search/{ep_num}", method='GET')
def handle_search_request(ep_num=PathValue(),
                          text=Parameter('text', default=''),
                          name=Parameter('name', default='')):
    res = validate_arg(ep_num) # Input validation
    if(res != None): return res

    if(text == '' and name == ''): # Deal with an empty request
        log(Mode.WARN, 'Skipping an empty serach request!')
        return {"code": 406, "message": "cannot serve empty search request!"}
    else:
        path = prepare_script("eng_" + Time.pad(int(ep_num), precision=3) + "_Code_Lyoko.ass")
        ep_data = Episode(path)
        sres = ep_data.search(name=name, text=text)
        res = {"code": 200, "message": { "path": path, "text": text, "character": name, "search_results": []}}
        for line in sres: res["message"]["search_results"].append(str(line))
        return res

@request_map("/script/{ep_num}", method="GET")
def handle_transcript_request(ep_num=PathValue()):
    res = validate_arg(ep_num) # Input validation
    if(res != None): return res

    # Padding
    if(int(ep_num) < 10): ep_num = "00" + str(ep_num)
    elif(int(ep_num) < 100): ep_num = "0" + str(ep_num)

    # Construct file name
    file_path = prepare_script("eng_" + Time.pad(int(ep_num), precision=3) + "_Code_Lyoko.ass")

    # Return result
    return StaticFile(file_path, "UTF-8")

def handle_close():
    log(Mode.WARN, "Clearing the cache and closing the server!")
    if(Path(LOCAL_BASE).exists()): shutil.rmtree(LOCAL_BASE)
    sys.exit(0)

def main():
    if(not Path(LOCAL_BASE).exists()): os.makedirs(LOCAL_BASE)

    try: server.start(host=HOST, port=PORT)
    except KeyboardInterrupt: handle_close()
    except HttpError: handle_http_error()

if __name__ == "__main__": main()
