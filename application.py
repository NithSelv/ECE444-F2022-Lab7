import flask
from flask import jsonify, request
from flask_reestful import Resource, Api

#Import model libraries
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

##############################################################################################
#
#   INIT
#
##############################################################################################

##### model loading #####
loaded_model = None
with open('basic_classifier.pkl', 'rb') as fid:
    loaded_model = pickle.load(fid)
    
vectorizer = None
with open('count_vectorizer.pkl', 'rb') as vd:
    vectorizer = pickle.load(vd)

##############################################################################################
#
#   FLASK APP
#
##############################################################################################

# The flask app for serving predictions
application = flask.Flask(__name__)
api = Api(application)

class Evaluate(Resource):
    def get(self):
        data = request.args.get('data', '', str)
        if len(data) == 0:
            rep = jsonify({'evaluation': '-1'})
            rep.status_code = 400
        else:
            if loaded_model.predict(vectorizer.transform([data]))[0] == 'FAKE':
                rep = jsonify({'evaluation': '1'})
            else:
                rep = jsonify({'evaluation': '0'})
            rep.status_code = 200
        return rep

api.add_resource(Evaluate, '/')

if __name__ == '__main__':
    application.run()
