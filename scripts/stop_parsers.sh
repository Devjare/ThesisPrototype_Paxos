docker container stop $(docker ps -q --filter="label=LP_CID")
docker container prune -f
