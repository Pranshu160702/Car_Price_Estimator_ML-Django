from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
import numpy as np
import pickle

model = pickle.load(open(r'C:/Users/asus/Desktop/Projects/Machine Learning Concepts/LinearRegression_Django/django_lr/django_lr/LinearRegressionModel.pkl','rb'))

data = pd.read_csv(r'C:/Users/asus/Desktop/Projects/Machine Learning Concepts/LinearRegression_Django/django_lr/django_lr/cleaned_car_data.csv')

def homePage(request):
    company = sorted(data['company'].unique())
    name = sorted(data['name'].unique())
    year = sorted(data['year'].unique(),reverse=True)
    fuel_type = sorted(data['fuel_type'].unique())
    kms_driven = sorted(data['kms_driven'].unique())
    dict = {
        'companies':company, 
        'car_models':name, 
        'years':year, 
        'fuel_types':fuel_type,
        'kms_driven':kms_driven
    }
    return render(request, 'index.html', dict)

def estimatePrice(request):
    company = ''
    car_model = ''
    year = ''
    fuel_type = ''
    kms_driven = ''
    prediction = ''
    try:
        if request.method=="POST":
            data = request.POST
            for key,value in data.items():
                if key=='company':
                    company = value
                if key=='car_model':
                    car_model = value
                if key=='year':
                    year = value
                if key=='fuel_type':
                    fuel_type = value
                if key=='kms_driven':
                    kms_driven = value
            prediction = model.predict(pd.DataFrame([[car_model, company, year, kms_driven, fuel_type]], columns=['name', 'company', 'year', 'kms_driven', 'fuel_type']))
    except:
        return HttpResponse(request, "Some Unidentified Error has occured")
    dictas = {
        'car_company': company,
        'car_model': car_model,
        'car_year': year,
        'car_fuel_type': fuel_type,
        'final_price': '₹ ' + str(np.round(prediction[0])),
    }
    return render(request, 'predictionPage.html', dictas)