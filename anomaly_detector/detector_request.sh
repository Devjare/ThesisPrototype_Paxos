# export ENDPOINT=http://192.168.1.217:1765/detect_anomalies
export ENDPOINT=http://localhost:1765/detect
# export ENDPOINT=http://172.17.0.2:5051/parse
export CTYPE='Content-Type: application/json'
export STRUCTURED_LOG=../data/drain_result/HDFS_100k.log_structured.csv
export LABEL_FILE=../data/anomaly_label.csv
curl -X POST $ENDPOINT -H "$CTYPE" -d '{"structuredLog":"../data/drain_result/HDFS_100k.log_structured.csv", "labelFile":"../data/anomaly_label.csv","window":"session", "trainRatio":0.5,"splitType":"uniform","termWeighting":"tf-idf","normalization":"uniform" }'
