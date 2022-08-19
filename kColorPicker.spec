#
# Conditional build:
%bcond_with	tests		# build with tests
Summary:	Qt based Color Picker with popup menu
Name:		kColorPicker
Version:	0.2.0
Release:	1
License:	GPL v2+
Group:		X11/Libraries
Source0:	https://github.com/ksnip/kColorPicker/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	58a14db496f2e782be9abc4b604b5334
URL:		https://github.com/ksnip/kColorPicker/
BuildRequires:	Qt5Gui-devel >= 5.15.2
BuildRequires:	cmake >= 2.8.12
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Qt based Color Picker with popup menu.

%package devel
Summary:	Header files for %{name} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{name}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	cmake >= 3.16

%description devel
Header files for %{name} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{name}.

%prep
%setup -q
#%patch0

%build
install -d build
cd build
%cmake \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DHTML_INSTALL_DIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	..
%ninja_build

%if %{with tests}
ctest
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libkColorPicker.so.*.*.*
%ghost %{_libdir}/libkColorPicker.so.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libkColorPicker.so
%{_includedir}/kColorPicker
%{_libdir}/cmake/kColorPicker
