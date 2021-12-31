all:
	mkdir /var/db/cport.d
	mkdir /etc/cport.d

	cp src/main.py /usr/sbin/cport
	cp src/cp_*.py /usr/lib/python3.10/site-packages/

	cp src/{blacklist,installed}.db /var/db/cport.d/
	cp src/config/* /etc/cport.d/

	touch /var/log/cport.log

remove:
	rm -rf /var/db/cport.d
	rm -rf /etc/cport.d
	rm -rf /usr/lib/python3.10/site-packages/cp_{blacklists,default,info,install,remove}.py
	rm -rf /usr/sbin/cport