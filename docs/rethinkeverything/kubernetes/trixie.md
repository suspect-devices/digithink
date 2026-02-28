
# Rinse Lather Repeat. K8s on trixie.

Found a decent example of how to run up kubernetes by someone else trying to get a CKA.

https://max-pfeiffer.github.io/installing-kubernetes-on-debian-13-trixie.html

Unfortunately there was a little piece missing  '--set cni.binPath=/usr/lib/cni' which pretty much meant reinstalling everything about 4 times. On the third iteration I started seeing the point of getting cloud-init (or ansible, or puppet) involved in the bass systems.

## Attempt #1/2 (do it by hand and then batch a bunch)

```sh
incus init trixie-vm-cloud -c limits.cpu=6 -c limits.memory=12GiB -d root,size=24GiB --vm gru -p default -p merlot   -c cloud-init.network-config="$(cat <<EOF
version: 2
ethernets:
  enp5s0:
    addresses:
      - 192.168.129.130/17
    gateway4: 192.168.128.1
    nameservers:
      addresses:
        - 192.168.128.1
EOF
)"
incus start gru --console
incus init trixie-vm-cloud -c limits.cpu=6 -c limits.memory=12GiB -d root,size=24GiB --vm minion1 -p default -p merlot   -c cloud-init.network-config="$(cat <<EOF
version: 2
ethernets:
  enp5s0:
    addresses:
      - 192.168.129.131/17
    gateway4: 192.168.128.1
    nameservers:
      addresses:
        - 192.168.128.1
EOF
)"
incus start minion1
incus init trixie-vm-cloud -c limits.cpu=6 -c limits.memory=12GiB -d root,size=24GiB --vm minion2 -p default -p merlot   -c cloud-init.network-config="$(cat <<EOF
version: 2
ethernets:
  enp5s0:
    addresses:
      - 192.168.129.132/17
    gateway4: 192.168.128.1
    nameservers:
      addresses:
        - 192.168.128.1
EOF
)"
incus init trixie-vm-cloud -c limits.cpu=6 -c limits.memory=12GiB -d root,size=24GiB --vm minion3 -p default -p merlot   -c cloud-init.network-config="$(cat <<EOF
version: 2
ethernets:
  enp5s0:
    addresses:
      - 192.168.129.133/17
    gateway4: 192.168.128.1
    nameservers:
      addresses:
        - 192.168.128.1
EOF
)"
for h in gru minion1 minion2 minion3 ; do echo $h; done
for h in gru minion1 minion2 minion3 ; do incus exec $h -- modprobe overlay; done
for h in gru minion1 minion2 minion3 ; do incus exec $h -- modprobe overlay; done
for h in gru minion1 minion2 minion3 ; do incus exec $h -- modprobe br-netfilter; done
cat <<EOF | tee k8s.sysctl.d.conf
net.ipv4.ip_forward = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF
for h in gru minion1 minion2 minion3 ; do incus file push k8s.sysctl.d.conf $h/etc/sysctl.d/k8s.conf; done
for h in gru minion1 minion2 minion3 ; do incus exec $h -- sysctl --system; done
for h in gru minion1 minion2 minion3 ; do incus exec $h -- apt update; done
; done
for h in gru minion1 minion2 minion3 ; do incus exec $h -- install -m 0755 -d /etc/apt/keyrings; done
for h in gru minion1 minion2 minion3 ; do incus exec $h -- curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc; ; done
for h in gru minion1 minion2 minion3 ; do incus exec $h -- curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc; done
for h in gru minion1 minion2 minion3 ; do incus exec $h -- chmod a+r /etc/apt/keyrings/docker.asc; done
for h in gru minion1 minion2 minion3 ; do incus file push /etc/apt/sources.list.d/docker.list $h/etc/apt/sources.list.d/docker.list; done
for h in gru minion1 minion2 minion3 ; do incus exec $h -- apt update; done
for h in gru minion1 minion2 minion3 ; do incus exec $h -- apt install containerd.io; done
containerd config default | tee config.toml
sed -e 's/SystemdCgroup = false/SystemdCgroup = true/g' -i config.toml
apt install containerd
nano /etc/resolv.conf 
apt install containerd
containerd config default | tee config.toml
sed -e 's/SystemdCgroup = false/SystemdCgroup = true/g' -i config.toml
for h in gru minion1 minion2 minion3 ; do incus file push config.toml $h/etc/containerd/config.toml; done
for h in gru minion1 minion2 minion3 ; do incus exec $h -- systemctl restart containerd && systemctl status containerd; done
curl -fsSL https://packages.buildkite.com/helm-linux/helm-debian/gpgkey | gpg --dearmor | tee helm.gpg > /dev/null
for h in gru minion1 minion2 minion3 ; do incus file push helm.gpg $h/usr/share/keyrings/helm.gpg; done
echo "deb [signed-by=/usr/share/keyrings/helm.gpg] https://packages.buildkite.com/helm-linux/helm-debian/any/ any main" | sudo tee helm-stable-debian.list
for h in gru minion1 minion2 minion3 ; do incus file push helm.gpg $h/etc/apt/sources.list.d/helm-stable-debian.list; done
for h in gru minion1 minion2 minion3 minion4; do incus file push helm-stable-debian.list $h/etc/apt/sources.list.d/helm-stable-debian.list; done
for h in gru minion1 minion2 minion3 minion4; do incus exec $h -- apt update && apt install helm; done
incus shell gru
for h in gru minion1 minion2 minion3 minion4; do incus exec $h -- apt install helm; done
ls
mkdir cka
mv config.toml helm* cka/
cd cka
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.33/deb/Release.key | gpg --dearmor -o kubernetes-apt-keyring.gpg
for h in gru minion1 minion2 minion3 minion4; do incus file push kubernetes-apt-keyring.gpg $h/etc/apt/keyrings/kubernetes-apt-keyring.gpg; done
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.33/deb/ /'|tee kubernetes.list
for h in gru minion1 minion2 minion3 minion4; do incus file push kubernetes.list $h/etc/apt/sources.list.d/kubernetes.list; done
for h in gru minion1 minion2 minion3 minion4; do incus exec $h -- apt update; done
for h in gru minion1 minion2 minion3 minion4; do incus exec $h -- apt dist-upgrade; done
for h in gru minion1 minion2 minion3 minion4; do incus exec $h -- apt dist-upgrade -y; done
for h in gru minion1 minion2 minion3 minion4; do incus exec $h -- apt install -y kubeadm=1.33.5-1.1 kubelet=1.33.5-1.1 kubectl=1.33.5-1.1; done
for h in gru minion1 minion2 minion3 minion4; do incus exec $h -- apt-mark hold kubelet kubeadm kubectl; done
cat <<EOF | sudo tee k8s.conf 
overlay
br_netfilter
EOF
ls
for h in gru minion1 minion2 minion3 minion4; do incus file push k8s.conf $h/etc/sysctl.d/k8s.conf; done
cat <<EOF | tee k8s.sysctl.conf
net.ipv4.ip_forward = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF
for h in gru minion1 minion2 minion3 minion4; do incus exec $h -- kubeadm config images list; done
incus file pull gru/etc/containerd/config.toml
incus file pull gru/etc/containerd/config.toml .
nano config.toml 
for h in gru minion1 minion2 minion3 minion4; do incus file push config.toml $h/etc/containerd/config.toml; done
for h in gru minion1 minion2 minion3 minion4; do incus exec $h -- systemctl restart containerd; done
top
cat /etc/hosts
incus shell minion1
incus shell minion2
incus shell minion3
incus shell minion4
for h in gru minion1 minion2 minion3 minion4; do incus file push k8s.conf $h/etc/sysctl.d/k8s.conf; done
for h in gru minion1 minion2 minion3 minion4; do incus file push /etc/apt/sources.list.d/docker.list $h/etc/apt/sources.list.d/docker.list; done
```
## Attempt #3/4 

### take the boring parts and make cloud init do the work.


### also the key point.

```sh
kubeadm init --kubernetes-version 1.33.5 --control-plane-endpoint gru
export KUBECONFIG=/etc/kubernetes/admin.conf
helm install cilium cilium/cilium --version 1.18.3 --namespace kube-system  --set cni.binPath=/usr/lib/cni
```

### Make it work at the colo.

```sh
incus init trixie-vm -c limits.cpu=16 -c limits.memory=24GiB -d root,size=24GiB --vm gru -p default -p k8s-colo -c cloud-init.network-config="$(cat <<EOF
version: 2
ethernets:
  enp5s0:
    addresses:
      - 69.41.138.117/27
    gateway4: 69.41.138.97
    nameservers:
      addresses:
        - 69.41.138.98
        - 8.8.4.4
EOF
)"
incus start gru
```

Initialize the control plane

```sh
kubeadm init --kubernetes-version 1.33.5 --control-plane-endpoint gru
export KUBECONFIG=/etc/kubernetes/admin.conf
helm install cilium cilium/cilium --version 1.18.3 --namespace kube-system  --set cni.binPath=/usr/lib/cni
```

Set up the nodes

```sh
incus init trixie-vm -c limits.cpu=16 -c limits.memory=24GiB -d root,size=24GiB --vm minion1 -p default -p k8s-colo -c cloud-init.network-config="$(cat <<EOF
version: 2
ethernets:
  enp5s0:
    addresses:
      - 69.41.138.118/27
    gateway4: 69.41.138.97
    nameservers:
      addresses:
        - 69.41.138.98
        - 8.8.4.4
EOF
)"
incus start minion1

incus init trixie-vm -c limits.cpu=16 -c limits.memory=24GiB -d root,size=24GiB --vm minion2 -p default -p k8s-colo -c cloud-init.network-config="$(cat <<EOF
version: 2
ethernets:
  enp5s0:
    addresses:
      - 69.41.138.119/27
    gateway4: 69.41.138.97
    nameservers:
      addresses:
        - 69.41.138.98
        - 8.8.4.4
EOF
)"
incus start minion2

incus init trixie-vm -c limits.cpu=16 -c limits.memory=24GiB -d root,size=24GiB --vm minion3 -p default -p k8s-colo -c cloud-init.network-config="$(cat <<EOF
version: 2
ethernets:
  enp5s0:
    addresses:
      - 69.41.138.120/27
    gateway4: 69.41.138.97
    nameservers:
      addresses:
        - 69.41.138.98
        - 8.8.4.4
EOF
)"
incus start minion3
```

## references

- <https://discuss.linuxcontainers.org/t/how-to-use-cloud-init-to-set-up-a-vm-or-container-static-ip/22075/2>
- <https://forum.linuxfoundation.org/discussion/869484/issue-with-coredns-pods-after-initial-cluster-setup>
- <https://max-pfeiffer.github.io/installing-kubernetes-on-debian-13-trixie.html>