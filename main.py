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

## KIVY GARDEN ( This is included at run time )
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

#OTHER LIBRARIES
import matplotlib.pyplot as plt
import time 
import requests
import json

#LOCAL LIBRARIES
from report_data import report_data

kivy.require('1.9.1')

## Landing Page Class Construction
class StartUpWindow(Screen):

  def continueBtn(self):
    ## Switches Screen Manager to the Main Dash board 
    sm.current = "main"
  
  def howToButton(self):
    ## Opens a Pop up window with instructions on how to get started 
    pop = PopupWindow()
    self.popup = Popup(title='How to Get Started', content= pop , size_hint = (.8,.8), 
      separator_color = [1, .57, .3, .5],auto_dismiss=True)
      
    self.popup.open()
  
## Pop Up window class for displaying how to instructions
class PopupWindow(BoxLayout):
  pass

## Main Dash Board class Contruction 
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

  ##Updates percentages and stores the information as a class variable 
  def updatePercent(self):
    pro = 0 
    total = 0 

    ## For each element in Productive Data
    for element in self.data[3]:
      pro += self.data[0][element]
      total += self.data[0][element]

    ## For each element in Unproductive Data 
    for element in self.data[4]:
      total += self.data[0][element]

    self.percentProd = round((pro/total)*100)
    self.ids["percentProductive"].text = "Productivty: "+str(self.percentProd)
      
  ## Reports a list of productive and unproductive apps used
  def updateProdAppStats(self):
    ## Clear Widgets 
    self.ids["prod"].clear_widgets()
    self.ids["unPro"].clear_widgets()

    ## Default List Values 
    if len(self.data[3]) == 0: ## Productive 
      self.data[3].append("Better Get To Work")
    
    if len(self.data[4]) == 0: ## Unproductive 
      self.data[4].append("Way to Grind!")

    ## Create and Place new widgets 
    for task in self.data[3]: ## Productive 
      l = Label(text=task, color= (0,0,0,1))
      self.ids["prod"].add_widget(l)

    for task in self.data[4]: ## Unproductive 
      l = Label(text=task, color= (0,0,0,1))
      self.ids["unPro"].add_widget(l)
    
  ## Connects to report data engine to update informaiton 
  def background_collect(self):
    print("Collecting Data")
    self.data = self.report.update()
    self.onRefresh()

  ## What is done every minute to the GUI 
  @mainthread
  def onRefresh(self):

    ## Update GUI elements 
    self.ids["timeCollected"].text = "Time Collected: "+ str(self.data[2])+ " Minutes "
    self.ids["lastTime"].text = "Last Collected: "+self.data[1]
    self.updatePercent()

    self.createBarGraph(self.data[0])
    self.createPieChart(self.data[0])

    self.updateProdAppStats()
  
  ## Starts the scheduler 
  def start_counting(self):

    ## Schedule to collect every 60 Seconds 
    Clock.schedule_interval(lambda dt: self.background_collect(),60)

  ## Changes GUI asspects upon start 
  def startButton(self):

    ## Disable Button Visually 
    self.ids["start"].background_color = [0,0,0,.7]
    self.ids["start"].text=""

    ## Start counting 
    self.start_counting()

  
  def createPieChart(self, timeDic):
    ## Creating the Pie Chart using KIVY and MatPlotlib  
    ## Documentation: matplotlib.org/gallery/pie_and_polar_charts/pie_and_donut_labels.html%23sphx-glr-gallery-pie-and-polar-charts-pie-and-donut-labels-py

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
    ##Documentation: matplotlib.org/

    ## Clear the GUI of the old Graph 
    self.ids["bar"].clear_widgets()

    # Find values 
    x = []
    y = []

    ## Calculates the number of minutes of total productive time 
    x.append("Productive")
    xSum = 0 
    for key in self.data[3]:
      xSum += timeDic[key]
    y.append( xSum)

    ## Calculates the number of minutes of total unproductive time 
    x.append("Unproductive")
    xSum = 0 
    for key in self.data[4]:
      xSum += timeDic[key]
    y.append( xSum)

    ## Generates Plots 
    pltCol = plt.bar(x,y, label='Bars1')
    pltCol[0].set_color('g')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Productivity Comparision')

    self.ids["bar"].add_widget(FigureCanvasKivyAgg(plt.gcf()))
    plt.close()

  ## Shares Producrtivity Stats to the speficied slack wekhook 
  def shareButton(self):
    ## Webhook from Slack api ( currently disabled )
    url = 'https://hooks.slack.com/services/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'

    ##The Messages you want to send 
    slack_data = "I've been " + str(self.percentProd)+"% Productive today! Can you beat that? Track your productivity too with STRV"

    ##Pack it using Json 
    data = json.dumps(slack_data)

    ## API POST 
    response = requests.post(
        url, json={"text": data},
        headers={'Content-Type': 'application/json'}
    )
 

## Sets up class for the Screen Manager 
class WindowManager(ScreenManager):
  pass 

##Import Kv Lang File 
Builder.load_file('ProdApp.kv')
sm = WindowManager()

## Initalize Screen Classes for the window manager
screens = [StartUpWindow(name="start"), MainWindow(name="main")]
for screen in screens:
  sm.add_widget(screen)

## Sets the inital screen 
sm.current = "start"


## Application MAIN
class STRVApp(App):
  def build(self):
    ## Builds a screen manager 
    return sm


# run the App  
if __name__ == "__main__": 
    STRVApp().run() 