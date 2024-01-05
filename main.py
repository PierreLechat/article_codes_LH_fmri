# Load the NeuroKit package
import neurokit2 as nk
#import os
#import csv
import time
import numpy as np
import seaborn as sn
from matplotlib import pyplot as plt
#from itertools import chain
import pandas as pd
import seaborn as sns
#bash : accès au bon dossier:  cd ../../Volumes/Samsung_T5/Projet\ Recherche\ Maîtrise/Analyse_signal_EDA

#Sujet d'étude
global subject_n
subject_n = "ImpAcq_01"

#Nombre de volume par sujet
global number_volumes
if subject_n == "ImpAcq_01":
    number_volumes= 20
else :
    number_volumes = 22


#Chemin d'accès vers le dossier où sont stockées les données pour chaque participants aux formats (ImpAcq_01 ... ImpAcq_20)

global path_acces_data
path_access_data = "/Volumes/Samsung_T5/Projet Recherche Maîtrise/Analyse_signal_EDA/"

#Lien d'accès aux fichiers :
global path_fichier_txt_eda_trig
path_fichier_txt_eda_trig = path_access_data+ subject_n +"/"+ subject_n +"_eda_trig.csv"
# "/Volumes/Samsung_T5/Projet Recherche Maîtrise/Analyse_signal_EDA/ImpAcq_01/eda_signal.txt"
global path_saved_eda
path_saved_eda =path_access_data+ subject_n +"/eda_signal.txt"

#"/Volumes/Samsung_T5/Projet Recherche Maîtrise/Analyse_signal_EDA/ImpAcq_01/trigger_signal.txt"
global path_saved_trig
path_saved_trig = path_access_data+ subject_n +"/trigger_signal.txt"



# Seq_1 = trigger_signal[13050000:13700000] , eda_signal[13050000:13700000]
# Seq_resolution = []



class Seance:
    def __init__(self):
        self.path_fichier_txt_eda_trig = path_fichier_txt_eda_trig

    def save_txt2array(self):
        self.file = open(self.path_fichier_txt_eda_trig, 'r') #Warning ImpAcq_01 saved en txt avec délimiteur espace
        self.eda_signal = []
        self.trigger_signal = []
        for line in self.file:
            self.trigger_signal.append(float(line.split("\t")[0]))
            self.eda_signal.append(float(line.split("\t")[1]))
        self.eda_signal = np.array(self.eda_signal)
        self.trigger_signal = np.array(self.trigger_signal)
        np.savetxt(path_saved_eda,self.eda_signal)
        np.savetxt(path_saved_trig,self.trigger_signal)

    def load_array(self):
        self.eda_signal = np.loadtxt(path_saved_eda)
        self.trigger_signal = np.loadtxt(path_saved_trig)


    def identification_seq(self):
        self.L_seq_trigger = [[]]
        self.L_seq_eda = [[]]
        k = 0
        p = 0
        for i in range(1, len(self.trigger_signal)):

            if 3 < self.trigger_signal[i] < 6 and not (3 < self.trigger_signal[i - 1] < 6):
                m = i

                #Récupération des données avant le début de séquence afin d'observe
                # if k == 0 and p == 0:
                #     self.L_seq_trigger[k] = list(self.trigger_signal[m-1])
                #
                #     self.L_seq_eda[k]= list(self.eda_signal[m-1])

                while 3 < self.trigger_signal[m] < 6 and m < len(self.trigger_signal):
                    self.L_seq_trigger[k].append(self.trigger_signal[m])
                    self.L_seq_eda[k].append(self.eda_signal[m])

                    m = m + 1
                while not (3 < self.trigger_signal[m] < 6) and m-i < 30000 and m < len(self.trigger_signal):
                    self.L_seq_trigger[k].append(self.trigger_signal[m])
                    self.L_seq_eda[k].append(self.eda_signal[m])
                    m = m + 1

                p = p + 1
                print( "p =", p)
                print("k =", k)
            if p == number_volumes and k<6:
                self.L_seq_trigger.append([])
                self.L_seq_eda.append([])
                k = k + 1
                p = 0

    def save_seq(self):
        for i in range(6):
            np.savetxt(path_access_data+ subject_n +"/eda_signal_seq"+str(i)+".txt",self.L_seq_eda[i])

        for i in range(6):
            np.savetxt(path_access_data+ subject_n +"/trigger_signal_seq"+str(i)+".txt", self.L_seq_trigger[i])

    def load_seq(self):
        self.L_seq_trigger = [[]]*6
        self.L_seq_eda = [[]] * 6
        for i in range(6):
            self.L_seq_trigger[i] = np.loadtxt(path_access_data+ subject_n +"/trigger_signal_seq"+str(i)+".txt")
        for i in range(6):
            self.L_seq_eda[i] = np.loadtxt(path_access_data+ subject_n +"/eda_signal_seq"+str(i)+".txt")

    def frequ_ech(self): #Méthode qui était pertinente au début (oubli de la fréquence d'échantillonage), qui ne l'est plus
        trig_max = []
        n_trig_max = []

        for i in range(len(self.trigger_signal)):
            if 2 < self.trigger_signal[i] < 8:
                trig_max.append(self.trigger_signal[i])
                n_trig_max.append(i)

        ecart_n_trig_max = []
        for i in range(1, len(n_trig_max)):
            ecart_n_trig_max.append(n_trig_max[i] - n_trig_max[i - 1])
    def synchro(self):
        #Liste indice des trigger captés par le biopac
        self.i_trig = [0,1]
        for i in range(1,len(self.trigger_signal)):
            if self.trigger_signal[i] > 3:
                self.i_trig.append(i)
        del self.i_trig[0]
        del self.i_trig[0]
        liste_indice = []
        for j in range(len(self.i_trig) - 1):
            if self.i_trig[j] == self.i_trig[j + 1] - 1:
                liste_indice.append(j + 1)
        for j in range(len(liste_indice)):
            liste_indice[j] = liste_indice[j] - len(liste_indice[0:j])
        for j in range(len(liste_indice)):
            del self.i_trig[liste_indice[j]]
        np.savetxt(path_access_data+ subject_n +"/i_trig.txt",self.i_trig)

        #print("3*")
        #Ouverture du fichier de synchronisation
        df = pd.read_csv(path_access_data+ subject_n +"/"+ subject_n +"_press_file.csv",sep=";",header=0) # Warning séparateur peut changer ainsi que le type du fichier
        #Liste des temps à laquelle sont captés les TR
        self.List_time_TR =[]
        for i in range(len(df["Temps(s)"])):
            if df["Event"][i] == "T":
                self.List_time_TR.append(df["Temps(s)"][i])
        #Warning : étape particulière à au sujet numéro 1 : branchement usb du signal trigger tardif => capture de 11 trigger fictif qui n'existe pas dans le fichier texte du sub-01
        # for i in range(11):
        #     del self.List_time_TR[0]
        for i in range(len(self.List_time_TR)):
            self.List_time_TR[i] = self.List_time_TR[i] #Temps du début d'aquisition IRMf
        #division des temps TR en chaque séquence
        self.list_seq_time_TR = []
        #print("4*")
        for i in range(5):
            self.list_seq_time_TR.append([])
            for j in range(number_volumes):
                self.list_seq_time_TR[i].append(self.List_time_TR[number_volumes*i+j])

        #Identification du premier temps TR selon la séquence (car première séquence, enregistrement de multiple entrée clavier "T" sans volume associé)
        if subject_n != "ImpAcq_01":
            for i in range(len(df["Event"])):
                if df["Event"][i] == "T":
                    First_T_time = df["Temps(s)"][i]
                    break
        else:
            First_T_time = 84.77945685386658

        # Liste des 1er TR de chaque début de séquence
        self.list_time_start_seq = [First_T_time] #Temps à laquelle est présenté le premier stimulus  #t_1st_event_ImpAcq_01 = 84.77945685386658
        for i in range(len(df["Event"])):
            if df["Event"][i] == "T" and df["WordDisplay"][i] == "Res" and df["Temps(s)"][i] > self.list_time_start_seq[-1] + 4:
                self.list_time_start_seq.append(df["Temps(s)"][i] + 4)

        self.list_time_display =[]
        for i in range(len(self.list_time_start_seq)):
            self.list_time_display.append(self.list_time_start_seq[i])
            self.list_time_display.append(self.list_time_start_seq[i] + 20)
            self.list_time_display.append(self.list_time_start_seq[i] + 40)
        #print(4)
        #Ajout du début de la séquence RS


        # Création liste des temps synchro avec chaque séquence EDA
        list_seq_temps_sync = []
        for i in range(5):
            list_seq_temps_sync.append(np.linspace(self.list_seq_time_TR[i][0],
                                                   self.list_seq_time_TR[i][number_volumes - 1] + 3,
                                                   len(self.L_seq_eda[i])
                                                   ))

        #liste des temps ou le bouton est pressé
        self.list_press_d_time = []
        for i in range(len(df["Event"])):
            if df["Event"][i] == "d" : #2eme éléments de la condition qui ne fonctionne que pour le 1st subject (and df["Temps(s)"][i] > 88)
                self.list_press_d_time.append(df["Temps(s)"][i])

        #Booléen si le ieme event a reçu une reponse (pression sur le bouton "d")
        self.rep_bool = []
        k = 0
        for i in range(len(self.list_time_display) - 1):
            if k < len(self.list_press_d_time) and (self.list_press_d_time[k] > self.list_time_display[i]) and (self.list_press_d_time[k] < self.list_time_display[i] + 20):
                self.rep_bool.append(True)
                k = k + 1
            else:
                self.rep_bool.append(False)
        if self.list_time_display[-1] < self.list_press_d_time[-1]:
            self.rep_bool.append(True)
        else:
            self.rep_bool.append(False)


        # Bouton pressé séparé en séquence
        k = 0
        self.list_seq_press_d_time = []
        for i in range(5):
            self.list_seq_press_d_time.append([])
            for j in range(3):
                if self.rep_bool[i * 3 + j]:
                    self.list_seq_press_d_time[i].append(self.list_press_d_time[k])
                    k = k + 1

        # linspace du temps du 1er TR à la fin de la liste en temps (s)
        self.List_synchro_time = np.linspace(self.List_time_TR[0], self.List_time_TR[0] +
                                             (self.List_time_TR[1] - self.List_time_TR[0]) /
                                             (self.i_trig[1] - self.i_trig[0])
                                             * (len(self.eda_signal) - self.i_trig[0]),
                                             len(self.eda_signal) - self.i_trig[0])
        #Liste de temps synchronisé avec chacune des séquences finissant 3 sc après le dernier TR
        self.list_seq_temps_sync = []
        for i in range(5):
            self.list_seq_temps_sync.append(np.linspace(self.list_seq_time_TR[i][0],
                                                   self.list_seq_time_TR[i][number_volumes - 1] + 3,
                                                   len(self.L_seq_eda[i])
                                                   ))
        self.list_time_start_seq_true = []
        for i in range(5):
            self.list_time_start_seq_true.append([])
            for j in range(3):
                if self.rep_bool[i * 3 + j]:
                    self.list_time_start_seq_true[i].append(self.list_time_display[i * 3 + j])
        self.list_i_time_start_seq_true = []
        for i in range(5):
            self.list_i_time_start_seq_true.append([])
            for j in range(len(self.list_time_start_seq_true[i])):
                self.list_i_time_start_seq_true[i].append(
                    (self.list_time_start_seq_true[i][j] - self.list_time_start_seq[i]) * 10000)

    def preproc_eda(self):
        self.phasic_signal_seq = []
        for i in range(5):
            signals, info = nk.eda_process(self.L_seq_eda[i], sampling_rate=10000)
            self.phasic_signal_seq.append(signals["EDA_Phasic"].values.tolist())


    def plot_seq_n(self,n,signal_type): #Plot la n iéme séquence du sujet chargé au début du code
        signals, info = nk.eda_process(self.L_seq_eda[n], sampling_rate=10000)
        plt.plot(self.list_seq_temps_sync[n], signals[signal_type])
        plt.title('Signal EDA -' + " séquence n°" + str(n+1), fontsize=15)
        plt.xlabel('Temps [s]')
        plt.ylabel('Intensité')
        for i in range(len(self.list_seq_press_d_time[n])):
            plt.axvline(x=self.list_seq_press_d_time[n][i], color='r')
            plt.text(self.list_seq_press_d_time[n][i] - 3, max(signals[signal_type]), "Press " + str(i + 1),
                     bbox=dict(facecolor='white', edgecolor='red', pad=5.0
                               ))
        for i in range(3):
            plt.axvline(x=self.list_time_display[i + 3 * n], color='b')
            plt.text(self.list_time_display[n * 3 + i] - 3, min(signals[signal_type]), "Event " + str(i + 1),
                     bbox=dict(facecolor='white', edgecolor='blue', pad=5.0
                               ))

    def boxplot_seq_sub_n(self):
        #Sont séparés (ppur idnetification) les intensités du signal phasique au sein de chaque séquence entre la phase de réflexion et la phase de non-réflexion
        self.seq_eda_IsThinking = []
        self.seq_eda_NotThinking = []
        #Même chose pour les peaks, heights des peaks et leurs amplitudes
        seq_bool_scr_peaks_Isth = []
        seq_bool_scr_peaks_Noth = []
        seq_scr_amplitude_Isth = []
        seq_scr_amplitude_Noth = []
        seq_scr_Height_Isth = []
        seq_scr_Height_Noth = []
        seq_number_peak_Isth = []
        seq_number_peak_Noth = []

        for seq in range(5):
            # Création liste des positions des event dans les epochs
            n_event_position = [(int(self.list_time_display[3 * seq] - self.list_seq_temps_sync[seq][0]) * 10000),
                                int((self.list_time_display[1 + 3 * seq] - self.list_seq_temps_sync[seq][0]) * 10000),
                                int((self.list_time_display[2 + 3 * seq] - self.list_seq_temps_sync[seq][0]) * 10000)]
            n_press_position = []
            for i in range(len(self.list_seq_press_d_time[seq])):
                n_press_position.append(int((self.list_seq_press_d_time[seq][i] - self.list_seq_temps_sync[seq][0]) * 10000))
                
            # Création de l'array avec signal dans A = "Is thinking to a solution" ou dans !A pour fit avec seaborn (création de boîte)
            signals, info = nk.eda_process(self.L_seq_eda[seq], sampling_rate=10000)

            #Enregistrement des différentes données d'intérêts
            L_signals = signals["EDA_Phasic"].values.tolist()
            L_bool_scr_peaks = signals['SCR_Peaks'].values.tolist()
            L_scr_amplitude = signals['SCR_Amplitude'].values.tolist()
            L_scr_SCR_Height = signals['SCR_Height'].values.tolist()

            #Liste dans lesquelles les différentes séquences des signaux sont enregistrées
            seq_eda_IsThinking_n = []
            seq_eda_NotThinking_n = []
            seq_bool_scr_peaks_Isth_n = []
            seq_bool_scr_peaks_Noth_n = []
            seq_scr_amplitude_Isth_n = []
            seq_scr_amplitude_Noth_n = []
            seq_scr_Height_Isth_n = []
            seq_scr_Height_Noth_n = []

            n_False = 0 #Evite les erreurs d'incréments dues à l'absence de réponses à l'event et donc l'absence dans la liste n_press_position
    
            for i in range(3):
                if self.rep_bool[3 * seq + i] == True: #La condition parcourt la liste comportant le booleen "La réponse a été trouvée pendant la présentation de l'event, exprimé par l'appuie sur le bouton" == True
                    #Remplissage de la liste de l'Event "Is Thinking"
                    seq_eda_IsThinking_n.append(L_signals[n_event_position[i]:n_press_position[i - n_False]])
                    seq_bool_scr_peaks_Isth_n.append(L_bool_scr_peaks[n_event_position[i]:n_press_position[i - n_False]])
                    seq_scr_amplitude_Isth_n.append(L_scr_amplitude[n_event_position[i]:n_press_position[i - n_False]])
                    seq_scr_Height_Isth_n.append(L_scr_SCR_Height[n_event_position[i]:n_press_position[i - n_False]])

                    # Remplissage de la liste de l'Event "Not Thinking"
                    if n_event_position[i] + 200000 < len(L_signals): #S'assure que pour le dernier Event de chaque séquence n'est pas séléctonné une plage de donnée plus grande que la mesure du signal IRM (pour travailler sur les mêmes plages de temps entre les deux analyses)
                        seq_eda_NotThinking_n.append(L_signals[n_press_position[i- n_False]:n_event_position[i] + 200000])
                        seq_bool_scr_peaks_Noth_n.append(L_bool_scr_peaks[n_press_position[i- n_False]:n_event_position[i] + 200000])
                        seq_scr_amplitude_Noth_n.append(L_scr_amplitude[n_press_position[i- n_False]:n_event_position[i] + 200000])
                        seq_scr_Height_Noth_n.append(L_scr_SCR_Height[n_press_position[i- n_False]:n_event_position[i] + 200000])

                    else:
                        seq_eda_NotThinking_n.append(L_signals[n_press_position[i - n_False]:])
                        seq_bool_scr_peaks_Noth_n.append(L_bool_scr_peaks[n_press_position[i - n_False]:])
                        seq_scr_amplitude_Noth_n.append(L_scr_amplitude[n_press_position[i - n_False]:])
                        seq_scr_Height_Noth_n.append(L_scr_SCR_Height[n_press_position[i - n_False]:])
                        
                else: #Si self.rep_bool[3 * seq + i] == False alors la réponse n'a pas été trouvée ainsi il n'y a pas de moment "Not thinking" décrit avec les conditions données dans le protocole
                    n_False = n_False + 1
                    if n_event_position[i] + 200000 < len(L_signals):
                        seq_eda_IsThinking_n.append(L_signals[n_event_position[i]:n_event_position[i] + 200000])
                        seq_bool_scr_peaks_Isth_n.append(L_bool_scr_peaks[n_event_position[i]:n_event_position[i] + 200000])
                        seq_scr_amplitude_Isth_n.append(L_scr_amplitude[n_event_position[i]:n_event_position[i] + 200000])
                        seq_scr_Height_Isth_n.append(L_scr_SCR_Height[n_event_position[i]:n_event_position[i] + 200000])

                    else:
                        seq_eda_IsThinking_n.append(L_signals[n_event_position[i]:])
                        seq_bool_scr_peaks_Isth_n.append(L_bool_scr_peaks[n_event_position[i]:])
                        seq_scr_amplitude_Isth_n.append(L_scr_amplitude[n_event_position[i]:])
                        seq_scr_Height_Isth_n.append(L_scr_SCR_Height[n_event_position[i]:])
                        
                        
            #Liste séparant les signaux selon l'évenement "Is Thinking" à travers Les séquences 1 à 5
            self.seq_eda_IsThinking.append(seq_eda_IsThinking_n)
            self.seq_eda_NotThinking.append(seq_eda_NotThinking_n)
            #Création de la liste nombre de peak dans l'évenement :
            seq_number_peak_Isth.append([[sum(seq_bool_scr_peaks_Isth_n[0])]*len(seq_bool_scr_peaks_Isth_n[0]),[sum(seq_bool_scr_peaks_Isth_n[1])]*len(seq_bool_scr_peaks_Isth_n[1]),[sum(seq_bool_scr_peaks_Isth_n[2])]*len(seq_bool_scr_peaks_Isth_n[2])]) #Création d'une liste de même taille composée des nombres de pics dans la dite séquence
            seq_number_peak_Noth_n = []
            if len(seq_bool_scr_peaks_Noth_n)>0:
                for i in range (len(seq_bool_scr_peaks_Noth_n)):
                    seq_number_peak_Noth_n.append([sum(seq_bool_scr_peaks_Noth_n[i])]*len(seq_bool_scr_peaks_Noth_n[i]))
            seq_number_peak_Noth.append(seq_number_peak_Noth_n)
            seq_bool_scr_peaks_Isth.append(seq_bool_scr_peaks_Isth_n)
            seq_bool_scr_peaks_Noth.append(seq_bool_scr_peaks_Noth_n)
            seq_scr_amplitude_Isth.append(seq_scr_amplitude_Isth_n)
            seq_scr_amplitude_Noth.append(seq_scr_amplitude_Noth_n)
            seq_scr_Height_Isth.append(seq_scr_Height_Isth_n)
            seq_scr_Height_Noth.append(seq_scr_Height_Noth_n)
            

        #Construction du dataframe pour coller ensuite à l'affichage avec seaborn
        IntensitySignal = []
        IsThinking = []
        Seq = []
        NumeroEvent = []
        Booleen_Peak = []
        Scr_amplitude = []
        Scr_height = []
        number_peak = []

        for i in range(len(self.seq_eda_IsThinking)):
            for j in range(len(self.seq_eda_IsThinking[i])):
                IntensitySignal.extend(self.seq_eda_IsThinking[i][j])
                IsThinking.extend("Yes" for _ in self.seq_eda_IsThinking[i][j])
                Seq.extend(i for _ in self.seq_eda_IsThinking[i][j])
                NumeroEvent.extend(j for _ in self.seq_eda_IsThinking[i][j])
                Booleen_Peak.extend(seq_bool_scr_peaks_Isth[i][j])
                Scr_amplitude.extend(seq_scr_amplitude_Isth[i][j])
                Scr_height.extend(seq_scr_Height_Isth[i][j])
                number_peak.extend(seq_number_peak_Isth[i][j])
                
        for i in range(len(self.seq_eda_NotThinking)):
            for j in range(len(self.seq_eda_NotThinking[i])):
                IntensitySignal = IntensitySignal + self.seq_eda_NotThinking[i][j]
                IsThinking = IsThinking + ["No"] * len(self.seq_eda_NotThinking[i][j])
                Seq = Seq + [i] * len(self.seq_eda_NotThinking[i][j])
                NumeroEvent = NumeroEvent + [j] * len(self.seq_eda_NotThinking[i][j])
                Booleen_Peak = Booleen_Peak + seq_bool_scr_peaks_Noth[i][j]
                Scr_amplitude = Scr_amplitude + seq_scr_amplitude_Noth[i][j]
                Scr_height = Scr_height + seq_scr_Height_Noth[i][j]
                number_peak = number_peak + seq_number_peak_Noth[i][j]

        self.df_signal = pd.DataFrame(data={"IntensitySignal": IntensitySignal, "IsThinking": IsThinking, "Seq": Seq,
                                                      "NumeroEvent": NumeroEvent,"Booleen_Peak" : Booleen_Peak,"Scr_amplitude" : Scr_amplitude,
                                                      "Scr_height": Scr_height, "number_peak" : number_peak})
        #sns.boxplot(data=df, x="IntensitySignal", y="IsThinking")
        #plt.show()
        #sns.boxplot(data=self.df_signal[(self.df_signal["Booleen_Peak"] == 1)], x="IntensitySignal", y="IsThinking") #Affiche seulement pour les peaks
        #sns.violinplot(data=self.df_signal[(self.df_signal["Booleen_Peak"] == 1)], x="Scr_amplitude", y="IsThinking")
        #print(5)
    def Open_all_sub_OCEAN(self):
        self.all_sub = pd.read_csv(
            "/Volumes/Samsung_T5/Projet Recherche Maîtrise/Analyse_signal_EDA/Multi_analyses/all_sub_df_OCEAN_10_02.csv",
            sep=",", header=0, index_col=0)
        del seance_01.all_sub['Unnamed: 0']
        self.all_sub_drop_dup = self.all_sub.drop_duplicates()
        #sn.heatmap(seance_01.all_sub_reduc.corr(), annot=True, fmt=".1f")

    def Reducing_all_sub(self):
        self.all_sub_reduc = self.all_sub.copy(deep=True)
        del seance_01.all_sub_reduc['Unnamed: 0']
        del seance_01.all_sub_reduc['IntensitySignal']
        del seance_01.all_sub_reduc['Seq']
        del seance_01.all_sub_reduc['NumeroEvent']
        del seance_01.all_sub_reduc['Booleen_Peak']
        del seance_01.all_sub_reduc['Scr_amplitude']
        del seance_01.all_sub_reduc['Scr_height']
        self.all_sub_reduc = seance_01.all_sub_reduc.drop_duplicates()

    def save_df_signal(self,i):
        self.df_signal.to_csv(path_access_data + "/Multi_analyses/" + "df_signal_" + str(i) + ".csv")


    def load_df_signal(self):
        self.multi_df_signal = []
        for i in range(1,15):
            self.multi_df_signal.append(pd.read_csv(path_access_data + "/Multi_analyses/" + "df_signal_" + str(i) + ".csv"))
        for i in [1,4,5,8,11,12,13]: #Sujet du groupe de contrôle
            self.multi_df_signal[i-1]["Sub"] = [i] * len(self.multi_df_signal[i-1])
            self.multi_df_signal[i-1]["Groupe"] = [0] * len(self.multi_df_signal[i-1])
        for i in [2,3,6,7,9,10,14]: #Sujet du groupe de contrôle
            self.multi_df_signal[i-1]["Sub"] = [i] * len(self.multi_df_signal[i-1])
            self.multi_df_signal[i-1]["Groupe"] = [1] * len(self.multi_df_signal[i-1])

        self.score_par = np.loadtxt("/Volumes/Samsung_T5/Projet Recherche Maîtrise/Analyse_OCEAN_data/score_participant_1.txt")

        self.all_sub_df = pd.concat(self.multi_df_signal, ignore_index=True)
        self.all_sub_df["IsTh"] = [1 if v == "Yes" else 0 for v in self.all_sub_df["IsThinking"]]
        del self.all_sub_df["IsThinking"]

        self.all_sub_df["O"] = [float(self.score_par[self.all_sub_df["Sub"][i] - 1][0]) for i in range(len(self.all_sub_df))]
        print(3)
        self.all_sub_df["C"] = [float(self.score_par[self.all_sub_df["Sub"][i] - 1][1]) for i in range(len(self.all_sub_df))]
        print(4)
        self.all_sub_df["E"] = [float(self.score_par[self.all_sub_df["Sub"][i] - 1][2]) for i in range(len(self.all_sub_df))]
        print(5)
        self.all_sub_df["A"] = [float(self.score_par[self.all_sub_df["Sub"][i] - 1][3]) for i in range(len(self.all_sub_df))]
        print(6)
        self. all_sub_df["N"] = [float(self.score_par[self.all_sub_df["Sub"][i] - 1][4]) for i in range(len(self.all_sub_df))]

        self.all_sub_df.to_csv("/Volumes/Samsung_T5/Projet Recherche Maîtrise/Analyse_signal_EDA/Multi_analyses/all_sub_df_OCEAN_14sub.csv")




    def creation_file_event(self):
        self.list_startend_stim = [84.77945685386658, 88.12396335601807, 104.77945685386658, 108.88244605064392,
                              124.77945685386658, 130.5121042728424, 273.44892024993896, 288.82819056510925,
                              293.44892024993896, 320.1982033252716, 417.8721024990082, 441.0298933982849,
                              457.8721024990082, 477.8721024990082, 584.5181286334991, 592.7262485027313,
                              604.5181286334991, 624.1150598526001, 624.5181286334991, 644.3886015415192,
                              754.2622048854828, 769.3167021274567, 774.2622048854828, 791.9685461521149,
                              794.2622048854828, 824.2622048854828]
        #Liste booléen de l'évenement "est en réfléxion supposée" sur l'ensemble de l'expérience (prends en compte les phases de questions)
        self.list_TR_01 = []
        for i in range(int((824.2622048854828 - 84.77945685386658) / 2.89)):
            for j in range(len(self.list_startend_stim)-1):
                if self.list_startend_stim[j] <= 84.77945685386658 + 2.89 * i <= self.list_startend_stim[j + 1]:
                    if (j + 1) % 2 == 1:
                        self.list_TR_01.append(1)
                    else:
                        self.list_TR_01.append(0)
        t = np.linspace(84.77945685386658,824.2622048854828,int((824.2622048854828-84.77945685386658)/2.89))

        # Création de l'évenement "moment de réflexion" = "instant entre l'apparition de l'évenement et la pression du bouton"
        list_seq_startend_stim = [[84.77945685386658, 88.12396335601807], [104.77945685386658, 108.88244605064392],
                              [124.77945685386658, 130.5121042728424], [273.44892024993896, 288.82819056510925],
                              [293.44892024993896, 320.1982033252716], [417.8721024990082, 441.0298933982849],
                              [457.8721024990082, 477.8721024990082], [584.5181286334991, 592.7262485027313],
                              [604.5181286334991, 624.1150598526001], [624.5181286334991, 644.3886015415192],
                              [754.2622048854828, 769.3167021274567], [774.2622048854828, 791.9685461521149],
                              [794.2622048854828, 824.2622048854828]]

        # Liste booléen de l'évenement "est en réfléxion supposée" séparé avec les 5 séquences
        self.list_seq_TR_01 = []
        for i in range(5):
            self.list_seq_TR_01.append([])
            for j in range(number_volumes):
                for m in range(len(list_seq_startend_stim)):
                    if list_seq_startend_stim[m][0] <= self.list_seq_time_TR[i][j] <= list_seq_startend_stim[m][1]:
                        self.list_seq_TR_01[i].append(1)
                        break
                    elif m == len(list_seq_startend_stim) - 1 and not (list_seq_startend_stim[m][0] <= self.list_seq_time_TR[i][j] <= list_seq_startend_stim[m][1]):
                        self.list_seq_TR_01[i].append(0)
                        break
                    elif m == len(list_seq_startend_stim) - 1:
                        print("error création list_seq_TR_01 : situation non définie")
        #Création de l'évenement "pression sur le bouton"
        # Liste des booléen de l'évenement "pression sur le bouton"
        self.list_seq_press_01 = []

        # Liste des du signal phasique échantillonné au TR
        self.list_fullphasic_resamp = []
        for i in range(5):
            self.list_fullphasic_resamp.append([])
            for j in range(number_volumes):
                self.list_fullphasic_resamp[i].append(self.phasic_signal_seq[i][self.i_trig[i * 20 + j]-self.i_trig[i * 20]])
        #Liste eda signal resamp mis au format event de fsl
        list_seq_event_eda = []
        for i in range(5):
            list_seq_event_eda.append([])
            for j in range(number_volumes - 1):
                list_seq_event_eda[i].append([])
                list_seq_event_eda[i][j].append(self.list_seq_time_TR[i][j])
                list_seq_event_eda[i][j].append(self.list_seq_time_TR[i][j + 1] - self.list_seq_time_TR[i][j])
                list_seq_event_eda[i][j].append(self.list_fullphasic_resamp[i][j])
            list_seq_event_eda[i].append([])
            list_seq_event_eda[i][number_volumes - 1].append(self.list_seq_time_TR[i][number_volumes - 1])
            list_seq_event_eda[i][number_volumes - 1].append(2.89)
            list_seq_event_eda[i][number_volumes - 1].append(self.list_fullphasic_resamp[i][number_volumes - 1])
        # for i in range(5):
        #     np.savetxt("/Volumes/Samsung_T5/Projet Recherche Maîtrise/Analyse_signal_EDA/ImpAcq_01/seq_" + str(
        #         i) + "_event_signal_eda_resamp.txt", np.array(list_seq_event_eda[i]))

        #Liste évenement du bouton pressé
        list_seq_event_press_d = []
        for i in range(5):
            list_seq_event_press_d.append([])
            for j in range(len(self.list_seq_press_d_time[i])):
                list_seq_event_press_d[i].append([])
                list_seq_event_press_d[i][j].append(str(self.list_seq_press_d_time[i][j]))
                list_seq_event_press_d[i][j].append("0.25")
                list_seq_event_press_d[i][j].append("1")
        # for i in range(5):
        #     np.savetxt("/Volumes/Samsung_T5/Projet Recherche Maîtrise/Analyse_signal_EDA/ImpAcq_01/seq_" + str(
        #         i) + "_event_press_d.txt", np.array(list_seq_event_press_d[i]))


    def analyse_seq(self):
        list_duration = []
        for i in range(int(len(self.list_startend_stim) / 2)):
            list_duration.append(self.list_startend_stim[i * 2 + 1] - self.list_startend_stim[i * 2])
        self.array_duration_stim = np.array(list_duration)
        list_time_display_first = []
        for i in range(int(len(self.list_startend_stim) / 2)):
            list_time_display_first.append(self.list_startend_stim[i * 2])
            #df_event = pd.DataFrame(data={'onset': list_time_display_first, 'duration': np.array(list_duration)})

    def perf_code(self):
        perf = []
        seance_01 = Seance()
        for i in range(14):
            print(i)
            #
            subject_n = "ImpAcq_0"+str(i)
            perf.append([])
            #
            temps = time.time()
            seance_01.load_array()
            perf[-1].append(time.time()-temps)
            temps = time.time()
            seance_01.load_seq()
            perf[-1].append(time.time() - temps)
            temps = time.time()
            seance_01.synchro()
            perf[-1].append(time.time() - temps)
            temps = time.time()
            seance_01.boxplot_seq_sub_n()
            perf[-1].append(time.time() - temps)
            seance_01.save_df_signal(i)

        np.savetxt("/Volumes/Samsung_T5/Projet Recherche Maîtrise/Analyse_signal_EDA/perf.txt",
                   np.array(np.array([perf[i] for i in range(len(perf))])))
        print("end")


seance_01 = Seance()


"""
Attention : lors du premier lancement le dossier doit forcément contenir les fichiers ImpAcq_0*_press_file.csv (séparer par des point virgule) et Impacq_0*_eda_trig.csv (séparé par des virgules) au format csv utf-8

condition sur Impacq_0*_eda_trig.csv :
Fréquence d'enregistrement 10 000Hz
Première ligne "Trigger - Custom, HLT100C - A 5",EDA - EDA100C-MRI" doit être supprimée

condition sur ImpAcq_0*_press_file.csv :

3 colonnes Temps(s) , Event, WordDisplay
Ne doit pas contenir de double pression pour un seul affichage, Première pression prise si double pression

Warning fichier txt Eda_trig [5,10,12,13,14] avec 3 colonnes, voir ligne 58,59 et changer indexe [0] to [1] et [1] to [2]

Command acq - conversion acq to csv : acq2txt ImpAcq2023-06-22T16_25_16_ImpAcq_05.acq -o Impacq_05_eda_trig.csv --channel-indexes=0,1
"""
#Parti chargement /ou création et enregistrement des fichiers

#Module à lancer lors du premier traitement des données :
#seance_01.save_txt2array()
#
#seance_01.identification_seq()
print(1)
#
#seance_01.save_seq()

#Module à lancer lorsque le premier traitement a déjà été fait:
#seance_01.load_array()
#seance_01.load_seq()

#print(2)


#Synchronisation entre le fichier press_files et le fichier eda_trigger
#print(3)
#seance_01.synchro() #Non optionnel puisque création d'attributs utiles aux modules de plot
#print(4)
#Création des fichier file_event pour fit avec FSL et l'analyse des données IRM
#seance_01.creation_file_event()

#Preprocessing et analyse
#seance_01.preproc_eda()
#seance_01.boxplot_seq_sub_n()
#seance_01.save_df_signal(1)
#plot_plot_seq_n :


""" 
'EDA_Raw', 'EDA_Clean', 'EDA_Tonic', 'EDA_Phasic', 'SCR_Onsets',
       'SCR_Peaks', 'SCR_Height', 'SCR_Amplitude', 'SCR_RiseTime',
       'SCR_Recovery', 'SCR_RecoveryTime'
"""
# Charger la multi analyse
#seance_01.load_df_signal()
#seance_01.Open_all_sub_OCEAN()

#pd.read_csv("/Volumes/Samsung_T5/Projet Recherche Maîtrise/Analyse_signal_EDA/Multi_analyses/all_sub_df_OC.csv",sep=",",header=0)
#all_sub_df.to_csv("/Volumes/Samsung_T5/Projet Recherche Maîtrise/Analyse_signal_EDA/Multi_analyses/all_sub_df_OCEAN_10_02.csv")

#all_sub_drop_dup = all_sub_df.drop_duplicates()

print(7)
