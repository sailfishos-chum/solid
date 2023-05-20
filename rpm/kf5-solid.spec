%global kf5_version 5.106.0

Name: opt-kf5-solid
Version: 5.106.0
Release: 1%{?dist}
Summary: KDE Frameworks 5 Tier 1 integration module that provides hardware information

License: LGPLv2+
URL:     https://solid.kde.org/
Source0: %{name}-%{version}.tar.bz2

## upstreamable patches
%{?opt_kf5_default_filter}

BuildRequires: opt-extra-cmake-modules >= %{majmin}
BuildRequires: opt-kf5-rpm-macros >= %{majmin}
BuildRequires: libupnp-devel
BuildRequires: opt-qt5-qtbase-devel
BuildRequires: opt-qt5-qtdeclarative-devel
BuildRequires: opt-qt5-qttools-devel
BuildRequires: systemd-devel

# Predicate parser deps
BuildRequires:  bison
BuildRequires:  flex
# really runtime-only dep, but doesn't hurt to check availability at buildtime
#BuildRequires:  media-player-info
#BuildRequires:  pkgconfig(libimobiledevice-1.0)
BuildRequires:  pkgconfig(mount)

%{?_opt_qt5:Requires: %{_opt_qt5}%{?_isa} = %{_opt_qt5_version}}
Requires: opt-qt5-qtbase-gui
Requires: opt-qt5-qtdeclarative
Requires: udisks2
#Requires: media-player-info
#Requires: upower

Provides:       opt-kf5-solid-libs = %{version}-%{release}
Provides:       opt-kf5-solid-libs%{?_isa} = %{version}-%{release}

%description
Solid provides the following features for application developers:
 - Hardware Discovery
 - Power Management
 - Network Management

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires: opt-qt5-qtbase-devel
%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -n %{name}-%{version}/upstream -p1

%build
export QTDIR=%{_opt_qt5_prefix}
touch .git

mkdir -p build
pushd build

%_opt_cmake_kf5 ../ \
  -DWITH_NEW_POWER_ASYNC_API:BOOL=ON \
  -DWITH_NEW_POWER_ASYNC_FREEDESKTOP:BOOL=ON \
  -DWITH_NEW_SOLID_JOB:BOOL=ON
%make_build

popd

%install
pushd build
make DESTDIR=%{buildroot} install
popd


%find_lang_kf5 solid5_qt

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README.md TODO
%license LICENSES/*.txt
%{_opt_kf5_datadir}/qlogging-categories5/solid.*
%{_opt_kf5_bindir}/solid-hardware5
# if building with new WIP api's
%{_opt_kf5_bindir}/solid-power
#files libs
%{_opt_kf5_qmldir}/org/kde/solid/
%{_opt_kf5_libdir}/libKF5Solid.so.*
%{_opt_kf5_datadir}/locale/

%files devel
%{_opt_kf5_includedir}/KF5/Solid/
%{_opt_kf5_libdir}/libKF5Solid.so
%{_opt_kf5_libdir}/cmake/KF5Solid/
%{_opt_kf5_archdatadir}/mkspecs/modules/qt_Solid.pri

