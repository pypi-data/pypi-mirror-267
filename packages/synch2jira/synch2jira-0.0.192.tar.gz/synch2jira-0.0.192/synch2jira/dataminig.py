import json
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
        print(dataframe["created"].describe())
        print(dataframe['resolutiondate'].describe())
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
