import getUTRData as UTR
import getITFData as ITF
import pprint as pp
import xlwt
from xlwt import Workbook

wb = Workbook()
masterDict = {}

def getData():
    UTR.getUTRData(masterDict)
    ITF.getITFData(masterDict)

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

def generate_spreadsheet():
    out = wb.add_sheet("Sheet 1")
    out.write(0,0,"NAME")
    out.write(0,1,"AGE")
    out.write(0,2,"COUNTRY")
    out.write(0,3,"STATUS")
    out.write(0,4,"UTR")
    out.write(0,5,"ITF")
    out.write(0,6,"USTA")

    row = 0
    for name in masterDict.keys():
        print_player(out, name, row)
        row += 1