echo "Delete K8S resources within namespace 'ml-sentiment-namespace'..."
kubectl delete namespaces ml-sentiment-namespace
kubectl delete pv ml-sentiment-pv-storage
kubectl delete pv ml-sentiment-pv-logs
