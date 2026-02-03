
set -ex

IMAGE_NAME=webrogue/webrogue-lld-builder
CONTAINER_NAME=temp_container_name
docker build --tag $IMAGE_NAME .
docker create --name $CONTAINER_NAME $IMAGE_NAME
docker cp $CONTAINER_NAME:/app/out out
docker rm $CONTAINER_NAME
