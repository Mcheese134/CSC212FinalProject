# To install
# pip install pyautogui
# pip install pytesseract
# pip install NLTK
# pip install opencv-python
# Install Tesseract https://github.com/UB-Mannheim/tesseract/wiki
# Set your OCR directory in line 31 (currently it is set up for my personal directory)


# TODO 
# Drop down box to get domain of presentation
# Get user coordinates for screenshot


import pyautogui
import cv2
import numpy as np
import time
import pytesseract
import json
from PIL import Image
import nltk
from nltk.stem.snowball import SnowballStemmer
from wiktionaryparser import WiktionaryParser
import subprocess





def screenRecord(screenCoord):

    #OCR Directory
    #pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Nasty\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

    screen = pyautogui.size()
    print("SCREEN: " + str(screen))

    

    #Data is split between in order: x coordinates array and y coordinate array. They are in order
    screenCoord =  json.loads(screenCoord)

    if subprocess.call("system_profiler SPDisplaysDataType | grep -i 'retina'", shell= True) == 0: 
            for i in range(len(screenCoord)):
                for j in range(len(screenCoord[i])):
                   screenCoord[i][j] = screenCoord[i][j] * 2.0

    print("I have coord: " + str(screenCoord))
    top = screenCoord[1][0]
    bottom = screenCoord[1][1]
    left = screenCoord[0][0]
    right = screenCoord[0][1]
   
    width = abs(right - left)
    height = abs(top - bottom)


    


    sno = nltk.stem.SnowballStemmer('english')
    parser = WiktionaryParser()

    # Front-End Variable - This will get slideNum, definitions, and words
    frontend = []

    with open("wordList.txt") as f:
        content = f.readlines()
    content = [x.strip() for x in content]

    lastText = ""
    slideNum = 0
    domain = "computing" # Have this domain be set by the user



    

    count = 0
    while count != 1:

    
    
        img = pyautogui.screenshot(region=(left,top,width, height) )# (left, top, width, height)
        img.save("screenshot.png")
        img.save("static/screenshot.png")

        # (left, top, width, height)
        
        #This is for front-end

        image = cv2.imread("screenshot.png")
        gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        threshold_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        im = Image.open("screenshot.png")
        newText = pytesseract.image_to_string(im).strip().lower().split()

        if (newText != lastText):
            lastText = newText
            #print("Last deciphered text: ")
            #print(lastText)
            slideNum = slideNum + 1
            #print("Slide Number: ")  
           # print(slideNum)
            uncommonWordsOnSlide = [x for x in lastText if x not in content]
            print("Uncommon words: ")
            print(uncommonWordsOnSlide)

            frontend.append(slideNum)

            desc = []
            cannotParse = []


            for i in uncommonWordsOnSlide:
                
                specialDef = False # Set this to true if program finds a domain-specific definition

                word = parser.fetch(i)


                if(len(word) <= 0):
                    cannotParse.append(i)
                    continue

                
                for k, v in word[0].items():
                    if (k == 'definitions'):

                        if(len(v) == 0):
                            desc.append("Definition Not Found For: " + str(i))
                            break
                        else:
                            print("LENGTH OF V: " + str(len(v)))

                        listStuff = v[0].get('text')
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
                        if specialDef == False: # If program does not find a definition specific to the domain
                            print(listStuff) # This prints all definitions, can be changed to only first definition
                            desc.append(listStuff[1])

            for dup in cannotParse:
                uncommonWordsOnSlide.remove(dup)
            print("UNCOMMON: " + str(uncommonWordsOnSlide))
            frontend.append(uncommonWordsOnSlide)

            frontend.append(desc)
                        
        time.sleep(2)
        count+=1

    print("I am done")

    return frontend


