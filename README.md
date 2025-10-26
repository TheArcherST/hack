AEZA DNS Backend.<br>
Stack:
<ul>
    <li>Dishka</li>
    <li>sqlalchemy</li>
    <li>fastapi</li>
    <li>postgresql</li>
    <li>redis</li>
    <li>taskiq</li>
</ul>

Tests:
<ul>
    <li>PING</li>
    <li>DNS</li>
    <li>HTTP/S</li>
    <li>TCP/UDP</li>
    <li>TRACEROUTE</li>
    <li>GEOIP</li>
    <li>NMAP</li>
</ul>

How to deploy (using Makefile shortcuts for docker commands):
1. Ensure you installed docker and make on your host
2. Fill all .env files with provided .env.example templates.
3. `make up`

How to connect agent:
1. Ensure you installed docker on your host
2. Create new directory for the deployment
3. Place downloaded from frontend compose.yaml into it
4. `docker compose up -d`
