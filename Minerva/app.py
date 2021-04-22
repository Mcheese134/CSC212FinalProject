from flask import Flask, render_template, request, jsonify;
from flask_bootstrap import Bootstrap;
import json



import sys;
sys.path.append("../backend")


from pynput.mouse import Button, Listener

from screenrecorder import screenRecord;


xs = []
ys = []

coord = []

listener = 0

def activate():
  global listener
  global coord
  global xs
  listener = Listener(on_click=on_click)
  listener.start()
  listener.join()








def on_click(x, y, button, pressed):
    global xs
    global ys

   
    if button == Button.left and pressed:
        if len(xs) < 2 and len(ys) < 2:

            xs.append(x)
            ys.append(y)
            print(xs, ys)
        else:
          listener.stop()

          print("XS: " + str(xs))
          return False

            
  



app = Flask(__name__)
@app.route("/")
def index():
    return render_template('intro.html')


 #background process happening without any refreshing
@app.route('/background_process_test', methods=['GET', 'POST'])
def background_process_test():

  global xs
  

  if request.method == 'POST':

    xs = []
    ys = []

    activate()

    print("XSA: " + str(xs))



    return json.dumps(coord)
  



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