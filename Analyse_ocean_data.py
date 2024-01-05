import csv
import numpy as np

#Les questions présentes dans le test OCEAN

"Êtes-vous une femme ou un homme ?"
"Quel est votre date de naissance ?"
"Avez-vous déjà passé un test OCEAN auparavant ?"

#Question OCEAN :
#O  Ouverture à l'expérience (Originalité)
#C	Consciencieusité (Contrôle, Contrainte)
#E	Extraversion (Énergie, Enthousiasme)
#A	Agréabilité (Altruisme, Affection)
#N	Neuroticisme ou névrotisme (émotions Négatives, Nervosité)

#Est noté positivement ce qui augmente le score dans cette catégorie et négativement ce qui diminue le score dans celle-ci
questions = ["1 - Est volubile (aime parler) :",   #Extraversion +, [0,0,1,0,0]
"2- A tendance à remarquer les défauts des autres", #Agréabilité -,[0,0,0,-1,0]
"3 - Fait du bon travail", #Consciencieusité +, [0,1,0,0,0]
"4- Est déprimée, mélancolique", #Neuroticisme +,[0,0,0,0,1]
"5- Est original(e), a des idées nouvelles", #Ouverture à l'expérience +,[1,0,0,0,0]
"6- Est réservé(e)", #Extraversion - [0,0,-1,0,0]
"7- Est serviable et généreux avec les autres", #Agréabilité +, [0,0,0,1,0]
"8- Peut être un peu négligent(e)", #Consciencieusité -, [0,-1,0,0,0]
"9- Est relaxe, détendu(e), gère bien le stress", #Neuroticisme -,[0,0,0,0,-1]
"10- Est curieux(se) à propos de plusieurs choses différentes", #Ouverture à l'expérience +,[1,0,0,0,0]
"11- Est plein(e) d'énergie", #Extraversion +, [0,0,1,0,0]

"1- Provoque des disputes avec les autres", #Agréabilité -, [0,0,0,-1,0]
"2- Est un travailleur(se) fiable", #Consciencieusité +,[0,1,0,0,0]
"3- Peut être tendu(e)", #Névrotisme +, [0,0,0,0,1]
"4- Est ingénieux(se), pense beaucoup", #Ouverture à l'expérience +, [1,0,0,0,0]
"5- Communique beaucoup d'enthousiasme", #Agréabilité + Extraversion+, [0,0,1,1,0]
"6- Est de nature indulgente (a tendance à pardonner)", #Agréabilité +, [0,0,0,1,0]
"7- A tendance à être désorganisé(e)", #Consciencieusité -,[0,-1,0,0,0]
"8- S'inquiète beaucoup", #Neuroticisme +,[0,0,0,0,1]
"9- A une imagination active", #Ouverture à l'expérience +,[1,0,0,0,0]
"10- A tendance à être tranquille, silencieux(se)", #Extraversion -, névrotisme -, [0,0,-1,0,-1]
"11- Fait généralement confiance aux autres", #Agréabilité +,[0,0,0,1,0]

"1- A tendance à être paresseux(se)", #Consciencieusité -,[0,-1,0,0,0]
"2- Est stable émotivement, n'est pas facilement perturbé(e)", #Neuroticisme -,[0,0,0,0,-1]
"3- Est inventif(ve)", #Ouverture à l'expérience +,[1,0,0,0,0]
"4- S'affirme", #Extraversion +, [0,0,1,0,0]
"5- Peut être froid(e) et distant(e)", #Extraversion -, Neuroticisme+, [0,0,-1,0,1]
"6- Persévère jusqu'à ce que la tâche soit terminée", # Consciencieusité +, [0,1,0,0,0]
"7- Peut être de mauvaise humeur", # Neuroticisme +, Agréabilité -, [0,0,0,-1,1]
"8- Valorise les expériences artistiques, esthétiques", #Ouverture à l'expérience +,[1,0,0,0,0]
"9- Est parfois timide, inhibé(e)", #Extraversion -, [0,0,-1,0,0]
"10- Est prévenant(e) et gentil(le) avec presque tout le monde", #Agréabilité +,[0,0,0,1,0]
"11- Fait les choses efficacement", #Consciencieusité +, [0,1,0,0,0]

"1- Reste calme dans les situations tendues", #névrotisme -, Consciencieusité +,[0,1,0,0,-1]
"2- Préfère le travail routinier", #Ouverture à l'expérience -,[-1,0,0,0,0]
"3- Est ouvert(e), sociable", #Agréabilité +,Extraversion +, [0,0,1,1,0]
"4- Est parfois rude avec les autres", # Agréabilité -,[0,0,0,-1,0]
"5- Fait des plans et les suit", #Consciencieusité +,[0,1,0,0,0]
"6- Devient facilement nerveux(se)", #Neuroticisme+, [0,0,0,0,-1]
"7- Aime réfléchir, jouer avec les idées", #Ouverture à l'expérience +, [1,0,0,0,0]
"8- A peu d'intérêts artistiques", #Ouverture à l'expérience -, [-1,0,0,0,0]
"9- Aime coopérer avec les autres", #Agréabilité + , Extraversion +,[0,0,1,1,0]
"10- Est facilement distrait(e)", #Consciencieusité -, [0,-1,0,0,0]
"11- Est sophistiqué(e) en ce qui concerne les arts, la musique et la littérature" #Ouverture à l'expérience +, [1,0,0,0,0]
]
#On créée des np.array sous la forme [0,0,0,0,0] de taille la valeur associée dans le test OCEAN, ex : Agréabilité + = [0,0,0,1,0], ou
# Agréabilité +,Extraversion + = [0,0,1,1,0]
Point_questions = [[0,0,1,0,0],[0,0,0,-1,0],[0,1,0,0,0],[0,0,0,0,1],[1,0,0,0,0],[0,0,-1,0,0],[0,0,0,1,0],[0,-1,0,0,0],[0,0,0,0,-1],[1,0,0,0,0],[0,0,1,0,0],
                   [0,0,0,-1,0],[0,1,0,0,0],[0,0,0,0,1],[0,0,1/2,1/2,0],[0,0,0,1,0],[0,-1,0,0,0],[0,0,0,0,1],[0,0,0,0,-1],[1,0,0,0,0],[0,0,-1/2,0,-1/2],[0,0,0,1,0],
                    [0,-1,0,0,0],[0,0,0,0,-1],[1,0,0,0,0],[0,0,1,0,0],[0,0,-1/2,0,1/2],[0,1,0,0,0],[0,0,0,-1/2,1/2],[1,0,0,0,0],[0,0,-1,0,0],[0,0,0,1,0],[0,1,0,0,0],
                    [0,1/2,0,0,-1/2],[-1,0,0,0,0],[0,0,1/2,1/2,0],[0,0,0,-1,0],[0,1,0,0,0],[0,0,0,0,-1],[1,0,0,0,0],[-1,0,0,0,0],[0,0,1/2,1/2,0],[0,-1,0,0,0],[1,0,0,0,0]
]

#Reponse max du test
array_p= [0]*44
for i in range(len(Point_questions)):
    array_p[i]=np.array(Point_questions[i])
a=0
for i in range(len(array_p)):
    a = a + array_p[i]
#Max = array([ 5. ,  1.5,  1.5,  2. , -1. ]) #Tout à fait d'accord à toute les réponses


Chemin = "/Volumes/Samsung_T5/Projet Recherche Maîtrise/Analyse_OCEAN_data/survey.user_input_6h.csv"
fichier = open(Chemin,"r")
cr = csv.reader(fichier, delimiter = ";")

Header = []
Header = next(cr)

rows = []

for row in cr :
    rows.append(row)
Participants = []
Nb_parti_in_file = int(len(rows)/47)
for i in range(Nb_parti_in_file): #Nombre de participants
    Participants.append([])
    for j in range(47): #Nombre de ligne par participant : 44 questions à choix multiple + 3 questions
        if j==1 :
            Participants[i].append(rows[j+i*47][11]) #Date de naissance pas sur la même colonne
        else:
            Participants[i].append(rows[j + i * 47][10])


for i in range(Nb_parti_in_file):
    for j in range(44):
        if Participants[i][j + 3] == "Fortement en accord":
            Participants[i][j + 3] = 4
        elif Participants[i][j + 3] == "Modérément en accord":
            Participants[i][j + 3] = 3
        elif Participants[i][j + 3] == "Modérément en en accord": #léger bug de double "en en"
            Participants[i][j + 3] = 3
        elif Participants[i][j + 3] == "Ni en accord, ni en désaccord":
            Participants[i][j + 3] = 2
        elif Participants[i][j + 3] == "Modérément en désaccord":
            Participants[i][j + 3] = 1
        elif Participants[i][j + 3] == "Modérément en en désaccord": #léger bug de double "en en"
            Participants[i][j + 3] = 1
        elif Participants[i][j + 3] == "Fortement en désaccord":
            Participants[i][j + 3] = 0

#Compte score max possible
Range_max = []
for i in range(5):
    Range_max.append([])
    max = 0
    min = 0
    for j in range(len(Point_questions)):
        if Point_questions[j][i] > 0 :
            max = max + Point_questions[j][i]
        else :
            min = min + Point_questions[j][i]
    print(max)
    print(min)
    Range_max[i].append(min*4)
    Range_max[i].append(max*4)




score_participant = []
for i in range(Nb_parti_in_file):
    score_participant.append(np.array([0, 0, 0, 0, 0]))
    for j in range(44):
        score_participant[i] = score_participant[i] + Participants[i][j + 3] * np.array(Point_questions[questions.index(rows[j + 3 + 47 * i][14])])

for i in range(Nb_parti_in_file):
    for j in range(5):
        score_participant[i][j] = (score_participant[i][j] + (-1)*Range_max[j][0])/(Range_max[j][1]+ (-1)*Range_max[j][0])*5



np.savetxt("/Volumes/Samsung_T5/Projet Recherche Maîtrise/Analyse_OCEAN_data/score_participant_1.txt",score_participant)

import seaborn as sn
import matplotlib.pyplot as plt
import scipy
#sn.heatmap(np.corrcoef([[score_participant[i][j] for i in range(len(score_participant))] for j in range(5)]), xticklabels=["O","C","E","A","N"], yticklabels=["O","C","E","A","N"], annot=True, fmt=".1f")



sn.jointplot(x=[score_participant[i][0] for i in range(len(score_participant))],y=[score_participant[i][3] for i in range(len(score_participant))],
                  kind="reg", truncate=False,color="#f4835b", height=7)

#plt.savefig('/Volumes/Samsung_T5/Projet Recherche Maîtrise/Graph_article/Carte_corr_OCEAN_11sub.jpg')

# Correlation entre les réponses et le test OCEAN

Chemin1 = "/Volumes/Samsung_T5/Projet Recherche Maîtrise/Analyse_OCEAN_data/Time_rep_Ctrl_test.csv"

fichier1 = open(Chemin1,"r")
cr1 = csv.reader(fichier1, delimiter = ";")

Header1 = []


rows1 = []

for row in cr1 :
    rows1.append(row)

Participants_time = []

for i in range(int(len(rows1)/5)):
    Participants_time.append([])
    for j in range(5):
        Participants_time[i].append(str(rows1[i*5+j][0]) if len(rows1[i*5+j])==1 else 0 )

#Liste des temps et des scores OCEAN combinés
print(1)
Data_prep = [[] for i in range(6)]
for i in range(len(Participants_time)):
    for j in range(5):
        Data_prep[0].append(float(Participants_time[i][j].replace(",",".")) if  isinstance(Participants_time[i][j],str) else Participants_time[i][j])
        for k in range(1,6):
            Data_prep[k].append(score_participant[i][k-1])
import scipy
#scipy.stats.pearsonr(Data_prep[0],Data_prep[1])
#scipy.stats.pearsonr(Data_prep[0],Data_prep[2])
#scipy.stats.pearsonr(Data_prep[0],Data_prep[3])
#scipy.stats.pearsonr(Data_prep[0],Data_prep[4])
#scipy.stats.pearsonr(Data_prep[0],Data_prep[5])

#Data_prep sans les fausses réponses (c'est à dire sans les temps de 20

Data_prep_120 = [[] for i in range(6)]

for j in range(len(Data_prep[0])):
    if Data_prep[0][j] < 20:
        for k in range(6):
            Data_prep_120[k].append(Data_prep[k][j])

#Data_prep avec booleen des réponses "Réponse vraie"
Data_prep_bool = [[] for i in range(6)]

for j in range(len(Data_prep[0])):
    if Data_prep[0][j] < 20:
        Data_prep_bool[0].append(1)
        for k in range(1,6):
            Data_prep_bool[k].append(Data_prep[k][j])
    else:
        Data_prep_bool[0].append(0)
        for k in range(1, 6):
            Data_prep_bool[k].append(Data_prep[k][j])

#Corrélation avec les erreurs de consignes

Parti_err_consigne = [0,2,4,1,2,5,6,3,0,2,0,2,3,2]
L_OCEAN = [[score_participant[i][j] for i in range(len(score_participant))] for j in range(5)] #score des particpants regroupé par catégorie
sn.heatmap([[scipy.stats.spearmanr(L_OCEAN[i],L_OCEAN[j])[0] for i in range(5)] for j in range(5)], xticklabels=["O","C","E","A","N"], yticklabels=["O","C","E","A","N"], annot=True, fmt=".1f")
plt.title("Carte des corrélations entre chaque axe du test OCEAN")
#scipy.stats.pearsonr(Parti_err_consigne,Data_prep[1])

#Corre entre groupe et test OCEAN

Parti_group_bool = [0,1,1,0,0,1,1,0,1,1,0,0,0,1]




Score_ctrl_O = [3.888888889,3.333333333,4.166666667,5,3.888888889,3.055555556,3.888888889]
Score_ctrl_C = [3.75,2.763157895,3.947368421,2.697368421,3.157894737,2.565789474,3.486842105]
Score_ctrl_E = [2.666666667,3.666666667,2.5,2.833333333,3.333333333,1.416666667,1.75]
Score_ctrl_A = [3.541666667,3.75,3.958333333,4.166666667,3.611111111,2.5,3.333333333]
Score_ctrl_N = [1.944444444,1.944444444,2.708333333,2.152777778,1.944444444,2.222222222,3.055555556]
Time_ctrl = [11.08467364,7.284459829,14.22349653,7.569649506,7.002228021,5.448309231,10.2926115]

Score_LH_O = [4.444444444,3.611111111,2.361111111,3.194444444,4.583333333,2.222222222,2.222222222]
Score_LH_C = [2.697368421,3.157894737,3.026315789,3.289473684,3.618421053,3.75,1.644736842]
Score_LH_E = [1.916666667,3.833333333,2.5,2.25,4.5,2.25,2]
Score_LH_A = [2.99,3.819444444,3.333333333,2.638888889,4.236111111,2.222222222,2.430555556]
Score_LH_N = [2.291666667,1.458333333,2.083333333,2.847222222,2.638888889,1.944444444,3.055555556]
Time_LH = [11.1027261,10.48813248,11.68079653,16.77039685,12.88549709,13.03474317,15.7090745]



print(1)


