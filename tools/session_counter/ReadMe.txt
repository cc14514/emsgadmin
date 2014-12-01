###install peewee
$ git clone https://github.com/coleifer/peewee.git
$ cd peewee
$ python setup.py install

###install mysql
$ wget http://jaist.dl.sourceforge.net/project/mysql-python/mysql-python-test/1.2.4b4/MySQL-python-1.2.4b4.tar.gz
$ gunzip MySQL-python-1.2.4b4.tar.gz
$ tar -xvf MySQL-python-1.2.4b4.tar
$ cd MySQL-python-1.2.4b4
$ python setup.py build
$ python setup.py install

$ crontab -e

### session sample job
 * * * * * root python /root/py/get_total_count.py
