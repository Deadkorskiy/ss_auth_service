# Freeradius + MySQL + Daloradius in docker

## Install

### Install docker
`bash install-docker.sh`


### Run freeradius
```
docker run \
    --name freeradius \
    -d \
    -p 1812:1812/udp \
    -p 1813:1813/udp \
    -p 80:80 \
    -e CLIENT_SECRET=RADIUS_SECRET \
    -e CLIENT_NET=0.0.0.0/0 \
    --restart always \
    asdaru/freeradius-mysql-daloradius
```
*You could add  `--net="host"` or `-p 3306:3306` to open MySQL for host*

Dockerfile
```
# src:
# https://hub.docker.com/r/asdaru/freeradius-mysql-daloradius/dockerfile
# https://github.com/asdaru/freeradius-mysql-daloradius

FROM ubuntu:16.04

MAINTAINER Andrey Mamaev <asda@asda.ru>

ENV MYSQLTMPROOT toor

RUN echo mysql-server mysql-server/root_password password $MYSQLTMPROOT | debconf-set-selections;\
  echo mysql-server mysql-server/root_password_again password $MYSQLTMPROOT | debconf-set-selections;\
  apt-get update && apt-get install -y mysql-server mysql-client libmysqlclient-dev \
  nginx php php-common php-gd php-curl php-mail php-mail-mime php-pear php-db php-mysqlnd \
  freeradius freeradius-mysql freeradius-utils \
  wget unzip && \
  pear install DB && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /root/.cpan	

ENV RADIUS_DB_PWD radpass
ENV CLIENT_NET "0.0.0.0/0"
ENV CLIENT_SECRET testing123


RUN wget https://github.com/lirantal/daloradius/archive/master.zip && \
	unzip *.zip && \
	mv daloradius-master /var/www/daloradius && \
 	chown -R www-data:www-data /var/www/daloradius && \
	chmod 644 /var/www/daloradius/library/daloradius.conf.php && \
	rm /etc/nginx/sites-enabled/default

#	cp -R /var/www/daloradius/contrib/chilli/portal2/hotspotlogin /var/www/daloradius

COPY init.sh /	
COPY etc/nginx/radius.conf /etc/nginx/sites-enabled/
		

	
EXPOSE 1812 1813 80

ENTRYPOINT ["/init.sh"]

```

### Change administrator pass

Default login and password for web interface: `Login: administrator Password: radius`

Go to Config -> Operations to change administrator password 

### Enjoy 

If you would like to build your own freeradius container see the `Dockerfile` 


## Connection examples

### Python

See the https://pypi.org/project/py-radius/

```
import radius

username = 'user_name'
password = 'pass'

r = radius.Radius('RADIUS_SECRET', host='RADIUS_HOST', port=1812)
print('success' if r.authenticate(username, password) else 'failure')
```

### Go

```

package main


import (
	"context"
	"log"

	"layeh.com/radius"
	"layeh.com/radius/rfc2865"
)

func main() {
	var RadiusSecret string = "secret"
	var USER_NAME string = "some_username"
	var PASSWORD string = "user_pass"

	packet := radius.New(radius.CodeAccessRequest, []byte(RadiusSecret))
	rfc2865.UserName_SetString(packet, USER_NAME)
	rfc2865.UserPassword_SetString(packet, PASSWORD)
	response, err := radius.Exchange(context.Background(), packet, "localhost:1812")
	if err != nil {
		log.Fatal(err)
	}

	log.Println("Code:", response.Code)
}

```

### OpenVPN

[OpenVPN radius plugin repo](https://github.com/brainly/openvpn-auth-radius)

Tutorials:
  - http://lenwe.net/atlassian-crowd-authentication-for-openvpn
  - https://www.vpsserver.com/community/tutorials/17/authenticate-openvpn-clients-thru-the-freeradius-server/
  - https://www.osradar.com/openvpn-authentication-with-freeradius/
  - https://adminvps.ru/blog/nastrojka-avtorizacii-openvpn-cherez-freeradius/


Easy way to install OpenVPN: `wget https://raw.githubusercontent.com/Nyr/openvpn-install/master/openvpn-install.sh && bash openvpn-install.sh`


To download and build OpenVPN radius plugin you could use following script:
```
# update
apt-get update -y
apt-get install libgcrypt11-dev gcc make build-essential -y

# rm if exists
rm radiusplugin_v2.1a_beta1.tar.gz -f && rm radiusplugin_v2.1a_beta1 -Rf

# download src for freeradius openvpn plugin
wget http://www.nongnu.org/radiusplugin/radiusplugin_v2.1a_beta1.tar.gz && \
    tar xvfz radiusplugin_v2.1a_beta1.tar.gz && \
    rm radiusplugin_v2.1a_beta1.tar.gz -f

# build 
cd radiusplugin_v2.1a_beta1/ && make

# copy to /etc/openvpn/
cp radiusplugin.so /etc/openvpn/ && cp radiusplugin.cnf /etc/openvpn/

# clear
cd ../ && rm radiusplugin_v2.1a_beta1 -Rf
```


To debug OpenVPN server `tail -f /var/log/syslog`




