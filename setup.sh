echo "Setup Kubernetes cluster..."

echo "Create 'ml-application-namespace'..."
kubectl create namespace ml-application-namespace

echo "Create resources from 'application.yaml'"
kubectl create -f application.yaml --namespace=ml-application-namespace

echo "Get resources: "
kubectl get all --namespace=ml-application-namespace

echo "Ingress is: "
kubectl get ingress --namespace=ml-application-namespace

echo "Waiting resources up..."
sleep 35

echo "Get resources: "
kubectl get all --namespace=ml-application-namespace

echo "Checking readiness endpoint: "
curl -i  http://localhost:80/readiness