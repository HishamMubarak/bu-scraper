import requests
import csv
from bs4 import BeautifulSoup
from csv import writer

students = []
prefix = "15XWSB"
start = 7000
end = 7121
for num in range(start, end):
    students.append(prefix+str(num))
allStudents = []
addedHeader = False
fieldNames = None

for index, eachId in enumerate(students):
    url = "http://52.77.88.220:7878"
    fields = {"__VIEWSTATE":"/wEPDwULLTIxNDY4MDQ4NjYPZBYCAgMPZBYCAggPPCsAEQIBEBYAFgAWAAwUKwAAZBgBBQlndlJlc3VsdHMPZ2QRk9fksoV5Ul/RMr5bHZjPxNDjIYgQ14atj8br0w+MZA==",
    "__VIEWSTATEGENERATOR":"F14BD380",
    "__EVENTVALIDATION":"/wEdAAPelJBg/YYMqiVugcKwhlZ6b05AccaY0WTpjM9jxHOiA4Xk8eg39i9/g7dDieziUysBE9b7nwiVQ2Y+/2FxZWPwCoQ7ri5OCliBtVATktjtlw==",
    "txtRegisterNumber":eachId,
    "btnViewResult":"Check Result"}

    response = requests.post(url, fields)
    soup = BeautifulSoup(response.text, "html.parser")
   
    if soup.find(id="lblMessageBox") != None:
        print(eachId + " IS NOT REGISTERED")
    else:
        
        results = soup.find(id="gvResults", newline='')
        if addedHeader == False:
            addedHeader = True
            # ADDING CELL HEADERS. ID, NAME and SUBJECT LIST
            tableHeader = ["ID", "Name"]
            for each in results:
                headers = each.find("span")
                if headers == -1:
                    continue
                elif headers == None:
                    continue
                else:
                    tableHeader.append(headers.get_text() + " = " + each.select_one("td:nth-of-type(5)").text)
            with open("results.csv", "w") as csv_file:
                fieldNames = tableHeader
                writer = csv.DictWriter(csv_file, fieldnames=tableHeader)
                writer.writeheader()
    
        # GETTING STUDENT DETAILS
        studentDetails = soup.find(class_="table-light-green")
        name = studentDetails.select("#lblStudentName")[0].text

        # GETTING SUBJECT AND MARKS
        rows = results.find_all("tr")
        dataToPush = {"ID":eachId, "Name":name}
        # Getting Subject Details into Array
        for rowIndex,row in enumerate(rows[1:]):
            row.find(class_="hide").decompose()
            row.find(id="gvResults_imgRank_"+str(rowIndex)).decompose()
            row.find(id="gvResults_lblRankDetails_"+str(rowIndex)).decompose()

            eachSubject = row.select_one("td:nth-of-type(1)").find("span").text
            subType = row.select_one("td:nth-of-type(4)").text
            eachMarks = row.select_one("td:nth-of-type(5)").text

            with open('results.csv', newline='') as myFile:
                csv_input = csv.reader(myFile)
                header = next(csv_input)
                for titleIndex, eachTitle in enumerate(header):
                    if eachSubject in eachTitle:
                        if subType in eachTitle:
                            dataToPush[eachTitle] = eachMarks

        allStudents.append(dataToPush)
        print(eachId)

with open('results.csv', 'w', newline='') as csvFile:
    writer = csv.DictWriter(csvFile, fieldnames=fieldNames)
    writer.writeheader()
    writer.writerows(allStudents)

