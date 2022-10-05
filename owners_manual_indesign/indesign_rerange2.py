import win32com.client
import os
import time

app = win32com.client.Dispatch('InDesign.Application.2022')

start = time.time()

# 임시 인디자인 파일 생성
newDocument = app.Documents.Add()

newPage = newDocument.Pages.Item(1)

newFile = r'C:\hskim\ws\python\pythonLibs\owners_manual_indesign\NE2_new.indd'
directory = os.path.dirname(newFile)
try:
    if not os.path.exists(directory):
        os.makedirs(directory)
    if os.path.exists(directory):
        newDocument.Save(newFile)
except Exception as e:
    print('Make new indesign file failed: ' + str(e))

# 원본 인디자인 파일 열기
myFile = r'C:\Users\daredevil\PycharmProjects\pythonLibs\owners_manual_indesign\NE1-0.indd'
myDoc = app.Open(myFile, ShowingWindow=False)
docBaseName = myDoc.Name

# Navigate a document page wise
all_item_list = []
item_list = []
for myPage in myDoc.Pages:
    # Get the text frames in the page
    for myFrame in myPage.TextFrames:
        # Get Contents directly: Type = str
        if myFrame.Contents != "":
            newTextFrame = newPage.TextFrames.Add()
            item_list.append('t')
            item_list.extend(list(map(int, myFrame.GeometricBounds)))
            newTextFrame.GeometricBounds = myFrame.GeometricBounds
            newTextFrame.Contents = myFrame.Contents
            item_list.append(myFrame.Contents)
            print("contents : " + myFrame.Contents)
            all_item_list.append(item_list)
            # Get paragraphs in the text frame
        # Navigate a document storywise
    for item in myPage.PageItems:
        # print(story.Contents)
        for rec in item.Rectangles:
            for image in rec.Images:
                print(image.ItemLink.FilePath)
                myRectangle = newPage.Rectangles.Add()
                myRectangle.GeometricBounds = rec.GeometricBounds
                myRectangle.Place(image.ItemLink.FilePath)




            # Get all the paragraph styles in the document

# if app.Documents.Count is not 0:
#     directory = os.path.dirname(myFile)
#     docBaseName = myDocument.Name
#     stories = myDocument.stories.Item(5)
#
#     for x in range(0, myDocument.Pages.Count):
#         myItem = myDocument.Pages.Item(x + 1).PageItems
#
#         newPage.Item.Add(myItem)

# 추출한 아이템 재배치

# 재배치한 아이템을 새로운 indesign 파일에 저장


# 저장한 indesign 파일을 pdf로 변환
for y in range(0, newDocument.Pages.Count):
    myPageName = newDocument.Pages.Item(y + 1).Name
    # We want to export only one page at the time
    app.PDFExportPreferences.PageRange = myPageName
    # strip last 5 char(.indd) from docBaseName
    myFilePath = directory + "\\" + docBaseName[:-5] + "_" + myPageName + ".pdf"
    newDocument.Export(1952403524, myFilePath)

    print("time :", time.time() - start)
# 원본 indesign 파일 닫기
myDoc.Close()
# 새로운 indesign 파일 닫기
newDocument.Close()
















