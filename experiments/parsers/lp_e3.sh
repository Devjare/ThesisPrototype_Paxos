
# Make a request
export CTYPE='Content-Type: application/json'

export ENDPOINT=http://localhost:60002/parse

curl -X POST $ENDPOINT -H "$CTYPE" -d '{"inputDir":"/logparser/data/raw_logs", "logFileName":"HDFS_1M.log","regex":["blk_(|-)[0-9]+","(/|)([0-9]+\\.){3}[0-9]+(:[0-9]+|)(:|)","(?<=[^A-Za-z0-9])(\\-?\\+?\\d+)(?=[^A-Za-z0-9])|[0-9]+$"], "logFormat":"<Date> <Time> <Pid> <Level> <Component>: <Content>","st":0.5,"depth":4 }'
