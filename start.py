#!/usr/bin/env python3
import os, foxtrot_api.server as ftfapi, sys
from foxtrot_api.common import config_path
from ftf_utilities import load_json, dump_json, log, Mode

# Get the cert file paths
KEY = os.getenv('FTF_API_KEY')
CERT = os.getenv('FTF_API_CERT')

# Load the config file
try: config = load_json(config_path)
except FileNotFoundError as e:
    log(Mode.WARN, "Config file does not exist!\n\tGenerating: " + config_path)
    dump_json(config_path, load_json("foxtrot_api/default_config.json"))
    config = load_json(config_path)

# Start the server
try: ftfapi.start(config['host'], config['port'], KEY, CERT)
except KeyboardInterrupt as e:
    print("Closing server on port " + str(config['port']) + "...")
    ftfapi.stop()
    print("Goodbye!")
