#!/usr/bin/env python3
import os, foxtrot_api.server as ftfapi, sys
from foxtrot_api.common import config_path, cache_dir
from ftf_utilities import load_json, dump_json, log, Mode

# Prime the cache directory
if(not os.path.exists(cache_dir)):
    log(Mode.WARN, 'Cache dir not found: ' + str(cache_dir) + '\n\tCreating now...')
    os.makedirs(cache_dir, exist_ok=True)

# Load the config file
try: config = load_json(config_path)
except FileNotFoundError as e:
    log(Mode.WARN, "Config file does not exist!\n\tGenerating: " + config_path)
    dump_json(config_path, load_json("foxtrot_api/default_config.json"))
    config = load_json(config_path)

# Start the server
try: ftfapi.start(config['host'], config['port'])
except KeyboardInterrupt as e:
    print("Closing server on port " + str(config['port']) + "...")
    ftfapi.stop()
    print("Goodbye!")
