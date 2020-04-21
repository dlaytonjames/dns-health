def check_recursive(q, ns_list):
    # checks for if RD flag is checked in the response
    # q is for the server outside the jurisdiction of the name servers
    # ns_list is a list of all the name servers to be tested
    import dns.message
    import dns.query
    import socket
    recursion_exists = False
    for x in ns_list:
        query = dns.message.make_query(q, dns.rdatatype.NS)
        x = socket.gethostbyname(x) 
        response = dns.query.udp(query, x)
        s = str(response)
        if "RA" in s: # When "RA" is in the response message then the ns server tells the client that recursion have happened
            recursion_exists = True
            print("The name server is set to use recursion when it tried to query", x)
    return recursion_exists
