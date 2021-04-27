#Retrieve dependencies
from flask import Flask, render_template, request, jsonify;
from flask_bootstrap import Bootstrap;


import json
import sys;

#Add a system path to call backend functions
sys.path.append("../backend")

#Needs to be called after the system path - Python script located there
from screenrecorder import screenRecord;
from pynput.mouse import Button, Listener


#Get X and Y Coordinates
x_coords = []
y_coords = []

#Final list to append all (x,y) coordinates
all_coords = []

#Establish an event listener for clicks
listener = 0

#This function will activate listener for mouse clicks
def activate():
  global listener
  listener = Listener(on_click=on_click)
  listener.start()
  listener.join()



#This function will retrieve x and y coordinates up to two mouse clicks
def on_click(x, y, button, pressed):
    global x_coords
    global y_coords
    global all_coords

   
    if button == Button.left and pressed:
        if len(x_coords) < 1 and len(y_coords) < 1:
            x_coords.append(x)
            y_coords.append(y)
        else:
          x_coords.append(x)
          y_coords.append(y)
          coord.append(x_coords)
          coord.append(y_coords)
          listener.stop()
          return False

            
  
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# No caching at all for API endpoints.
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

#Renders the landing page for the application
@app.route("/")
def index():
    return render_template('intro.html')


#background process happening without any refreshing
@app.route('/background_process_test', methods=['GET', 'POST'])
def background_process_test():
  global coord
  global xs
  global ys

  #Reset coordinates each time a post request is made and retrieve new coords as a json string
  if request.method == 'POST':
    coord = []
    xs = []
    ys = []
    activate()
    return json.dumps(coord)
  

#Renders the main applicaion page
@app.route("/home")
def intro():
 #Query String
  coord = request.cookies.get('coord')
  domain = request.cookies.get('domain')

  #Variable that holds all data on slide number, uncommon words found, and the matching description
  attributes = screenRecord(coord, domain)

  #Split into individual varibales
  slideNum = attributes[0]
  uncommonWords = attributes[1]
  desc = attributes[2]

  return render_template('index.html', slideNum = slideNum, uncommonWords = uncommonWords, desc = desc)  
if __name__ == "__main__":
  app.run()