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
Release: 9
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
BuildRequires: pkgconfig(gnome-doc-utils)
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


%changelog
* Sun May 22 2011 Funda Wang <fwang@mandriva.org> 0.9.2-8mdv2011.0
+ Revision: 677087
- rebuild to add gconf2 as req

* Thu May 05 2011 Funda Wang <fwang@mandriva.org> 0.9.2-7
+ Revision: 669120
- br gconf2

  + Oden Eriksson <oeriksson@mandriva.com>
    - mass rebuild

* Thu Sep 30 2010 Funda Wang <fwang@mandriva.org> 0.9.2-6mdv2011.0
+ Revision: 582166
- add missing requires

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9.2-5mdv2010.1
+ Revision: 523696
- rebuilt for 2010.1

* Wed Aug 26 2009 Frederic Crozat <fcrozat@mandriva.com> 0.9.2-4mdv2010.0
+ Revision: 421495
- Patch2 (Fedora): fix object registration (fdo bug #23297, mdv bug #50486)
- Patch3 (Fedora): don't spawn when running under GDM
- Patch4 (Fedora): fix clickable button

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 0.9.2-3mdv2009.1
+ Revision: 351641
- rebuild

* Wed Sep 10 2008 Frederic Crozat <fcrozat@mandriva.com> 0.9.2-2mdv2009.0
+ Revision: 283605
- Patch0: fix i18n init
- Patch1: fix for user with non-UTF8 locale

* Thu Aug 21 2008 Frederic Crozat <fcrozat@mandriva.com> 0.9.2-1mdv2009.0
+ Revision: 274505
- fix BR
- Release 0.9.2
- Remove some obsolete buildrequires

* Thu Aug 07 2008 Götz Waschk <waschk@mandriva.org> 0.9-1mdv2009.0
+ Revision: 266054
- new version
- update deps
- handle gconf schema

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 0.8-2mdv2009.0
+ Revision: 265532
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Tue May 06 2008 Götz Waschk <waschk@mandriva.org> 0.8-1mdv2009.0
+ Revision: 201966
- new version
- drop patches
- bump policykit dep

* Mon Mar 03 2008 Frederic Crozat <fcrozat@mandriva.com> 0.7-3mdv2008.1
+ Revision: 178122
- Patch0 (GIT): don't crash if user has no .face
- Patch1 (GIT): show user list when needed
- Patch2 (GIT): remove some icon warnings
- Move menu try to Tools/System Tools

* Mon Feb 25 2008 Götz Waschk <waschk@mandriva.org> 0.7-2mdv2008.1
+ Revision: 175150
- fix devel provides

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Dec 06 2007 Frederic Crozat <fcrozat@mandriva.com> 0.7-1mdv2008.1
+ Revision: 115952
- Fix BuildRequires
- import policykit-gnome


