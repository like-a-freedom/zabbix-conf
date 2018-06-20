# Zabbix agent configuration for SecureTower DLP system monitoring
Here you can find out configuration files and other stuff for Zabbix agent. We make a lot of pre-configured windows perfomance counters for monitoring SecureTower processes on target server.
## Configuration file
* zabbix_agentd.win.conf
## Templates
Templates for Zabbix web-interface with appropriated keys.
## Scripts
Some other stuff for additional monitoring
### - Python
* zbxjson.py — script for monitoring REST API JSON data and its keys.
### - PowerShell
A number of simple posh scripts that sent SUM data of couple instances of processes:
* get_fgindexer_proc_private_bytes_private_bytes.ps1
* get_fgindexer_proc_private_bytes_working_set.ps1
* get_postgres_private_bytes.ps1
* get_postgres_private_bytes_working_set.ps1


