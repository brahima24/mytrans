from flask import render_template,session,redirect,request
import values as V
import functions as F
import configs as C
from functools import wraps
import datetime
import os
import pyrebase
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore,auth
current_dir = os.getcwd()

files = os.path.join(current_dir,'static')
getPrfl = lambda : files+'temp\\'+session.get(V.email)+'.jpg'

cred = credentials.Certificate(C.admConf)
fadm = firebase_admin.initialize_app(cred)
fbase = pyrebase.initialize_app(C.fbConf)
db = firestore.client()

coll = lambda nom: db.collection(nom)
updt = lambda coll,id,field,val: db.collection(coll).document(id).update({field:val})
form = lambda titre,key,msg="",req={}: render_template('form.html', session=session, titre=titre,V=V, F=F,ctt=F.Form(key,msg,req))
home = lambda: render_template('home.html', F=F,V=V,titre='Accueil')
panel = lambda id,r: redirect(f"{V.links[V.lkPnl]}/{id}/{F.getSt(r)}")

userColl = coll(V.collUser)

cAuth = fbase.auth()

def getData(clt,id):
    dt = coll(clt).document(id).get()

    if dt.exists:
        return dt.to_dict()
    return False

def allArgs(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        """A wrapper function"""
        desc = dict(request.args)
        if len(desc.keys())!=0:
            return redirect('/')
        # else: return redirect('/login')
        return func(*args, **kwargs)
        # Extend some capabilities of func
    return wrapper

def args(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        """A wrapper function"""
        desc = dict(request.args)
        l = len(desc.keys())
        if l==0: return redirect('/')
        for i in desc.keys():
            if i not in [V.date,V.moyen]:
                return redirect('/')
        # return desc
        # else: return redirect('/login')
        return func(*args, **kwargs)
        # Extend some capabilities of func
    return wrapper

def lArgs(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        """A wrapper function"""
        desc = dict(request.args)
        l = len(desc.keys())
        if l==0: return func(*args, **kwargs)
        if l!=3: return redirect('/')
        for i in desc.keys():
            if i not in [V.date,V.moyen,V.chemin]:
                return redirect('/')
        # return desc
        # else: return redirect('/login')
        return func(*args, **kwargs)
        # Extend some capabilities of func
    return wrapper

class Ctrt():
    def __init__(self,field,comp,val):
        self.field = [field]
        self.comp = [comp]
        self.val = [val]

    def add(self,field,comp,val):
        self.field.append(field)
        self.comp.append(comp)
        self.val.append(val)

    def min(self,ind=None):

        self.field =  self.field[:ind]+self.field[ind+1] if ind else self.field[:-1]
        self.comp = self.comp[:ind]+self.comp[ind+1] if ind else self.comp[:-1]
        self.val = self.val[:ind]+self.val[ind+1] if ind else self.val[:-1]

def notTk():
    session.clear()
    return redirect(V.links[V.login])

def chkTk(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        """A wrapper function"""
        if session.get(V.tk) is not None:
            try:
                user = auth.verify_id_token(session.get(V.tk))
            except:
                return notTk()
            return func(*args, **kwargs)
        return notTk()
    return wrapper

def chkAdm(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        """A wrapper function"""
        if F.isAdm():
            return func(*args, **kwargs)
        return redirect('/')
    return wrapper

def chkSprUsr(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        """A wrapper function"""
        if F.isSprUsr():
            return func(*args, **kwargs)
        return redirect('/')
    return wrapper

def deAuth(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if session.get(V.tk):
            return redirect(V.links[V.lkConn])
        return f(*args, **kwargs)
    return wrap

def saveInColl(clt,doc,cid='id'):
    try:
        coll(clt).document(doc[cid]).set(doc)
        return True
    except:
        return False

def getAllData(coll,ctrt: Ctrt=None):

    if ctrt is None:
        data = db.collection(coll).order_by('id').stream()
    else:
        qry = "db.collection(coll)"
        # data = transaction
        # data = eval(f"transaction.where('{V.email}','{'=='}',{type('brahima.sogodogo@usmba.ac.ma').__name__}('{'brahima.sogodogo@usmba.ac.ma'}')).stream()")

        for c in range(len(ctrt.field)):
            tp = type(ctrt.val[c]).__name__
            vl = f"""{tp}("{ctrt.val[c]}")""" if tp!='list' else ctrt.val[c]
            qry += f""".where('{ctrt.field[c]}','{ctrt.comp[c]}',{vl})"""
        qry += ".stream()"
        print(qry)
        data = eval(f"""{qry}""")
    l = []

    for c in data:
        if c.exists: l.append(c.to_dict())

    return l

def chkLst(my,dte):
        ct = Ctrt(V.moyen,'==',my)
        ct.add(V.jourDeVoyage,'==',dte)
        ls = getAllData(V.collListe,ct)
        return len(ls)==0

def getListe(id,pub=False):#chm,dt,my,pub=False):

    lctrt = Ctrt(V.collListe,'==',id)
    # lctrt = Ctrt(F.getChV(chm),'==',dt)
    # lctrt.add(V.moyen,'==',my)
    # lctrt.add(V.statut,'==',V.valider)
    # lctrt.add(V.statut,'in',[V.valider,V.busAttente])
    lst = getAllData(V.collDmd,lctrt)
    # print(lst)
    return F.sortDf(lst,V.date,True,pub)

def getVoyL(isDep,dt):

    def chkDt(d,isAl=True):

        lst = V.bus_aller if isAl else V.bus_retour
        if d>=lst[-1]: return lst[0]
        elif d<lst[1]: return lst[1]
        else: return lst[2]

    # id,dt = F.crtIdDt()
    # dt = pd.to_datetime(dt)
    # day = dt.weekday()
    # if day in V.bus_aller:

    # dt += datetime.timedelta(days=2)
    # dt = f'{jr}/{mois}/{an}'
    # print(dt)
    col = V.dateDepart if isDep else V.dateArrivee
    ctrt = Ctrt(col,'==',dt)
    ctrt.add(V.statut,'==',V.confirmer)

    data = getAllData(V.collDmd,ctrt)
    data = data if len(data)==0 else F.sortDf(data,V.dateConf)

    return data

def getDep(jr=None,mois=None,an=None):
    dt = f'{jr}/{mois}/{an}'
    ctrt = Ctrt(V.dateDepart,'==',dt)
    ctrt.add(V.statut,'==',V.confirmer)

    return

def getConnData(coll=None):
    data = []
    # if F.isAdm():
    #     ctrt = Ctrt(V.statut,'==',V.valider)

    #     data = getAllData(coll if coll else V.collDmd, ctrt)
    # else:
    ctrt = Ctrt(V.dept,'==',F.sDept())
    # ctrt.add(V.dept,'==',F.sDept())
    ctrt.add(V.statut,'==',V.attente)
    data = getAllData(coll if coll else V.collDmd,ctrt)
    data = data if len(data)==0 else F.sortDf(data,V.date)

    return data

def conn(email,pwd):
    msg = 'Veuillez bien verifer votre email ou mot de passe'
    try:
        print(email)
        usr = cAuth.sign_in_with_email_and_password(email,pwd)
        # print(usr)
        tk = usr['idToken']
        usrInf = cAuth.get_account_info(tk)
        # print(usrInf)
        # if not usrInf['users'][0]['emailVerified']:
        #     cAuth.send_password_reset_email(email)
        #     return f'Desolé cet email vous devez change votre mot de passe, un email vient de vous etre adreese a l\'email {email} !!'
        user = getData(V.collUser,email)
        print(user)
        if user:
            # user = user.to_dict()
            # print(F.sTk())
            for i in user.keys():
                session[i] = user[i]
            session[V.tk] = tk
            return True
        session.clear()
        return msg
    except:
        session.clear()
        return msg

def create_user(user):
    try:
        eml = user[V.email]
        usr = cAuth.create_user_with_email_and_password(eml,'mmmmmm@99')
        v = cAuth.send_password_reset_email(eml)
        return saveInColl(V.collUser,user,V.email)
    
    except Exception as e:
        if type(e).__name__=='EmailAlreadyExistsError':
            return False
        print(e)
        return None

def checkPwd(pwd):
    try:
        # print(F.sEml())
        usr = cAuth.sign_in_with_email_and_password(F.sEml(),pwd)
        return True
    except Exception as e:
        print(e)

        return False

def logout():
    # if os.path.exists(getPrfl()):
    #     os.remove(getPrfl())
    session.clear()
    return redirect('/')


