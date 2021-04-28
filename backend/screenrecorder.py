# To install
# pip install pyautogui
# pip install pytesseract
# pip install NLTK
# pip install opencv-python
# Install Tesseract https://github.com/UB-Mannheim/tesseract/wiki
# Set your OCR directory in line 31 (currently it is set up for my personal directory)


# TODO 
# Drop down box to get domain of presentation


#Import all the dependencies
import pyautogui
import cv2
import numpy as np
import time
import pytesseract
import json
import nltk
import subprocess

from PIL import Image
from nltk.stem.snowball import SnowballStemmer
from wiktionaryparser import WiktionaryParser




#This function will take the coordinates, screenshot, parse that screenshot for technical jargon, and output definitions/slideNum
def screenRecord(screenCoord, domain):

    #OCR Directory - For Windows : Set your directory path
    #pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Nasty\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

    #Can be used to get screen size 
    screen = pyautogui.size()
    

    #Data is split between in order: x coordinates array and y coordinate array. They are in order
    screenCoord =  json.loads(screenCoord)

    #This will detect a retina display - Needs to be doubled because it has double pixels
    if subprocess.call("system_profiler SPDisplaysDataType | grep -i 'retina'", shell= True) == 0: 
            for i in range(len(screenCoord)):
                for j in range(len(screenCoord[i])):
                   screenCoord[i][j] = screenCoord[i][j] * 2.0

    #Split coordinates into these attributes
    top = screenCoord[1][0]
    bottom = screenCoord[1][1]
    left = screenCoord[0][0]
    right = screenCoord[0][1]
   
   #Establish Width and Height
    width = abs(right - left)
    height = abs(top - bottom)


    #Initialize Wikitionary Parser
    sno = nltk.stem.SnowballStemmer('english')
    parser = WiktionaryParser()

    # Front-End Variable - This will get slideNum, definitions, and words
    frontend = []

    #Retrieve all the common words
    with open("wordList.txt") as f:
        content = f.readlines()
    content = [x.strip() for x in content]

    # Variable that will hold the last parsed text
    lastText = ""

    #Current slide number when image changes
    slideNum = 0

    # Have this domain be set by the user   
    domain = domain

    #TODO: Make this automated for now. Need to refresh to update and only checks once
    count = 0
    while count != 1:

    
        #Take screenshot 
        img = pyautogui.screenshot(region=(left,top,width, height) )# (left, top, width, height)
        img.save("screenshot.png")
        img.save("static/screenshot.png")

        
        #Parse the screenshot that was established
        image = cv2.imread("screenshot.png")
        gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        threshold_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        im = Image.open("screenshot.png")
        newText = pytesseract.image_to_string(im).strip().lower().split()

        #Only check for technical words if the text are different
        if (newText != lastText):

            # New Text will be compared when new screenshot is made
            lastText = newText

            #set the values for the data to be sent to frontend
            slideNum = slideNum + 1
            uncommonWordsOnSlide = [x for x in lastText if x not in content]
            desc = []

            #This will filter out words that was not successfully parsed
            cannotParse = []



            #Run through all known technical jargon
            for i in uncommonWordsOnSlide:

                for c in "!@#%&*()[]{}/?<>,":
                    i = i.replace(c, "")
                
                specialDef = False # Set this to true if program finds a domain-specific definition

                #Parse the word to see if it has any definitions
                word = parser.fetch(i)

                #Add to cannot parse if no data was collected
                if(len(word) <= 0):
                    cannotParse.append(i)
                    continue

                
                #Loop through parsed data for definitions
                for k, v in word[0].items():

                    #Check if current item is definitions
                    if (k == 'definitions'):

                        #If no definition found, then default to this
                        if(len(v) == 0):
                            desc.append("Definition not found for: " + str(i))
                            break

                        #Get the text for definitions
                        listStuff = v[0].get('text')

                        #Run through all definitions and get special definitions based on selected domain
                        for i in listStuff:
                            if domain == "computing" and (("computing" in i) or ("computer science" in i)):
                                print(i) # Prints the definition with (computing)
                                specialDef = True
                                desc.append(i)
                                break
                            elif domain == "mathematics" and "mathematics" in i:
                                print(i) # Prints the definition with (mathematics)
                                specialDef = True
                                desc.append(i)
                                break
                            elif domain == "physics" and "physics" in i:
                                print(i) # Prints the definition with (physics)
                                specialDef = True
                                desc.append(i)
                                break
                            elif domain == "biology" and "biology" in i:
                                print(i) # Prints the definition with (biology)
                                specialDef = True
                                desc.append(i)
                                break
                            elif domain == "chemistry" and "chemistry" in i:
                                print(i) # Prints the definition with (chemistry)
                                specialDef = True
                                desc.append(i)
                                break
                        #Display only the first defintion (index 0 is "not comparable" usually in this case)
                        if specialDef == False: # If program does not find a definition specific to the domain
                           # print(listStuff) # This prints all definitions, can be changed to only first definition
                            desc.append(listStuff[1])

            #Remove parsed words
            for dup in cannotParse:
                uncommonWordsOnSlide.remove(dup)

            #Append necessary data for frontend
            frontend.append(slideNum)
            frontend.append(uncommonWordsOnSlide)
            frontend.append(desc)
                        
        time.sleep(2)
        count+=1

    return frontend


