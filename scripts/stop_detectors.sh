docker container stop $(docker ps -q --filter="label=AD_CID")
docker container prune -f
