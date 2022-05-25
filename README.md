### Setup

- create virtualenv with Python >= 3.7
- install packages: ```pip install -r requirements.txt```
- run tests: ```make pytest```
- run app: ```make run``` 

### Usage
request:

`curl --location --request POST 'http://0.0.0.0:8008/api/cmd' \
--header 'Content-Type: application/json' \
--data-raw '{
    "command": "ping",
    "arg": "127.0.0.1",
    "opts": "-c 4"
}'`

response:

`{
    "response": [
        "PING 127.0.0.1 (127.0.0.1): 56 data bytes",
        "64 bytes from 127.0.0.1: icmp_seq=0 ttl=64 time=0.059 ms",
        "64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.089 ms",
        "64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.082 ms",
        "64 bytes from 127.0.0.1: icmp_seq=3 ttl=64 time=0.140 ms",
        "",
        "--- 127.0.0.1 ping statistics ---",
        "4 packets transmitted, 4 packets received, 0.0% packet loss",
        "round-trip min/avg/max/stddev = 0.059/0.092/0.140/0.030 ms",
        ""
    ]
}`

### Graceful shutdown:
- run long-running request, eg `ping` from example above
- kill -s SIGINT $pid (find pid in application logs: time-stamp [46691] [INFO] ... 46691 - PID)
- requests should be finished with correct response, after that application will stops 
### Warning:
- `cat`s a 100GB file will lead to the server OOM


### Help:
- create forbidden dir:
`mkdir tests/forbidden && sudo chown root tests/forbidden && sudo chmod 700 tests/forbidden`
