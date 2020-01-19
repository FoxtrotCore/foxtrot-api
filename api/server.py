#!/usr/bin/env python3

import simple_http_server.server as server, sys
from ftfutils import log, Mode
from episode import Episode
from line import Time
from simple_http_server import request_map, HttpError, StaticFile, PathValue, Parameter

HOST = "localhost"
PORT = 8080

BASE_URL="../transcripts/"

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
                          episode=Parameter('episode', default=''),
                          name=Parameter('name', default='')):
    res = validate_arg(ep_num) # Input validation
    if(res != None): return res

    if(text == '' and episode == '' and name == ''): # Deal with an empty request
        log(Mode.WARN, 'Skipping an empty serach request!')
        return {"code": 406, "message": "cannot serve empty search request!"}
    else:
        path = BASE_URL + "eng_" + Time.pad(int(ep_num), precision=3) + "_Code_Lyoko.ass"
        ep_data = Episode(path)
        sres = ep_data.search(name="aelita")
        res = {"code": 200, "message": { "path": path, "text": text, "episode": episode, "character": name, "search_results": []}}
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
    file_path = BASE_URL + "eng_" + ep_num + "_Code_Lyoko.ass"

    # Return result
    return StaticFile(file_path, "UTF-8")

def handle_close():
    log(Mode.WARN, "Closing the server!")
    # TODO: Save logs + other things
    sys.exit(0)

def main():
    try: server.start(host=HOST, port=PORT)
    except KeyboardInterrupt: handle_close()
    except HttpError: handle_http_error()

if __name__ == "__main__": main()
