from flask import request
lkCrtUsr = 'lkCrtUsr'
mytrans = 'myTrans'
lkDmd = 'demande'
lkStatut = 'statut'
lkListe = 'liste'
login = 'login'
titre = 'titre'
sTitre = 'sous_titre'
field = 'field'
email = 'email'
lbl = 'label'
lk = 'link'
isReg = 'isReg'
password = 'password'
prenom = 'prenom'
nom = 'nom'
dept = 'departement'
costCode = 'costCode'
depart = 'depart'
arrive = 'arrive'
dateDepart = 'date_depart'
dateArrivee = 'date_retour'
hod = 'chef_departement'
demande = 'demande'
statut = 'statut'
id = 'id'
badge = 'badge'
tk = '__transport__authorisation__token__'
collUser = 'user'
collDmd = 'demande'
collConf = 'confirmer'
collVld = 'valider'
role = 'role'
lkConn = 'conn'
lkLgt = 'logout'
trainee = 'trainee'
numero = 'numero'
sc = 'sous_couvert'
ste = 'societe'
loulo = 'Loulo'
gkto = 'Gounkoto'
bko = 'Bamako'
sousTrai = 'Sous Traitant'
nbrEnf = 'nombre_enfant'
jour = 'jour'
mois = 'mois'
annee = 'annee'
moyen = 'moyen'
bus = 'BUS'
avion = 'VOL / FLY'
lieu = 'lieu'
raison = 'raison'
heberger = 'heberger'
lkPnl = 'panel'
attente = "En attente d\'approbation/ Awaiting approval"
confirmer = "Approuvé/ Approved"
valider = 'Validé/ Valid'
niveau = 'niveau'
lkConf = 'lkConf'
lkDmdSt = 'dmd_staut'
nbrPlace = 'nombre_de_place'
crtUser = 'create_user'
nomC = 'nom_complet'
usr = 0
adm = 1
lkVal = 'valider'
lkConnDmd = 'conn_dmd'
crtDmd = 'create_demande'
date = 'date'
lkDep = 'depart'
lkRet = 'retour'
mode = 'mode'
oobCode = 'oobCode'
apiKey = 'apiKey'
lang = 'lang'
collListe = 'liste'
age = 'age'
dateConf = 'date_confirmation'
busAttente = 'Liste d\'attente'
jourDeVoyage = 'jour_de_voyage'
lkListe = 'listes'
publier = 'publier'
chemin = 'chemin'
lkListDisp = 'liste_disponible'
retour = 'retour'
lkVoy = 'voyage'
lkChm = 'chemin'
urg = 'Urgence'
sDt = 'simple_date'
oui = 'Oui'
non = 'Non'
na = 'NA'
no = 'Numero'
volAttente = 'En attente de vol'
faible = 1
interm = 2
elevee = 3
lkUrg = 'urgence'
somilo = 'SOMILO'
gktoSA = 'Gounkoto S.A.'
nb_tent = 'nb_tentative'
bloque = 'bloque'
maxTentative = 4
isBlocked = 1
notBlocked = 0
filesDir = 'static/files/'
fileDepts = 'depts.json'
lkSpUsr='sprusr'
collLog = 'log'
resultat = 'resultat'
conn = 'connexion'
abrev = 'abreviation'
fbaseDsbld = 'TOO_MANY_ATTEMPTS_TRY_LATER'
pwdIncorr = 'INVALID_PASSWORD'
emlNotFound = 'EMAIL_NOT_FOUND'
accBlocked = 'ACCOUNT_BLOQUED'
limitTent = 'LIMIT_TENTATIVE'
cntd = 'CONNECTED'
emlExist = 'EMAIL_EXIST'
invOob = 'INVALID_OOB_CODE'
rstRai = 'RESET_PASSWORD'
failure = 'FAILURE'
success = 'SUCESS'
deptNm = 'nom'
modifDate = 'modif_date'
lkRstPwd = 'resetPassword'
rstPwd = 'resetPwd'
pwdConf = 'pwdConf'
lkAdd = 'add'
confPar = 'confirmer_par'
valPar = 'valider_par'
creePar = 'creer_par'
statuts = {
    valider: valider,
    confirmer: confirmer,
    attente: attente,
    busAttente: busAttente,
    volAttente:volAttente,
}
sttCls = {
    valider: 'green-200',
    confirmer: 'yellow-200',
    attente: 'blue-200',
    # attente: 'blue-200',
}
labels = {
    abrev: 'Abreviation',
    moyen: 'Moyen de transport / Means of transport',
    nbrEnf: 'Nombre d\'enfant / Number of child',
    ste: 'Société / Company',
    email: 'Email',
    numero:'Numero de telephone / Cell Phone',
    password: 'Mot de passe / Password',
    pwdConf: 'Confirmez le mot de passe / Confirm password',
    prenom: 'Prenom / Fist name',
    nom:'Nom / Last name',
    nomC: 'Noms & Prénoms / Names & Surnames',
    dept: 'Département / Department',
    costCode: 'Cost code',
    id: 'Identifiant de votre demande / Request Id',
    badge: 'Numéro de badge / Badge number',
    trainee: 'Stagiaire / Trainee',
    sc:'Sous couvert / Under Cover',
    lieu:'Lieu de depart / departure',
    raison: 'Raison du voyage / Travel Raison',
    heberger: 'A héberger? / To host where?',
    nbrPlace: 'Nombre de place / Number of place',
    niveau: 'Niveau d\'acces / Acces level',
    role: 'Role de l\'utilsateur / User\'s role',
    date: 'Date'

}
links = {
    lkRstPwd : '/resetPassword',
    lkCrtUsr: '/crtUsr',
    lkConnDmd: '/usrDmd',
    lkDmd: '/demander',
    lkListe: '/listes',
    lkStatut: '/statut',
    login: '/login',
    lkConn: '/demandes',
    lkLgt: '/logout',
    lkPnl: '/panel',
    lkConf: lambda st: '/confirmer' if st==attente else '/valider',
    lkDmdSt: '/demande',
    lkVoy:'/voyage',
    lkChm: lambda l: f'/voyage/{l}',
    lkAdd: '/addDept',
    # lkDep: f'/voyage/{depart}',
    # lkRet: f'/{retour}',
    lkListDisp: '/liste',
    lkUrg: '/urgence',
    lkSpUsr: lambda l='':'/superuser/'+l 
}
fmtFrm = lambda tt,fld,lb,l :{
        titre: tt,
        field: fld,
        lbl: lb,
        lk: l
    }
rsLk = lambda vl: links[lkRstPwd]+ f'?{oobCode}={vl}' if vl else ''
formInfos = {
    rstPwd: lambda vl: fmtFrm('Reinitialisation de mote de passe / Resetting password', [password,pwdConf],'Confirmez / Confirm',rsLk(vl)),
    dept: fmtFrm('Ajout d\'un nouveau departemt / Adding new department',[deptNm],'Ajouter/Add','#'),
    login: {
        titre: '',
        field: [email,password],
        lbl: 'Se connecter / Sign in',
        lk: links[login]
    },
    demande: {
        titre: 'Demande de transport / Travel request',
        field: [prenom,nom,dept,badge,costCode,trainee],
        lbl: 'Demander / Request',
        lk: links[lkDmd]
    },
    statut:{
        titre: 'Statut d\'une demande / Request status',
        field: [id],
        lbl: 'Envoyer / Send',
        lk: links[lkStatut]
    },
    crtDmd:{
        titre: 'Demande de transport / Travel request',
        field: [moyen,nbrEnf,lieu,date,raison],
        lbl: 'Envoyer / Send',
        lk: links[lkConnDmd]
    },
# {
#     badge:"202",
#     ,
#     email:"admin.test@trans.com",
#     niveau:3,
#     nom:"Test",
#     prenom:"Admin",
#     role:1,
#     'societe':"SOMILO",
# }
    crtUser:{
        titre: 'Creation d\'un utilisateur / Create User',
        field: [prenom,nom,email,ste,dept,role,niveau],
        lbl: 'Envoyer / Send',
        lk: links[lkCrtUsr]
    },
    urg:{
        titre: 'Demande Urgent',
        field: [nomC,dept,moyen,lieu,sDt],
        lbl: 'Envoyer / Send',
        lk: links[lkUrg]
    },

}
spUsrMnu = {
    'Creer un utilisateur': links[lkCrtUsr],
    'Ajouter un dwepartement': ''
}
siteMenu = {
    'Accueil': '/',
    'Faire une demande': links[lkDmd],
    'Suivre une demande': links[lkStatut],
    'Liste de transport': links[lkListDisp]
}
chemins = {
        depart:'Loulo-Bamako',
        retour:'Bamako-Loulo'
    }
dmdMsg = lambda st: f"""
    Une demande {'approuvée' if st == confirmer else 'validée'} ne vous garantit pas une place!! <br />
    {'Approved' if st == confirmer else 'Valid'} request doesn't garantee you a seat!!
    """
imgs = lambda my: f"img/{'bus' if my == bus else 'plane'}.png"
deptEng = 'Engineering'
deptAdm='Admin'
deptOcm = 'OC Mining'
superUsr = 10
data = {
    age: {
        '3 mois':'3 mois',
        '6 mois':'6 mois',
        '9 mois':'9 mois',
        '1 an':'1 an',
        '2 ans':'2 ans',
    },
    dept: {
        deptEng:deptEng,
        deptAdm:deptAdm,
        deptOcm:deptOcm
        },
    trainee: {
        'Non': 'Non',
        'Oui': 'Oui'
    },
    ste: {
        gktoSA: gktoSA,
        somilo: somilo,
        sousTrai: sousTrai
    },
    moyen: {
        bus: bus,
        avion: avion
    },
    lieu:{
        loulo: loulo,
        gkto: gkto,
        bko: bko
    },
    niveau:{
        faible:faible,
        interm: interm,
        elevee: elevee,
        # superUsr: superUsr
    },
    role: {
        usr: 'User',
        adm: 'Admin',
        # superUsr: 'Super Utilisateur'
    },
    chemin:chemins

}
nbrPer = {
    bus: 10,
    avion: 1
}


textType = [prenom,badge,nom,id,sc,nomC,raison]
isMod = [lieu,trainee,badge,nbrEnf,sc]
pwdType = [password,pwdConf]
nbrType = [costCode,numero,nbrEnf]
slctType = list(data.keys())
notReq = [sc,trainee,badge,heberger]
dmdDate = [dateDepart,dateArrivee]
usrDspl = [badge,nomC,ste,lieu,sc,raison,dateDepart,dateArrivee]
lstDspl = [moyen,chemin,jourDeVoyage,publier]
admDspl = usrDspl+[lieu,moyen,niveau]
trsDspl = [no,id,nomC,ste,badge,statut]
bus_retour = [1,3,5]
bus_depart = [0,2,4]
vol = [2,4]
dmdFields = [id,lieu,date,badge,statut,dateDepart,sc,raison,dateConf,dept,niveau,ste,nbrEnf,dateArrivee,nomC,numero,moyen,heberger,trainee]
vDt = [{
    'id': '154zh', 'lieu': 'Gounkoto', 'date': '2022/8/5 20:52:57', 'badge': 'bg3', 'statut': 'Valider', 'date_depart': '17/08/2022', 'sous_couvert': '-', 'raison': 'Miammm', 'date_confirmation': '2022/8/5 21:54:8', 'departement': 'Admin', 'niveau': 0, 'societe': 'Cliquez', 'nombre_enfant': 0, 'date_retour': '//', 'nom_complet': 'Capo Loup', 'numero': '7777789', 'moyen': 'VOL / FLY', 'heberger': '', 'trainee': 'Non'},
    {'lieu': 'Loulo', 'date_confirmation': '2022/8/6 17:33:13', 'date': '2022/8/6 13:9:35', 'niveau': 0, 'societe': 'Gounkoto S.A.', 'sous_couvert': '-', 'numero': '3125', 'moyen': 'VOL / FLY', 'badge': '11324', 'raison': 'Vsa', 'departement': 'Admin', 'statut': 'Valider', 'nom_complet': 'V.JEU', 'nombre_enfant': 0, 'date_depart': '17/08/2022', 'date_retour': '19/08/2022', 'id': '2026qe', 'heberger': '', 'trainee': 'Non'}, {'statut': 'En attente de confirmation', 'numero': '57655', 'niveau': 0, 'nom_complet': 'TYTYSD', 'moyen': 'VOL / FLY', 'raison': 'GYF', 'societe': 'SOMILO', 'date_depart': '17/08/2022', 'id': '3086mh', 'lieu': 'Gounkoto', 'nombre_enfant': 0, 'date_retour': '//', 'sous_couvert': '-', 'heberger': '', 'trainee': 'Non', 'badge': '655', 'date': '2022/8/8 23:6:2', 'departement': 'Admin'}, {'id': '548hl', 'lieu': 'Bamako', 'date': '2022/8/6 13:17:49', 'badge': 'NA', 'statut': 'En attente de confirmation', 'date_depart': '17/08/2022', 'sous_couvert': 'Bsnq', 'raison': 'Hsjs', 'departement': 'Cliquez', 'societe': 'Gounkoto S.A.', 'niveau': 0, 'nombre_enfant': 0, 'date_retour': '19/08/2022', 'nom_complet': 'Qqq', 'numero': '548', 'moyen': 'VOL / FLY', 'heberger': '', 'trainee': 'Non'}, {'id': '6816xr', 'numero': '7777789', 'moyen': 'VOL / FLY', 'date_confirmation': '2022/8/5 21:54:8', 'sous_couvert': '-', 'statut': 'Valider', 'lieu': 'Bamako', 'departement': 'Admin', 'niveau': 0, 'raison': 'Miammm miiiiiiii', 'nom_complet': 'wave', 'heberger': '', 'trainee': 'Non', 'societe': 'SOMILO', 'badge': '0099', 'date_depart': '17/08/2022', 'date': '2022/8/5 20:56:34', 'nombre_enfant': 0, 'date_retour': '//'}, {'moyen': 'VOL / FLY', 'date_confirmation': '2022/8/6 17:32:3', 'sous_couvert': '-', 'lieu': 'Loulo', 'raison': 'GQIUW', 'statut': 'Valider', 'departement': 'Admin', 'societe': 'Sous Traitant', 'niveau': 0, 'badge': '234', 'date_depart': '17/08/2022', 'nom_complet': 'CHAPOULA MATATA', 'date': '2022/8/6 11:53:58', 'heberger': '', 'nombre_enfant': 0, 'trainee': 'Non', 'date_retour': '19/08/2022', 'id': '8779tw', 'numero': '12345678'}, {'numero': '9999999', 'id': '9427km', 'moyen': 'VOL / FLY', 'date_confirmation': '2022/8/5 2:8:59', 'sous_couvert': '-', 'statut': 'Valider', 'lieu': 'Gounkoto', 'departement': 'Admin', 'niveau': 0, 'raison': 'Miammm', 'nom_complet': 'Capo Loup', 'heberger': '', 'trainee': 'Oui', 'societe': 'SOMILO', 'badge': 'GP', 'date_depart': '17/08/2022', 'date': '2022/8/5 2:8:7', 'nombre_enfant': 0, 'date_retour': '//'}, {'moyen': 'VOL / FLY', 'date_confirmation': '2022/8/5 22:3:16', 'sous_couvert': "Fuck y'all ", 'lieu': 'Bamako', 'raison': 'Sirrrrr', 'statut': 'Valider', 'departement': 'Admin', 'niveau': 0, 'societe': 'Gounkoto S.A.', 'date_depart': '17/08/2022', 'badge': 'NA', 'date': '2022/8/5 20:58:32', 'nom_complet': 'Test', 'heberger': '', 'trainee': 'Non', 'nombre_enfant': 0, 'date_retour': '//', 'numero': '44444', 'id': '9905xw'},{'id': '154zh', 'lieu': 'Gounkoto', 'date': '2022/8/5 20:52:57', 'badge': 'bg3', 'statut': 'Valider', 'date_depart': '17/08/2022', 'sous_couvert': '-', 'raison': 'Miammm', 'date_confirmation': '2022/8/5 21:54:8', 'departement': 'Admin', 'niveau': 0, 'societe': 'Cliquez', 'nombre_enfant': 0, 'date_retour': '//', 'nom_complet': 'Capo Loup', 'numero': '7777789', 'moyen': 'VOL / FLY', 'heberger': '', 'trainee': 'Non'}, {'lieu': 'Loulo', 'date_confirmation': '2022/8/6 17:33:13', 'date': '2022/8/6 13:9:35', 'niveau': 0, 'societe': 'Gounkoto S.A.', 'sous_couvert': '-', 'numero': '3125', 'moyen': 'VOL / FLY', 'badge': '11324', 'raison': 'Vsa', 'departement': 'Admin', 'statut': 'Valider', 'nom_complet': 'V.JEU', 'nombre_enfant': 0, 'date_depart': '17/08/2022', 'date_retour': '19/08/2022', 'id': '2026qe', 'heberger': '', 'trainee': 'Non'}, {'statut': 'En attente de confirmation', 'numero': '57655', 'niveau': 0, 'nom_complet': 'TYTYSD', 'moyen': 'VOL / FLY', 'raison': 'GYF', 'societe': 'SOMILO', 'date_depart': '17/08/2022', 'id': '3086mh', 'lieu': 'Gounkoto', 'nombre_enfant': 0, 'date_retour': '//', 'sous_couvert': '-', 'heberger': '', 'trainee': 'Non', 'badge': '655', 'date': '2022/8/8 23:6:2', 'departement': 'Admin'}, {'id': '548hl', 'lieu': 'Bamako', 'date': '2022/8/6 13:17:49', 'badge': 'NA', 'statut': 'En attente de confirmation', 'date_depart': '17/08/2022', 'sous_couvert': 'Bsnq', 'raison': 'Hsjs', 'departement': 'Cliquez', 'societe': 'Gounkoto S.A.', 'niveau': 0, 'nombre_enfant': 0, 'date_retour': '19/08/2022', 'nom_complet': 'Qqq', 'numero': '548', 'moyen': 'VOL / FLY', 'heberger': '', 'trainee': 'Non'}, {'id': '6816xr', 'numero': '7777789', 'moyen': 'VOL / FLY', 'date_confirmation': '2022/8/5 21:54:8', 'sous_couvert': '-', 'statut': 'Valider', 'lieu': 'Bamako', 'departement': 'Admin', 'niveau': 0, 'raison': 'Miammm miiiiiiii', 'nom_complet': 'wave', 'heberger': '', 'trainee': 'Non', 'societe': 'SOMILO', 'badge': '0099', 'date_depart': '17/08/2022', 'date': '2022/8/5 20:56:34', 'nombre_enfant': 0, 'date_retour': '//'}, {'moyen': 'VOL / FLY', 'date_confirmation': '2022/8/6 17:32:3', 'sous_couvert': '-', 'lieu': 'Loulo', 'raison': 'GQIUW', 'statut': 'Valider', 'departement': 'Admin', 'societe': 'Sous Traitant', 'niveau': 0, 'badge': '234', 'date_depart': '17/08/2022', 'nom_complet': 'CHAPOULA MATATA', 'date': '2022/8/6 11:53:58', 'heberger': '', 'nombre_enfant': 0, 'trainee': 'Non', 'date_retour': '19/08/2022', 'id': '8779tw', 'numero': '12345678'}, {'numero': '9999999', 'id': '9427km', 'moyen': 'VOL / FLY', 'date_confirmation': '2022/8/5 2:8:59', 'sous_couvert': '-', 'statut': 'Valider', 'lieu': 'Gounkoto', 'departement': 'Admin', 'niveau': 0, 'raison': 'Miammm', 'nom_complet': 'Capo Loup', 'heberger': '', 'trainee': 'Oui', 'societe': 'SOMILO', 'badge': 'GP', 'date_depart': '17/08/2022', 'date': '2022/8/5 2:8:7', 'nombre_enfant': 0, 'date_retour': '//'}, {'moyen': 'VOL / FLY', 'date_confirmation': '2022/8/5 22:3:16', 'sous_couvert': "Fuck y'all ", 'lieu': 'Bamako', 'raison': 'Sirrrrr', 'statut': 'Valider', 'departement': 'Admin', 'niveau': 0, 'societe': 'Gounkoto S.A.', 'date_depart': '17/08/2022', 'badge': 'NA', 'date': '2022/8/5 20:58:32', 'nom_complet': 'Test', 'heberger': '', 'trainee': 'Non', 'nombre_enfant': 0, 'date_retour': '//', 'numero': '44444', 'id': '9905xw'},{'id': '154zh', 'lieu': 'Gounkoto', 'date': '2022/8/5 20:52:57', 'badge': 'bg3', 'statut': 'Valider', 'date_depart': '17/08/2022', 'sous_couvert': '-', 'raison': 'Miammm', 'date_confirmation': '2022/8/5 21:54:8', 'departement': 'Admin', 'niveau': 0, 'societe': 'Cliquez', 'nombre_enfant': 0, 'date_retour': '//', 'nom_complet': 'Capo Loup', 'numero': '7777789', 'moyen': 'VOL / FLY', 'heberger': '', 'trainee': 'Non'}, {'lieu': 'Loulo', 'date_confirmation': '2022/8/6 17:33:13', 'date': '2022/8/6 13:9:35', 'niveau': 0, 'societe': 'Gounkoto S.A.', 'sous_couvert': '-', 'numero': '3125', 'moyen': 'VOL / FLY', 'badge': '11324', 'raison': 'Vsa', 'departement': 'Admin', 'statut': 'Valider', 'nom_complet': 'V.JEU', 'nombre_enfant': 0, 'date_depart': '17/08/2022', 'date_retour': '19/08/2022', 'id': '2026qe', 'heberger': '', 'trainee': 'Non'}, {'statut': 'En attente de confirmation', 'numero': '57655', 'niveau': 0, 'nom_complet': 'TYTYSD', 'moyen': 'VOL / FLY', 'raison': 'GYF', 'societe': 'SOMILO', 'date_depart': '17/08/2022', 'id': '3086mh', 'lieu': 'Gounkoto', 'nombre_enfant': 0, 'date_retour': '//', 'sous_couvert': '-', 'heberger': '', 'trainee': 'Non', 'badge': '655', 'date': '2022/8/8 23:6:2', 'departement': 'Admin'}, {'id': '548hl', 'lieu': 'Bamako', 'date': '2022/8/6 13:17:49', 'badge': 'NA', 'statut': 'En attente de confirmation', 'date_depart': '17/08/2022', 'sous_couvert': 'Bsnq', 'raison': 'Hsjs', 'departement': 'Cliquez', 'societe': 'Gounkoto S.A.', 'niveau': 0, 'nombre_enfant': 0, 'date_retour': '19/08/2022', 'nom_complet': 'Qqq', 'numero': '548', 'moyen': 'VOL / FLY', 'heberger': '', 'trainee': 'Non'}, {'id': '6816xr', 'numero': '7777789', 'moyen': 'VOL / FLY', 'date_confirmation': '2022/8/5 21:54:8', 'sous_couvert': '-', 'statut': 'Valider', 'lieu': 'Bamako', 'departement': 'Admin', 'niveau': 0, 'raison': 'Miammm miiiiiiii', 'nom_complet': 'wave', 'heberger': '', 'trainee': 'Non', 'societe': 'SOMILO', 'badge': '0099', 'date_depart': '17/08/2022', 'date': '2022/8/5 20:56:34', 'nombre_enfant': 0, 'date_retour': '//'}, {'moyen': 'VOL / FLY', 'date_confirmation': '2022/8/6 17:32:3', 'sous_couvert': '-', 'lieu': 'Loulo', 'raison': 'GQIUW', 'statut': 'Valider', 'departement': 'Admin', 'societe': 'Sous Traitant', 'niveau': 0, 'badge': '234', 'date_depart': '17/08/2022', 'nom_complet': 'CHAPOULA MATATA', 'date': '2022/8/6 11:53:58', 'heberger': '', 'nombre_enfant': 0, 'trainee': 'Non', 'date_retour': '19/08/2022', 'id': '8779tw', 'numero': '12345678'}, {'numero': '9999999', 'id': '9427km', 'moyen': 'VOL / FLY', 'date_confirmation': '2022/8/5 2:8:59', 'sous_couvert': '-', 'statut': 'Valider', 'lieu': 'Gounkoto', 'departement': 'Admin', 'niveau': 0, 'raison': 'Miammm', 'nom_complet': 'Capo Loup', 'heberger': '', 'trainee': 'Oui', 'societe': 'SOMILO', 'badge': 'GP', 'date_depart': '17/08/2022', 'date': '2022/8/5 2:8:7', 'nombre_enfant': 0, 'date_retour': '//'}, {'moyen': 'VOL / FLY', 'date_confirmation': '2022/8/5 22:3:16', 'sous_couvert': "Fuck y'all ", 'lieu': 'Bamako', 'raison': 'Sirrrrr', 'statut': 'Valider', 'departement': 'Admin', 'niveau': 0, 'societe': 'Gounkoto S.A.', 'date_depart': '17/08/2022', 'badge': 'NA', 'date': '2022/8/5 20:58:32', 'nom_complet': 'Test', 'heberger': '', 'trainee': 'Non', 'nombre_enfant': 0, 'date_retour': '//', 'numero': '44444', 'id': '9905xw'},{'id': '154zh', 'lieu': 'Gounkoto', 'date': '2022/8/5 20:52:57', 'badge': 'bg3', 'statut': 'Valider', 'date_depart': '17/08/2022', 'sous_couvert': '-', 'raison': 'Miammm', 'date_confirmation': '2022/8/5 21:54:8', 'departement': 'Admin', 'niveau': 0, 'societe': 'Cliquez', 'nombre_enfant': 0, 'date_retour': '//', 'nom_complet': 'Capo Loup', 'numero': '7777789', 'moyen': 'VOL / FLY', 'heberger': '', 'trainee': 'Non'}, {'lieu': 'Loulo', 'date_confirmation': '2022/8/6 17:33:13', 'date': '2022/8/6 13:9:35', 'niveau': 0, 'societe': 'Gounkoto S.A.', 'sous_couvert': '-', 'numero': '3125', 'moyen': 'VOL / FLY', 'badge': '11324', 'raison': 'Vsa', 'departement': 'Admin', 'statut': 'Valider', 'nom_complet': 'V.JEU', 'nombre_enfant': 0, 'date_depart': '17/08/2022', 'date_retour': '19/08/2022', 'id': '2026qe', 'heberger': '', 'trainee': 'Non'}, {'statut': 'En attente de confirmation', 'numero': '57655', 'niveau': 0, 'nom_complet': 'TYTYSD', 'moyen': 'VOL / FLY', 'raison': 'GYF', 'societe': 'SOMILO', 'date_depart': '17/08/2022', 'id': '3086mh', 'lieu': 'Gounkoto', 'nombre_enfant': 0, 'date_retour': '//', 'sous_couvert': '-', 'heberger': '', 'trainee': 'Non', 'badge': '655', 'date': '2022/8/8 23:6:2', 'departement': 'Admin'}, {'id': '548hl', 'lieu': 'Bamako', 'date': '2022/8/6 13:17:49', 'badge': 'NA', 'statut': 'En attente de confirmation', 'date_depart': '17/08/2022', 'sous_couvert': 'Bsnq', 'raison': 'Hsjs', 'departement': 'Cliquez', 'societe': 'Gounkoto S.A.', 'niveau': 0, 'nombre_enfant': 0, 'date_retour': '19/08/2022', 'nom_complet': 'Qqq', 'numero': '548', 'moyen': 'VOL / FLY', 'heberger': '', 'trainee': 'Non'}, {'id': '6816xr', 'numero': '7777789', 'moyen': 'VOL / FLY', 'date_confirmation': '2022/8/5 21:54:8', 'sous_couvert': '-', 'statut': 'Valider', 'lieu': 'Bamako', 'departement': 'Admin', 'niveau': 0, 'raison': 'Miammm miiiiiiii', 'nom_complet': 'wave', 'heberger': '', 'trainee': 'Non', 'societe': 'SOMILO', 'badge': '0099', 'date_depart': '17/08/2022', 'date': '2022/8/5 20:56:34', 'nombre_enfant': 0, 'date_retour': '//'}, {'moyen': 'VOL / FLY', 'date_confirmation': '2022/8/6 17:32:3', 'sous_couvert': '-', 'lieu': 'Loulo', 'raison': 'GQIUW', 'statut': 'Valider', 'departement': 'Admin', 'societe': 'Sous Traitant', 'niveau': 0, 'badge': '234', 'date_depart': '17/08/2022', 'nom_complet': 'CHAPOULA MATATA', 'date': '2022/8/6 11:53:58', 'heberger': '', 'nombre_enfant': 0, 'trainee': 'Non', 'date_retour': '19/08/2022', 'id': '8779tw', 'numero': '12345678'}, {'numero': '9999999', 'id': '9427km', 'moyen': 'VOL / FLY', 'date_confirmation': '2022/8/5 2:8:59', 'sous_couvert': '-', 'statut': 'Valider', 'lieu': 'Gounkoto', 'departement': 'Admin', 'niveau': 0, 'raison': 'Miammm', 'nom_complet': 'Capo Loup', 'heberger': '', 'trainee': 'Oui', 'societe': 'SOMILO', 'badge': 'GP', 'date_depart': '17/08/2022', 'date': '2022/8/5 2:8:7', 'nombre_enfant': 0, 'date_retour': '//'}, {'moyen': 'VOL / FLY', 'date_confirmation': '2022/8/5 22:3:16', 'sous_couvert': "Fuck y'all ", 'lieu': 'Bamako', 'raison': 'Sirrrrr', 'statut': 'Valider', 'departement': 'Admin', 'niveau': 0, 'societe': 'Gounkoto S.A.', 'date_depart': '17/08/2022', 'badge': 'NA', 'date': '2022/8/5 20:58:32', 'nom_complet': 'Test', 'heberger': '', 'trainee': 'Non', 'nombre_enfant': 0, 'date_retour': '//', 'numero': '44444', 'id': '9905xw'}]
