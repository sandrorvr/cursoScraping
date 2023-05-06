import json
from ExtactPages import ExtractPages
from DataBaseConection import DB

with open('departments.json') as file:
    DEPARTMENTSJSON = json.load(file)
    
extrator = ExtractPages()


for key in DEPARTMENTSJSON.keys():
    for pg in range(1,3):
        print(key, pg)
        books = extrator.getBooksByDepartmentByPage(DEPARTMENTSJSON[key], pag=pg)
        for bk in books:
            data = [
                (
                    bk.getIdBook(),
                    bk.extractTitle(),
                    ','.join(bk.extractAuthors()),
                    bk.extractPrice()
                )
            ]
            print(data)
            