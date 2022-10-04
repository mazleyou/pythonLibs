import win32com.client
import os

app = win32com.client.Dispatch('InDesign.Application.2022')

myFile = r'C:\hskim\ws\python\pythonLibs\indesign_rerange\NE3.indd'
directory = os.path.dirname(myFile)

myDocument = app.Open(myFile)
myPage = myDocument.Pages.Item(1)
myItem = myPage.PageItems
for item in myItem:
    print(item)

myRectangle = myPage.Rectangles.Add()
myRectangle.GeometricBounds = ["6p", "6p", "18p", "18p"]
myRectangle.StrokeWeight = 12
#leave the document open...
print(myDocument.FullName)
# myDocument.Close()

# cdispatch to array
# https://stackoverflow.com/questions/11264684/convert-win32com-collection-to-python-list