import json
from flask import Flask, request

app = Flask(__name__)

# Receive the results from browser and store them in a json file
@app.route("/store_results", methods=['POST'])
def store_results():
    results = request.get_json(force=True)
    with open('results/results.json', 'a') as results_file:
        json.dump(results, results_file)
    return "SUCCESS"

if __name__ == "__main__":
    app.debug = True
    app.run()
