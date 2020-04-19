import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt


kivy.require('1.9.1')

class StartUpWindow(Screen):
  def continueBtn(self):
    sm.current = "main"

class MainWindow(Screen):
  def __init__(self, **kw):
    super().__init__(**kw)

    ##Creating the Pie Chart using KIVY and MatPlotlib   
    labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
    sizes = [15, 30, 45, 10]
    explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
    plt.figure(1)
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    self.ids["pieSpace"].add_widget(FigureCanvasKivyAgg(plt.gcf()))
    plt.close()

    ##Creating a bar graph using KIVY and MatPlotLib 
    x = [2,4,6,8,10]
    y = [6,7,8,2,4]

    x2 = [1,3,5,7,9]
    y2 = [7,8,2,4,2]

    plt.bar(x,y, label='Bars1', color='blue')
    plt.bar(x2,y2, label='Bars2', color='c')

    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Interesting Graph\nCheck It out')
    plt.legend()

    self.ids["bar"].add_widget(FigureCanvasKivyAgg(plt.gcf()))
    plt.close()

    data=[Label(text="VS Code: 03:32:37", color= (0,0,0,1)  ),Label(text="VS Code: 03:32:37", color= (0,0,0,1)  ),
      Label(text="VS Code: 03:32:37", color= (0,0,0,1)  ),Label(text="VS Code: 03:32:37", color= (0,0,0,1)  )]
    data2=[Label(text="VS Code: 03:32:37", size_hint_y=.05,color= (0,0,0,1)  ),Label(text="VS Code: 03:32:37", size_hint_y=.05,color= (0,0,0,1)  ),
      Label(text="VS Code: 03:32:37", size_hint_y=.05,color= (0,0,0,1)  ),Label(text="VS Code: 03:32:37", size_hint_y=.05,color= (0,0,0,1)  )]
    for label in data:
      self.ids["prod"].add_widget(label)
    for label in data2: 
      self.ids["unPro"].add_widget(label)
  pass 

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