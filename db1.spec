Summary:	BSD database library for C
Summary(pl):	Biblioteka bazodanowa z BSD dla C
Name:		db1
Version:	1.85
Release:	8
License:	BSD
Group:		Libraries
# alternative site (sometimes working): http://www.berkeleydb.com/
Source0:	http://www.sleepycat.com/update/snapshot/db.%{version}.tar.gz
# Source0-md5:	42cc6c1e1e25818bd3e3f91328edb0f1
Patch0:		%{name}.patch
URL:		http://www.sleepycat.com/
BuildConflicts:	glibc-db1
Conflicts:	glibc < 2.1.90
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	glibc-db1

%description
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. It should be installed if compatibility is
needed with databases created with db1. This library used to be part
of the glibc package.

%description -l pl
Berkeley Database (Berkeley DB) to zestaw narzêdzi programistycznych
zapewniaj±cych obs³ugê baz danych w aplikacjach tradycyjnych jak i
klient-serwer. Powinna byæ zainstalowana je¿eli potrzebna jest
kompatybilno¶æ z bazami stworzonymi db1. Ta biblioteka by³a czê¶ci±
glibc.

%package devel
Summary:	Header files for Berkeley database library
Summary(pl):	Pliki nag³ówkowe do biblioteki Berkeley Database
Group:		Development/Libraries
Requires:	%{name} = %{version}
Conflicts:	glibc-devel < 2.1.90
Obsoletes:	glibc-db1-devel

%description devel
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. Berkeley DB includes B tree, Hashing,
Fixed and Variable-length record access methods.

This package contains the header files, and documentation for building
programs which use Berkeley DB.

%description devel -l pl
Berkeley Database (Berkeley DB) to zestaw narzêdzi programistycznych
zapewniaj±cych obs³ugê baz danych w aplikacjach tradycyjnych jak i
klient-serwer. Berkeley DB obs³ugje dostêp do bazy przez B-drzewa i
funkcje mieszaj±ce ze sta³± lub zmienn± wielko¶ci± rekordu.

Ten pakiet zawiera pliki nag³ówkowe i dokumentacjê do budowania
programów u¿ywaj±cych Berkeley DB.

%package static
Summary:	Static libraries for Berkeley database library
Summary(pl):	Statyczne biblioteki Berkeley Database
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}
Conflicts:	glibc-static < 2.1.90
Obsoletes:	glibc-db1-static

%description static
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. Berkeley DB includes B tree, Hashing,
Fixed and Variable-length record access methods.

This package contains the static libraries for building programs which
use Berkeley DB.

%description static -l pl
Berkeley Database (Berkeley DB) to zestaw narzêdzi programistycznych
zapewniaj±cych obs³ugê baz danych w aplikacjach tradycyjnych jak i
klient-serwer. Berkeley DB obs³ugje dostêp do bazy przez B-drzewa i
funkcje mieszaj±ce ze sta³± lub zmienn± wielko¶ci± rekordu.

Ten pakiet zawiera statyczne biblioteki do budowania programów
u¿ywaj±cych Berkeley DB.

%prep
%setup -q -n db.%{version}
%patch -p1

%build
cd PORT/linux
%{__make} CC=%{__cc} OORG="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d ${RPM_BUILD_ROOT}%{_prefix}/{include/db1,lib,bin}

sed -n '/^\/\*-/,/^ \*\//s/^.\*.\?//p' include/db.h | grep -v '^@.*db\.h' > LICENSE

cd PORT/linux
sover=`echo libdb.so.* | sed 's/libdb.so.//'`
install libdb.a			$RPM_BUILD_ROOT%{_libdir}/libdb1.a
install libdb.so.$sover		$RPM_BUILD_ROOT%{_libdir}/libdb1.so.$sover
ln -sf libdb1.so.$sover 	$RPM_BUILD_ROOT%{_libdir}/libdb1.so
ln -sf libdb1.so.$sover		$RPM_BUILD_ROOT%{_libdir}/libdb.so.$sover
install ../include/ndbm.h	$RPM_BUILD_ROOT%{_includedir}/db1/
install ../../include/db.h	$RPM_BUILD_ROOT%{_includedir}/db1/
install ../../include/mpool.h	$RPM_BUILD_ROOT%{_includedir}/db1/
install db_dump185		$RPM_BUILD_ROOT%{_bindir}/db1_dump185
cd ../..

%clean
rm -rf ${RPM_BUILD_ROOT}

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README LICENSE changelog
%attr(755,root,root) %{_libdir}/libdb*.so.*
%attr(755,root,root) %{_bindir}/db1_dump185

%files devel
%defattr(644,root,root,755)
%doc docs/*.ps
%attr(755,root,root) %{_libdir}/libdb1.so
%{_includedir}/db1

%files static
%defattr(644,root,root,755)
%{_libdir}/libdb1.a
