from http.server import HTTPServer, BaseHTTPRequestHandler
from http.client import HTTPSConnection
from urllib.parse import urlparse, parse_qs
from ftf_utilities import load_json, log, Mode
from .episode import Episode
from .line import Line
from .common import *
import os.path, sys, json, time

httpd = None
config = None
episode_table = {}

class Handler(BaseHTTPRequestHandler):
    def __init__(self, request, client_addr, server):
        '''A forward constructor for BaseHTTPRequestHandler'''
        super().__init__(request, client_addr, server)

    def ep_to_fn(self, episode): return 'eng_' + str(episode).rjust(3, '0') + '_Code_Lyoko.ass'

    def dump_script(self, filename):
        '''
        Reads a local file and dumps the contents.
        filename: The path to the local file.
        Returns: File contents in UTF-8 Encoding.
        '''
        file = open(filename, 'r+')
        data = file.read()
        file.close()
        return data

    def get_script(self, filename):
        local_script_path = cache_dir + filename
        remote_script_path = config['script_uri'] + filename

        if(os.path.exists(local_script_path)): return self.dump_script(local_script_path)
        else:
            con = HTTPSConnection(config['script_url'])
            con.request('GET', remote_script_path, {}, {})
            res = con.getresponse()

            if(res.status == 200):
                data = res.read().decode()
                file = open(local_script_path, 'w+')
                file.write(data)
                file.close()
                return data
            else: return None

    def cache_episodes(self, episodes):
        '''
        Attemts to cache episodes locally.

        episodes: The list of episodes to cache.
        Returns: A boolean of whether or not all requested episodes got cached.
        '''
        global episode_table
        did_cache = True
        if(len(episodes) > 0): stuff = episodes
        else: stuff = list(range(96))

        for e in stuff:
            if(episode_table.get(e) is None):
                name = self.ep_to_fn(e)
                log(Mode.WARN, 'Episode #' + str(e) + ' is not loaded in the episode table!')
                ep_data = self.get_script(name)
                if(ep_data is None):
                    log(Mode.ERROR, 'Failed to retrieve remote file: ' + name)
                    did_cache = False
                else: episode_table[e] = Episode(e, ep_data)
        return did_cache

    def sanitize_request(self, req):
        '''
        Sanitizes list of attributes according to their names.

        req: A semi-processed http request object
        Returns: [ list of characters, list of episodes, list of dialogues ]
        '''
        characters = []
        episodes = []
        dialogues = []
        raw_char = req.get('character')
        raw_eps = req.get('episode')
        raw_dial = req.get('dialogue')

        if(type(raw_char) is list):
            for c in raw_char: characters.append(c.strip())

        if(type(raw_eps) is list):
            for e in raw_eps: episodes.append(int(e))
        else: episodes = list(range(96))

        if(type(raw_dial) is list):
            for d in raw_dial: dialogues.append(d.strip())

        return characters, episodes, dialogues

    def error_req(self, code, message=None):
        '''
        Sends a JSON error message to the client.
        This assumes no header has been constructed and that the response body is currently empty.

        code: The HTTP response code.
        message: An optional message to append to the response.
        Returns: The HTTP status code.
        '''
        log(Mode.WARN, 'SENT TO CLIENT [' + str(code) + ']: ' + str(message))
        self.send_response(code)
        self.do_JSON_HEAD()
        self.wfile.write(bytearray(json.dumps({ 'status': code,
                                                'error': BaseHTTPRequestHandler.responses[code][1],
                                                'message': message}), 'utf-8'))
        return code

    def do_JSON_HEAD(self):
        '''Constructs a response body in JSON.'''
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_HTML_HEAD(self):
        '''Constructs a response body in HTML.'''
        self.send_header('Content-Type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self):
        '''Handles an HTTP GET request.'''
        start = time.time()
        url_path = urlparse(self.path)
        query = parse_qs(url_path.query)

        if(url_path.path == '/'): # Handle root path request
            file = open('index.html')
            res = file.read()
            file.close()

            self.send_response(200)
            self.do_HTML_HEAD()
            self.wfile.write(bytearray(res, 'UTF-8'))
        elif(url_path.path == '/search'): # Handle search request
            characters, episodes, dialogues = self.sanitize_request(query)
            self.cache_episodes(episodes)

            qres = []
            res = {}
            res['search_results'] = []
            res['missing_eps'] = []

            for e in episodes:
                if(episode_table.get(e) is None):
                    log(Mode.ERROR, 'Episode #' + str(e) + ' is missing, skipping!')
                    res['missing_eps'].append(e)
                    continue
                else:
                    if(len(characters) > 0 and len(dialogues) > 0):
                        for c in characters:
                            for d in dialogues: qres += episode_table[e].search(name=c, text=d)
                    elif(len(characters) > 0):
                        for c in characters: qres += episode_table[e].search(name=c)
                    elif(len(dialogues) > 0):
                        for d in dialogues: qres += episode_table[e].search(text=d)
                    else: return self.error_req(400, 'Not enough search terms provided!')

            for line in qres: res['search_results'].append(line.to_dict())
            elapsed = round(1 * (time.time() - start), 4)
            res['search_time'] = elapsed

            log(Mode.INFO, 'Search finished in ' + str(elapsed) + 's: ' + str(res))

            self.send_response(200)
            self.do_JSON_HEAD()
            self.wfile.write(bytearray(json.dumps(res), 'UTF-8'))
        elif(url_path.path == '/available'): # Handle availability request
            self.cache_episodes(list(range(96)))
            res = {}
            res['available_episodes'] = sorted(list(episode_table.keys()))
            elapsed = round(1 * (time.time() - start), 4)
            res['search_time'] = elapsed

            log(Mode.INFO, 'Episode table populated in ' + str(elapsed) + 's: ' + str(res))

            self.send_response(200)
            self.do_JSON_HEAD()
            self.wfile.write(bytearray(json.dumps(res), 'UTF-8'))
        elif(url_path.path == '/script'): # Handle raw script retrieval request
            characters, episodes, dialogues = self.sanitize_request(query)

            if(len(episodes) == 1):
                if(self.cache_episodes(episodes)):
                    script = self.dump_script(cache_dir + self.ep_to_fn(episodes[0]))
                    elapsed = round(1 * (time.time() - start), 4)

                    log(Mode.INFO, 'Raw transcript fetched in ' + str(elapsed) + 's')

                    self.send_response(200)
                    self.do_HTML_HEAD()
                    self.wfile.write(bytearray(script, 'utf-8'))
                else: self.error_req(506, 'Failed to retrieve requested script!')
            else: return self.error_req(400, 'Too few or too many episodes specified!')
        else: self.error_req(404) # Handle undefined path

def error(msg):
    '''
    Prints an error message to stdout then exits with a status of -1
    '''
    log(Mode.ERROR, 'fatal: ' + msg)
    sys.exit(-1)

def start(host, port):
    global httpd, config

    try: config = load_json(config_path)
    except FileNotFoundError as e: error("Config file does not exist! Server cannot continue!")

    httpd = HTTPServer((host, port), Handler) # Create the HTTP server
    log(Mode.INFO, 'Server bound to port ' + str(port))
    httpd.serve_forever(); # Start the server

def stop():
    global httpd
    httpd.shutdown()
