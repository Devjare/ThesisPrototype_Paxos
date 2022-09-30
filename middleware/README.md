# Middleare

The function of the middleware is to manage requests from users.
It is specified to be connected to both, log parsing network(lp\_net), and anomaly detection network(ad\_net).
But only some of the middelwares containers are connected to those, so not all middlewares are capable
of requesting parsing or anomaly detection from those containers.

In order to achieve a complete availability in terms of request management, a consensus algorithm(paxos) is implemented
to make a consensus based on which middleware is able to reache a container which can provide the requested service.

Some functions are implemented to achieve the consensus:

- **scan_network()** scan\_network searches for all the ips available on network and returns the ones that are up.
	this fucntion is used only to detect whichc middleware containers are availble to further identify the ones
	able to realize the requested service(parsing or detection).
- **multi_ping().** Multi ping funciont makes a ping to a range of IPs on a network of the requested service, this is
	done in order to find out which ip of the service(parsing or detection) network is available. To further
	determine wether such ip is able to do the servcie(can_parse, can_detect functions). scan_network does not
	work with ips on different networks altough in theory the middleware calling this function is also on the
	service network, but for some reason it does not work.
