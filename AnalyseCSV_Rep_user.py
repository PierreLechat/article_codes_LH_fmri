import csv
import unidecode

TailleL_Info = 5
ListeRep = [["CHINE","CHENI","CHIEN"],["CRIME"],["AUBE"],
            ["APERO","PAREO"],["SANTE","ANTES","ENTAS","NESTA","SEANT"],["CHARME","MACHER"],
            ["GERA","RAGE","GREA"],["AMIS","MISA","SAMI","SIMA"],["CERTES","CRETES","TERCES"],
            ["PUREMENT"],["BARRE"],["ESPOIR","PROIES"],
            ["RIDES","REDIS"],["SILENCE"],["IMAGINER"],
            ["LOUPE"],["IMAGE"],["GUIDE"],
            ["PERSO","PROSE","POSER","PORES","REPOS","PSORE"],["PIGEON"],
            ["MENAGE","ENGAME","MAGNEE","MANGEE"],["GOYAVE"],["NATIVE","VEINAT","VENAIT","ENVIAT"],
            ["CENTRE","CREENT","TENREC"],["EROS","ORES","ROSE","SORE"],["PEUR","PUER","PRUE","REPU"],
            ["MONDE"],["DEITE","EDITE","TIEDE"],["PEINE","PINEE"],
            ["INTRA","RIANT","TARIN","TRINA"]
            ]
ListeQuesti = ["NICHE","MERCI","BEAU",
               "OPERA","SENAT","MARCHE",
               "GARE","MAIS","SECRET",
               "EMPRUNTE","ARBRE","POIRES",
               "DESIR","ENCLISE","MIGRAINE",
               "POULE","MAGIE","DIGUE",
               "SPORE","POIGNE","MANEGE",
               "VOYAGE","VANITE","RECENT",
               "OSER","PURE","DEMON",
               "DIETE", "EPINE","TRAIN"]

Chemin = "/Volumes/Samsung_T5/Projet Recherche Maîtrise/Reponse_Anagramme_labac/survey.user_input.csv"

fichier = open(Chemin,"r")
cr = csv.reader(fichier, delimiter = ",")

Header = []
Header = next(cr)

rows =[]

for row in cr :
    rows.append(row)
Participants = []

for i in range(12):

    Participants.append([])
    Participants[i].append(rows[35*i][11])
    Participants[i].append(rows[35 * i+1][11])


Temps = []

for k in range(30):
    Temps.append([])

    for i in range(12):
        if unidecode.unidecode(rows[5+k+35*i][11].upper()).replace(" ","") in ListeRep[k]:
            ch1 = rows[4+k+35*i][10]
            ch2 = rows[5+k+35*i][10]
            t2 = int(ch2[14:].split(":")[0])*60+int(ch2[14:].split(":")[1])
            t1 = int(ch1[14:].split(":")[0])*60+int(ch1[14:].split(":")[1])
            Temps[k].append(t2 - t1)
        else :
            Temps[k].append(False)



import statistics

TempsMoyen = []
Liste_nb_false = []

for i in range(30):
    m = 0
    k = 0
    nbfalse = 0
    for j in range(12):
        if Temps[i][j] != 0:
            m = m + Temps[i][j]
            k = k + 1
        else:
            nbfalse = nbfalse + 1
    if k == 0 :
        k = 1

    TempsMoyen.append(m/k)
    Liste_nb_false.append(nbfalse)




def triListe(TempsMoyen,ListeQuesti):
    TmoyCopy = TempsMoyen.copy()
    ListeQuestiCopy = ListeQuesti.copy()
    Liste_nb_falseCopy = Liste_nb_false.copy()

    for i in range(1,len(TempsMoyen)):
        for j in range(0,i):
            if TmoyCopy[i] < TmoyCopy[j] :
                TmoyCopy.insert(j,TmoyCopy[i])
                ListeQuestiCopy.insert(j, ListeQuestiCopy[i])
                Liste_nb_falseCopy.insert(j, Liste_nb_falseCopy[i])
                del TmoyCopy[i+1]
                del ListeQuestiCopy[i + 1]
                del Liste_nb_falseCopy[i + 1]
                break
    return TmoyCopy,ListeQuestiCopy,Liste_nb_falseCopy

TmoyCopy,ListeQuestiCopy, Liste_nb_falseCopy= triListe(TempsMoyen,ListeQuesti)

for i in range(len(TmoyCopy)):
    print(str(ListeQuestiCopy[i]) + " : " + str(TmoyCopy[i]) + " et nombre de bonne réponse : " + str((1-Liste_nb_falseCopy[i]/12)*100)+ "%")


TempsReflexionEstime =[]

