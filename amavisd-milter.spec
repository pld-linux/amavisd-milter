# set this back to /var/amavis
Summary:	Sendmail milter for amavisd-new with support for the AM.PDP protocol
Name:		amavisd-milter
Version:	1.5.0
Release:	0.1
License:	BSD
Group:		Applications/System
URL:		http://amavisd-milter.sourceforge.net/
Source0:	http://downloads.sourceforge.net/amavisd-milter/%{name}-%{version}.tar.gz
# Source0-md5:	2c9f601012164d14a0c2815a9e0928fe
Source1:	%{name}.init
Source2:	%{name}.sysconfig
BuildRequires:	libmilter-devel >= 8.13
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	amavisd-new >= 1:2.7.0
Requires:	rc-scripts
Requires(post,preun):	/sbin/chkconfig
Obsoletes:	amavisd-new-sendmail < 1:2.7.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_localstatedir	%{_var}/spool/amavis

%description
amavisd-milter is a sendmail milter (mail filter) for amavisd-new
2.4.3 or and sendmail 8.13 and above (limited support for sendmail
8.12 is provided) which use the new AM.PDP protocol.

Instead of older amavis-milter helper program, full amavisd-new
functionality is available, including adding spam and virus
information header fields, modifying Subject, adding address
extensions and removing certain recipients from delivery while
delivering the same message to the rest.

%prep
%setup -q

%build
%configure \
	--with-working-dir=%{_localstatedir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}
install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add amavisd-milter
%service amavisd-milter restart

%preun
if [ "$1" -eq 0 ]; then
	%service amavisd-milter stop
	/sbin/chkconfig --del amavisd-milter
fi

%files
%defattr(644,root,root,755)
%doc README TODO CHANGES
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(755,root,root) %{_sbindir}/amavisd-milter
%{_mandir}/man8/amavisd-milter.8*
