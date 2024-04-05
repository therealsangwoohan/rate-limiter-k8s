DEPLOY FROM SCRATCH

1) Build image for linux/amd64 and push it to Docker Hub.

docker buildx build --platform linux/amd64 -t therealsangwoohan/rate-limiter:0.0.0 --push .

2) Create rate-limiter-deployment

kubectl create -f kubernetes-manifests/rate-limiter-deployment.yaml

3) Create rate-limiter-service

kubectl create -f kubernetes-manifests/rate-limiter-service.yaml

4) Get the external ip and the port

kubectl get services