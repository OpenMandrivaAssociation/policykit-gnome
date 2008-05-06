%define dbus_version		0.90
%define dbus_glib_version	0.71
%define gtk2_version		2.12
%define gnome_vfs2_version	2.4
%define libsexy_version		0.1.11
%define gnome_doc_utils_version 0.3.2
%define polkit_version		0.8
%define intltool_version	0.35

%define pkgname PolicyKit-gnome

%define lib_major 0
%define lib_name %mklibname polkit-gnome %{lib_major}
%define lib_name_devel %mklibname polkit-gnome -d

Summary: PolicyKit integration for the GNOME desktop
Name: policykit-gnome
Version: 0.8
Release: %mkrel 1
License: GPLV2+
Group: System/Libraries
URL: http://gitweb.freedesktop.org/?p=users/david/PolicyKit-gnome.git;a=summary
Source0: http://hal.freedesktop.org/releases/%{pkgname}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: dbus-devel  >= %{dbus_version}
BuildRequires: dbus-glib-devel >= %{dbus_glib_version}
BuildRequires: dbus-glib >= %{dbus_glib_version}
BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: gnome-vfs2-devel >= %{gnome_vfs2_version}
BuildRequires: libsexy-devel >= %{libsexy_version}
BuildRequires: polkit-devel >= %{polkit_version}
BuildRequires: gnome-doc-utils >= %{gnome_doc_utils_version}
BuildRequires: intltool >= %{intltool_version}
BuildRequires: gettext
BuildRequires: desktop-file-utils
BuildRequires: gtk-doc
Requires: policykit >= %{polkit_version}
Provides: %{pkgname} = %{version}-%{release}

%description 
PolicyKit-gnome provides a GNOME integration library and tools for
PolicyKit including an Authentication Agent that matches the look and
feel of the GNOME desktop.

%package -n %{lib_name}
Summary: PolicyKit integration for the GNOME desktop
Group: System/Libraries
License: LGPLv2+
Requires: %{name} >= %{version}

%description -n %{lib_name}
PolicyKit-gnome provides a GNOME integration library and tools for
PolicyKit including an Authentication Agent that matches the look and
feel of the GNOME desktop.

%package -n %{lib_name_devel}
Summary: Headers, libraries and API docs for PolicyKit-gnome
Group: Development/C
License: LGPLv2+
Requires: %{name} >= %{version}
Provides: %name-devel = %version-%release

%description -n %{lib_name_devel}
This package provides headers, libraries and API docs for
PolicyKit-gnome.

%package demo
Summary: Demo application for PolicyKit-gnome
Group: Development/C
License: GPLv2+
Requires: %{name} = %{version}-%{release}

%description demo 
Policy-gnome-demo provides a sample application that demonstrates the
features of both PolicyKit and PolicyKit-gnome. You normally don't
want to have this package installed.

%prep
%setup -q -n %{pkgname}-%{version}

%build
%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std

desktop-file-install --vendor="" \
  --add-category="GNOME" \
  --add-category="GTK" \
  --add-category="System" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*


%find_lang %{pkgname}

# remove unpackaged files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.{la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %{lib_name} -p /sbin/ldconfig

%postun -n %{lib_name} -p /sbin/ldconfig


%files -f %{pkgname}.lang
%defattr(-,root,root,-)
%doc README AUTHORS NEWS COPYING HACKING TODO

%{_bindir}/polkit-gnome-authorization
%{_libexecdir}/polkit-gnome-manager
%{_datadir}/dbus-1/services/org.gnome.PolicyKit.service
%{_datadir}/dbus-1/services/org.gnome.PolicyKit.AuthorizationManager.service
%{_datadir}/dbus-1/services/gnome-org.freedesktop.PolicyKit.AuthenticationAgent.service
%{_datadir}/applications/polkit-gnome-authorization.desktop

%files -n %{lib_name}
%defattr(-,root,root,-)
%{_libdir}/*.so.%{lib_major}*

%files -n %{lib_name_devel}
%defattr(-,root,root,-)
%doc %{_datadir}/gtk-doc/html/*
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*

%files demo
%defattr(-,root,root,-)
%{_bindir}/polkit-gnome-example
%{_datadir}/PolicyKit/policy/polkit-gnome-example.policy
