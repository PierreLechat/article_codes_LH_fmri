from tkinter import Label, Tk
import time
import os
import datetime

ListeAnagram = [["SECRET", "POULE", "GARE"],
                ["PURE", "OPERA", "BEAU"],
                ["DIETE", "DIGUE", "RECENT"],
                ["SPORE", "DESIR", "MARCHE"],
                ["OSER", "MAIS", "DEMON"]]

ListeRate = [["SECRET : 60%", " POULE : 90% ", " GARE : 83% "],
             [" PURE : 67% ", " OPERA : 75% ", "BEAU : 97% "],
             ["DIETE : 95% ", "DIGUE : 78% ", "RECENT : 75% "],
             ["SPORE : 67% ", "DESIR : 60% ", "MARCHE : 70% "],
             ["OSER : 92% ", "MAIS : 93% ", " DEMON : 92% "]
             ]

app_window = Tk()
app_window.title("Anagramme")
app_window.attributes('-fullscreen', True)

Time = time.time()

Repertoire = "/Volumes/Samsung_T5/Projet Recherche Maîtrise/AfficheurAnagramme/sub-"
n = 1
Daydate = datetime.date.today()

while os.path.exists(Repertoire + str(n) + "-(" + str(Daydate) + ").txt"):
    n = n + 1

fichier = open(Repertoire + str(n) + "-(" + str(Daydate) + ").txt", "x")
fichier.write("Temps(s)" + "    " + "Event" + "    " + "WordDisplay" + "\r")


class Texte:
    def __init__(self, fichier, Time):

        self.fichier = fichier
        self.Time = Time
        self.enterbool = False
        self.t_enterbool = None
        self.t_suivi = 0
        # Liste des temps où l'experimentateur fait le suivi des réponses aux anagrammes avec le participant
        self.list_t_suivi = []

        self.list_TR = [0]
        self.TR_bool = False
        text_font = ("Boulder", 100, 'bold')
        background = "#FFFFFF"
        foreground = "#000000"
        self.label = Label(font=text_font, bg=background, fg=foreground)
        self.label1 = Label(font=("Boulder", 67, 'bold'), bg="#FFFFFF", fg="#000000")
        self.label2 = Label(font=("Boulder", 67, 'bold'), bg="#FFFFFF", fg="#000000")
        self.label3 = Label(font=("Boulder", 67, 'bold'), bg="#FFFFFF", fg="#000000")

    def affichage(self):
        # Temps d'arrière plan
        t = time.time() - self.Time

        if t - self.list_TR[-1] > 3 and self.TR_bool == False:
            self.TR_bool = True
            fichier.write(str(t) + "    "+ "entrée Attente TR"+ "\r")

        # temps permettant de piloter les séquences
        # Affichage en pause si l'IRM ne réalise plus l'acquisition
        if not self.enterbool and (not self.TR_bool or 4 <= self.t_enterbool % 89 < 89):
            self.t_enterbool = t - sum(self.list_t_suivi)


        seq = int(self.t_enterbool // 89)
        app_window.bind('<KeyPress>', lambda event: self.frappesaver(event, t, self.t_enterbool, self.fichier))
        app_window.bind('<Escape>', lambda escape: self.close(escape))
        app_window.bind('<Return>', lambda enter: self.suivireponse(enter, t))

        if self.enterbool:
            self.label.config(text="")
            self.label.place(relx=0.5, rely=0.5, anchor="center")
            self.label.after(50, self.affichage)

        elif 4 <= self.t_enterbool % 89 < 64 and not self.enterbool:

            self.label.config(text=ListeAnagram[seq][int(self.t_enterbool % 89 - 4) // 20])
            self.label.place(relx=0.5, rely=0.5, anchor="center")
            self.label.after(50, self.affichage)

        elif 64 <= self.t_enterbool % 89 < 79 and not self.enterbool:
            self.label.config(text="")
            self.label.place(relx=0.5, rely=0.5, anchor="center")
            self.label.after(50, self.affichage)

        elif 79 <= self.t_enterbool % 89 < 89 and not self.enterbool:
            self.label1.config(text=ListeRate[seq][0])
            self.label1.place(relx=0.5, rely=0.3, anchor="center")
            self.label2.config(text=ListeRate[seq][1])
            self.label2.place(relx=0.5, rely=0.5, anchor="center")
            self.label3.config(text=ListeRate[seq][2])
            self.label3.place(relx=0.5, rely=0.7, anchor="center")
            self.label1.after(50, self.affichage)

        elif 0 <= self.t_enterbool % 89 < 4 and not self.enterbool:
            self.label.config(text="*")
            self.label.place(relx=0.5, rely=0.5, anchor="center")

            self.label1.destroy()
            self.label2.destroy()
            self.label3.destroy()

            self.label1 = Label(font=("Boulder", 67, 'bold'), bg="#FFFFFF", fg="#000000")
            self.label2 = Label(font=("Boulder", 67, 'bold'), bg="#FFFFFF", fg="#000000")
            self.label3 = Label(font=("Boulder", 67, 'bold'), bg="#FFFFFF", fg="#000000")

            self.label.after(50, self.affichage)
        elif self.t_enterbool > 445:
            fichier.close()

    def frappesaver(self, event, t, t_enterbool, fichier):
        if event.char == "T":
            self.list_TR.append(t)

            if self.TR_bool == True and t_enterbool % 89 < 4:
                self.list_t_suivi.append(t - t_enterbool - sum(self.list_t_suivi))
                self.TR_bool = False
                fichier.write(str(t) + "    "+"sortie Attente TR"+ "\r")


        if 4 < int(t_enterbool % 89) < 64:
            fichier.write(str(t) + "    " + event.char + "    " + ListeAnagram[int(t_enterbool // 89)][
                int(t_enterbool % 89 - 4) // 20] + "\r")
        elif 64 <= int(t_enterbool % 89) < 79:
            fichier.write(str(t) + "    " + event.char + "    " + "/""/" + "\r")
        elif 79 <= int(t_enterbool % 89) < 89 or int(t_enterbool % 89) < 4:
            fichier.write(str(t) + "    " + event.char + "    " + "Res" + "\r")

        self.affichage()

    def suivireponse(self, enter, t):
        if not self.enterbool:
            fichier.write(str(t) + "    " + "entrée Attente espace"+ "\r")
            self.list_t_suivi.append(time.time() - self.Time)
        elif self.enterbool:
            fichier.write(str(t) + "    " + "sortie Attente espace"+ "\r")
            self.list_t_suivi[-1] = time.time() - self.Time - self.list_t_suivi[-1]

        self.enterbool = not self.enterbool
        fichier.write(str(t) + "    " + "enter" + "    " + "Answer_moment" + "\r")
        self.affichage()

    def close(self, escape):
        print(escape.char)
        # fichier.write(str(t) + "Info complémentaire :" + "\r" + "Liste TR :"+ str(self.list_TR) + "\r" + "Liste TR :"+ str(self.list_TR) )
        fichier.close()
        app_window.destroy()


Texteaff = Texte(fichier, Time)

Texteaff.affichage()
app_window.mainloop()
