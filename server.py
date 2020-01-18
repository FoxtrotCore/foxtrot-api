#!/usr/bin/env python3

import simple_http_server.server as server, sys
from ftfutils import log, Mode
from simple_http_server import request_map, HttpError, StaticFile, PathValue, Parameter

HOST = "localhost"
PORT = 8080

@request_map("/", method="GET")
def root_handle(): return StaticFile('./index.html', 'utf-8'), {"code": 200, "message": "success!"}

@request_map("/search/{ep_num}", method='GET')
def handle_search_request(ep_num=PathValue(),
                          text=Parameter('text', default=''),
                          episode=Parameter('episode', default=''),
                          character=Parameter('character', default='')):
    if(text == '' and episode == '' and character == ''): # Deal with an empty request
        log(Mode.WARN, 'Skipping an epmty serach request!')
        return {"code": 406, "message": "cannot serve empty search request!"}
    else:
        # TODO: Search transcripts
        return {"code": 200, "message": { "text": text, "episode": episode, "character": character }}

def handle_close():
    log(Mode.WARN, "Closing the server!")
    # TODO: Save logs + other things
    sys.exit(0)

def main():
    try: server.start(host=HOST, port=PORT)
    except KeyboardInterrupt: handle_close()
    except HttpError: handle_http_error()

if __name__ == "__main__": main()
