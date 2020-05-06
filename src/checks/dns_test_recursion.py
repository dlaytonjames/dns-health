def run(domain, ns):
    res = check_recursive(domain, ns)
    return {"description": "Check nameservers not recursive", "result": not res.get("result"), "details": res.get("details")}

def check_recursive(q, ns_list):
    # checks for if RD flag is checked in the response
    # q is for the server outside the jurisdiction of the name servers
    # ns_list is a list of all the name servers to be tested
    import dns.message
    import dns.query
    import socket
    for x in ns_list:
        try:
            query = dns.message.make_query(q, dns.rdatatype.NS)
        
            y = socket.gethostbyname(x) 
            response = dns.query.udp(query, y)
            s = str(response)
            if "RA" in s: # When "RA" is in the response message then the ns server tells the client that recursion have happened
                
                return {"result": True, "details": "Recursion has been detected because RA was found in the response message from {0}".format(x)}
                # print("The name server is set to use recursion when it tried to query", x)
        except Exception:
            pass

    
    return {"result": False, "details": "no recursion"}

    # It will return a boolean of whether recursion occured

