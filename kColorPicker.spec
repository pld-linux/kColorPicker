#
# Conditional build:
%bcond_with	tests		# build with tests
%bcond_without	qt5		# build without qt5 version
%bcond_without	qt6		# build without qt6 version
Summary:	Qt based Color Picker with popup menu
Name:		kColorPicker
Version:	0.3.1
Release:	1
License:	GPL v2+
Group:		X11/Libraries
Source0:	https://github.com/ksnip/kColorPicker/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	1efc91252446af0d7e5c467ea7d517e7
URL:		https://github.com/ksnip/kColorPicker/
%{?with_qt5:BuildRequires:	Qt5Gui-devel >= 5.15.2}
%{?with_qt6:BuildRequires:	Qt6Gui-devel}
BuildRequires:	cmake >= 3.20
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Qt based Color Picker with popup menu.

%package qt5
Summary:	Qt5 based Color Picker with popup menu
Obsoletes:	%{name} < 0.3.1
Conflicts:	%{name}-qt6

%description qt5
Qt5 based Color Picker with popup menu.

%package qt5-devel
Summary:	Header files for %{name}-qt5 development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{name}-qt5
Group:		X11/Development/Libraries
Requires:	%{name}-qt5 = %{version}-%{release}
Requires:	cmake >= 3.20
Obsoletes:	%{name}-devel < 0.3.1

%description qt5-devel
Header files for %{name}-qt5 development.

%description qt5-devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{name}-qt5.

%package qt6
Summary:	Qt6 based Color Picker with popup menu
Conflicts:	%{name}-qt5

%description qt6
Qt6 based Color Picker with popup menu.

%package qt6-devel
Summary:	Header files for %{name}-qt6 development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{name}-qt6
Group:		X11/Development/Libraries
Requires:	%{name}-qt6 = %{version}-%{release}
Requires:	cmake >= 3.20

%description qt6-devel
Header files for %{name}-qt6 development.

%description qt6-devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{name}-qt6.


%prep
%setup -q
#%patch0

%build
%if %{with qt5}
%cmake -B build-qt5 \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DHTML_INSTALL_DIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build-qt5

%if %{with tests}
ctest --test-dir build-qt5
%endif
%endif

%if %{with qt6}
%cmake -B build-qt6 \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DBUILD_WITH_QT6=ON \
	-DHTML_INSTALL_DIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build-qt6

%if %{with tests}
ctest --test-dir build-qt6
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{?with_qt5:%ninja_install -C build-qt5}
%{?with_qt6:%ninja_install -C build-qt6}

%clean
rm -rf $RPM_BUILD_ROOT

%post	qt5 -p /sbin/ldconfig
%postun	qt5 -p /sbin/ldconfig
%post	qt6 -p /sbin/ldconfig
%postun	qt6 -p /sbin/ldconfig

%if %{with qt5}
%files qt5
%defattr(644,root,root,755)
%ghost %{_libdir}/libkColorPicker.so.0
%attr(755,root,root) %{_libdir}/libkColorPicker.so.*.*

%files qt5-devel
%defattr(644,root,root,755)
%{_includedir}/kColorPicker-Qt5
%{_libdir}/cmake/kColorPicker-Qt5
%{_libdir}/libkColorPicker.so
%endif

%if %{with qt6}
%files qt6
%defattr(644,root,root,755)
%defattr(644,root,root,755)
%ghost %{_libdir}/libkColorPicker.so.0
%attr(755,root,root) %{_libdir}/libkColorPicker.so.*.*

%files qt6-devel
%defattr(644,root,root,755)
%{_includedir}/kColorPicker-Qt6
%{_libdir}/cmake/kColorPicker-Qt6
%{_libdir}/libkColorPicker.so
%endif
