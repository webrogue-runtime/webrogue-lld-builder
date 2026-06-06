
set -ex

ARCH=$1
IMAGE_NAME=webrogue/webrogue-lld-$ARCH-builder
CONTAINER_NAME=temp_container_name_$ARCH

docker build \
    --tag $IMAGE_NAME \
    --build-arg ARCH=$ARCH \
    --platform linux/$ARCH \
    .

docker create --name $CONTAINER_NAME $IMAGE_NAME
docker cp $CONTAINER_NAME:/app/out out
docker rm $CONTAINER_NAME
