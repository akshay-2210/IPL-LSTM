from flask import Flask, render_template, request, url_for
import pickle
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import tensorflow as tf



app=Flask(__name__)
model_path = 'ipl.h5'
model = load_model(model_path)
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')




@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        bat = str(request.form['Batting team'])
        bowl = str(request.form['Bowling team'])
        if bat == bowl:
            return render_template('index.html',prediction_text='Batting and Bowling team can not be the same.')

            
        overs = float(request.form['Overs'])
        balls = float(request.form['Balls'])
        scored = float(request.form['Runs Scored'])
        wicket = float(request.form['Wicket left'])
        required = float(request.form['Required Runs'])
         
       
        probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])
        predictions = probability_model.predict([[[overs,balls,scored,wicket,required]]])

        if predictions[0][0]>predictions[0][1]:
            result = bowl
            probability = predictions[0][0]
        else:
            result = bat
            probability = predictions[0][1]
    
        
        return render_template('index.html',prediction_text="{} has {}% chance of winning the match".format(result,np.round(probability*100,2)))


if __name__=="__main__":
    app.run(debug=True)
