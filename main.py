#KIVY IMPORTS 
import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock, mainthread

## KIVY GARDEN
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

#OTHER LIBRARIES
import matplotlib.pyplot as plt
import time 
import requests
import json

#LOCAL LIBRARIES
from report_data import report_data

kivy.require('1.9.1')

class StartUpWindow(Screen):
  def continueBtn(self):
    sm.current = "main"
  
  def howToButton(self):
    pop = PopupWindow()
    self.popup = Popup(title='How to Get Started', content= pop , size_hint = (.8,.8), 
      separator_color = [1, .57, .3, .5],auto_dismiss=True)
      
    self.popup.open()
  

class PopupWindow(BoxLayout):
  pass

class MainWindow(Screen):
  def menuButton(self):
    sm.current ="start"
    
  def __init__(self, **kw):
    super().__init__(**kw)

    ##Creating the Pie Chart using KIVY and MatPlotlib   
    self.report = report_data()
    self.data = self.report.update()
    timeDic = self.data[0]

    ##TEXT
    self.ids["date"].text = self.report.getDate()
    self.ids["timeCollected"].text = "Time Collected: 0 Minutes"
    self.ids["lastTime"].text = "Last Collected: Never"
    self.updatePercent()
    
    ##CHARTS
    self.createBarGraph(timeDic)
    self.createPieChart(timeDic)

    ##DATA
    self.updateProdAppStats()

  def updatePercent(self):
    pro = 0 
    total = 0 

    for element in self.data[3]:
      pro += self.data[0][element]
      total += self.data[0][element]

    for element in self.data[4]:
      total += self.data[0][element]

    self.percentProd = round((pro/total)*100)
    self.ids["percentProductive"].text = "Productivty: "+str(self.percentProd)
      
  def updateProdAppStats(self):
    ## Clear Widgets 
    self.ids["prod"].clear_widgets()
    self.ids["unPro"].clear_widgets()

    ##Default Values 
    if len(self.data[3]) == 0:
      self.data[3].append("Better Get To Work")
    
    if len(self.data[4]) == 0:
      self.data[4].append("Way to Grind!")

    ##Creat and Place new widgets 
    for task in self.data[3]:
      l = Label(text=task, color= (0,0,0,1))
      self.ids["prod"].add_widget(l)

    for task in self.data[4]:
      l = Label(text=task, color= (0,0,0,1))
      self.ids["unPro"].add_widget(l)
    

  def background_collect(self):
    print("Collecting Data")
    self.data = self.report.update()
    self.onRefresh()

  @mainthread
  def onRefresh(self):
    self.ids["timeCollected"].text = "Time Collected: "+ str(self.data[2])+ " Minutes "
    self.ids["lastTime"].text = "Last Collected: "+self.data[1]
    self.updatePercent()

    self.createBarGraph(self.data[0])
    self.createPieChart(self.data[0])

    self.updateProdAppStats()
  
  def start_counting(self):

    ## Schedule to collect every 60 Seconds 
    Clock.schedule_interval(lambda dt: self.background_collect(),60)

  def startButton(self):

    ## Disable Button Visually 
    self.ids["start"].background_color = [0,0,0,.7]
    self.ids["start"].text=""

    ## Start counting 
    self.start_counting()

  def createPieChart(self, timeDic):
    ## Creating the Pie Chart using KIVY and MatPlotlib  

    ## Clear Space
    self.ids["pieSpace"].clear_widgets()

    ## Create tracking Variables 
    largest_value = 0
    largest_place = 0
    current_place = 0 
    labels = []
    sizes = [] 

    ## Collect the Apps information
    for key, value in timeDic.items():
      labels.append(key)
      sizes.append(value)

      ## Collect Data for the exploding piece of the chart
      if value > largest_value:
        largest_place = current_place
        largest_value = value 
         
      current_place = current_place +1 

    ## Create the explode variable
    explode = ()
    for x in range(current_place):
      if x == largest_place:
        explode = explode + (.1,)
      else: 
        explode = explode + (0,)

    plt.figure(1)

    ## Plot the graph in matlibplots
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    ## Add Plot to the GUI 
    self.ids["pieSpace"].add_widget(FigureCanvasKivyAgg(plt.gcf()))
    
    ## Clear Ploter for next use 
    plt.close()
 
  def createBarGraph(self, timeDic):
    ##Creating a bar graph using KIVY and MatPlotLib 

    ## Clear the GUI of the old Graph 
    self.ids["bar"].clear_widgets()

    # Find values 
    x = []
    y = []

    x.append("Productive")
    xSum = 0 
    for key in self.data[3]:
      xSum += timeDic[key]
    y.append( xSum)

    x.append("Unproductive")
    xSum = 0 
    for key in self.data[4]:
      xSum += timeDic[key]
    y.append( xSum)

    pltCol = plt.bar(x,y, label='Bars1')
    pltCol[0].set_color('g')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Productivity Comparision')

    self.ids["bar"].add_widget(FigureCanvasKivyAgg(plt.gcf()))
    plt.close()

  def shareButton(self):
    url = 'https://hooks.slack.com/services/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'
    slack_data = "I've been " + str(self.percentProd)+"% Productive today! Can you beat that? Track your productivity too with STRV"
    data = json.dumps(slack_data)
    response = requests.post(
        url, json={"text": data},
        headers={'Content-Type': 'application/json'}
    )
 

class WindowManager(ScreenManager):
  pass 

Builder.load_file('ProdApp.kv')
sm = WindowManager()

screens = [StartUpWindow(name="start"), MainWindow(name="main")]
for screen in screens:
  sm.add_widget(screen)

sm.current = "start"


class STRVApp(App):
  def build(self):
    return sm


# run the App  
if __name__ == "__main__": 
    STRVApp().run() 