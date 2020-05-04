from http.server import HTTPServer, BaseHTTPRequestHandler
from http.client import HTTPSConnection
from urllib.parse import urlparse, parse_qs
from ftf_utilities import load_json, log, Mode
from .episode import Episode
from .line import Line
from .common import *
import os.path, sys, json, time, shutil

httpd = None
config = None
episode_table = {}

class Handler(BaseHTTPRequestHandler):
    def __init__(self, request, client_addr, server):
        '''A forward constructor for BaseHTTPRequestHandler'''
        super().__init__(request, client_addr, server)

    def ep_to_fn(self, episode): return 'eng_' + str(episode).rjust(3, '0') + '_Code_Lyoko.ass'

    def load_enc(self, path):
        with open(path, 'rb') as file: return file.read()

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
        else: stuff = list(range(96 - (96 - config['ep_cap'])))

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
        else: episodes = list(range(96 - (96 - config['ep_cap'])))

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

    def common_header(self):
        '''Common attributes among headers'''
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Security-Policy', 'default-src: self')
        self.end_headers()

    def do_JSON_HEAD(self):
        '''Constructs a response body in JSON.'''
        self.send_header('Content-Type', 'application/json')
        self.common_header()

    def do_HTML_HEAD(self):
        '''Constructs a response body in HTML.'''
        self.send_header('Content-Type', 'text/html')
        self.common_header()

    def do_DOC_HEAD(self, name):
        '''Constructs a response body in plain text.'''
        self.send_header('Content-Type', 'application/x-www-form-urlencoded')
        self.send_header('Content-Disposition', 'attatchment; filename="' + name + '"')
        self.common_header()

    def do_ICO_HEAD(self):
        self.send_header('Content-Type', 'image/x-icon')
        self.common_header()

    def do_REDIRECT(self, path):
        '''Constructs a response for permanent redirect.'''
        self.send_response(301)
        self.send_header('Location', path)
        self.common_header()

    def do_GET(self):
        '''Handles an HTTP GET request.'''
        global episode_table
        start = time.time()
        url_path = urlparse(self.path)
        query = parse_qs(url_path.query)

        if(url_path.path == '/'): # Handle root path request
            file = open('res/index.html')
            res = file.read()
            file.close()

            self.send_response(200)
            self.do_HTML_HEAD()
            self.wfile.write(bytearray(res, 'UTF-8'))
        elif(url_path.path == '/favicon.ico'):
            self.send_response(200)
            self.do_ICO_HEAD()
            self.wfile.write(self.load_enc('res/favicon.ico'))
        elif(url_path.path == '/search'): # Handle search request
            try:
                characters, episodes, dialogues = self.sanitize_request(query)
                self.cache_episodes(episodes)
            except ValueError:
                self.error_req(400, 'Bad parameter value types.')
                return

            qres = []
            res = {}
            res['search_results'] = []
            res['missing_episodes'] = []
            ep_cap = config.get('ep_cap')
            if(ep_cap is not None and ep_cap < 96): res['missing_episodes'] = list(range(ep_cap, 96))

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
            self.cache_episodes([])
            res = {}
            res['available_episodes'] = sorted(list(episode_table.keys()))
            res['missing_episodes'] = []
            ep_cap = config.get('ep_cap')
            if(ep_cap is not None and ep_cap < 96): res['missing_episodes'] = list(range(ep_cap, 96))
            elapsed = round(1 * (time.time() - start), 4)
            res['search_time'] = elapsed

            log(Mode.INFO, 'Episode table populated in ' + str(elapsed) + 's: ' + str(res))

            self.send_response(200)
            self.do_JSON_HEAD()
            self.wfile.write(bytearray(json.dumps(res), 'UTF-8'))
        elif(url_path.path == '/script'): # Handle raw script retrieval request
            try: characters, episodes, dialogues = self.sanitize_request(query)
            except ValueError:
                self.error_req(400, 'Bad parameter value types.')
                return

            if(len(episodes) == 1):
                if(self.cache_episodes(episodes)):
                    script = self.dump_script(cache_dir + self.ep_to_fn(episodes[0]))
                    elapsed = round(1 * (time.time() - start), 4)

                    log(Mode.INFO, 'Raw transcript fetched in ' + str(elapsed) + 's')

                    self.send_response(200)
                    self.do_DOC_HEAD('eng_' + str(episodes[0]).rjust(3, '0') + '_Code_Lyoko.ass')
                    self.wfile.write(bytearray(script, 'utf-8'))
                else: self.error_req(506, 'Failed to retrieve requested script!')
            else: return self.error_req(400, 'Too few or too many episodes specified!')
        else: self.error_req(404) # Handle undefined path

    def do_POST(self):
        '''Handles an HTTP GET request.'''
        global episode_table
        start = time.time()
        url_path = urlparse(self.path)
        query = parse_qs(url_path.query)
        api_tokens = load_json(tokens_path)
        client_token = self.headers.get('Authorization')

        if(client_token in api_tokens):
            if(url_path.path == '/clearcache'): # Handle cache clear requests
                # Wipe the existing cache in memory and on disk
                episode_table = {}
                shutil.rmtree(cache_dir, ignore_errors = True)
                os.makedirs(cache_dir)
                log(Mode.INFO, "Clearing cache dir: " + cache_dir)

                # Recache and redirect to the '/available' endpoint
                self.cache_episodes([])
                self.do_REDIRECT('/available')
            else: self.error_req(404) # Handle undefined path
        else: self.error_req(403)

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
