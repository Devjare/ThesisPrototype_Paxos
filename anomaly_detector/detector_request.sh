export ENDPOINT=http://148.247.204.202:5052/detect_anomalies
# export ENDPOINT=http://172.17.0.2:5051/parse
export CTYPE='Content-Type: application/json'
export STRUCTURED_LOG=../data/drain_result/HDFS_100k.log_structured.csv
export LABEL_FILE=../data/labels_100k.csv
curl -X POST $ENDPOINT -H "$CTYPE" -d '{"structuredLog":"../data/drain_result/HDFS_100k.log_structured.csv", "labelFile":"../data/labels_100k.csv","window":"session", "trainRatio":0.5,"splitType":"uniform","termWeighting":"tf-idf","normalization":"uniform" }'
