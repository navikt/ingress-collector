
sed  's/127.0.0.1/host.docker.internal/g' ${KUBECONFIG} > ./tmp/KUBECONFIG.yml
docker-compose up -d --remove-orphans --build
