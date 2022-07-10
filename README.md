# PerformanceMonitor

Flask based web server which store client performance data

## Environment

The server and postgres database are run in Docker containers. To start web server please execute:
* docker-compose build
* docker-compose up


## Communication protocol

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

## Data storage
There are two possible ways to store data: file and database. Now to change store type source code (main file) should be updated. File is used by default.
Every client session has its own hash which identify client session. At this moment client can request only cpu data for current session.

### File storage
Performance data is stored in .csv file for every client session. Files named client's hash are stored in users_data directory and have format "cpu","time".

Client data is stored in text file which contains name, password and all sessions(hash) list. The files are stored in users directory.

In general, it is possible to get all cpu data for all session that have been run manually.

```text
_______________              __________________
users          |            |users_data        |
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

### Database(DB) storage

When server is running the first time DB should be initialized using the following script:
* init_db.py<br>

It creates "performancemonitor" DB and needed tables.

User data is stored in user table which contains name, password and special ID. This ID connects(in fact just a counter) connects "user" table with "sessions" table. "sessions" table contents hash and all posted data.

```text
_______________________________       ____________________________________________
users                          |     |sessions                                    |
_______________________________|     |____________________________________________|
user_name|user_passwd|user_id  |     |user_id|user_session|user_cpu|user_timestamp|
_________|___________|_________|     |_______|____________|________|______________|
user1    | passwd1   |   1     |     |  1    |  hash1     | 15.3   |1649596019.895|
user2    | passwd2   |   2     |     |  1    |  hash1     | 4.5    |1949596019.895|
_________|___________|_________|     |  1    |  hash2     | 6.3    |1649858019.895|
                                     |  2    |  hash3     | 7.5    |1449596019.895|                    
                                     |_______|____________|________|______________|
```