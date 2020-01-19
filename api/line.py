class Time:
    def __init__(self, hrs = 0, min = 0, sec = 0, mil = 0):
        self.hrs = hrs
        self.min = min
        self.sec = sec
        self.mil = mil

    def pad(arg, precision=2):
        for i in range(1, precision):
            if(arg < 10**i):
                pad = ""
                for j in range(0, (precision - i)): pad += "0"
                return str(pad + str(arg))
        return str(arg)

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

    def __eq__(self, src): return (self.hrs == src.hrs and self.min == src.min and self.sec == src.sec and self.mil == src.mil)
    def __str__(self): return str(Time.pad(self.hrs) + ":" + Time.pad(self.min) + ":" + Time.pad(self.sec) + "." + Time.pad(self.mil, precision=3))

class Line:
    def __init__(self,
                 start = Time(),
                 end = Time(),
                 name = "N/A",
                 text = "N/A"):
         # if(start > end): raise "Cannot start a line after it ends!"
         self.start = start
         self.end = end
         self.name = name
         self.text = text

    def is_character(self, name): return (self.name.upper() == name.upper())
    def has_text(self, text): return (self.text.upper().find(text.upper()) != -1)

    def __str__(self): return str("[" + str(self.start) + " - " + str(self.end) + "] <" + self.name + ">: " + self.text)
    def __str__(self): return str("[" + str(self.start) + " - " + str(self.end) + "] <" + self.name + ">: " + self.text)
