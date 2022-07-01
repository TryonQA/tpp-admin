from flask import Flask, request
#from flask_cors import CORS
import dl_gen as dl

app = Flask(__name__)
#CORS(app)

@app.route("/dl/", methods=['GET'])
def get_dl_num():
    state = request.args.get('state', '')
    dl_num = dl.pars_arg(state)
    return dl_num