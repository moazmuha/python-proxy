# Simple Python Proxy
•A Proxy Server using Python’s Socket API  
•Proxy server handles simultaneous TCP connections  
•Caches pages for set amount of time  
•Adds label to inform client if they are accessing a Cached or Fresh version of the page 
•Supports HTTP pages. Redirects any pages that use HTTPS

## Contents
1.[User Guide](#userguide) <br>
2.[Links for Testing](#Links)  <br>
3.[Examples](#Examples) <br>
4.[Notes](#Notes)


## User Guide
1. Download the repo
2. Run using "python proxy.py"
4. Takes optional cache expire time argument. Default value for cache expire time is 120 seconds if no time argument is given. To specify time use command "python proxy.py [time]" where time is in an integer in seconds.
5. In your browser enter http://localhost:8888/[websiteURL]. For example try http://localhost:8888/www.example.org

## Links
Here are some links you can try. Note: Larger pages with many images may take some time to load. Be pateint :)
1. http://localhost:8888/www.example.org (should load very quick)
2. http://localhost:8888/www.cs.toronto.edu/~ylzhang/
3. http://localhost:8888/www.cs.toronto.edu/~arnold/ (images may take time to show up)
4. http://localhost:8888/www.cs.toronto.edu/~ylzhang/csc258/memes.html (may take time to load all images)

You may try to load all the pages at once in different tabs. Pages being loaded simultaneously have been tested but may slow down the loading of pages further. The available hardware resources of the system the server is running on can make a substantial difference in how long it may take pages to load. Cached pages should load significantly faster. If the pages refuse to load, try restarting the server. Your browser may also cache pages. You can use private windows to avoid browser caching.


## Examples
![image](https://user-images.githubusercontent.com/66569506/116111484-b0fa0000-a684-11eb-8ab4-acd6cf508164.png)
![image](https://user-images.githubusercontent.com/66569506/116111006-38933f00-a684-11eb-8342-f4b2a2511f51.png)

## Notes you(notes)
•Improvements can be made, message me or open an issue if you would like to contribute <br />
•Caching needs to be improved <br />
•The same favicon.ico is used for all pages currently. <br />
•The project was completed without the zlib library, hence why we request a decompressed version of pages so we can add the HTML tag without having to decompress data. This may be a cause of further slowdowns. However, not adding new imports was a requirement for this porject. <br />




