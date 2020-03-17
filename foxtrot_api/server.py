from http.server import HTTPServer, BaseHTTPRequestHandler
from http.client import HTTPSConnection
from urllib.parse import urlparse, parse_qs
from ftf_utilities import load_json, log, Mode
from .episode import Episode
from .line import Line
import os, os.path, ssl, sys, json, time

httpd = None
config = None
episode_table = {}
home_dir = os.path.expanduser("~/.ftf-api/")
cache_dir = home_dir + "cache/"

class Handler(BaseHTTPRequestHandler):
    def __init__(self, request, client_addr, server):
        super().__init__(request, client_addr, server)

    def get_script(self, filename):
        local_script_path = cache_dir + filename
        remote_script_path = config['script_uri'] + filename

        if(os.path.exists(local_script_path)):
            file = open(local_script_path, 'r+')
            data = file.read()
            file.close()
            return data
        else:
            con = HTTPSConnection(config['script_url'])
            con.request('GET', remote_script_path, {}, {})
            res = con.getresponse()

            if(res.status == 200):
                data = res.read().decode()
                file = open(local_script_path, "w+")
                file.write(data)
                file.close()
                return data
            else: return None

    def cache_episodes(self, episodes):
        global episode_table
        if(len(episodes) > 0): stuff = episodes
        else: stuff = list(range(96))

        for e in stuff:
            if(episode_table.get(e) is None):
                name = "eng_" + str(e).rjust(3, '0') + '_Code_Lyoko.ass'
                log(Mode.WARN, "Episode #" + str(e) + " is not loaded in the episode table!")
                ep_data = self.get_script(name)
                if(ep_data is None): log(Mode.ERROR, "Failed to retrieve remote file: " + name)
                else: episode_table[e] = Episode(e, ep_data)

    def sanitize_request(self, req):
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

    def do_JSON_HEAD(self):
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def do_HTML_HEAD(self):
        self.send_header('Content-Type', 'text/html')
        self.end_headers()

    def do_GET(self):
        global episode_table
        url_path = urlparse(self.path)
        query = parse_qs(url_path.query)

        if(url_path.path == '/'):
            file = open('index.html')
            res = file.read()
            file.close()

            self.send_response(200)
            self.do_HTML_HEAD()
            self.wfile.write(bytearray(res, 'UTF-8'))
        elif(url_path.path == "/search"):
            start = time.time()
            characters, episodes, dialogues = self.sanitize_request(query)
            self.cache_episodes(episodes)

            qres = []
            res = {}
            res['search_results'] = []
            res['missing_eps'] = []

            for e in episodes:
                if(episode_table.get(e) is None):
                    log(Mode.ERROR, "Episode #" + str(e) + " is missing, skipping!")
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
                    else:
                        log(Mode.ERROR, "Not enough search terms!")
                        break

            for line in qres: res['search_results'].append(line.to_dict())
            elapsed = round(1 * (time.time() - start), 4)
            res['search_time'] = elapsed

            log(Mode.INFO, "Search finished in " + str(elapsed) + "s: " + str(res))

            self.send_response(200)
            self.do_JSON_HEAD()
            self.wfile.write(bytearray(json.dumps(res), 'UTF-8'))
        elif(url_path.path == "/available"):
            start = time.time()
            self.cache_episodes(list(range(96)))
            res = {}
            res['available_episodes'] = sorted(list(episode_table.keys()))
            elapsed = round(1 * (time.time() - start), 4)
            res['search_time'] = elapsed

            log(Mode.INFO, "Episode table populated in " + str(elapsed) + "s: " + str(res))

            self.send_response(200)
            self.do_JSON_HEAD()
            self.wfile.write(bytearray(json.dumps(res), 'UTF-8'))
        else:
            code = 404
            self.send_response(code)
            self.do_HTML_HEAD()
            self.wfile.write(bytearray(BaseHTTPRequestHandler.responses[code][1], 'utf-8'))

def prime_file(filename):
    if(filename is None): error("Must specify an SSL Cert/Key Pair!")
    elif(not os.path.exists(filename)): error("Could not find SSL Cert/Key Pair!")

def prime_cache():
    if(not os.path.exists(cache_dir)):
        log(Mode.WARN, "Cache dir not found: " + str(cache_dir) + "\n\tCreating now...")
        os.makedirs(cache_dir, exist_ok=True)

def error(msg):
    log(Mode.ERROR, "fatal: " + msg)
    sys.exit(-1)

def start(host, port, key, cert):
    global httpd, config

    # Prime the prerequisite files on disk
    prime_file(key)
    prime_file(cert)
    prime_cache()
    config = load_json(home_dir + "config.json")

    httpd = HTTPServer((host, port), Handler) # Create the HTTP server
    httpd.socket = ssl.wrap_socket(httpd.socket, # Wrap with SSL
                    keyfile=key,
                    certfile=cert,
                    server_side=True)
    log(Mode.INFO, "Server bound to port " + str(port) + "\n\tKey File: " + str(key) + "\n\tCert File: " + str(cert))
    httpd.serve_forever(); # Start the server

def stop():
    global httpd
    httpd.shutdown()
