./parser/buildimage.sh
./scripts/launch_parsers.sh lp_net

./anomaly_detector/buildimage.sh
./scripts/launch_detectors.sh ad_net

./middleware/buildimage.sh
./scripts/launch_middlewares.sh mw_net
