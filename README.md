# nightshift

NightShift is a little thing I felt like writing to see if I could do it. The NightShift project is an http 404 status C2 written in python3 using aiohttp.

<h3>Was inspired by two other projects:</h3>

<p>https://github.com/theG3ist/404</p>

<p>https://github.com/cedowens/SimpleC2_Server</p>

I am using json formating to send data back and forth. Also using a dga to generate new keys everday for encryption. It curently only works with linux.

Usage:
<p>This writes the custom 404 command</p><br>
python3 nighshift_cmd.py

To Do:

Use the dga fuction to generate and check the domains for your flexability.

Write a config file generator to customize the client and server (i.e. custom 404 message, custom URI paths, preconfigure server ip or url, user agent strings, redirecting urls and port)

Build Windows clinet.

Build a script with precanned commands that are commonly ran on Windows and Linux. You will be able to enter the command when asked by the nightshift_cmd script.

Also thinking about putting all the data into an ELK stack backend running on docker. So I may post a docker compse file for that.
