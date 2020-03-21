from top_extraction import top_extraction 

class report_data:

    def __init__(self):
        self.top = top_extraction()
        self.raw = self.top.get_top()
        self.AAL = [] ## Acceptable Application List ( i.e. all )
        self._get_AAL()


    def _get_AAL(self):
        f = open("aal.txt","r")
        text = f.read()
        self.AAL = text.split("\n")

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


def main():
    report = report_data()
    print(report.report_important())

if __name__ == "__main__":
    main()