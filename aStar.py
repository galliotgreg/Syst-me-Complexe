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

    global tabGrille, noeudDepart, noeudFinal, listeFermee, \
        listeOuverte, echelle, resolution, caseDepart, caseArrivee, \
        tabCasesChemin, tabCasesListeOuverte, tabCasesListeFermee

    grilleJeu.delete(ALL)
    tabGrille = []
    resolution = int(400 / echelle)
    for i in range(resolution):
        tabGrille.append([[]] * resolution)
    for ligne in range(resolution):
        for colonne in range(resolution):
            tabGrille[ligne][colonne] = 0
    for i in range(resolution):
        grilleJeu.create_line(i * echelle, 0, i * echelle, 400, fill='white')
    for i in range(resolution):
        grilleJeu.create_line(1, i * echelle, 400, i * echelle, fill='white')

    noeudDepart = Noeud(0, 0)
    caseDepart = grilleJeu.create_rectangle(noeudDepart.colonne * echelle,
                                            noeudDepart.ligne * echelle, (noeudDepart.colonne * echelle)
                                            + echelle, (noeudDepart.ligne * echelle) + echelle,
                                            outline='white', fill='blue')
    noeudFinal = Noeud(resolution - 1, resolution - 1)
    caseArrivee = grilleJeu.create_rectangle(noeudFinal.colonne * echelle,
                                             noeudFinal.ligne * echelle, (noeudFinal.colonne * echelle)
                                             + echelle, (noeudFinal.ligne * echelle) + echelle,
                                             outline='white', fill='green')
    listeFermee = []
    listeOuverte = []
    tabCasesChemin = []
    tabCasesListeOuverte = []
    tabCasesListeFermee = []


def Algorithme(event):

    global listeOuverte, listeFermee, noeudCourant, text, tabCasesListeOuverte, \
        tabCasesListeFermee, intervalTemps

    EffaceChemin('l')
    intervalTemps = 250
    tabCasesListeOuverte = []
    tabCasesListeFermee = []
    listeOuverte = []
    listeFermee = []

    noeudCourant = noeudDepart
    noeudCourant.coutH = Distance(noeudCourant, noeudFinal)
    noeudCourant.coutF = noeudCourant.coutH

    listeOuverte.append(noeudCourant)

    while (not (noeudCourant.ligne == noeudFinal.ligne and \
                            noeudCourant.colonne == noeudFinal.colonne) \
                   and listeOuverte != []):

        noeudCourant = MeilleurNoeud()
        AjouterListeFermee(noeudCourant)

        caseCourant = grilleJeu.create_rectangle(noeudCourant.colonne * echelle,
                                                 noeudCourant.ligne * echelle,
                                                 (noeudCourant.colonne * echelle) + echelle,
                                                 (noeudCourant.ligne * echelle) + echelle, fill='maroon')
        fen.update()

        fen.after(intervalTemps, CasesListeFermee())

        tabCasesListeFermee.append(caseCourant)
        grilleJeu.lift(caseDepart)

        fen.after(intervalTemps, AjouterCasesAdjacentes(noeudCourant))

    if noeudCourant.ligne == noeudFinal.ligne and noeudCourant.colonne == noeudFinal.colonne:
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


def AjouterCasesAdjacentes(noeudCourant):
    global listeOuverte, listeFermee

    if choixDirections == 'huitPoints':
        deplacements = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    elif choixDirections == 'quatrePoints':
        deplacements = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    for direction in deplacements:
        coordSuivante = (noeudCourant.ligne + direction[0],
                         noeudCourant.colonne + direction[1])
        if coordSuivante[0] >= 0 and coordSuivante[0] <= len(tabGrille) - 1 and coordSuivante[1] >= 0 and coordSuivante[1] <= len(tabGrille[0]) - 1:
            if tabGrille[coordSuivante[0]][coordSuivante[1]] == 0:
                noeudTemp = Noeud(coordSuivante[1], coordSuivante[0])
                noeudTemp.parent = noeudCourant
                if not DejaPresentDansListe(noeudTemp, listeFermee):
                    noeudTemp.coutG = noeudTemp.parent.coutG + Distance(noeudTemp, noeudTemp.parent)
                    noeudTemp.coutH = Distance(noeudTemp, noeudFinal)
                    noeudTemp.coutF = noeudTemp.coutG + noeudTemp.coutH

                    n = DejaPresentDansListe(noeudTemp, listeOuverte)
                    if n != False:
                        if noeudTemp.coutG < n.coutG:
                            n.parent = noeudCourant
                            n.coutG = noeudTemp.coutG
                            n.coutH = noeudTemp.coutH
                            n.coutF = noeudTemp.coutF
                    else:
                        listeOuverte.append(noeudTemp)
                        fen.after(intervalTemps, CasesListeOuverte(noeudTemp))
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
    tabCasesListeOuverte.append(grilleJeu.create_rectangle(n.colonne * echelle, n.ligne * echelle, (n.colonne * echelle) + echelle, (n.ligne * echelle) + echelle, fill='orange'))

def CasesListeFermee():
    if tabCasesListeFermee != []:
        grilleJeu.itemconfigure(tabCasesListeFermee[-1], fill='SteelBlue')
        fen.update()

def RemonterListe():
    global tabCasesChemin

    chemin = []
    tabCasesChemin = []
    n = listeFermee[-1]
    chemin.append(n)
    n = n.parent
    while n.parent != n:
        chemin.append(n)
        tabCasesChemin.append(grilleJeu.create_rectangle(n.colonne * echelle,
                                                         n.ligne * echelle, (n.colonne * echelle) + echelle,
                                                         (n.ligne * echelle) + echelle, fill='red'))
        n = n.parent
    chemin.append(n)
    grilleJeu.lift(caseDepart)
    grilleJeu.lift(caseArrivee)


def EffaceChemin(event):
    if tabCasesChemin:
        for caseRouge in tabCasesChemin:
            grilleJeu.delete(caseRouge)
    if tabCasesListeOuverte:
        for caseOrange in tabCasesListeOuverte:
            grilleJeu.delete(caseOrange)
    if tabCasesListeFermee:
        for caseGrise in tabCasesListeFermee:
            grilleJeu.delete(caseGrise)


def Position(event):
    global tabGrille, noeudDepart, noeudFinal

    EffaceChemin('l')
    if event.x > 0 and event.x < 400 and event.y > 0 and event.y < 400:
        indice_colonne = int(event.x / echelle)
        indice_ligne = int(event.y / echelle)
        if mode == 'mur':
            if (indice_colonne == noeudDepart.colonne and indice_ligne == noeudDepart.ligne) or (indice_colonne == noeudFinal.colonne and indice_ligne == noeudFinal.ligne):
                return
            else:
                grilleJeu.create_rectangle(indice_colonne * echelle, indice_ligne * echelle, (indice_colonne * echelle) + echelle, (indice_ligne * echelle) + echelle, outline='white', fill='black')
                tabGrille[indice_ligne][indice_colonne] = 2


def EffacerMur(event):
    global tabGrille

    EffaceChemin('l')
    if event.x > 0 and event.x < 400 and event.y > 0 and event.y < 400:
        indice_colonne = event.x / echelle
        indice_ligne = event.y / echelle
        if (indice_colonne == noeudDepart.colonne and indice_ligne == noeudDepart.colonne) or (indice_colonne == noeudFinal.colonne and indice_ligne == noeudFinal.colonne):
            return
        else:
            grilleJeu.create_rectangle(indice_colonne * echelle, indice_ligne * echelle, (indice_colonne * echelle) + echelle, (indice_ligne * echelle) + echelle, outline='white', fill='wheat')
            tabGrille[indice_ligne][indice_colonne] = 0

def Mur(event):
    global mode

    mode = 'mur'

### ----------------------------------------------------------------------------
fen = Tk()
fen.title("Algorithme A*")
fen.resizable(0, 0)
tabGrille = []
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
