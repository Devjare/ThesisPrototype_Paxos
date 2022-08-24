import sys
sys.path.append('../')
from PCA import PCA
from utils import dataloader, preprocessing
from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/home")
def home():
    return "<h5>Home!</h5>"

@app.route("/paxos_function")
def paxos_function():

@app.route("/detect_anomalies", methods=["POST"])
def detect_anomalies():
    print("Current dir: ", os.getcwd()) 
    model = PCA()
    # print(model) 
    args = request.json
    struct_log = args['structuredLog']
    label_file = args['labelFile']
    window = args['window'] 
    train_ratio = args['trainRatio']
    split_type = args['splitType']
    term_weighting = args['termWeighting']
    normalization = args['normalization']

    print("StructuredLog File Dir: ", struct_log)
    print("Label File Dir: ", label_file)

    # struct_log = 'data/HDFS_100k.log_structured.csv' # The structured log file
    # label_file = 'data/anomaly_label.csv' # The anomaly label file

    # TODO: IMPLEMENT A GENERIC PREPROCESOR/DATALOADER
    # (x_train, y_train), (x_test, y_test) = dataloader.load_HDFS(struct_log,
    #                                                             label_file=label_file,
    #                                                             window='session', 
    #                                                             train_ratio=0.5,
    #                                                             split_type='uniform')
    # feature_extractor = preprocessing.FeatureExtractor()
    # x_train = feature_extractor.fit_transform(x_train, term_weighting='tf-idf', 
    #                                           normalization='zero-mean')
    (x_train, y_train), (x_test, y_test) = dataloader.load_HDFS(struct_log,
                                                                label_file=label_file,
                                                                window=window, 
                                                                train_ratio=train_ratio,
                                                                split_type=split_type)
    feature_extractor = preprocessing.FeatureExtractor()
    x_train = feature_extractor.fit_transform(x_train, term_weighting=term_weighting, 
                                              normalization=normalization)
    x_test = feature_extractor.transform(x_test)

    model = PCA()
    model.fit(x_train)
    print("X_Train: ", x_train)
    print("Y_Train: ", y_train)
    
    print("X_Test: ", x_test)
    print("Y_Test: ", y_test)

    print('Train validation:')
    precision, recall, f1 = model.evaluate(x_train, y_train)
    
    print('Test validation:')
    precision, recall, f1 = model.evaluate(x_test, y_test)
    return { 'status': 'Success',
             'message': 'Succsesfully executed anomaly detection!',
             'content': {'precision': precision, 'recall': recall, 'f1': f1 }
             }
    

if __name__ == "__main__":
    PORT = os.getenv("PORT")
    app.run(debug=True, host="0.0.0.0", port=PORT)
