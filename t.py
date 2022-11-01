import pyodbc
import json

conn = pyodbc.connect('Driver={SQL Server};'
            'Server=BRA-SOGODOGO;'
            'Database=mytrans;'
            'Trusted_Connection=yes;'
        )

cr = conn.cursor()
# cr.execute(qry)
# conn.commit()
def chkTb(tb):
    # cr = conn.cursor()
    
    for k in cr.tables():
        if k.table_name==tb:
            return True
    return False

# print(chkTb('Persons'))

# qry = lambda :"""
#         CREATE TABLE Persons (
#             PersonID int primary key,
#             LastName varchar(255),
#             FirstName varchar(255),
#             Address varchar(255),
#             City varchar(255)
#         )
#         """
        
with open(r"U:\PP\mytrans\static\files\schema.json") as f:
    tabs = json.load(f)

def crtTab(nm,dt):
    try:
            
        fl = ""
        
        for i in dt.keys():
            fl += f"{i} {dt[i]},"
        fl = fl[:-1]
        
        qry = f"""create table {nm}({fl})"""
        # cr = conn.cursor()
        cr.execute(qry)
        conn.commit()
    except:
        return False
    return True

# print(jj)
j=0
for i in tabs.keys():
    # print(chkTb(i))
    if not chkTb(i):
        j += 1
        qry = crtTab(i,tabs[i])
        # qry = """
        #     CREATE TABLE Persons (
        #         PersonID int primary key,
        #         LastName varchar(255),
        #         FirstName varchar(255),
        #         Address varchar(255),
        #         City varchar(255)
        #     )
        # """
    # print(qry)
        # cr1 = conn.cursor()
        # cr1.execute(qry)
        # conn.commit()
print(j)   
        

# print(crtTab('demande',tabs['demande']))