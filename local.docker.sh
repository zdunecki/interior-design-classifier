function build() {
  docker build -f train.local.dockerfile \
  -t registry.gitlab.com/topifyresearch/interior-design-mnist \
  --build-arg SSH_PRIVATE_KEY="$(cat ~/.ssh/id_rsa)" \
  --build-arg SSH_PUB_KEY="$(cat ~/.ssh/id_rsa.pub)" \
  .
}

function train() {
  docker run \
  -e IMAGE_WIDTH=150 \
  -e IMAGE_HEIGHT=150 \
  -e MODEL_OUTPUT="./output/model.json" \
  -e WEIGHTS_OUTPUT="./output/weights.h5" \
  -e BATCH_SIZE=1 \
  -v "$PWD"/data/test:/app/data \
  -v "$PWD"/output:/app/output \
  registry.gitlab.com/topifyresearch/interior-design-mnist
}

$1

# usage: sh local.docker.sh <function_name>