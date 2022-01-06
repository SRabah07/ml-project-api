if [ -z "$1" ]
  then
    echo "If you are running K8S using Minikube, restart this script by providing 'minikube' as argument. Otherwise we suppose you are using Desktop Docker to enable K8S"
    INGRESS_IP='localhost'
elif [ "$1" = "minikube" ]
  then
    echo "You are using Minikube."
    minikube addons enable ingress
    INGRESS_IP=`minikube ip`
fi


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

echo "Mount Storage, used by PV under hostPath"
minikube mount ./storage/models:/storage/models &

echo "Checking readiness endpoint: "
curl -i  http://$INGRESS_IP:80/readiness

echo "Ingress is listing on Address: http://$INGRESS_IP:80/."
