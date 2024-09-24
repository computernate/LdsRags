from flask import Flask, request, abort, jsonify
import json

app = Flask(__name__)

@app.route('/test', methods=['GET'])
def test():
    return json.dumps({"status":200,"text":"WORSK FINE"})

if __name__ == '__main__':
    app.run()