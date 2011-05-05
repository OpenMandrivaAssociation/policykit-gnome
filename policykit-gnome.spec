%define dbus_version		0.90
%define dbus_glib_version	0.71
%define gtk2_version		2.13.6
%define gnome_doc_utils_version 0.3.2
%define polkit_version		0.9
%define intltool_version	0.35

%define pkgname PolicyKit-gnome

%define lib_major 0
%define lib_name %mklibname polkit-gnome %{lib_major}
%define lib_name_devel %mklibname polkit-gnome -d

Summary: PolicyKit integration for the GNOME desktop
Name: policykit-gnome
Version: 0.9.2
Release: %mkrel 7
License: GPLV2+
Group: System/Libraries
URL: http://gitweb.freedesktop.org/?p=users/david/PolicyKit-gnome.git;a=summary
Source0: http://hal.freedesktop.org/releases/%{pkgname}-%{version}.tar.bz2
# (fc) 0.9.2-2mdv fix i18n init
Patch0: PolicyKit-gnome-0.9.2-i18ninit.patch
# (fc) 0.9.2-2mdv fix for use with non UTF8 locale
Patch1: PolicyKit-gnome-0.9.2-nonutf8.patch
# (fc) 0.9.2-4mdv fix object registration (fdo bug #23297, mdv bug #50486) (Fedora)
Patch2: PolicyKit-gnome-0.9.2-fix-manager-object-path-fdo-23297.patch
# (fc) 0.9.2-4mdv don't spawn when running under GDM (Fedora)
Patch3: PolicyKit-gnome-0.9.2-dont-spawn-when-running-under-gdm.patch
# (fc) 0.9.2-4mdv fix clickable button (Fedora)
Patch4: PolicyKit-gnome-0.9.2-fix-clickable-buttons.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: dbus-devel  >= %{dbus_version}
BuildRequires: dbus-glib-devel >= %{dbus_glib_version}
BuildRequires: dbus-glib >= %{dbus_glib_version}
BuildRequires: libGConf2-devel GConf2
BuildRequires: gtk2-devel >= %{gtk2_version}
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
Requires: %{lib_name} = %{version}-%{release}
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
%patch0 -p1 -b .i18ninit
%patch1 -p1 -b .nonutf8
%patch2 -p1 -b .fix-manager-path
%patch3 -p1 -b .no-spawning-under-gdm
%patch4 -p1 -b .fix-clickable-buttons

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

%if %mdkversion < 200900
%post -n %{lib_name} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{lib_name} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post
%post_install_gconf_schemas polkit-gnome
%endif

%preun
%preun_uninstall_gconf_schemas polkit-gnome

%files -f %{pkgname}.lang
%defattr(-,root,root,-)
%doc README AUTHORS NEWS COPYING HACKING TODO
%_sysconfdir/gconf/schemas/polkit-gnome.schemas
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
%_datadir/PolicyKit/policy/org.gnome.policykit.examples.policy
