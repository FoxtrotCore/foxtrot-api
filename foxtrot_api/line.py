class Time:
    def __init__(self, hrs = 0, min = 0, sec = 0, mil = 0):
        self.hrs = hrs
        self.min = min
        self.sec = sec
        self.mil = mil

    def __lt__(self, src):
        if(self.hrs < src.hrs): return True
        elif(self.min < src.min): return True
        elif(self.sec < src.sec): return True
        elif(self.mil < src.mil): return True
        return False

    def __le__(self, src):
        if(self.hrs < src.hrs): return True
        elif(self.hrs == src.hrs):
            if(self.min < src.min): return True
            elif(self.min == src.min):
                if(self.sec < src.sec): return True
                elif(self.sec == src.sec):
                    if(self.mil < src.mil): return True
                    elif(self.mil == src.mil): return True
        return False

    def __gt__(self, src):
        if(self.hrs > src.hrs): return True
        elif(self.min > src.min): return True
        elif(self.sec > src.sec): return True
        elif(self.mil > src.mil): return True
        return False

    def __ge__(self, src):
        if(self.hrs > src.hrs): return True
        elif(self.hrs == src.hrs):
            if(self.min > src.min): return True
            elif(self.min == src.min):
                if(self.sec > src.sec): return True
                elif(self.sec == src.sec):
                    if(self.mil > src.mil): return True
                    elif(self.mil == src.mil): return True
        return False

    def __eq__(self, src): return (self.hrs == src.hrs \
                                    and self.min == src.min \
                                    and self.sec == src.sec \
                                    and self.mil == src.mil)
    def __str__(self): return str(str(self.hrs).rjust(2, '0') \
                        + ":" + str(self.min).rjust(2, '0') \
                        + ":" + str(self.sec).rjust(2, '0') \
                        + "." + str(self.mil).rjust(3, '0'))

class Line:
    def __init__(self,
                 ep_num = -1,
                 start = Time(),
                 end = Time(),
                 name = "N/A",
                 text = "N/A"):
         # if(start > end): raise "Cannot start a line after it ends!"
         self.ep_num = ep_num
         self.start = start
         self.end = end
         self.name = name
         self.text = text

    def is_character(self, name): return (self.name.upper() == name.upper())
    def has_text(self, text): return (self.text.lower().find(text.lower()) != -1)

    def to_dict(self):
        res = {}
        res['episode_number'] = self.ep_num
        res['timestamp'] = {}
        res['timestamp']['in'] = str(self.start)
        res['timestamp']['out'] = str(self.end)
        res['name'] = self.name
        res['dialogue'] = self.text
        return res

    def __str__(self): return str("[" + str(self.start) + " - " + str(self.end) + "] <" + self.name + ">: " + self.text)
