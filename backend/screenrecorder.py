# To install
# pip install pyautogui
# pip install pytesseract
# pip install NLTK
# pip install opencv-python
# Install Tesseract https://github.com/UB-Mannheim/tesseract/wiki
# Set your OCR directory in line 31 (currently it is set up for my personal directory)


# TODO 
# Drop down box to get domain of presentation
# Return definition based on domain, not fully implemented
# Move code from while loop into a function call
# Get user coordinates for screenshot
# Get topic of presentation from slide 1
# Return first def if specific definition isn't available
# Return wiktionary link for the word in question, for frontend to use


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

def screenRecord(screenCoord):

    #OCR Directory
    #pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Nasty\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

    screenCoord =  json.loads(screenCoord)
    print("I have coord: " + str(screenCoord))

    print("Button Click Coord: " + str(screenCoord[0][0]))

    print("Top Left Coord: " + str(screenCoord[1][0]))

    print("Top Right Coord: " + str(screenCoord[2][0]))

    print("Bottom Left Coord: " + str(screenCoord[3][0]))


    print("Bottom Right Coord: " + str(screenCoord[4][0]))




    sno = nltk.stem.SnowballStemmer('english')
    parser = WiktionaryParser()

    # Front-End Variable
    frontend = []

    with open("wordList.txt") as f:
        content = f.readlines()
    content = [x.strip() for x in content]

    lastText = ""
    slideNum = 0
    domain = "computing" # Have this domain be set by the user

    

    count = 0
    while count != 1:
        img = pyautogui.screenshot(region=(0,100,1280, 940)) # (left, top, width, height)

        img.save("screenshot.png")
        image = cv2.imread("screenshot.png")
        gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        threshold_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        im = Image.open("slide4.png")
        newText = pytesseract.image_to_string(im).strip().lower().split()

        if (newText != lastText):
            lastText = newText
            print("Last deciphered text: ")
            print(lastText)
            slideNum = slideNum + 1
            print("Slide Number: ")  
            print(slideNum)
            uncommonWordsOnSlide = [x for x in lastText if x not in content]
            print("Uncommon words: ")
            print(uncommonWordsOnSlide)

            frontend.append(slideNum)
            frontend.append(uncommonWordsOnSlide)

            desc = []
            
            for i in uncommonWordsOnSlide:
                specialDef = False # Set this to true if program finds a domain-specific definition
                word = parser.fetch(i)
                for k, v in word[0].items():
                    if (k == 'definitions'):
                        listStuff = v[0].get('text')
                        for i in listStuff:
                            if domain == "computing" and "(computing)" in i: 
                                print(i) # Prints the definition with (computing)
                                specialDef = True
                                desc.append(i)
                                break
                        if specialDef == False: # If program does not find a definition specific to the domain
                            print(listStuff) # This prints all definitions, can be changed to only first definition
                            desc.append(listStuff[0])
            frontend.append(desc)
                        
        time.sleep(2)
        count+=1

    print("I am done")

    return frontend


