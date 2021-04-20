from flask import Flask, render_template;
from flask_bootstrap import Bootstrap;

import sys;
sys.path.append("../backend")

from screenrecorder import screenRecord;


app = Flask(__name__)
@app.route("/")
def index():
  attributes = screenRecord()
  slideNum = attributes[0]
  uncommonWords = attributes[1]
  print("UncommonWords: " + str(len(uncommonWords)))
  return render_template('index.html', slideNum = slideNum, uncommonWords = uncommonWords)

@app.route("/intro")
def intro():
  return render_template('intro.html')
  
if __name__ == "__main__":
  app.run()