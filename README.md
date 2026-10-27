# k8s-service-lab

A tiny web app deployed as 3 Kubernetes replicas behind a NodePort Service, showing round-robin load balancing: each pod answers with its own name.

## Run

Build the image and apply the manifests (works with minikube, kind, or any cluster):

```bash
docker build -t hello-web:latest .

kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl rollout status deployment/hello-web
```

Then send requests and count which pod answered:

```bash
./demo.sh http://localhost:30080 30
```

You should see the requests spread across all three pod names.

With minikube, get the URL first: `minikube service hello-web --url`.

## Local test (no cluster)

```bash
pip install -r requirements.txt
pytest            # run the smoke tests
python app.py     # serve on http://localhost:8080
```
