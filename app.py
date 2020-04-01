#!/usr/bin/env python3
import csv
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from aws_cdk import core
from dll_infra.dll_infra_stack import SageMakerStack


def get_csv_users():
    res = []
    with open(os.getenv('USERLIST', 'users.csv'), 'r') as f:
        for row in csv.DictReader(f):
            res.append(row)
    return res

def get_firebase_users():
    cred = credentials.Certificate('firebase_credentials.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    users = set()
    res = []
    for team in db.collection('team').stream():
        for user_email in team.to_dict()['members'].keys():
            if user_email in users:
                raise ValueError('% exist in more than one team', user_email)
            res.append({'email': user_email, 'password': 'changeit', 'team': team.id}) # XXX: handle pwgen
    return res

app = core.App()
users = get_firebase_users()

SageMakerStack(app, "dll-sg", 
        users=users,
        env={'region': os.getenv('AWS_REGION', 'us-east-1')})

app.synth()
