import json
import os
import config 
import pandas as pd
import matplotlib
import seaborn as sns

from synch2jira.issue_csv import IssueCSV
from synch2jira.issue_json import IssueJSON
matplotlib.use('Agg')

import matplotlib.pyplot as plt



def generate_issue_data_mining_csv(state1=config.workflow_status1,state2=config.workflow_status2):
    with open(config.json_issues_file, 'r') as file :
            json_data = json.load(file)
    issue_list = [IssueJSON.json_to_issue(issue_data,json_data,state1,state2) for issue_data in json_data]
    IssueCSV.generate_csv_data(issue_list,config.csv_issue_file)

def csv_to_dataframe(file_path):
    df = pd.read_csv(file_path)
    return df

def str_df_to_dt_df(dataframe,use_workflow=config.use_workflow):
    if use_workflow:
        dataframe['created'] = pd.to_datetime(dataframe['workflow_start_time'],utc=True)
        dataframe['resolutiondate'] = pd.to_datetime(dataframe['workflow_end_time'],utc=True)
        dataframe = dataframe.dropna(subset=['workflow_start_time','workflow_end_time'])
        return dataframe
    dataframe['created'] = pd.to_datetime(dataframe['created'],utc=True)
    dataframe['resolutiondate'] = pd.to_datetime(dataframe['resolutiondate'],utc=True)
    dataframe = dataframe.dropna(subset=['resolutiondate','created'])
    return dataframe

def genarate_creation_resolution_figure(dataframe):
    
    dataframe = str_df_to_dt_df(dataframe)
    # Trier les données par date de création
    dataframe.sort_values(by='created', inplace=True)
    print(dataframe)
    plt.figure(figsize=(12, 6))
    plt.scatter(dataframe.index, dataframe['created'], label='Date de création', color='blue')
    plt.scatter(dataframe.index, dataframe['resolutiondate'], label='Date de résolution', color='green')
    plt.xlabel('ticket')
    plt.ylabel('dates creation_resolution')
    plt.title('Tendances creation_resolution des tickets ')
    plt.xticks(rotation=45)  
    plt.legend()
    plt.tight_layout()  
    plt.savefig(config.image_directory + 'creation_resolution_by_issue_type.png')
    plt.show()

def genarate_creation_resolution_figure_by_issue_type(dataframe):
    dataframe = str_df_to_dt_df(dataframe)
    
    dataframe.sort_values(by='created', inplace=True)
    
    types_issues = dataframe['issuetypename'].unique()
    
    fig, axes = plt.subplots(nrows=len(types_issues), ncols=1, figsize=(12, 6*len(types_issues)))
    
    for i, issue_type in enumerate(types_issues):
        data_filtered = dataframe[dataframe['issuetypename'] == issue_type]
        
        axes[i].scatter(data_filtered.index, data_filtered['created'], label='Date de création', color='blue')
        
        axes[i].scatter(data_filtered.index, data_filtered['resolutiondate'], label='Date de résolution', color='green')
        
        axes[i].set_xlabel('ticket')
        axes[i].set_ylabel('dates creation_resolution')
        axes[i].set_title(f'Tendances creation_resolution des tickets ({issue_type})')
        axes[i].legend()
        axes[i].tick_params(axis='x', rotation=45)
        
    plt.tight_layout()  
    plt.savefig(config.image_directory + 'creation_resolution_by_issue_type.png')
    plt.show()

def genarate_creation_resolution_figure_by_issue_field(dataframe,field):
    dataframe = str_df_to_dt_df(dataframe)
    
    dataframe.sort_values(by='created', inplace=True)
    
    types_issues = dataframe[field].unique()
    
    fig, axes = plt.subplots(nrows=len(types_issues), ncols=1, figsize=(12, 6*len(types_issues)))
    
    for i, issue_type in enumerate(types_issues):
        data_filtered = dataframe[dataframe[field] == issue_type]
        
        axes[i].scatter(data_filtered.index, data_filtered['created'], label='Date de création', color='blue')
        
        axes[i].scatter(data_filtered.index, data_filtered['resolutiondate'], label='Date de résolution', color='green')
        
        axes[i].set_xlabel('ticket')
        axes[i].set_ylabel('dates creation_resolution')
        axes[i].set_title(f'Tendances creation_resolution des tickets ({issue_type})')
        axes[i].legend()
        axes[i].tick_params(axis='x', rotation=45)
        
    plt.tight_layout()  
    plt.savefig(config.image_directory + f'/creation_resolution_by_issue_{field}.png')
    plt.show()


def get_creation_resolution_time_statistics(dataframe):
    dataframe = str_df_to_dt_df(dataframe)
    dataframe['creation_resolution_time'] = dataframe.apply(lambda row: row['resolutiondate'] - row['created'], axis=1)
    average_resolution_time = dataframe['creation_resolution_time'].mean()
    print("Différence de temps moyenne entre création et résolution : ", average_resolution_time)
    print("difference max de temps de resolution",dataframe['creation_resolution_time'].max(),dataframe['creation_resolution_time'].min())
    print(dataframe['creation_resolution_time'].describe())
    return dataframe['creation_resolution_time'].describe()
 
def get_month_statistics(dataframe ):
    dataframe = str_df_to_dt_df(dataframe)
    dataframe['created_month'] = dataframe['created'].dt.month
    dataframe['resolution_time'] = dataframe['resolutiondate'] - dataframe['created'] #
    dataframe = dataframe[['created_month','resolution_time']]
    # statistiques groupées par mois
    statistics_by_month = dataframe.groupby('created_month')['resolution_time'].describe()
    return statistics_by_month



def get_period_statistics(dataframe, period):
    dataframe = str_df_to_dt_df(dataframe)
    
    if period == 'week':
        dataframe['period'] = dataframe['created'].dt.isocalendar().week
    elif period == 'month':
        dataframe['period'] = dataframe['created'].dt.month
    elif period == 'year':
        dataframe['period'] = dataframe['created'].dt.year
    else:
        raise ValueError("Période non valide. Veuillez spécifier 'day', 'month' ou 'year'.")
    
    dataframe['resolution_time'] = dataframe['resolutiondate'] - dataframe['created']
    
    
    dataframe = dataframe[['period', 'resolution_time']]
    
    statistics_by_period = dataframe.groupby('period')['resolution_time'].describe()
    
    return statistics_by_period


def get_statistics_by_issue_type(dataframe):
    dataframe = str_df_to_dt_df(dataframe)
    dataframe['resolution_time'] = dataframe['resolutiondate'] - dataframe['created']
    statistics_by_issue_type = dataframe.groupby('issuetypename')['resolution_time'].describe()

    return statistics_by_issue_type

def get_statistics_by_field(dataframe,field):
    dataframe = str_df_to_dt_df(dataframe)
    dataframe['resolution_time'] = dataframe['resolutiondate'] - dataframe['created']
    statistics_by_issue_field = dataframe.groupby(field)['resolution_time'].describe()

    return statistics_by_issue_field

def get_double_group_by_statistics(dataframe,period):
    dataframe = str_df_to_dt_df(dataframe)
    dataframe['resolution_time'] = dataframe['resolutiondate'] - dataframe['created']
    if period == 'week':
        dataframe['period'] = dataframe['created'].dt.isocalendar().week
    elif period == 'month':
        dataframe['period'] = dataframe['created'].dt.month
    elif period == 'year':
        dataframe['period'] = dataframe['created'].dt.year
    else:
        raise ValueError("Période non valide. Veuillez spécifier 'day', 'month' ou 'year'.")
    
    statistics = dataframe.groupby(['period',"issuetypename"])['resolution_time'].describe()
    for line in statistics :
        print(line)
        print(statistics[line])
    return statistics

def get_number_issues_solved_within_preriod_graph(dataframe,period):
    dataframe = str_df_to_dt_df(dataframe)
    #dataframe['resolution_time'] = dataframe['resolutiondate'] - dataframe['created']
    dataframe['resolution_time_days'] = (dataframe['resolutiondate'] - dataframe['created']).dt.days
    print(dataframe['resolution_time_days'].describe())
    # 3. Identify and visualize the proportion of issues resolved within 30 days
    dataframe['resolved_within'] = dataframe['resolution_time_days'] <= period

    resolution_proportion = dataframe['resolved_within'].value_counts(normalize=True) * 100
    print(dataframe['resolved_within'].describe())
    plt.figure(figsize=(6, 6))
    resolution_proportion.plot(kind='pie', autopct='%1.1f%%', startangle=140, labels=[f'en plus de  {period} jour', f'en moins de  {period} jour'], colors=['lightgreen', 'lightcoral'])
    plt.ylabel('')
    plt.title(f'Proportion des tickets resolu en  {period} jour')
    plt.tight_layout()
    plt.savefig(config.image_directory +f'issues_resolved_within_{period}_days.png')
    plt.show()

def plot_issue_types_distribution(df):
    issue_counts = df['issuetypename'].value_counts()
    issue_counts.plot(kind='bar')
    plt.title('Répartition des Types d\'Issues')
    plt.xlabel('Type d\'Issue')
    plt.ylabel('Nombre d\'Issues')
    plt.xticks(rotation=12)
    plt.savefig('images/issue_types_distribution')
    plt.show()


def analyze_time_spent_on_issues(df):
    df['timespend_hours'] = df['timespend'] / 3600 # Convertir le temps passé en heures
    print(df['timespend_hours'].describe())
    average_time = df.groupby('issuetypename')['timespend_hours'].mean()
    average_time.plot(kind='bar')
    plt.title('Temps Moyen Passé par Type d\'Issue')
    plt.xlabel('Type d\'Issue')
    plt.ylabel('Temps Moyen (Heures)')
    plt.xticks(rotation=45)
    plt.savefig('images/time_spent_on_issues')
    plt.show()

def a(df):
    df = str_df_to_dt_df(df)
    df['resolution_time'] = df['resolutiondate'] - df['created']

    resolution_time_stats = df['resolution_time'].describe()
    a = df['resolution_time'].dt.days
    print(a.describe())
    plt.figure(figsize=(12, 6))
    sns.histplot(df['resolution_time'].dt.days, kde=False, color="blue")
    plt.title('Distribution des Temps de resolution')
    plt.xlabel('Temps de resolution(Jour)')
    plt.ylabel('Frequence')
    plt.tight_layout()
    plt.savefig('images/resolution_time_distribution')
    plt.show()
    return resolution_time_stats

def tickets_clotures_en_mois(dataframe, annee, mois):
    dataframe = str_df_to_dt_df(dataframe)
    
    # Filtrer les données pour le mois et l'année spécifiés
    dataframe_mois_annee = dataframe[(dataframe['resolutiondate'].dt.year == annee) & (dataframe['resolutiondate'].dt.month == mois)]
    
    # Calculer le nombre de tickets clôturés
    nombre_tickets_clotures = dataframe_mois_annee.shape[0]
    
    return nombre_tickets_clotures
def tickets_clotures_par_mois(dataframe, annee):
    dataframe = str_df_to_dt_df(dataframe)
    print(dataframe['created'].describe())
    print(dataframe['resolutiondate'].describe())
    # Filtrer les données pour l'année spécifiée
    dataframe_annee = dataframe[dataframe['resolutiondate'].dt.year == annee]
    print(dataframe_annee['created'].describe())
    print(dataframe['resolutiondate'].describe())
    # Calculer le nombre de tickets clôturés par mois
    tickets_clotures = dataframe_annee['resolutiondate'].dt.month.value_counts().sort_index()
    print(tickets_clotures)
    # Créer le graphique
    plt.figure(figsize=(10, 6))
    plt.plot(tickets_clotures.index, tickets_clotures.values, marker='o')
    plt.xlabel('Mois')
    plt.ylabel('Nombre de tickets clôturés')
    plt.title(f'Nombre de tickets clôturés par mois pour l\'année {annee}')
    plt.grid(True)
    plt.xticks(range(1, 13), ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc'])
    plt.savefig(f'tickets_clotures_par_mois_{annee}.png')
    plt.show()
    return


###
def lead_time_par_mois(dataframe):
    dataframe = str_df_to_dt_df(dataframe)
    
    # Calculer le lead time pour chaque ticket et l'ajouter comme une nouvelle colonne
    dataframe['lead_time'] = (dataframe['resolutiondate'] - dataframe['created']).dt.days
    
    # Créer le graphique
    plt.figure(figsize=(10, 6))

    years = dataframe['created'].dt.year.unique()
    
    # Boucler sur chaque année présente dans le DataFrame
    for annee in years:
        # Filtrer les données pour l'année spécifiée
        dataframe_annee = dataframe[dataframe['created'].dt.year == annee]
        
        # Calculer la moyenne du lead time par mois
        lead_time_moyen = dataframe_annee.groupby(dataframe_annee['created'].dt.month)['lead_time'].mean()
        
        # Sauvegarder le graphique dans un fichier par année
        plt.plot(lead_time_moyen.index, lead_time_moyen.values, marker='o', label=f'Année {annee}')
        plt.xlabel('Mois')
        plt.ylabel('Lead time moyen (jours)')
        plt.title(f'Lead time moyen par mois pour toutes les années')
        plt.grid(True)
        plt.xticks(range(1, 13), ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc'])
        plt.legend()
        plt.savefig(f'lead_time_par_mois_{annee}test.png')
        plt.clf()  # Effacer la figure pour le prochain tour de boucle
    
    # Afficher le graphique (vide, juste pour éviter d'avoir un message d'avertissement)
    plt.show()
    return True



###
def tickets_clotures_par_annee(dataframe):
    
    dataframe = str_df_to_dt_df(dataframe)
    tickets_clotures = dataframe[dataframe['resolutiondate'].notnull()]['resolutiondate'].dt.year.value_counts().sort_index()
    
    # Créer le graphique
    plt.figure(figsize=(10, 6))
    plt.plot(tickets_clotures.index, tickets_clotures.values, marker='o')
    plt.xlabel('Année')
    plt.ylabel('Nombre de tickets clôturés')
    plt.title('Nombre de tickets clôturés par année')
    plt.grid(True)
    plt.savefig('tickets_clotures_par_annee')
    plt.show()
    return True 

###
def tickets_cree_par_annee(dataframe):
    
    dataframe = str_df_to_dt_df(dataframe)
    tickets_clotures = dataframe[dataframe['created'].notnull()]['created'].dt.year.value_counts().sort_index()
    
    # Créer le graphique
    plt.figure(figsize=(10, 6))
    plt.plot(tickets_clotures.index, tickets_clotures.values, marker='o')
    plt.xlabel('Année')
    plt.ylabel('Nombre de tickets crées')
    plt.title('Nombre de tickets créés par année')
    plt.grid(True)
    plt.savefig('tickets_crees_par_annee2')
    plt.show()
    return True

###
def nombre_ticket_creer_cloture(dataframe):
    dataframe = str_df_to_dt_df(dataframe)

    tickets_crees = dataframe['created'].dt.year.value_counts().sort_index()
    tickets_clotures = dataframe[dataframe['resolutiondate'].notnull()]['resolutiondate'].dt.year.value_counts().sort_index()

    plt.figure(figsize=(10, 6))

    # courbe pour les tickets créés
    plt.plot(tickets_crees.index, tickets_crees.values, marker='o', label='Tickets créés')
    # courbe pour les tickets clôturés
    plt.plot(tickets_clotures.index, tickets_clotures.values, marker='o', label='Tickets clôturés')

    plt.xlabel('Année')
    plt.ylabel('Nombre de tickets')
    plt.title('Nombre de tickets créés et clôturés par année')
    plt.grid(True)
    plt.legend()
    plt.savefig('nombre_de_tickets_cree_et_clôturés_par_année.png')
    # Afficher le graphique
    plt.show()
    return True

### 
def tickets_clotures_par_mois_par_annee(dataframe, output_directory):
    dataframe = str_df_to_dt_df(dataframe)    
    # années uniques présentes dans le DataFrame
    annees = dataframe['resolutiondate'].dt.year.unique()
    
    # Créer le répertoire de sortie s'il n'existe pas déjà
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    for annee in annees:
        dataframe_annee = dataframe[dataframe['resolutiondate'].dt.year == annee]
        # Calculer le nombre de tickets clôturés par mois
        tickets_clotures_par_mois = dataframe_annee.groupby(dataframe_annee['resolutiondate'].dt.month).size()
        
        # Créer le graphique
        plt.figure(figsize=(10, 6))
        plt.plot(tickets_clotures_par_mois.index, tickets_clotures_par_mois.values, marker='o')
        plt.xlabel('Mois')
        plt.ylabel('Nombre de tickets clôturés')
        plt.title(f'Nombre de tickets clôturés par mois pour l\'année {annee}')
        plt.grid(True)
        plt.xticks(range(1, 13), ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc'])
        
        filename = os.path.join(output_directory, f'tickets_clotures_{annee}.png')
        plt.savefig(filename)
        
        plt.close()
    return True

### 
def tickets_cree_par_mois_par_annee(dataframe, output_directory):
    dataframe = str_df_to_dt_df(dataframe)    
    annees = dataframe['created'].dt.year.unique()
    
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    for annee in annees:
        dataframe_annee = dataframe[dataframe['created'].dt.year == annee]
        
        tickets_clotures_par_mois = dataframe_annee.groupby(dataframe_annee['created'].dt.month).size()
        
        # Créer le graphique
        plt.figure(figsize=(10, 6))
        plt.plot(tickets_clotures_par_mois.index, tickets_clotures_par_mois.values, marker='o')
        plt.xlabel('Mois')
        plt.ylabel('Nombre de tickets créés')
        plt.title(f'Nombre de tickets créés par mois pour l\'année {annee}')
        plt.grid(True)
        plt.xticks(range(1, 13), ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc'])
        
        filename = os.path.join(output_directory, f'tickets_créés_{annee}.png')
        plt.savefig(filename)
        
        # Afficher le graphique
        plt.close()
    return True

###
def lead_time_par_annee(dataframe):
    dataframe =  str_df_to_dt_df(dataframe)
    
    # Calculer le lead time pour chaque ticket et l'ajouter comme une nouvelle colonne
    dataframe['lead_time'] = (dataframe['resolutiondate'] - dataframe['created']).dt.days
    
    # Calculer la moyenne du lead time par année
    lead_time_moyen = dataframe.groupby(dataframe['created'].dt.year)['lead_time'].mean()
    
    # Créer le graphique
    plt.figure(figsize=(10, 6))
    plt.plot(lead_time_moyen.index, lead_time_moyen.values, marker='o')
    plt.xlabel('Année')
    plt.ylabel('Lead time moyen (jours)')
    plt.title('Lead time moyen par année')
    plt.savefig('demo/lead_time_par_année.png')
    plt.grid(True)
    plt.show()
    return True


### 
def lead_time_par_mois_par_annee(dataframe, output_directory):
    dataframe = str_df_to_dt_df(dataframe)    
    # années uniques présentes dans le DataFrame
    annees = dataframe['resolutiondate'].dt.year.unique()
    
    # Créer le répertoire de sortie s'il n'existe pas déjà
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    for annee in annees:
        dataframe_annee = dataframe[dataframe['resolutiondate'].dt.year == annee]
        # Calculer le nombre de tickets clôturés par mois
        tickets_clotures_par_mois = dataframe_annee.groupby(dataframe_annee['resolutiondate'].dt.month).size()
        
        # Créer le graphique
        plt.figure(figsize=(10, 6))
        plt.plot(tickets_clotures_par_mois.index, tickets_clotures_par_mois.values, marker='o')
        plt.xlabel('Mois')
        plt.ylabel('Nombre de tickets clôturés')
        plt.title(f'Nombre de tickets clôturés par mois pour l\'année {annee}')
        plt.grid(True)
        plt.xticks(range(1, 13), ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc'])
        
        filename = os.path.join(output_directory, f'tickets_clotures_{annee}.png')
        plt.savefig(filename)
        
        plt.close()
    return True



#file_path = 'issue.csv'  
#dataframe = csv_to_dataframe(file_path)
#print(a(dataframe))
#plot_issue_types_distribution(dataframe)
#analyze_time_spent_on_issues(dataframe)
#get_number_issues_solved_within_preriod_graph(dataframe,2)
# df_created_solved = dataframe[['issue_key','created','resolutiondate']]
# #print(df_created_solved)
# #print(type(get_creation_resolution_time_statistics(dataframe)))
# print(get_month_statistics(dataframe))

#print(get_month_statistics(dataframe))
#genarate_creation_resolution_figure(dataframe)
#print(get_statistics_by_field(dataframe,'creatorname'))
#print(get_statistics_by_field(dataframe,'issuetypename'))
#print(get_statistics_by_field(dataframe,'projectname'))

#print(get_statistics_by_field(dataframe,'assignee'))
#result = get_double_group_by_statistics(dataframe,'week')
#,issuetypeid,,issuetypename,issuetypesubtask,issuetypehierarchyLevel,timespend,projectid,,projectname,projectTypeKey,aggregatetimespent,resolutiondate,workratio,watchCount,isWatching,lastViewed,created,priorityname,priorityid,labelsnumber,assignee,statusname,statuscategoryname,,,aggregatetimeestimate,creatoremailAddress,creatorname,subtasksnumber,reportername,reporteremail,duedate,votes,workflow_start_time,workflow_end_time

#print(get_double_group_by_statistics(dataframe,'month'))
