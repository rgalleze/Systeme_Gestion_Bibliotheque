# Modèle Logique de Données
![status_2](https://img.shields.io/badge/Rendu%202-done-brightgreen)

<h2><center>Version 2</center></h2>

- Justifiez vos choix de transformation de l'héritage :heavy_check_mark: 
- Il vous manque les domaines des attributs :heavy_check_mark: 
- Pour Sanction, considérer la clé comme la référence vers Utilisateur n'est pas une bonne idée, et même une erreur. Il faut la clé et en plus une référence étrangère vers Adhérent (et non Utilisateur) :heavy_check_mark: 


## Tables
**Ressource**(#code: int, titre: string, date_apparition: date, code_classification: int, editeur: string, genre: string) avec titre, code_classification NOT NULL


- Classe mère abstraite, héritage exclusif : une ressource a un type unique (Film ou Musique ou Livre), héritage non complet (les classes filles ont des attributs propres à elles).
- Héritage par classe mère à éviter car il y aurait beaucoup de contraintes à cause des associations des classes filles. Dde plus, ce type d'héritage implique l'ajout de contraintes de vérification des types (par exemple, lorsqu'on instancie un film, on doit s'assurer que les attributs ISBN et résumé sont NULL).
- Héritage par classe filles à éviter car la classe mère possède une composition avec exemplaire et l'héritage est exclusif.
- => On opte ainsi pour un héritage par référence.

**Film**(#code=>Ressource.code: int, synopsis: string, langue: string, longueur: int) avec langue, synopsis, longueur NOT NULL

**Musique**(#code=>Ressource.code: int, longueur: int) avec longeur NOT NULL

**Livre**(#code=>Ressource.code, ISBN: int, resume: texte, langue: string) avec ISBN key et resume, langue NOT NULL

**Acteur**(#film=>Film.code: int, #contrib=><span>Contributeur.id</span>: int)

**Realisateur**(#film=>Film.code: int, #contrib=><span>Contributeur.id</span>: int)

**Auteur**(#livre=>Livre.code: int, #contrib=><span>Contributeur.id</span>: int)

**Compositeur**(#musique=>Musique.code: int, #contrib=><span>Contributeur.id</span>: int)

**Interprete**(#musique=>Musique.code: int, #contrib=><span>Contributeur.id</span>: int)

**Contributeur**(#id: int, nom: string, prenom: string, date_naissance: date, nationalite: string) avec * NOT NULL

**Exemplaire**(#id: int, #code_ressource=>Ressource.code: int, etat:{neuf, bon, abime, perdu}) avec etat NOT NULL

**Pret**(#id_pret: int, adherent=>Adherent<span>.id: int, code_ressource=>Exemplaire.code_ressource, exemplaire=>Exemplaire</span>.id: int, date_debut: date, date_fin: date, rendu: booleen) avec date_debut <= date_fin, all NOT NULL

**Sanction**(#idSanction: int, idAdherent=><span>Adherent.id</span>: int, motif: {retard, deterioration, perte}, date_debut: date, date_fin: date) avec date_debut <= date_fin, date_debut, motif NOT NULL


> "*Si une clé candidate (globale) permet d'identifier de façon unique une partie indépendamment du tout, on préférera la conserver comme clé candidate plutôt que de la prendre pour clé primaire.
> Si on la choisit comme clé primaire cela revient à avoir transformé la composition en agrégation, en redonnant une vie propre aux objets composants.*"
> D'après le cours [mod4](https://moodle.utc.fr/pluginfile.php/249144/mod_resource/content/1/co/mod4c21.html) sur la transformation des compositions en relationelle, il  est donc, ici, plus judicieux de choisir login en tant que key (unique not null) et non en tant que clé primaire



**Utilisateur**(#id: int, nom: string, prenom: string, num_adresse: int, rue: string, code_postal: int,  ville: string, mail: string) nom, prenom not null

- Classe mère abstraite, héritage non complet (les classes filles ont des attributs propres à elles).
- Héritage par classe mère à éviter car il y aurait beaucoup de contraintes à causes des associations des classes filles. De plus ce type d'héritage implique l'ajout de contraintes de vérification des types (par exemple, lorsqu'on instancie un utilisateur (personnel), on doit s'assurer que le statut d'adhésion est NULL).
- Héritage par classe filles à éviter car la classe mère possède une composition avec compte.
- => On opte ainsi pour un héritage par référence.

**Personnel**(#id=><span>Utilisateur.id</span>: int)

**Adherent**(#id=><span>Utilisateur.id</span>: int, date_naissance: date, num_tel: int, statut_adhesion: {active, expiree, suspendue, blacklistee}) statut_adhesion NOT NULL

**Compte**(#id=><span>Utilisateur.id</span>: int, login: string, password: string) login key, password not null
 
---

## Contraintes :

#### Héritage classe Ressource :

- INTERSECTION (PROJECTION(Film,code), PROJECTION(Musique,code), PROJECTION(Livre,code)) = NULL (Héritage exclusif classe Ressource )

- UNION (PROJECTION(Film,code), PROJECTION(Musique,code), PROJECTION(Livre,code)) = PROJECTION(Ressource,code) (classe Ressource abstraite)

#### Héritage classe Utilisateur :

- INTERSECTION (PROJECTION(Personnel,id), PROJECTION(Adherent,code)) = NULL (Héritage exclusif classe Utilisateur )

- UNION (PROJECTION(Personnel,id), PROJECTION(Adherent,id),  = PROJECTION(Utilisateur,id) (classe Utilisateur abstraite)


