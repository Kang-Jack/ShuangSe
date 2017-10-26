#pip install xlrd
import xlrd
import dblottery
debug=1
db = dblottery.dblottery()
i=0
for year in range (2003,2016):
    book = xlrd.open_workbook(r"../data/"+str(year)+".xlsx")
    if debug : print("The number of worksheets is {0}".format(book.nsheets))
    if debug : print("Worksheet name(s): {0}".format(book.sheet_names()))
    sh = book.sheet_by_index(0)
    if debug : print("{0} {1} {2}".format(sh.name, sh.nrows, sh.ncols))
    if debug : print("Cell C30 is {0}".format(sh.cell_value(rowx=29, colx=2)))
    num_cols = sh.ncols

    for row_idx in range(sh.nrows):
        identifier = int(sh.cell(row_idx, 0).value)
        print(identifier)
        colors= str(sh.cell(row_idx, 1).value).split('|')
        colors= str(sh.cell(row_idx, 1).value).split('|')
        if debug : print (colors)
        reds =colors[0].split(',')
        if year == 2008 or year ==2009:
            reds.sort()
        r1=reds[0]
        r2=reds[1]
        r3=reds[2]
        r4=reds[3]
        r5=reds[4]
        r6=reds[5]
        b1=colors[1]
        if debug : print(str(sh.cell(row_idx, 1).value))
        lottery_date=str(sh.cell(row_idx, 2).value)
        if debug : print(r1)
        if debug : print(r2)
        if debug : print(r3)
        if debug : print(r4)
        if debug : print(r5)
        if debug : print(r6)
        if debug : print(b1)
        i=i+1
        db.insert_doubleball(identifier,lottery_date,r1,r2,r3,r4,r5,r6,b1)
print (i)