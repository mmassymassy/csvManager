import csv
class CsvManager():
    def __init__(self,nomFichier) -> None:
        self.nomFichier = nomFichier
        self.data = []
        self.header = []
    def lireCsv(self):
        with open(self.nomFichier, 'r') as f:
            reader = csv.reader(f, delimiter=',', lineterminator='\n')
            self.header = next(reader)
            for row in reader:
                print(row)
                row = [int(x) for x in row[:3]] + [x for x in row[3:]]
                row = dict(zip(self.header, row))
                self.data.append(row)
        f.close()
    def getLigne(self,numero : int):
        for ligne in self.data:
            if ligne['numero'] == numero:
                return ligne
        return "Machine inexistante"
    def filtrerParLigne(self,ligne : int):
        return [x for x in self.data if x['ligne'] == ligne]
    def filtrerParSecteur(self,secteur : int):
        return [x for x in self.data if x['secteur'] == secteur]
    def filtrerParLigneSecteur(self,ligne : int, secteur : int):
        return [x for x in self.data if x['ligne'] == ligne and x['secteur'] == secteur]
    def filtrerParNumero(self,numero : int):
        return [x for x in self.data if x['numero'] == numero]
    def ligneExiste(self,numero : int):
        for ligne in self.data:
            if ligne['numero'] == numero:
                return True
        return False
    def validerLigne(self,ligne : dict):
        return type(ligne['numero'])== int and type(ligne['ligne']) == int and type(ligne['secteur']) == int and ligne['photo'] != '' and ligne['lien'] != ''
    def ajouterLigne(self,ligne : dict):
        if(not self.validerLigne(ligne)):
            return "Champs manquants ou invalides"
        if(self.ligneExiste(ligne['numero'])):
            return "Ligne déjà existante"
        self.data.append(ligne)
        with open('data.csv', 'a') as f:
            writer = csv.DictWriter(f, fieldnames=self.header, delimiter=',', lineterminator='\n')
            writer.writerow(ligne)
        f.close()
        return "Ajouté avec succés"
    def supprimerLigne(self,numero : int):
        if(not self.ligneExiste(numero)):
            return "Ligne inexistante"
        self.data = [x for x in self.data if x['numero'] != numero]
        with open(self.nomFichier, 'a') as f:
            self.reinitCsv()
            writer = csv.DictWriter(f, fieldnames=self.header, delimiter=',', lineterminator='\n')
            writer.writerows(self.data)
        f.close()
        return "Supprimé avec succés"
    def modifierColonne(self,numero : int, colonne : str, valeur : str or int):
        if(not self.ligneExiste(numero)):
            return "Machine inexistante"
        if(colonne not in self.header):
            return "Colonne inexistante"
        for ligne in self.data:
            if ligne['numero'] == numero:
                ligne[colonne] = valeur
        with open(self.nomFichier, 'a') as f:
            self.reinitCsv()
            writer = csv.DictWriter(f, fieldnames=self.header, delimiter=',', lineterminator='\n')
            writer.writerows(self.data)
        f.close()
    def modifierColonnes(self,numero : int, colonnes : list, valeurs : list):
        if(not self.ligneExiste(numero)):
            return "Machine inexistante"
        if(len(colonnes) != len(valeurs)):
            return "Nombre de colonnes et de valeurs différentes"
        if(not all([x in self.header for x in colonnes])):
            return "Colonne inexistante"
        for ligne in self.data:
            if ligne['numero'] == numero:
                for i in range(len(colonnes)):
                    ligne[colonnes[i]] = valeurs[i]
        with open(self.nomFichier, 'a') as f:
            self.reinitCsv()
            writer = csv.DictWriter(f, fieldnames=self.header, delimiter=',', lineterminator='\n')
            writer.writerows(self.data)
        f.close()
        return "Modifié avec succés"
    def refresh(self):
        self.data = []
        self.lireCsv()
    def reinitCsv(self):
        with open(self.nomFichier+".bak", 'w') as f:
            for ligne in self.data:
                writer = csv.DictWriter(f, fieldnames=self.header, delimiter=',', lineterminator='\n')
                writer.writerow(ligne)
        f.close()
        with open(self.nomFichier, 'w') as f:
            writer = csv.writer(f, delimiter=',', lineterminator='\n')
            writer.writerow(['numero', 'ligne', 'secteur', 'photo', 'lien'])
        f.close()
        self.refresh()

