from ast import Return
from flask import Flask,render_template,request,redirect
from flask_cors import CORS,cross_origin
import pickle
import pandas as pd
import numpy as np


from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import math
import os

app=Flask(__name__)
cors=CORS(app)
model=pickle.load(open('RandomForestRegressor.pkl','rb'))
car=pd.read_csv('cardekho_updated.csv')

@app.route('/',methods=['GET','POST'])
def index():
    full_name=sorted(car['full_name'].unique())
    year=sorted(car['year'].unique(),reverse=True)
    seller_type=sorted(car['seller_type'].unique())
    fuel_type=car['fuel_type'].unique()
    transmission_type=sorted(car['transmission_type'].unique())
    mileage=car['mileage'].unique()
    engine=(car['engine'].unique())
    max_power=car['max_power'].unique()
    seats=car['seats'].unique()
    
  
    return render_template('index.html',full_name=full_name,year=year,
                           seller_type=seller_type,fuel_type=fuel_type,
                           transmission_type=transmission_type,mileage=mileage,engine=engine,max_power=max_power,seats=seats)
@app.route('/predict',methods=['POST'])
@cross_origin()
def predict():
    full_name=request.form.get('full_name')
    year=request.form.get('year')
    seller_type=request.form.get('seller_type')
    km_driven=request.form.get('km_driven')
    fuel_type=request.form.get('fuel_type')
    transmission_type=request.form.get('transmission_type')
    mileage=request.form.get('mileage')
    engine=request.form.get('engine')
    max_power=request.form.get('max_power')
    seats=request.form.get('seats')
    print(type(seller_type),seller_type)
    print(type(km_driven),km_driven)
    print(type(fuel_type),fuel_type)
    print(type(full_name),full_name)
    print(type(transmission_type),transmission_type)
    print(type(mileage),mileage)
    print(type(engine),engine)
    print(type(max_power),max_power)
    print(type(seats),seats)
    print(type(year),year)
   
    
    '''km_driven = km_driven.split(' ')
    km_driven = km_driven[0]
    km_driven = km_driven.replace(',','')'''
    mileage = mileage.split(' ')
    mileage = mileage[0].split('e')
    mileage = mileage[2]
    print(mileage)
    engine = engine.split(' ')
    engine = engine[0].split('e')
    engine = engine[1]
    print(engine)
    max_power= max_power.split(' ')
    max_power = max_power[1].split('r')
    max_power = max_power[1]
    print(max_power)
    #seats = seats.split('s')
    #seats = seats[1] 
    x=[]
    x.append(year)
    x.append(km_driven)
    x.append(mileage)
    x.append(engine)
    x.append(max_power)
    x.append("5")
    if seller_type == "Individual":
        x = x+["1","0"]
    else:
        x = x+["0","1"]
    if fuel_type == "Diesel":
        x = x+["1","0","0","0"]
    elif fuel_type=="Electric":
        x = x+["0","1","0","0"]
    elif fuel_type == "LPG":
        x = x+["0","0","1","0"]
    else:
        x = x+["0","0","0","1"]
    if transmission_type == "Manual":
        x.append("1")
    else:
        x.append("0") 
    if "BMW" in full_name:
        x = x+["1","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]
    elif "Chevrolet" in full_name:
        x = x+["0","1","0","0","0","0","0","0","0","0","0","0","0","0","0"]
    elif "Ford" in full_name:
        x = x+["0","0","1","0","0","0","0","0","0","0","0","0","0","0","0"]
    elif "Honda" in full_name:
        x = x+["0","0","0","1","0","0","0","0","0","0","0","0","0","0","0"]
    elif "Hyundai" in full_name:
        x = x+["0","0","0","0","1","0","0","0","0","0","0","0","0","0","0"]
    elif "Mahindra" in full_name:
        x = x+["0","0","0","0","0","1","0","0","0","0","0","0","0","0","0"]
    elif "Maruti" in full_name:
        x = x+["0","0","0","0","0","0","1","0","0","0","0","0","0","0","0"]
    elif "Mercedes-Benz" in full_name:
        x = x+["0","0","0","0","0","0","0","1","0","0","0","0","0","0","0"]
    elif "Nissan" in full_name:
        x = x+["0","0","0","0","0","0","0","0","1","0","0","0","0","0","0"]
    elif "Renault" in full_name:
        x = x+["0","0","0","0","0","0","0","0","0","1","0","0","0","0","0"]
    elif "Skoda" in full_name:
        x = x+["0","0","0","0","0","0","0","0","0","0","1","0","0","0","0"]
    elif "Tata" in full_name:
        x = x+["0","0","0","0","0","0","0","0","0","0","0","1","0","0","0"]
    elif "Toyota" in full_name:
        x = x+["0","0","0","0","0","0","0","0","0","0","0","0","1","0","0"]
    elif "Volkswagen" in full_name:
        x = x+["0","0","0","0","0","0","0","0","0","0","0","0","0","1","0"]
    else:
        x = x+["0","0","0","0","0","0","0","0","0","0","0","0","0","0","1"]
    
    df = pd.DataFrame([x], columns = ["year","km_driven","mileage","engine","max_power","seats",
                                        "seller_type_Individual","seller_type_Trustmark Dealer",
                                    "fuel_type_Diesel","fuel_type_Electric","fuel_type_LPG","fuel_type_Petrol ",
                                        "transmission_type_Manual",
                                        "company_BMW","company_Chevrolet","company_Ford", "company_Honda","company_Hyundai",
                                        "company_Mahindra","company_Maruti","company_Mercedes-Benz","company_Nissan","company_Renault", "company_Skoda", "company_Tata","company_Toyota","company_Volkswagen","company_others"
                                 ])
    print(x)
    prediction = model.predict(df)
    return prediction
    

if __name__=='__main__':
    app.run()
   
    