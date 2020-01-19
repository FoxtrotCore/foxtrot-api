#!/usr/bin/env python3

from ftfutils import log, Mode
from episode import Episode
from line import Time

BASE_URL = "../transcripts/"

def is_dialogue(line): return (line.split(':')[0] == "Dialogue")

def main():
    for i in range(0, 9):
        path = BASE_URL + "eng_00" + str(i) + "_Code_Lyoko.ass"
        ep1 = Episode(path)
        res = ep1.search(name="", text="xana")

        if(len(res) > 0):
            log(Mode.INFO, "Episode " + str(i) + ": ")
            for line in res:
                print("\t" + str(line))

if __name__ == "__main__": main()
