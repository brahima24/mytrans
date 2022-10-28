import values as V
from time import localtime
from flask import session,url_for
import os
import numpy as np
import pandas as pd
import string
import random
import json

gs = lambda k: session.get(k)
sTk = lambda: gs(V.tk)
sEml = lambda: gs(V.email)
sNom = lambda: gs(V.nom)
sPrNom = lambda: gs(V.prenom)
sDept = lambda: gs(V.dept)
sBdg = lambda: gs(V.badge)
sRole = lambda: gs(V.role)
sNvo = lambda: gs(V.niveau)
sSte = lambda: gs(V.ste)
isAdm = lambda: sRole()==V.adm
isSprUsr = lambda: sNvo()==sRole()==V.superUsr
isBlocked = lambda user: user[V.bloque]==V.isBlocked

def lk(l,k,v):
    c = lambda l1,k1,v1: l1+f'&{k1}={v1}' if '?' in l else f'{l1}?{k1}={v1}'
    if type(k).__name__=='str':
        return c(l,k,v)
    l = c(l,k[0],v[0])
    for i in range(1,len(k)):
        l += f'&{k[i]}={v[i]}'
    return l
lkV = lambda my,isD=True: eval('lk(V.links[V.lkChm]('+('V.depart' if isD else 'V.retour')+'),V.moyen,my)')
lbl = lambda key: f'<span class="px-1 font-bold text-sm uppercase text-black font bold">{V.labels[key]}</span>'
req = lambda key: '' if key in V.notReq else 'required'
fCls = 'class="text-md text-black block px-3 py-2 w-full bg-white border-b-4 bg-gray-200 border-gray-500 shadow-md focus:bg-gray-100 focus:border-gray-700 focus:outline-none"'
dCls = 'class="p-1 w-full"'
tcCls = 'mx-2 border-2 border-gray-400'
fTtr = lambda my,chm,jVy: f"{my}_{chm}_{jVy}".replace('/','-').replace(' ','_')

nTtr = lambda my, chm, jVy: fTtr(my,chm,jVy)+'.xlsx'
lsPth = os.path.join(os.path.dirname(__file__),'static','liste')
fPth = lambda my, chm, jVy: os.path.join(lsPth,nTtr(my,chm,jVy))

getCls = lambda cl: cl[7:-1]
getChV = lambda chm : V.dateDepart if chm==V.data[V.chemin][V.depart] else V.dateArrivee
getSt = lambda r: 'ok' if r else 'no'

def rdJSON(nm):
    fn = V.filesDir+nm
    try:
        if os.path.exists(fn):
            print('Miammmm')
            with open(fn) as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(str(e),'__Read_JSONNN__')
        return {}

def saveJSON(nm,doc):
    fn = V.filesDir+nm
    try:
        if os.path.exists(fn):
            with open(fn,'w') as f:
                json.dump(doc,f)
                return True
        return False
    except:
        return False

def saveDept(nm):
    try:
        fn = 'depts.json'
        dc = rdJSON(fn)
        if nm in dc.keys():
            return None
        dc[nm]=nm
        saveJSON(fn,dc)
        return True
    except Exception as e:
        print(str(e),'__Saveee_JSONNN__')
        return False
    
def crtHist(email=None,raison=''):
    email = email if email else sTk()
    idd,dt = crtIdDt()
    idd1 = crtIdDt()
    idd2 = crtIdDt()
    return {
        'id': dt[:4]+idd+idd1[0]+idd2[0],
        V.date: dt,
        V.email: email,
        V.raison: raison
    }

mfrm = lambda x,k: """
<div x-show='xxxxxx' class="w-full bg-opacity-50 h-full fixed block top-0 left-0 bg-white z-50">
    <div class='text-right w-1/3 mx-auto'>
        <button class='font-bold text-2xl' @click='xxxxxx=false'>
        X
        </button>
    </div>
</div>
""".replace('xxxxxx',x).replace('yyyyyyy',Form(k))

def mnu_lk():
    dct = {
        'Creer un utilisateur / Create user':V.links[V.lkCrtUsr],
        'Ajouter un departement / Add department':V.links[V.lkAddDept]
    }
    m = ''
    for i in dct.keys():
        m += f'''
        <div class="flex flex-col bg-opacity-75 text-white font-bold justify-between md:w-1/3 w-full p-4 mt-4 rounded-lg md:flex-row md:space-x-8 md:mt-0 md:text-sm md:font-medium md:border-0 dark:bg-gray-800 md:dark:bg-gray-900 dark:border-gray-700">
            <div>
            <a href='{dct[i]}' class="block py-2 pr-4 pl-3 text-gray-700 rounded hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 md:p-0 md:dark:hover:text-white dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent dark:border-gray-700">
                {i}
            </a>
          </div>
        </div>
    '''
    return m

def getVyDt(df,vl,isVol=False):
    if len(df)==0: return []
    # print(df)
    # print(vl)
    df = pd.DataFrame(df)
    # print(df)
    df = df[~df[V.lieu].isin(vl)]
    # df = eval(f'df[{"~" if isVol else ""}df[V.lieu].isin(vl)]')
    # print(df,'llllllllll')
    return df.to_dict('records')
    return []

def btnAdm(my):
    isDep = True if my==V.chemins[V.depart] else False
    # print()
    btn = """
          <div @click.away="open = false" class="relative" x-data="{ open: false }">
            <button @click="open = !open" class="uppercase block py-2 pr-4 pl-3 text-gray-700 rounded hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 md:p-0 md:dark:hover:text-white dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent dark:border-gray-700">
            """
    btn += my
    btn += """

            </button>
            <div x-show="open" x-transition:enter="transition ease-out duration-100"
                x-transition:enter-start="transform opacity-0 scale-95"
                x-transition:enter-end="transform opacity-100 scale-100"
                x-transition:leave="transition ease-in duration-75"
                x-transition:leave-start="transform opacity-100 scale-100"
                x-transition:leave-end="transform opacity-0 scale-95"
                class="absolute origin-top-left left-0 md:right-0 w-full mt-2 md:origin-top-right rounded-md shadow-lg md:w-48">
                <div class="py-2 bg-white text-blue-800 text-sm rounded-sm border border-main-color shadow-sm">


                 <ul class="py-1" aria-labelledby="dropdown">
                    <li>
                    <a class="block px-4 py-2 mt-2 text-sm bg-white md:mt-0 focus:text-gray-900 hover:bg-indigo-100 focus:bg-gray-200 focus:outline-none focus:shadow-outline"
                        href="
            """

    btn += lkV(V.bus,isDep)+f"\">{V.bus}"

    btn += """</a></li>
                    <li>
                    <a class="block px-4 py-2 mt-2 text-sm bg-white md:mt-0 focus:text-gray-900 hover:bg-indigo-100 focus:bg-gray-200 focus:outline-none focus:shadow-outline"
                        href="
            """
    # print(l,k,v,'-'*5)
    btn += lkV(V.avion,isDep)+" \"> "
    btn += V.avion+"""
            </a></li>
                </ul>
                </div>
            </div>
        </div>
            """
    # print(btn)
    return btn

def sortDf(ds,col,isL=False,pub=False):
    if len(ds)!=0:
        df = pd.DataFrame(ds)
        df[col] = pd.to_datetime(df[col],format='%Y/%m/%d %H:%M:%S')
        df= df.sort_values(col)
        if isL:
            vD = df[df[V.statut]==V.valider]
            vA = df[df[V.statut]==V.busAttente]
            df = pd.concat([vD,vA])
            df[V.no] = list(range(1,df.shape[0]+1))
            if pub!=False:
                ddf = df[V.trsDspl]
                pth = os.path.join(os.path.dirname(__file__),'static','liste',pub+'.xlsx')
                # print(rf'{pth}','*'*10)
                ddf.to_excel(pth,index=False)
        return df.to_dict('records')
    return []

def fmtdt(dt, isEng=False):

    try:
        x = dt.split(' ')
        # print(x,dt)
        if len(x)==2 or isEng:
            x = x[0].split('-') if isEng else x[0].split('/')
            # print(x,'ppppppp')
            dt = f'{x[2]}/{x[1]}/{x[0]}'
        else: dt = dt
        # return dt
        x=dt.split('/')
        # print(x)
        if(len(x)==3):
            jr = f'0{x[0]}' if len(x[0])==1 else x[0]
            mois = f'0{x[1]}' if len(x[1])==1 else x[1]
            an = f'20{x[2]}' if len(x[2])==2 else x[2]
            return f'{jr}/{mois}/{an}'
        return dt
    except: return False

def transDate(form,dmd):

    for i in V.dmdDate:
        d = [i+'_jr',i+'_mois',i+'_an']
        if d[0] in form.keys():
            dmd[i] = ''
            for j in d:
                dmd[i] += form[j]+"/"
                del form[j]
            # if F.chkDateV()
            dmd[i] = fmtdt(dmd[i][:-1])
            dmd[i]
    return form,dmd

banner = lambda msg: """
<div x-data="{bt:'{msg}' !== ''?true:false}" x-show="bt" class="fixed top-28 right-0 w-full md:bottom-8 md:right-12 md:w-auto z-60">
    <div class="bg-red-500 font-bold text-gray-100 text-sm p-3 md:rounded shadow-lg flex justify-between">
      <div>👉 {msg}</div>
      <button class="text-slate-500 hover:text-slate-400 ml-5" @click="bt=!bt">
        <span class="sr-only">Close</span>
        <svg class="w-4 h-4 shrink-0 fill-current" viewBox="0 0 16 16">
          <path d="M12.72 3.293a1 1 0 00-1.415 0L8.012 6.586 4.72 3.293a1 1 0 00-1.414 1.414L6.598 8l-3.293 3.293a1 1 0 101.414 1.414l3.293-3.293 3.293 3.293a1 1 0 001.414-1.414L9.426 8l3.293-3.293a1 1 0 000-1.414z" />
        </svg>
      </button>
    </div>
  </div>
""".replace('{msg}',msg)

td = lambda vl: f"""<td class="{tcCls}">{vl}</td>"""
th = lambda vl: f"""<th class="{tcCls}">{vl}</th>"""
tr = lambda ct: f"""<tr class="w-full">{ct}</tr>"""

def minTab(flds,lst):
    
    mth,mtb = '',''
    
    for i in flds:
        mth += th(i)
    
    for i in lst:
        mtd = ''
        for j in flds:
            mtd += td(i[j] if j in i.keys() else '')
        mtb += tr(mtd)
        
    return f"""
        <div class="overflow-x-auto">
            <table class="table-auto overflow-y-auto w-full uppercase">
                <thead class="bg-gray-800 text-center py-2 text-gray-200 w-full ">
                    {tr(mth)}
                </thead>
                <tbody class="bg-grey-light text-center overflow-y-scroll w-full">
                    {mtb}
                </tbody>
            </table>
        </div> 
"""

def table(dmds,lnk,val,ttr=None,isL=None,tr=None):
    nb = len(dmds)
    bt = ''
    tt = tr if tr else 'Il n\'y a pas de demande!!'
    tb =''
    xdt = ''
    if nb!=0:
        tt = tr if tr else f'Il y\'a {nb} demandes!'
        bt = f"""
            <div class="w-1/2 flex justify-end">
                <button class="p-1 bg-gray-400 text-gray-100 rounded-lg hover:bg-gray-500" type="submit">
                {'Publier' if isL else ('Valider' if isL is None else 'Confirmer')}
                </button>
            </div>
            """ if not val else ""
        ttr = ttr if ttr else V.admDspl if isAdm() else V.usrDspl
        tb = """
        <div class="overflow-x-auto">
	<table class="table-auto overflow-y-auto w-full uppercase">
		<thead class="bg-gray-800 text-center py-2 text-gray-200 w-full ">
			<tr class="w-full">
              """
        tb += th('Modifier')+th('Telecharger') if isL else ''

        for t in ttr:

            tb += th(t)

        cTd = th('') if not val else ''

        tb += cTd+th('Miamm') + """ </tr>
            </thead>
		<tbody class="bg-grey-light text-center overflow-y-scroll w-full">
            """
        for dmd in dmds:
            nid = f'a{dmd["id"]}'
            xdt += f'{nid}: false,'
            
            tb += f"""
              <tr class='w-full' @mouseleave="{nid} = false" >
            """
            if isL :
                my,jv,chm = dmd[V.moyen],dmd[V.jourDeVoyage],dmd[V.chemin]

                tr = nTtr(my,chm,jv)
                dwnld = f"""

                <a href='{url_for('static',filename='liste/'+tr)}'>
                    <i class='fa fa-download'></i>
                </a>

                """ if tr in os.listdir(lsPth) else ''
                ll = f'''
                <a href='{lk(V.links[V.lkListe],['id'],[dmd['id']])}'>
                    <i class='fa fa-edit'></i>
                </a>
                '''
                tb += td(ll)+td(dwnld)
            
            # [V.moyen,V.date,V.chemin],[my,jv,chm]
            for t in ttr:
                tb += td(dmd[t] if t in dmd.keys() else '')
            # x = 's' in dmd[V.nomC]
            ckd = 'checked' if (V.publier in dmd.keys() and dmd[V.publier]==V.oui) or (V.statut in dmd.keys() and dmd[V.statut] in [V.valider,V.busAttente]) else ''# and dmd[V.publier]!='Non'
            cTd = f"""<input type="checkbox"  @click="ch" {ckd} name="{dmd['id']}" />
                """ if not val else ''
            cc = f'<span x-show="{nid}"> Okk </span>'
            tb += td(cTd)+td(cc)+"</tr>"

        tb += """
                        </tbody>
                </table>
            </div>
        """
    sl = """
    <span  x-text='`Nombres selectionnes: ${nb}`'></span>
    """ if nb!=0 else ''
    ctt = f"""
    <div class='w-5/6 h-screen px-2' x-data="{'{'+xdt+'}'}" >
    """
    ctt += f"""
        <form
            action="{lnk}" method="post" enctype="multipart/form-data"
            class="m-1 md:m-3 col-span-full w-full xl:col-span-8 bg-gray-100 shadow-lg rounded-lg border border-gray-200">

            <header class="px-5 sticky py-4 border-b border-slate-100">
                <div class="flex flex-wrap">
                    <div class="w-1/2 flex justify-start">
                        <h2 class="font-semibold text-slate-800">{tt}</h2>
                    </div>
                        {bt}
                </div>
                {sl}
            </header>
      {tb}
    """
    return ctt + "</form></div>"

def crtIdDt():

    t = localtime()
    dt=''
    for i in range(3):
        dt += str(t[i])+'/'
    dt = dt[:-1]+' '
    for i in range(3,6):
        dt += str(t[i])+':'
    dt = dt[:-1]
    id = str(int(np.random.rand()*10000))
    lt = ''.join(random.choice(string.ascii_lowercase) for i in range(2))
    id = list(id+lt)
    random.shuffle(id)
    id = ''.join(i for i in id)

    return id,dt

def chgDate(dt):
    try: dt = pd.to_datetime(dt,format='%d/%m/%Y')
    except: dt=False
    return dt

def rmSpc(vl):
    val = ''
    vl = vl.strip()
    vl = vl.split('  ')
    if len(vl)==0: return vl[0]
    for i in vl:
        val += i.strip()+' ' if i!='' else ''
    return val[:-1]

def chkDtV(dt,my,isDep=True):
    isBus = True if my==V.bus else False
    dt = chgDate(dt)
    if dt:
        lst = (V.bus_depart if isDep else V.bus_retour) if isBus else V.vol
        # print(dt.weekday(), lst)
        return dt.weekday() in lst
    return dt

def chkDateV(dt1,dt2,li,myn):
    msg1 = 'Le delai d\'une semaine avant le depot n\'est pas respecter!!!'
    msg = 'Desolé les dates entrées ne correspondes pas au jour de voyage!!!'
    id,dt = crtIdDt()
    dt = pd.to_datetime(dt)

    dt1 = chgDate(dt1)
    dt2 = chgDate(dt2)
    if dt1:
        j1 = dt1.weekday()
        c1 = (dt1-dt).days
        if c1<5: return msg1
        # print(c.days)
        if dt2:
            j2 = dt2.weekday()
            c2 = (dt2-dt).days
            if c2<7: return msg1
            if myn==V.avion:
                if j1 in V.vol:# and j2 in V.vol:
                    return True
                return msg

            if li==V.bko and j1 in V.bus_retour and j2 in V.bus_depart:
                return True
            elif li in [V.gkto,V.loulo] and j1 in V.bus_depart and j2 in V.bus_retour:
                return True
            return msg
        if myn==V.avion:
            if j1 in V.vol:
                return True
            return msg
        if li==V.bko and j1 in V.bus_retour:
            return True
        elif li in [V.gkto,V.loulo] and j1 in V.bus_depart:
            return True
        return msg

    return msg

cht1 = lambda lbl1,c1Dt1,c1Dt2: """

                <div class="w-full md:w-1/2 p-3">
                    <!--Graph Card-->
                    <div class="bg-gray-900 border border-gray-800 rounded shadow">
                        <div class="border-b border-gray-800 p-3">
                            <h5 class="font-bold uppercase text-gray-600">Graph</h5>
                        </div>
                        <div class="p-5">
                            <canvas id="chartjs-0" class="chartjs" width="undefined" height="undefined"></canvas>
                            <script>
                                new Chart(document.getElementById("chartjs-0"), {
                                    "type": "line",
                                    "data": {
                                        "labels": {lbl1},
                                        "datasets": [{
                                            "label": "Views",
                                            "data": {c1Dt1} ,
                                            "fill": false,
                                            "borderColor": "rgb(75, 192, 192)",
                                            "lineTension": 0.1
                                        },{
                                            "label": "PPPP",
                                            "data": {c1Dt2},
                                            "fill": false,
                                            "borderColor": "rgb(90, 90, 92)",
                                            "lineTension": 0.1
                                        }]
                                    },
                                    "options": {}
                                });
                            </script>
                        </div>
                    </div>
                    <!--/Graph Card-->
                </div>
""".replace('{lbl1}',str(lbl1)).replace('{c1Dt1}',str(c1Dt1)).replace('{c1Dt2}',str(c1Dt2))

cht2 = lambda lbl2,c2Dt1,c2Dt2: """

                <div class="w-full md:w-1/2 p-3">
                    <!--Graph Card-->
                    <div class="bg-gray-900 border border-gray-800 rounded shadow">
                        <div class="border-b border-gray-800 p-3">
                            <h5 class="font-bold uppercase text-gray-600">Graph</h5>
                        </div>
                        <div class="p-5">
                            <canvas id="chartjs-1" class="chartjs" width="undefined" height="undefined"></canvas>
                            <script>
                                new Chart(document.getElementById("chartjs-1"), {
                                    "type": "bar",
                                    "data": {
                                        "labels": {lbl2},
                                        "datasets": [{
                                            "label": "Likes",
                                            "data": {c2Dt1},
                                            "fill": false,
                                            "backgroundColor": ["rgba(255, 99, 132, 0.2)", "rgba(255, 159, 64, 0.2)", "rgba(255, 205, 86, 0.2)", "rgba(75, 192, 192, 0.2)", "rgba(54, 162, 235, 0.2)", "rgba(153, 102, 255, 0.2)", "rgba(201, 203, 207, 0.2)"],
                                            "borderColor": ["rgb(255, 99, 132)", "rgb(255, 159, 64)", "rgb(255, 205, 86)", "rgb(75, 192, 192)", "rgb(54, 162, 235)", "rgb(153, 102, 255)", "rgb(201, 203, 207)"],
                                            "borderWidth": 1
                                        },{
                                            "label": "Likes",
                                            "data": {c2Dt2},
                                            "fill": false,
                                            "backgroundColor": ["rgba(255, 99, 132, 0.2)", "rgba(255, 159, 64, 0.2)", "rgba(255, 205, 86, 0.2)", "rgba(75, 192, 192, 0.2)", "rgba(54, 162, 235, 0.2)", "rgba(153, 102, 255, 0.2)", "rgba(201, 203, 207, 0.2)"],
                                            "borderColor": ["rgb(255, 99, 132)", "rgb(255, 159, 64)", "rgb(255, 205, 86)", "rgb(75, 192, 192)", "rgb(54, 162, 235)", "rgb(153, 102, 255)", "rgb(201, 203, 207)"],
                                            "borderWidth": 1
                                        }]
                                    },
                                    "options": {
                                        "scales": {
                                            "yAxes": [{
                                                "ticks": {
                                                    "beginAtZero": true
                                                }
                                            }]
                                        }
                                    }
                                });
                            </script>
                        </div>
                    </div>
                    <!--/Graph Card-->
                </div>
""".replace('{lbl2}',str(lbl2)).replace('{c2Dt1}',str(c2Dt1)).replace('{c2Dt2}',str(c2Dt2))

transConfF = lambda action,id: f"""

            <form method="post" enctype="multipart/form-data" action="/{action}/{id}">
                <span class="px-1 text-base text-gray-300 font-bold">Votre mot de passe</span>
                <input type="password" name="pwd" required class="text-md text-black block px-2 py-1 rounded-lg
                    bg-gray-300 border-2 border-gray-300 placeholder-gray-600 lg:w-1/3
                    shadow-md focus:placeholder-gray-500 focus:bg-white focus:border-gray-600 focus:outline-none">


                <button type="submit" class="text-white bg-blue-500 hover:bg-blu-700 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-2 py-1 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
                {action.capitalize()}
                </button>
            </form>
"""

mod = lambda md: f'x-model="{md}"' if md else ''

chTxt = lambda key,val='', md=None : f"""
    <div {dCls} >
        {lbl(key)}
        <input type="text" {mod(md)} value="{val}" {req(key)} name="{key}" {fCls} />
    </div>

"""

chNbr = lambda key,val='', md=None : f"""
    <div {dCls} />
        {lbl(key)}
        <input type="number" {mod(md)} value="{val}" {req(key)} name="{key}"
            {fCls} />
    </div>
"""

chPwd = lambda key: f"""
    <div {dCls}>
        {lbl(key)}
        <input type="password" {req(key)} name="{key}" minlength="6"
                {fCls} />
    </div>

    """

chEml = lambda key,val='' : f"""
    <div {dCls}>
        {lbl(key)}
        <input type="email" name="{key}"  value="{val}" {req(key)}
               {fCls} />
    </div>

    """

def chSel(key,data={},md=None):
    
    
    el = {}
    sel = f"""
            <div {dCls}>
            {lbl(key)}
                <select name="{key}" {req(key)} {mod(md)}
                        {fCls}>
                    <option hidden selected></option>
            """
    el = rdJSON('depts.json') if key==V.dept else V.data[key] if key else data
    
    # if key==V.dept:
    #     el = rdJSON('depts.json')
    
    ks = el.keys()
    if len(ks)!=0:
        for k in ks:
            sel += f"""
            <option key='{k}' value='{k}'>{el[k]}</option>
            """

    sel += '</select></div>'
    return sel

def chAg():
    temp = f"""

    {chNbr(V.nbrEnf,md='nbrEnf')}

        <div x-show="Number(nbrEnf)!=0" class="p-1 w-full">
    """
    temp += f"""
    <template x-for="i in Number(nbrEnf)">
                <div class=" w-full ml-3 p-1">
                    <span x-text="'Enfant '+String(i)"></span>
                    <div class="flex flex-wrap w-full p-1">
                        <!-- <div class="w-3/4">
                            <span>Nom Complet</span>
                        </div>
                        <div class="w-1/4">
                            <span>Age</span>
                        </div>
                        <div class="w-3/4">
                            <input type="text" x-bind:name="'enf'+String(i)" />
                        </div>
                        <div class="w-1/4">
                            <input type="number" x-bind:name="'age'+String(i)" />
                        </div> -->
                        <div class="w-3/4">
                            <div {dCls} >
                                Nom:
                                <input type="text" {fCls} required x-bind:name="'nom_enfant_'+String(i)" >
                            </div>
                        </div>

                        <div class="w-1/4">
    """
    sel = f"""
            <div {dCls}>
            Age
                <select x-bind:name="'age_enfant_'+String(i)" required
                        {fCls}>
                    <option hidden selected>Cliquez</option>
            """
    el = V.data[V.age]
    for k in el.keys():
        sel += f"""
        <option key='{k}' value='{k}'>{el[k]}</option>
        """

    sel += '</select></div>'

    temp += f"""
                    {sel}
                        </div>
                    </div>
                </div>
            </template>
        </div>

    """
    return temp

def chDate(cn=False):
    k = V.dateDepart
    j = V.dateArrivee
    lbl1 = 'Depart' if cn else f"""
    <span class="w-full" x-text="lieu+'-'+(lieu==='{V.bko}'?'{V.loulo}':'{V.bko}')" ></span>
    """
    lbl2 = 'Retour' if cn else f"""
    <span class="w-full" x-text="(lieu==='{V.bko}'?'{V.loulo}':'{V.bko}')+'-'+lieu" ></span>
    """

    dt = f"""
    <div {'' if cn else'x-show="lieu"'} class="pt-3 w-full flex flex-wrap">
        <div class="w-full bg-gray-200 py-2">
            Date du voyage (Date of tavel)
        </div>
        <div class='flex flex-wrap w-full my-1'>

            <div class="w-2/5"></div>
            <div class="w-1/5">Jour</div>
            <div class="w-1/5">Mois</div>
            <div class="w-1/5">Année</div>
        </div>
        <div class='flex flex-wrap w-full my-1'>
            <div class="w-2/5">

                {lbl1}
            </div>
            <div class="w-1/5">
                <input type="number" class='w-10 border-2 bg-gray-100' min='1' max="31" required name="{k}_jr"  >
            </div>
            <div class="w-1/5">
                <input type="number" class='w-10 border-2 bg-gray-100' min='1' max="31" required name="{k}_mois"  >
            </div>
            <div class="w-1/5">
                <input type="number" class='w-14 border-2 bg-gray-100' required name="{k}_an"  >
            </div>
        </div>
        <div class='flex flex-wrap w-full my-1'>
            <div class="w-2/5">

                {lbl2}
            </div>
            <div class="w-1/5">
                <input type="number" class='w-10 border-2 bg-gray-100' min='1' max="31"  name="{j}_jr"  >
            </div>
            <div class="w-1/5">
                <input type="number" class='w-10 border-2 bg-gray-100' min='1' max="31"  name="{j}_mois"  >
            </div>
            <div class="w-1/5">
                <input type="number" class='w-14 border-2 bg-gray-100' name="{j}_an"  >
            </div>
        </div>
    </div>
        """

    return dt

chImg = lambda key: f"""
    <div class="py-1 w-full">
        {lbl(key)}
        <input type="file" name="{key}" {'required' if key==V.icn else ''} />
    </div>
"""

chSDt= lambda val='': f"""
    <div class="py-1 w-full">
        {lbl(V.date)}
        <input type="date" value="{val}" name="{V.date}" {req(V.sDt)} {fCls} />
    </div>
"""

usrMenu = lambda nom,eml,init : """

            <div @click.away="open = false" class="relative" x-data="{ open: false }">
                <button @click="open = !open"
                    class="flex flex-row rounded-full items-center w-10 h-10 text-2xl font-bold text-center bg-transparent md:inline focus:bg-blue-300 border-2 focus:shadow-outline">
                    ###
                </button>
                <div x-show="open" x-transition:enter="transition ease-out duration-100"
                    x-transition:enter-start="transform opacity-0 scale-95"
                    x-transition:enter-end="transform opacity-100 scale-100"
                    x-transition:leave="transition ease-in duration-75"
                    x-transition:leave-start="transform opacity-100 scale-100"
                    x-transition:leave-end="transform opacity-0 scale-95"
                    class="absolute right-0 w-full mt-2 origin-top-right rounded-md shadow-lg md:w-48">
                    <div class="py-2 bg-white text-blue-800 text-sm rounded-sm border border-main-color shadow-sm">
                     <div class="py-3 px-4">
                        <span class="block text-sm text-gray-900 dark:text-white"> {} </span>
                        <span class="block text-sm font-medium text-gray-500 truncate dark:text-gray-400"> *** </span>
                    </div>
                        <div class="border-b"></div>

                     <ul class="py-1" aria-labelledby="dropdown">
                        <li>
                            <a class="block px-4 py-2 mt-2 text-sm bg-white md:mt-0 focus:text-gray-900 hover:bg-indigo-100 focus:bg-gray-200 focus:outline-none focus:shadow-outline"
                                href="/logout">
                                Deconnexion
                            </a>
                        </li>
                    </ul>
                    </div>
                </div>
            </div>
        """.replace('{}',nom).replace('***',eml).replace('###',init)

dfltMenu = """
        <a href="/login">
          <button
            id="navAction"
            class="mx-auto lg:mx-0 hover:underline bg-white text-gray-800 font-bold rounded-full mt-4 lg:mt-0 py-4 px-8 shadow opacity-75 focus:outline-none focus:shadow-outline transform transition hover:scale-105 duration-300 ease-in-out"
          >Se connecter
          </button>
        </a>
"""

panelPage = lambda key,mt='',email='': f"""
    <div class="pt-24">
        <div class="container px-3 mx-auto flex flex-wrap flex-col md:flex-row items-center">

<section class="bg-white border-b py-8 mx-auto">
    <div class="container max-w-5xl mx-auto m-8">
        <h1 class="w-full my-2 text-5xl font-bold leading-tight text-center text-gray-800">
        {V.messages(mt,email)[key][V.title]}
        </h1>
        <div class="w-full mb-4">
        <div class="h-1 mx-auto gradient w-64 opacity-25 my-0 py-0 rounded-t"></div>
        </div>
        <div class="flex flex-wrap">
        <div class="w-5/6 sm:w-1/2 p-6">
            <h3 class="text-3xl text-gray-800 font-bold leading-none mb-3">
            {V.messages(mt,email)[key][V.subtitle]}
            </h3>
            <p class="text-gray-600 mb-8">
            {V.messages(mt,email)[key][V.msg]}
                <br />
                <br />
            </p>
        </div>
        </div>
    </div>
    </section>
    </div></div>
"""

pnl = lambda val,title : f"""
<div class="bg-white shadow rounded-lg p-4 sm:p-6 xl:p-8 ">
    <div class="flex items-center">
        <div class="flex-shrink-0">
        <span class="text-2xl sm:text-3xl leading-none font-bold text-gray-900">{val}</span>
        <h3 class="text-base font-normal text-gray-500">{title}</h3>
        </div>
    </div>
</div>
"""

Msg = lambda m: f"""
    <div class="text-base text-red-800">{m}</div>
"""

menu = lambda : usrMenu(f"{gs(V.prenom)} {gs(V.nom)}",gs(V.email),f"{gs(V.prenom)[0]}{gs(V.nom)[0]}".upper()) if gs(V.tk) else dfltMenu

def MiniField(key,val=''):
    try:
        if key in V.textType:
            return chTxt(key,val,)
        elif key in V.pwdType:
            return chPwd(key)
        elif key == V.email:
            return chEml(key,val)
        elif key == V.nbrEnf:
            return chAg()
        elif key in V.nbrType:
            return chNbr(key,val)
        elif key in V.slctType:
            return chSel(key,md=key)
        elif key == V.date:
            return chDate()
        elif key==V.sDt:
            return chSDt(val)
        # elif key in [V.image,V.icn]:
        #     return chImg(key)
    except Exception as e:
        print(str(e))
        return ''
# os.p
titleP = lambda ttr: f"""
<div class="text-center font-semibold text-black pb-12">
    {ttr}
</div>
"""

btn = lambda bt: f"""
<button type='submit' class="mt-5 w-full text-lg uppercase font-semibold bg-gray-800 text-white rounded-lg px-6 py-3 block shadow-xl hover:text-white hover:bg-black">
    {bt}
</button>
"""

def Form(key,msg='',rq=None,oob=''):
    try:
        vals = V.formInfos[key]
        if key==V.rstPwd:
            vals = vals(oob)
        lk = vals[V.lk]
        # print(rq,'mm'*12)
            
        fields,fD = '',''
        r = ",rq[k])" if rq else ')'
        # print(r)
        for k in vals[V.field]:
            # print(k)
            fields += eval("MiniField(k"+ r)
        return f"""
                    <div  class="py-5 rounded w-full p-5 md:w-2/3 xl:w-2/5 mx-auto flex flex-wrap flex-col md:flex-row bg-gray-100 bg-opacity-25 justify-center items-center">
                        {banner(msg)}
                        <form {fD} action="{lk}" method="post" enctype="multipart/form-data" class="flex w-full flex-col md:w-4/5 justify-center items-start md:text-left items-center">
                            {titleP(vals[V.titre])}
                            {fields}
                            {btn(vals[V.lbl])}
                        </form>
                    </div>

                """
    except Exception as e:
        print(str(e))
        return 'Probleme veuillez reesayer'
