import numpy as np
import pandas as pd 
import pickle
import pymsgbox as msg

from flask import render_template , request , Flask

app = Flask(__name__)

model = pickle.load(open('mark.pkl','rb'))
   
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/predict',methods=['POST'])
def predict():
    m1 = float(request.form.get('mid1'))
    m2 = float(request.form.get('mid2'))
    if m1<0 or m1>10 or m2<0 or m2>10:
        if m1>10 or m1<0:
            msg.alert('Mid1 is based on GPA.You should enter between 0 to 10', 'title')
        elif m2>10 or m2<0:
            msg.alert('Mid2 is based on GPA.You should enter between 0 to 10', 'title')
        return render_template('home.html')
    else:
        dt =np.array([[m1,m2]])
        sample =pd.DataFrame(dt)
        output = model.predict(sample)
        foutput = np.around(output, 2)
        if foutput>10:
            foutput=10
            str = 'EXCELLENT!'
            return render_template('home.html',result=foutput,note=str)
        elif foutput>8.0:
            str1 = 'WELL DONE!'
            return render_template('home.html',result=foutput[0][0],note=str1)
        elif foutput>6.0:
            str2 = 'GOOD!KEEP PRACTICING'
            return render_template('home.html',result=foutput[0][0],note=str2)
        elif foutput>5.0:
            str3 = 'BORDER PASS!NEED TO BE PRACTICE'
            return render_template('home.html',result=foutput[0][0],note=str3)
        else:
            str4 = 'FAILED'
            return render_template('home.html',result=foutput[0][0],note=str4)

if __name__ == '__main__':
    app.run(debug=True)
