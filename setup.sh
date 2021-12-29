echo "Setup Kubernetes cluster..."

echo "Create 'ml-sentiment-namespace'..."
kubectl create namespace ml-sentiment-namespace

echo "Create resources from 'application.yaml'"
kubectl create -f application.yaml --namespace=ml-sentiment-namespace

echo "Created resources: "
kubectl get all --namespace=ml-sentiment-namespace

echo "Ingress is: "
kubectl get ingress

echo "Waiting resources up..."
sleep 35

echo "Created resources: "
kubectl get all --namespace=ml-sentiment-namespace

echo "Checking readiness endpoint: "
curl -i  http://localhost:80/readiness