import json
import os
from flask import Flask, request

import dromaeo_utils

app = Flask(__name__)

# Receive the results from browser and store them in a json file
@app.route("/store_results", methods=['POST'])
def store_results():
    results = request.get_json(force=True)
    with open(os.path.join(dromaeo_utils.config.ResultsDir, 'results.json'), 'a') as results_file:
        json.dump(results, results_file)
    return "SUCCESS"

if __name__ == "__main__":
    app.debug = True
    dromaeo_utils.config.init("dromaeo.conf")
    app.run(port=dromaeo_utils.config.Port)
