
class WinGenerator(object):
    def __init__(self,dictionary):
        self.dic=dictionary
    def Window(self):
   
        maxHR=220-int(self.dic["age"])
        if self.dic["goal"]=="A":
            min_window=maxHR*0.5
            max_window=maxHR*0.6
        elif self.dic["goal"]=="B":
            min_window=maxHR*0.6
            max_window=maxHR*0.7
        elif self.dic["goal"]=="C":
            min_window=maxHR*0.7
            max_window=maxHR*0.8
        elif self.dic["goal"]=="D":
            min_window=maxHR*0.8
            max_window=maxHR*0.9
        elif self.dic["goal"]=="E":
            min_window=maxHR*0.9
            max_window=maxHR
            
        return round(min_window),round(max_window)
      
