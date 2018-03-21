
%global		_hardened_build 1

Name:		libntirpc
Version:	1.6.2
Release:	1%{?dev:%{dev}}%{?dist}
Summary:	New Transport Independent RPC Library
Group:		System Environment/Libraries
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

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

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
* Wed Mar 21 2018 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.6.2-1
- libntirpc 1.6.2 GA

* Fri Feb 9 2018 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.6.1-1
- libntirpc 1.6.1 GA

* Mon Jan 29 2018 Kaleb S. KEITHLEY <kkeithle at redhat.com> 1.5.4-1
- libntirpc 1.5.4 GA

* Thu Aug 10 2017 Niels de Vos <ndevos@redhat.com> - 1.5.3-1
- Update to version 1.5.3

* Thu Jun 1 2017 Niels de Vos <ndevos@redhat.com> - 1.5.2-1
- Update to version 1.5.2

* Tue May 30 2017 Niels de Vos <ndevos@redhat.com> - 1.5.1-1
- update libntirpc to 1.5.1 for NFS-Ganesha 2.5

* Tue Nov 22 2016 Niels de Vos <ndevos@redhat.com> - 1.4.3-1
- update libntirpc to 1.4.3 for NFS-Ganesha 2.4

* Wed Jul 27 2016 Niels de Vos <ndevos@redhat.com> - 1.3.1-3
- Rebuilt for CentOS Storage SIG, new ppc64le architecture

* Fri Apr 22 2016 Niels de Vos <ndevos@redhat.com> - 1.3.1-2
- Rebuild for Aarch64

* Thu Nov 12 2015 Niels de Vos <ndevos@redhat.com> - 1.3.1-1
- Rename back to libntirpc, Fedora will keep that name

* Fri Oct 30 2015 Niels de Vos <ndevos@redhat.com> - 1.3.1-1
- Import from current Fedora Rawhide libntirpc package
- Disable jemalloc usage
