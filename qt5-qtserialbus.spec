#
# Conditional build:
%bcond_without	doc	# Documentation

%define		orgname		qtserialbus
%define		qtbase_ver		%{version}
%define		qttools_ver		%{version}
Summary:	The Qt5 SerialBus library
Summary(pl.UTF-8):	Biblioteka Qt5 SerialBus
Name:		qt5-%{orgname}
Version:	5.15.15
Release:	1
License:	LGPL v3 or GPL v2+ or commercial
Group:		X11/Libraries
Source0:	https://download.qt.io/official_releases/qt/5.15/%{version}/submodules/%{orgname}-everywhere-opensource-src-%{version}.tar.xz
# Source0-md5:	bb35f1cda75a7cc7e79ef92b2fe2e9af
URL:		https://www.qt.io/
BuildRequires:	Qt5Core-devel >= %{qtbase_ver}
BuildRequires:	Qt5Network-devel >= %{qtbase_ver}
%if %{with doc}
BuildRequires:	qt5-assistant >= %{qttools_ver}
BuildRequires:	qt5-doc-common >= %{qttools_ver}
%endif
BuildRequires:	qt5-build >= %{qtbase_ver}
BuildRequires:	qt5-qmake >= %{qtbase_ver}
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.016
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing
%define		qt5dir		%{_libdir}/qt5

%description
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.

This package contains Qt5 SerialBus library.

%description -l pl.UTF-8
Qt to wieloplatformowy szkielet aplikacji i interfejsów użytkownika.
Przy użyciu Qt można pisać aplikacje powiązane z WWW i wdrażać je w
systemach biurkowych, przenośnych i wbudowanych bez przepisywania kodu
źródłowego.

Ten pakiet zawiera bibliotekę Qt5 SerialBus.

%package -n Qt5SerialBus
Summary:	The Qt5 SerialBus library
Summary(pl.UTF-8):	Biblioteka Qt5 SerialBus
Group:		X11/Libraries
%requires_eq_to	Qt5Core Qt5Core-devel
Requires:	Qt5Network >= %{qtbase_ver}

%description -n Qt5SerialBus
Qt5 SerialBus library.

%description -n Qt5SerialBus -l pl.UTF-8
Biblioteka Qt5 SerialBus.

%package -n Qt5SerialBus-devel
Summary:	Qt5 SerialBus - development files
Summary(pl.UTF-8):	Biblioteka Qt5 SerialBus - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	Qt5Core-devel >= %{qtbase_ver}
Requires:	Qt5SerialBus = %{version}-%{release}

%description -n Qt5SerialBus-devel
Qt5 SerialBus - development files.

%description -n Qt5SerialBus-devel -l pl.UTF-8
Biblioteka Qt5 SerialBus - pliki programistyczne.

%package doc
Summary:	Qt5 SerialBus documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 SerialBus w formacie HTML
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
BuildArch:	noarch

%description doc
Qt5 SerialBus documentation in HTML format.

%description doc -l pl.UTF-8
Dokumentacja do biblioteki Qt5 SerialBus w formacie HTML.

%package doc-qch
Summary:	Qt5 SerialBus documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 SerialBus w formacie QCH
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
BuildArch:	noarch

%description doc-qch
Qt5 SerialBus documentation in QCH format.

%description doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt5 SerialBus w formacie QCH.

%package examples
Summary:	Qt5 SerialBus examples
Summary(pl.UTF-8):	Przykłady do biblioteki Qt5 SerialBus
Group:		X11/Development/Libraries
BuildArch:	noarch

%description examples
Qt5 SerialBus examples.

%description examples -l pl.UTF-8
Przykłady do biblioteki Qt5 SerialBus.

%prep
%setup -q -n %{orgname}-everywhere-src-%{version}

%build
%{qmake_qt5}
%{__make}
%{?with_doc:%{__make} docs}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%if %{with doc}
%{__make} install_docs \
	INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

# useless symlinks
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.so.5.??
# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n Qt5SerialBus -p /sbin/ldconfig
%postun	-n Qt5SerialBus -p /sbin/ldconfig

%files -n Qt5SerialBus
%defattr(644,root,root,755)
%doc dist/changes-*
# R: Qt5Core Qt5Network Qt5SerialPort
%attr(755,root,root) %{_libdir}/libQt5SerialBus.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5SerialBus.so.5
# R: Qt5Core Qt5SerialBus
%attr(755,root,root) %{qt5dir}/bin/canbusutil
%dir %{qt5dir}/plugins/canbus
%attr(755,root,root) %{qt5dir}/plugins/canbus/libqtpassthrucanbus.so
%attr(755,root,root) %{qt5dir}/plugins/canbus/libqtpeakcanbus.so
%attr(755,root,root) %{qt5dir}/plugins/canbus/libqtsocketcanbus.so
%attr(755,root,root) %{qt5dir}/plugins/canbus/libqttinycanbus.so
%attr(755,root,root) %{qt5dir}/plugins/canbus/libqtvirtualcanbus.so

%files -n Qt5SerialBus-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5SerialBus.so
%{_libdir}/libQt5SerialBus.prl
%{_includedir}/qt5/QtSerialBus
%{_pkgconfigdir}/Qt5SerialBus.pc
%{_libdir}/cmake/Qt5SerialBus
%{qt5dir}/mkspecs/modules/qt_lib_serialbus.pri
%{qt5dir}/mkspecs/modules/qt_lib_serialbus_private.pri

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtserialbus

%files doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtserialbus.qch
%endif

%files examples
%defattr(644,root,root,755)
# XXX: dir shared with qt5-qtbase-examples
%dir %{_examplesdir}/qt5
%{_examplesdir}/qt5/serialbus
