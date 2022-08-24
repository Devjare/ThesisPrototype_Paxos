# Make a request
export CTYPE='Content-Type: application/json'

if [ $1 = 1 ]
then
	export ENDPOINT=http://localhost:60002/parse
	curl -X POST $ENDPOINT -H "$CTYPE" -d '{"inputDir":"/source/ds", "logFileName":"HDFS_100k.log","regex":["blk_(|-)[0-9]+","(/|)([0-9]+\\.){3}[0-9]+(:[0-9]+|)(:|)","(?<=[^A-Za-z0-9])(\\-?\\+?\\d+)(?=[^A-Za-z0-9])|[0-9]+$"], "logFormat":"<Date> <Time> <Pid> <Level> <Component>: <Content>","st":0.5,"depth":4 }'
else
	export ENDPOINT=http://localhost:60002/detect
	curl -X POST $ENDPOINT -H "$CTYPE" -d '{"structuredLog":"/data/HDFS_100k.log_structured.csv", "labelFile":"/data/anomaly_label.csv","window":"session", "trainRatio":0.5,"splitType":"uniform","termWeighting":"tf-idf","normalization":"uniform" }'
fi

