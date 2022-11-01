from flask import render_template,session,redirect,request
# from matplotlib.style import use
# from numpy import save
# from requests import HTTPError
import requests
import values as V
import functions as F
import configs as C
from functools import wraps
# import datetime
import os
import pyrebase
# import pandas as pd
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
updt = lambda coll,id,field='',val='',dct={}: db.collection(coll).document(id).update({field:val} if not dct else dct)
form = lambda titre,key,msg="",req={},oob='': render_template('form.html', session=session, titre=titre,V=V, F=F,ctt=F.Form(key,msg,req,oob))
home = lambda: render_template('home.html', F=F,V=V,titre='Accueil')
panel = lambda id,r: redirect(f"{V.links[V.lkPnl]}/{id}/{F.getSt(r)}")
isGet = lambda: request.method == 'GET'
userColl = coll(V.collUser)

cAuth = fbase.auth()

freeUser = lambda email: updt(V.collUser,email,dct={V.bloque:V.notBlocked})

def getData(clt,id):
    try:    
        dt = coll(clt).document(id).get()

        if dt.exists:
            return dt.to_dict()
        return False
    except:
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


def rstArgs(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        """A wrapper function"""
        desc = dict(request.args)
        l = len(desc.keys())
        if l not in [4,1]: return redirect('/')
        # if 
        lst = [V.mode,V.oobCode,V.apiKey,V.lang] if l==4 else [V.oobCode]
        for i in desc.keys():
            if i not in lst :
                return redirect('/')
        # return desc
        # else: return redirect('/login')
        return func(*args, **kwargs)
        # Extend some capabilities of func
    return wrapper

def chkNivo(id):
    try:
        dmd = getData(V.collDmd,id)
        if dmd:
            return int(F.sNvo())>int(dmd[V.niveau])
        return False
    except:
        return False

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

def setTks(user):
    session[V.tk] = user['idToken']
    session[V.rTk] = user['refreshToken']
    
def chkTk(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        """A wrapper function"""
        if session.get(V.tk) is not None:
            try:
                user = auth.verify_id_token(session.get(V.tk))
                user = cAuth.refresh(session.get(V.rTk))
                setTks(user)
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
            return redirect('/')
        return f(*args, **kwargs)
    return wrap

def saveInColl(clt,doc,cid='id'):
    try:
        coll(clt).document(doc[cid]).set(doc)
        return True
    except:
        return False

def getAllData(coll,ctrt: Ctrt=None,k=None,v=None):

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
        # print(qry)
        data = eval(f"""{qry}""")
    l = []

    for c in data:
        if c.exists: 
            vl = c.to_dict()
            if k and v:
                if vl[k]==v:
                    l.append(vl)
                # else: pass
            else: l.append(vl)
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
    ctrt.add(V.niveau,'>',int(F.sNvo()))
    ctrt.add(V.statut,'==',V.attente)
    data = getAllData(coll if coll else V.collDmd,ctrt)
    data = data if len(data)==0 else F.sortDf(data,V.date)

    return data

def conn(email,pwd):
    # msg = 'Veuillez bien verifer votre email ou mot de passe'
    msg = 'Cet compte est bloqué, contactez le service informatique!'
    
    hist = F.crtHist(email,V.conn)
    
    
    try:
        
        # print(email)
        usr = cAuth.sign_in_with_email_and_password(email,pwd)
        # print(usr)
        tk = usr['idToken']
        # rtk = usr['refreshToken']
        usrInf = cAuth.get_account_info(tk)
        # print(usrInf)
        if not usrInf['users'][0]['emailVerified']:
            cAuth.send_password_reset_email(email)
            return f'Desolé cet email vous devez change votre mot de passe, un email vient de vous etre adreese a l\'email {email} !!'
        user = getData(V.collUser,email)
        # print(user)
        if user:
            if user[V.bloque]==V.isBlocked:
                hist[V.resultat] = V.accBlocked
                saveInColl(V.collLog,hist)
                return msg
            # user = user.to_dict()
            # print(F.sTk())
            updt(V.collUser,email,V.nb_tent,0)
            user[V.nb_tent] = 0
            
            for i in user.keys():
                session[i] = user[i]
            # session[V.tk] = tk
            # session[V.rTk] = rtk
            setTks(usr)
            hist[V.resultat] = V.cntd
            
            saveInColl(V.collLog,hist)
            return True
        
        hist[V.resultat] = V.emlNotFound
        saveInColl(V.collLog,hist)
        msg = 'Cet utilisateur n\'existe pas'
        session.clear()
        return msg
    except requests.exceptions.HTTPError as e:
        # print(e)
        user = getData(V.collUser,email)
        if user and F.isBlocked(user):
            hist[V.resultat] = V.accBlocked
            saveInColl(V.collLog,hist)
            return msg
        
        e = str(e)
        msg = 'Veuillez bien verifer votre '
        if V.pwdIncorr in e:
            nt = user[V.nb_tent]
            if nt==V.maxTentative:
                hist[V.resultat] = V.limitTent
                updt(V.collUser,email,V.bloque,V.isBlocked)
            else:
                hist[V.resultat] = V.pwdIncorr
                updt(V.collUser,email,V.nb_tent,nt+1)
            msg += 'mot de passe'
        elif V.emlNotFound in e:
            hist[V.resultat] = V.emlNotFound
            msg += 'email'
        elif V.fbaseDsbld in e:
            hist[V.resultat] = V.accBlocked
            # user = getData(V.collUser,email)
            updt(V.collUser,email,V.bloque,V.isBlocked)
            msg = 'Cet compte est bloqué, contactez le service informatique!'
        saveInColl(V.collLog,hist)
        session.clear()
        return msg

def saveHist(hist,rslt):
    hist[V.resultat] = rslt
    saveInColl(V.collLog,hist)

def resetPwd(pwd,oobCode):
    hist = F.crtHist('req@req.req',V.rstRai)
    try:
        usr = cAuth.verify_password_reset_code(oobCode,pwd)
        eml = usr['email']
        hist[V.email]=eml
        freeUser(eml)
        saveHist(hist,V.success)
        return True
    except Exception as e:
        e = str(e)
        l = ''
        if V.invOob in e:
            l = V.invOob
            saveHist(hist,l)
            return None
        else: l= V.failure
        saveHist(hist,l)
        return False    

def create_user(user):
    hist = F.crtHist(raison='CREATE_USER')
    l = ''
    
    try:
        
        eml = user[V.email]
        usr = cAuth.create_user_with_email_and_password(eml,'miam===?milouu.%+!!!22')
        
        cAuth.send_password_reset_email(eml)
        rs = saveInColl(V.collUser,user,V.email)
        
        if rs:
            l = V.success
        else:
            l = V.failure
            cAuth.delete_user_account(usr['idToken'])
        saveHist(hist,l)
        return rs
        
            
    
    except Exception as e:
        if type(e).__name__=='EmailAlreadyExistsError':
            l = V.emlExist
        else:
            l = V.failure
        # print(e)
        saveHist(hist,l)
        return None

def checkPwd(pwd):
    try:
        # print(F.sEml())
        usr = cAuth.sign_in_with_email_and_password(F.sEml(),pwd)
        return True
    except Exception as e:
        # print(e)

        return False

def logout():
    # if os.path.exists(getPrfl()):
    #     os.remove(getPrfl())
    session.clear()
    return redirect('/')


