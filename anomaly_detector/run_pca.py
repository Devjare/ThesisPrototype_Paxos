import sys
sys.path.append('../')
from PCA import PCA
from utils import dataloader, preprocessing
from flask import Flask, request
import os
import time

app = Flask(__name__)

@app.route("/")
def home():
    return "<h5>Home!</h5>"

@app.route("/detect", methods=["POST"])
def detect_anomalies():
    model = PCA()
    args = request.json
    struct_log = args['structuredLog']
    label_file = args['labelFile']
    window = args['window'] 
    train_ratio = args['trainRatio']
    split_type = args['splitType']
    term_weighting = args['termWeighting']
    normalization = args['normalization']

    (x_train, y_train), (x_test, y_test) = dataloader.load_HDFS(struct_log,
                                                                label_file=label_file,
                                                                window=window, 
                                                                train_ratio=train_ratio,
                                                                split_type=split_type)
    feature_extractor = preprocessing.FeatureExtractor()
    start_time = time.time()
    x_train = feature_extractor.fit_transform(x_train, term_weighting=term_weighting, 
                                              normalization=normalization)
    x_test = feature_extractor.transform(x_test)
    
    print("X_TRAIN: ", x_train)
    print("X_TEST: ", x_test)
    
    model = PCA()
    model.fit(x_train)
    precision, recall, f1 = model.evaluate(x_train, y_train)
    
    precision, recall, f1 = model.evaluate(x_test, y_test)
    end_time = time.time()
    
    total_time_taken = end_time - start_time
    return { 'status': 'Success',
             'timeTaken': total_time_taken,
             'message': 'Succsesfully executed anomaly detection!',
             'content': {'precision': precision, 'recall': recall, 'f1': f1 }
             }
    

if __name__ == "__main__":
    # PORT = os.getenv("PORT")
    app.run(debug=True, host="0.0.0.0", port=1765)
