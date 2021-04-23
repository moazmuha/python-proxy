# python-proxy
Python Proxy Server <br />
•Created a Proxy Server using Python’s Socket API  <br />
•Proxy server handles simultaneous TCP connections  <br />
•Caches pages for set amount of time  <br />
•Adds label to inform client if they are accessing a Cached or Fresh version of the page  <br />

Takes optional cache expire time argument.  <br />
For example "python proxy.py 60" where 60 is in seconds. Default value for cache expire time is 120 seconds.  <br />
Supports HTTP pages. Redirects any pages that use HTTPS.
