# cport
# (C) 2022 Michail Krasnov

install:
	mkdir /var/db/cport.d
	mkdir /etc/cport.d

	cp src/cport.py                 /usr/sbin/cport
	cp src/api/cp_*.py              /usr/lib/python3.10/site-packages/
	cp src/lib/libcport.py          /usr/lib/python3.10/site-packages/

	cp src/databases/*.db           /var/db/cport.d/
	cp src/config/*                 /etc/cport.d/

	touch /var/log/cport.log

remove:
	rm -rf /var/db/cport.d
	rm -rf /etc/cport.d
	rm -rf /usr/lib/python3.9/site-packages/cp_{blacklists,default,info,install,remove}.py
	rm -rf /usr/sbin/cport
