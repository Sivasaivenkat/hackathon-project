from flask import Flask,request,render_template
import numpy as np
import pandas
import sklearn
import pickle

# importing model
#model_path='models/'
#with open(model_path,'rb') as file:
#    model = pickle.load(file)

model = pickle.load(open('models/model.pkl','rb'))
sc = pickle.load(open('models/standscaler.pkl','rb'))
ms = pickle.load(open('models/minmaxscaler.pkl','rb'))


# creating flask app
app = Flask(__name__)

#this is my base page
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about_us')
def about():
    return render_template('about_us.html')

@app.route('/overview', methods = ['GET'])
def overview():
    return render_template('overview.html')

@app.route('/predict',methods=['POST'])
def predict():
    N = int(request.form['Nitrogen'])
    P = int(request.form['Phosporus'])
    K = int(request.form['Potassium'])
    temp =int( request.form['Temperature'])
    humidity =int( request.form['Humidity'])
    ph = float(request.form['Ph'])
    rainfall = int(request.form['Rainfall'])

    feature_list = [N, P, K, temp, humidity, ph, rainfall]
    single_pred = np.array(feature_list).reshape(1, -1)

    scaled_features = ms.transform(single_pred)
    final_features = sc.transform(scaled_features)
    prediction = model.predict(final_features)

    crop_dict = {1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya", 7: "Orange",
                 8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
                 14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 18: "Mothbeans",
                 19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"}

    if prediction[0] in crop_dict:
        crop = crop_dict[prediction[0]]
        result = "{} is the best crop to be cultivated right there".format(crop)
    else:
        result = "Sorry, we could not determine the best crop to be cultivated with the provided data."
    return render_template('index.html',result = result)

# python main
if __name__ == "__main__":
    app.run(use_reloader=True,debug=True,port=5012)