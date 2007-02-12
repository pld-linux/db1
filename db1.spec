Summary:	BSD database library for C
Summary(pl.UTF-8):	Biblioteka bazodanowa z BSD dla C
Name:		db1
Version:	1.85
Release:	8
License:	BSD
Group:		Libraries
# alternative site (sometimes working): http://www.berkeleydb.com/
#Source0Download: http://dev.sleepycat.com/downloads/releasehistorybdb.html
Source0:	http://downloads.sleepycat.com/db.%{version}.tar.gz
# Source0-md5:	42cc6c1e1e25818bd3e3f91328edb0f1
Patch0:		%{name}.patch
URL:		http://www.sleepycat.com/
BuildConflicts:	glibc-db1
Conflicts:	glibc < 2.1.90
Obsoletes:	glibc-db1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. It should be installed if compatibility is
needed with databases created with db1. This library used to be part
of the glibc package.

%description -l pl.UTF-8
Berkeley Database (Berkeley DB) to zestaw narzędzi programistycznych
zapewniających obsługę baz danych w aplikacjach tradycyjnych jak i
klient-serwer. Powinna być zainstalowana jeżeli potrzebna jest
kompatybilność z bazami stworzonymi db1. Ta biblioteka była częścią
glibc.

%package devel
Summary:	Header files for Berkeley database library
Summary(pl.UTF-8):	Pliki nagłówkowe do biblioteki Berkeley Database
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Conflicts:	glibc-devel < 2.1.90
Obsoletes:	glibc-db1-devel

%description devel
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. Berkeley DB includes B tree, Hashing,
Fixed and Variable-length record access methods.

This package contains the header files, and documentation for building
programs which use Berkeley DB.

%description devel -l pl.UTF-8
Berkeley Database (Berkeley DB) to zestaw narzędzi programistycznych
zapewniających obsługę baz danych w aplikacjach tradycyjnych jak i
klient-serwer. Berkeley DB obsługje dostęp do bazy przez B-drzewa i
funkcje mieszające ze stałą lub zmienną wielkością rekordu.

Ten pakiet zawiera pliki nagłówkowe i dokumentację do budowania
programów używających Berkeley DB.

%package static
Summary:	Static libraries for Berkeley database library
Summary(pl.UTF-8):	Statyczne biblioteki Berkeley Database
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Conflicts:	glibc-static < 2.1.90
Obsoletes:	glibc-db1-static

%description static
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. Berkeley DB includes B tree, Hashing,
Fixed and Variable-length record access methods.

This package contains the static libraries for building programs which
use Berkeley DB.

%description static -l pl.UTF-8
Berkeley Database (Berkeley DB) to zestaw narzędzi programistycznych
zapewniających obsługę baz danych w aplikacjach tradycyjnych jak i
klient-serwer. Berkeley DB obsługje dostęp do bazy przez B-drzewa i
funkcje mieszające ze stałą lub zmienną wielkością rekordu.

Ten pakiet zawiera statyczne biblioteki do budowania programów
używających Berkeley DB.

%prep
%setup -q -n db.%{version}
%patch0 -p1

%build
%{__make} -C PORT/linux \
	CC="%{__cc}" \
	OORG="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_includedir}/db1,%{_libdir},%{_bindir}}

sed -n '/^\/\*-/,/^ \*\//s/^.\*.\?//p' include/db.h | grep -v '^@.*db\.h' > LICENSE

cd PORT/linux
sover=`echo libdb.so.* | sed 's/libdb.so.//'`
install libdb.a			$RPM_BUILD_ROOT%{_libdir}/libdb1.a
install libdb.so.$sover		$RPM_BUILD_ROOT%{_libdir}/libdb1.so.$sover
ln -sf libdb1.so.$sover 	$RPM_BUILD_ROOT%{_libdir}/libdb1.so
ln -sf libdb1.so.$sover		$RPM_BUILD_ROOT%{_libdir}/libdb.so.$sover
install ../include/ndbm.h	$RPM_BUILD_ROOT%{_includedir}/db1
install ../../include/db.h	$RPM_BUILD_ROOT%{_includedir}/db1
install ../../include/mpool.h	$RPM_BUILD_ROOT%{_includedir}/db1
install db_dump185		$RPM_BUILD_ROOT%{_bindir}/db1_dump185
cd ../..

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README LICENSE changelog
%attr(755,root,root) %{_bindir}/db1_dump185
%attr(755,root,root) %{_libdir}/libdb*.so.*

%files devel
%defattr(644,root,root,755)
%doc docs/*.ps
%attr(755,root,root) %{_libdir}/libdb1.so
%{_includedir}/db1

%files static
%defattr(644,root,root,755)
%{_libdir}/libdb1.a
