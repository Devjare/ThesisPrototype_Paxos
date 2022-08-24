docker container stop $(docker ps -q --filter="label=AD_CID")
docker container stop $(docker ps -q --filter="label=LP_CID")
docker container stop $(docker ps -q --filter="label=MW_CID")

docker container rm $(docker ps -qa --filter="label=AD_CID")
docker container rm $(docker ps -qa --filter="label=LP_CID")
docker container rm $(docker ps -qa --filter="label=MW_CID")
