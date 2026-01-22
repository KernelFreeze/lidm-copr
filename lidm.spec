Name:           lidm
Version:        2.0.0
Release:        %autorelease
Summary:        A fully colorful customizable TUI display manager made in C

License:        GPL-3.0-only
URL:            https://github.com/javalsai/lidm
Source0:        https://github.com/javalsai/lidm/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

# Packaged extras (kept in the dist-git alongside the spec)
Source10:       lidm.pam

# SELinux policy module sources (kept in the dist-git alongside the spec)
# This module is intentionally minimal and only labels the lidm executable as xdm_exec_t.
Source20:       lidm.te
Source21:       lidm.fc

BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  make
BuildRequires:  pam-devel
BuildRequires:  systemd-rpm-macros

# Needed to build an SELinux policy module (.pp)
BuildRequires:  selinux-policy-devel
BuildRequires:  checkpolicy
BuildRequires:  policycoreutils

Requires:       pam
Recommends:     %{name}-selinux = %{version}-%{release}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
A fully colorful customizable TUI display manager made in C.
Features full color customization and a text-based user interface.

%package selinux
Summary:        SELinux policy module for %{name} (labels lidm as a display manager)
BuildArch:      noarch
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       selinux-policy-targeted
Requires(post): policycoreutils
Requires(post): libselinux-utils
Requires(postun): policycoreutils
Requires(postun): libselinux-utils

%description selinux
SELinux policy module for %{name}. This policy is minimal and primarily labels
the %{name} executable as a display-manager entrypoint (xdm_exec_t) so it runs
under the standard display manager SELinux domain.

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

# Build SELinux module (lidm.pp) from the shipped .te/.fc sources
cp -p %{SOURCE20} ./lidm.te
cp -p %{SOURCE21} ./lidm.fc
make -f /usr/share/selinux/devel/Makefile lidm.pp

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

# Install themes
mkdir -p %{buildroot}%{_datadir}/%{name}/themes
cp -r themes/* %{buildroot}%{_datadir}/%{name}/themes/

# Install PAM service file
mkdir -p %{buildroot}%{_sysconfdir}/pam.d
install -m644 %{SOURCE10} %{buildroot}%{_sysconfdir}/pam.d/%{name}

# Install SELinux module package for the selinux subpackage
mkdir -p %{buildroot}%{_datadir}/selinux/packages
install -m0644 ./lidm.pp %{buildroot}%{_datadir}/selinux/packages/lidm.pp

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%post selinux
# Install the module and relabel the executable (labels come from lidm.fc).
if selinuxenabled 2>/dev/null; then
    %{_sbindir}/semodule -i %{_datadir}/selinux/packages/lidm.pp || :
    %{_sbindir}/restorecon -Fv %{_bindir}/%{name} || :
fi

%postun selinux
# Remove the module on final erase.
if [ $1 -eq 0 ] && selinuxenabled 2>/dev/null; then
    %{_sbindir}/semodule -r lidm || :
    %{_sbindir}/restorecon -Fv %{_bindir}/%{name} || :
fi

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}.ini
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%{_mandir}/man1/%{name}.1*
%{_mandir}/man5/%{name}-config.5*
%{_unitdir}/%{name}.service
%{_datadir}/%{name}/

%files selinux
%{_datadir}/selinux/packages/lidm.pp

%changelog
%autochangelog
