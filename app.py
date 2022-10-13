from flask import Flask, render_template, request,redirect,session
from flask_session import Session
import values as V
import functions as F
# from waitress import serve
import api as A


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
@A.allArgs
@A.deAuth
def home():
    # print(F.lkV('bus'))
    # tb = F.table(V.vDt,'','')
    return render_template('home.html', F=F,V=V,titre='Accueil', tb = '' )

@app.route('/superuser')
@A.allArgs
@A.chkTk
def spAdm():
    return render_template('home.html',V=V,F=F,titre='SP-USR')

@app.route(V.links[V.lkCrtUsr], methods=['GET','POST'])
@A.allArgs
@A.chkTk
@A.chkSprUsr
def crt_user():
    
    if request.method == 'GET':
        return A.form('Creer utilisateur',V.crtUser)
    
    form = dict(request.form)

    for k in form.keys():
        form[k] = F.rmSpc(form[k])
    
    form[V.role]= int(form[V.role])
    form[V.niveau] = V.superUsr if form[V.role]==V.superUsr else int(form[V.niveau])
    rs = A.create_user(form)
        # return render_template('aff.html',F=F,V=V,titre='Success')
    return redirect('/crt/'+('succes' if rs else 'echec'))


@app.route(V.links[V.lkConn], defaults={'tp':''}, methods=['GET','POST'])
# @app.route(V.links[V.lkConn]+'/<tp>', methods=['GET','POST'])
@A.allArgs
@A.chkTk
def conn(tp):
    # print(F.isSprUsr(),F.sNvo(),)
    if F.isSprUsr(): return redirect('/superuser')
    cTmp = lambda dmds, lk,val=False,msg='': render_template('conn.html', F=F,V=V,titre='Connecté',tb=F.table(dmds,lk,val),msg=msg)

    lk = V.links[V.lkConn]+f'/{tp}' if tp!='' else V.links[V.lkConn]
    if request.method == 'GET':
        # val = True if tp!='' else False
        # :
            # ctrt = A.Ctrt(V.statut,'==',V.statuts[V.valider] if F.isAdm() else V.statuts[V.confirmer])
            # print(ctrt.field)
        ttr = V.admDspl if F.isAdm() else V.usrDspl
        dmds = A.getConnData()
        nb = len(dmds)
        # dmds = dmds if nb==0 else F.sortDf(dmds,V.dateConf if F.isAdm() else V.date)
        # dmds = dmds if nb==0 else F.sortDf(dmds,V.dateConf if F.isAdm() else V.date)
        tb = f'Il y\'a {nb} demandes!' if nb!=0 else 'Il n\'a pas de demande!!'
        # dmds = [1,2,3]
        return cTmp(dmds,lk)
    # if lk!='':
    form = request.form
    id,dt = F.crtIdDt()
    for i in form.keys():
        A.updt(V.collDmd,i,V.statut,V.statuts[V.valider] if F.isAdm() else V.statuts[V.confirmer])
        A.updt(V.collDmd,i,V.dateConf,dt)
    return redirect(lk)

@app.route(V.links[V.login], methods=['GET','POST'])
@A.allArgs
@A.deAuth
def login():
    ttr = 'Form. de conn.'
    if request.method == 'GET':
        return A.form(titre=ttr,key=V.login)
    else:
        email = request.form[V.email]
        if len(request.form.keys())!=2:
            return A.form(ttr,V.login,'Le formulaire n\'est pa correcte!!',request.form)
        pwd = request.form[V.password]
        # conn = True
        conn = A.conn(email,pwd)
        # print(conn)
        if conn is True:
            return redirect(V.links[V.lkConn])
        else: return A.form(ttr,V.login,conn,request.form)


@app.route(V.links[V.lkListe], methods=['GET','POST'])
# @A.lArgs
@A.chkTk
@A.chkAdm
def listes():
    desc = dict(request.args)
    isD = len(desc.keys())==1
    if isD:
        id = desc['id']
        # my = desc[V.moyen]
        # dt = desc[V.date]
        # chm = desc[V.chemin]
        # cDt = F.getChV(chm)
    # dt = desc[V.date] if V.date in desc.keys() else False
    lk = V.links[V.lkListe]
    liste = lambda lst,tr=None,val=False,isL=True : render_template('listes.html',V=V,F=F,titre='Listes disponibles',tb=F.table(lst,lk,val,V.lstDspl if isL else V.admDspl,isL,tr=tr,))
    # dt = F.fmtdt(dt)
    if request.method=='GET':
        if isD:
            dmds = A.getListe(id)
            if len(dmds)!=0:
                # isD = False if dmds[0][V.lieu]==V.bko else True

                lk = F.lk(lk,['id'],[id])
                # lk1 = F.lk(F.lk(F.lk(lk,V.moyen,my),V.date,dt),V.chemin)
            return liste(dmds,isL=False)
        lst = A.getAllData(V.collListe)
        # lst=[]
        l = len(lst)
        tr = 'Il n\'y a pas de liste!!!' if l==0 else f'Il y {l} liste{"s" if l>1 else ""}!!'
        return liste(lst,tr)
    form = dict(request.form)

    if isD:
        dmds = A.getListe(id)
        for dmd in dmds:
            id = dmd['id']
            if id not in form.keys():
                A.updt(V.collDmd,id,V.statut,V.busAttente)

        return redirect(lk)
    lst = A.getAllData(V.collListe)
    for l in lst:
        i = l['id']
        if i in form.keys():
            chm, dt, my = l[V.chemin], l[V.jourDeVoyage], l[V.moyen]
            mmm = A.getListe(i,F.fTtr(my,chm,dt))
            A.updt(V.collListe,i,V.publier,V.oui)
        else: A.updt(V.collListe,i,V.publier,V.non)

    # return f'{form}'
    return redirect(lk)

@app.route(V.links[V.lkListDisp])
@A.allArgs
def liste():
    liste = lambda ctt,nb : render_template('liste.html',V=V,F=F,nb=nb,titre='Listes de transport', ctt=ctt)
    ctrt = A.Ctrt(V.publier,'==',V.oui)
    lst = A.getAllData(V.collListe,ctrt)
    ctt = ''
    l = len(lst)
    if l!=0:
        for ls in lst:
            # cDt = F.getChV(ls[V.chemin])
            # lctrt = A.Ctrt(dt,'==',ls[V.jourDeVoyage])
            # lctrt.add(dt,'==',ls[V.moyen])
            # lctrt.add(V.statut,'in',[V.valider,V.busAttente])
            # dmds = A.getAllData(V.collDmd,lctrt)
            # dmds = F.sortDf(dmds,V.dateConf,True)
            # print(cDt,ls[V.jourDeVoyage],ls[V.moyen])
            dmds = A.getListe(ls['id'])
            ctt += F.table(dmds,'',True,V.trsDspl,tr=F.fTtr(ls[V.moyen], ls[V.chemin], ls[V.jourDeVoyage]))
            # print(ctt)
            # print(len(dmds),'lllllll')
    return liste(ctt,l)

@app.route(f'{V.links[V.lkVoy]}/<chemin>', methods=['GET','POST'])
@A.chkTk
@A.args
@A.chkAdm
def voyage(chemin):
    desc = dict(request.args)
    isBus = False if desc[V.moyen]==V.avion else True if desc[V.moyen]==V.bus else None
    isDep = True if chemin==V.depart else False if chemin==V.retour else None

    if isBus is None or isDep is None: return redirect('/')

    dte = desc[V.date] if V.date in desc.keys() else None
    moyen = V.bus if isBus else V.avion
    col = V.dateDepart if isDep else V.dateArrivee
    vDep = [V.gkto,V.loulo] if isDep else [V.bko]
    notCol = V.dateDepart if not isDep else V.dateArrivee

    tt = V.chemins[chemin]+' '+moyen
    lk = F.lkV(desc[V.moyen]) if isDep else F.lkV(desc[V.moyen],False) #F.lk(V.links[V.lkChm](V.depart),V.moyen,desc[V.moyen])
    lk1 = F.lk(lk,V.date,dte) if dte else ''

    # lk1 =  F.lk(V.links[V.lkChm](V.retour),V.moyen,desc[V.moyen])
    ctrt = A.Ctrt(V.statut,'==',V.confirmer)
    ctrt.add(V.moyen,'==',moyen)
    voy = lambda dmds,req=None : render_template('depart.html',dt=dte,nb=len(dmds),V=V, F=F,titre=tt, lk=lk, tb=F.table(dmds,lk1,False,V.admDspl+[V.statut],req))
    if request.method=='GET':
        # if chemin==V.depart:
        if dte:
            ctrt.add(col,'==',F.fmtdt(dte,True))
            dmds = F.sortDf(A.getAllData(V.collDmd,ctrt))
            return voy(dmds)
        dmds = []
        return voy(dmds)

    form = dict(request.form)
    if dte:
        # ct = A.Ctrt(V.jourDeVoyage,'==',F.fmtdt(dte))
        ctrt.min(0)
        ctrt.add(V.statut,'==',V.valider)
        ctrt.add(col,'==',dte)
        ct = A.Ctrt(V.jourDeVoyage, '==' ,dte)
        ct.add(V.moyen,'==',moyen)
        lll = A.getAllData(V.collDmd,ctrt)
        ll = A.getAllData(V.collListe,ct)
        lst = len(ll) == 0
        # print(ll)
        l = len(lll)

        # print(lll)
        # ctrt.add(col,'==',F.fmtdt(dte))
        # dmds = A.getAllData
        nb = V.nbrPer[moyen]
        j = l
        liste = {}
        if lst:

            id,dt = F.crtIdDt()
            liste = {
                'id': id,
                V.date: dt,
                V.jourDeVoyage: dte,
                V.moyen: moyen,
                V.publier: V.non,
                V.chemin: V.data[V.chemin][V.depart] if isDep else V.data[V.chemin][V.retour]
            }
            # print(liste)
            res = A.saveInColl(V.collListe,liste)
            if not res: return redirect(lk1)

        lId = liste['id'] if lst else ll[0]['id']
        for i in request.form.keys():
            n = j<nb
            if moyen == V.bus:
                A.updt(V.collDmd,i,V.statut,V.valider if n else V.busAttente)
            elif n:
                A.updt(V.collDmd,i,V.statut,V.valider)
            else: return redirect(V.links[V.lkListe])
            A.updt(V.collDmd,i,V.collListe, lId)
            j += 1
        return redirect(V.links[V.lkListe])
        # return f'{form,lll}'
        # print(chemin==V.retour and moyen==V.bus)
        # if chemin==V.retour and moyen==V.bus:
            # ctrt.min()

    dte = F.fmtdt(form[V.date], True)
    # dte = 'dte'
    lk1 = F.lk(lk,V.date,dte)
    # ll = eval(ll)
    if moyen==V.bus and not A.chkLst(V.avion,dte):
            # ctrt.min()
        # ctrt.min()
        # ctrt.add(V.statut,'in',[V.confirmer,V.volAttente])
        ctrt.min()
            # ctrt.min()
            # ctrt.add(V.statut,'in',[V.confirmer,V.volAttente])

    ctrt.add(col if isDep else notCol,'==',dte)
    ctrt.add(V.lieu,'in',vDep)
    # print(col,dte)
    # if not isBus:
        # print(col,'==',dte)
    # print(V.lieu,'in',vDep)




    dmds = A.getAllData(V.collDmd,ctrt)#,col)

    # print(ctrt.field,ctrt.val,dmds)

    # if isBus:
    #     ''
    ctrt.min()
    ctrt.min()
    # ctrt.min()
    ctrt.add(notCol if isDep else col,'==',dte)

    # ctrt.add(V.lieu,'in',vDep)
    dmds1 = A.getAllData(V.collDmd,ctrt)#,col)
    print(ctrt.field,ctrt.val,dmds)
    dd = F.getVyDt(dmds1,vDep,True)
    dmds += dd
    dmds = F.sortDf(dmds,V.dateConf)
    # print(dd)
    return voy(dmds)
    # ctrt = A.Ctrt(V.moyen,'==',moyen)

    # if dte:
    #     nb = 5
    #     j = 0
    #     for i in request.form.keys():
    #         rq = 'A.updt(V.collDmd,i,V.statut,'
    #         if j<nb:
    #             rq += 'V.valider)'
    #         else: rq += 'V.busAttente'
    #         eval(rq)
    #     return redirect(V.links[V.lkListe])
    # dte = request.form(V.date)
    # ctrt.add(col,'==',dte)
    # dmds = F.sortDf(A.getAllData(V.collDmd,ctrt),V.jourDeVoyage)
    return f'{isBus,moyen,col,ll,request.form}'

@app.route(V.links[V.lkUrg], methods=['GET','POST'])
@A.allArgs
@A.chkTk
def urgence():
    cDmd = lambda msg='',rq=None: A.form('Demande',V.urg,msg,rq)
    if request.method == 'GET':
        return cDmd()
    else:
        id,dte = F.crtIdDt()
        dmd = {
            'id':id,
            V.date: dte
        }
        form = dict(request.form)
        my = form[V.moyen]
        li = form[V.lieu]
        isD = li!=V.bko
        dt = F.fmtdt(form[V.date],True)
        t = F.chkDtV(dt,my,isD)
        if not t: return cDmd('La date ne correspond pas au jour de voyage!!',form)
        del form[V.date]
        for i in form.keys():
            dmd[i] = form[i]
        col = V.dateDepart if isD else V.dateArrivee
        dmd[col] = dt
        dmd[V.dateConf] = dte
        dmd[V.statut] = V.valider
        dmd[V.raison] = V.urg

        for i in V.dmdFields:
            if i not in dmd.keys():
                dmd[i] = '--'

        ct = A.Ctrt(V.jourDeVoyage, '==' ,dt)
        ct.add(V.moyen,'==',my)
        ll = A.getAllData(V.collListe,ct)
        # isD = F.getChV()
        lst = len(ll) == 0
        dt = F.chgDate(dt)


        if lst:

            id,dt = F.crtIdDt()
            liste = {
                'id': id,
                V.date: dte,
                V.jourDeVoyage: dt,
                V.moyen: my,
                V.publier: V.non,
                V.chemin: V.data[V.chemin][V.depart] if isD else V.data[V.chemin][V.retour]
            }
            # print(liste)
            res = A.saveInColl(V.collListe,liste)
            if not res: return cDmd('Probleme, reessayer plus tard!!',form)
            # if not res: return redirect(lk1)
        dmd[V.collListe] = liste['id'] if lst else ll[0]['id']
        print(dmd)
        A.saveInColl(V.collDmd,dmd)

        chm = V.data[V.chemin]
        cm = chm[V.depart] if isD else chm[V.retour]
        lk = F.lk(V.links[V.lkListe],[V.moyen,V.date,V.chemin],[my,dt,cm])
        return redirect(lk) #f'{form,col,dt,t,dmd,isD,lk}'

@app.route(V.links[V.lkConnDmd], methods=['GET','POST'])
@A.allArgs
@A.chkTk
def conn_dmd():
    # key = V.urg if F.isAdm() else V.crtDmd
    cDmd = lambda msg='',rq=None: A.form('Demande',V.crtDmd,msg,rq)
    if request.method == 'GET':
        return cDmd()
    id,dte = F.crtIdDt()
    dmd = {
        'id':id,
        V.date: dte,
        V.dateConf: dte,
    }
    form = dict(request.form)
    # form,dmd = F.transDate(form,dmd)
    # for i in form.keys():
        # dmd[i] = form[i]

    form,dmd = F.transDate(form,dmd)
    if F.sNvo()!=V.elevee:
        c = F.chkDateV(dmd[V.dateDepart],dmd[V.dateArrivee],form[V.lieu],form[V.moyen])
        if c!=True:
            return cDmd(c)

    for i in form.keys():
        dmd[i] = form[i]
    dmd[V.nomC] = f"{F.sPrNom()} {F.sNom()}"
    dmd[V.badge] = F.sBdg()
    dmd[V.niveau] = F.sNvo()
    dmd[V.statut] = V.confirmer if F.sNvo()==V.elevee else V.attente
    dmd[V.dept] = F.sDept()
    dmd[V.ste] = F.sSte()
    nt = "*"*7
    for k in [V.numero,V.raison,V.sc,V.trainee,V.heberger]:
        dmd[k] = nt
    # dmd[V.nbrEnf] = 0
    r = A.saveInColl(V.collDmd,dmd)
    return A.panel(id,r)

    return f"{dmd,form}"

@app.route('/crt/<tp>')
@A.allArgs
@A.chkTk
def aff(tp):
    return render_template('aff.html',F=F,V=V,rs=tp=='succes')

@app.route(V.links[V.lkDmd], methods=['GET','POST'])
@A.allArgs
# @A.deAuth
def demande():
    if F.sTk(): return redirect(V.links[V.lkConnDmd])
    dTemp = lambda msg='':render_template('demande.html', V=V, F=F,msg=msg,titre=f'Demandes')
    if request.method=='GET':
        # return A.form('Dmd',V.demande)
        return dTemp()
    else:
        form = dict(request.form)
        id,dt = F.crtIdDt()
        dmd = {
            'id': id,
            'date': dt
        }

        li = form[V.lieu]
        form,dmd = F.transDate(form,dmd)

        cd = F.chkDateV(dmd[V.dateDepart],dmd[V.dateArrivee],li,form[V.moyen])
        if cd != True:
            return dTemp(cd)
        for k in form.keys():
            # if k not in V.da
            dmd[k] = form[k]
        # dmd[V.date] = F.fmtdt(dmd[V.date])
        req = 'Desolé, l\'un des champs badge, sous couvert ou stagiaire doit etre rempli!!!!'
        if dmd[V.trainee]==V.oui:
            dmd[V.sc] = '-'
            dmd[V.badge] = 'GP'
            req=True
        elif dmd[V.badge] != '':
            dmd[V.trainee] = V.non
            dmd[V.sc] = '-'
            req=True
        elif dmd[V.sc] != '':
            dmd[V.trainee] = V.non
            dmd[V.badge] = V.na
            req=True
        if req!=True: return dTemp(req)
        dmd[V.statut] = V.statuts[V.attente]
        dmd[V.niveau] = 0
        nb = int(dmd[V.nbrEnf])
        dmd[V.nbrEnf] = nb
        for k in dmd.keys():
            dmd[k] = F.rmSpc(dmd[k]) #if type(dmd[k]).__name__=='str' else dmd[k]
        r = A.saveInColl(V.collDmd,dmd)
        # st = F.getSt() #'ok' if r else 'no'

        return A.panel(id,r)

@app.route(V.links[V.lkDmdSt]+'/<id>')
@A.allArgs
def dmd(id):
    dmd = A.getData(V.collDmd,id)
    return render_template('dmdStatut.html',V=V,F=F,dmd=dmd,titre=f'Demande {id}')

@app.route(V.links[V.lkStatut], methods=['GET','POST'])
@A.allArgs
def statut():
    if request.method=='GET':
        return A.form('Statut',V.statut)
    else:
        id = request.form[V.id].lower()
        # dt = A.getData(V.collDmd,id)
        # st='ok' if dt[V.statut]==V.statuts[V.valider] else 'att' if dt[V.statut]==V.statuts[V.confirmer] else 'no'


        # msg = f"""
        #     <h1 class='text-lg'>Id: {id}</h1>
        #     Statut: {dt[V.statut]} <br/>
        # """ if dt else 'Desolee ette demande n\'existe pas!!!'

        return redirect(V.links[V.lkDmdSt]+f'/{id}')

@app.route(V.links[V.lkLgt])
@A.allArgs
def logout():
    return A.logout()

@app.route(V.links[V.lkPnl]+'/<id>/<st>')
@A.allArgs
def panel(id,st):

    msg = 'Vous pouvez suivre l\'etat de votre demande avec l\'identifiant ci dessus!!' if st=='ok' else 'Probelem!!!!!!!!!'
    return render_template('panel.html', V=V, F=F,id=id,msg=msg,st=st,titre=f'Demande {id}')

@app.route('/test')
@A.allArgs
# @A.chkTk
# @A.chkAdm
def tt():
    dds = A.getAllData(V.collDmd)#,A.Ctrt(V.statut,'==',V.valider))
    for d in dds:
        A.updt(V.collDmd,d['id'],V.statut,V.confirmer)
    # msg = 'Vous pouvez suivre l\'etat de votre demande avec l\'identifiant ci dessus!!' if st=='ok' else 'Probelem!!!!!!!!!'
    return redirect('/')#render_template('temp.html')

# git init
# git add README.md
# git commit -m "first commit"
# git remote add origin git@github.com:alexpchin/<reponame>.git
# git push -u origin master

## Pushh
# git remote add origin https://github.com/brahima24/mytrans.git
# git branch -M main
# git push -u origin main
if __name__=='__main__':

    app.debug = False
    app.run('0.0.0.0',2022)
    # serve(app,host='0.0.0.0',port=2022, threads=1)
 