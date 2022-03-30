# PerformanceMonitor

Flask based web server which store client performance data

Client-Server communication is performed via REST API and has the following format:
* To register new user:<br>
Action: post<br>
Resource: /register<br>
Data: {"user": user_name, "passwd": user_passwd}<br>
OK Response:  status: OK, Data = {"hash": user_hash}<br>
NOK Response: status: BAD_REQUEST, Data = {"reason": "User is already registered"}
* To login existing user:<br>
Action: post <br>
Resource: /login <br>
Data: {"user": user_name, "passwd": user_passwd}<br>
OK Response:  status: OK, Data = {"hash": user_hash}<br>
NOK Response: status: UNAUTHORIZED, Data = {"reason": "Wrong credentials or user is not registered"}
* To store cpu data:<br>
Action: post <br>
Resource: /cpu <br>
Data: {"hash": user_hash, "cpu": cpu, "time": current_time}<br>
OK Response:  status: OK, Data = {'payload': {'cpu': cpu, 'hash': hash, 'time': time}}<br>
NOK Response: status: BAD_REQUEST, Data = {"reason": "Bad arguments"} / status: UNAUTHORIZED, Data = {"reason": "Not authorized user try to post data, please login"}
* To get all cpu data for current session:<br>
Action: get <br>
Resource: /cpu with additional parameters: user_hash, start_time, cur_time. <br>start_time and cur_time are not used now. It is for future implementation to get cpu data for specific time range.<br>
OK Response:  status: OK, Data = {'payload': [{'cpu': cpu, 'timestamp': timestamp]}<br>
NOK Response: status: BAD_REQUEST, Data = {"reason": "Bad arguments"} / status: UNAUTHORIZED, Data = {"reason": "Not authorized user try to post data, please login"}

Every client session has its own hash. Performance data is stored in .csv file for every client session. Files named client's hash are stored in storage_data_files directory and have format "cpu","time".

Client data is stored in text file which contains name, password and all hash data for every session. The files are stored in used_data_files directory.

At this moment client can request only cpu data for current session. But in general it is possible to get all cpu data for all session that have been run.

```text
_______________              __________________
user_data_files|            |storage_data_files|
_______________|            |__________________|
user1.txt:                   ->  hash1.csv:
user1, passwd1              |    cpu, time  
hash1 ----------------------     cpu, time
hash2 ----------------------                           
                            |->  hash2.csv:
                                 cpu, time
user2.txt:                       cpu, time      
user2, passwd2                                 
hash3------------------------->  hash3.csv:
                                 cpu, time
                                 cpu, time
```
