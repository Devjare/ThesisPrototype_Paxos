# Make a request
export CTYPE='Content-Type: application/json'

export ENDPOINT=http://localhost:60002/detect

curl -X POST $ENDPOINT -H "$CTYPE" -d '{"structuredLog":"/data/parse_result/HDFS_100k.log_structured.csv", "labelFile":"/data/anomaly_label.csv","window":"session", "trainRatio":0.5,"splitType":"uniform","termWeighting":"tf-idf","normalization":"uniform" }'

