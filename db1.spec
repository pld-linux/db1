Summary:	BSD database library for C
Name:		db1
Version:	1.85
Release:	7
License:	BSD
Group:		Libraries
Group(de):	Libraries
Group(es):	Bibliotecas
Group(fr):	Librairies
Group(pl):	Biblioteki
URL:		http://www.sleepycat.com
Source0:	http://www.sleepycat.com/update/%{version}/db.%{version}.tar.gz
Patch0:		%{name}.patch
Conflicts:	glibc < 2.1.90
BuildConflicts:	glibc-db1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	glibc-db1

%description
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. It should be installed if compatibility is
needed with databases created with db1. This library used to be part
of the glibc package.

%package devel
Summary:	Development libraries and header files for Berkeley database library
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}
Conflicts:	glibc-devel < 2.1.90
Obsoletes:	glibc-db1-devel

%description devel
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. Berkeley DB includes B tree, Hashing,
Fixed and Variable-length record access methods.

This package contains the header files, libraries, and documentation
for building programs which use Berkeley DB.

%package static
Summary:	Static libraries for Berkeley database library
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
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

%prep
%setup -q -n db.%{version}
%patch -p1

%build
cd PORT/linux
%{__make} OORG="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d ${RPM_BUILD_ROOT}%{_prefix}/{include/db1,lib,bin}

sed -n '/^\/\*-/,/^ \*\//s/^.\*.\?//p' include/db.h | grep -v '^@.*db\.h' > LICENSE

cd PORT/linux
sover=`echo libdb.so.* | sed 's/libdb.so.//'`
install libdb.a			$RPM_BUILD_ROOT/%{_libdir}/libdb1.a
install libdb.so.$sover		$RPM_BUILD_ROOT/%{_libdir}/libdb1.so.$sover
ln -sf libdb1.so.$sover 	$RPM_BUILD_ROOT/%{_libdir}/libdb1.so
ln -sf libdb1.so.$sover		$RPM_BUILD_ROOT/%{_libdir}/libdb.so.$sover
install ../include/ndbm.h	$RPM_BUILD_ROOT/%{_includedir}/db1/
install ../../include/db.h	$RPM_BUILD_ROOT/%{_includedir}/db1/
install ../../include/mpool.h	$RPM_BUILD_ROOT/%{_includedir}/db1/
install -s db_dump185		$RPM_BUILD_ROOT/%{_bindir}/db1_dump185
cd ../..

gzip -9nf docs/*.ps README LICENSE changelog

%clean
rm -rf ${RPM_BUILD_ROOT}

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc {README,LICENSE,changelog}.gz
%attr(755,root,root) %{_libdir}/libdb*.so.*
%attr(755,root,root) %{_bindir}/db1_dump185

%files devel
%defattr(644,root,root,755)
%doc docs/*.ps.gz
%attr(755,root,root) %{_libdir}/libdb1.so
%{_includedir}/db1

%files static
%defattr(644,root,root,755)
%{_libdir}/libdb1.a
