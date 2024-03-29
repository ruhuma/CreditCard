from flask import Flask, render_template, request
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib
import pandas as pd
import os
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)
@app.route('/')
def Hello():
    return render_template('index.html')

@app.route('/classification', methods = ['GET','POST'])
def hey():
    try:
        if request.method == 'POST':
            print('1 starting')
            selected_month = float(request.form['month'])
            print('month',selected_month)
            age = float(request.form['age'])
            print('age',age)
            occupation = request.form['occupation']
            annualincome = float(request.form['annualincome'])
            print('annualincome',annualincome)
            num_bank_accounts = float(request.form['num_bank_accounts'])
            num_credit_card = float(request.form['num_credit_card'])
            interest_rate = float(request.form['interest_rate'])
            num_loans = float(request.form['num_loans'])
            print('2')
            delay_due_date = float(request.form['delay_due_date'])
            delay_payments = float(request.form['delay_payments'])
            changed_credit_limit = float(request.form['changed_credit_limit'])
            #credit_inquiry = float(request.form['credit_inquiry'])
            credit_mix = float(request.form['credit_mix'])
            #outstanding_debts = float(request.form['outstanding_debts'])
            credit_ration = float(request.form['credit_ration'])
            credit_history_age = float(request.form['credit_history_age'])
            minimum_amount = float(request.form['minimum_amount'])
            EMI_per_month = float(request.form['EMI_per_month'])
            #amount_invested_monthly = float(request.form['amount_invested_monthly'])
            monthly_balance = float(request.form['monthly_balance'])
            payment_behaviour = float(request.form['payment_behaviour'])
            print(payment_behaviour)
            print(occupation)
            with open('label_encoder_5.pkl', 'rb') as file:
                label_encoder = pickle.load(file)
            #occupation_encoded = label_encoder.transform(np.array([[occupation]]))
            #print('encoded',occupation_encoded)
            #occupation_encoded_d = occupation_encoded[0].astype(np.float64)
            #print(occupation_encoded_d)
            if occupation in label_encoder.classes_:
                occupation_encoded = label_encoder.transform(np.array([[occupation]]))
                # Convert to float64 if needed
                occupation_encoded_d = occupation_encoded[0].astype(np.float64)
            else:
                le=LabelEncoder()
                occupation_encoded = le.fit_transform(np.array([[occupation]]))
                occupation_encoded_d = occupation_encoded[0].astype(np.float64)
            print('monthly balance',monthly_balance)
            print('occupation encoded',occupation_encoded_d)

            input_array = np.array([[selected_month,age,occupation_encoded_d,annualincome,num_bank_accounts,num_credit_card,interest_rate
                                     ,num_loans,delay_due_date,delay_payments,changed_credit_limit,credit_mix,credit_ration,credit_history_age,minimum_amount,
                                     EMI_per_month,payment_behaviour,monthly_balance]]).astype(np.float64)
            
            model = pickle.load(open('best_rf_model_5.pkl','rb'))
            scaler = joblib.load("stdscaler_CS_5.pkl")
            input_scaled_G = scaler.transform(input_array)
            print('Input scaled',input_scaled_G)
            creditscoreclassified = model.predict(input_scaled_G)
            print('Input Array',input)
            print('Scaled Array',input_scaled_G)
            print(creditscoreclassified)
            if creditscoreclassified == 0:
                classification = 'Good'
            elif creditscoreclassified== 1:
                classification = 'Bad'
            elif creditscoreclassified== 2:
                classification = 'Standard'
            else:
                classification = 'Unable to process'
            return render_template('classification.html',creditscore=classification)
        else:
            return render_template('error.html',creditscore='Unable to process with received input.')
    except ValueError:
        return render_template('error.html',creditscore='Not correct Input. Please enter correct data types in the form!')

if __name__ == '__main__':
    app.run()
