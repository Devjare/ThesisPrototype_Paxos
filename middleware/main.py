from flask import Flask, request
import json
import os
import random
import requests
import socket

app = Flask(__name__)
    
MY_ROLE = os.getenv("PAXOS_ROLE") # 'P' | 'A' | 'L' 
REQ_ID = int(os.getenv("CURRENT_REQ_ID"))

@app.route("/")
def home():
    return "<h5>Middleware Home!</h5>"

def get_ip(start, end):
    start_sections = start.split(".")
    start_ip_last_number = int(start_sections[-1])
    
    end_sections = end.split(".")
    end_ip_last_number = int(end_sections[-1])

    # Last number selection
    ip_id = random.randint(start_ip_last_number, end_ip_last_number)
   
    ip_array = start_sections[:3]
    ip_array.append(str(ip_id))
    selected_ip = '.'.join(ip_array)
    
    print("Selected ip: ", selected_ip)
    
    return selected_ip

def get_port(start, end):
    int_start = int(start)
    int_end = int(end)

    port = random.randint(int_start, int_end)

    print("Selected Port: ", port)
    return port

@app.route("/my_role")
def get_role():
    return { 'my_role': os.getenv("PAXOS_ROLE") }

def get_acceptors(connected):
    acceptors = []
    for ip in connected:
        url = f"http://{ip}/my_role"
        app.logger.info(f"Making request to: {url}")
        req = requests.get(url)
        response = req.json()
    
        if(response):
            app.logger.info(f"\tRequest response: {response}")
            role = response['my_role'] 
            if(role == 'A'):
                acceptors.append(ip)

    return acceptors

@app.route("/promise")
def promise():
    # IF IM A PROPOSER, MY INTEREST IS TO SEND PROMISE REQUEST.
    if MY_ROLE == "P":
        app.logger.info('PROPOSER Promise Request')
        # ONLY A PROPOSER HAS AN IP LIST DEFINED AS ENV VARIABLE.
        # FUTURE WORK: IP_LIST NOT DEFINED ON ENV, BUT DISCOVER IPS ON NET.
        connected = os.getenv("IP_LIST").split(",")
        app.logger.info(f"Connected ips: {connected}")
        # Get acceptors list.
        acceptors = get_acceptors(connected)

        # Comma separated ips of acceptors on MW_NET.
        # acceptors = os.getenv("ACCEPTORS").split(",")

        app.logger.info(f"ACCEPTORS list: {acceptors}")
        for acceptor in acceptors:
            # process -> Which process to be done(Parser or AD), 
            # ip -> who is going to do that process.
            newValue = os.getenv("VALUE_TO_PROMISE")

            app.logger.info(f"PROPOSER Promise Request to acceptor with ip:port = {acceptor}")
            url = f"http://{acceptor}/promise?newValue={newValue}&reqId={REQ_ID}" # Send a promise to all acceptors.
            app.logger.info(f"Making a request to: {url}")
            req = requests.get(url)
            app.logger.info('Request response: %s!', req.text)
            response = req.json()

        return "Promise request sent."

    if MY_ROLE == "A":
        app.logger.info("Acceptor request obtained!")
        # LAST_ACCEPTED value from LAST_REQ_FROM
        newValue = request.args.get("newValue") # newValue to accept.
        process = newValue.split("=")[0] # Which process
        ip = newValue.split("=")[1] # To be donde by which ip
        reqId = int(request.args.get("reqId")) # Request ID, accept only from the greater.
        
        currentReqId = int(os.getenv("CURRENT_REQ_ID")) # ID of last promise to accept.
        if(reqId >= currentReqId):
            # Accept
            # SAVE NEW VALUE AS PROMISED TO ACCEPT LATER ON A ACCEPT REQUEST.
            os.environ[f"PROMISE_{process}_IP"] = str(ip)
            return { 'promised': True }

        return { 'promised_ph': False }
    # if MY_ROLE == "L" theorically would neve enter this method

@app.route("/accept")
def accept():
    if MY_ROLE == "P":
        connected = os.getenv("IP_LIST").split(",")
        
        # Get acceptors list.
        acceptors = get_acceptors(connected)
        
        majority = len(acceptors) / 2 + 1
        # acceptor -> ip:port
        
        process_ip = os.getenv("VALUE_TO_ACCEPT")
        # send acceptors nevalue to accept. 
        for acceptor in acceptors:
            url = f"http://{acceptor}/accept?newValue={process_ip}&reqId={REQ_ID}"
            req = requests.get(url)
            response = req.json()
        
            if(response['accepted'] == True):
                majority -= 1

        if(majority <= 0):
            # enough to commit.
            return { 'majorityAccepted': True, 'majority': majority }
 
    if(MY_ROLE == "A"):
        app.logger.info("Acceptor request obtained!")
        # LAST_ACCEPTED value from LAST_REQ_FROM
        newValue = request.args.get("newValue") # newValue to accept.
        process = newValue.split("=")[0] # Which process
        ip = newValue.split("=")[1] # To be donde by which ip
        reqId = int(request.args.get("reqId")) # Request ID, accept only from the greater.
        
        currentReqId = int(os.getenv("CURRENT_REQ_ID")) # ID of last promise to accept.
        # If current Request Id is grearer than the new request, then not accept.
        # ADN if promised IP is equal to the newIP. Can be accepted.
        if(reqId >= currentReqId and os.environ[f"PROMISE_{process}_IP"] == str(ip)):
            # Accept
            # ACCEPTED_{process}_IP -> Current accepted value.
            os.environ[f"ACCEPTED_{process}_IP"] = str(ip)
            return { 'accepted': True }

        return { 'accepted': False }


    return "<h5>Accept phase</h5>"
        

@app.route("/commit")
def commit():
    if MY_ROLE == "P":
        app.logger.info('PROPOSER Promise Request')
        connected = os.getenv("IP_LIST").split(",")
        # on commit phase, 
        for c in connected:
            # process -> Which process to be done(Parser or AD), 
            # ip -> who is going to do that process.
            newValue = os.getenv("VALUE_TO_COMMIT")

            app.logger.info(f"PROPOSER Commit Request to all with ip:port = {c}")
            url = f"http://{c}/commit?newValue={newValue}&reqId={REQ_ID}" 
            app.logger.info(f"Making a request to: {url}")
            req = requests.get(url)
            app.logger.info('Request response: %s!', req.text)
            response = req.json()

            if response['state'] == 'success':
                app.logger.info(f"Succesfully commited value: {newValue} on majority of nodes.")
                return { 'state': 'success' }
            else:
                app.logger.error(f"Failed to commit value: {process_ip} on majority of nodes.")
                return { 'state': 'failed' }
    else:
        # Any other role(Acceptor or learner) now will know the value
        app.logger.info("Commit request obtained!")
        newValue = request.args.get("newValue") # newValue to accept.
        process = newValue.split("=")[0] # Which process
        ip = newValue.split("=")[1] # To be donde by which ip

        # Current process ip will tell who is going to realizer 'process', which ip.
        os.environ[f'CURRENT_{process}_IP'] = ip
        
        return { 'state': 'success' }
 
    return { "state": "failed" }


@app.route("/start_paxos")
def start_paxos():
    global REQ_ID, MY_ROLE
    # PHASE 1: PROMISE
    # SEARCH WHICH VALUE TO PROPOSE.
    # In order to do that, launch a request to every IP on table for a wether they can
    # or cannot do Parsing or Anomaly detection.
    # If more than one return a positive answer, choose randomly and pass to promise()
    # as the new proposed value.
    paxos_status = ''
    consensus_achieved = False
    if(MY_ROLE == "P"):
        connected = os.getenv("IP_LIST").split(",")
        
        # PAXOS FOR LOG PARSERS
        can_parse_list = [] # list of middleware that have access to parsers net.
        for c in connected:
            url = f"http://{c}/can_parse"
            app.logger.info(f"Requesting can_parse to {url}.")
            req = requests.get(url)
            app.logger.info(f"Request: {req}.")
            response = req.json()
            app.logger.info(f"Response from {url}: {response}")
            
            chosen_parser = ""
            if(response['canParse'] == True):
                # list of ips that are available for parsing
                parsers_list = response['reachableIps'] 
                # middleware c, has acces to parsers_list ips.
                # can_parse_list.append({ c: parsers_list}) 
                can_parse_list.append(c) 
        
        # Chosen middleware will be value to controll access to parsers.
        chosen_middleware = random.choice(can_parse_list)

        # Send promise
        # Only SEND if ROLE = PROPOSER
        # AnomalyDetection(AD) is going to be done by IP
        value = f"LP={chosen_middleware}"
        os.environ["VALUE_TO_PROMISE"] = value
        promiseResponse = promise() 
        app.logger.info(f"PROMISE RESPONSE: {promiseResponse}")

        # PHASE 2: ACCEPTION
        # Majority Promised, then send accept.
        os.environ["VALUE_TO_ACCEPT"] = value
        acceptResponse = accept()
        if('majorityAccepted' not in acceptResponse):
            app.logger.error(f"Majority of acceptions not achieved on request {REQ_ID}!")
            paxos_status = 'Failed to achieve consensus because of majority not completed!'
            consensus_achieved = False
        else: 
            app.logger.info(f"Majority of acceptions achieved on request {REQ_ID}! Proceeding to commit {value}")
            consensus_achieved = True
            paxos_status = 'Successfully finished!'
            if(acceptResponse['majorityAccepted'] == True):
                # If majority accepted, commit
                # PHASE 3: COMMIT.
                # Send commit.
                os.environ["VALUE_TO_COMMIT"] = value
                commit()
                
                # MAKE PROPOSER KNOWN OF THE CURRENT VALUE.
                process = value.split("=")[0] # Which process
                ip = value.split("=")[1] # To be donde by which ip
                envname = f'CURRENT_{process}_IP'
                os.environ[envname] = ip
                app.logger.info(f"Consensus for {process} determined to be done by {ip}, set on env: {envname}, for role: {MY_ROLE}")
        
        # Update req id for new future requests.
        REQ_ID += 1

        
        # PAXOS FOR ANOMALY DETECTORS
    else:
        # request proposer to start paxos.
        proposer = os.getenv("PROPOSER_IP")
        url = f"http://{proposer}:60001/start_paxos"
        app.logger.info(f"Requesting {proposer}:60001 to /start_paxos.")
        req = requests.get(url)

        return req.response.text # Return text in order to prevent json decoding errors.
        

    return { 'paxos_status': paxos_status,
            'consensus_achieved': consensus_achieved }


@app.route("/process_logs", methods=["POST"])
def process_logs():
    
    print("Processing logs completely!")
    ip = os.getenv("IPLOCAL")
    # PARSER PORT
    LP_IP_RANGE = os.getenv("LP_IP_RANGE").split("-") # PORT RANGE FRO LOG PARSERS(LP) 
    parser_port = 40001 # get_port(LP_PORT_RANGE[0], LP_PORT_RANGE[1])
    parser_url = f"http://{ip}:{parser_port}/parse"

    detector_port = 50001
    detector_url = f"http://{ip}:{detector_port}/detect_anomalies"
    
    print(f"Getting args...")
    payload = request.json
    print(f"Payload: {payload}")
    parser_payload = payload['parserReq']
    detector_payload = payload['detectorReq']

    headers = {'Content-Type': 'application/json'}
    
    print(f"Parsing on URL {parser_url}, and post data: {parser_payload}")
    parser_req = requests.post(parser_url, data=json.dumps(parser_payload), headers=headers)
    parser_response = parser_req.json()
    if(parser_response):
        print("PArser response: ", parser_response) 
        print(f"Detecting anomalies on URL {detector_url}, and post data: {detector_payload}")
        detector_req = requests.post(detector_url, data=json.dumps(detector_payload), headers=headers)
        detector_response = detector_req.json()
        if(detector_response):
            print("Detector response: ", detector_response)

    return "Finished processing logs."


def make_ping(ip):
    response = os.system("ping -c 1 " + ip)
    #and then check the response...
    reachable = False
    if response == 0:
        reachable = True

    return reachable

@app.route("/can_parse")
def can_parse():
    
    reachableIps = []
    LP_IP_RANGE = os.getenv("LP_IP_RANGE").split("-") # IP RANGE FRO LOG PARSERS(LP)
    
    start_sections = LP_IP_RANGE[0].split(".") # Start ip
    # sipln = start_ip_last_number
    sipln = int(start_sections[-1]) # Last number
    
    end_sections = LP_IP_RANGE[1].split(".") # End ip
    # eipln = end_ip_last_number
    eipln = int(end_sections[-1]) # Last number
    
    # network
    subdomain = start_sections[:3]
    reachable_ips = []
    for i in range(sipln, eipln+1):
        ip_array = subdomain.copy()
        ip_array.append(str(i)) # for each ip last number in range, append i.
        selected_ip = '.'.join(ip_array)
        app.logger.info(f"Selected ip: {selected_ip}")
        
        # Make a ping to every ip in order to see if the middleware has access to any of the
        # containers capable of parsing.
        is_reachable = make_ping(selected_ip)
        
        if(is_reachable == True):
            # if selected ip from range is reachable, then is possible to make a request
            # to such ip for log parsing.
            reachable_ips.append(selected_ip)
    
    if(len(reachable_ips) == 0):
        return { "canParse": False, 'reachableIps': [] }
    
    # Return which ips are available for parsing.
    return { 'canParse': True, 'reachableIps': reachable_ips }

@app.route("/can_detect")
def can_detect():
    reachableIps = []
    AD_IP_RANGE = os.getenv("AD_IP_RANGE").split("-") # IP RANGE FOR ANOMALY DETECTORS(AD)
    
    start_sections = AD_IP_RANGE[0].split(".") # Start ip
    # sipln = start_ip_last_number
    sipln = int(start_sections[-1]) # Last number
    
    end_sections = AD_IP_RANGE[1].split(".") # End ip
    # eipln = end_ip_last_number
    eipln = int(end_sections[-1]) # Last number
    
    # network
    subdomain = start_sections[:3]
    reachable_ips = 0
    for i in range(sipln, eipln+1):
        ip_array = subdomain.copy()
        ip_array.append(str(i)) # for each ip last number in range, append i.
        selected_ip = '.'.join(ip_array)
        app.logger.info("Selected ip: ", selected_ip)
        
        # Make a ping to every ip in order to see if the middleware has access to any of the
        # containers capable of parsing.
        is_reachable = make_ping(selected_ip)
        
        if(is_reachable == True):
            # if selected ip from range is reachable, then is possible to make a request
            # to such ip for log parsing.
            reachable_ips.append(selected_ip)
    
    if(len(reachable_ips) == 0):
        return { "canDetect": False, 'reachableIps': [] }
    
    # Return which ips are available for anomaly detection.
    return { 'canDetect': True, 'reachableIps': reachable_ips }

def request_parsing(payload):
    # REQUEST PARSING TO PARSER CONTAINERS
    LP_IP_RANGE = os.getenv("LP_IP_RANGE").split("-") # IP RANGE FRO LOG PARSERS(LP)
    LP_PORT_RANGE = os.getenv("LP_PORT_RANGE").split("-") # PORT RANGE FRO LOG PARSERS(LP)
    
    ip = get_ip(LP_IP_RANGE[0], LP_IP_RANGE[1])
    # Static port, ip changes.
    port = 40001 # get_port(LP_PORT_RANGE[0], LP_PORT_RANGE[1]) # Randomly choose port.
    url = f"http://{ip}:{port}/parse"
    app.logger.info(f"parse(): Requesting to: {url}")
    
    # IP MAY BE NOT NEEDED
    headers = {'Content-Type': 'application/json'}
    # req = requests.post(url)
    # payload = request.json
    r = requests.post(url, data=json.dumps(payload), headers=headers)

    result = r.json()
    app.logger.debug(f"Parser Results: {result}")

    return result

@app.route("/parse", methods=["POST"])
def parse():
    global MY_ROLE
    if len(os.getenv("CURRENT_LP_IP")) <= 0:
        start_paxos()
        app.logger.info(f"CONSENSUS FINISHED, CURRENT_LP_IP = {os.getenv('CURRENT_LP_IP')}")

    
    # ip = get_ip(LP_IP_RANGE[0], LP_IP_RANGE[1])
    ip = os.getenv("CURRENT_LP_IP") # middleware in charge of parsing.
    myip = socket.gethostbyname(socket.gethostname())
    
    app.logger.info(f"CURRENT_LP_IP: {ip}")
    app.logger.info(f"I am {myip} ROLE: {MY_ROLE}")
    parsing_result = {}
    # compare only the ip part, exclude port.
    if(ip.split(":")[0] == myip):
        app.logger.info(f"Requesting parsing from {ip}.")
        # CAN REQUEST PARSING.
        payload = request.json
        parsing_result = request_parsing(payload)     
        return parsing_result
    else:
        # MAKE REQUEST TO MW WHO CAN REACH PARSER(ip)
        url = f"http://{ip}/parse"
        app.logger.info(f"parse(): Requesting parsing to MW: {url}")
        
        # IP MAY BE NOT NEEDED
        headers = {'Content-Type': 'application/json'}
        # payload from original request will be resend to a new middleware
        # capable of reaching parsers.
        payload = request.json
        app.logger.info(f"PAYLOAD: {payload}")
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        app.logger.info(f"\tRequest parse() response: {r}")
        parsing_result = r.text
        app.logger.info(f"\tRequest response: {parsing_result}")

        # parsingResult = requestParsing(ip)    
    
    return parsing_result

@app.route("/detect", methods=["POST"])
def detect_anomalies():
    print("ENV: ", os.getenv("AD_IP_RANGE"))
    print("ENV: ", os.getenv("AD_PORT_RANGE"))
    AD_IP_RANGE = os.getenv("AD_IP_RANGE").split("-") # IP RANGE FRO LOG PARSERS(LP)
    ad_port = 50001 # 50001 - 50006 for AD on host exposition. Inside docker env 50001 is accesible.
    # PORT WILL BE STATIC
    # AD_PORT_RANGE = os.getenv("AD_PORT_RANGE").split("-") # PORT RANGE FRO LOG PARSERS(LP)
    
    # ip = get_ip(LP_IP_RANGE[0], LP_IP_RANGE[1])
    # IP MAY BE NOT NEEDED, USING STATIC(LOCAL HOST IP)
    ip = os.getenv("IPLOCAL")
    port = get_port(AD_PORT_RANGE[0], AD_PORT_RANGE[1])
    url = f"http://{ip}:{port}/detect_anomalies"
    print("Requesting to: ", url)
    
    headers = {'Content-Type': 'application/json'}
    # req = requests.post(url)
    payload = request.json
    r = requests.post(url, data=json.dumps(payload), headers=headers)

    result = r.text
    print("Results: ", result)

    return result

if __name__ == "__main__":
    # INITIALIZE SOME ENV VARIABLES.
    os.environ["CURRENT_LP_IP"] = ""

    PORT=os.getenv("PORT")

    app.run(debug=True, host="0.0.0.0", port=PORT)
