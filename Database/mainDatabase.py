import pandas as pd
from datetime import datetime
import bcrypt
import shutil
import csv
import os

user_directory=r'Database\Users\users.csv' #temp until we create a real database
project_directory=r'Database\Projects\projects.csv' #temp until we create a real database
raw_datasets_directory=r'Database\\rawDatasets\\'
processed_datasets_directory=r'Database\processedDatasets\\'

def check_login(username,password):
    df=pd.read_csv(user_directory)
    row=df[(df['username'] == username)]
    if row.shape[0] > 0:
        return bcrypt.checkpw(password.encode(), row.password.values[0].encode())
    
def get_user_id(username):
    df=pd.read_csv(user_directory)

    return str(df[df['username']==username]['user_id'].values[0])


def delete_user(user_id):
    df=pd.read_csv(user_directory)
    # Drop rows where the 'user_id' column is equal to user_id
    df = df[df['user_id'] != user_id]
    df.to_csv(user_directory,index=False)

def change_user_data(user_id,email,first_name,last_name,username,password):
    df=pd.read_csv(user_directory)
    df.loc[df['user_id'] == user_id, ['email', 'first_name','last_name','username','password']]\
    = [email,first_name,last_name,username,password]
    df.to_csv(user_directory,index=False)

def add_user(email, first_name, last_name, username, password):
    df=pd.read_csv(user_directory)
    if len(df)>0:
        ID=int(df.user_id.tail(1).values[0])+1
    else:
        ID=1
    with open(user_directory, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([ID,email,first_name,last_name,username,password]) 

def username_exist(username):
    df=pd.read_csv(user_directory)
    return df[(df['username'] == username)].shape[0] > 0

def email_exist(email):
    df=pd.read_csv(user_directory)
    return df[(df['email'] == email)].shape[0] > 0

def signup(email, first_name, last_name, username, password):
    if email_exist(email):
        return "Email already exists."
    elif username_exist(username):
        return "Username already exists."
    else:
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        add_user(email,first_name,last_name,username,hashed_password)
        return "Signup successful!"

def fetch_name(user_id):
    df=pd.read_csv(user_directory)
    return df[df['user_id'].astype(str)==user_id]['first_name'].values[0]

def fetch_username(user_id):
    df=pd.read_csv(user_directory)
    return df[df['user_id'].astype(str)==str(user_id)]['username'].values[0]

def fetch_email(user_id):
    df=pd.read_csv(user_directory)
    return df[df['user_id'].astype(str)==user_id]['email'].values[0]

def create_project(name,user_id,uploaded_file):
    df=pd.read_csv(project_directory)
    if len(df)>0:
        ID=int(df.project_id.tail(1).values[0])+1
    else:
        ID=1
    current_date = datetime.now().strftime("%d-%m-%Y")

    with open(project_directory, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([ID,user_id,name,current_date])
    
    file_path = raw_datasets_directory+f"raw_dataset_{ID}.csv"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)    

def read_projects(user_id):
    df = pd.read_csv(project_directory)
    user_projects = df[df['user_id'].astype(str) == str(user_id)]
    
    projects_dict = {}
    for _, row in user_projects.iterrows():
        projects_dict[row['project_id']] = {
            'name': row['name'],
            'date': row['date']
        }
    
    return projects_dict


def get_project(project_id):
    # Read project details from the project directory
    df = pd.read_csv(project_directory)
    project = df[df['project_id'].astype(str) == str(project_id)].iloc[0]
    project_details = {
        'name': project['name'],
        'date': project['date']
    }
    
    # Get raw dataset
    raw_dataset_path = os.path.join(raw_datasets_directory, f"raw_dataset_{project_id}.csv")
    if os.path.exists(raw_dataset_path):
        raw_dataset = pd.read_csv(raw_dataset_path)
        project_details['raw_dataset'] = raw_dataset.to_json()
    else:
        project_details['raw_dataset'] = None
    
    # Get processed dataset
    processed_dataset_path = os.path.join(processed_datasets_directory, f"processed_dataset_{project_id}.csv")
    if os.path.exists(processed_dataset_path):
        processed_dataset = pd.read_csv(processed_dataset_path)
        project_details['processed_dataset'] = processed_dataset.to_json()
    else:
        project_details['processed_dataset'] = None
    
    return project_details
