
set -ex

IMAGE_NAME=webrogue/webrogue-lld-builder
docker build --tag $IMAGE_NAME .
docker run --rm -t --entrypoint cat $IMAGE_NAME /app/out >out
