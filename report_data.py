from top_extraction import top_extraction 

import time 
import calendar
from datetime import datetime, date

class report_data:

    def __init__(self):
        self.top = top_extraction()
        self.raw = self.top.get_top()
        
        #Chart Data
        self.timeDic = {}

        #Time Data
        self.LastTime = ''
        self.RunningTime = 0

        #Date Data 
        today = date.today()

        self.date = calendar.day_name[today.weekday()]+", "+ today.strftime("%B %d, %Y")
        self.AAL = [] ## Acceptable Application List ( i.e. all )
        self._get_AAL()
        self._get_prodApp()

    ## Obtain list of applications to track from aal.txt 
    def _get_AAL(self):
        f = open("aal.txt","r")
        text = f.read()
        self.AAL = text.split("\n")
        f.close()

    ## Obtain list of productive application from prod_app.txt
    def _get_prodApp(self):
        f = open("prod_app.txt","r")
        text = f.read()
        self.prodApp = text.split("\n")
        f.close()

    ## Returns the current date 
    def getDate(self):
        return self.date

    ## Returns a tuple of data that has changed 
    def update(self):
        #Retrive Top 
        self.raw = self.top.update()

        #Record Time
        now = datetime.now()
        self.LastTime = now.strftime("%H:%M:%S")
        self.RunningTime = self.RunningTime +1 

        #Parce Data 
        self.report_important()
        self.update_timeDic()
        self.reportProd()

        return [self.timeDic, self.LastTime, self.RunningTime, self.pro, self.unpro ]

    ## Gets a report of the all data and then the apps that are to be tracked 
    def get_report( self ):
        return ( self.important_list, self.raw)

    ## Returns a list of application that are currently running 
    def _report_running( self):
        self.running_list = []

        for key, value in self.raw.items():
            percent, running, time = value 
            if running == "running":
                self.running_list.append(key)
        
        return self.running_list

    ## Return the application running on the CPU for the longest time 
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

    ## Returns a list of current application that we are suppose to be tracking. 
    def report_important( self ):
        self.important_list = []
        for key, value in self.raw.items():
            for app in self.AAL:
                if app.find(key.rstrip()) >= 0:
                    self.important_list.append(key)
        
        return self.important_list

    ## Returns a dictions of all application since start and the time that they've been running 
    def update_timeDic(self):
        if len(self.important_list) == 0:
            self.important_list.append("idle")
        for key in self.important_list:
            if key in self.timeDic:
                self.timeDic[key]= self.timeDic[key]+ 1
            else:
                self.timeDic[key]= 1
        self.important_list = []

    ## Returns a list of application that are deemed productive by the user 
    def reportProd(self):
        self.pro = []
        self.unpro = []

        for key in self.timeDic:
            found = False
            for app in self.prodApp:
                if app.find(key.rstrip()) >= 0: 
                    self.pro.append(key)
                    found = True
            if not found:
                self.unpro.append(key)

        return( self.pro, self.unpro)

def main():
    report = report_data()
    print(report.report_important())

if __name__ == "__main__":
    main()