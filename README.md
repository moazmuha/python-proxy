# Simple Python Proxy
•A Proxy Server using Python’s Socket API  
•Proxy server handles simultaneous TCP connections  
•Caches pages for set amount of time  
•Adds label to inform client if they are accessing a Cached or Fresh version of the page
•Supports HTTP pages. Redirects any pages that use HTTPS

## User Guide
1. Download the repo
2. Run using "python proxy.py"
4. Takes optional cache expire time argument. Default value for cache expire time is 120 seconds if no time argument is given. To specify time use command "python proxy.py [time]" where time is in an integer in seconds.
5. In your browser enter http://localhost:8888/[websiteURL]. For example try http://localhost:8888/www.example.org

## Examples
![image](https://user-images.githubusercontent.com/66569506/116111154-5d87b200-a684-11eb-9449-465e85d17766.png)
![image](https://user-images.githubusercontent.com/66569506/116111006-38933f00-a684-11eb-8342-f4b2a2511f51.png)


