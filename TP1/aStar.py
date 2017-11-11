from tkinter import *
from math import sqrt


class Noeud():

    def __init__(self, x, y):
        self.colonne = x
        self.ligne = y
        self.coutF = 0
        self.coutG = 0
        self.coutH = 0
        self.parent = self


def Init(event):

    global t_Grille, n_Depart, n_Final, listeFermee, \
        listeOuverte, echelle, resolution, caseDepart, caseArrivee, \
        t_CasesChemin, t_CasesListeOuverte, t_CasesListeFermee

    grilleJeu.delete(ALL)
    t_Grille = []
    resolution = int(400 / echelle)
    for i in range(resolution):
        t_Grille.append([[]] * resolution)
    for ligne in range(resolution):
        for colonne in range(resolution):
            t_Grille[ligne][colonne] = 0
    for i in range(resolution):
        grilleJeu.create_line(i * echelle, 0, i * echelle, 400, fill='white')
    for i in range(resolution):
        grilleJeu.create_line(1, i * echelle, 400, i * echelle, fill='white')

    n_Depart = Noeud(0, 0)
    caseDepart = grilleJeu.create_rectangle(n_Depart.colonne * echelle,
                                            n_Depart.ligne * echelle, (n_Depart.colonne * echelle)
                                            + echelle, (n_Depart.ligne * echelle) + echelle,
                                            outline='white', fill='blue')
    n_Final = Noeud(resolution - 1, resolution - 1)
    caseArrivee = grilleJeu.create_rectangle(n_Final.colonne * echelle,
                                             n_Final.ligne * echelle, (n_Final.colonne * echelle)
                                             + echelle, (n_Final.ligne * echelle) + echelle,
                                             outline='white', fill='green')
    listeFermee = []
    listeOuverte = []
    t_CasesChemin = []
    t_CasesListeOuverte = []
    t_CasesListeFermee = []


def Algorithme(event):

    global listeOuverte, listeFermee, n_Courant, text, t_CasesListeOuverte, \
        t_CasesListeFermee, intervalTemps

    EffaceChemin('l')
    intervalTemps = 250
    t_CasesListeOuverte = []
    t_CasesListeFermee = []
    listeOuverte = []
    listeFermee = []

    n_Courant = n_Depart
    n_Courant.coutH = Distance(n_Courant, n_Final)
    n_Courant.coutF = n_Courant.coutH

    listeOuverte.append(n_Courant)

    while (not (n_Courant.ligne == n_Final.ligne and \
                            n_Courant.colonne == n_Final.colonne) \
                   and listeOuverte != []):

        n_Courant = MeilleurNoeud()
        AjouterListeFermee(n_Courant)

        caseCourant = grilleJeu.create_rectangle(n_Courant.colonne * echelle,
                                                 n_Courant.ligne * echelle,
                                                 (n_Courant.colonne * echelle) + echelle,
                                                 (n_Courant.ligne * echelle) + echelle, fill='maroon')
        fen.update()

        fen.after(intervalTemps, CasesListeFermee())

        t_CasesListeFermee.append(caseCourant)
        grilleJeu.lift(caseDepart)

        fen.after(intervalTemps, AjouterCasesAdjacentes(n_Courant))

    if n_Courant.ligne == n_Final.ligne and n_Courant.colonne == n_Final.colonne:
        RemonterListe()

def MeilleurNoeud():
    cout = 5000000
    noeud = None
    for n in listeOuverte:
        if n.coutF < cout:
            cout = n.coutF
            noeud = n
    return noeud


def AjouterListeFermee(noeud):
    global listeOuverte, listeFermee

    listeFermee.append(noeud)
    listeOuverte.remove(noeud)


def AjouterCasesAdjacentes(n_Courant):
    global listeOuverte, listeFermee

    if choixDirections == 'huitPoints':
        deplacements = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    elif choixDirections == 'quatrePoints':
        deplacements = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    for direction in deplacements:
        coordSuivante = (n_Courant.ligne + direction[0],
                         n_Courant.colonne + direction[1])
        if coordSuivante[0] >= 0 and coordSuivante[0] <= len(t_Grille) - 1 and coordSuivante[1] >= 0 and coordSuivante[1] <= len(t_Grille[0]) - 1:
            if t_Grille[coordSuivante[0]][coordSuivante[1]] == 0:
                n_Temp = Noeud(coordSuivante[1], coordSuivante[0])
                n_Temp.parent = n_Courant
                if not DejaPresentDansListe(n_Temp, listeFermee):
                    n_Temp.coutG = n_Temp.parent.coutG + Distance(n_Temp, n_Temp.parent)
                    n_Temp.coutH = Distance(n_Temp, n_Final)
                    n_Temp.coutF = n_Temp.coutG + n_Temp.coutH

                    n = DejaPresentDansListe(n_Temp, listeOuverte)
                    if n != False:
                        if n_Temp.coutG < n.coutG:
                            n.parent = n_Courant
                            n.coutG = n_Temp.coutG
                            n.coutH = n_Temp.coutH
                            n.coutF = n_Temp.coutF
                    else:
                        listeOuverte.append(n_Temp)
                        fen.after(intervalTemps, CasesListeOuverte(n_Temp))
                        fen.update()


def Distance(noeud1, noeud2):
    a = noeud2.ligne - noeud1.ligne
    b = noeud2.colonne - noeud1.colonne
    if choixHeuristique == 'racineDistEucli':
        return sqrt((a * a) + (b * b))
    elif choixHeuristique == 'distanceEucli':
        return ((a * a) + (b * b))
    elif choixHeuristique == "distManhattan":
        return (abs(a) + abs(b))


def DejaPresentDansListe(noeud, liste):
    for n in liste:
        if n.ligne == noeud.ligne and n.colonne == noeud.colonne:
            return n
    return False

def CasesListeOuverte(n):
    t_CasesListeOuverte.append(grilleJeu.create_rectangle(n.colonne * echelle, n.ligne * echelle, (n.colonne * echelle) + echelle, (n.ligne * echelle) + echelle, fill='orange'))

def CasesListeFermee():
    if t_CasesListeFermee != []:
        grilleJeu.itemconfigure(t_CasesListeFermee[-1], fill='SteelBlue')
        fen.update()

def RemonterListe():
    global t_CasesChemin

    chemin = []
    t_CasesChemin = []
    n = listeFermee[-1]
    chemin.append(n)
    n = n.parent
    while n.parent != n:
        chemin.append(n)
        t_CasesChemin.append(grilleJeu.create_rectangle(n.colonne * echelle,
                                                         n.ligne * echelle, (n.colonne * echelle) + echelle,
                                                         (n.ligne * echelle) + echelle, fill='red'))
        n = n.parent
    chemin.append(n)
    grilleJeu.lift(caseDepart)
    grilleJeu.lift(caseArrivee)


def EffaceChemin(event):
    if t_CasesChemin:
        for caseRouge in t_CasesChemin:
            grilleJeu.delete(caseRouge)
    if t_CasesListeOuverte:
        for caseOrange in t_CasesListeOuverte:
            grilleJeu.delete(caseOrange)
    if t_CasesListeFermee:
        for caseGrise in t_CasesListeFermee:
            grilleJeu.delete(caseGrise)


def Position(event):
    global t_Grille, n_Depart, n_Final

    EffaceChemin('l')
    if event.x > 0 and event.x < 400 and event.y > 0 and event.y < 400:
        indice_colonne = int(event.x / echelle)
        indice_ligne = int(event.y / echelle)
        if mode == 'mur':
            if (indice_colonne == n_Depart.colonne and indice_ligne == n_Depart.ligne) or (indice_colonne == n_Final.colonne and indice_ligne == n_Final.ligne):
                return
            else:
                grilleJeu.create_rectangle(indice_colonne * echelle, indice_ligne * echelle, (indice_colonne * echelle) + echelle, (indice_ligne * echelle) + echelle, outline='white', fill='black')
                t_Grille[indice_ligne][indice_colonne] = 2


def EffacerMur(event):
    global t_Grille

    EffaceChemin('l')
    if event.x > 0 and event.x < 400 and event.y > 0 and event.y < 400:
        indice_colonne = event.x / echelle
        indice_ligne = event.y / echelle
        if (indice_colonne == n_Depart.colonne and indice_ligne == n_Depart.colonne) or (indice_colonne == n_Final.colonne and indice_ligne == n_Final.colonne):
            return
        else:
            grilleJeu.create_rectangle(indice_colonne * echelle, indice_ligne * echelle, (indice_colonne * echelle) + echelle, (indice_ligne * echelle) + echelle, outline='white', fill='wheat')
            t_Grille[indice_ligne][indice_colonne] = 0

def Mur(event):
    global mode

    mode = 'mur'

### ----------------------------------------------------------------------------
fen = Tk()
fen.title("Algorithme A*")
fen.resizable(0, 0)
t_Grille = []
grilleJeu = Canvas(fen, width=400, height=400, bg='wheat')
grilleJeu.grid(row=0, column=0)

grilleJeu.bind('<Button-1>', Position)
grilleJeu.bind("<B1-Motion>", Position)
grilleJeu.bind('<Button-3>', EffacerMur)
grilleJeu.bind("<B3-Motion>", EffacerMur)

fen.bind("t", Algorithme)
fen.bind('e', Init)
fen.bind('l', EffaceChemin)

mode = 'mur'
fen.bind('m', Mur)

indice = 1
choixHeuristique = 'distanceEucli'
choixDirections = 'quatrePoints'
echelle = 10
Init('e')
fen.mainloop()
