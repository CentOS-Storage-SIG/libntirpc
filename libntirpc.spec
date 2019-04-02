
%global		_hardened_build 1

Name:		libntirpc
Version:	1.7.2
Release:	1%{?dev:%{dev}}%{?dist}
Summary:	New Transport Independent RPC Library
License:	BSD
Url:		https://github.com/nfs-ganesha/ntirpc

Source0:	https://github.com/nfs-ganesha/ntirpc/archive/v%{version}/ntirpc-%{version}.tar.gz

BuildRequires:	gcc cmake
BuildRequires:	krb5-devel
%if ( 0%{?fedora} && 0%{?fedora} > 27 )
BuildRequires:  libnsl2-devel
%endif
# libtirpc has /etc/netconfig, most machines probably have it anyway
# for NFS client
Requires:	libtirpc

%description
This package contains a new implementation of the original libtirpc, 
transport-independent RPC (TI-RPC) library for NFS-Ganesha. It has
the following features not found in libtirpc:
 1. Bi-directional operation
 2. Full-duplex operation on the TCP (vc) transport
 3. Thread-safe operating modes
 3.1 new locking primitives and lock callouts (interface change)
 3.2 stateless send/recv on the TCP transport (interface change)
 4. Flexible server integration support
 5. Event channels (remove static arrays of xprt handles, new EPOLL/KEVENT
    integration)

%package devel
Summary:	Development headers for %{name}
Requires:	%{name}%{?_isa} = %{version}

%description devel
Development headers and auxiliary files for developing with %{name}.

%prep
%setup -q -n ntirpc-%{version}

%build
%cmake . -DOVERRIDE_INSTALL_PREFIX=/usr -DTIRPC_EPOLL=1 -DUSE_GSS=ON "-GUnix Makefiles"

make %{?_smp_mflags}

%install
## make install is broken in various ways
## make install DESTDIR=%%{buildroot}
mkdir -p %{buildroot}%{_libdir}/pkgconfig
install -p -m 0755 src/%{name}.so.%{version} %{buildroot}%{_libdir}/
ln -s %{name}.so.%{version} %{buildroot}%{_libdir}/%{name}.so.1
ln -s %{name}.so.%{version} %{buildroot}%{_libdir}/%{name}.so
mkdir -p %{buildroot}%{_includedir}/ntirpc
cp -a ntirpc %{buildroot}%{_includedir}/
install -p -m 644 libntirpc.pc %{buildroot}%{_libdir}/pkgconfig/

%files
%{_libdir}/libntirpc.so.*
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc NEWS README

%files devel
%{_libdir}/libntirpc.so
%{_includedir}/ntirpc/
%{_libdir}/pkgconfig/libntirpc.pc

%changelog
* Wed Feb 27 2019 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.7.2-1
- libntirpc 1.7.2 GA

* Wed Feb 20 2019 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.7.1-1
- rebuild for f31/rawhide

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct 16 2018 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.7.1-1
- libntirpc 1.7.1 GA

* Mon Sep 17 2018 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.7.0-1
- libntirpc 1.7.0 GA

* Wed Aug 22 2018 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.6.3-1
- libntirpc 1.6.3 GA

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Mar 20 2018 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.6.2-1
- libntirpc 1.6.2 GA

* Mon Feb 19 2018 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.6.1-3
- gcc BuildRoot

* Thu Feb 15 2018 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.6.1-2
- ldconfig

* Fri Feb 9 2018 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.6.1-1
- libntirpc 1.6.1 GA

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 17 2018 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.6.0-1
- libntirpc 1.6.0 GA

* Thu Oct 19 2017 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.5.3-4
- libntirpc 1.5.3 PR https://github.com/nfs-ganesha/ntirpc/pull/85

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.5.3-1
- libntirpc 1.5.3 GA

* Tue May 30 2017 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.5.2-1
- libntirpc 1.5.2 GA

* Mon May 8 2017 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.5.1-1
- libntirpc 1.5.1 GA

* Fri Apr 21 2017 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.5.0-1
- libntirpc 1.5.0 GA

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Oct 25 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.4.3-1
- libntirpc 1.4.3 GA

* Tue Oct 25 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.4.2-1
- libntirpc 1.4.2 GA

* Tue Sep 20 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.4.1-1
- libntirpc 1.4.1 GA

* Mon Sep 19 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.4.0-1
- libntirpc 1.4.0 GA

* Tue Sep 6 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.4.0-0.4pre3
- libntirpc 1.4.0-pre3, without jemalloc

* Thu Aug 4 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.4.0-0.3pre3
- libntirpc 1.4.0-pre3

* Mon Feb 29 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.4.0-0.2pre2
- libntirpc 1.4.0-pre2

* Fri Feb 5 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.4.0-0.1pre1
- libntirpc 1.4.0-pre1, correct release

* Fri Feb 5 2016 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.4.0-1pre1
- libntirpc 1.4.0-pre1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 9 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com>
- Requires: libtirpc for /etc/netconfig (most already have it)

* Mon Oct 26 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.3.1-1
- libntirpc 1.3.1 GA

* Fri Oct 9 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.3.0-3
- libntirpc 1.3.0 GA, w/ -DTIRPC_EPOLL=ON

* Wed Sep 9 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.3.0-2
- libntirpc 1.3.0 GA, w/ correct top-level CMakeList.txt

* Wed Sep 9 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.3.0-1
- libntirpc 1.3.0 GA

* Thu Jul 16 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.2.1-3
- RHEL 6 finally has new enough cmake
- use -isystem ... to ensure correct <rpc/rpc*.h> are used
- ensure -DTIRPC_EPOLL is defined for correct evchan functionality

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 23 2015 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.2.1-1
- Initial commit
