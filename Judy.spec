Name:		Judy
Version:	1.0.5
Release:	3%{?dist}
Summary:	General purpose dynamic array
Group:		System Environment/Libraries
License:	LGPLv2+
URL:		http://sourceforge.net/projects/judy/
Source0:	http://downloads.sf.net/judy/Judy-%{version}.tar.gz
Source1:	README.Fedora
# Make tests use shared instead of static libJudy
Patch0:		Judy-1.0.4-test-shared.patch
# The J1* man pages were incorrectly being symlinked to Judy, rather than Judy1
# This patch corrects that; submitted upstream 2008/11/27
Patch1:		Judy-1.0.4-fix-Judy1-mans.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Judy is a C library that provides a state-of-the-art core technology
that implements a sparse dynamic array. Judy arrays are declared
simply with a null pointer. A Judy array consumes memory only when it
is populated, yet can grow to take advantage of all available memory
if desired. Judy's key benefits are scalability, high performance, and
memory efficiency. A Judy array is extensible and can scale up to a
very large number of elements, bounded only by machine memory. Since
Judy is designed as an unbounded array, the size of a Judy array is
not pre-allocated but grows and shrinks dynamically with the array
population.

%package devel
Summary:	Development libraries and headers for Judy
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the development libraries and header files
for developing applications that use the Judy library.

%prep
%setup -q -n judy-%{version}
%patch0 -p1 -b .test-shared
%patch1 -p1 -b .fix-Judy1-mans
cp -p %{SOURCE1} .

%build
%configure --disable-static
make 
#%{?_smp_mflags}
# fails to compile properly with parallel make:
# http://sourceforge.net/tracker/index.php?func=detail&aid=2129019&group_id=55753&atid=478138

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="install -p"
# get rid of static libs and libtool archives
rm -f %{buildroot}%{_libdir}/*.{a,la}
# clean out zero length and generated files from doc tree
rm -rf doc/man
rm -f doc/Makefile* doc/ext/README_deliver
[ -s doc/ext/COPYRIGHT ] || rm -f doc/ext/COPYRIGHT
[ -s doc/ext/LICENSE ] || rm -f doc/ext/LICENSE

%check
cd test
./Checkit
cd -

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README README.Fedora examples/
%{_libdir}/libJudy.so.*

%files devel
%defattr(-,root,root,-)
%doc doc
%{_includedir}/Judy.h
%{_libdir}/libJudy.so
%{_mandir}/man3/J*.3*

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
* Fri Jan  6 2012 Paul Howarth <paul@city-fan.org> 1.0.5-3
- rebuilt for gcc 4.7

* Mon Feb  7 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1.0.5-2
- rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 18 2010 Paul Howarth <paul@city-fan.org> 1.0.5-1
- update to 1.0.5
  - added proper clean targets to enable multiple builds
  - added examples directory
  - correctly detects 32/64-bit build environment
  - allow explicit configure for 32/64-bit environment
- cosmetic spec file clean-ups

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1.0.4-6
- rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1.0.4-5
- rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Dec 13 2008 Charles R. Anderson <cra@wpi.edu> 1.0.4-4
- for Judy1 man page fix, patch Makefile.{am,in} instead of
  relying on autotools to regenerate the latter
- add README.Fedora with upstream's license explanation

* Thu Nov 30 2008 Charles R. Anderson <cra@wpi.edu> 1.0.4-3
- fix Judy1 man page symlinks
- use valid tag License: LGPLv2+ confirmed with upstream
- use version macro in Source0
- remove Makefiles from installed doc tree

* Thu Nov 27 2008 Charles R. Anderson <cra@wpi.edu> 1.0.4-2
- patch tests to run with shared library
- run tests in check section

* Sun Oct 05 2008 Charles R. Anderson <cra@wpi.edu> 1.0.4-1
- initial package for Fedora
