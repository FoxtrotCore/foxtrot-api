#!/usr/bin/env python3

from ftfutils import log, Mode
from episode import Episode
from line import Time

BASE_URL = "../transcripts/"

def is_dialogue(line): return (line.split(':')[0] == "Dialogue")

def main():
    for i in range(0, 9):
        path = BASE_URL + "eng_00" + str(i) + "_Code_Lyoko.ass"
        log(Mode.INFO, "Loading file: " + path)
        ep1 = Episode(path)
        res = ep1.search(name="yumi")
        log(Mode.INFO, "Results: ")
        for line in res:
            print("\t" + str(line))

if __name__ == "__main__": main()
