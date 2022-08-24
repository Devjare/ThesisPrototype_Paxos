# export ENDPOINT=http://148.247.204.202:5050/parse
# export ENDPOINT=http://172.17.0.3:50023/parse

export ENDPOINT=http://localhost:60002/process_logs
export CTYPE='Content-Type: application/json'
curl -X POST $ENDPOINT -H "$CTYPE" -d '{ "parserReq": {"inputDir":"/source/ds", "logFileName":"HDFS_100k.log","regex":["blk_(|-)[0-9]+","(/|)([0-9]+\\.){3}[0-9]+(:[0-9]+|)(:|)","(?<=[^A-Za-z0-9])(\\-?\\+?\\d+)(?=[^A-Za-z0-9])|[0-9]+$"], "logFormat":"<Date> <Time> <Pid> <Level> <Component>: <Content>","st":0.5,"depth":4 }, "detectorReq": {"structuredLog":"/data/HDFS_100k.log_structured.csv", "labelFile":"/data/labels_100k.csv","window":"session", "trainRatio":0.5,"splitType":"uniform","termWeighting":"tf-idf","normalization":"uniform"} }'
