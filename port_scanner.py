import socket
import common_ports

def get_open_ports(target, port_range, verbose = False):
    open_ports = []
    for port in range (port_range[0], port_range[1]+1):
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        try: 
            print("Target Host:", target)
            print("Attempting to connect to Port:", port)
               
            result = sock.connect_ex((target, port))

            if result == 0:
                print("!!!!! >>>> OPEN PORT:", port)
                open_ports.append(port)
                sock.close() 
        
        except OSError as e:
            if e.errno == -2:
                checkIfTargetIsNumbersOnly = target.replace('.','').isnumeric()
                if checkIfTargetIsNumbersOnly:
                    open_ports = "Error: Invalid IP address"
                    continue
                else:
                    open_ports = "Error: Invalid hostname"
                    continue
                    
        finally:
            sock.close() 
                           
  
    if (verbose == True):
        resultPrint = ""
        website = ""
        verboseTarget = ""
        checkIfTargetIsNumbersOnly = target.replace('.','').isnumeric()
        if checkIfTargetIsNumbersOnly:

            def dns_ptr_lookup(addr):
                try:
                    return socket.gethostbyaddr(addr)
                except socket.herror:
                    return None, None, None
           
            website = dns_ptr_lookup(target)
            
            if website[0] == None:
                verboseTarget = target
            else:
                verboseTarget = f"{website[0]}"+ " ("+f"{target}"+")"
        
        else:
            
            def URL_ptr_lookup(url):
                try:
                    return socket.gethostbyname(url)
                except socket.herror:
                    return None

            website = URL_ptr_lookup(target)
            
            if website == None:
                verboseTarget = target
            else:
                verboseTarget = f"{target}"+ " ("+f"{website}"+")"
        
        for openPort in open_ports:
            service = common_ports.ports_and_services[int(openPort)]
            resultPrint = resultPrint + f"\n{openPort:<9}"+f"{service}"
        open_ports = f"Open ports for {verboseTarget}\nPORT     SERVICE"  + resultPrint
    
    return(open_ports)