#
# Conditional build:
%bcond_with	tests		# build with tests
# TODO:
# PackageKit qt5
#
%define		kdeplasmaver	6.5.4
%define		qtver		5.15.2
%define		kpname		plasma-desktop

Summary:	KDE Plasma Desktop
Name:		kp6-%{kpname}
Version:	6.5.4
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	bf691b719c6bf9febff9452fd511b4dd
URL:		https://www.kde.org/
BuildRequires:	AppStream-qt6-devel
BuildRequires:	Qt6Concurrent-devel >= %{qtver}
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6PrintSupport-devel >= %{qtver}
BuildRequires:	Qt6Quick-devel >= %{qtver}
BuildRequires:	Qt6Sql-devel >= %{qtver}
BuildRequires:	Qt6Svg-devel >= %{qtver}
BuildRequires:	boost-devel
BuildRequires:	cmake >= 3.16.0
BuildRequires:	docbook-dtd45-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	fontconfig-devel
BuildRequires:	ibus-devel
BuildRequires:	ka6-kaccounts-integration-devel
BuildRequires:	kf6-attica-devel
BuildRequires:	kf6-baloo-devel
BuildRequires:	kf6-extra-cmake-modules
BuildRequires:	kf6-karchive-devel
BuildRequires:	kf6-kauth-devel
BuildRequires:	kf6-kcmutils-devel
BuildRequires:	kf6-kconfigwidgets-devel
BuildRequires:	kf6-kdbusaddons-devel
BuildRequires:	kf6-kdeclarative-devel
BuildRequires:	kf6-kded-devel
BuildRequires:	kf6-kdoctools-devel
BuildRequires:	kf6-kglobalaccel-devel
BuildRequires:	kf6-ki18n-devel
BuildRequires:	kf6-kirigami-devel
BuildRequires:	kf6-knewstuff-devel
BuildRequires:	kf6-knotifications-devel
BuildRequires:	kf6-knotifyconfig-devel
BuildRequires:	kf6-kpeople-devel
BuildRequires:	kf6-krunner-devel
BuildRequires:	kf6-kservice-devel
BuildRequires:	kf6-kwallet-devel
BuildRequires:	kf6-kwindowsystem-devel
BuildRequires:	kf6-kxmlgui-devel
BuildRequires:	kf6-qqc2-desktop-style-devel
BuildRequires:	kp6-breeze-devel >= %{kdeplasmaver}
BuildRequires:	kp6-kscreenlocker-devel >= %{kdeplasmaver}
BuildRequires:	kp6-kwin-devel >= %{kdeplasmaver}
BuildRequires:	kp6-libksysguard-devel >= %{kdeplasmaver}
BuildRequires:	kp6-plasma-activities-devel
BuildRequires:	kp6-plasma-activities-stats-devel
BuildRequires:	kp6-plasma-workspace-devel >= %{kdeplasmaver}
BuildRequires:	libaccounts-qt6-devel
BuildRequires:	libcanberra-devel
BuildRequires:	libsignon-qt6-devel
BuildRequires:	libwacom-devel
BuildRequires:	libxkbregistry-devel
BuildRequires:	ninja
BuildRequires:	phonon-qt6-devel
BuildRequires:	pulseaudio-devel
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	scim-devel
BuildRequires:	udev-devel
BuildRequires:	xcb-util-image-devel
BuildRequires:	xcb-util-keysyms-devel
BuildRequires:	xkeyboard-config
BuildRequires:	xorg-driver-input-evdev-devel
BuildRequires:	xorg-driver-input-libinput-devel
BuildRequires:	xorg-driver-input-synaptics-devel
BuildRequires:	xorg-lib-libXcursor-devel
BuildRequires:	xorg-lib-libXft-devel
BuildRequires:	xorg-xserver-server-devel
BuildRequires:	xz
Requires:	%{name}-data = %{version}-%{release}
Requires:	/bin/awk
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	kp5-%{kpname} < 6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
KDE Plasma Desktop.

%package data
Summary:	Data files for %{kpname}
Summary(pl.UTF-8):	Dane dla %{kpname}
Group:		X11/Applications
Requires(post,postun):	desktop-file-utils
Obsoletes:	kp5-%{kpname}-data < 6
BuildArch:	noarch

%description data
Data files for %{kpname}.

%description data -l pl.UTF-8
Dane dla %{kpname}.

%prep
%setup -q -n %{kpname}-%{version}

%build
rm -rf po/id
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir}
%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build
rm -rf $RPM_BUILD_ROOT%{_kdedocdir}/{sr,sr@latin}

# not supported by glibc yet
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ie

%find_lang %{kpname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post data
%update_desktop_database_post

%postun data
%update_desktop_database_postun

%files
%defattr(644,root,root,755)
/etc/xdg/autostart/kaccess.desktop
%attr(755,root,root) %{_bindir}/kaccess
%attr(755,root,root) %{_bindir}/kapplymousetheme
%attr(755,root,root) %{_bindir}/kcm-touchpad-list-devices
%attr(755,root,root) %{_bindir}/knetattach
%attr(755,root,root) %{_bindir}/krunner-plugininstaller
%attr(755,root,root) %{_bindir}/solid-action-desktop-gen
%attr(755,root,root) %{_bindir}/tastenbrett
%ghost %{_libdir}/libkglobalaccelmodel.so.6
%{_libdir}/libkglobalaccelmodel.so.*.*
%{_libdir}/qt6/plugins/kf6/kded/device_automounter.so
%{_libdir}/qt6/plugins/kf6/kded/keyboard.so
%{_libdir}/qt6/plugins/kf6/krunner/krunner_keys.so
%{_libdir}/qt6/plugins/kf6/krunner/krunner_kwin.so
%{_libdir}/qt6/plugins/kf6/krunner/krunner_plasma-desktop.so
%dir %{_libdir}/qt6/qml/org/kde/plasma/activityswitcher
%{_libdir}/qt6/qml/org/kde/plasma/activityswitcher/libactivityswitcherextensionplugin.so
%{_libdir}/qt6/qml/org/kde/plasma/activityswitcher/qmldir
%dir %{_libdir}/qt6/qml/org/kde/plasma/private/kimpanel
%{_libdir}/qt6/qml/org/kde/plasma/private/kimpanel/libkimpanelplugin.so
%{_libdir}/qt6/qml/org/kde/plasma/private/kimpanel/qmldir
%dir %{_libdir}/qt6/qml/org/kde/plasma/private/pager
%{_libdir}/qt6/qml/org/kde/plasma/private/pager/libpagerplugin.so
%{_libdir}/qt6/qml/org/kde/plasma/private/pager/qmldir
%dir %{_libdir}/qt6/qml/org/kde/plasma/private/showdesktop
%{_libdir}/qt6/qml/org/kde/plasma/private/showdesktop/libshowdesktopplugin.so
%{_libdir}/qt6/qml/org/kde/plasma/private/showdesktop/qmldir
%dir %{_libdir}/qt6/qml/org/kde/plasma/private/taskmanager
%{_libdir}/qt6/qml/org/kde/plasma/private/taskmanager/libtaskmanagerplugin.so
%{_libdir}/qt6/qml/org/kde/plasma/private/taskmanager/qmldir
%dir %{_libdir}/qt6/qml/org/kde/private/desktopcontainment
%dir %{_libdir}/qt6/qml/org/kde/private/desktopcontainment/folder
%{_libdir}/qt6/qml/org/kde/private/desktopcontainment/folder/libfolderplugin.so
%{_libdir}/qt6/qml/org/kde/private/desktopcontainment/folder/qmldir
%attr(755,root,root) %{_prefix}/libexec/kimpanel-ibus-panel
%attr(755,root,root) %{_prefix}/libexec/kimpanel-ibus-panel-launcher
%attr(755,root,root) %{_prefix}/libexec/kimpanel-scim-panel
%dir %{_libdir}/qt6/qml/org/kde/plasma/emoji
%{_libdir}/qt6/qml/org/kde/plasma/emoji/libEmojierDeclarativePlugin.so
%{_libdir}/qt6/qml/org/kde/plasma/emoji/qmldir
%{_libdir}/qt6/plugins/kf6/kded/kded_touchpad.so
%dir %{_libdir}/qt6/plugins/plasma/kcminit
%{_libdir}/qt6/plugins/plasma/kcminit/kcm_mouse_init.so
%{_libdir}/qt6/plugins/plasma/kcminit/kcm_touchpad_init.so
%dir %{_libdir}/qt6/plugins/plasma
%dir %{_libdir}/qt6/plugins/plasma/applets
%{_libdir}/qt6/plugins/plasma/applets/org.kde.panel.so
%{_libdir}/qt6/plugins/plasma/applets/org.kde.plasma.kicker.so
%{_libdir}/qt6/plugins/plasma/applets/org.kde.plasma.kickoff.so
%{_libdir}/qt6/plugins/plasma/applets/org.kde.plasma.trash.so
%{_libdir}/qt6/plugins/plasma/applets/org.kde.plasma.windowlist.so
%dir %{_libdir}/qt6/plugins/plasma/kcms
%dir %{_libdir}/qt6/plugins/plasma/kcms/systemsettings
%{_libdir}/qt6/plugins/plasma/kcms/systemsettings/kcm_access.so
%{_libdir}/qt6/plugins/plasma/kcms/systemsettings/kcm_baloofile.so
%{_libdir}/qt6/plugins/plasma/kcms/systemsettings/kcm_kded.so
%{_libdir}/qt6/plugins/plasma/kcms/systemsettings/kcm_keyboard.so
%{_libdir}/qt6/plugins/plasma/kcms/systemsettings/kcm_keys.so
%{_libdir}/qt6/plugins/plasma/kcms/systemsettings/kcm_landingpage.so
%{_libdir}/qt6/plugins/plasma/kcms/systemsettings/kcm_mouse.so
%{_libdir}/qt6/plugins/plasma/kcms/systemsettings/kcm_smserver.so
%{_libdir}/qt6/plugins/plasma/kcms/systemsettings/kcm_splashscreen.so
%{_libdir}/qt6/plugins/plasma/kcms/systemsettings/kcm_tablet.so
%{_libdir}/qt6/plugins/plasma/kcms/systemsettings/kcm_touchpad.so
%{_libdir}/qt6/plugins/plasma/kcms/systemsettings/kcm_workspace.so
%dir %{_libdir}/qt6/plugins/plasma/kcms/systemsettings_qwidgets
%{_libdir}/qt6/plugins/plasma/kcms/systemsettings_qwidgets/kcm_clock.so
%{_libdir}/qt6/plugins/plasma/kcms/systemsettings_qwidgets/kcm_device_automounter.so
%{_libdir}/qt6/plugins/plasma/kcms/systemsettings_qwidgets/kcm_qtquicksettings.so
%{_libdir}/qt6/plugins/plasma/kcms/systemsettings_qwidgets/kcm_solid_actions.so
%{_libdir}/qt6/plugins/plasma/kcms/systemsettings_qwidgets/kcmspellchecking.so
%dir %{_libdir}/qt6/plugins/plasma/kcms/desktop
%{_libdir}/qt6/plugins/plasma/kcms/desktop/kcm_krunnersettings.so
%{_libdir}/qt6/plugins/plasma/kcms/systemsettings/kcm_plasmasearch.so
%{_libdir}/qt6/plugins/plasma/kcms/systemsettings_qwidgets/kcm_recentFiles.so
%attr(755,root,root) %{_bindir}/plasma-emojier
%{_libdir}/qt6/plugins/plasma/kcms/systemsettings/kcm_touchscreen.so
%{_libdir}/qt6/plugins/plasma/kcms/systemsettings/kcm_activities.so
%{_libdir}/qt6/plugins/plasma/kcms/systemsettings/kcm_desktoppaths.so
%{_libdir}/qt6/plugins/plasma/kcms/systemsettings/kcm_gamecontroller.so
%{_libdir}/qt6/qml/org/kde/plasma/activityswitcher/activityswitcherextensionplugin.qmltypes
%{_libdir}/qt6/qml/org/kde/plasma/activityswitcher/kde-qmlmodule.version
%{_libdir}/qt6/qml/org/kde/plasma/emoji/EmojierDeclarativePlugin.qmltypes
%{_libdir}/qt6/qml/org/kde/plasma/emoji/kde-qmlmodule.version
%dir %{_libdir}/qt6/qml/org/kde/plasma/private/kcm_keyboard
%{_libdir}/qt6/qml/org/kde/plasma/private/kcm_keyboard/libkcm_keyboard_declarative.so
%{_libdir}/qt6/qml/org/kde/plasma/private/kcm_keyboard/qmldir
%attr(755,root,root) %{_prefix}/libexec/kf6/kauth/kcmdatetimehelper
%{_libdir}/qt6/plugins/attica_kde.so
%{systemduserunitdir}/plasma-kaccess.service
%{_libdir}/qt6/qml/org/kde/plasma/private/pager/kde-qmlmodule.version
%{_libdir}/qt6/qml/org/kde/plasma/private/pager/pagerplugin.qmltypes
%{_libdir}/qt6/qml/org/kde/private/desktopcontainment/folder/folderplugin.qmltypes
%{_libdir}/qt6/qml/org/kde/private/desktopcontainment/folder/kde-qmlmodule.version
%{_libdir}/qt6/qml/org/kde/plasma/private/kcm_keyboard/kcm_keyboard_declarative.qmltypes
%{_libdir}/qt6/qml/org/kde/plasma/private/kcm_keyboard/kde-qmlmodule.version
%{_libdir}/qt6/qml/org/kde/plasma/private/kimpanel/kde-qmlmodule.version
%{_libdir}/qt6/qml/org/kde/plasma/private/kimpanel/kimpanelplugin.qmltypes
%{_libdir}/qt6/qml/org/kde/plasma/private/showdesktop/kde-qmlmodule.version
%{_libdir}/qt6/qml/org/kde/plasma/private/showdesktop/showdesktopplugin.qmltypes
%{_libdir}/qt6/qml/org/kde/plasma/private/taskmanager/kde-qmlmodule.version
%{_libdir}/qt6/qml/org/kde/plasma/private/taskmanager/taskmanagerplugin.qmltypes

%files data -f %{kpname}.lang
%defattr(644,root,root,755)
%{_desktopdir}/org.kde.knetattach.desktop
%{_desktopdir}/org.kde.plasma.emojier.desktop
%{_datadir}/config.kcfg/kactivitymanagerd_plugins_settings.kcfg
%{_datadir}/config.kcfg/kactivitymanagerd_settings.kcfg
%{_datadir}/config.kcfg/kcmaccessibilitybell.kcfg
%{_datadir}/config.kcfg/kcmaccessibilitykeyboard.kcfg
%{_datadir}/config.kcfg/kcmaccessibilitymouse.kcfg
%{_datadir}/config.kcfg/kcmaccessibilityscreenreader.kcfg
%{_datadir}/config.kcfg/splashscreensettings.kcfg
%{_datadir}/config.kcfg/workspaceoptions_kdeglobalssettings.kcfg
%{_datadir}/config.kcfg/workspaceoptions_plasmasettings.kcfg
%{_datadir}/config.kcfg/kcmaccessibilitycolorblindnesscorrection.kcfg
%{_datadir}/dbus-1/interfaces/org.kde.touchpad.xml
%{_datadir}/dbus-1/system-services/org.kde.kcontrol.kcmclock.service
%{_datadir}/dbus-1/system.d/org.kde.kcontrol.kcmclock.conf
%{_iconsdir}/hicolor/*x*/devices/input*.png
%{_iconsdir}/hicolor/scalable/devices/input-touchpad.svgz
%dir %{_datadir}/kcmkeys
%{_datadir}/kcmkeys/kde3.kksrc
%{_datadir}/kcmkeys/kde4.kksrc
%{_datadir}/kcmkeys/mac4.kksrc
%{_datadir}/kcmkeys/unix3.kksrc
%{_datadir}/kcmkeys/win3.kksrc
%{_datadir}/kcmkeys/win4.kksrc
%{_datadir}/kcmkeys/wm3.kksrc
%dir %{_datadir}/kcmsolidactions
%{_datadir}/kcmsolidactions/solid-action-template.desktop
%{_datadir}/kglobalaccel/org.kde.plasma.emojier.desktop
%{_datadir}/kglobalaccel/org.kde.touchpadshortcuts.desktop
%{_datadir}/knsrcfiles/krunner.knsrc
%{_datadir}/knsrcfiles/ksplash.knsrc
%{_datadir}/metainfo/org.kde.desktopcontainment.appdata.xml
%{_datadir}/metainfo/org.kde.paneltoolbox.appdata.xml
%{_datadir}/metainfo/org.kde.plasma.desktop.appdata.xml
%{_datadir}/metainfo/org.kde.plasma.desktop.appmenubar.appdata.xml
%{_datadir}/metainfo/org.kde.plasma.desktop.defaultPanel.appdata.xml
%{_datadir}/metainfo/org.kde.plasma.desktop.emptyPanel.appdata.xml
%{_datadir}/metainfo/org.kde.plasma.folder.appdata.xml
%{_datadir}/metainfo/org.kde.plasma.icontasks.appdata.xml
%{_datadir}/metainfo/org.kde.plasma.keyboardlayout.appdata.xml
%{_datadir}/metainfo/org.kde.plasma.kimpanel.appdata.xml
%{_datadir}/metainfo/org.kde.plasma.marginsseparator.appdata.xml
%{_datadir}/metainfo/org.kde.plasma.minimizeall.appdata.xml
%{_datadir}/metainfo/org.kde.plasma.pager.appdata.xml
%{_datadir}/metainfo/org.kde.plasma.showActivityManager.appdata.xml
%{_datadir}/metainfo/org.kde.plasma.showdesktop.appdata.xml
%{_datadir}/metainfo/org.kde.plasma.taskmanager.appdata.xml
%{_datadir}/metainfo/org.kde.plasmashell.metainfo.xml
%dir %{_datadir}/plasma/layout-templates
%dir %{_datadir}/plasma/layout-templates/org.kde.plasma.desktop.appmenubar
%dir %{_datadir}/plasma/layout-templates/org.kde.plasma.desktop.appmenubar/contents
%{_datadir}/plasma/layout-templates/org.kde.plasma.desktop.appmenubar/contents/layout.js
%{_datadir}/plasma/layout-templates/org.kde.plasma.desktop.appmenubar/metadata.json
%dir %{_datadir}/plasma/layout-templates/org.kde.plasma.desktop.defaultPanel
%dir %{_datadir}/plasma/layout-templates/org.kde.plasma.desktop.defaultPanel/contents
%{_datadir}/plasma/layout-templates/org.kde.plasma.desktop.defaultPanel/contents/layout.js
%{_datadir}/plasma/layout-templates/org.kde.plasma.desktop.defaultPanel/metadata.json
%dir %{_datadir}/plasma/layout-templates/org.kde.plasma.desktop.emptyPanel
%dir %{_datadir}/plasma/layout-templates/org.kde.plasma.desktop.emptyPanel/contents
%{_datadir}/plasma/layout-templates/org.kde.plasma.desktop.emptyPanel/contents/layout.js
%{_datadir}/plasma/layout-templates/org.kde.plasma.desktop.emptyPanel/metadata.json
%dir %{_datadir}/plasma/packages/org.kde.paneltoolbox
%dir %{_datadir}/plasma/packages/org.kde.paneltoolbox/contents
%dir %{_datadir}/plasma/packages/org.kde.paneltoolbox/contents/ui
%{_datadir}/plasma/packages/org.kde.paneltoolbox/contents/ui/main.qml
%{_datadir}/plasma/packages/org.kde.paneltoolbox/metadata.json
%{_datadir}/plasma/plasmoids/org.kde.desktopcontainment
%{_datadir}/plasma/plasmoids/org.kde.plasma.folder
%{_datadir}/plasma/plasmoids/org.kde.plasma.icontasks
%{_datadir}/plasma/plasmoids/org.kde.plasma.keyboardlayout
%{_datadir}/plasma/plasmoids/org.kde.plasma.kimpanel
%{_datadir}/plasma/plasmoids/org.kde.plasma.marginsseparator
%{_datadir}/plasma/plasmoids/org.kde.plasma.minimizeall
%{_datadir}/plasma/plasmoids/org.kde.plasma.pager
%{_datadir}/plasma/plasmoids/org.kde.plasma.showActivityManager
%{_datadir}/plasma/plasmoids/org.kde.plasma.showdesktop
%{_datadir}/plasma/plasmoids/org.kde.plasma.taskmanager
%{_datadir}/plasma/shells/org.kde.plasma.desktop
%{_datadir}/polkit-1/actions/org.kde.kcontrol.kcmclock.policy
%{_datadir}/solid/devices/solid-device-Battery.desktop
%{_datadir}/solid/devices/solid-device-Block.desktop
%{_datadir}/solid/devices/solid-device-Camera.desktop
%{_datadir}/solid/devices/solid-device-OpticalDisc.desktop
%{_datadir}/solid/devices/solid-device-OpticalDrive.desktop
%{_datadir}/solid/devices/solid-device-PortableMediaPlayer.desktop
%{_datadir}/solid/devices/solid-device-Processor.desktop
%{_datadir}/solid/devices/solid-device-StorageAccess.desktop
%{_datadir}/solid/devices/solid-device-StorageDrive.desktop
%{_datadir}/solid/devices/solid-device-StorageVolume.desktop
%{_datadir}/config.kcfg/landingpage_kdeglobalssettings.kcfg
#%{_datadir}/plasma/services/touchpad.operations
#%{_datadir}/plasma/desktoptheme/default/icons/touchpad.svg
#%{_datadir}/plasma/plasmoids/touchpad
%{_desktopdir}/kcm_access.desktop
%{_desktopdir}/kcm_activities.desktop
%{_desktopdir}/kcm_baloofile.desktop
%{_desktopdir}/kcm_clock.desktop
%{_desktopdir}/kcm_desktoppaths.desktop
%{_desktopdir}/kcm_kded.desktop
%{_desktopdir}/kcm_keyboard.desktop
%{_desktopdir}/kcm_keys.desktop
%{_desktopdir}/kcm_mouse.desktop
%{_desktopdir}/kcm_plasmasearch.desktop
%{_desktopdir}/kcm_qtquicksettings.desktop
%{_desktopdir}/kcm_smserver.desktop
%{_desktopdir}/kcm_solid_actions.desktop
%{_desktopdir}/kcm_splashscreen.desktop
%{_desktopdir}/kcm_tablet.desktop
%{_desktopdir}/kcm_touchpad.desktop
%{_desktopdir}/kcm_workspace.desktop
%{_desktopdir}/kcmspellchecking.desktop
%dir %{_datadir}/kcmmouse
%{_datadir}/kcmmouse/cursor*.pcf.gz
%{_datadir}/kcmmouse/pics
%{_desktopdir}/kcm_krunnersettings.desktop
%{_datadir}/config.kcfg/krunnersettingsbase.kcfg
%{_datadir}/config.kcfg/workspaceoptions_kwinsettings.kcfg
%{_desktopdir}/kcm_landingpage.desktop
%{_desktopdir}/kcm_recentFiles.desktop
%{_datadir}/metainfo/org.kde.plasma.activitypager.appdata.xml
%dir %{_datadir}/plasma/plasmoids/org.kde.plasma.activitypager
%{_datadir}/plasma/plasmoids/org.kde.plasma.activitypager/metadata.json
%{_desktopdir}/kcm_touchscreen.desktop
%{_desktopdir}/kaccess.desktop
%{_desktopdir}/kcm_gamecontroller.desktop
%dir %{_datadir}/kcm_recentFiles
%dir %{_datadir}/kcm_recentFiles/workspace
%dir %{_datadir}/kcm_recentFiles/workspace/settings
%dir %{_datadir}/kcm_recentFiles/workspace/settings/qml
%dir %{_datadir}/kcm_recentFiles/workspace/settings/qml/recentFiles
%{_datadir}/kcm_recentFiles/workspace/settings/qml/recentFiles/ExcludedApplicationView.qml
%{_datadir}/knotifications6/kaccess.notifyrc
##%{_datadir}/knotifications6/kcm_touchpad.notifyrc
%{_datadir}/plasma/emoji
%{_datadir}/qlogging-categories6/kcm_gamecontroller.categories
%{_datadir}/qlogging-categories6/kcm_kded.categories
%{_datadir}/qlogging-categories6/kcm_keyboard.categories
%{_datadir}/qlogging-categories6/kcm_mouse.categories
%{_datadir}/qlogging-categories6/kcm_tablet.categories
%{_datadir}/qlogging-categories6/kcm_touchscreen.categories
%{_datadir}/qlogging-categories6/kcmkeys.categories
%{_datadir}/accounts/providers/kde/opendesktop.provider
%{_datadir}/accounts/services/kde/opendesktop-rating.service
%{_desktopdir}/kde-mimeapps.list
%{_datadir}/sddm/themes/breeze/Background.qml
%{_datadir}/sddm/themes/breeze/KeyboardButton.qml
%{_datadir}/sddm/themes/breeze/Login.qml
%{_datadir}/sddm/themes/breeze/Main.qml
%{_datadir}/sddm/themes/breeze/SessionButton.qml
%{_datadir}/sddm/themes/breeze/default-logo.svg
%{_datadir}/sddm/themes/breeze/faces/.face.icon
%{_datadir}/sddm/themes/breeze/metadata.desktop
%{_datadir}/sddm/themes/breeze/preview.png
%{_datadir}/sddm/themes/breeze/theme.conf
%attr(755,root,root) %{_datadir}/sddm/themes/breeze/Messages.sh
%{_datadir}/config.kcfg/kcmaccessibilityinvert.kcfg
%{_datadir}/config.kcfg/kcmaccessibilityshakecursor.kcfg
%{_datadir}/config.kcfg/kcmaccessibilityzoommagnifier.kcfg
