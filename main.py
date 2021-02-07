import getUTRData as UTR
import getITFData as ITF
import tennis_recruiting_net as trn
import pprint as pp
import xlwt
from xlwt import Workbook

masterDict = {}

def getData():
    UTR.getUTRData(masterDict)
    trn.retrieve_tennis_recruiting_net(masterDict)
    #ITF.getITFData(masterDict)
    print(str(len(masterDict)) + " players in database")

def print_player(out, name, row):
    out.write(row,0,name)
    out.write(row,1,masterDict[name].age)
    out.write(row,2,masterDict[name].country)
    out.write(row,3,masterDict[name].status)
    if "UTR" in masterDict[name].site.keys():
        out.write(row,4,masterDict[name].site["UTR"])
    if "ITF" in masterDict[name].site.keys():
        out.write(row,5,masterDict[name].site["ITF"])
    if "USTA" in masterDict[name].site.keys():
        out.write(row,6,masterDict[name].site["USTA"])
    if "TRN" in masterDict[name].site.keys():
        out.write(row,7,masterDict[name].site["TRN"])

def generate_spreadsheet():
    wb = Workbook()
    out = wb.add_sheet("Recruitment_Sheet", cell_overwrite_ok=True)
    out.write(0,0,"NAME")
    out.write(0,1,"AGE")
    out.write(0,2,"COUNTRY")
    out.write(0,3,"STATUS")
    out.write(0,4,"UTR")
    out.write(0,5,"ITF")
    out.write(0,6,"USTA")

    row = 1
    for name in masterDict.keys():
        print_player(out, name, row)
        row += 1

    wb.save("Recruitment_Sheet.xls")

getData()
generate_spreadsheet()