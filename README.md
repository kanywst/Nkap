# Nkap

Nkap is a simple network reconnaissance tool. It can be used in CTFs and other penetration testing environments (e.g. OSCP, Hack The Box, Vulnhub)

## Origin

Nkap was inspired by AutoRecon.

## Features

- Simple
- Automatically executes the first thing that would be done in a penetration test environment.

## Requirements

### Python 3

```
$ sudo apt install python3
$ sudo apt install python3-pip
```

### Supporring packages

```
nmap
nikto
gobuster
```

```
$ sudo apt install nmap nikto gobuster
```

## Installation

```
$ pip install git+https://github.com/kanywst/nkap
```

## Usage

```
usage: nkap [-h] [-w WORDLIST] [-o OUTPUT_DIR] target

Nkap is a simple network reconnaissance tool

positional arguments:
  target                The target URL

optional arguments:
  -h, --help            show this help message and exit
  -w WORDLIST, --wordlist WORDLIST
                        Path to the wordlist
  -o OUTPUT_DIR, --output OUTPUT_DIR
                        The output directory for results. Default: results
```

### Examples

Scanning sinle target

```
$ nkap 192.168.2.133
[NMAP]
22/ssh          tcp open
25/smtp         tcp open
53/domain       tcp open
80/http         tcp open
111/rpcbind     tcp open
42012/unknown   tcp open
[*] Running port scan: 192.168.2.133:22
[*] Running port scan: 192.168.2.133:25
[*] Running port scan: 192.168.2.133:53
[*] Running port scan: 192.168.2.133:80
[*] Running port scan: 192.168.2.133:111
[*] Running port scan: 192.168.2.133:42012

[NIKTO]
---------------------------------------------------------------------------
+ Server: Apache
+ The anti-clickjacking X-Frame-Options header is not present.
+ The X-XSS-Protection header is not defined. This header can hint to the user agent to protect against some forms of XSS
+ The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type
+ No CGI Directories found (use '-C all' to force check all possible dirs)
+ OSVDB-3268: /games/: Directory indexing found.
+ Entry '/games/' in robots.txt returned a non-forbidden or redirect HTTP code (200)
+ Entry '/dropbox/' in robots.txt returned a non-forbidden or redirect HTTP code (200)
+ Entry '/contact/' in robots.txt returned a non-forbidden or redirect HTTP code (200)
+ Entry '/search/' in robots.txt returned a non-forbidden or redirect HTTP code (200)
+ Entry '/archive/' in robots.txt returned a non-forbidden or redirect HTTP code (200)
+ Entry '/wp-admin/' in robots.txt returned a non-forbidden or redirect HTTP code (200)
+ Entry '/wp-content/' in robots.txt returned a non-forbidden or redirect HTTP code (200)
+ Entry '/wp-includes/' in robots.txt returned a non-forbidden or redirect HTTP code (200)
+ Entry '/comment-page-/' in robots.txt returned a non-forbidden or redirect HTTP code (200)
+ Entry '/trackback/' in robots.txt returned a non-forbidden or redirect HTTP code (200)
+ Entry '/xmlrpc.php' in robots.txt returned a non-forbidden or redirect HTTP code (301)
+ Entry '/blackhole/' in robots.txt returned a non-forbidden or redirect HTTP code (200)
+ Entry '/mint/' in robots.txt returned a non-forbidden or redirect HTTP code (200)
+ Entry '/feed/' in robots.txt returned a non-forbidden or redirect HTTP code (200)
+ "robots.txt" contains 26 entries which should be manually viewed.
+ Server may leak inodes via ETags, header found with file /, inode: d3, size: 54c550ee22d56, mtime: gzip
+ Allowed HTTP Methods: OPTIONS, GET, HEAD, POST 
+ OSVDB-3092: /archive/: This might be interesting...
+ OSVDB-3092: /support/: This might be interesting...
+ OSVDB-3092: /manual/: Web server manual found.
+ OSVDB-3268: /manual/images/: Directory indexing found.
+ OSVDB-3233: /icons/README: Apache default file found.
+ /wp-admin/: Admin login page/section found.
+ /phpmyadmin/: phpMyAdmin directory found
+ 7943 requests: 0 error(s) and 28 item(s) reported on remote host
+ End Time:           2020-07-19 10:12:28 (GMT9) (63 seconds)
---------------------------------------------------------------------------

[GOBUSTER]
[*] 200 OK
        /robots.txt
[*] 301 Moved Permanently
        /archive
        /blackhole
        /blog
        /contact
        /control
        /dropbox
        /extend
        /feed
        /games
        /manual
        /mint
        /phpmyadmin
        /plugins
        /search
        /support
        /tag
        /themes
        /trackback
        /wp-content
        /xmlrpc.php
        /wp-admin
        /wp-includes
[*] 403 Forbidden
        /.htpasswd
        /.htpasswd.php
        /.htaccess
        /.htaccess.php
        /server-status
[*] Finished
```

### Results

```
.
|
└── scans/
    ├── commands.log
    ├── nmap.txt
    ├── nikto.txt
    ├── gobuster.txt
    ├── tcp_22_ssh_nmap.txt
    ├── tcp_25_smtp_nmap.txt
    ├── tcp_53_domain_nmap.txt
    ├── tcp_80_http_nmap.txt
    └── tcp_42012_unknown_nmap.txt
 ```

