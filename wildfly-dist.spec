Name:		wildfly-dist
Version:	10.0.0.Final
Release:	1%{?dist}
Summary:	WildFly Application Server
Group:		System Environment/Daemons
License:	LGPL 2.1
URL:		http://www.wildfly.org
Source:		http://download.jboss.org/wildfly/%{version}/wildfly-%{version}.tar.gz

ExclusiveArch:	x86_64 i686
ExclusiveOS:	Linux

Requires(pre):	shadow-utils
Requires:	java >= 1.8.0
Requires:	/etc/init.d/functions
Provides:	wildfly

%undefine _missing_build_ids_terminate_build
%define __arch_install_post QA_SKIP_RPATHS=2 %{__arch_install_post} 
%define __jar_repack 0

%description
WildFly Application Server packaged from the binary distribution.


%prep
%setup -q -n wildfly-%{version}


%install
WILDFLY_VERSION=10.1.0.Final
WILDFLY_FILENAME=wildfly-$WILDFLY_VERSION
WILDFLY_ARCHIVE_NAME=$WILDFLY_FILENAME.tar.gz

INSTALL_DIR=/opt
WILDFLY_FULL_DIR=$INSTALL_DIR/$WILDFLY_FILENAME
WILDFLY_DIR=$INSTALL_DIR/wildfly

WILDFLY_USER="wildfly"
WILDFLY_SERVICE="wildfly"
WILDFLY_MODE="standalone"

mkdir -p %{buildroot}/opt/wildfly
cp -R . %{buildroot}/opt/wildfly
mkdir -p %{buildroot}/etc/init.d
mkdir -p %{buildroot}/etc/default
WILDFLY_VERSION=10.1.0.Final
WILDFLY_FILENAME=wildfly-$WILDFLY_VERSION
WILDFLY_ARCHIVE_NAME=$WILDFLY_FILENAME.tar.gz
WILDFLY_DOWNLOAD_ADDRESS=http://download.jboss.org/wildfly/$WILDFLY_VERSION/$WILDFLY_ARCHIVE_NAME

INSTALL_DIR=/opt
WILDFLY_FULL_DIR=$INSTALL_DIR/$WILDFLY_FILENAME
WILDFLY_DIR=$INSTALL_DIR/wildfly

WILDFLY_USER="wildfly"
WILDFLY_SERVICE="wildfly"
WILDFLY_MODE="standalone"

WILDFLY_STARTUP_TIMEOUT=240
WILDFLY_SHUTDOWN_TIMEOUT=30



#echo "Cleaning up..."
#rm -f "$WILDFLY_DIR"
#rm -rf "$WILDFLY_FULL_DIR"
#rm -rf "/var/run/$WILDFLY_SERVICE/"
#rm -f "/etc/init.d/$WILDFLY_SERVICE"

#echo "Installation..."
#mkdir $WILDFLY_FULL_DIR
#tar -xzf $WILDFLY_ARCHIVE_NAME -C $INSTALL_DIR
#ln -s $WILDFLY_FULL_DIR/ $WILDFLY_DIR
#useradd -s /sbin/nologin $WILDFLY_USER
#chown -R $WILDFLY_USER:$WILDFLY_USER $WILDFLY_DIR
#chown -R $WILDFLY_USER:$WILDFLY_USER $WILDFLY_DIR/
#
##mkdir -p /var/log/$WILDFLY_SERVICE

echo "Registrating Wildfly as service..."
# if should use systemd

    # Script from $WILDFLY_DIR/docs/contrib/scripts/systemd/launch.sh didn't work for me
    cp $WILDFLY_DIR/docs/contrib/scripts/systemd/launch.sh  %{buildroot}$WILDFLY_DIR/bin/
    cat > $WILDFLY_DIR/bin/launch.sh << "EOF"



    WILDFLY_HOME="/opt/wildfly"



    echo 'Starting Wildfly in standalone mode.'
    $WILDFLY_HOME/bin/standalone.sh -c $2 -b $3
    #>> /var/log/$WILDFLY_SERVICE/server-`date +%Y-%m-%d`.log

    # $WILDFLY_HOME is not visible here
    sed -i -e 's,WILDFLY_HOME=.*,WILDFLY_HOME='$WILDFLY_DIR',g' %{buildroot}$WILDFLY_DIR/bin/launch.sh
    #sed -i -e 's,$WILDFLY_SERVICE,'$WILDFLY_SERVICE',g' %{buildroot}$WILDFLY_DIR/bin/launch.sh
    chmod +x $WILDFLY_DIR/bin/launch.sh
    
    cp $WILDFLY_DIR/docs/contrib/scripts/systemd/wildfly.service %{buildroot}/etc/systemd/system/$WILDFLY_SERVICE.service
    WILDFLY_SERVICE_CONF=/etc/default/$WILDFLY_SERVICE
    # To install multiple instances of Wildfly replace all hardcoding in systemd file
    sed -i -e 's,EnvironmentFile=.*,EnvironmentFile='$WILDFLY_SERVICE_CONF',g' %{buildroot}/etc/systemd/system/$WILDFLY_SERVICE.service
    sed -i -e 's,User=.*,User='$WILDFLY_USER',g' /etc/systemd/system/$WILDFLY_SERVICE.service
    sed -i -e 's,PIDFile=.*,PIDFile=/var/run/wildfly/'$WILDFLY_SERVICE'.pid,g' %{buildroot}/etc/systemd/system/$WILDFLY_SERVICE.service
    sed -i -e 's,ExecStart=.*,ExecStart='$WILDFLY_DIR'/bin/launch.sh $WILDFLY_MODE $WILDFLY_CONFIG $WILDFLY_BIND,g' %{buildroot}/etc/systemd/system/$WILDFLY_SERVICE.service
    systemctl daemon-reload
    #systemctl enable $WILDFLY_SERVICE.service


WILDFLY_USER=${WILDFLY_USER}
WILDFLY_DIR=${WILDFLY_DIR}



    echo "Configuring service..."
    echo JBOSS_HOME=\"$WILDFLY_DIR\" > %{buildroot}$WILDFLY_SERVICE_CONF
    echo JBOSS_USER=\"$WILDFLY_USER\" >> %{buildroot}$WILDFLY_SERVICE_CONF
    echo WILDFLY_HOME=\"$WILDFLY_DIR\" >> %{buildroot}$WILDFLY_SERVICE_CONF
    echo WILDFLY_USER=\"$WILDFLY_USER\" >> %{buildroot}$WILDFLY_SERVICE_CONF
    echo STARTUP_WAIT=$WILDFLY_STARTUP_TIMEOUT >> %{buildroot}$WILDFLY_SERVICE_CONF
    echo SHUTDOWN_WAIT=$WILDFLY_SHUTDOWN_TIMEOUT >> %{buildroot}$WILDFLY_SERVICE_CONF   
    echo WILDFLY_CONFIG=$WILDFLY_MODE.xml >> %{buildroot}$WILDFLY_SERVICE_CONF
    echo WILDFLY_MODE=$WILDFLY_MODE >> %{buildroot}$WILDFLY_SERVICE_CONF
    echo WILDFLY_BIND=0.0.0.0 >> %{buildroot}$WILDFLY_SERVICE_CONF


echo "Configuring application server..."
sed -i -e 's,<deployment-scanner path="deployments" relative-to="jboss.server.base.dir" scan-interval="5000",<deployment-scanner path="deployments" relative-to="jboss.server.base.dir" scan-interval="5000" deployment-timeout="'$WILDFLY_STARTUP_TIMEOUT'",g' %{buildroot}$WILDFLY_DIR/$WILDFLY_MODE/configuration/$WILDFLY_MODE.xml
sed -i -e 's,<inet-address value="${jboss.bind.address:127.0.0.1}"/>,<any-address/>,g' %{buildroot}$WILDFLY_DIR/$WILDFLY_MODE/configuration/$WILDFLY_MODE.xml
#sed -i -e 's,<socket-binding name="ajp" port="${jboss.ajp.port:8009}"/>,<socket-binding name="ajp" port="${jboss.ajp.port:28009}"/>,g' $WILDFLY_DIR/$WILDFLY_MODE/configuration/$WILDFLY_MODE.xml
#sed -i -e 's,<socket-binding name="http" port="${jboss.http.port:8080}"/>,<socket-binding name="http" port="${jboss.http.port:28080}"/>,g' $WILDFLY_DIR/$WILDFLY_MODE/configuration/$WILDFLY_MODE.xml
#sed -i -e 's,<socket-binding name="https" port="${jboss.https.port:8443}"/>,<socket-binding name="https" port="${jboss.https.port:28443}"/>,g' $WILDFLY_DIR/$WILDFLY_MODE/configuration/$WILDFLY_MODE.xml
#sed -i -e 's,<socket-binding name="osgi-http" interface="management" port="8090"/>,<socket-binding name="osgi-http" interface="management" port="28090"/>,g' $WILDFLY_DIR/$WILDFLY_MODE/configuration/$WILDFLY_MODE.xml



echo "Done."

# The init script doesn't default the user and crashes. Might as well set the
# home dir since we know what it is.
sed -e 's/# JBOSS_HOME/JBOSS_HOME/' -i %{buildroot}/etc/default/wildfly.conf
sed -e 's/# JBOSS_USER/JBOSS_USER/' -i %{buildroot}/etc/default/wildfly.conf

mkdir -p %{buildroot}/var/log/wildfly
mkdir -p %{buildroot}/var/run/wildfly


%pre
getent group wildfly >/dev/null || groupadd -r wildfly
getent passwd wildfly >/dev/null || \
    useradd -r -g wildfly -d /opt/wildfly -s /sbin/nologin wildfly


%post
alternatives --install /etc/alternatives/wildfly wildfly /opt/wildfly 100


%postun
alternatives --remove wildfly /opt/wildfly


%files
%defattr(-,root,root,0755)


%files
%defattr(-,root,root,0755)
%config /etc/default/wildfly.conf
/etc/init.d/wildfly
%dir /opt/wildfly
/opt/wildfly/appclient
/opt/wildfly/bin
/opt/wildfly/domain
/opt/wildfly/jboss-modules.jar
/opt/wildfly/modules
%attr(-,wildfly,wildfly) /opt/wildfly/standalone
/opt/wildfly/welcome-content
%dir /var/log/wildfly
%dir /var/run/wildfly

%doc /opt/wildfly/copyright.txt
%doc /opt/wildfly/LICENSE.txt
%doc /opt/wildfly/README.txt
%doc /opt/wildfly/docs


%changelog
* Tue Dec 27 2016 Jorge Figueira <morpheus9999@gmail.com>
- bump to 10.0.0.Final
* Tue Jul 21 2015 Charles Simpson <csimpson@gmail.com>
- bump to 9.0.0.Final

* Tue Jul 21 2015 Charles Simpson <csimpson@gmail.com>
- bump to 8.2.0.Final

* Tue Jul 21 2015 Charles Simpson <csimpson@gmail.com>
- eliminate split between wildfly-common and wildfly
- change location to /opt/wildfly (see bin/init.d/wildfly.conf for default)
- install init.d and configuration files

* Sun Jul 13 2014 Charles Simpson <csimpson@gmail.com>
- initial creation
