<h2>NightShift 404 C2 - Burning the midnight oil</h2>
<p>
NightShift is a little thing I felt like writing to see if I could do it. The NightShift project is an http 404 status C2 written in python3 using aiohttp. I am using json formating to send data back and forth. Also using a dga to generate new keys everday for encryption. It curently only works with linux.
</p>
<dl>
  <dt><b>Was inspired by two other projects:</b></dt>
  <dd>https://github.com/theG3ist/404</dd>
  <dd>https://github.com/cedowens/SimpleC2_Server</dd>
</dl>

<dl>
  <dt><b>Usage:</b></dt>
  <dt>No need to edit the file diectly, you can now confiugure the client and server (FQDN/IP, URI, User-Agent, listening port). Also if you set the port to 80 you will have to run the server under sudo.</dt>
  <dd><i>python3 nightshift_cmd_conf.py conf (to generate a client/server configuration file)</i></dd>
  <dt>Writing the 404 command</dt>
  <dd><i>python3 nightshift_cmd_conf.py cmd (to generate the fof c2 command)</i></dd>
  <dt>Starting up the server, currently runs on 8080</dt>
  <dd><i>python3 nighshift_server.py</i></dd>
  <dt>Starting up the client.</dt>
  <dd><i>python3 nighshift_client.py</i></dd>
</dl>

<dl>
  <dt><b>To Do:</b></dt>
  <dd>- Use the dga fuction to generate and check the domains for your flexability.</dd>
  <dd>- DONE - Write a config file generator to customize the client and server (i.e. custom 404 message, custom URI paths, preconfigure server ip or url, user agent strings, redirecting urls and port)</dd>
  <dd>- DONE, though it only does powershell right now and it is not a PE, that is coming soon - Build a Windows client.</dd>
  <dd>- Build a script with precanned commands that are commonly ran on Windows and Linux. You will be able to enter the command when asked by the nightshift_cmd script.</dd>
  <dd>- Also thinking about putting all the data into an ELK stack backend running on docker. So I may post a docker compse file for that.</dd>
</dl>
