import pandas as pd
import os
import bcrypt
import csv

user_directory='Database\Users\users.csv'
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