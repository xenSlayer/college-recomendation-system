from flask import Flask, render_template, url_for, request
import pandas as pd
import math
import pickle


# app intialization
app = Flask(__name__)
version = 1
data = pd.read_csv(f'data.csv')


# routes

# Home page route
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


# routes for university lists
@app.route('/universities')
def universities():
    collegenames = []
    for i in data['Universities']:
        collegenames.append(i)
    return render_template('universities.html', data=data, datalen=len(data),
                           ld=math.ceil(len(data)/20), title='Universities', collegenames=collegenames)


# About page route
@app.route('/about')
def about():
    return render_template('about.html', title='About')

# Findy my college route


@app.route('/findmycollege', methods=['GET', 'POST'])
def findmycollege():
    # getting user input of dream college
    usercollege = []
    if request.method == "POST":
        if request.form.get('Public_university') == '1':
            usercollege.append(1)
        else:
            usercollege.append(0)
        if request.form.get('Scholarship') == '1':
            usercollege.append(1)
        else:
            usercollege.append(0)
        if request.form.get('Accommodation') == '1':
            usercollege.append(1)
        else:
            usercollege.append(0)
        usercollege.append(float(request.form['Fees']))
        usercollege.append(int(request.form['TOFEL']))
        if request.form['IELTS'] == "1":
            usercollege.append(0)
        else:
            usercollege.append(float(request.form['IELTS']))
        if request.form['PTE'] == "10":
            usercollege.append(0)
        else:
            usercollege.append(float(request.form['PTE']))
        if request.form['GRE'] == "260":
            usercollege.append(0)
        else:
            usercollege.append(float(request.form['GRE']))

        # importing our recommender model to find the right university for user

        col = ['Image', 'link']
        result = []
        pdata = data.drop(col, 1)
        pivot_data = pdata.set_index('Universities')
        model = pickle.load(open(f'college{version}.pkl', 'rb'))
        d, i = model.kneighbors([usercollege], n_neighbors=10)
        for j in range(len(d.flatten())):
            result.append(pivot_data.index[i.flatten()[j]])
        df = pd.DataFrame({'Universities': result})
        df = df.merge(data, on="Universities")
        datalen = len(df)
        return render_template('findmycollege.html', title='Filter', data=df,
                               datalen=datalen, userdata=usercollege, userdatalen=len(usercollege))
    return render_template('findmycollege.html', title='Filter')


if __name__ == '__main__':
    app.run(debug=True)
