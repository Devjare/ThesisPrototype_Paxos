# ANONALY DETECTION. # default name ad_net
if [ $# -eq 0 ]
then
	export NET_NAME=ad_net #DEFAULT NAME
else
	export NET_NAME=$1
fi

export SUB_NET=146.100.0.0/16
export IP_RANGE=146.100.3.0/24 # 146.0.2.N -> UNIQUE FOR ANOMALY DETECTORS.

export EXISTS=$(docker network ls --filter="label=AD_NET" | sed -sn 2p | awk '{ print $2 }')
# echo $EXISTS

if [ "$EXISTS" = "$NET_NAME" ]
then
	echo "NETOWKR EXISTS"
else
	# Create ad network if doesn't exists
	echo "NETWORK DOESN'T EXISTS, CREATING NETWOEK $NET_NAME"
	docker network create $NET_NAME --label "AD_NET=ANOMALY_DETECTION_NETWORK"  --subnet=$SUB_NET --ip-range=$IP_RANGE
fi


export BASE_IMAGE=localhost:5000/djandr/anomaly_detector:latest
# Launch all containers
# Connect all to anomaly detection network(ad_net)
export DEFAULT_PORT=50001
export SHARED_VOLUME=shared_volume
export DOCKER_VOLUME_MAP=/data/ # Where on the container will the SHARED_VOLUME will map.
for (( i=2; i<=6; i++))
do
	export PORT=5000$i
	echo "Launching container ad$i on port $PORT"
	docker container run --name ad$i -l AD_CID=AD$i -p $PORT:$DEFAULT_PORT -v $SHARED_VOLUME:$DOCKER_VOLUME_MAP --net $NET_NAME -d -e PAXOS_ROLE=1 $BASE_IMAGE
done

echo "Containers launched: "
docker container ps --filter="label=AD_CID" --format="table {{.Names}} \t\t {{.Status}} \t\t {{.Ports}}"
