Name:           lidm
Version:        1.2.3
Release:        %autorelease
Summary:        A fully colorful customizable TUI display manager made in C

License:        GPL-3.0-only
URL:            https://github.com/javalsai/lidm
Source0:        https://github.com/javalsai/lidm/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  make
BuildRequires:  pam-devel
BuildRequires:  systemd-rpm-macros

Requires:       pam
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
A fully colorful customizable TUI display manager made in C.
Features full color customization and a text-based user interface.

%prep
%autosetup -n %{name}-%{version}

%build
%make_build \
    CFLAGS="%{optflags} -fPIE" \
    LIBS="-lpam %{build_ldflags} -pie" \
    CPPFLAGS+='-DPAM_SERVICE_FALLBACK="\"login\""' \
    CPPFLAGS+='-DSESSIONS_XSESSIONS="\"/usr/share/xsessions\""' \
    CPPFLAGS+='-DSESSIONS_WAYLAND="\"/usr/share/wayland-sessions\""' \
    CPPFLAGS+='-DLIDM_CONF_PATH="\"/etc/lidm.ini\""' \
    INFO_GIT_REV="v%{version}-%{release}" \
    INFO_BUILD_TS="$(date +%%s)"

%check
# Verify the binary was built successfully
./lidm -v

# Basic sanity check that the binary exists and is executable
test -x ./lidm

%install
%make_install PREFIX=%{_prefix}

# Install systemd service file
mkdir -p %{buildroot}%{_unitdir}
install -m644 ./assets/services/systemd.service %{buildroot}%{_unitdir}/%{name}.service

mkdir -p %{buildroot}%{_datadir}/%{name}/themes
cp -r themes/* %{buildroot}%{_datadir}/%{name}/themes/

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}.ini
%{_mandir}/man1/%{name}.1*
%{_mandir}/man5/%{name}-config.5*
%{_unitdir}/%{name}.service
%{_datadir}/%{name}/

%changelog
* Sat Jan 03 2026 Celeste Peláez <celeste@etheryal.net> - 1.2.3-1
- Initial Fedora package
