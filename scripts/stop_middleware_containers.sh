docker container stop $(docker ps -q --filter="label=MW_CID")
docker container prune -f
