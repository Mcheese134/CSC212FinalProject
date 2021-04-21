from flask import Flask, render_template, request;
from flask_bootstrap import Bootstrap;


import sys;
sys.path.append("../backend")

from screenrecorder import screenRecord;


app = Flask(__name__)
@app.route("/")
def index():

    return render_template('intro.html')


 

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