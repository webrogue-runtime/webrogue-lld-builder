
set -ex

LIBC=$1
ARCH=$2
IMAGE_NAME=webrogue/webrogue-lld-$ARCH-$LIBC-builder
CONTAINER_NAME=temp_container_name_$ARCH_$LIBC

docker build \
    --tag $IMAGE_NAME \
    --build-arg ARCH=$ARCH \
    --platform linux/$ARCH \
    --file $LIBC.Dockerfile \
    .

docker create --name $CONTAINER_NAME $IMAGE_NAME
docker cp $CONTAINER_NAME:/app/out out
docker rm $CONTAINER_NAME
