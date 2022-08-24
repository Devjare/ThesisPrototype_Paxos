# export ENDPOINT=http://148.247.204.202:50022/parse # CINVESTAV LOCAL
# export ENDPOINT=http://172.17.0.2:50022/parse # LOCAL CONTAINER
export ENDPOINT=http://192.168.1.37:50022/parse # HOME LOCAL IP
export CTYPE='Content-Type: application/json'
curl -X POST $ENDPOINT -H "$CTYPE" -d '{"inputDir":"../data", "logFileName":"HDFS_100k.log","regex":["blk_(|-)[0-9]+","(/|)([0-9]+\\.){3}[0-9]+(:[0-9]+|)(:|)","(?<=[^A-Za-z0-9])(\\-?\\+?\\d+)(?=[^A-Za-z0-9])|[0-9]+$"], "logFormat":"<Date> <Time> <Pid> <Level> <Component>: <Content>","st":0.5,"depth":4 }'
