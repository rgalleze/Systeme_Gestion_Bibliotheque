![status_3](https://img.shields.io/badge/Rendu%203-in%20progress-orange)

# SQL Partie 1 : Création & insertion 

Pour l'utilisation de clé artificielle, nous utiliserons le type SERIAL, qui, en POSTGRESQL, est un entier auto-incrémenté lors de l'insertion d'une donnée dans la table.

### CREATION 
~~~sql
CREATE TABLE Ressource(
    code INTEGER PRIMARY KEY,
    titre VARCHAR NOT NULL,
    date_apparition DATE,
    code_classification INTEGER NOT NULL,
    editeur VARCHAR,
    genre VARCHAR
);

CREATE TABLE Film(
    code INTEGER REFERENCES Ressource(code),
    synopsis VARCHAR NOT NULL,
    langue VARCHAR NOT NULL,
    longueur INTEGER NOT NULL,
    PRIMARY KEY (code)
);

CREATE TABLE Musique(
    code INTEGER REFERENCES Ressource(code),
    longueur INTEGER NOT NULL,
    PRIMARY KEY (code)
);

CREATE TABLE Livre(
    code INTEGER REFERENCES Ressource(code),
    ISBN VARCHAR(17) UNIQUE NOT NULL,
    resume VARCHAR NOT NULL,
    langue VARCHAR NOT NULL,
    PRIMARY KEY (code)
);


CREATE TABLE Contributeur(
    id SERIAL PRIMARY KEY ,
    nom VARCHAR NOT NULL,
    prenom VARCHAR NOT NULL,
    date_naissance DATE NOT NULL,
    nationalite VARCHAR NOT NULL
);

CREATE TABLE Acteur(
    film INTEGER REFERENCES Film(code) NOT NULL,
    contrib INTEGER REFERENCES Contributeur(id)NOT NULL,
    PRIMARY KEY(film,contrib)
);


CREATE TABLE Realisateur(
    film INTEGER REFERENCES Film(code) NOT NULL,
    contrib INTEGER REFERENCES Contributeur(id)NOT NULL,
    PRIMARY KEY(film,contrib)
);

CREATE TABLE Auteur(
    livre INTEGER REFERENCES Livre(code) NOT NULL,
    contrib INTEGER REFERENCES Contributeur(id)NOT NULL,
    PRIMARY KEY(livre,contrib)
);

CREATE TABLE Compositeur(
    musique INTEGER REFERENCES Musique(code) NOT NULL,
    contrib INTEGER REFERENCES Contributeur(id)NOT NULL,
    PRIMARY KEY(musique,contrib)
);

CREATE TABLE Interprete(
    musique INTEGER REFERENCES Musique(code) NOT NULL,
    contrib INTEGER REFERENCES Contributeur(id)NOT NULL,
    PRIMARY KEY(musique,contrib)
);

CREATE TYPE etat AS ENUM ('neuf', 'bon', 'abîmé','perdu');

CREATE TABLE Exemplaire(
    id SERIAL,
    code_ressource INTEGER REFERENCES Ressource(code),
    etat etat NOT NULL,
    PRIMARY KEY(id,code_ressource)
);

CREATE TABLE Utilisateur(
    id SERIAL PRIMARY KEY ,
    nom VARCHAR NOT NULL,
    prenom VARCHAR NOT NULL,
    num_adresse INTEGER,
    rue VARCHAR,
    code_postal INTEGER,
    ville VARCHAR,
    mail VARCHAR
);

CREATE TABLE Personnel(
    id INTEGER REFERENCES Utilisateur(id),
    PRIMARY KEY(id)
);

CREATE TABLE Compte(
    id INTEGER REFERENCES Utilisateur(id),
    login VARCHAR UNIQUE NOT NULL,
    password VARCHAR NOT NULL,
    PRIMARY KEY(id)
);

CREATE TYPE Adhesion AS ENUM ('active', 'expirée', 'suspendue','blacklistée');

CREATE TABLE Adherent(
    id INTEGER REFERENCES Utilisateur(id),
    date_naissance DATE,
    num_tel INTEGER,
    statut_adhesion Adhesion NOT NULL,
    PRIMARY KEY(id)
);

CREATE TYPE Motif AS ENUM ('retard', 'deterioration', 'perte');

CREATE TABLE Pret(
    id_pret SERIAL PRIMARY KEY ,
    adherent INTEGER REFERENCES Adherent(id) NOT NULL,
    exemplaire INTEGER,
    code_ressource INTEGER,
    date_debut DATE NOT NULL,
    date_fin DATE ,
    rendu BOOLEAN NOT NULL,
    FOREIGN KEY (exemplaire, code_ressource) REFERENCES Exemplaire(id,code_ressource),
    CHECK(date_fin>=date_debut)
);

CREATE TABLE Sanction(
    idSanction SERIAL PRIMARY KEY,
    idAdherent INTEGER REFERENCES Adherent(id) NOT NULL,
    motif Motif NOT NULL,
    date_debut DATE NOT NULL,
    date_fin DATE,
    CHECK(date_fin>=date_debut)
);
~~~

### INSERTIONS
~~~sql


INSERT INTO Ressource VALUES(1,'Star Wars IV','1977-10-19',1019,'Lucasfilm','Science-fiction');
INSERT INTO Film VALUES(1,'Dans une galaxie lointaine, très lointaine...','Français',121);
INSERT INTO Contributeur(nom,prenom,date_naissance,nationalite) VALUES('Lucas', 'George','1944-05-14','Américaine');
INSERT INTO Realisateur VALUES(1,1);
INSERT INTO Contributeur(nom,prenom,date_naissance,nationalite)  VALUES('Hamill', 'Mark','1951-09-25','Américaine');
INSERT INTO Acteur VALUES(1,2);

INSERT INTO Ressource VALUES(2,'Thriller','1982-11-30',2046,'Epic Records','Pop');
INSERT INTO Musique VALUES(2,42);
INSERT INTO Contributeur(nom,prenom,date_naissance,nationalite)  VALUES('Jackson', 'Michael','1958-08-29','Américaine');
INSERT INTO Compositeur VALUES(2,3);
INSERT INTO Interprete VALUES(2,3);


INSERT INTO Ressource VALUES(3,'The Lord of the Rings','1954-07-29',1154,'Allen & Unwin','Fantasy');
INSERT INTO Livre VALUES(3,9780048230461, 'A fellowship gathers itself over a mysterious ring.','English');
INSERT INTO Contributeur(nom,prenom,date_naissance,nationalite)  VALUES('Tolkien', 'J. R. R.','1892-01-03','Britannique');
INSERT INTO Auteur VALUES(3,4);

INSERT INTO utilisateur(nom, prenom, num_adresse, rue, code_postal, ville, mail) values('Galleze', 'Rayane', '21', 'rue du dépôt', '60280', 'Compiègne', 'rgalleze@etu.utc.fr');
INSERT INTO utilisateur(nom, prenom, num_adresse, rue, code_postal, ville, mail) values('Pillis', 'Julien', '21', 'rue du dépôt', '60280', 'Compiègne', 'julien.pillis@etu.utc.fr');
INSERT INTO utilisateur(nom, prenom, num_adresse, rue, code_postal, ville, mail) values('Vivat', 'Benjamin', '99', 'rue Victor Hugo ', '60200', 'Compiègne', 'benjamin.vivat@etu.utc.fr');
INSERT INTO utilisateur(nom, prenom, num_adresse, rue, code_postal, ville, mail) values('Labouré', 'Alexandre', '69', 'rue Générale de G ', '95300', 'Pontoise', 'alexandre.laboure@etu.utc.fr');

INSERT INTO personnel values(1);
INSERT INTO personnel values(2);

INSERT INTO adherent values(3, '2000-02-02', 0668234125, 'blacklistée');
INSERT INTO adherent values(4, '2005-02-02', 0669991252, 'suspendue');

INSERT INTO compte values(1, 'rgalleze', '2908$RGnf18tropbien');
INSERT INTO compte values(2, 'pllisju', 'MDxo9g2jzFTvri');
INSERT INTO compte values(3, 'bvivat', 'UpRUsWNoL7wYHZ');
INSERT INTO compte values(4, 'alaboure', 'EYzgJj5Gdcs5TZ');

INSERT INTO EXEMPLAIRE(code_ressource,etat) VALUES (1,'neuf');
INSERT INTO EXEMPLAIRE(code_ressource,etat) VALUES (2,'bon');
INSERT INTO EXEMPLAIRE(code_ressource,etat) VALUES (3,'abîmé');
INSERT INTO EXEMPLAIRE(code_ressource,etat) VALUES (3,'bon');
INSERT INTO EXEMPLAIRE(code_ressource,etat) VALUES (1,'bon');
INSERT INTO EXEMPLAIRE(code_ressource,etat) VALUES (1,'perdu');
INSERT INTO EXEMPLAIRE(code_ressource,etat) VALUES (3,'abîmé');
INSERT INTO EXEMPLAIRE(code_ressource,etat) VALUES (3,'abîmé');
INSERT INTO EXEMPLAIRE(code_ressource,etat) VALUES (2,'neuf');

INSERT INTO PRET(adherent,exemplaire,code_ressource,date_debut,date_fin,rendu) VALUES (3,1,1,DATE('2022-09-10'),DATE('2022-09-10'),true);
INSERT INTO PRET(adherent,exemplaire,code_ressource,date_debut,date_fin,rendu) VALUES (4,1,1,DATE('2022-09-12'),DATE('2022-09-13'),true);
INSERT INTO PRET(adherent,exemplaire,code_ressource,date_debut,date_fin,rendu) VALUES (4,5,1,DATE('2022-09-11'),DATE('2022-09-15'),true);
INSERT INTO PRET(adherent,exemplaire,code_ressource,date_debut,date_fin,rendu) VALUES (3,9,2,DATE('2022-10-24'),DATE('2022-11-19'),false);
INSERT INTO PRET(adherent,exemplaire,code_ressource,date_debut,date_fin,rendu) VALUES (3,3,3,DATE('2022-09-8'),DATE('2022-11-02'),false);
INSERT INTO PRET(adherent,exemplaire,code_ressource,date_debut,date_fin,rendu) VALUES (4,9,2,DATE('2022-11-20'),DATE('2022-11-23'),false);

INSERT INTO SANCTION(idadherent,motif,date_debut,date_fin) VALUES (4,'retard',DATE('2022-11-03'),null);
INSERT INTO SANCTION(idadherent,motif,date_debut,date_fin) VALUES (3,'perte',DATE('2022-11-03'),DATE('2022-11-05'));
INSERT INTO SANCTION(idadherent,motif,date_debut,date_fin) VALUES (3,'perte',DATE('2022-11-11'),null);
~~~
