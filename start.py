#!/usr/bin/env python3
import os
import sys
import foxtrot_api.server as server
from cryptography.fernet import Fernet
from foxtrot_api.database import Database
from foxtrot_api.common import config_path, \
                            cache_dir, \
                            secrets_dir, \
                            db_path, \
                            admin_token_path, \
                            secret_path
from ftf_utilities import load_json, dump_json, log, Mode

# Prime the cache directory
if(not os.path.exists(cache_dir)):
    log(Mode.WARN, 'Cache dir not found: ' + str(cache_dir)
        + '\n\tCreating now...')
    os.makedirs(cache_dir, exist_ok=True)

# Prime the secrets directory
if(not os.path.exists(secrets_dir)):
    log(Mode.WARN, 'Secrets dir not found: ' + str(secrets_dir)
        + '\n\tCreating now...')
    os.makedirs(secrets_dir, exist_ok=True)

# Load the config file
try:
    config = load_json(config_path)
except FileNotFoundError:
    log(Mode.WARN, "Config file does not exist!\n\tGenerating: " + config_path)
    dump_json(config_path, load_json("res/default_config.json"))
    config = load_json(config_path)

# Load the secret file
try:
    secret = load_json(secret_path)['secret']
except FileNotFoundError:
    log(Mode.WARN, "Secret file does not exist!\n\tGenerating: " + secret_path)
    dump_json(secret_path, {'secret': str(Fernet.generate_key())[2:-1]})
    secret = load_json(secret_path)['secret']

# Create the user-agent database + table
if(not os.path.exists(db_path)):
    create_table = True
else:
    create_table = False

user_agents_db = Database(db_path, secret)
if(create_table):
    log(Mode.WARN, "User Agents DB does not exist!\n\tGenerating: " + db_path)
    if(user_agents_db.create_table()):
        log(Mode.INFO, "Success!\n\tCreating admin account...")
        admin_token = user_agents_db.add_user_agent('admin', privilege=3)
        dump_json(admin_token_path, {'token': admin_token})
        log(Mode.WARN, "New admin account generated! Token saved to: "
            + admin_token_path)
    else:
        log(Mode.ERROR, "failure: could not create the user agents table!")
        sys.exit(-1)

# Start the server
try:
    server.start(config['host'], config['port'], user_agents_db)
except KeyboardInterrupt:
    print("Closing server on port " + str(config['port']) + "...")
    server.stop()
    print("Goodbye!")
