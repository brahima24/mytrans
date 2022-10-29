import pyodbc
import pandas as pd
import os


class Values():
    
    def __init__(self):
        
        tInt = 'int'
        tFloat = 'float'
        tList = 'list'
        tStr = 'str'
        tTpl = 'tuple'
        self.static = 'static'
        self.tempDir = self.static+'/temp/'
        # self.server_name = 'ARCH-VM-01'
        # self.db_name = 'MoovappsProcess'
        self.tabDmd = 'fc_file'
        self.str = 'str'
        self.nbr = 'nbr'
        self.na = '****'
        self.multiple = 'multiple'
        self.tabTest = 'test'
        self.tabData = 'r_worimportgrou'
        self.date = 'date'
        self.typeNumber = [tInt,tFloat]
        self.typeString = [tStr]
        self.typeMultiple = [tList,tTpl]

class Constraint():
    
    def __init__(self,field:str,comparator:str,value):
        # self.fields = [field] if self.fields else  self.fields.append(field)
        # self.comparators = [comparator] if self.comparators else  self.comparators.append(comparator)
        # self.values = [value] if self.values else  self.values.append(value)
        self.fields = [field]
        self.comparators = [comparator]
        self.values = [value]
        self.connector = []
    
    def add(self,connector,field,comparator,value):
        
        # ad = lambda ls,vl: ls.append(vl)
        self.connector += [connector]
        self.fields += [field]
        # self.fields = ad(self.fields,field)
        self.comparators += [comparator]
        self.values += [value]
    
    def min(self,ind=None):
        
        mn = lambda ls: ls[:ind]+ls[ind+1] if ind else ls[:-1]
        self.fields =  mn(self.fields)
        self.comparators = mn(self.comparators)
        self.values = mn(self.values)

class Funcs():
    
    def __init__(self):
        pass
        # self.vv = 'Milouuu'
    
    getT = lambda self, val: type(val).__name__
    isT = lambda self, vl,ls: self.getT(vl) in ls
    isStr = lambda self, vl: self.getT(vl) == 'str'
    getV = lambda self, val: f'{val}' if self.isT(val,v.typeNumber) else  f"'{val}'" if self.isT(val,v.typeString) else None
    jnPth = lambda self,p1,p2: p1+'/'+p2
    toDf = lambda self, sr: pd.DataFrame(sr.to_frame())
    cctDf = lambda self, c: pd.concat(c,axis=1).transpose() if len(c)!=0 else pd.DataFrame()
    getNa = lambda self, df: df[df.isna().any(axis=1)]
    getNotNa = lambda self, df: df.dropna(axis=0)
    fPth = lambda self,dt: f'temp/{dt["id"]}.pdf'
    readExl = lambda self,ctt: pd.read_excel(ctt).fillna(v.na)
    fmtVal = lambda self, vl: str(vl).replace("'",'')
    dfToDict = lambda self,dt: dt.iloc[0].to_dict() if len(dt)!=0 else {}
    # getIdsInDf = lambda self,df,ids: 
    hdFile = lambda self,dt: '' if os.path.exists(v.static+'/'+self.fPth(dt)) else shutil.copyfile(v.filesDir+dt[v.relPath].replace('\\','')+'/'+dt[v.phPath], v.static+'/'+self.fPth(dt))
    
    def rmSpc(self,vl):
        val = ''
        vl = str(vl).strip()
        # print(vl)
        vl = vl.split('  ')
        if len(vl)==0: return vl[0]
        for i in vl:
            val += i.strip()+' ' if i!='' else ''
        return val[:-1]
    
    def chkInt(self,v):
        try:
            return int(v)
        except:
            return False
    
    def getVal(self,val):
        # if self.isT(tp,v.typeNumber):v = f'{val}' 
        # elif self.isT(tp,v.typeString): v = f'"{val}"'
        v = self.getV(val)
        
        if not v:
            v = '('
            for j in val:
                v += f'{self.getV(j)},'
            v = v[:-1]+')'
        
        return v
    
    def makeWhere(self,ctrt: Constraint=None):
        
        if not ctrt: return ''
        wh = ''
        for i in range(len(ctrt.fields)):
            vl = ctrt.values[i]
            v = self.getVal(vl)
            wh += ctrt.connector[i-1] if i>0 else ''
            wh += f' {ctrt.fields[i]} {ctrt.comparators[i]} {v} '
        return f'where{wh}'
    
    def makeQuery(self,tab:str,fields: list=None, ctrt: Constraint= None):
        tb = ''
        jn = ''
        if fields:
            for f in fields:
                tb += f'{f},'
                
            tb = tb[:-1]
        elif tab == v.tabData:
            tab = f"{tab} d"
            tb = """
                d.id, d.sysReference, d.Cercle, d.Commune, d.CentreDEtatCivil, d.NDuRegistre, d.Annee, 
                d.NatureDoc, d.TypeReg, dbo.rmSpc(f.name,1) name,
                dbo.rmSpc(f.relativePath,1) relativePath,
                dbo.rmSpc(f.physicalName,1) physicalName
            """
            
            jn = """
                LEFT OUTER JOIN dbo.r_worimportgrou_Document d1 ON d.id = d1.resource_id
                LEFT OUTER JOIN dbo.fc_file f ON d1.link_id = f.id
            """ 
            ctrt.add('and', 'sysReferenceroot', '=', 'ImportGroupe_ImportDesDocuments_1.0') 
        else: tb = '*'
        
        cond = self.makeWhere(ctrt) #if tab==v.tabData else ''
        return f"""
            SELECT {tb} FROM {tab} 
            {jn}
            {cond}
        """
    
    def crtIdDt(self):
        t = localtime()
        dt=''
        id = 'mm'
        for i in range(3):
            dt += str(t[i])+'/'
        dt = dt[:-1]+' '
        for i in range(3,6):
            # id += i
            dt += str(t[i])+':'
        dt = dt[:-1]
        # id = str(int(np.random.rand()*10000))
        # lt = ''.join(np.random.choice(string.ascii_lowercase) for i in range(2))
        # id = list(id+lt)
        # random.shuffle(id)
        # id = []
        # id = ''.join(i for i in id)
        return id,dt

v = Values()
f = Funcs()
class SQL():
    
    def __init__(self):
        self.conn = pyodbc.connect('Driver={SQL Server};'
                                        'Server=BRA-SOGODOGO;'
                                        'Database=mytrans;'
                                        'Trusted_Connection=yes;'
                                    )
    
    
    pdQry = lambda self,qry: pd.read_sql_query(qry,self.conn).fillna(v.na)
    
    def excQry(self, qry):
        cursor = self.conn.cursor()
        cursor.execute(qry)

    def getAllData(self,tab: str, fields: list=None ,ctrt: Constraint=None):
        qry = f.makeQuery(tab,fields,ctrt)
        return self.pdQry(qry)
    
    
    def chkId(self,idd,tb):
        # print(idd)
        c = 'id' #if tb==v.tbCorr else 'd.id'
        ct = Constraint(c, '=', int(str(idd).replace(' ','')))
        qry = f.makeQuery(tb,ctrt=ct)
        # print(qry)
        return f.dfToDict(self.pdQry(qry))

    def insertIntoDB(self,tab,dt):

        try:
            # print('Miammmmmmm')
            d = self.chkId(dt['id'],tab)
            # print(d)
            if not d:
                flds = ''
                vls = ""

                for i in dt.keys():
                    flds += f"{i},"
                    vls += f"'{dt[i]}',"
                qry = f"""
                    insert into {tab}({flds[:-1]}) values ({vls[:-1]})
                """
                # print(qry)
                self.excQry(qry)
                self.conn.commit()
            return True
        except Exception as e:
            # print(str(e))
            return False


    