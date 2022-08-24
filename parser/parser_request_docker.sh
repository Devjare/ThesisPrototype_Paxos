# export ENDPOINT=http://148.247.204.202:5050/parse
# export ENDPOINT=http://172.17.0.3:50023/parse
export ENDPOINT=http://localhost:40002/parse
export CTYPE='Content-Type: application/json'
curl -X POST $ENDPOINT -H "$CTYPE" -d '{"inputDir":"/source/ds", "logFileName":"HDFS_100k.log","regex":["blk_(|-)[0-9]+","(/|)([0-9]+\\.){3}[0-9]+(:[0-9]+|)(:|)","(?<=[^A-Za-z0-9])(\\-?\\+?\\d+)(?=[^A-Za-z0-9])|[0-9]+$"], "logFormat":"<Date> <Time> <Pid> <Level> <Component>: <Content>","st":0.5,"depth":4 }'
