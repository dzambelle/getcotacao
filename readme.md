## Alterado o MySQLdb pelo pymysql
#
## comanda para funcionar a query de um container ao outro
#  ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'Asdfghj10';
#
## alteração no security level do ssl pra funcionar a parte do tesouro
#  https://askubuntu.com/questions/1233186/ubuntu-20-04-how-to-set-lower-ssl-security-level
#
## fiz a alteraçaõ de timezone usando este site
#  https://www.vivaolinux.com.br/artigo/Modificando-o-TimeZone-2-metodos]
	# Encontrar o Time Zone atual
	cat /etc/timezone
	America/Sao_Paulo

	# Econtrar Timezones disponiveis
	ls /usr/share/zoneinfo/America/

	# ls /usr/share/zoneinfo/America/ | grep Noronha
	Noronha

	# Altere então de America/Sao_Paulo para America/Noronha.
	vi /etc/timezone

	# Agora para atualizar utilizando a variável TZ faça:
	export TZ=America/Noronha

	# Vamos verificar com:
	date

## Fiz alteração de SSL baixando o nivel de seguranca
#  https://askubuntu.com/questions/1233186/ubuntu-20-04-how-to-set-lower-ssl-security-level
	# editar o arquvio SSL
	nano /etc/ssl/openssl.cnf
		# Add this line at the top:
		openssl_conf = openssl_init

		# And add these lines at the end:
		[openssl_init]
		ssl_conf = ssl_sect

		[ssl_sect]
		system_default = system_default_sect

		[system_default_sect]
		CipherString = DEFAULT@SECLEVEL=1

## instalacao do Python 3 
#  https://www.educative.io/edpresso/installing-pip3-in-ubuntu
	apt-get update
	apt-get -y install python3
	python3 --version

## instalacao do pip3
#  https://www.educative.io/edpresso/installing-pip3-in-ubuntu
	apt-get update
	apt-get -y install python3-pip
	pip3 --version

## instalacao e configuracao do Cron
#  https://stackoverflow.com/questions/1802337/how-to-install-cron
#  https://www.pair.com/support/kb/paircloud-using-cron/
	# install
	apt-get update
	apt-get -y install cron
	# use
	crontab -e
		# dentro do arquivo, roda cada 15min de seg a sexta e entre 9hs e 19hs
		*/15 9-19 * * 1-5 /usr/bin/python3 /usr/share/nginx/html/getcotacao/getcotacao.py >>cron.log

## instalacao do pymysql
#  https://pypi.org/project/PyMySQL/
	pip3 install PyMySQL
	
## este cara resolveu o problema na maquina de subir o cron automatico
# https://askubuntu.com/questions/907388/start-cron-service-with-supervisor
# I have the following in my etc/supervisord.conf:

	[program:cron]
	command=cron -f
	autostart=true
	autorestart=false
	stderr_logfile=/var/log/cron.err.log
	stdout_logfile=/var/log/cron.out.log
