# 
# fix_links.py
#

import sys

from xlrd import open_workbook # ,cellname
from xlwt import Formula, Workbook
from xlutils.copy import copy
# from xlutils.save import save

def find_cell(sheet, row_index, col_index):
    row = sheet._Worksheet__rows.get(row_index)
    if row:
        return row._Row__cells.get(col_index)
    return None

def update_url(url, textmark):
    print "Original: " + url
    index = url.find("%20-%20")
    if index != -1:
        url[index:index+7] = "%23"
        print "Fixed: " + url
    index = url.find("#")
    if index != -1:
        url[index] = "%23"
        print "Fixed: " + url
    if textmark is not None:
        url += "%23" + textmark
        print "Fixed: " + url
    return url

def update_sheet(book_sheet, sheet):
    for row_index in range(book_sheet.nrows):
        for col_index in range(book_sheet.ncols):
            link = book_sheet.hyperlink_map.get((row_index, col_index))
            if link is None:
                continue
            url = link.url_or_path
            if url is None:
                continue
            url = update_url(url, link.textmark)
            old_cell = find_cell(sheet, row_index, col_index)
            sheet.write(row_index, col_index, Formula('HYPERLINK("%s";"%s")' % (url,link.desc)))
            if old_cell:
                new_cell = find_cell(sheet, row_index, col_index)
                if new_cell:
                    new_cell.xf_idx = old_cell.xf_idx
            # print cellname(row_index, col_index),'-',
            # print sheet.cell(row_index, col_index)
            # try:
            #     print sheet.cell(row_index, col_index).value
            # except UnicodeEncodeError:
            #     print "UnicodeEncodeError"

def update_workbook(filename):
    book = open_workbook(filename, formatting_info=True) # , on_demand=True)
    sheets = book.sheets()
    nsheets = book.nsheets
    wb = copy(book)
    for x in range(nsheets):
        book_sheet = sheets[x]
        sheet = wb.get_sheet(x)
        print sheet.name
        update_sheet(book_sheet, sheet)
    wb.save(filename)


# Problems:
# formatting not completely preserved (mostly colors, and cell sizes)
# running the program twice removes all cells with modified links
# hyperlink functionality becomes limited
# fails for .xlsx files (formatting_info not implemented)
if __name__ == "__main__":
    args = sys.argv[1:]
    for filename in args:
        update_workbook(filename)