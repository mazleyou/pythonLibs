import win32com.client
import os

# Use your version of InDesign here
app = win32com.client.Dispatch('InDesign.Application.2022')
myFile = r'C:\hskim\ws\python\pythonLibs\owners_manual_indesign\NE2.indd'
myDoc = app.Open(myFile, ShowingWindow=False)

# Navigate a document page wise
for myPage in myDoc.Pages:
    # Get the text frames in the page
    for myFrame in myPage.TextFrames:
        # Get Contents directly: Type = str
        myContents = myFrame.Contents
        print("contents : " + myContents)
        # Get paragraphs in the text frame
        # Navigate a document storywise
    for item in myPage.PageItems:
        # print(story.Contents)
        for rec in item.Rectangles:
            for image in rec.Images:

                print("story : ")
