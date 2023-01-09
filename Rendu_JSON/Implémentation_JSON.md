# Implémentation JSON
## I. Réflexion sur l'intégration d'attributs de type JSON

Dans cette étape de notre conception d'une base de données, nous allons nous intéresser à l'implémentation d'attributs de type JSON dans nos tables déjà conçues. Pour ce faire, regardons de plus près notre diagramme UML : 

![](https://gitlab.utc.fr/pillisju/projet-nf18-td1_g2-bibliotheque/-/raw/main/img/Integration_JSON.png)

Nous observons 3 associations (zones rouge, bleue et verte) dans que nous pouvons modifier à l'aide du type JSON. 

En zone verte , la relation <b>EXAMPLAIRE</b> peut se transformer en attribut JSON au sein de la relation <b>RESSOURCE</b> car il s'agit d'une composition.
Cependant, nous devons faire attention à bien conserver l'attribut <b>id</b> d'exemplaire, car nécessaire pour son association avec la classe <b>ADHERENT</b> (classe d'association <b>PRET</b>).
Par contrainte de la cardinalité <b>1..n</b>, nous devons ajouter la contrainte <b>NOT NULL</b> à ce nouvel attribut.

:warning: 
Cependant, cette implémentation est pour le moment difficilement envisageable. En effet, n'ayant pas vu cela dans le cours, nous ne savons pas comment récupérer l'id de l'example, qui est un sous-attribut d'un attribut json

Dans la suite de cette partie, nous avons supposé qu'il est possible de récupérer cet id.


En zone rouge, la relation <b>SANCTION</b> peut se transformer en attribut JSON au sein de la relation <b>ADHERENT</b> grâce aux cardinalités de l'association (équivalent à une composition). 

Enfin, en zone bleue, la relation <b>COMPTE</b> peut se transformer en attribut JSON au sein de la relation <b>UTILISATEUR</b> car il s'agit d'une nouvelle fois d'une composition.
Par contrainte de la cardinalité <b>1</b>, nous devons ajouter la contrainte <b>NOT NULL</b> à ce nouvel attribut.

## II. Implémentation de ces attributs dans les tables concernées (SQL)

``` sql
CREATE TABLE Ressource(
    code INTEGER PRIMARY KEY,
    titre VARCHAR NOT NULL,
    date_apparition DATE,
    code_classification INTEGER NOT NULL,
    editeur VARCHAR,
    genre VARCHAR,
    exemplaires JSON NOT NULL
);


CREATE TABLE Utilisateur(
    id SERIAL PRIMARY KEY ,
    nom VARCHAR NOT NULL,
    prenom VARCHAR NOT NULL,
    num_adresse INTEGER,
    rue VARCHAR,
    code_postal INTEGER,
    ville VARCHAR,
    mail VARCHAR,
    compte JSON NOT NULL
);



CREATE TABLE Adherent(
    id INTEGER REFERENCES Utilisateur(id),
    date_naissance DATE,
    num_tel INTEGER,
    statut_adhesion Adhesion NOT NULL,
    sanctions JSON,
    PRIMARY KEY(id)
);


CREATE TABLE Pret(
    id_pret SERIAL PRIMARY KEY ,
    adherent INTEGER REFERENCES Adherent(id) NOT NULL,
    exemplaire INTEGER REFERENCES Ressource(exemplaire.id),
    code_ressource INTEGER REFERENCES Ressource(code),
    date_debut DATE NOT NULL,
    date_fin DATE ,
    rendu BOOLEAN NOT NULL,
    
    CHECK(date_fin>=date_debut)
);
```

:warning:  Dans la création de la table <b>PRET</b> nous supposons qu'exemplaire récupère l'id de l'exemplaire.
(c.f : Partie I)


 
## III. Exemples d'insertion sur ces nouvelles tables 
 
``` sql
INSERT INTO utilisateur(nom, prenom, num_adresse, rue, code_postal, ville, mail, compte) values(
    'Galleze',
    'Rayane',
    '21',
    'rue du dépôt',
    '60280',
    'Compiègne',
    'rgalleze@etu.utc.fr',
    '{"login":"rgalleze", "password":"2908$RGnf18tropbien"}'
);

INSERT INTO adherent values(
    3,
    '2000-02-02',
    0668234125,
    'blacklisté',
    '[
        {"motif":"perte","date_debut":"2022-11-03","date_fin":"2022-11-05"},
        {"motif":"perte","date_debut":"2022-11-11","date_fin":null}
    ]'
);

INSERT INTO Ressource VALUES(
    3,
    'The Lord of the Rings',
    '1954-07-29',
    1154,
    'Allen & Unwin',
    'Fantasy',
    '[
        {"id":"1","etat":"abîmé"},
        {"id":"2","etat":"bon"},
        {"id":"3","etat":"abîmé"},
        {"id":"4","etat":"abîmé"}
    ]'
);

```

## IV. Exemples requêtes avec implémentation JSON

```sql
SELECT nom, prenom, num_adresse, rue, code_postal, ville, mail, c->>'login' AS login, c->>'password' AS password
FROM Utilisateur u, JSON_ARRAY_ELEMENTS(u.compte) c;

SELECT u.nom, u.prenom, a.statut_adhesion, s->>'motif' AS motif_sanction, CAST(s->>'date_debut' AS DATE) AS debut_sanction, CAST(s->>'date_fin' AS DATE) AS fin_sanction
FROM Adherent a NATURAL JOIN Utilisateur u, JSON_ARRAY_ELEMENTS(a.sanctions) s;

SELECT code, titre, editeur, CAST(e->>'id' AS INTEGER) AS id_exemplaire, e->>'etat' AS etat
FROM Ressource r, JSON_ARRAY_ELEMENTS(r.exmplaires) e;

```


