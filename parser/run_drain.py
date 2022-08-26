#!/usr/bin/env python
from flask import Flask, request
from drain import Drain
import time
import os

app = Flask(__name__)

@app.route("/home")
def home():
    return "<h5>Home!</h5>"

@app.route("/parse", methods=["POST"])
def parse():
    args = request.json

    input_dir = args['inputDir']
    output_dir = './data/parse_result/' # The output directory of parsing results
    logfile_name = args['logFileName']
    log_format = args['logFormat']
    rex = args['regex'] # List of regex., optional.

    depth = args['depth']
    st = args['st']
   
    start_time = time.time()
    parser = Drain.LogParser(log_format, indir=input_dir, outdir=output_dir,  depth=depth, st=st, rex=rex)
    parser.parse(logfile_name)
    
    end_time = time.time()
    
    total_time_taken = end_time - start_time
    
    return { "status": "Successfully parsed!",
             "timeTaken": total_time_taken,
             "message": "Stored structured logs on default storage."
             }


if __name__ == "__main__":
    PORT = os.getenv("PORT")
    app.run(debug=True, host="0.0.0.0", port=PORT)
