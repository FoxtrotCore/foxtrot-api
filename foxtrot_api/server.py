from http.server import HTTPServer, BaseHTTPRequestHandler
from http.client import HTTPSConnection
from urllib.parse import urlparse, parse_qs
from ftf_utilities import load_json, log, Mode
from .episode import Episode
from .line import Line
import os, os.path, ssl, sys, json, time

httpd = None
home_dir = os.path.expanduser("~/.ftf-api/")
cache_dir = home_dir + "cache/"
config = load_json(home_dir + "config.json")
episode_table = {}

class Handler(BaseHTTPRequestHandler):
    def __init__(self, request, client_addr, server):
        super().__init__(request, client_addr, server)

    def get_script(self, filename):
        local_script_path = cache_dir + filename
        remote_script_path = config['script_uri'] + filename

        if(os.path.exists(local_script_path)): return local_script_path
        else:
            log(Mode.DEBUG, "Script does not exist: " + local_script_path)
            con = HTTPSConnection(config['script_url'])
            con.request('GET', remote_script_path, {}, {})
            res = con.getresponse()

            if(res.status == 200):
                data = res.read().decode()
                file = open(local_script_path, "w+")
                file.write(data)
                file.close()
                return local_script_path
            else: return None

    def cache_episodes(self, episodes):
        global episode_table
        if(len(episodes) > 0): stuff = episodes
        else: stuff = list(range(96))

        for e in stuff:
            if(episode_table.get(e) is None):
                name = "eng_" + str(e).rjust(3, '0') + '_Code_Lyoko.ass'
                log(Mode.WARN, "File not loaded: " + str(e))
                ep_path = self.get_script(name)
                if(ep_path is None): log(Mode.ERROR, "Failed to retrieve remote file: " + name)
                else: episode_table[e] = Episode(ep_path)

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

    def do_HEAD(self):
        self.send_header('Content-type', 'application/json')
        self.send_header('Save-Data', 'on')
        self.send_header('Allow', 'GET')
        self.end_headers()

    def do_GET(self):
        self.do_HEAD()

        global episode_table
        url_path = urlparse(self.path)
        query = parse_qs(url_path.query)

        log(Mode.DEBUG, "A new request was received: " + str(url_path.path) + " | QArgs: " + str(query))

        if(url_path.path == "/search"):
            start = time.time()
            code = 200
            characters, episodes, dialogues = self.sanitize_request(query)
            log(Mode.DEBUG, "Characters: " + str(characters) + "\n\tEpisodes: " + str(episodes) + "\n\tDialogues: " + str(dialogues))
            self.cache_episodes(episodes)

            log(Mode.DEBUG, "Master Table: " + str(episode_table))

            qres = []
            res = []

            for e in episodes:
                log(Mode.INFO, "Searching ep" + str(e))
                if(len(characters) > 0): character = characters[0]
                else: character = ''

                if(len(dialogues) > 0): dialogue = dialogues[0]
                else: dialogue = ''

                if(character is None and dialogue is None):
                    log(Mode.INFO, "Not enough search terms!")
                    break
                else: qres += episode_table[e].search(name=character, text=dialogue)

            for line in qres: res.append(str(line))
            elapsed = round(time.time() - start, 4)

            log(Mode.INFO, "Search results in " + str(elapsed) + "s: " + str(res))

            start = time.time()
            self.wfile.write(bytearray(json.dumps({'code': 200, 'message': json.dumps(res), 'received': 'ok'}), 'utf-8'))
            self.end_headers()
            elapsed = round(time.time() - start, 4)
            log(Mode.INFO, "Served in " + str(elapsed) + "s!")
        else:
            code = 400
            self.send_response(code)
            self.end_headers()
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
    global httpd

    # Prime the prerequisite files on disk
    prime_file(key)
    prime_file(cert)
    prime_cache()

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
