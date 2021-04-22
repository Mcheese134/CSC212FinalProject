from flask import Flask, render_template, request;
from flask_bootstrap import Bootstrap;


import sys;
sys.path.append("../backend")


from pynput.mouse import Button, Listener

from screenrecorder import screenRecord;


xs = []
ys = []

listener = 0

def activate():
  global listener
  listener = Listener(on_click=on_click)

  listener.start()





def on_click(x, y, button, pressed):

    global xs
    global ys
    global listener
    if button == Button.left and pressed:
        if len(xs) < 1 and len(ys) < 1:
            xs.append(x)
            ys.append(y)
            print(xs, ys)
        else:
            xs.append(x)
            ys.append(y)
            print(xs, ys)
            listener.stop()
            
  



app = Flask(__name__)
@app.route("/")
def index():
    return render_template('intro.html')


 #background process happening without any refreshing
@app.route('/background_process_test')
def background_process_test():
  
  activate()

  return "Hello world"



@app.route("/home")
def intro():
 #Query String
  coord = request.cookies.get('coord')


  #Backend Data
  attributes = screenRecord(coord)
  slideNum = attributes[0]
  uncommonWords = attributes[1]
  desc = attributes[2]



  print("UncommonWords: " + str(len(uncommonWords)))
  return render_template('index.html', slideNum = slideNum, uncommonWords = uncommonWords, desc = desc)  
if __name__ == "__main__":
  app.run()