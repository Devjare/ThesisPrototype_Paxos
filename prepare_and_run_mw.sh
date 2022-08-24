# DEFINE LATER.
# 70801, 708... -> for request to middleware
# 50801, 508... -> for request to parsers
# 30801, 308... -> for request to Anomaly detectors

# SET ENV VARS NEEDED.

# FOR LOCAL RUN
# export LP_IP_RANGE="172.22.0.2-172.22.0.6"
# export LP_PORT_RANGE="50022-50026"


# FOR CONTAINERIZED RUN
export IPLOCAL="192.168.1.37"
export LP_IP_RANGE="172.22.0.2-172.22.0.6"
export LP_PORT_RANGE="50022-50026"

export AD_IP_RANGE="172.21.0.2-172.21.0.6"
export AD_PORT_RANGE="5052-5056"

python ./middleware/main.py

