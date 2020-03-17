from .line import *

class Episode:
    def is_dialogue(line): return (line.split(':')[0] == "Dialogue")

    def parse_time(time):
        pieces = time.split(':')
        hrs = int(pieces[0])
        min = int(pieces[1])
        sec = int(pieces[2].split('.')[0])
        mil = int(pieces[2].split('.')[1])
        return Time(hrs, min, sec, mil)

    def parse_line(line):
        if(Episode.is_dialogue(line)):
            pieces = line.split(',')
            start = Episode.parse_time(pieces[1])
            end = Episode.parse_time(pieces[2])
            name = pieces[4]
            text = ', '.join(pieces[9:]).rstrip()
            return Line(start, end, name, text)
        else: return None

    def search(self, start = '', end = '', name = '', text = ''):
        results = []
        for line in self.lines:
            if((start == '' or (line.start >= start)) and
               (end == '' or (line.end <= end)) and
               (name == '' or line.is_character(name)) and
               (text == '' or line.has_text(text))):
                results.append(line)
                continue
        return results

    def __init__(self, file_path = None):
        if(file_path == None): self.lines = []
        else:
            file = open(file_path)
            raw_lines = file.readlines()
            file.close()

            self.lines = []
            for line in raw_lines:
                line = Episode.parse_line(line)
                if(line != None): self.lines.append(line)
