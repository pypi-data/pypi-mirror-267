# sync2jira

# Faut avoir la version 3.10.12 de python 
## Importer le package
```
 pip install synch2jira
```

## Mettre à jour le package 
⚠️ A faire 2 fois !! 
```
 pip install --upgrade synch2jira
 pip install --upgrade synch2jira
 
```





## Remplir le fichier de config 
Pour remplir les différents paramétres du fichier de config
*   from synch2jira.config_package import config_package
*    config_package()

Un fichier config.py va etre crée

## Tester le package 
# Tester la connection à Jira : 
importez la classe IssueS2 :
* from synch2jira.Isssue_S2 import IssueS2
executez la fonction :
* IssueS2.try_jira_connection()
elle doit vous renvoyer True dans le cas contraire verifiez vos identifiants de conexion à Jira

# Recuper le nombre de ticket d'un projet 
Allez Dans le fichier de configuration remplacez la ligne jql_query comme suit : 
* jql_query = " projet = <cle_de_votre_projet>"
importez la classe IssueS2 :
* from synch2jira.Isssue_S2 import IssueS2
executez la fonction :
* IssueS2.all_key()
elle doit vous renvoyer une liste de clé  dans le cas contraire verifiez la connecxion à jira puis votre jql_query



## Creer et remplir la Base de Donnée : 
pour Creer et Remplir la base de Donnée vous devez :
- importer la classe IssueWokflow
* from synch2jira.Issue_workflow import IssueWokflow
- executer la fonction 
* IssueWokflow.fill_issue_workflow_bdd()

Cette fonction va vous creer une base de donnée et la remplir avec vos données Jira si elle vous renvoit une erreur assurez vous de creer un dossier database puis recommencez à nouveau 


## Liste de quelques fonctions Utiles :
# Dans la Classe synchronisation 

# Workflow :
- importer Workflow :
* from synch2jira.Issue_workflow import Wokflow 
- Obtenir le Lead time :
* Wokflow.get_all_wokflow_in_csv(state1, state2)
cette fonction vous creera un fichier csv contenant les données de votre lead time 
- obtenir le debit : 
* rate = Workflow.get_rate(date1,date2)
* print(rate)
cette fonction vous renvoit un entier representant le debit des ticket entre les deux dates 

## Développer les fonctions suivantes dans S1 :

* All() : Cette fonction retourne la liste de tous les enregistrements disponibles dans S1.

* first() : Retourne le premier élément de la liste des enregistrements.

* last() : Retourne le dernier élément de la liste des enregistrements.

* find_by() : Cette fonction permet de rechercher des enregistrements en fonction de certains critères spécifiés.

* find_by_id(id) : Retourne l'enregistrement correspondant à l'ID spécifié.

* update() : Met à jour un enregistrement existant dans la base de données.

* delete() : Supprime un enregistrement de la base de données.

* save() : Enregistre un nouvel enregistrement dans la base de données.

* get() : Cette fonction récupère des informations spécifiques sur un enregistrement donné.





