import requests

#url = "http://ksqldb-server:8088/ksql", 
#headers = {"Accept" : "application/vnd.ksql.v1+json", "Content-Type" : "application/vnd.ksql.v1+json" }

#body={
#"ksql": "CREATE STREAM s2 AS SELECT * FROM s1 EMIT CHANGES;", "streamsProperties": {
#"ksql.streams.auto.offset.reset": "earliest" }
#}
#response = requests.post(url, headers=headers, json=body
#)
# Print the response post_response_json = response.json() print(post_response_json)

import requests

# Define the URL and headers
url = "http://ksqldb-server:8088/ksql"
headers = {
    "Content-Type": "application/vnd.ksql.v1+json; charset=utf-8"
}

# Define the payload
payload = {
    "ksql": "SHOW STREAMS;",
    "streamsProperties": {}
}

# Make the POST request
response = requests.post(url, json=payload, headers=headers)

# Check the response
print(response.status_code)
print(response.json())
