#!/usr/bin/env python3
import os, foxtrot_api.server as ftfapi, sys
KEY = os.getenv('FTF_API_KEY')
CERT = os.getenv('FTF_API_CERT')
HOST = ""
PORT = 443
try: ftfapi.start(HOST, PORT, KEY, CERT)
except KeyboardInterrupt as e:
    print("Closing server on port " + str(PORT) + "...")
    ftfapi.stop()
    print("Goodbye!")
