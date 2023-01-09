#!/usr/bin/python3


import psycopg2
from tkinter import *
from tkinter import ttk


def window():
    # Create an instance of tkinter frame
    win = Tk()
    win.title("Bibliothèque NF18")
    # Set the geometry of frame
    width = win.winfo_screenwidth()
    height = win.winfo_screenwidth()
    win.geometry(f"{width}x{height}")
    s = ttk.Style()
    s.theme_use('clam')

    # Add the rowheight
    s.configure('Treeview', rowheight=45)
    return win


def landingFrame(win, conn, prev_frame=None):
    if (prev_frame != None): clear_frame(prev_frame)
    frame = Frame(win)
    frame.grid(row=0, column=0)
    Label(frame, text="Bibliothèque | NF18", font=("Arial", 20)).grid(row=0, column=2, pady=20, padx=300)
    boutonAdherent = Button(frame, text="Accès Espace Adhérents",
                            command=lambda: login_frame(win, conn, 'Adhérents', False, frame), padx=20)
    boutonAdherent.grid(row=1, column=2, pady=50)
    boutonAdmin = Button(frame, text="Accès Espace Personnel de Bibliothèque",
                         command=lambda: login_frame(win, conn, 'Personnel', False, frame), padx=20)
    boutonAdmin.grid(row=2, column=2)
    win.mainloop()


def login_frame(win, conn, status, retry=False, prev_frame=None):
    if (prev_frame != None): clear_frame(prev_frame)
    frame = Frame(win)
    frame.grid(row=0, column=0)
    Label(frame, text=f"Connexion à l'espace {status}", font=("Arial", 20), padx=10, pady=10).grid(row=0, column=0,
                                                                                                   columnspan=3,
                                                                                                   padx=200)
    Label(frame, text="Login : ", font=("Arial", 10), padx=10, pady=10).grid(row=1, column=0)
    Label(frame, text="Mot de passe : ", font=("Arial", 10), pady=15).grid(row=2, column=0)

    entryLogin = Entry(frame)
    entryLogin.grid(row=1, column=1)
    entryLogin.focus_set()
    entryPassword = Entry(frame, show="*")
    entryPassword.grid(row=2, column=1)

    Button(frame, text="Retour", bg='red', command=lambda: landingFrame(win, conn, frame), padx=20).grid(row=3,
                                                                                                         column=0)
    Button(frame, text="Connexion", bg='green',
           command=lambda: user_connection(win, conn, status, entryLogin.get(), entryPassword.get(), frame),
           padx=20).grid(row=3, column=2)

    if retry: Label(frame, text=f"Login et/ou mot de passe {status} incorrect(s)", font=("Arial", 10), padx=10, pady=10,
                    fg='red').grid(row=4, column=0, columnspan=3)


def clear_frame(frame):
    for widgets in frame.winfo_children():
        widgets.destroy()


def db_connection():
    """Connection function to database"""
    HOST = "tuxa.sme.utc"

    USER = "nf18a008"

    PASSWORD = "vjOTb3UU"

    DATABASE = "dbnf18a008"

    # Connect to an existing database

    conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (HOST, DATABASE, USER, PASSWORD))
    print(conn)
    return conn


def user_connection(win, conn, status, username, password, prev_frame=None):
    """Connection function for allowing access to DB"""
    if (prev_frame != None): clear_frame(prev_frame)
    cursor = conn.cursor()
    query = f"SELECT Compte.id FROM Compte INNER JOIN {'adherent' if status == 'Adhérents' else 'personnel'} on Compte.id = {'adherent' if status == 'Adhérents' else 'personnel'}.id WHERE login = '{username}' AND password = '{password}';"  # vérification que la personne se connecte bien en tant qu'adhérent/personnel
    print(query)
    try:
        cursor.execute(query)
        raw = cursor.fetchone()
        query = f"SELECT * FROM Utilisateur WHERE id = {raw[0]};"  # récupération des infors perso
        cursor.execute(query)
        profil = cursor.fetchone()
        if status == "Adhérents":
            espaceAdherents(win, conn, profil)
        else:
            espacePersonnels(win, conn, profil)
    except:
        login_frame(win, conn, status, True)


def espaceAdherents(win, conn, profil, prev_frame=None):
    if (prev_frame != None): clear_frame(prev_frame)
    frame = Frame(win)
    frame.grid(row=0, sticky="ew")

    Label(frame, text=f"Bienvenue sur l'espace Adhérents ", font=("Arial", 20), padx=10, pady=10).grid(row=0, column=0,
                                                                                                       columnspan=3)
    Label(frame, text=f"Mes informations : ", font=("Arial", 15), padx=10, pady=10).grid(row=1, column=0, columnspan=3)
    Label(frame, text=f"Nom : ", font=("Arial", 10, 'bold'), padx=10, pady=10).grid(row=2, column=0, sticky='w')
    Label(frame, text=f"{profil[1]}", font=("Arial ", 10), padx=10, pady=10).grid(row=2, column=1, columnspan=2,
                                                                                  sticky='w')
    Label(frame, text=f"Prénom : ", font=("Arial", 10, 'bold'), padx=10, pady=10).grid(row=3, column=0, sticky='w')
    Label(frame, text=f"{profil[2]}", font=("Arial ", 10), padx=10, pady=10).grid(row=3, column=1, columnspan=2,
                                                                                  sticky='w')
    Label(frame, text=f"Ville : ", font=("Arial", 10, 'bold'), padx=10, pady=10).grid(row=4, column=0, sticky='w')
    Label(frame, text=f"{profil[6]}", font=("Arial ", 10), padx=10, pady=10).grid(row=4, column=1, columnspan=2,
                                                                                  sticky='w')
    Label(frame, text=f"Adresse mail : ", font=("Arial", 10, 'bold'), padx=10, pady=10).grid(row=5, column=0,
                                                                                             sticky='w')
    Label(frame, text=f"{profil[7]}", font=("Arial ", 10), padx=10, pady=10).grid(row=5, column=1, columnspan=2,
                                                                                  sticky='w')
    cursor = conn.cursor()
    query = f"SELECT statut_adhesion FROM Adherent WHERE id = {profil[0]};"
    cursor.execute(query)
    adhesion = cursor.fetchone()
    Label(frame, text=f"Adhésion : ", font=("Arial", 10, 'bold'), padx=10, pady=10).grid(row=6, column=0, sticky='w')
    Label(frame, text=f"{adhesion[0]}", font=("Arial ", 10), padx=10, pady=10).grid(row=6, column=1, columnspan=2,
                                                                                    sticky='w')
    Label(frame, text=f"Mes sanctions : ", font=("Arial", 10, 'bold'), padx=10, pady=10).grid(row=7, column=0,
                                                                                              sticky='w')
    Button(frame, text="Voir", command=lambda: accesSanctions(win, conn, frame, profil), padx=20).grid(row=7, column=1,
                                                                                                       columnspan=2,
                                                                                                       sticky='w')

    Label(frame, text=f"Parcourir : ", font=("Arial", 15), padx=10, pady=10).grid(row=1, column=3, columnspan=2)
    Button(frame, text="Films", command=lambda: espaceFilms(win, conn, frame, profil), padx=20, bg='blue').grid(row=2,
                                                                                                                column=4,
                                                                                                                columnspan=3,
                                                                                                                sticky='nesw')
    Button(frame, text="Musiques", command=lambda: espaceMusiques(win, conn, frame, profil), padx=20, bg='yellow').grid(
        row=3, column=4, columnspan=3, sticky='nesw')
    Button(frame, text="Livres", command=lambda: espaceLivres(win, conn, frame, profil), padx=20, bg='purple').grid(
        row=4,
        column=4,
        columnspan=3, sticky='nesw')
    Button(frame, text="Contributeurs", command=lambda: espaceContributeurs(win, conn, frame, profil), padx=20,
           bg='green').grid(row=5, column=4, columnspan=3, sticky='nesw')

    # Button(frame, text="Recherche par titre", command=lambda: espaceContributeurs(win, conn, frame, profil), padx=20,
    #      bg='cyan').grid(row=6, column=4, columnspan=3, sticky='nesw')

    Button(frame, text="Déconnexion", command=lambda: landingFrame(win, conn, frame), padx=20,
           bg='red').grid(row=8, column=0, sticky='w', padx=10)


def espacePersonnels(win, conn, profil, prev_frame=None):
    if (prev_frame != None): clear_frame(prev_frame)
    frame = Frame(win)
    frame.grid(row=0, sticky="ew")
    Label(frame, text=f"Bienvenue sur l'espace Personnel : ", font=("Arial", 20), padx=10, pady=10).grid(row=0,
                                                                                                         column=0,
                                                                                                         pady=10)
    boutonAddRessource = Button(frame, text="Ajouter une Ressource",
                                command=lambda: addRessource_frame(win, conn, profil, False, frame), padx=20)
    boutonAddRessource.grid(row=1, column=0, sticky='nswe', padx=10)
    boutonAddAdherent = Button(frame, text="Ajouter un Adherent",
                               command=lambda: addAdherent_frame(win, conn, profil, False, frame), padx=20)
    boutonAddAdherent.grid(row=2, column=0, sticky='nswe', padx=10)
    boutonAddSanction = Button(frame, text="Ajouter une Sanction",
                               command=lambda: addSanction_frame(win, conn, profil, False, frame), padx=20)
    boutonAddSanction.grid(row=3, column=0, sticky='nswe', padx=10)

    boutonUpdateSanction = Button(frame, text="Modifier une Sanction",
                                  command=lambda: updateSanction_frame(win, conn, profil, False, frame), padx=20)
    boutonUpdateSanction.grid(row=4, column=0, sticky='nswe', padx=10)

    boutonAddExemplaire = Button(frame, text="Ajouter un exemplaire",
                                 command=lambda: addExemplaire_frame(win, conn, profil, False, frame), padx=20)
    boutonAddExemplaire.grid(row=5, column=0, sticky='nswe', padx=10)

    boutonAddPret = Button(frame, text="Enregistrer un prêt",
                           command=lambda: addPret_frame(win, conn, profil, False, frame), padx=20)
    boutonAddPret.grid(row=6, column=0, sticky='nswe', padx=10)

    # boutonAddRealisateur = Button(frame, text="Ajouter un Contributeur",command=lambda: addSanction_frame(win, conn, profil, False, frame), padx=20)
    # boutonAddRealisateur.grid(row=7, column=0)

    # ICI ON AFFICHE QUELQUES REQUÊTES STATISTIQUES

    cursor = conn.cursor()
    # Durée moyenne d'un prêt
    Label(frame, text=f"Durée moyenne d'un prêt : ", font=("Arial", 10, 'bold'), padx=10, pady=10).grid(row=1, column=2)
    query = "SELECT AVG(date_fin - date_debut) AS duree_moyenne FROM Pret;"
    cursor.execute(query)
    Label(frame, text=f"{(cursor.fetchone())[0]:0.2f} jours", font=("Arial", 10), padx=10, pady=10).grid(row=1,
                                                                                                         column=3)

    # Nombre de prêt en cours
    Label(frame, text=f"Nombre de prêt en cours : ", font=("Arial", 10, 'bold'), padx=10, pady=10).grid(row=2,
                                                                                                        column=2, )
    query = "SELECT COUNT(*) FROM Pret WHERE NOT rendu;"
    cursor.execute(query)
    Label(frame, text=f"{(cursor.fetchone())[0]}", font=("Arial", 10), padx=10, pady=10).grid(row=2, column=3)

    # Adhérent le plus sanctionné
    Label(frame, text=f"Adhérent le plus sanctionné : ", font=("Arial", 10, 'bold'), padx=10, pady=10).grid(row=3,
                                                                                                            column=2)
    query = "SELECT idadherent, prenom, nom, statut_adhesion, COUNT(idadherent) AS nombre_sanctions FROM Sanction S INNER JOIN Adherent A ON S.idadherent = A.id NATURAL JOIN Utilisateur GROUP BY idadherent, statut_adhesion, prenom, nom ORDER BY nombre_sanctions DESC LIMIT 1;"
    cursor.execute(query)
    adherent = cursor.fetchone()
    Label(frame,
          text=f"(ID Adhérent : {adherent[0]}, adhésion : {adherent[3]}) Nom : {adherent[2]} | Prénom : {adherent[1]} ",
          font=("Arial", 10), padx=10, pady=10).grid(row=3, column=3)

    # Ressources la plus empruntée
    Label(frame, text=f"Ressource la plus empruntée : ", font=("Arial", 10, 'bold'), padx=10, pady=10).grid(row=4,
                                                                                                            column=2)
    query = "SELECT titre, code_classification, COUNT(code_ressource) AS nb_emprunts FROM Ressource R INNER JOIN Pret P on R.code = P.code_ressource GROUP BY code_ressource, titre, code_classification ORDER BY nb_emprunts DESC LIMIT 1;"
    cursor.execute(query)
    res = cursor.fetchone()
    print(res)
    Label(frame, text=f"Titre : {res[0]} | Classification : {res[1]} | Emprunts : {res[2]}", font=("Arial", 10),
          padx=10, pady=10).grid(row=4, column=3)

    # Classement des motis de sanctions les plus émis
    Label(frame, text=f"Classement des motifs de sanctions les plus émis ", font=("Arial", 10, 'bold'), padx=10,
          pady=10).grid(row=20, column=0)

    query = "SELECT motif, COUNT(motif) AS nombre FROM Sanction GROUP BY motif ORDER BY nombre DESC;"
    cursor.execute(query)
    motifs = cursor.fetchall()

    tree = ttk.Treeview(frame, columns=("c1", "c2"), show='headings', height=len(motifs))
    tree.column("# 1", anchor=CENTER)
    tree.heading("# 1", text="Motif")
    tree.column("# 2", anchor=CENTER)
    tree.heading("# 2", text="Utilisations")

    for i in range(len(motifs)):
        tree.insert('', 'end', text="1", values=(motifs[i][0], motifs[i][1]))
    tree.grid(row=21, columnspan=2)

    # Prêts en retard
    Label(frame, text=f"Prêts en retard : ", font=("Arial", 10, 'bold'), padx=10, pady=10).grid(row=20, column=2)
    query = "SELECT id_pret, adherent, code_ressource, exemplaire, NOW() - date_fin AS retard FROM Pret WHERE date_fin < NOW() AND NOT rendu;"
    cursor.execute(query)
    prets = cursor.fetchall()

    tree = ttk.Treeview(frame, columns=("c1", "c2", "c3", "c4", "c5"), show='headings', height=len(prets))
    tree.column("# 1", anchor=CENTER)
    tree.heading("# 1", text="ID Prêt")
    tree.column("# 2", anchor=CENTER)
    tree.heading("# 2", text="ID Adhérent")
    tree.column("# 3", anchor=CENTER)
    tree.heading("# 3", text="Code Ressource")
    tree.column("# 4", anchor=CENTER)
    tree.heading("# 4", text="ID Exemplaire")
    tree.column("# 5", anchor=CENTER)
    tree.heading("# 5", text="Retard")
    for i in range(len(prets)):
        tree.insert('', 'end', text="1", values=(prets[i][0], prets[i][1], prets[i][2], prets[i][3], prets[i][4]))
    tree.grid(row=21, column=2, columnspan=5, padx=10)

    Button(frame, text="Déconnexion", command=lambda: landingFrame(win, conn, frame), padx=20,
           bg='red').grid(row=30, column=0, sticky='w', padx=10, pady=10)


def addPret_frame(win, conn, profil, retry=False, prev_frame=None, valid=False):

    query = "SELECT * FROM Pret ;"

    cursor = conn.cursor()
    cursor.execute(query)
    ff = cursor.fetchall()
    for f in ff :
        print(f)

    if (prev_frame != None): clear_frame(prev_frame)
    frame = Frame(win)
    frame.grid(row=0, sticky="ew")
    Label(frame, text=f"Enregistrer un prêt", font=("Arial", 20), padx=10, pady=10).grid(row=0, column=0, columnspan=2)
    Label(frame, text=f"ID Adherent", font=("Arial", 10), padx=10, pady=10).grid(row=1, column=0, sticky='nswe')
    Label(frame, text=f"ID Exemplaire", font=("Arial", 10), padx=10, pady=10).grid(row=2, column=0, sticky='nswe')
    Label(frame, text=f"Code Ressource", font=("Arial", 10), padx=10, pady=10).grid(row=3, column=0, sticky='nswe')
    Label(frame, text=f"Date début (YYYY-MM-DD)", font=("Arial", 10), padx=10, pady=10).grid(row=4, column=0, sticky='nswe')
    Label(frame, text=f"Date Fin (YYYY-MM-DD)", font=("Arial", 10), padx=10, pady=10).grid(row=5, column=0, sticky='nswe')

    idAdherent = Entry(frame, font=("Arial", 10))
    idAdherent.grid(row=1, column=1)
    idExemplaire = Entry(frame, font=("Arial", 10))
    idExemplaire.grid(row=2, column=1)
    codeRessource = Entry(frame, font=("Arial", 10))
    codeRessource.grid(row=3, column=1)
    dateDebut = Entry(frame, font=("Arial", 10))
    dateDebut.grid(row=4, column=1)

    dateFin = Entry(frame, font=("Arial", 10))
    dateFin.grid(row=5, column=1)

    query = "SELECT id, nom, prenom,mail,date_naissance,num_tel FROM Adherent NATURAL JOIN Utilisateur WHERE statut_adhesion = 'active';"

    cursor = conn.cursor()
    cursor.execute(query)
    adherents = cursor.fetchall()

    tree = ttk.Treeview(frame, columns=("c1", "c2", "c3", "c4", "c5", "c6"),
                        show='headings',
                        height=len(adherents))

    tree.column("# 1", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 1", text="ID Adhérent")
    tree.column("# 2", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 2", text="Nom")
    tree.column("# 3", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 3", text="Prénom")
    tree.column("# 4", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 4", text="Mail")
    tree.column("# 5", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 5", text="Naissance")
    tree.column("# 6", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 6", text="Tél")

    for i in range(len(adherents)):
        tree.insert('', 'end', text="1", values=(
            adherents[i][0], adherents[i][1], adherents[i][2], adherents[i][3], adherents[i][4], adherents[i][5]))

    Label(frame, text=f"Liste adhérents autorisés pour emprunt", font=("Arial", 15, 'bold'), padx=10, pady=10).grid(
        row=0, column=3, sticky='nswe')
    tree.grid(row=1, column=3, columnspan=6, rowspan=len(adherents), padx=10)

    query = "SELECT E.id,code,titre,code_classification FROM Exemplaire E LEFT JOIN (SELECT exemplaire,code_ressource FROM Pret P WHERE rendu ='false') AS D ON D.exemplaire = E.id AND D.code_ressource = E.code_ressource INNER JOIN Ressource R on E.code_ressource = R.code WHERE etat <> 'perdu' AND D.exemplaire IS NULL AND D.code_ressource IS NULL;"
    cursor = conn.cursor()
    cursor.execute(query)
    exemplaire = cursor.fetchall()

    tree = ttk.Treeview(frame, columns=("c1", "c2", "c3", "c4"),
                        show='headings',
                        height=len(exemplaire))

    tree.column("# 1", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 1", text="ID Exemplaire")
    tree.column("# 2", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 2", text="Code ressource")
    tree.column("# 3", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 3", text="Titre")
    tree.column("# 4", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 4", text="Classification")

    for i in range(len(exemplaire)):
        tree.insert('', 'end', text="1", values=(
            exemplaire[i][0], exemplaire[i][1], exemplaire[i][2], exemplaire[i][3]))

    Label(frame, text=f"Liste exemplaires disponibles", font=("Arial", 15, 'bold'), padx=10, pady=10).grid(
        row=1 + len(adherents), column=3, sticky='nswe')
    tree.grid(row=2 + len(adherents), column=3, columnspan=4, rowspan=len(exemplaire), padx=10)

    if (valid):
        Label(frame, text=f"Prêt enregistré !", fg='green', font=("Arial", 10), padx=10, pady=10).grid(row=12, column=0)
    elif (retry):
        Label(frame, text=f"Impossible d'enregistrer le prêt, vérifiez les données saisies et le statut de l'adhérent",
              fg='red', font=("Arial", 10), padx=10, pady=10).grid(row=12,
                                                                   column=0)
    Button(frame, text="Valider", bg="green", command=lambda: addPret(win, conn, profil, frame, (
    idAdherent.get(), idExemplaire.get(), codeRessource.get(), dateDebut.get(), dateFin.get())), padx=20).grid(row=13,
                                                                                                               column=2)

    Button(frame, text="Retour", command=lambda: espacePersonnels(win, conn, profil, prev_frame=frame), padx=20).grid(
        row=13, column=0)


def addPret(win, conn, profil, frame, values):
    print(values)
    cursor = conn.cursor()
    error = False
    valid = False
    try:
        # Si statut adhesion = active et exemplaire disponible (select exemplaire exemplaire id where rendu = false est vide) et etat non perdu
        query = f"SELECT statut_adhesion FROM Adherent WHERE id={int(values[0])};"
        #query = 'SELECT * FROM Pret;'
        print(query)
        cursor.execute(query)
        #print(cursor.fetchall())
        statut = True if (cursor.fetchone())[0] == 'active' else False

        query = f"SELECT etat FROM Exemplaire E WHERE E.id = {int(values[1])} AND E.code_ressource =  {int(values[2])};"
        print(query)
        cursor.execute(query)
        etat = True if (cursor.fetchone())[0] != 'perdu' else False

        query = f"SELECT COUNT(*) FROM Pret P WHERE P.exemplaire = {int(values[1])} AND P.code_ressource =  {int(values[2])} AND rendu = False;"
        print(query)
        cursor.execute(query)
        dispo = True if (cursor.fetchone())[0] == 0 else False

        if (dispo and etat and statut):
            query = f"INSERT INTO Pret(adherent,exemplaire,code_ressource,date_debut,date_fin,rendu) VALUES ({int(values[0])}, {int(values[1])},{int(values[2])},DATE('{values[3]}'),DATE('{values[4]}'),False);"
            print(query)
            cursor.execute(query)
            conn.commit()
            valid = True

    except Exception as er:
       print(er)
       error = True
       conn.rollback()

    addPret_frame(win, conn, profil, error, frame, valid)


def addExemplaire_frame(win, conn, profil, retry=False, prev_frame=None, valid=False):
    if (prev_frame != None): clear_frame(prev_frame)
    frame = Frame(win)
    frame.grid(row=0, sticky="ew")
    Label(frame, text=f"Ajouter un exemplaire", font=("Arial", 20), padx=10, pady=10).grid(row=0, column=0,
                                                                                           columnspan=2)
    Label(frame, text=f"Code ressource", font=("Arial", 10), padx=10, pady=10).grid(row=1, column=0, sticky='nswe')
    Label(frame, text=f"Etat ('neuf','bon','abîmé','perdu')", font=("Arial", 10), padx=10, pady=10).grid(row=2,
                                                                                                         column=0,
                                                                                                         sticky='nswe')

    code = Entry(frame, font=("Arial", 10))
    code.grid(row=1, column=1)
    etat = Entry(frame, font=("Arial", 10))
    etat.grid(row=2, column=1)

    query = "SELECT Ressource.code,titre,date_apparition,code_classification,editeur,genre FROM RESSOURCE;"
    cursor = conn.cursor()
    cursor.execute(query)
    res = cursor.fetchall()

    tree = ttk.Treeview(frame, columns=("c1", "c2", "c3", "c4", "c5", "c6"), show='headings',
                        height=len(res))

    tree.column("# 1", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 1", text="Code")
    tree.column("# 2", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 2", text="Titre")
    tree.column("# 3", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 3", text="Apparition")
    tree.column("# 4", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 4", text="Classification")
    tree.column("# 5", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 5", text="Editeur")
    tree.column("# 6", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 6", text="Genre")

    for i in range(len(res)):
        tree.insert('', 'end', text="1", values=(
            res[i][0], res[i][1], res[i][2], res[i][3], res[i][4], res[i][5]))
    Label(frame, text=f"Liste des ressources", font=("Arial", 15, 'bold'), padx=10, pady=10).grid(row=0, column=3,
                                                                                                  columnspan=2)
    tree.grid(row=1, column=3, columnspan=6, rowspan=len(res), padx=10)

    if (valid):
        Label(frame, text=f"Exemplaire ajouté !", fg='green', font=("Arial", 10), padx=10, pady=10).grid(row=12,
                                                                                                         column=0)
    elif (retry):
        Label(frame, text=f"Impossible d'ajouter l'exemplaire'", fg='red', font=("Arial", 10), padx=10, pady=10).grid(
            row=12,
            column=0)
    Button(frame, text="Valider", bg="green",
           command=lambda: addExemplaire(win, conn, profil, frame, (code.get(), etat.get())), padx=20).grid(row=13,
                                                                                                            column=2)
    Button(frame, text="Retour", command=lambda: espacePersonnels(win, conn, profil, prev_frame=frame), padx=20).grid(
        row=13, column=0)


def addExemplaire(win, conn, profil, frame, values):
    print(values)
    cursor = conn.cursor()
    error = False
    valid = False
    try:
        query = f"INSERT INTO Exemplaire(code_ressource,etat) VALUES ({int(values[0])},'{values[1]}');"
        print(query)
        cursor.execute(query)
        conn.commit()
        valid = True
    except Exception as er:
        error = True
        conn.rollback()
    addExemplaire_frame(win, conn, profil, error, frame, valid)


def updateSanction_frame(win, conn, profil, retry=False, prev_frame=None, valid=False):
    if (prev_frame != None): clear_frame(prev_frame)
    frame = Frame(win)
    frame.grid(row=0, sticky="ew")
    Label(frame, text=f"Modifier une sanction", font=("Arial", 20), padx=10, pady=10).grid(row=0, column=0,
                                                                                           columnspan=2)
    Label(frame, text=f"Numéro de sanction : ", font=("Arial", 10), padx=10, pady=10).grid(row=1, column=0, sticky='nswe')
    Label(frame, text=f"Date de Fin (YYYY-MM-DD) :", font=("Arial", 10), padx=10, pady=10).grid(row=2, column=0, sticky='nswe')

    num = Entry(frame, font=("Arial", 10))
    num.grid(row=1, column=1)
    date = Entry(frame, font=("Arial", 10))
    date.grid(row=2, column=1)

    query = "SELECT idadherent, nom,prenom,statut_adhesion, motif, date_debut AS nombre_sanctions FROM Sanction S INNER JOIN Adherent A ON S.idadherent = A.id NATURAL JOIN Utilisateur WHERE date_fin IS NULL;"

    cursor = conn.cursor()
    cursor.execute(query)
    adherents = cursor.fetchall()

    tree = ttk.Treeview(frame, columns=("c1", "c2", "c3", "c4", "c5", "c6"),
                        show='headings',
                        height=len(adherents))

    tree.column("# 1", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 1", text="ID Adhérent")
    tree.column("# 2", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 2", text="Nom")
    tree.column("# 3", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 3", text="Prénom")
    tree.column("# 4", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 4", text="Adhésion")
    tree.column("# 5", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 5", text="Motif")
    tree.column("# 6", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 6", text="Date_debut")

    for i in range(len(adherents)):
        tree.insert('', 'end', text="1", values=(
            adherents[i][0], adherents[i][1], adherents[i][2], adherents[i][3], adherents[i][4], adherents[i][5]))

    Label(frame, text=f"Liste des sanctions en cours", font=("Arial", 15, 'bold'), padx=10, pady=10).grid(row=0,
                                                                                                          column=3,
                                                                                                          columnspan=2)
    tree.grid(row=1, column=3, columnspan=7, rowspan=len(adherents), padx=10)

    if (valid):
        Label(frame, text=f"Sanction modifiée !", fg='green', font=("Arial", 10), padx=10, pady=10).grid(row=12,
                                                                                                         column=0)
    elif (retry):
        Label(frame, text=f"Impossible de modifier la sanction", fg='red', font=("Arial", 10), padx=10, pady=10).grid(
            row=12,
            column=0)
    Button(frame, text="Valider", bg="green",
           command=lambda: updateSanction(win, conn, profil, frame, (num.get(), date.get())),
           padx=20).grid(row=13, column=2)
    Button(frame, text="Retour", command=lambda: espacePersonnels(win, conn, profil, prev_frame=frame), padx=20).grid(
        row=13, column=0)


def updateSanction(win, conn, profil, frame, values):
    print(values)
    cursor = conn.cursor()
    error = False
    valid = False
    try:
        query = f"UPDATE Sanction SET date_fin = DATE('{values[1]}') WHERE idSanction={int(values[0])}; "
        print(query)
        cursor.execute(query)
        conn.commit()
        valid = True
    except Exception as er:
        error = True
        conn.rollback()
    updateSanction_frame(win, conn, profil, error, frame, valid)


def addRessource_frame(win, conn, profil, retry=False, prev_frame=None):
    if (prev_frame != None): clear_frame(prev_frame)
    frame = Frame(win)
    frame.grid(row=0, sticky="ew")
    Label(frame, text=f"Ajouter une ressource", font=("Arial", 20), padx=10, pady=10).grid(row=0, column=0,
                                                                                           columnspan=2)
    boutonAddFilm = Button(frame, text="Film", command=lambda: addFilm_frame(win, conn, profil, False, frame), padx=20)
    boutonAddFilm.grid(row=1, column=0, sticky='nswe', padx=10, pady=10)
    boutonAddMusique = Button(frame, text="Musique", command=lambda: addMusique_frame(win, conn, profil, False, frame),
                              padx=20)
    boutonAddMusique.grid(row=2, column=0, sticky='nswe', padx=10, pady=10)
    boutonAddLivre = Button(frame, text="Livre", command=lambda: addLivre_frame(win, conn, profil, False, frame),
                            padx=20)
    boutonAddLivre.grid(row=3, column=0, sticky='nswe', padx=10, pady=10)

    query = "SELECT Ressource.code,titre,date_apparition,code_classification,editeur,genre FROM RESSOURCE;"
    cursor = conn.cursor()
    cursor.execute(query)
    res = cursor.fetchall()

    tree = ttk.Treeview(frame, columns=("c1", "c2", "c3", "c4", "c5", "c6"), show='headings',
                        height=len(res))

    tree.column("# 1", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 1", text="Code")
    tree.column("# 2", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 2", text="Titre")
    tree.column("# 3", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 3", text="Apparition")
    tree.column("# 4", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 4", text="Classification")
    tree.column("# 5", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 5", text="Editeur")
    tree.column("# 6", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 6", text="Genre")

    for i in range(len(res)):
        tree.insert('', 'end', text="1", values=(
            res[i][0], res[i][1], res[i][2], res[i][3], res[i][4], res[i][5]))

    Label(frame, text=f"Liste des ressources déjà enregistrées", font=("Arial", 15, 'bold'), padx=10, pady=10).grid(
        row=0, column=3,
        columnspan=2)
    tree.grid(row=1, column=3, columnspan=6, rowspan=len(res), padx=10)

    Button(frame, text="Retour", command=lambda: espacePersonnels(win, conn, profil, prev_frame=frame)).grid(
        row=4, column=0, pady=10)


def addAdherent_frame(win, conn, profil, retry=False, prev_frame=None, valid=False):
    if (prev_frame != None): clear_frame(prev_frame)
    frame = Frame(win)
    frame.grid(row=0, sticky="ew")
    Label(frame, text=f"Ajouter un Adhérent", font=("Arial", 20), padx=10, pady=10).grid(row=0, column=0, columnspan=2)
    Label(frame, text=f"Nom", font=("Arial", 10), padx=10, pady=10).grid(row=1, column=0, sticky='nswe', )
    Label(frame, text=f"Prénom", font=("Arial", 10), padx=10, pady=10).grid(row=2, column=0, sticky='nswe', )
    Label(frame, text=f"Numéro d'adresse", font=("Arial", 10), padx=10, pady=10).grid(row=3, column=0, sticky='nswe', )
    Label(frame, text=f"Rue", font=("Arial", 10), padx=10, pady=10).grid(row=4, column=0, sticky='nswe', )
    Label(frame, text=f"Code postal", font=("Arial", 10), padx=10, pady=10).grid(row=5, column=0, sticky='nswe', )
    Label(frame, text=f"Ville", font=("Arial", 10), padx=10, pady=10).grid(row=6, column=0, sticky='nswe', )
    Label(frame, text=f"Adresse mail", font=("Arial", 10), padx=10, pady=10).grid(row=7, column=0, sticky='nswe', )
    Label(frame, text=f"Date de naissance (YYYY-MM-DD) ", font=("Arial", 10), padx=10, pady=10).grid(row=8, column=0, sticky='nswe', )
    Label(frame, text=f"Tél", font=("Arial", 10), padx=10, pady=10).grid(row=9, column=0, sticky='nswe', )
    Label(frame, text=f"Login", font=("Arial", 10), padx=10, pady=10).grid(row=10, column=0, sticky='nswe', )
    Label(frame, text=f"Mot de passe", font=("Arial", 10), padx=10, pady=10).grid(row=11, column=0, sticky='nswe', )

    nom = Entry(frame, text=f"nom", font=("Arial", 10))
    nom.grid(row=1, column=1)
    prenom = Entry(frame, text=f"prenom", font=("Arial", 10))
    prenom.grid(row=2, column=1)
    num_adresse = Entry(frame, text=f"num adresse", font=("Arial", 10))
    num_adresse.grid(row=3, column=1)
    rue = Entry(frame, text=f"rue", font=("Arial", 10))
    rue.grid(row=4, column=1)
    code_postal = Entry(frame, text=f"code postal", font=("Arial", 10))
    code_postal.grid(row=5, column=1)
    ville = Entry(frame, text=f"ville", font=("Arial", 10))
    ville.grid(row=6, column=1)
    mail = Entry(frame, text=f"adresse mail", font=("Arial", 10))
    mail.grid(row=7, column=1)
    date_naissance = Entry(frame, text=f"date de naissance (YYYY-MM-DD) ", font=("Arial", 10))
    date_naissance.grid(row=8, column=1)
    tel = Entry(frame, text=f"tel", font=("Arial", 10))
    tel.grid(row=9, column=1)
    login = Entry(frame, text=f"login", font=("Arial", 10))
    login.grid(row=10, column=1)
    mdp = Entry(frame, text=f"mdp", font=("Arial", 10))
    mdp.grid(row=11, column=1)

    query = "SELECT id, nom, prenom, num_adresse,rue,code_postal,ville,mail,date_naissance,num_tel,statut_adhesion FROM Adherent NATURAL JOIN Utilisateur ;"

    cursor = conn.cursor()
    cursor.execute(query)
    adherents = cursor.fetchall()

    tree = ttk.Treeview(frame, columns=("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "c11"),
                        show='headings',
                        height=len(adherents))

    tree.column("# 1", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 1", text="ID Adhérent")
    tree.column("# 2", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 2", text="Nom")
    tree.column("# 3", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 3", text="Prénom")
    tree.column("# 4", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 4", text="Num")
    tree.column("# 5", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 5", text="Rue")
    tree.column("# 6", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 6", text="CP")
    tree.column("# 7", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 7", text="Ville")
    tree.column("# 8", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 8", text="Mail")
    tree.column("# 9", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 9", text="Naissance")
    tree.column("# 10", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 10", text="Tél")
    tree.column("# 11", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 11", text="Adhésion")

    for i in range(len(adherents)):
        tree.insert('', 'end', text="1", values=(
            adherents[i][0], adherents[i][1], adherents[i][2], adherents[i][3], adherents[i][4], adherents[i][5],
            adherents[i][6], adherents[i][7],
            adherents[i][8],
            adherents[i][9], adherents[i][10]))

    Label(frame, text=f"Liste des adhérents déjà existants", font=("Arial", 15, 'bold'), padx=10, pady=10).grid(row=0,
                                                                                                                column=3,
                                                                                                                columnspan=2)
    tree.grid(row=1, column=3, columnspan=11, rowspan=len(adherents), padx=10)

    Button(frame, text="Ajouter", command=lambda: addAdherent(win, conn, profil, frame, (
        nom.get(), prenom.get(), num_adresse.get(), rue.get(), code_postal.get(), ville.get(), mail.get(),
        date_naissance.get(), tel.get(), login.get(), mdp.get())), padx=20, bg="green").grid(row=13, column=2,
                                                                                             sticky='nswe')

    if (valid):
        Label(frame, text=f"Film ajouté !", fg='green', font=("Arial", 10), padx=10, pady=10).grid(row=12, column=0)
    elif (retry):
        Label(frame, text=f"Impossible d'ajouter l'adhérent !", fg='red', font=("Arial", 10), padx=10, pady=10).grid(row=12,
                                                                                                                 column=0)

    Button(frame, text="Retour", command=lambda: espacePersonnels(win, conn, profil, prev_frame=frame), padx=20).grid(
        row=13, column=0, sticky='nswe', )


def addAdherent(win, conn, profil, frame, values):
    print(values)
    cursor = conn.cursor()
    error = False
    valid = False
    try:
        query = f"INSERT INTO Utilisateur(nom, prenom, num_adresse, rue, code_postal, ville, mail) VALUES ('{values[0]}','{values[1]}', {int(values[2])},'{values[3]}',{int(values[4])},'{values[5]}','{values[6]}');"
        cursor.execute(query)
    except Exception as er:
        print(er)
        error = True
        conn.rollback()
    try:

        if (not error):
            # Les contraintes du MLD sont implicitement vérifiées par l'interface. Un utilisateur appartient forcément à une catégorie et elle ne peut pas se retrouver dans plusieurs catégories. Ici, on ne peut créer que des adhérents
            query = f"SELECT id FROM Utilisateur WHERE nom ='{values[0]}'and prenom='{values[1]}'and num_adresse= {int(values[2])} and rue='{values[3]}' and code_postal={int(values[4])} and ville='{values[5]}'and mail='{values[6]}';"
            cursor.execute(query)
            id = cursor.fetchone()[0]
            query = f"INSERT INTO Adherent VALUES ({id},DATE('{values[7]}'),{values[8]},'active');"
            cursor.execute(query)
    except Exception as er:
        print(er)
        error = True
        conn.rollback()
    try:
        if (not error):
            query = f"INSERT INTO Compte VALUES ({id},'{values[9]}','{values[10]}');"
            cursor.execute(query)
            print("ajout adhérent")
            conn.commit()
            valid = True
    except Exception as er:
        print(er)
        error = True
        conn.rollback()

    addAdherent_frame(win, conn, profil, error, frame, valid)


def addSanction_frame(win, conn, profil, retry=False, prev_frame=None, valid=False):
    if (prev_frame != None): clear_frame(prev_frame)
    frame = Frame(win)
    frame.grid(row=0, sticky="ew")
    Label(frame, text=f"Ajouter une Sanction", font=("Arial", 20), padx=10, pady=10).grid(row=0, column=0, columnspan=3)
    Label(frame, text=f"ID Adhérent", font=("Arial", 10), padx=10, pady=10).grid(row=1, column=0, sticky='nswe')
    Label(frame, text=f"Motif ('retard','deterioration' ou 'perte')", font=("Arial", 10), padx=10, pady=10).grid(row=2,
                                                                                                                 column=0)
    Label(frame, text=f"Date d'émission (YYYY-MM-DD)", font=("Arial", 10), padx=10, pady=10).grid(row=3, column=0, sticky='nswe')

    id = Entry(frame, font=("Arial", 10))
    id.grid(row=1, column=1)
    motif = Entry(frame, font=("Arial", 10))
    motif.grid(row=2, column=1)
    date = Entry(frame, font=("Arial", 10))
    date.grid(row=3, column=1)

    query = "SELECT id, nom, prenom,mail,date_naissance,num_tel,statut_adhesion FROM Adherent NATURAL JOIN Utilisateur ;"

    cursor = conn.cursor()
    cursor.execute(query)
    adherents = cursor.fetchall()

    tree = ttk.Treeview(frame, columns=("c1", "c2", "c3", "c4", "c5", "c6", "c7"),
                        show='headings',
                        height=len(adherents))

    tree.column("# 1", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 1", text="ID Adhérent")
    tree.column("# 2", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 2", text="Nom")
    tree.column("# 3", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 3", text="Prénom")
    tree.column("# 4", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 4", text="Mail")
    tree.column("# 5", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 5", text="Naissance")
    tree.column("# 6", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 6", text="Tél")
    tree.column("# 7", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 7", text="Adhésion")

    for i in range(len(adherents)):
        tree.insert('', 'end', text="1", values=(
            adherents[i][0], adherents[i][1], adherents[i][2], adherents[i][3], adherents[i][4], adherents[i][5],
            adherents[i][6]))

    Label(frame, text=f"Liste des adhérents", font=("Arial", 15, 'bold'), padx=10, pady=10).grid(row=0, column=3,
                                                                                                 columnspan=2)
    tree.grid(row=1, column=3, columnspan=7, rowspan=len(adherents), padx=10)

    if (valid):
        Label(frame, text=f"Sanction ajoutée !", fg='green', font=("Arial", 10), padx=10, pady=10).grid(row=12,
                                                                                                        column=0)
    elif (retry):
        Label(frame, text=f"Impossible d'ajouter la sanction!", fg='red', font=("Arial", 10), padx=10, pady=10).grid(
            row=12,
            column=0)
    Button(frame, text="Ajouter",
           command=lambda: addSanction(win, conn, profil, frame, (id.get(), motif.get(), date.get())), padx=20,
           bg="green").grid(
        row=13, column=2)
    Button(frame, text="Retour", command=lambda: espacePersonnels(win, conn, profil, prev_frame=frame), padx=20).grid(
        row=13, column=0)


def addSanction(win, conn, profil, frame, values):
    print(values)
    cursor = conn.cursor()
    error = False
    valid = False
    try:
        query = f"INSERT INTO Sanction(idadherent,motif,date_debut,date_fin) VALUES ({int(values[0])},'{values[1]}',DATE('{values[2]}'),NULL);"
        cursor.execute(query)
        conn.commit()
        valid = True
    except Exception:
        error = True
        conn.rollback()

    addSanction_frame(win, conn, profil, error, frame, valid)


def addFilm_frame(win, conn, profil, retry=False, prev_frame=None, valid=False):
    if (prev_frame != None): clear_frame(prev_frame)
    frame = Frame(win)
    frame.grid(row=0, sticky="ew")
    Label(frame, text=f"Ajouter un Film", font=("Arial", 20), padx=10, pady=10).grid(row=0, column=0, columnspan=2)
    Label(frame, text=f"Code", font=("Arial", 10), padx=10, pady=10).grid(row=1, column=0, sticky='nswe')
    Label(frame, text=f"Titre", font=("Arial", 10), padx=10, pady=10).grid(row=2, column=0)
    Label(frame, text=f"Apparition (YYYY-MM-DD)", font=("Arial", 10), padx=10, pady=10).grid(row=3, column=0, sticky='nswe')
    Label(frame, text=f"Classification", font=("Arial", 10), padx=10, pady=10).grid(row=4, column=0, sticky='nswe')
    Label(frame, text=f"Éditeur", font=("Arial", 10), padx=10, pady=10).grid(row=5, column=0, sticky='nswe')
    Label(frame, text=f"Genre", font=("Arial", 10), padx=10, pady=10).grid(row=6, column=0, sticky='nswe')
    Label(frame, text=f"Synopsis", font=("Arial", 10), padx=10, pady=10).grid(row=7, column=0, sticky='nswe')
    Label(frame, text=f"Langue", font=("Arial", 10), padx=10, pady=10).grid(row=8, column=0, sticky='nswe')
    Label(frame, text=f"Longueur", font=("Arial", 10), padx=10, pady=10).grid(row=9, column=0, sticky='nswe')

    code = Entry(frame, text=f"code", font=("Arial", 10))
    code.grid(row=1, column=1)
    titre = Entry(frame, text=f"titre", font=("Arial", 10))
    titre.grid(row=2, column=1)
    apparition = Entry(frame, text=f"apparition (YYYY-MM-DD)", font=("Arial", 10))
    apparition.grid(row=3, column=1)
    classification = Entry(frame, text=f"classification", font=("Arial", 10))
    classification.grid(row=4, column=1)
    editeur = Entry(frame, text=f"editeur", font=("Arial", 10))
    editeur.grid(row=5, column=1)
    genre = Entry(frame, text=f"genre", font=("Arial", 10))
    genre.grid(row=6, column=1)
    synopsis = Entry(frame, text=f"synopsis", font=("Arial", 10))
    synopsis.grid(row=7, column=1)
    langue = Entry(frame, text=f"langue", font=("Arial", 10))
    langue.grid(row=8, column=1)
    longueur = Entry(frame, text=f"longueur", font=("Arial", 10))
    longueur.grid(row=9, column=1)

    query = "SELECT Ressource.code,titre,date_apparition,code_classification,editeur,genre,synopsis,langue,longueur FROM RESSOURCE NATURAL JOIN FILM;"
    cursor = conn.cursor()
    cursor.execute(query)
    films = cursor.fetchall()

    tree = ttk.Treeview(frame, columns=("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9"), show='headings',
                        height=len(films))

    tree.column("# 1", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 1", text="Code")
    tree.column("# 2", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 2", text="Titre")
    tree.column("# 3", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 3", text="Apparition")
    tree.column("# 4", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 4", text="Classification")
    tree.column("# 5", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 5", text="Editeur")
    tree.column("# 6", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 6", text="Genre")
    tree.column("# 7", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 7", text="Synopsis")
    tree.column("# 8", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 8", text="Langue")
    tree.column("# 9", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 9", text="Longueur")
    for i in range(len(films)):
        tree.insert('', 'end', text="1", values=(
        films[i][0], films[i][1], films[i][2], films[i][3], films[i][4], films[i][5], films[i][6], films[i][7],
        films[i][8]))
    tree.grid(row=0, column=3, columnspan=9, rowspan=len(films), padx=10)

    if (valid):
        Label(frame, text=f"Film ajouté !", fg='green', font=("Arial", 10), padx=10, pady=10).grid(row=12, column=0)
    elif (retry):
        Label(frame, text=f"Impossible d'ajouter le film!", fg='red', font=("Arial", 10), padx=10, pady=10).grid(row=12,
                                                                                                                 column=0)

    Button(frame, text="Ajouter", bg="green", command=lambda: addFilm(win, conn, profil, frame, (
    code.get(), titre.get(), apparition.get(), classification.get(), editeur.get(), genre.get(), synopsis.get(),
    langue.get(), longueur.get())), padx=20).grid(row=100, column=2)

    Button(frame, text="Retour", command=lambda: addRessource_frame(win, conn, profil, prev_frame=frame), padx=20).grid(
        row=100, column=0)


def addFilm(win, conn, profil, frame, values):
    print(values)
    cursor = conn.cursor()
    error = False
    valid = False
    try:
        query = f"INSERT INTO Ressource VALUES ({int(values[0])},'{values[1]}',DATE('{values[2]}'),{int(values[3])},'{values[4]}','{values[5]}');"
        cursor.execute(query)
    except Exception:
        error = True
        conn.rollback()
    try:
        if (not error):
            # Les contraintes du MLD sont implicitement vérifiées par l'interface. Un ressource appartient forcément à une catégorie et elle ne peut pas se retrouver dans plusieurs catégories
            query = f"INSERT INTO Film VALUES ({int(values[0])},'{values[6]}','{values[7]}',{int(values[8])});"
            cursor.execute(query)
            print("ajout film")
            conn.commit()
            valid = True
    except Exception:
        error = True;
        conn.rollback()

    addFilm_frame(win, conn, profil, error, frame, valid)


def addMusique_frame(win, conn, profil, retry=False, prev_frame=None, valid=False):
    if (prev_frame != None): clear_frame(prev_frame)
    frame = Frame(win)
    frame.grid(row=0, sticky="ew")
    Label(frame, text=f"Ajouter une Musique", font=("Arial", 20), padx=10, pady=10).grid(row=0, column=0, columnspan=2)
    Label(frame, text=f"Code", font=("Arial", 10), padx=10, pady=10).grid(row=1, column=0, sticky='nswe')
    Label(frame, text=f"Titre", font=("Arial", 10), padx=10, pady=10).grid(row=2, column=0, sticky='nswe')
    Label(frame, text=f"Apparition (YYYY-MM-DD)", font=("Arial", 10), padx=10, pady=10).grid(row=3, column=0, sticky='nswe')
    Label(frame, text=f"Classification", font=("Arial", 10), padx=10, pady=10).grid(row=4, column=0, sticky='nswe')
    Label(frame, text=f"Éditeur", font=("Arial", 10), padx=10, pady=10).grid(row=5, column=0, sticky='nswe')
    Label(frame, text=f"Genre", font=("Arial", 10), padx=10, pady=10).grid(row=6, column=0, sticky='nswe')
    Label(frame, text=f"Longueur", font=("Arial", 10), padx=10, pady=10).grid(row=7, column=0, sticky='nswe')

    code = Entry(frame, text=f"code", font=("Arial", 10))
    code.grid(row=1, column=1)
    titre = Entry(frame, text=f"titre", font=("Arial", 10))
    titre.grid(row=2, column=1)
    apparition = Entry(frame, text=f"apparition (YYYY-MM-DD)", font=("Arial", 10))
    apparition.grid(row=3, column=1)
    classification = Entry(frame, text=f"classification", font=("Arial", 10))
    classification.grid(row=4, column=1)
    editeur = Entry(frame, text=f"editeur", font=("Arial", 10))
    editeur.grid(row=5, column=1)
    genre = Entry(frame, text=f"genre", font=("Arial", 10))
    genre.grid(row=6, column=1)
    longueur = Entry(frame, text=f"longueur", font=("Arial", 10))
    longueur.grid(row=7, column=1)

    query = "SELECT Ressource.code,titre,date_apparition,code_classification,editeur,genre,longueur FROM RESSOURCE NATURAL JOIN Musique;"
    cursor = conn.cursor()
    cursor.execute(query)
    musiques = cursor.fetchall()

    tree = ttk.Treeview(frame, columns=("c1", "c2", "c3", "c4", "c5", "c6", "c7"), show='headings',
                        height=len(musiques))

    tree.column("# 1", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 1", text="Code")
    tree.column("# 2", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 2", text="Titre")
    tree.column("# 3", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 3", text="Apparition")
    tree.column("# 4", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 4", text="Classification")
    tree.column("# 5", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 5", text="Editeur")
    tree.column("# 6", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 6", text="Genre")
    tree.column("# 7", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 7", text="Longueur")

    for i in range(len(musiques)):
        tree.insert('', 'end', text="1", values=(
            musiques[i][0], musiques[i][1], musiques[i][2], musiques[i][3], musiques[i][4], musiques[i][5],
            musiques[i][6]))
    tree.grid(row=0, column=3, columnspan=9, rowspan=len(musiques), padx=10)

    if (valid):
        Label(frame, text=f"Musique ajoutée !", fg='green', font=("Arial", 10), padx=10, pady=10).grid(row=12, column=0)
    elif (retry):
        Label(frame, text=f"Impossible d'ajouter la musique !", fg='red', font=("Arial", 10), padx=10, pady=10).grid(
            row=12, column=0)

    Button(frame, text="Ajouter", bg="green", command=lambda: addMusique(win, conn, profil, frame, (
    code.get(), titre.get(), apparition.get(), classification.get(), editeur.get(), genre.get(), longueur.get())),
           padx=20).grid(row=13, column=2)
    Button(frame, text="Retour", command=lambda: addRessource_frame(win, conn, profil, prev_frame=frame), padx=20).grid(
        row=13, column=0)


def addMusique(win, conn, profil, frame, values):
    print(values)
    cursor = conn.cursor()
    error = False
    valid = False
    try:
        query = f"INSERT INTO Ressource VALUES ({int(values[0])},'{values[1]}',DATE('{values[2]}'),{int(values[3])},'{values[4]}','{values[5]}');"
        cursor.execute(query)
    except Exception as error:
        print(error)
        error = True
        conn.rollback()
    try:
        if (not error):
            # Les contraintes du MLD sont implicitement vérifiées par l'interface. Un ressource appartient forcément à une catégorie et elle ne peut pas se retrouver dans plusieurs catégories
            query = f"INSERT INTO Musique VALUES ({int(values[0])},{int(values[6])});"
            cursor.execute(query)
            print("ajout musique")
            conn.commit()
            valid = True
    except Exception as er:
        print(er)
        error = True;
        conn.rollback()

    print(error)

    addMusique_frame(win, conn, profil, error, frame, valid)


def addLivre_frame(win, conn, profil, retry=False, prev_frame=None, valid=False):
    if (prev_frame != None): clear_frame(prev_frame)
    frame = Frame(win)
    frame.grid(row=0, sticky="ew")
    Label(frame, text=f"Ajouter un Livre", font=("Arial", 20), padx=10, pady=10).grid(row=0, column=0, columnspan=2)
    Label(frame, text=f"Code", font=("Arial", 10), padx=10, pady=10).grid(row=1, column=0, sticky='nswe')
    Label(frame, text=f"Titre", font=("Arial", 10), padx=10, pady=10).grid(row=2, column=0, sticky='nswe')
    Label(frame, text=f"Apparition (YYYY-MM-DD)", font=("Arial", 10), padx=10, pady=10).grid(row=3, column=0, sticky='nswe')
    Label(frame, text=f"Classification", font=("Arial", 10), padx=10, pady=10).grid(row=4, column=0, sticky='nswe')
    Label(frame, text=f"Éditeur", font=("Arial", 10), padx=10, pady=10).grid(row=5, column=0, sticky='nswe')
    Label(frame, text=f"Genre", font=("Arial", 10), padx=10, pady=10).grid(row=6, column=0, sticky='nswe')
    Label(frame, text=f"ISBN", font=("Arial", 10), padx=10, pady=10).grid(row=7, column=0, sticky='nswe')
    Label(frame, text=f"Résumé", font=("Arial", 10), padx=10, pady=10).grid(row=8, column=0, sticky='nswe')
    Label(frame, text=f"Langue", font=("Arial", 10), padx=10, pady=10).grid(row=9, column=0, sticky='nswe')

    code = Entry(frame, text=f"code", font=("Arial", 10))
    code.grid(row=1, column=1)
    titre = Entry(frame, text=f"titre", font=("Arial", 10))
    titre.grid(row=2, column=1)
    apparition = Entry(frame, text=f"apparition (YYYY-MM-DD)", font=("Arial", 10))
    apparition.grid(row=3, column=1)
    classification = Entry(frame, text=f"classification", font=("Arial", 10))
    classification.grid(row=4, column=1)
    editeur = Entry(frame, text=f"editeur", font=("Arial", 10))
    editeur.grid(row=5, column=1)
    genre = Entry(frame, text=f"genre", font=("Arial", 10))
    genre.grid(row=6, column=1)
    synopsis = Entry(frame, text=f"ISBN", font=("Arial", 10))
    synopsis.grid(row=7, column=1)
    langue = Entry(frame, text=f"resume", font=("Arial", 10))
    langue.grid(row=8, column=1)
    longueur = Entry(frame, text=f"langue", font=("Arial", 10))
    longueur.grid(row=9, column=1)

    query = "SELECT Ressource.code,titre,date_apparition,code_classification,editeur,genre,ISBN,resume,langue FROM RESSOURCE NATURAL JOIN Livre;"
    cursor = conn.cursor()
    cursor.execute(query)
    livres = cursor.fetchall()

    tree = ttk.Treeview(frame, columns=("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9"), show='headings',
                        height=len(livres))

    tree.column("# 1", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 1", text="Code")
    tree.column("# 2", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 2", text="Titre")
    tree.column("# 3", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 3", text="Apparition")
    tree.column("# 4", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 4", text="Classification")
    tree.column("# 5", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 5", text="Editeur")
    tree.column("# 6", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 6", text="Genre")
    tree.column("# 7", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 7", text="ISBN")
    tree.column("# 8", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 8", text="Résumé")
    tree.column("# 9", anchor=CENTER, minwidth=0, width=100, stretch=NO)
    tree.heading("# 9", text="Langue")
    for i in range(len(livres)):
        tree.insert('', 'end', text="1", values=(
            livres[i][0], livres[i][1], livres[i][2], livres[i][3], livres[i][4], livres[i][5], livres[i][6],
            livres[i][7],
            livres[i][8]))
    tree.grid(row=0, column=3, columnspan=9, rowspan=len(livres), padx=10)

    if (valid):
        Label(frame, text=f"Livre ajouté !", fg='green', font=("Arial", 10), padx=10, pady=10).grid(row=12, column=0)
    elif (retry):
        Label(frame, text=f"Impossible d'ajouter le livre !", fg='red', font=("Arial", 10), padx=10, pady=10).grid(
            row=12, column=0)

    Button(frame, text="Ajouter", bg='green', command=lambda: addLivre(win, conn, profil, frame, (
    code.get(), titre.get(), apparition.get(), classification.get(), editeur.get(), genre.get(), synopsis.get(),
    langue.get(), longueur.get())), padx=20).grid(row=13, column=2)
    Button(frame, text="Retour", command=lambda: addRessource_frame(win, conn, profil, prev_frame=frame), padx=20).grid(
        row=13, column=0)


def addLivre(win, conn, profil, frame, values):
    print(values)
    cursor = conn.cursor()
    error = False
    valid = False
    try:
        query = f"INSERT INTO Ressource VALUES ({int(values[0])},'{values[1]}',DATE('{values[2]}'),{int(values[3])},'{values[4]}','{values[5]}');"
        cursor.execute(query)
    except Exception as er:
        print(er)
        error = True
        conn.rollback()
    try:
        if (not error):
            # Les contraintes du MLD sont implicitement vérifiées par l'interface. Un ressource appartient forcément à une catégorie et elle ne peut pas se retrouver dans plusieurs catégories
            query = f"INSERT INTO Livre VALUES ({int(values[0])},'{values[6]}','{values[7]}', '{values[8]}');"
            cursor.execute(query)
            print("ajout livre")
            conn.commit()
            valid = True
    except Exception as er:
        print(er)
        error = True;
        conn.rollback()

    addLivre_frame(win, conn, profil, error, frame, valid)


def accesSanctions(win, conn, prev_frame, profil):
    if (prev_frame != None): clear_frame(prev_frame)
    frame = Frame(win)
    frame.grid(row=0, sticky="ew")
    Label(frame, text=f"Mes sanctions", font=("Arial", 20), padx=10, pady=10).grid(row=0, column=0, columnspan=3)

    cursor = conn.cursor()
    query = f"SELECT motif,date_debut,date_fin FROM Sanction WHERE idAdherent = {profil[0]};"
    cursor.execute(query)
    sanctions = cursor.fetchall()
    print(sanctions)
    tree = ttk.Treeview(frame, columns=("c1", "c2", "c3"), show='headings', height=len(sanctions))
    tree.column("# 1", anchor=CENTER)
    tree.heading("# 1", text="Motif")
    tree.column("# 2", anchor=CENTER)
    tree.heading("# 2", text="Date d'émission'")
    tree.column("# 3", anchor=CENTER)
    tree.heading("# 3", text="Date de résolution")

    for i in range(len(sanctions)):
        tree.insert('', 'end', text="1", values=(
            sanctions[i][0], sanctions[i][1], sanctions[i][2] if sanctions[i][2] != None else 'non résolue'))
    tree.grid(row=1, columnspan=3)

    Button(frame, text="<", command=lambda: espaceAdherents(win, conn, profil, frame), padx=20).grid(
        row=0, column=0)


def espaceFilms(win, conn, prev_frame, profil):
    """Récuperation des films"""

    if (prev_frame != None): clear_frame(prev_frame)
    frame = Frame(win)
    frame.grid(row=0, column=0)
    Label(frame, text=f"Espace Films : ", font=("Arial", 20), padx=10).grid(row=0, column=1)
    cursor = conn.cursor()
    query = "SELECT code,code_classification,titre, date_apparition, genre, langue, longueur FROM Ressource NATURAL JOIN Film F ;"
    cursor.execute(query)
    films = cursor.fetchall()
    print(films)
    tree = ttk.Treeview(frame, columns=("c1", "c2", "c3", "c4", "c5", "c6"), show='headings', height=len(films))
    tree.column("# 1", anchor=CENTER)
    tree.heading("# 1", text="Classification")
    tree.column("# 2", anchor=CENTER)
    tree.heading("# 2", text="Titre")
    tree.column("# 3", anchor=CENTER)
    tree.heading("# 3", text="Apparition (YYYY-MM-DD)")
    tree.column("# 4", anchor=CENTER)
    tree.heading("# 4", text="Genre")
    tree.column("# 5", anchor=CENTER)
    tree.heading("# 5", text="Langue")
    tree.column("# 6", anchor=CENTER)
    tree.heading("# 6", text="Longueur")

    for i in range(1, len(films) + 1):
        tree.insert('', 'end', text="1",
                    values=(films[i - 1][1], films[i - 1][2], films[i - 1][3], films[i - 1][4], films[i - 1][5],
                            films[i - 1][6]))
        Button(frame, text="plus de détails",
               command=lambda v=films[i - 1][0]: afficherFilm(win, conn, v, profil, frame)).grid(
            row=i + 1, column=7, sticky='s')
    tree.grid(row=1, columnspan=6, rowspan=len(films) + 1)

    Button(frame, text="<", command=lambda: espaceAdherents(win, conn, profil, frame), padx=10).grid(
        row=0, column=0)


def afficherFilm(win, conn, film, profil, prev_frame=None):
    if (prev_frame != None): clear_frame(prev_frame)
    frame = Frame(win)
    frame.grid(row=0, sticky="ew")
    cursor = conn.cursor()
    query = f"SELECT F.code, titre, date_apparition, code_classification,editeur, genre, synopsis, langue, longueur FROM Ressource INNER JOIN Film F ON F.code = Ressource.code WHERE F.code = '{film}';"
    cursor.execute(query)
    film = cursor.fetchone()
    print(film)

    query = f"SELECT COUNT(*) FROM Exemplaire E WHERE E.code_ressource = {film[0]} AND etat<>'perdu';"
    cursor.execute(query)
    total = cursor.fetchone()[0]

    query = f"SELECT COUNT(*) FROM Pret P WHERE P.code_ressource = {film[0]} AND rendu = false ;"
    cursor.execute(query)
    non_dispo = cursor.fetchone()[0]

    query = f"SELECT * FROM Pret P ;"
    cursor.execute(query)
    print(cursor.fetchall())

    Label(frame, text=f"Information du Film : ", font=("Arial", 15), padx=10, pady=10).grid(row=0, column=0,
                                                                                            columnspan=3)
    Label(frame, text=f"Titre: ", font=("Arial", 10, 'bold'), padx=10, pady=10).grid(row=1, column=0, sticky='w')
    Label(frame, text=f"{film[1]}", font=("Arial", 10), padx=10, pady=10).grid(row=1, column=1, sticky='w')
    Label(frame, text=f"Date d'apparition (YYYY-MM-DD): ", font=("Arial", 10, 'bold'), padx=10, pady=10).grid(row=2, column=0,
                                                                                                sticky='w')
    Label(frame, text=f"{film[2]}", font=("Arial", 10), padx=10, pady=10).grid(row=2, column=1, sticky='w')
    Label(frame, text=f"Code de classification : ", font=("Arial", 10, 'bold'), padx=10, pady=10).grid(row=3, column=0,
                                                                                                       sticky='w')
    Label(frame, text=f"{film[3]}", font=("rAial", 10), padx=10, pady=10).grid(row=3, column=1, sticky='w')
    Label(frame, text=f"Editeur : ", font=("Arial", 10, 'bold'), padx=10, pady=10).grid(row=4, column=0, sticky='w')
    Label(frame, text=f"{film[4]}", font=("Arial", 10), padx=10, pady=10).grid(row=4, column=1, sticky='w')
    Label(frame, text=f"Genre : ", font=("Arial", 10, 'bold'), padx=10, pady=10).grid(row=5, column=0, sticky='w')
    Label(frame, text=f"{film[5]}", font=("Arial", 10), padx=10, pady=10).grid(row=5, column=1, sticky="w")
    Label(frame, text=f"Synopsis : ", font=("Arial", 10, 'bold'), padx=10, pady=10).grid(row=6, column=0, sticky='w')
    Label(frame, text=f"{film[6]}", font=("Arial", 10), padx=10, pady=10).grid(row=6, column=1, sticky='w')
    Label(frame, text=f"Langue : ", font=("Arial", 10, 'bold'), padx=10, pady=10).grid(row=7, column=0, sticky='w')
    Label(frame, text=f"{film[7]}", font=("Arial", 10), padx=10, pady=10).grid(row=7, column=1, sticky='w')
    Label(frame, text=f"Longueur : ", font=("Arial", 10, 'bold'), padx=10, pady=10).grid(row=8, column=0, sticky='w')
    Label(frame, text=f"{film[8]} min", font=("Arial", 10), padx=10, pady=10).grid(row=8, column=1, sticky='w')
    Label(frame, text=f"Disponibilité : ", font=("Arial", 10, 'bold'), padx=10, pady=10).grid(row=9, column=0,
                                                                                              sticky='w')
    print(non_dispo)
    Label(frame, text=f"{total - non_dispo}/{total}", font=("Arial", 10), padx=10, pady=10).grid(row=9, column=1,
                                                                                                 sticky='w')

    query = f"SELECT nom, prenom FROM Realisateur INNER JOIN Film F ON F.code = Realisateur.film INNER JOIN Contributeur C ON C.id = Realisateur.contrib WHERE F.code = '{film[0]}';"
    cursor.execute(query)
    realisateurs = cursor.fetchall()
    print(realisateurs)

    Label(frame, text=f"Réalisateur(s) :", font=("Arial", 10, 'bold'), padx=10, pady=10).grid(row=10, column=0,
                                                                                              columnspan=3)
    tree = ttk.Treeview(frame, columns=("c1", "c2"), show='headings', height=len(realisateurs))
    tree.column("# 1", anchor=CENTER)
    tree.heading("# 1", text="Nom")
    tree.column("# 2", anchor=CENTER)
    tree.heading("# 2", text="Prénom")

    for i in range(len(realisateurs)):
        tree.insert('', 'end', text="1", values=(realisateurs[i][0], realisateurs[i][1]))
    tree.grid(row=11, columnspan=3)

    query = f"SELECT nom, prenom FROM Acteur INNER JOIN Film F ON F.code = Acteur.film INNER JOIN Contributeur C ON C.id = Acteur.contrib WHERE F.code = '{film[0]}';"
    cursor.execute(query)
    acteurs = cursor.fetchall()
    print(acteurs)

    Label(frame, text=f"Acteur(s) :", font=("Arial", 10, 'bold'), padx=10, pady=10).grid(row=10, column=4, columnspan=3)
    tree = ttk.Treeview(frame, columns=("c1", "c2"), show='headings', height=len(acteurs))
    tree.column("# 1", anchor=CENTER)
    tree.heading("# 1", text="Nom")
    tree.column("# 2", anchor=CENTER)
    tree.heading("# 2", text="Prénom")

    for i in range(len(acteurs)):
        tree.insert('', 'end', text="1", values=(acteurs[i][0], acteurs[i][1]))
    tree.grid(row=11, column=4, columnspan=3)

    Button(frame, text="<", command=lambda: espaceFilms(win, conn, frame, profil), padx=20).grid(row=0, column=0)


def espaceMusiques(win, conn, prev_frame, profil):
    """Récuperation des musiques"""
    if (prev_frame != None): clear_frame(prev_frame)
    frame = Frame(win)
    frame.grid(row=0, sticky="ew")
    Label(frame, text=f"Espace Musiques: ", font=("Arial", 20), padx=10, pady=10).grid(row=0, column=1)
    cursor = conn.cursor()
    query = "SELECT code,code_classification,titre, date_apparition, genre, longueur FROM Ressource NATURAL JOIN Musique ;"
    cursor.execute(query)
    musiques = cursor.fetchall()
    print(musiques)
    tree = ttk.Treeview(frame, columns=("c1", "c2", "c3", "c4", "c5"), show='headings', height=len(musiques))
    tree.column("# 1", anchor=CENTER)
    tree.heading("# 1", text="Classification")
    tree.column("# 2", anchor=CENTER)
    tree.heading("# 2", text="Titre")
    tree.column("# 3", anchor=CENTER)
    tree.heading("# 3", text="Apparition")
    tree.column("# 4", anchor=CENTER)
    tree.heading("# 4", text="Genre")
    tree.column("# 5", anchor=CENTER)
    tree.heading("# 5", text="Longueur")

    for i in range(1, len(musiques) + 1):
        tree.insert('', 'end', text="1",
                    values=(
                    musiques[i - 1][1], musiques[i - 1][2], musiques[i - 1][3], musiques[i - 1][4], musiques[i - 1][5]))
        Button(frame, text="plus de détails",
               command=lambda v=musiques[i - 1][0]: afficherMusique(win, conn, v, profil, frame)).grid(row=i + 1,
                                                                                                       column=6,
                                                                                                       sticky='s', )
    tree.grid(row=1, columnspan=5, rowspan=len(musiques) + 1)

    Button(frame, text="<", command=lambda: espaceAdherents(win, conn, profil, frame), padx=20).grid(
        row=0, column=0)


def afficherMusique(win, conn, musique, profil, prev_frame=None):
    if (prev_frame != None): clear_frame(prev_frame)
    frame = Frame(win)
    frame.grid(row=0, sticky="ew")
    cursor = conn.cursor()
    query = f"SELECT M.code, titre, date_apparition, code_classification,editeur, genre, longueur FROM Ressource INNER JOIN Musique M ON M.code = Ressource.code WHERE M.code = '{musique}';"
    cursor.execute(query)
    musique = cursor.fetchone()
    print(musique)

    query = f"SELECT COUNT(*) FROM Exemplaire E WHERE E.code_ressource = {musique[0]};"
    cursor.execute(query)
    total = cursor.fetchone()[0]

    query = f"SELECT COUNT(*) FROM Pret P WHERE P.code_ressource = {musique[0]} AND rendu = false ;"
    cursor.execute(query)
    non_dispo = cursor.fetchone()[0]

    Label(frame, text=f"Information de la Musique: ", font=("Arial", 15), padx=10, pady=10).grid(row=1, column=0,
                                                                                                 columnspan=3)
    Label(frame, text=f"Titre: {musique[1]}", font=("Arial", 10), padx=10, pady=10).grid(row=2, column=0, columnspan=3)
    Label(frame, text=f"Date d'apparition (YYYY-MM-DD): {musique[2]}", font=("Arial", 10), padx=10, pady=10).grid(row=3, column=0,
                                                                                                     columnspan=3)
    Label(frame, text=f"Code de classification : {musique[3]}", font=("Arial", 10), padx=10, pady=10).grid(row=4,
                                                                                                           column=0,
                                                                                                           columnspan=3)
    Label(frame, text=f"Editeur : {musique[4]}", font=("Arial", 10), padx=10, pady=10).grid(row=5, column=0,
                                                                                            columnspan=3)
    Label(frame, text=f"Genre : {musique[5]}", font=("Arial", 10), padx=10, pady=10).grid(row=6, column=0, columnspan=3)
    Label(frame, text=f"Longueur : {musique[6]} min", font=("Arial", 10), padx=10, pady=10).grid(row=7, column=0,
                                                                                                 columnspan=3)
    Label(frame, text=f"Disponibilité : ", font=("Arial", 10, 'bold'), padx=10, pady=10).grid(row=8, column=0,
                                                                                              sticky='w')
    Label(frame, text=f"{total - non_dispo}/{total}", font=("Arial", 10), padx=10, pady=10).grid(row=8, column=1,
                                                                                                 sticky='w')

    query = f"SELECT nom, prenom FROM Compositeur INNER JOIN Musique M ON M.code = Compositeur.musique INNER JOIN Contributeur C ON C.id = Compositeur.contrib WHERE M.code = '{musique[0]}';"
    cursor.execute(query)
    compositeurs = cursor.fetchall()
    print(compositeurs)

    Label(frame, text=f"Compositeur(s) :", font=("Arial", 10), padx=10, pady=10).grid(row=9, column=0, columnspan=3)
    tree = ttk.Treeview(frame, columns=("c1", "c2"), show='headings', height=len(compositeurs))
    tree.column("# 1", anchor=CENTER)
    tree.heading("# 1", text="Nom")
    tree.column("# 2", anchor=CENTER)
    tree.heading("# 2", text="Prénom")

    for i in range(len(compositeurs)):
        tree.insert('', 'end', text="1", values=(compositeurs[i][0], compositeurs[i][1]))
    tree.grid(row=10, columnspan=3)

    query = f"SELECT nom, prenom FROM Interprete INNER JOIN Musique M ON M.code = Interprete.musique INNER JOIN Contributeur C ON C.id = Interprete.contrib WHERE M.code = '{musique[0]}';"
    cursor.execute(query)
    interpretes = cursor.fetchall()
    print(interpretes)

    Label(frame, text=f"Interprète(s) :", font=("Arial", 10), padx=10, pady=10).grid(row=9, column=4, columnspan=3)
    tree = ttk.Treeview(frame, columns=("c1", "c2"), show='headings', height=len(interpretes))
    tree.column("# 1", anchor=CENTER)
    tree.heading("# 1", text="Nom")
    tree.column("# 2", anchor=CENTER)
    tree.heading("# 2", text="Prénom")

    for i in range(len(interpretes)):
        tree.insert('', 'end', text="1", values=(interpretes[i][0], interpretes[i][1]))
    tree.grid(row=10, column=4, columnspan=3)

    Button(frame, text="<", command=lambda: espaceMusiques(win, conn, frame,profil), padx=20).grid(
        row=0, column=0)


def espaceLivres(win, conn, prev_frame, profil):
    """Récuperation des livres"""
    if (prev_frame != None): clear_frame(prev_frame)
    frame = Frame(win)
    frame.grid(row=0, sticky="ew")
    Label(frame, text=f"Espace Livres : ", font=("Arial", 20), padx=10, pady=10).grid(row=0, column=1)
    cursor = conn.cursor()
    query = "SELECT code,code_classification,titre, date_apparition, genre, langue, ISBN FROM Ressource NATURAL JOIN Livre L ;"
    cursor.execute(query)
    livres = cursor.fetchall()
    print(livres)

    tree = ttk.Treeview(frame, columns=("c1", "c2", "c3", "c4", "c5", "c6"), show='headings', height=len(livres))
    tree.column("# 1", anchor=CENTER)
    tree.heading("# 1", text="Classification")
    tree.column("# 2", anchor=CENTER)
    tree.heading("# 2", text="Titre")
    tree.column("# 3", anchor=CENTER)
    tree.heading("# 3", text="Apparition")
    tree.column("# 4", anchor=CENTER)
    tree.heading("# 4", text="Genre")
    tree.column("# 5", anchor=CENTER)
    tree.heading("# 5", text="Langue")
    tree.column("# 6", anchor=CENTER)
    tree.heading("# 6", text="ISBN")

    for i in range(1, len(livres) + 1):
        tree.insert('', 'end', text="1",
                    values=(livres[i - 1][1], livres[i - 1][2], livres[i - 1][3], livres[i - 1][4], livres[i - 1][5],
                            livres[i - 1][6]))
        Button(frame, text="plus de détails",
               command=lambda v=livres[i - 1][0]: afficherLivre(win, conn, v, profil, frame)).grid(
            row=i + 1, column=7, sticky='s')
    tree.grid(row=1, columnspan=6, rowspan=len(livres) + 1)

    Button(frame, text="<", command=lambda: espaceAdherents(win, conn, profil, frame), padx=20).grid(
        row=0, column=0)


def afficherLivre(win, conn, livre, profil, prev_frame=None):
    if (prev_frame != None): clear_frame(prev_frame)
    frame = Frame(win)
    frame.grid(row=0, sticky="ew")
    cursor = conn.cursor()
    query = f"SELECT L.code, titre, date_apparition, code_classification,editeur, genre, resume, langue, ISBN FROM Ressource INNER JOIN Livre L ON L.code = Ressource.code WHERE L.code = '{livre}';"
    cursor.execute(query)
    livre = cursor.fetchone()
    print(livre)

    query = f"SELECT COUNT(*) FROM Exemplaire E WHERE E.code_ressource = {livre[0]};"
    cursor.execute(query)
    total = cursor.fetchone()[0]

    query = f"SELECT COUNT(*) FROM Pret P WHERE P.code_ressource = {livre[0]} AND rendu = false ;"
    cursor.execute(query)
    non_dispo = cursor.fetchone()[0]

    Label(frame, text=f"Information du Livre : ", font=("Arial", 15), padx=10, pady=10).grid(row=1, column=0,
                                                                                             columnspan=3)
    Label(frame, text=f"Titre: {livre[1]}", font=("Arial", 10), padx=10, pady=10).grid(row=2, column=0, columnspan=3)
    Label(frame, text=f"Date d'apparition (YYYY-MM-DD): {livre[2]}", font=("Arial", 10), padx=10, pady=10).grid(row=3, column=0,
                                                                                                   columnspan=3)
    Label(frame, text=f"Code de classification : {livre[3]}", font=("Arial", 10), padx=10, pady=10).grid(row=4,
                                                                                                         column=0,
                                                                                                         columnspan=3)
    Label(frame, text=f"Editeur : {livre[4]}", font=("Arial", 10), padx=10, pady=10).grid(row=5, column=0, columnspan=3)
    Label(frame, text=f"Genre : {livre[5]}", font=("Arial", 10), padx=10, pady=10).grid(row=6, column=0, columnspan=3)
    Label(frame, text=f"Résumé : {livre[6]}", font=("Arial", 10), padx=10, pady=10).grid(row=7, column=0, columnspan=3)
    Label(frame, text=f"Langue : {livre[7]}", font=("Arial", 10), padx=10, pady=10).grid(row=8, column=0, columnspan=3)
    Label(frame, text=f"ISBN : {livre[8]}", font=("Arial", 10), padx=10, pady=10).grid(row=9, column=0, columnspan=3)
    Label(frame, text=f"Disponibilité : ", font=("Arial", 10, 'bold'), padx=10, pady=10).grid(row=10, column=0,
                                                                                              sticky='w')
    Label(frame, text=f"{total - non_dispo}/{total}", font=("Arial", 10), padx=10, pady=10).grid(row=10, column=1,
                                                                                                 sticky='w')

    query = f"SELECT nom, prenom FROM Auteur INNER JOIN Livre L ON L.code = Auteur.livre INNER JOIN Contributeur C ON C.id = Auteur.contrib WHERE L.code = '{livre[0]}';"
    cursor.execute(query)
    auteurs = cursor.fetchall()
    print(auteurs)

    Label(frame, text=f"Auteur(s) :", font=("Arial", 10), padx=10, pady=10).grid(row=11, column=0, columnspan=3)
    tree = ttk.Treeview(frame, columns=("c1", "c2"), show='headings', height=len(auteurs))
    tree.column("# 1", anchor=CENTER)
    tree.heading("# 1", text="Nom")
    tree.column("# 2", anchor=CENTER)
    tree.heading("# 2", text="Prénom")

    for i in range(len(auteurs)):
        tree.insert('', 'end', text="1", values=(auteurs[i][0], auteurs[i][1]))
    tree.grid(row=12, columnspan=3)

    print(frame.winfo_children())
    Button(frame, text="<", command=lambda: espaceLivres(win, conn,frame,profil), padx=20).grid(
        row=0, column=0)


def espaceContributeurs(win, conn, prev_frame, profil, order='None'):
    """Récuperation des Contributeurs"""
    if (prev_frame != None): clear_frame(prev_frame)
    frame = Frame(win)
    frame.grid(row=0, sticky="ew")
    Label(frame, text=f"Espace Contributeurs : ", font=("Arial", 20), padx=10, pady=10).grid(row=0, column=1)
    cursor = conn.cursor()
    supp = f"ORDER BY {order}"
    query = f"SELECT id,nom,prenom,date_naissance,nationalite FROM Contributeur {supp if order != 'None' else ''};"
    cursor.execute(query)
    contributeurs = cursor.fetchall()
    print(contributeurs)
    tree = ttk.Treeview(frame, columns=("c1", "c2", "c3", "c4"), show='headings', height=len(contributeurs))
    tree.column("# 1", anchor=CENTER)
    tree.heading("# 1", text="Nom", command=lambda: espaceContributeurs(win, conn, prev_frame, profil, 'nom'))
    tree.column("# 2", anchor=CENTER)
    tree.heading("# 2", text="Prénom", command=lambda: espaceContributeurs(win, conn, prev_frame, profil, 'prenom'))
    tree.column("# 3", anchor=CENTER)
    tree.heading("# 3", text="Naissance",
                 command=lambda: espaceContributeurs(win, conn, prev_frame, profil, 'date_naissance'))
    tree.column("# 4", anchor=CENTER)
    tree.heading("# 4", text="Nationalite",
                 command=lambda: espaceContributeurs(win, conn, prev_frame, profil, 'nationalite'))

    for i in range(1, len(contributeurs) + 1):
        tree.insert('', 'end', text="1", values=(
        contributeurs[i - 1][1], contributeurs[i - 1][2], contributeurs[i - 1][3], contributeurs[i - 1][4]))
        Button(frame, text="plus de détails",
               command=lambda v=contributeurs[i - 1][0]: afficherContributeur(win, conn, v, profil, frame)).grid(
            row=i + 1, column=5, sticky='s')

    tree.grid(row=1, columnspan=4, rowspan=len(contributeurs) + 1)

    Button(frame, text="<", command=lambda: espaceAdherents(win, conn, profil, frame), padx=20).grid(
        row=0, column=0)


def afficherContributeur(win, conn, contributeur, profil, prev_frame=None):
    print(contributeur)
    if (prev_frame != None): clear_frame(prev_frame)
    frame = Frame(win)
    frame.grid(row=0, sticky="ew")
    cursor = conn.cursor()
    query = f"SELECT id,nom,prenom,date_naissance,nationalite FROM Contributeur WHERE Contributeur.id = {contributeur};"
    cursor.execute(query)
    contributeur = cursor.fetchone()
    print(contributeur)
    Label(frame, text=f"Information du Contributeur : ", font=("Arial", 15), padx=10, pady=10).grid(row=1, column=0,
                                                                                                    columnspan=3)
    Label(frame, text=f"Nom: {contributeur[1]}", font=("Arial", 10), padx=10, pady=10).grid(row=2, column=0,
                                                                                            columnspan=3)
    Label(frame, text=f"Prénom: {contributeur[2]}", font=("Arial", 10), padx=10, pady=10).grid(row=3, column=0,
                                                                                               columnspan=3)
    Label(frame, text=f"date_naissance (YYYY-MM-DD) : {contributeur[3]}", font=("Arial", 10), padx=10, pady=10).grid(row=4, column=0,
                                                                                                        columnspan=3)
    Label(frame, text=f"nationalite : {contributeur[4]}", font=("Arial", 10), padx=10, pady=10).grid(row=5, column=0,
                                                                                                     columnspan=3)

    query = f"SELECT code_classification, titre FROM Ressource R INNER JOIN Film F ON F.code = R.code INNER JOIN Realisateur ON Realisateur.film = F.code INNER JOIN  Contributeur C ON C.id = Realisateur.contrib WHERE Realisateur.contrib = '{contributeur[0]}';"
    cursor.execute(query)
    films = cursor.fetchall()
    print(films)

    Label(frame, text=f"Réalisateur de :", font=("Arial", 10), padx=10, pady=10).grid(row=6, column=0)
    tree = ttk.Treeview(frame, columns=("c1", "c2"), show='headings', height=len(films))
    tree.column("# 1", anchor=CENTER)
    tree.heading("# 1", text="Code classification")
    tree.column("# 2", anchor=CENTER)
    tree.heading("# 2", text="Titre")

    for i in range(len(films)):
        tree.insert('', 'end', text="1", values=(films[i][0], films[i][1]))
    tree.grid(row=7, column=0)

    query = f"SELECT code_classification, titre FROM Ressource R INNER JOIN Film F ON F.code = R.code INNER JOIN Acteur ON Acteur.film = F.code INNER JOIN  Contributeur C ON C.id = Acteur.contrib WHERE Acteur.contrib = '{contributeur[0]}';"
    cursor.execute(query)
    films = cursor.fetchall()
    print(films)

    Label(frame, text=f"Acteur de :", font=("Arial", 10), padx=10, pady=10).grid(row=6, column=2)
    tree = ttk.Treeview(frame, columns=("c1", "c2"), show='headings', height=len(films))
    tree.column("# 1", anchor=CENTER)
    tree.heading("# 1", text="Code classification")
    tree.column("# 2", anchor=CENTER)
    tree.heading("# 2", text="Titre")

    for i in range(len(films)):
        tree.insert('', 'end', text="1", values=(films[i][0], films[i][1]))
    tree.grid(row=7, column=2)

    query = f"SELECT code_classification, titre FROM Ressource R INNER JOIN Musique M ON M.code = R.code INNER JOIN Compositeur ON Compositeur.musique = M.code INNER JOIN  Contributeur C ON C.id = Compositeur.contrib WHERE Compositeur.contrib = '{contributeur[0]}';"
    cursor.execute(query)
    musiques1 = cursor.fetchall()
    print(musiques1)

    Label(frame, text=f"Compositeur de :", font=("Arial", 10), padx=10, pady=10).grid(row=6, column=4)
    tree = ttk.Treeview(frame, columns=("c1", "c2"), show='headings', height=len(musiques1))
    tree.column("# 1", anchor=CENTER)
    tree.heading("# 1", text="Code classification")
    tree.column("# 2", anchor=CENTER)
    tree.heading("# 2", text="Titre")

    for i in range(len(musiques1)):
        tree.insert('', 'end', text="1", values=(musiques1[i][0], musiques1[i][1]))
    tree.grid(row=7, column=4)

    query = f"SELECT code_classification, titre FROM Ressource R INNER JOIN Musique M ON M.code = R.code INNER JOIN Interprete I ON I.musique = M.code INNER JOIN  Contributeur C ON C.id = I.contrib WHERE I.contrib = '{contributeur[0]}';"
    cursor.execute(query)
    musiques = cursor.fetchall()
    print(musiques)

    Label(frame, text=f"Interprete de :", font=("Arial", 10), padx=10, pady=10).grid(row=6+2+len(musiques1), column=0)
    tree = ttk.Treeview(frame, columns=("c1", "c2"), show='headings', height=len(musiques))
    tree.column("# 1", anchor=CENTER)
    tree.heading("# 1", text="Code classification")
    tree.column("# 2", anchor=CENTER)
    tree.heading("# 2", text="Titre")

    for i in range(len(musiques)):
        tree.insert('', 'end', text="1", values=(musiques[i][0], musiques[i][1]))
    tree.grid(row=6+3+len(musiques1), column=0)

    query = f"SELECT code_classification, titre FROM Ressource R INNER JOIN Livre L ON L.code = R.code INNER JOIN Auteur A ON A.livre = L.code INNER JOIN  Contributeur C ON C.id = A.contrib WHERE A.contrib = '{contributeur[0]}';"
    cursor.execute(query)
    livres = cursor.fetchall()
    print(livres)

    Label(frame, text=f"Auteur de :", font=("Arial", 10), padx=10, pady=10).grid(row=6+2+len(musiques), column=2)
    tree = ttk.Treeview(frame, columns=("c1", "c2"), show='headings', height=len(livres))
    tree.column("# 1", anchor=CENTER)
    tree.heading("# 1", text="Code classification")
    tree.column("# 2", anchor=CENTER)
    tree.heading("# 2", text="Titre")

    for i in range(len(livres)):
        tree.insert('', 'end', text="1", values=(livres[i][0], livres[i][1]))
    tree.grid(row=6+3+len(musiques), column=2)

    print(frame.winfo_children())
    Button(frame, text="<", command=lambda: espaceContributeurs(win, conn, frame, profil), padx=20).grid(
        row=0, column=0)


def main():
    try:
        connection = db_connection()
        landingFrame(window(), connection)

        # Close connection
        connection.close()
    except Exception:
        print("Erreur de connection à la BDD... Etes-vous connectez au réseau de l'UTC ?")


if __name__ == '__main__':
    main()
