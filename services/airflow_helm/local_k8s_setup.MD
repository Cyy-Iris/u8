# k8s set up
### - create cluster - ###
kind create cluster --name airflow-cluster --image kindest/node:v1.21.1 


### - add airflow helm stable repo - ###
```bash
helm repo add apache-airflow https://airflow.apache.org
helm repo update
```

### - Create namespace - ###
```bash
kubectl create namespace airflow
```

### - (OPTIONAL) Build extended imgae - ###
```bash
docker build -f services/airflow_helm/docker/Dockerfile -t extended-airflow:0.0.1 . // Remove the airflow in pyproject.toml as James did
kind load docker-image extended-airflow:0.0.1 --name airflow-cluster
```

### - Populate the value.yaml file with your image  - ###
Go to `ops/values.yaml`, change values below
```bash
defaultAirflowRepository: <your extended image>
defaultAirflowTag: <your tag>
```

### - Set up ssh key to connect to your dag repo - ###
Create SSH key, paste the public key in your **private** git repo of DAGs

Go to `ops/values.yaml`, populate with your own git repo
```bash
  gitSync:
    enabled: true

    # git repo clone url
    # ssh example: git@github.com:apache/airflow.git
    # https example: https://github.com/apache/airflow.git
    repo: https://github.com/<your git repo>
    branch: main
    rev: HEAD
    depth: 1
    # the number of consecutive failures allowed before aborting
    maxFailures: 0
    # subpath within the repo where dags are located
    # should be "" if dags are at repo root
    subPath: ""
```

### - Deploy configMap and secret  - ###
```bash
kubectl apply -f services/airflow_helm/ops/variable.yaml -n airflow
#kubectl create secret generic airflow-ssh-git-secret --from-file=gitSshKey= <your path of ssh private ket> -n airflow
```

### - Install the extended chart - ###
```bash
helm upgrade --install extended-airflow apache-airflow/airflow -f services/airflow_helm/ops/values.yaml --namespace airflow --debug
```

### - Port forward for airflow UI - ###
Your should see some output as below:

```bash
You can now access your dashboard(s) by executing the following command(s) and visiting the corresponding port at localhost in your browser:

Airflow Webserver:  kubectl port-forward svc/extended-airflow-webserver 8080:8080 --namespace airflow
Default Webserver (Airflow UI) Login credentials:
    username: admin
    password: admin
Default Postgres connection credentials:
    username: postgres
    password: postgres
    port: 5432
```

Forward the port:
```bash
kubectl port-forward svc/extended-airflow-webserver 8080:8080 --namespace airflow
```

