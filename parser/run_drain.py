#!/usr/bin/env python
from flask import Flask, request
from drain import Drain
import os

app = Flask(__name__)

@app.route("/home")
def home():
    return "<h5>Home!</h5>"

@app.route("/parse", methods=["POST"])
def parse():
    # Get parameters.
    args = request.json

    input_dir = args['inputDir']
    # output_dir = args['putDir'] Outputdir will be the same always(shared volume).
    output_dir = './data/drain_result/' # The output directory of parsing results
    logfile_name = args['logFileName']
    log_format = args['logFormat']
    rex = args['regex'] # List of regex., optional.

    depth = args['depth']
    st = args['st']
    
    # for i in range(len(rex)):
    #     # rex[i] = repr(rex[i])
    #     rex[i] = rex[i].replace('\\\\', '\\')
    
    print("Recieved regex: ", rex)
    parser = Drain.LogParser(log_format, indir=input_dir, outdir=output_dir,  depth=depth, st=st, rex=rex)
    parser.parse(logfile_name)
    
    return { "status": "Successfully parsed!",
             "message": "Stored structured logs on default storage."
             }


if __name__ == "__main__":
    PORT = os.getenv("PORT")
    app.run(debug=True, host="0.0.0.0", port=PORT)
