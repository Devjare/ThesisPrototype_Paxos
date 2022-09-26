# PCA Anomaly Detector Containerized with REST.

PCA Algorithm for anomaly detection from: [Logpai/loglizer](https://github.com/logpai/loglizer)

#### Build image from anomaly\_detector/ dir:

```
docker image build -t djandr/anomaly_detector:v3 .
```

#### Run container for the first time:

```
docker container run --name anomaly_detector -v shared_logs:/data/ djandr/anomaly_detector:v3 
```

Requests can be made executing "detector\_request.sh".
Change IP for localhost if running locally, or set the ip defined on container.
