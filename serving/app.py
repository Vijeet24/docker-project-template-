#!/usr/bin/env python
# coding: utf-8

# In[ ]:


"""
If you are in the same directory as this file (app.py), you can run run the app using gunicorn:
    
    $ gunicorn --bind 0.0.0.0:<PORT> app:app
gunicorn can be installed via:
    $ pip install gunicorn
"""
import os
from pathlib import Path
import logging
from flask import Flask, jsonify, request, abort, render_template 
import sklearn
import pandas as pd
import joblib


#import ift6758

#imports
import comet_ml
from comet_ml import API
import pickle
import numpy as np
# from waitress import serve


LOG_FILE = os.environ.get("FLASK_LOG", "flask.log")
expected_key = 'c2REbE8eQaoRTP059ajV8VYn9'

app = Flask(__name__)

Model = None

@app.before_first_request
def before_first_request():
    """
    Hook to handle any initialization before the first request (e.g. load model,
    setup logging handler, etc.)
    """
    # TODO: setup basic logging configuration
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

    #comet import default voting ens model
    comet_ml.init()

    if not Path(f'./models/Q6ens_s.joblib').exists():
        api = API(api_key=expected_key)
        # Download a Registry Model: eg "Q6-Full-ens" registered model name
        api.download_registry_model("ift-6758-2",'xgb-model-5-3-pickle','1.0.0',
                            output_path="./models", expand=True)

    logging.info('Default model loaded: Voting ensemble')

    global Model
    Model = pickle.load('./models/xgb-model-5-3-pickle.pickle')
    
    pass


@app.route("/logs", methods=["GET"])
def logs():
    """Reads data from the log file and returns them as the response"""
    # with open(LOG_FILE, 'r') as f:
    #     return render_template('content.html', text=f.read())
    
    response = {}
    with open(LOG_FILE) as f:
        for line in f:
            response[line] = line

    return jsonify(response)  # response must be json serializable!


@app.route("/download_registry_model", methods=["POST"])
def download_registry_model():
    """
    Handles POST requests made to http://IP_ADDRESS:PORT/download_registry_model
    The comet API key should be retrieved from the ${COMET_API_KEY} environment variable.
    Recommend (but not required) json with the schema:
        {
            workspace: (required),
            model: (required),
            version: (required),
            ... (other fields if needed) ...
        }
    
    """
    # Get POST json data
    json = request.get_json()
    app.logger.info(json)

    #Model name check
    Model_name = ''
    if json['model'] == 'xgb-model-5-3-pickle':
        Model_name = 'xgb-model-5-3-pickle.pickle'


    Workspace = json['workspace']
    Model_vers = json['version']
    Model_loaded = False
    # TODO: check to see if the model you are querying for is already downloaded
    # TODO: if yes, load that model and write to the log about the model change.  
    # eg: app.logger.info(<LOG STRING>)
    
    global Model
    if Path(f'./models/{Model_name}').exists() and Model_name != 'xgb-model-5-3-pickle.pickle':
        logging.info(f'Model exists and loaded: {Model_name}')
         
        Model = pickle.load(f'./models/{Model_name}')
        Model_loaded = True
    # TODO: if no, try downloading the model: if it succeeds, load that model and write to the log
    # about the model change. If it fails, write to the log about the failure and keep the 
    # currently loaded model
    else:
        api = API()
        try:
            # Download a Registry Model: eg "Q6-Full-ens" registered model name
            api.download_registry_model(Workspace, json['model'], Model_vers,
                                output_path="./models", expand=True)

            logging.info(f'Model downloaded and loaded: {Model_name}')

            Model = joblib.load(f'./models/{Model_name}')
            Model_loaded =True
        except Exception as e:
            logging.info(f'Exception: {e}, Using default Model')



    # Tip: you can implement a "CometMLClient" similar to your App client to abstract all of this
    # logic and querying of the CometML servers away to keep it clean here


    response = json
    if Model_loaded == True:
        response['Model_downloaded'] = True
    else:
        response['Model_downloaded'] = False

    app.logger.info(response)
    return jsonify(response)  # response must be json serializable!


@app.route("/predict", methods=["POST"])
def predict():
    """
    Handles POST requests made to http://IP_ADDRESS:PORT/predict
    Returns predictions
    """
    # Get POST json data
    json = request.get_json()
    #log the data received (takes a lot of space)
    #app.logger.info(json)
    #print(json)
    X = pd.DataFrame.from_dict(json)
    print(X.head())
    #or pd.read_json()

    #global Model
    y_pred = Model.predict_proba(X)[:,1]
    print(y_pred)
    #y_pred_prob = Model.predict_proba(X)
    response = pd.DataFrame(y_pred).to_json()
    print(response)

    return response
    logging.info(f'Number of predictions made: {y_pred.shape[0]}')
    unique, counts = np.unique(y_pred, return_counts=True)
    goal_percentage = counts[1]/y_pred.shape[0]
    logging.info(f'Goal percentage: {goal_percentage}, Number of Goals: {counts[1]}')

    #log the predictions (takes a lot of space)
    #app.logger.info(response)
      # response must be json serializable!

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    #serve(app, host='0.0.0.0', port=8080)


# In[ ]:





# In[ ]:




