import flask
from flask import jsonify, request
from flask_restful import Resource, Api

# Import model libraries
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
        if not request.is_json:
            rep = jsonify({'Error': 'Not JSON request!'})
            rep.status_code = 400
            return rep
        else:
            data = request.get_json(silent=True)
            if data is None:
                rep = jsonify({'Error': 'Failed to get JSON data!'})
                rep.status_code = 400
                return rep
            else:
                for key in data:
                    if not isinstance(key, str):
                        rep = jsonify({'Error': 'Invalid key!'})
                        rep.status_code = 400
                        return rep
                    if not isinstance(data[key], str):
                        rep = jsonify({'Error': 'Invalid value!'})
                        rep.status_code = 400
                        return rep
                eval_dict = {}
                for key in data:
                    if loaded_model.predict(vectorizer.transform([data[key]]))[0] == 'FAKE':
                        eval_dict[key] = 1
                    else:
                        eval_dict[key] = 0
                rep = jsonify(eval_dict)
                rep.status_code = 200
                return rep

api.add_resource(Evaluate, '/')

if __name__ == '__main__':
    application.run()
