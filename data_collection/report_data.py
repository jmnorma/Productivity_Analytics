from top_extraction import top_extraction 

import time 
from datetime import datetime, date

class report_data:

    def __init__(self):
        self.top = top_extraction()
        self.raw = self.top.get_top()
        
        #Chart Data
        self.timeDic = {}

        #Time Data
        self.LastTime 
        self.RunningTime = 0

        #Date Data 
        today = date.today()

        self.date = today.strftime("%B %d, %Y")
        self.AAL = [] ## Acceptable Application List ( i.e. all )
        self._get_AAL()


    def _get_AAL(self):
        f = open("aal.txt","r")
        text = f.read()
        self.AAL = text.split("\n")

    def getDate(self):
        return self.date

    def update(self):
        #Retrive Top 
        self.top.update()

        #Record Time
        now = datetime.now()
        self.LastTime = now.strftime("%H:%M:%S")
        self.RunningTime = self.RunningTime +1 

        #Parce Data 
        self.report_important()
        self.update_timeDic

        return [self.timeDic, self.LastTime, self.RunningTime ]

    def get_report( self ):
        return ( self.important_list, self.raw)

    def _report_running( self):
        self.running_list = []

        for key, value in self.raw.items():
            percent, running, time = value 
            if running == "running":
                self.running_list.append(key)
        
        return self.running_list

    def report_highest( self ):
        highest_percent = 0.0 
        highest_key = ""
        for key, value in self.raw.items():
            percent, running, time = value 
            if float(percent) > highest_percent:
                highest_percent = float(percent)
                highest_key = key 
        
        percent, running, time = self.raw[highest_key]
        print( highest_key+" , ("+ percent +", "+running+", "+time+")")

    def report_important( self ):
        self.important_list = []

        for key, value in self.raw.items():
            for app in self.AAL:
                if app.find(key) >= 0:
                    self.important_list.append(key)
        
        return self.important_list

    def update_timeDic(self):
        for key in self.important_list:
            if key in self.timeDic:
                print("Adding ONE")
                self.timeDic[key]= self.timeDic[key]+ 1
            else:
                print("new ADDITION")
                self.timeDic[key]= 1

def main():
    report = report_data()
    print(report.report_important())

if __name__ == "__main__":
    main()