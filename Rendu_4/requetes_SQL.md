# Répertoire SQL

## Voici un répertoire des requêtes SQL utilisées dans notre première application Python

Vous trouverez ici, les principales requêtes SQL utilisées pour notre application Python. Pour des raisons de redondances, nous en avons omises quelques unes (ex : insertion d'un livre est identique à celle d'un film, à des attributs près).

Bien évidemment, il s'agit d'une première version de l'application comme demandé. Nous n'avons pas encore pu intégrer toutes les requêtes nécessaires.

### Requête de connexion
On vérifie bien que la personne se connecte bien en tant qu'adhérent | personnel
~~~sql
query = f"SELECT Compte.id FROM Compte 
INNER JOIN {'adherent' if status == 'Adhérents' else 'personnel'} 
on Compte.id = {'adherent' if status == 'Adhérents' else 'personnel'}.id 
WHERE login = '{username}' AND password = '{password}';"  
~~~
Dans le cas ou le select retourne rien cela signifie que les identifianst ne sont pas présents sur notre BDD (Login et/ou mot de passe)


### Requêtes espace adhérent
Voici des exemples de requêtes pour avoir des informations sur une ressource : 
*NB: Les requêtes étant similaires pour les 3 types de ressources, nous avons listé que les requêtes concernant les films (voir code source pour le reste)* 
~~~sql
/* Récupération de la liste des films */
query = "SELECT code,
                code_classification,
                titre, date_apparition, genre, langue, longueur 
                FROM Ressource NATURAL JOIN Film F ;"
~~~
~~~sql
/* Récupération des détails d'un film donné */
query = f"SELECT F.code, 
                titre, date_apparition, code_classification, editeur, genre,
                synopsis, langue, longueur 
                FROM Ressource 
                INNER JOIN Film F 
                ON F.code = Ressource.code WHERE F.code = '{film}';"
~~~
~~~sql
/* Récupération du nombre d'exemplaire d'un film donné */
query = f"SELECT COUNT(*) FROM Exemplaire E 
                 WHERE E.code_ressource = {film[0]};"
cursor.execute(query)
total = cursor.fetchone()[0]
~~~
~~~sql
/* Récupération du nombre d'exemplaire actuellement en prêt d'un film donné */
query = f"SELECT COUNT(*) FROM Pret P 
                 WHERE P.code_ressource = {film[0]} AND rendu = false ;"
cursor.execute(query)
non_dispo = cursor.fetchone()[0]
~~~
~~~sql
/* Récupération des noms et prénoms des réalisateurs d'un film donné */
query = f"SELECT nom, prenom FROM Realisateur 
                 INNER JOIN Film F ON F.code = Realisateur.film 
                 INNER JOIN Contributeur C ON C.id = Realisateur.contrib 
                 WHERE F.code = '{film[0]}';"
~~~
~~~sql
/* Récupération des noms et prénoms des acteurs d'un film donné.*/
query = f"SELECT nom, prenom FROM Acteur 
                 INNER JOIN Film F ON F.code = Acteur.film 
                 INNER JOIN Contributeur C ON C.id = Acteur.contrib 
                 WHERE F.code = '{film[0]}';"
~~~

~~~sql
/* Récupération de la liste de contributeur avec choix(ordonnée/non_ordonnée) */
/* supp = f"ORDER BY {order}" */
/* Tri effectué lors du clique sur le nom de la colonne (uniquement fonctionnel pour les films car pas encore implémenté ailleurs)*/
query = f"SELECT id, nom, prenom, date_naissance, nationalite 
                 FROM Contributeur {supp if order != 'None' else '' };"
cursor.execute(query)
~~~

~~~sql
/* Récupération des informations d'un contributeur donné */
query = f"SELECT id, nom, prenom, date_naissance, nationalite 
                 FROM Contributeur 
                 WHERE Contributeur.id = {contributeur};"
~~~

### Requêtes espace personnel 

Les requêtes statistiques se trouvent en *bas de page*.

#### Requêtes générales (SELECT, INSERT, UPDATE)
~~~sql
/*Récupération adhérents avec adhésion active pour afficher ceux pouvant effectuer un prêt*/
query = "SELECT id, nom, prenom,mail,date_naissance,num_tel FROM Adherent 
         NATURAL JOIN Utilisateur 
         WHERE statut_adhesion = 'active';"
~~~

~~~sql
/*Récupération des exemplairs disponibles à l'emprunt (ils doivent être non perdus et rendus)*/
query = "SELECT E.id,code,titre,code_classification FROM Exemplaire E 
         LEFT JOIN 
         (SELECT exemplaire,code_ressource FROM Pret P WHERE rendu ='false') AS D 
         ON D.exemplaire = E.id AND D.code_ressource = E.code_ressource 
         INNER JOIN Ressource R on E.code_ressource = R.code 
         WHERE etat <> 'perdu' AND D.exemplaire IS NULL AND D.code_ressource IS NULL;"

~~~

~~~python
# Autorisation d'un emprunt et enregistrement de celui-ci
# Si adhesion de l'adhérent est active ,exemplaire disponible et son état non perdu, on autorise l'emprunt
Pour plus de clarté voici une partie du code Python :
 try:
        
        query = 'SELECT * FROM Pret;'
        print(query)
        cursor.execute(query)
        print(cursor.fetchall())
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
~~~

~~~sql
/*Affichage des ressources*/
query = "SELECT Ressource.code,titre,date_apparition,code_classification,editeur,genre FROM RESSOURCE;"

~~~

~~~sql
/*Ajout d'un exemplaire en fonction des données saisies par l'utilisateur*/
query = f"INSERT INTO Exemplaire(code_ressource,etat) 
          VALUES ({int(values[0])},'{values[1]}');"

~~~

~~~sql
/*Affichage des sanctions non résolues/en cours */
query = "SELECT idadherent, nom,prenom,statut_adhesion, motif, date_debut AS nombre_sanctions FROM Sanction S 
         INNER JOIN Adherent A ON S.idadherent = A.id 
         NATURAL JOIN Utilisateur 
         WHERE date_fin IS NULL;"

~~~

~~~sql
/*Mise à jour d'une sanction en fonction des données saisies par l'utilisateur*/
query = f"UPDATE Sanction SET date_fin = DATE('{values[1]}') 
          WHERE idSanction={int(values[0])}; "
~~~

~~~sql
/*Récupération des informations d'un adhérent*/
query = "SELECT id, nom, prenom, num_adresse,rue,code_postal,ville,mail,date_naissance,num_tel,statut_adhesion FROM Adherent 
         NATURAL JOIN Utilisateur ;"

~~~

~~~python
# Insertion d'un adhérent
Pour plus de clarté, voici le code Python :
    try:
        query = f"INSERT INTO Utilisateur(nom, prenom, num_adresse, rue, code_postal, ville, mail) VALUES ('{values[0]}','{values[1]}', {int(values[2])},'{values[3]}',{int(values[4])},'{values[5]}','{values[6]}');"
        cursor.execute(query)
    except Exception as er:
        print(er)
        error = True
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
~~~

~~~sql
/*Ajout d'une sanction relative à un adhérent (la date de fin est mise à null, elle pourra être modifiée plus tard avec grâce à l'interface*/
query = f"INSERT INTO Sanction(idadherent,motif,date_debut,date_fin) 
          VALUES ({int(values[0])},'{values[1]}',DATE('{values[2]}'),NULL);"
~~~

~~~python
# Insertion d'un film, le fonctionnement est quasiment identique pour insérer un livre ou une musique (c.f : code source)
Pour plus de clarté, voici le code Python :
    try:
        query = f"INSERT INTO Ressource VALUES ({int(values[0])},'{values[1]}',DATE('{values[2]}'),{int(values[3])},'{values[4]}','{values[5]}');"
        cursor.execute(query)
    except Exception:
        error = True
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
~~~

~~~sql
/*Affichage des sanctions*/
query = f"SELECT motif,date_debut,date_fin FROM Sanction 
          WHERE idAdherent = {profil[0]};"
~~~

~~~sql
~~~
#### Requêtes statistiques (GROUP BY, AVG, COUNT...) 


~~~sql
/*Durée moyenne d'un emprunt*/
query = "SELECT AVG(date_fin - date_debut) AS duree_moyenne FROM Pret;"
~~~
~~~sql
/*Nombre d'emprunts en cours */
 query = "SELECT COUNT(*) FROM Pret 
          WHERE NOT rendu;"
~~~
~~~sql
/*Ressource la plus empruntée*/
query = "SELECT idadherent, prenom, nom, statut_adhesion, COUNT(idadherent) AS nombre_sanctions FROM Sanction S 
         INNER JOIN Adherent A ON S.idadherent = A.id 
         NATURAL JOIN Utilisateur 
         GROUP BY idadherent, statut_adhesion, prenom, nom 
         ORDER BY nombre_sanctions 
         DESC LIMIT 1;"
~~~
~~~sql
/*Adhérent le plus sanctionné*/
query = "SELECT titre, code_classification, COUNT(code_ressource) AS nb_emprunts FROM Ressource R 
         INNER JOIN Pret P on R.code = P.code_ressource
         GROUP BY code_ressource, titre, code_classification 
         ORDER BY nb_emprunts 
         DESC LIMIT 1;"
~~~
~~~sql
/*Classement des motifs de sanctions les plus récurrents*/
query = "SELECT motif, COUNT(motif) AS nombre FROM Sanction 
         GROUP BY motif 
         ORDER BY nombre 
         DESC;"
~~~
~~~sql
/*Liste des prêts dont le rendu est en retard*/
query = "SELECT id_pret, adherent, code_ressource, exemplaire, NOW() - date_fin AS retard FROM Pret 
         WHERE date_fin < NOW() AND NOT rendu;"
~~~
