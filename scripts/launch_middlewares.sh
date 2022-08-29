# ANONALY DETECTION. # default name ad_net
if [ $# -eq 0 ]
then
	export NET_NAME=mw_net #DEFAULT NAME
else
	export NET_NAME=$1
fi

export SUB_NET=147.100.0.0/16
export IP_RANGE=147.100.4.0/24 # 147.0.3.N -> UNIQUE FOR MIDDLEWARE CONTROLLERS.
export EXISTS=$(docker network ls --filter="label=MW_NET" | sed -sn 2p | awk '{ print $2 }')
# echo $EXISTS

if [ "$EXISTS" = "$NET_NAME" ]
then
	echo "NETOWKR EXISTS"
else
	# Create ad network if doesn't exists
	echo "NETWORK DOESN'T EXISTS, CREATING NETWOEK $NET_NAME"
	docker network create $NET_NAME --label "MW_NET=MIDDLEWARE_NETWORK" --subnet=$SUB_NET --ip-range=$IP_RANGE
fi

# PREBUILD MIDDLEWARE IMAGE.
./middleware/buildimage.sh

export BASE_IMAGE=localhost:5000/djandr/middleware
# Launch all containers
# Connect all to anomaly detection network(mw_net)
export DEFAULT_PORT=60001

echo "Launching PROPOSER CONTAINER on PORT 60002"
docker container run --name mw1 -l MW_CID=MW1 -p 60002:$DEFAULT_PORT --net $NET_NAME -d --env-file ./scripts/proposer.env $BASE_IMAGE

echo "Launching LEARNER 1 CONTAINER on PORT 60003"
docker container run --name mw2 -l MW_CID=MW2 -p 60003:$DEFAULT_PORT --net $NET_NAME -d  --env-file ./scripts/learner.env $BASE_IMAGE
echo "Launching LEARNER 2 CONTAINER on PORT 60004"                                      
docker container run --name mw3 -l MW_CID=MW3 -p 60004:$DEFAULT_PORT --net $NET_NAME -d --env-file ./scripts/learner.env $BASE_IMAGE

echo "Launching ACCEPTOR CONTAINER on PORT 60005"
docker container create --name mw4 -l MW_CID=MW4 -p 60005:$DEFAULT_PORT --net $NET_NAME --env-file  ./scripts/acceptor.env $BASE_IMAGE
# After created, connect to second network
docker network connect lp_net mw4
# Start contaienr
docker container start mw4

echo "Launching ACCEPTOR CONTAINER on PORT 60006"
docker container create --name mw5 -l MW_CID=MW5 -p 60006:$DEFAULT_PORT --net $NET_NAME --env-file  ./scripts/acceptor.env $BASE_IMAGE
# After created, connect to second network
docker network connect lp_net mw5
# Start contaienr
docker container start mw5

echo "Launching ACCEPTOR CONTAINER on PORT 60006"
docker container create --name mw6 -l MW_CID=MW6 -p 60007:$DEFAULT_PORT --net $NET_NAME --env-file  ./scripts/acceptor.env $BASE_IMAGE
# After created, connect to second network
docker network connect ad_net mw6
# Start contaienr
docker container start mw6


echo "Launching ACCEPTOR CONTAINER on PORT 60006"
docker container create --name mw7 -l MW_CID=MW7 -p 60008:$DEFAULT_PORT --net $NET_NAME --env-file  ./scripts/acceptor.env $BASE_IMAGE
# After created, connect to second networ
docker network connect ad_net mw7
# Start contaienr
docker container start mw7

echo "Containers launched: "
docker container ps --filter="label=MW_CID" --format="table {{.Names}} \t\t {{.Status}} \t\t {{.Ports}}"
