Name: libfcrypto
Version: 20240414
Release: 1
Summary: Library to support encryption formats
Group: System Environment/Libraries
License: LGPL-3.0-or-later
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libfcrypto
 
BuildRequires: gcc 

%description -n libfcrypto
Library to support encryption formats

%package -n libfcrypto-static
Summary: Library to support encryption formats
Group: Development/Libraries
Requires: libfcrypto = %{version}-%{release}

%description -n libfcrypto-static
Static library version of libfcrypto.

%package -n libfcrypto-devel
Summary: Header files and libraries for developing applications for libfcrypto
Group: Development/Libraries
Requires: libfcrypto = %{version}-%{release}

%description -n libfcrypto-devel
Header files and libraries for developing applications for libfcrypto.

%package -n libfcrypto-python3
Summary: Python 3 bindings for libfcrypto
Group: System Environment/Libraries
Requires: libfcrypto = %{version}-%{release} python3
BuildRequires: python3-devel python3-setuptools

%description -n libfcrypto-python3
Python 3 bindings for libfcrypto

%prep
%setup -q

%build
%configure --prefix=/usr --libdir=%{_libdir} --mandir=%{_mandir} --enable-python
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -n libfcrypto
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so.*

%files -n libfcrypto-static
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.a

%files -n libfcrypto-devel
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so
%{_libdir}/pkgconfig/libfcrypto.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n libfcrypto-python3
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.so

%changelog
* Sun Apr 14 2024 Joachim Metz <joachim.metz@gmail.com> 20240414-1
- Auto-generated

