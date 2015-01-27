%{?scl:%scl_package Judy}
%{!?scl:%global pkg_name %{name}}

Name:		%{?scl_prefix}Judy
Version:	1.0.5
Release:	12%{?dist}
Summary:	General purpose dynamic array
Group:		System Environment/Libraries
License:	LGPLv2+
URL:		http://sourceforge.net/projects/judy/
Source0:	http://downloads.sf.net/judy/Judy-%{version}.tar.gz
Source1:	README.distro
# Make tests use shared instead of static libJudy
Patch0:		Judy-1.0.4-test-shared.patch
# The J1* man pages were incorrectly being symlinked to Judy, rather than Judy1
# This patch corrects that; submitted upstream 2008/11/27
Patch1:		Judy-1.0.4-fix-Judy1-mans.patch
# Fix some code with undefined behavior, commented on and removed by gcc
Patch2:		Judy-1.0.5-undefined-behavior.patch

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
%patch2 -p1 -b .behavior
cp -p %{SOURCE1} .

# make libtool able to handle soname in format sclname-1
sed -i -r 's|(major=\.)(`expr)|\1$verstring_prefix\2|' ltmain.sh

%build
export CFLAGS="%{optflags} -fno-strict-aliasing -fno-tree-ccp -fno-tree-dominator-opts -fno-tree-copy-prop -fno-tree-vrp"
%configure --disable-static
%{?scl_prefix:export verstring_prefix="%{scl_prefix}"}
make
#%{?_smp_mflags}
# fails to compile properly with parallel make:
# http://sourceforge.net/tracker/index.php?func=detail&aid=2129019&group_id=55753&atid=478138

%install
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

%files
%doc AUTHORS ChangeLog COPYING README README.distro examples/
%{_libdir}/libJudy.so.*

%files devel
%doc doc
%{_includedir}/Judy.h
%{_libdir}/libJudy.so
%{_mandir}/man3/J*.3*

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
* Tue Jan 27 2015 Honza Horak <hhorak@redhat.com> - 1.0.5-12
- Rename README.Fedora to README.distro

* Sun Jan 25 2015 Honza Horak <hhorak@redhat.com> - 1.0.5-11
- Convert to SCL package

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb 18 2014 Paul Howarth <paul@city-fan.org> - 1.0.5-8
- Fix some code with undefined behavior
- Build with -fno-strict-aliasing
- Disable various compiler tree optimizations that trigger reproducible
  crashes in gtkwave without generating compiler warnings (#1064090)

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jan  6 2012 Paul Howarth <paul@city-fan.org> - 1.0.5-3
- Rebuilt for gcc 4.7

* Mon Feb  7 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 18 2010 Paul Howarth <paul@city-fan.org> - 1.0.5-1
- Update to 1.0.5
  - Added proper clean targets to enable multiple builds
  - Added examples directory
  - Correctly detects 32/64-bit build environment
  - Allow explicit configure for 32/64-bit environment
- Cosmetic spec file clean-ups

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Dec 13 2008 Charles R. Anderson <cra@wpi.edu> - 1.0.4-4
- For Judy1 man page fix, patch Makefile.{am,in} instead of
  relying on autotools to regenerate the latter
- Add README.Fedora with upstream's license explanation

* Sun Nov 30 2008 Charles R. Anderson <cra@wpi.edu> - 1.0.4-3
- Fix Judy1 man page symlinks
- Use valid tag License: LGPLv2+ confirmed with upstream
- Use version macro in Source0
- Remove Makefiles from installed doc tree

* Thu Nov 27 2008 Charles R. Anderson <cra@wpi.edu> - 1.0.4-2
- Patch tests to run with shared library
- Run tests in check section

* Sun Oct 05 2008 Charles R. Anderson <cra@wpi.edu> - 1.0.4-1
- Initial package for Fedora
