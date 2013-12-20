Name:		jetty9-dist
Version:	9.1.0.v20131115
Release:	1%{?dist}
Summary:	Jetty web server
Group:		System Environment/Daemons
License:	ASL 2.0 or EPL 1.0
URL:		http://www.eclipse.org/jetty/
Source0:	jetty-distribution-%{version}.tar.gz
Source1:	http://eclipse.org/downloads/download.php?file=/jetty/%{version}/dist/

BuildArch:	noarch
Prefix:		/opt/jetty-%{version}
Requires:	java-1.7.0
Provides:	jetty9


%description
Jetty web server packaged from the binary distribution as a single RPM.

Jetty provides a Web server and javax.servlet container, plus support for SPDY,
WebSocket, OSGi, JMX, JNDI, JAAS and many other integrations.


%prep
%setup -q -n jetty-distribution-%{version}


%install
%define __jar_repack 0
mkdir -p %{buildroot}%{prefix}
cp -R . %{buildroot}%{prefix}


%post
alternatives --install /etc/alternatives/jetty-9 jetty-9 %{prefix} 100


%postun
alternatives --remove jetty-9 %{prefix}


%files
%defattr(-,root,root,0755)
%dir %{prefix}
%{prefix}/bin
%{prefix}/demo-base
%{prefix}/etc
%{prefix}/lib
%doc %{prefix}/license-eplv10-aslv20.html
%{prefix}/logs
%{prefix}/modules
%doc %{prefix}/notice.html
%doc %{prefix}/README.TXT
%dir %{prefix}/resources
%config %{prefix}/resources/log4j.properties
%dir %{prefix}/start.d
%config %{prefix}/start.d/http.ini
%config %{prefix}/start.ini
%{prefix}/start.jar
%doc %{prefix}/start.d/README.TXT
%doc %{prefix}/VERSION.txt
%{prefix}/webapps

# Included in -native package
%exclude %{prefix}/lib/setuid/libsetuid-linux.so
%exclude %{prefix}/lib/setuid/libsetuid-osx.so

%changelog
