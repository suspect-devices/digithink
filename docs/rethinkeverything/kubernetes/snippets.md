# sort pile.

## Fucking dumbest thing ever. So not impressed with the Linux Foundation here

translating this pile of shit in the middle of a pdf...

```sh
kubectl -n kube-system exec -it etcd-gru -- sh "ETCDCTL_API=3 ETCDCTL_CACERT=/etc/kubernetes/pki/etcd/ca.crt ETCDCTL_CERT=/etc/kubernetes/pki/etcd/server.crt ETCDCTL_KEY=/etc/kubernetes/pki/etcd/server.key etcdctl endpoint health"
# convoluted un pasteable and dumb. Try this.

export ETCDCTL_API=3
export ETCDCTL_CACERT=/etc/kubernetes/pki/etcd/ca.crt
export ETCDCTL_CERT=/etc/kubernetes/pki/etcd/server.crt
export ETCDCTL_KEY=/etc/kubernetes/pki/etcd/server.key
etcdctl endpoint health
```

On the control-plane node.

```sh
etcdctl snapshot save /var/lib/etcd/snapshot.db
mkdir $HOME/backup
cp /var/lib/etcd/snapshot.db $HOME/backup/snapshot.db-$(date +%m-%d-%y) 
#cp /root/kubeadm-config.yaml $HOME/backup/
# Source - https://stackoverflow.com/a/61023372
# Posted by Arghya Sadhu
# Retrieved 2026-03-06, License - CC BY-SA 4.0
kubectl get cm kubeadm-config  -n kube-system -o yaml > $HOME/backup/kubeadm-config.yaml
cp -r /etc/kubernetes/pki/etcd $HOME/backup/
```

```sh
feurig@pj ~ % kubectl drain minion1 --ignore-daemonsets
node/minion1 cordoned
```

```sh
sudo apt-mark unhold kubeadm
sed -i 's/33/34/g' /etc/apt/sources.list.d/kubernetes.list
apt update
apt-cache madison kubeadm
apt install kubeadm=1.34.1-1.1 -y
sudo apt-get update && sudo apt-get install -y kubeadm=1.34.2-1.1
sudo apt-mark hold kubeadm
kubeadm upgrade node
apt-mark unhold kubelet kubectl
apt-get install -y kubelet=1.34.1-1.1 kubectl=1.34.1-1.1
apt-mark hold kubelet kubectl
sudo systemctl daemon-reload
systemctl restart kubelet
```

```
