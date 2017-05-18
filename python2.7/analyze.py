import dblottery
debug=1
db = dblottery.dblottery()

def get_one_year_data_(year):
    rows =db.query(r"SELECT * FROM lottery.doubleball where doubleball.GENERATE_TIME like '"+year+"%'")
    #for row in rows:
    if debug==1: print str(rows[0]["IDENTIFIER"]).strip("\"")
    if debug==1: print rows[0]["GENERATE_TIME"].strip("\"")
    if debug==1: print rows[0]["RED1"].strip("\"")

def get_data_indentifier_range(year_begin,year_end):
    rows =db.query(r"SELECT * FROM lottery.doubleball where doubleball.IDENTIFIER between "+year_begin+" and "+ year_end )
    #for row in rows:
    if debug==1: print str(rows[0]["IDENTIFIER"]).strip("\"")
    if debug==1: print rows[0]["GENERATE_TIME"].strip("\"")
    if debug==1: print rows[0]["RED1"].strip("\"")
    if debug==1: print str(rows[len(rows)-1]["IDENTIFIER"]).strip("\"")
    if debug==1: print rows[len(rows)-1]["GENERATE_TIME"].strip("\"")
    if debug==1: print rows[len(rows)-1]["RED1"].strip("\"")


def get_all_data():
    rows =db.query(r"SELECT * FROM lottery.doubleball where 1=1 " )
    #for row in rows:
    if debug==1: print str(rows[0]["IDENTIFIER"]).strip("\"")
    if debug==1: print rows[0]["GENERATE_TIME"].strip("\"")
    if debug==1: print rows[0]["RED1"].strip("\"")
    if debug==1: print str(rows[len(rows)-1]["IDENTIFIER"]).strip("\"")
    if debug==1: print rows[len(rows)-1]["GENERATE_TIME"].strip("\"")
    if debug==1: print rows[len(rows)-1]["RED1"].strip("\"")

if __name__ == '__main__':
    get_one_year_data_('2008')
    get_data_indentifier_range('2009001','2010160')