# EXPORTATION ET AFFICHAGE DE LABYRINTHES

#1/ Travail préparatoire
def labyFromFile(fn) :
    """
    Lecture d'un labyrinthe dans le fichier de nom fn
    Read a maze from the file named fn.
    On renvoie les éléments suivants en appelant cette fonction :
1. le labyrinthe lu : une liste à 2 dimensions ;
2. son entrée : liste des 2 coordonnées ligne et colonne ;
3. sa sortie : liste des 2 coordonnées ligne et colonne
    """
    f = open(fn)
    laby = []
    indline = 0
    for fileline in f:
        labyline = []
        inditem = 0
        for item in fileline:
            # empty cell / case vide
            if item == ".":
                labyline.append(0)
            # wall / mur
            elif item == "#":
                labyline.append(1)
            # entrance / entree
            elif item == "x":
                labyline.append(0)
                mazeIn = [indline, inditem]
            # exit / sortie
            elif item == "X":
                labyline.append(0)
                mazeOut = [indline, inditem]
            # discard "\n" char at the end of each line
            inditem += 1
        laby.append(labyline)
        indline += 1
    f.close()
    return laby, mazeIn, mazeOut


"""Pour conserver toutes les informations utiles au jeu on cree un dictionnaire dicoJeu qui sera passé en paramètre dans toutes les fonctions
qui auront ainsi accès à toutes les informations nécessaires pour fonctionner"""
lab,ent,sor = labyFromFile("laby1.laby")#On stocke les éléments renvoyés de la fonction labyFromFile dans ces variables.
dicoJeu = {"Coin_Gauche": [-300, 300],     #le coin gauche du labyrinthe(debut du tracé du labyrinthe)
           "labyrinthe": lab,
           "entree": ent,
           "sortie": sor,
           "taille": 40}                   #la taille d'un carre representant un bloc du labyrinthe


#2/ Affichage de labyrinthe
def afficheTextuel(labyrinthe):
    """ Ici on reçoit un labyrinthe comme paramètre, et on l’affiche
textuellement dans la console, en représentant les murs par un caractère dièse #,
les passages par un espace, l’entrée par un x et la sortie par un o"""
    lignes = 0
    coorEntree = labyrinthe["entree"]
    coorSortie = labyrinthe["sortie"]
    for i in labyrinthe["labyrinthe"]:          #On parcours les lignes du labyrinthe
        colonne = 0
        for k in range(0,len(i)):               #On parcours les colones du labyrinthe
            if i[k]==1:
                print("#",end="")
            elif i[k]==0:
                if [lignes,colonne] == coorEntree:
                    print("x",end="")
                elif [lignes,colonne] == coorSortie:
                    print("o",end="")   
                else:
                    print(" ",end="")
            colonne += 1
        print()             #Pour sauter une ligne
        lignes += 1
#afficheTextuel(dicoJeu)

from turtle import *


def carre(l,c,C):
    """ Creation d'un bloc (carré) sur l'écran avec les paramètres l:longeur du carre
    c: couleur du carre ; C:couleur du bord """
    color(c)                # pencolor (couleur du tracé)
    begin_fill()            #Appeler cette fonction avant de dessiner le carré
    for i in range(0,4):
        pencolor(C)         # pencolor (couleur du tracé)
        forward(l)
        right(90)
    end_fill()              
    up()
    forward(l)
    down() 
    
    
def afficheGraphique(labyrinthe,epaisseur):
    """Reçoit un labyrinthe, l’affiche
graphiquement dans la fenêtre turtle, les murs en noir,
et les passages restent blancs. L’entrée et la sortie prennent une autre
couleur pour les distinguer."""
    lignes = 0
    coorEntree = labyrinthe["entree"]
    coorSortie = labyrinthe["sortie"]
    xcor = -300
    ycor = 300
    tracer(0,0)
    up()
    goto(xcor,ycor)
    down()
    for i in labyrinthe["labyrinthe"]:          # parcourir la liste a 2 dimensions(labyrinthe) et commencer a l'afficher sur la fenetre turtle.
        colonnes = 0
        for k in range(0,len(i)):
            if i[k]==1:                               # tracer les murs
                carre(epaisseur,"black","black")
            elif i[k]==0:
                if [lignes,colonnes] == coorEntree:   # tracer l'entree
                    carre(epaisseur,"purple","#222222")               
                elif [lignes,colonnes] == coorSortie: # tracer la sortie
                    carre(epaisseur,"green","#222222")
                else:            # blanc
                    #On modifie la fonction pour que ca affiche les carrefours et les impasses de différents couleur.
                    #On va donc utuliser la fonction Typecellule (partie 4) pour le faire
                    if typeCellule(lignes,colonnes) == "carrefour":
                        carre(epaisseur,"yellow","#222222")
                    elif typeCellule(lignes,colonnes)=="impasse":
                        carre(epaisseur,"gray","black")
                    else:
                        carre(epaisseur,"white","#222222")
            colonnes += 1
        ycor -= epaisseur                             # mettre le cursus au début la nouvelle ligne 
        up()
        goto(xcor,ycor)
        down()
        lignes += 1
    tracer(1)
    update()                                          # mettre a jour les nouvelles actions
    

# 3/Positionnement de la tortue                                # convertir des coors x,y de la position de tortue(pixels) vers coors(ligne et colonne)
"""dictionnaire qui contient les coors du coin gauche de laby, taille de cellule, nb de colonnes et nb de lignes du labyrinthe"""
Infos_Laby = {"coin_gauche":[-300,300],  
              "taille":40,
              "nb_colonnes":len(dicoJeu["labyrinthe"][0])-1 ,
              "nb_lignes":len(dicoJeu["labyrinthe"])-1}                  

def pixel2cell(x,y):                             # convertir les coors de tortue à (ligne,colonne)
    x_Coin_gauche = dicoJeu["Coin_Gauche"][0]
    y_Coin_gauche = dicoJeu["Coin_Gauche"][1]
    taille = dicoJeu["taille"]
    ligne = colonne = 0
    x_max = x_Coin_gauche + (Infos_Laby["nb_colonnes"]+1)*taille
    y_min = y_Coin_gauche - (Infos_Laby["nb_lignes"]+1)*taille
    
    #pour s'assurer qu'on ne passe pas en paramètre des coordonnées qui ne correspondent pas a celles du labyrinthe
    if x_Coin_gauche <= x <= x_max and y_Coin_gauche>=y>=y_min:      
        for i in range(0,Infos_Laby["nb_colonnes"]+1):
            if x_Coin_gauche+(taille*(i)) < x <= x_Coin_gauche+(taille*(i+1)):
                colonne = i 
            elif x == x_Coin_gauche:
                colonne = 0
            elif x < x_Coin_gauche or x > x_Coin_gauche+taille*(Infos_Laby["nb_colonnes"]+1):
                colonne = 0
        for j in range(0,Infos_Laby["nb_lignes"]+1):
            if y_Coin_gauche-(taille*(j)) > y >= y_Coin_gauche-(taille*(j+1)):
                ligne = j
            elif y == y_Coin_gauche:
                ligne = 0
            elif y > y_Coin_gauche or y < y_Coin_gauche-taille*(Infos_Laby["nb_lignes"]+1):
                ligne = 0
        return ligne,colonne
    else:
        return (0,0)                    

def testclic(x,y):
    if pixel2cell(x,y) == (0,0):
        print("hors") 
    else:
        print("ligne:",pixel2cell(x,y)[0],"\ncolonne:",pixel2cell(x,y)[1])
#onscreenclick(testclic)

    
def cell2pixel(i,j):
    """Convertir des coors (ligne et colonne) de la liste en position de tortue(pixels)"""
    taille= dicoJeu["taille"]
    x_coin_gauche= dicoJeu["Coin_Gauche"][0]
    y_coin_gauche= dicoJeu["Coin_Gauche"][1]
    x_centre= x_coin_gauche + taille/2
    y_centre= y_coin_gauche - taille/2
    if i==0 and j==0:
        x= x_centre
        y=y_centre
    elif i==0 and j!=0:
        x= x_centre + (j)*taille
        y= y_centre
    elif i!=1 and j==1:
        x= x_centre
        y= y_centre - (i)* taille
    else:
        x= x_centre + (j)*taille
        y= y_centre - (i)* taille
    return x, y
#print(cell2pixel(0,0))

# 4/ Cases spéciales
def typeCellule(ligne, colonne):
    resultat = ""
    if dicoJeu["labyrinthe"][ligne][colonne] == 1:  
        resultat = "mur"
    else:
        if ligne == dicoJeu["entree"][0] and colonne == dicoJeu["entree"][1]:
            resultat = "entrée"
        elif ligne == dicoJeu["sortie"][0] and colonne == dicoJeu["sortie"][1]:
            resultat = "sortie"
        else:
            compteur = 0
            if dicoJeu["labyrinthe"][ligne][colonne-1]==0:
                compteur += 1
            if dicoJeu["labyrinthe"][ligne][colonne+1]==0:
                compteur += 1
            if dicoJeu["labyrinthe"][ligne-1][colonne]==0:
                compteur += 1
            if dicoJeu["labyrinthe"][ligne+1][colonne]==0:
                compteur += 1
            if compteur==3:
                resultat = "carrefour"
            elif compteur==2:
                resultat="passage standard"
            elif compteur==1:
                resultat="impasse"
    return resultat  


# 6/ La partie 2 NAVIGATION GUIDEE
liste_chemin= []    #On crée cette liste en tant que variable gloable pour enregistrer les resultats des fonctions gauche
                    #droite, haut, bas (le chemin suivi par la tortue)


def couleur():                                  # changer couleur de la tortue à fonction de typecellule
    if typeCellule(pixel2cell(object.xcor(),object.ycor())[0],pixel2cell(object.xcor(),object.ycor())[1])=="carrefour":
        object.color("blue")
    elif typeCellule(pixel2cell(object.xcor(),object.ycor())[0],pixel2cell(object.xcor(),object.ycor())[1])=="impasse":
        object.color("purple")
    elif typeCellule(pixel2cell(object.xcor(),object.ycor())[0],pixel2cell(object.xcor(),object.ycor())[1])=="sortie":
        object.color("greenyellow")
    elif typeCellule(pixel2cell(object.xcor(),object.ycor())[0],pixel2cell(object.xcor(),object.ycor())[1])=="passage standard":
        object.color("pink")
    
def gauche():
    #Changer la couleur de la tortue selon la fonction typecellule (le type de la cellule sur laquelle la tortue est placé en ce moment)
    ligne,colonne = pixel2cell(object.xcor() - 40,object.ycor())       #pour recevoir les coordonnees de ligne et de colonne de la tortue
    object.setheading(180)                      #setheading: pour positionner l'orientation de la tortue selon un angle donné
    if typeCellule(ligne,colonne) != "mur":     #On utilise ligne et colonne qu'on a obtenu a partir de la fonction pixe2cell
        object.forward(40)
        couleur()                                #On appelle la fonction couleur pour verifier si on a passé sur une case spéciale
        print("gauche ; left")
        liste_chemin.append("g")                  #On appelle la fonction couleur pour verifier si on a passé sur une case spéciale
    else:
        object.color("red")
        ontimer(couleur,200)
        print("erreur")
    
def droite():
    ligne,colonne = pixel2cell(object.xcor() + 40,object.ycor())
    object.setheading(0)
    if typeCellule(ligne,colonne) != "mur":
        object.forward(40)
        couleur()
        print("droite ; right")
        liste_chemin.append("d")
    else:
        object.color("red")
        ontimer(couleur,200)
        print("erreur")
    
def bas():
    ligne,colonne = pixel2cell(object.xcor(),object.ycor() - 40)
    object.setheading(270)
    if typeCellule(ligne,colonne) != "mur":        
        object.forward(40)
        couleur()
        print("bas ; down")
        liste_chemin.append("b")
    else:
        object.color("red")
        ontimer(couleur,200)
        print("erreur")
    
def haut():
    # A completer: Optimiser nombre line
    if pixel2cell(object.xcor() - 40,object.ycor()) == "hors":
        print("erreur")
    else:
        ligne,colonne = pixel2cell(object.xcor(),object.ycor() + 40)
        object.setheading(90)
        if typeCellule(ligne,colonne) != "mur":        
            object.forward(40)
            couleur()
            print("haut ; up")
            liste_chemin.append("h")
        else:
            object.color("red")
            ontimer(couleur,200)
            print("erreur")
        
        
    

# déplacer la tortue en suivant commandes dans liste_chemin
def suivreChemin(li):
    drapeau = True
    i = 0
    while i <= len(li)-1 and drapeau:
        x = object.xcor()
        y = object.ycor()
        if li[i]=="g":
            gauche()
        elif li[i]=="h":
            haut()
        elif li[i]=="d":
            droite()
        else:
            bas()
        i+=1
        if object.xcor()==x and object.ycor()==y:    
            print("mouvement impossible")
            drapeau = False
    if i== len(li):
        print("réussite")
    
# déplacer la tortue en suivant commandes en sens inverse
def inverserChemin(li):
    liste = []
    for i in range(-1,-len(li)-1,-1):
        if li[i] == "d":
            liste.append("g")
        elif li[i] == "g":
            liste.append("d")
        elif li[i] == "h":
            liste.append("b")
        else:
            liste.append("h")
    suivreChemin(liste)         
  
  
  
# key bindings
def keys():
    onkeypress(gauche, "Left")
    onkeypress(droite, "Right")
    onkeypress(haut, "Up")
    onkeypress(bas, "Down")
    listen()


# affichage
wind=Screen()
wind.title("Labyrinthe par Kiro et Trungle")    #pour que le Labyrinthe s'affiche tout instantanément


# création de la tortue
object = Turtle()
object.shape("turtle")
object.color("pink")
object.shapesize(stretch_len=1.18,stretch_wid=1.6)
tracer(0)
object.penup()
object.goto(cell2pixel(dicoJeu["entree"][0],dicoJeu["entree"][1]))
tracer(1)


# TROISIEME PARTIE

def explorer():
    def checkmur(x, y):
        return typeCellule(x, y) == 'mur'

    def checkleft():
        tortue_o = int(object.heading())
        ligne, colonne = pixel2cell(object.xcor(), object.ycor())
        if (tortue_o == 0):
            if checkmur(ligne - 1, colonne): 
                return False 
            else: 
                return True
        elif (tortue_o == 90):
            if checkmur(ligne, colonne - 1): 
                return False 
            else: 
                return True
        elif (tortue_o == 180):
            if checkmur(ligne + 1, colonne): 
                return False 
            else: 
                return True
        elif (tortue_o == 270):
            if checkmur(ligne, colonne + 1): 
                return False 
            else: 
                return True
    
    '''Avoid float number'''
    chemin = []
    Pas_histoire = []
    while not (round(object.xcor()),round(object.ycor())) == cell2pixel(sor[0], sor[1]):
        # print("Current position: " + str(round(object.xcor())) + ' ' + str(round(object.ycor())))
        # print("FINISH: " + str(cell2pixel(sor[0], sor[1])))
        wind.update()
        if checkleft():         #si c'est mur on ne peut pas passer, et donc on varie l'orientation de la tortue pou verifier une autre case
                                # sinon on avance et on stocke ce mouvement dans la liste pas_histoire
            object.left(90)
            dict_orientation = {
                0: 'd',
                90: 'h',
                180: 'g',
                270: 'b'
            }
            if round(object.heading()) in dict_orientation :
                chemin.append(dict_orientation[round(object.heading())])            
            object.forward(40)
            Pas_histoire.append(pixel2cell(object.xcor(),object.ycor()))
        else:
            object.right(90)
    
    # algo trouver le plus court chemin
    i = 0
    while i>=0 and i<=len(chemin)-2:
        a = chemin[i]
        b = chemin[i+1]
        if (a=="d" and b=="g") or (a=="g" and b=="d") or (a=="h" and b=="b") or (a=="b" and b=="h"):
            chemin.pop(i)
            chemin.pop(i)
            if i>0:
                i-=1
        else:
            i+=1
    return chemin
  
# fonction pour écrire Victoire!!!   
crayon=Turtle()     
def writeVictoire(x=True):     
               
    crayon.hideturtle()
    crayon.penup()
    crayon.goto(0,0)
    crayon.pendown()
    crayon.color("springgreen")
    crayon.write("Victoire!!!!!",False,align="center",font=("Lora",50,"normal"))
    
    
## EXTENSIONS ##
# 7.ameliorer l'interface

# creation de bouton (manuel,auto,exit,replay)
def bouton_modemanuel():            
    wind.tracer(0)
    mode_manuel = Turtle()
    mode_manuel.hideturtle()
    mode_manuel.penup()
    mode_manuel.goto(-300,-250)
    mode_manuel.pendown()
    mode_manuel.pensize(5)
    mode_manuel.color("white")
    mode_manuel.begin_fill()
    for i in range (2):
        mode_manuel.pencolor("black")
        mode_manuel.forward(80)
        mode_manuel.right(90)
        mode_manuel.forward(40)
        mode_manuel.right(90)
    mode_manuel.end_fill()
    mode_manuel.penup()
    mode_manuel.goto(-290,-275)
    mode_manuel.write("manuel",font=("Courier",14,'normal'))
    
def bouton_modeauto():
    wind.tracer(0)
    mode_auto = Turtle()
    mode_auto.hideturtle()
    mode_auto.penup()
    mode_auto.goto(-150,-250)
    mode_auto.pendown()
    mode_auto.pensize(5)
    mode_auto.color("white")
    mode_auto.begin_fill()
    for i in range (2):
        mode_auto.pencolor("black")
        mode_auto.forward(80)
        mode_auto.right(90)
        mode_auto.forward(40)
        mode_auto.right(90)
    mode_auto.end_fill()
    mode_auto.penup()
    mode_auto.goto(-130,-275)
    mode_auto.write("auto",font=("Courier",14,'normal'))
    wind.tracer(1)
def bouton_exit():
    wind.tracer(0)
    exit = Turtle()
    exit.hideturtle()
    exit.penup()
    exit.goto(150,-250)
    exit.pendown()
    exit.pensize(5)
    exit.color("white")
    exit.begin_fill()
    for i in range (2):
        exit.pencolor("black")
        exit.forward(80)
        exit.right(90)
        exit.forward(40)
        exit.right(90)
    exit.end_fill()
    exit.penup()
    exit.goto(160,-275)
    exit.write("exit",font=("Courier",14,'normal'))
    wind.tracer(1)
def bouton_replay():
    replay = Turtle()
    replay.hideturtle()
    replay.penup()
    replay.goto(250,-250)
    replay.pendown()
    replay.pensize(5)
    replay.color("white")
    replay.begin_fill()
    for i in range (2):
        replay.pencolor("black")
        replay.forward(80)
        replay.right(90)
        replay.forward(40)
        replay.right(90)
    replay.end_fill()
    replay.penup()
    replay.goto(260,-275)
    replay.write("replay",font=("Courier",14,'normal'))
def click(x,y):                 
        if -150<x<-70 and -250>y>-290:    #bouton auto
            object.speed(1)
            a = explorer()
            explorer()
            object.goto(cell2pixel(dicoJeu["entree"][0],dicoJeu["entree"][1]))
            object.pendown()
            object.pensize(5)
            suivreChemin(a)
            writeVictoire()
        elif -300<x<-220 and -250>y>-290:    # bouton manuel
            object.speed(0)
            object.penup()
            booleen = True
            while booleen:
                wind.update()
                keys()
                if list(pixel2cell(object.xcor(),object.ycor())) == dicoJeu["sortie"]:
                    booleen=False
            writeVictoire()
        elif 150<x<230 and -250>y>-330:      # bouton exit
            print("end programme.")
            wind.bye()
        elif 250<x<330 and -250>y>-290:     # bouton replay
            crayon.clear()
            object.clear()
            object.penup()
            object.goto(cell2pixel(dicoJeu["entree"][0],dicoJeu["entree"][1]))
            object.color("pink")




#### PRINCIPAL PROGRAM ####
#start loop
def main():
    wind.bgcolor("lightblue")
    hideturtle()
    afficheGraphique(dicoJeu,40)
    update()
    bouton_modeauto()
    bouton_modemanuel()
    bouton_exit()
    bouton_replay()
    onscreenclick(click)
    
    
main()
done()

  

    


        

    
      
    
        
    
        
