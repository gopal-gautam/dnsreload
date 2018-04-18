# Simple script to reload/refresh dns record of dns server and dig the result out for verification

###### This is a simple script that is used to reload reverse dns loopup. Typically used whenever some information is added/edited from the dns record list and reload it. Since in production environment, we may have multiple servers, thus login  to each server and reloading the same dns query could be monotonous job. This tool can be used to automate login to the servers and reload the dns information.

`Usage`

```Bash
$ ./dnsreload.sh [-w <viewzone>] [-s <server>] [-t <dns type>] [-v] [--debug] host

#Get help info of dnsreload script
$ ./dnsreload.sh -h
```