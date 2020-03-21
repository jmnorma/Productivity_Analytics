import os
import subprocess
import re

class top_extraction: 
   

    def __init__(self): 

        ## Storage Text file 
        self.file_name = "output.txt"
        self.active_file = open(self.file_name, "w+")

        ##Initalizes the outfile file 
        subprocess.run(["top", "-l", "3","-n",'10',"-ncols","13"], stdout= self.active_file)
        self.active_file.close()

    def top_print(self ):

        self._extract()
        print(self.table)

    def get_top(self ):

        self._extract()
        return self.table
    
    def update(self):
        self.active_file = open(self.file_name, "w+")

        ##Initalizes the outfile file 
        subprocess.run(["top", "-l", "3","-n",'10',"-ncols","13"], stdout= self.active_file)
        self.active_file.close()

        self._extract()
        return self.table

    def _extract (self):  

        ##Open the output file
        f = open("output.txt", "r")
        lines = f.read()
        f.close()
        
        ##Extract the application lines from the top output 
        lines = lines.split("\n")
        lines = lines[56:] 

        self.table = {}

        for line in lines:
            if line == "":
                pass 

            else:
                strings =  line.split()

                temp = 1 
                name = ""

                ## Extracts the name of the task running until it reaches the CPU %
                while not bool(re.match("^\d+?\.\d+?$", strings[temp])): 
                    name +=strings[temp]+" "
                    temp+=1
                
                self.table[ name] = (strings[temp], strings[temp+10], strings[temp+1])