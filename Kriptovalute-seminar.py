from bitcoinrpc.authproxy import AuthServiceProxy,JSONRPCException
import ipinfo
import socket 
import matplotlib.pyplot as plt
import pandas as pd

def main():
    node_name="blockchain.oss.unist.hr"
    port="8332"
    rpc_user="student"
    rpc_password="WYVyF5DTERJASAiIiYGg4UkRH"
    rpc_connection = AuthServiceProxy("http://%s:%s@%s:%s"%(rpc_user,rpc_password,node_name,port))
    
    #Node status podaci
    getinfo = rpc_connection.getnetworkinfo()
    getnet= rpc_connection.getnettotals()
    getbcinfo= rpc_connection.getblockchaininfo()
    
    
    #Current Node explorer
    
    print ("HOST: %s , PORT: %s"%(node_name,port))
    print ("VRSTA LANCA: %s"%(getbcinfo["chain"]))
    print ("VERZIJA: %s (%s)"%(getinfo["version"],getinfo["subversion"]))
    print ("VERZIJA PROTOKOLA: %s"%(getinfo["protocolversion"]))
    print ("VELIČINA LANCA NA DISKU: %.2f GB"%((getbcinfo["size_on_disk"]/(1024**3))))
    print ("BROJ BLOKOVA: %s"%(getbcinfo["blocks"]))
    print ("TEŽINA: %s"%(getbcinfo["difficulty"]))
    if (getbcinfo["blocks"])==(getbcinfo["headers"]):
        print ("STATUS: ","Sinkronizirano")
    else:
        print ("STATUS: ","Nije sinkronizirano")
    print ("UKUPNO PRIMLJENO(U GB): %.2f GB"%((getnet["totalbytesrecv"]/(1024**3))))
    print ("UKUPNO POSLANO(U GB): %.2f GB"%((getnet["totalbytessent"]/(1024**3))))
    if getbcinfo["warnings"]!="":
        print ("UPOZORENJA: %s"%((getbcinfo["warnings"]).strip("Warning:")))
    else:
        print ("NEMA UPOZORENJA")
    
    
    
    df=pd.DataFrame(columns=["Country"])
  
    access_token = '27e7a6e53f8d99'
    handler = ipinfo.getHandler(access_token)
    getpeer=rpc_connection.getpeerinfo()
    print ("Povezani ste na čvor %s"%(node_name))
    print("Broj čvorova s kojim je povezna čvor %s je %d"%(node_name,(len(getpeer)-1)))
   
    for j in range (len(getpeer)):
              #if j<=20:
                adresa_port=getpeer[j]["addr"]
                adresa=adresa_port.split(":")[0]
                host_name = adresa
                host_ip = socket.gethostbyname(host_name) 
                #print("Hostname :  ",host_name) 
                #print("IP : ",host_ip) 
                response = handler.getDetails(adresa)
        
                #print ([adresa,host_name,response.country,response.country_name,response.region,response.timezone,response.city,response.latitude,response.longitude])
                country=response.country_name
               
                df.loc[j]=[country]
                #print (df)
   
   
    fig=df['Country'].value_counts().plot(kind='pie',title='Grupiranje čvorova po državama',autopct='%1.1f%%')
    plt.show()
    
    
if __name__=="__main__":
    main()
