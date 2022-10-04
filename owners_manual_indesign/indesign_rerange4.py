import win32com.client
import os
import time
import rerange_from_GeometricBounds

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
myFile = r'C:\hskim\ws\python\pythonLibs\owners_manual_indesign\NE2.indd'
myDoc = app.Open(myFile, ShowingWindow=False)
docBaseName = myDoc.Name

all_item_list = []
item_list = []
for myPage in myDoc.Pages:
    for myFrame in myPage.TextFrames:
        if myFrame.Contents != "":
            item_list.append('t')
            item_list.extend(list(map(int, myFrame.GeometricBounds)))
            item_list.append(myFrame.Contents)
            print("contents : " + myFrame.Contents)

            all_item_list.append(item_list)
            item_list = []
    for item in myPage.PageItems:
        for rec in item.Rectangles:
            for image in rec.Images:
                item_list.append('i')
                item_list.extend(list(map(int, rec.GeometricBounds)))
                item_list.append(image.ItemLink.FilePath)
                print("contents : " + image.ItemLink.FilePath)

                all_item_list.append(item_list)
                item_list = []

# 추출한 아이템 재배치
all_item_list = rerange_from_GeometricBounds.rerange(all_item_list)
# 재배치한 아이템을 새로운 indesign 파일에 저장
for record in all_item_list:
    if record[0] == 't':
        newTextFrame = newPage.TextFrames.Add()
        newTextFrame.GeometricBounds = tuple((map(str, record[1:5])))
        newTextFrame.Contents = record[5]
    elif record[0] == 'i':
        myRectangle = newPage.Rectangles.Add()
        myRectangle.GeometricBounds = tuple((map(str, record[1:5])))
        myRectangle.Place(record[5])
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
















