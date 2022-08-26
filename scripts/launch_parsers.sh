# LOG PARSING. default name lp_net

if [ $# -eq 0 ]
then
	export NET_NAME=lp_net #DEFAULT NAME
else
	export NET_NAME=$1
fi

export SUB_NET=145.100.0.0/16
export IP_RANGE=145.100.2.0/24 # 145.0.1.N -> UNIQUE FOR LOG PARSERS.

export EXISTS=$(docker network ls --filter="label=LP_NET" | sed -sn 2p | awk '{ print $2 }')
# echo $EXISTS

if [ "$EXISTS" = "$NET_NAME" ]
then
	echo "NETOWKR EXISTS"
else
	echo "NETWORK DOESN'T EXISTS, CREATING NETWOEK $NET_NAME"
	# Create ad network if doesn't exists
	docker network create $NET_NAME --label "LP_NET=LOG_PARSING_NETWORK"  --subnet=$SUB_NET --ip-range=$IP_RANGE
fi

export BASE_IMAGE=localhost:5000/djandr/log_parser:latest
# Launch all containers
# Connect all to anomaly detection network(ad_net)
export DEFAULT_PORT=40001
export SHARED_VOLUME=shared_volume
export DOCKER_VOLUME_MAP=/data/ # Where on the container will the SHARED_VOLUME will map.

# PARSER USES 2 VOLUMES:
#	1. UNSTRUCTURED LOGS DATA SOURCE(This should not be needed, extractor should allocate on the same volume the unstructured logs and the anomaly labels file)
#	2. OUTPUT VOLUME FOR STRUCTURED LOGS.

for (( i=1; i<6; i++))
do
	export PORT=4000$i
	echo "Launching container lp$i on port $PORT"
	# docker container run --name ad$i -l AD_CID=AD$i -p $PORT:$DEFAULT_PORT -v $SHARED_VOLUME:$DOCKER_VOLUME_MAP --net ad_net -d -e PAXOS_ROLE=1 $BASE_IMAGE
	docker container run --name lp$i -l LP_CID=LP$i -p $PORT:$DEFAULT_PORT  -v  shared_volume:/logparser/data/ --net $NET_NAME -d -e PAXOS_ROLE=1 $BASE_IMAGE

done

echo "Containers launched: "
docker container ps --filter="label=LP_CID" --format="table {{.Names}} \t\t {{.Status}} \t\t {{.Ports}}"
