# -*- coding: UTF-8 -*-
#!/usr/bin/env python3
#DNSHEALTH-14
import dns, dns.resolver, dns.query, dns.name
from dns.exception import DNSException

import re

def getTheIPofAServer(nameOfTheServer, ipv6_enabled):
   
    try:
        if(ipv6_enabled):
            temp  = dns.resolver.Resolver().query(nameOfTheServer,'AAAA')
        else:
            temp  = dns.resolver.Resolver().query(nameOfTheServer,'A')
        

    except Exception as e:

        return {"result": False, "description": "Check glue consistency" ,"details": e.msg}

    answer = temp.response.answer[0][0].to_text()

    if answer is not None:
        return {"result": answer, "description": "Check glue consistency", "details": "Successfully found the IP!"}
    elif ipv6_enabled:
        return {"result": False, "description": "Check glue consistency" ,"details": "No AAAA records for {0} server were found!".format(nameOfTheServer)}
    else:
        return {"result": False, "description": "Check glue consistency" ,"details": "No A records for {0} server were found!".format(nameOfTheServer)}

def __ask_servers(list_of_servers, request):
    counter = 0
    for server in list_of_servers:
        try:
            response = dns.query.udp(request, server, 0.3)          #Send a request to a DNS server and get the reply
            return ("OK", response)
        except dns.exception.Timeout:                               #If there's a timeout the loop continues and tries the next server
            counter += 1
            if counter == list_of_servers.__len__():                #If all servers are unavailable then the test fails
                return ("Failed", None)
            else:
                continue


#Checks for a server IP addresses from the given section of a DNS server's response 
def __parse_records(list_of_records, pattern, group):
 counter = 0
 servers = []

 #Check all records of response section
 for text_response in list_of_records:
    counter += 1

    record = re.search(pattern, text_response.to_text(), re.VERBOSE)         #Match it with the given regex pattern
    
    if record != None:                                                       #If the match succeeds add the selected part of the record to a list
        servers.append(record.group(group))

    if counter == list_of_records.__len__() and servers.__len__() == 0:     #If there are no matches with the regex then the parsing fails
        return ("Failed", [])

    if  counter == list_of_records.__len__():                               #When all records have been checked, exit loop and return a list of the selected fields
        return ("OK", servers)


#this function is testing the list of name servers given if their glue records are correct
#takes a domain(not used) and a list of name servers in string format
#returns true 

def getGlueRecords(domain, list_of_name_servers, ipv6_enabled):

    #hard coded list of all the root servers
    root_servers = [
        "198.41.0.4", 
        "199.9.14.201",
        "192.33.4.12",
        "199.7.91.13",
        "192.203.230.10",
        "192.5.5.241",
        "192.112.36.4",
        "198.97.190.53",
        "192.36.148.17", 
        "192.58.128.30",
        "193.0.14.129", 
        "199.7.83.42", 
        "202.12.27.33", 
    ]

    RR_pattern = r'''
    ^               #Check from start of string
    
    (\S+)           #Check if there's a URL    
    \s{1}           #Whitespace
    (\d+)           #TTL field
    \s{1}           #Whitespace
    (IN|CH|HS)      #DNS record class
    \s{1}           #Whitespace
    (A)             #A-type or NS-type record
    \s{1}           #Whitespace
    (\S+)           #Data field of record (IP address in this case)
    
    $               #The end of string should follow
    '''

    #ietrate over the list of name servers given so we can test them again the actual ip's and server names
    for server in list_of_name_servers:

        sub_string = server.split(".")

        query = dns.message.make_query(server, dns.rdatatype.A)
        
        (_, response_from_the_servers) = __ask_servers(root_servers,query)


        try:
            answer = response_from_the_servers.additional

            (_,response) = __parse_records(answer,RR_pattern,5)
        except Exception as e:
            return {"result": False, "description" :  "Check glue consistency" ,"details": e.msg}

        (_, response_from_the_servers)= __ask_servers(response,query)

        additional_section = response_from_the_servers.additional

        results = {}

        #build the dictionary based on the additional section of the response we got the server
        for entry in additional_section:

            name_of_the_server = entry.name.to_text().strip(".")
            
            if name_of_the_server in results :
                results[name_of_the_server].append(entry[0].to_text())
            else:
                results[name_of_the_server] = [entry[0].to_text()]

            if name_of_the_server not in list_of_name_servers:
                results.pop(name_of_the_server,None)

        #get all the ipv4 and ipv6 addresses and compare them against the dictionary we built
        for i in list_of_name_servers:
            
            ipv4_query = dns.message.make_query(i,dns.rdatatype.A)

            ipv6_query = dns.message.make_query(i,dns.rdatatype.AAAA)
            
            try:

                ip = getTheIPofAServer(i, False)
            
            except  dns.resolver.NXDOMAIN as e:
                
                return {"result": False, "description" :  "Check glue consistency" ,"details": e.msg}

            if ip["result"] == False :
                return ip
            
            ipv4_reponse_of_the_name_server = dns.query.udp(ipv4_query, getTheIPofAServer(i, False)["result"])

            ipv6_reponse_of_the_name_server = dns.query.udp(ipv6_query, getTheIPofAServer(i, False)["result"])

            ipv4_answer_of_the_name_server = ipv4_reponse_of_the_name_server.answer

            ipv6_answer_of_the_name_server = ipv6_reponse_of_the_name_server.answer
            
            #basically, our solution works like that. for every ip we get for every server, we delete them from the dictionary.
            #if the dictionary has some extra addresses or one of the results and not in the dictionary, return false.

            for ip["result"] in ipv4_answer_of_the_name_server:
                if i in results:
                    if ip["result"][0].to_text() not in results[i]:
                        return {"result": False,"description": "Check glue consistency", "details": "{0} could not be found in the glue records for ipv4 addresses".format(ip["result"][0].to_text())}

                    results[i].remove(ip["result"][0].to_text())

            for ip["result"] in ipv6_answer_of_the_name_server: 
                if i in results:
                    if ip["result"][0].to_text() not in results[i]:
                        print(ip["result"][0].to_text())
                        return {"result": False, "description": "Check glue consistency","details": "{0} could not be found in the glue records for ipv6 addresses".format(ip["result"][0].to_text())}

                    results[i].remove(ip["result"][0].to_text())

        for _,value in results.items():
            if len(value) != 0:
                return {"result": False, "description": "Check glue consistency", "details": "Extra addresses were found when queried the servers!({0})".format(value)}
        return {"result": True,"description": "Check glue consistency", "details": "Sucess! There is consistency between glue and authoritative data!"}

def run(domain, list_of_name_servers, ipv6_enabled):
    return getGlueRecords(domain,list_of_name_servers, ipv6_enabled)