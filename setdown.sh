echo "Delete K8S resources within namespace 'ml-application-namespace'..."
kubectl delete namespaces ml-application-namespace

echo "Delete PV, PVC"
kubectl delete persistentvolume ml-project-pv-storage
kubectl delete persistentvolumeclaims ml-project-pvc-storage