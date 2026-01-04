# lidm Fedora .spec

This repository provides a .spec file to build [lidm](https://github.com/javalsai/lidm) for Fedora Linux.

# Installation

## Enable the COPR repository

### For Fedora Workstation

Run `dnf copr enable celestelove/lidm`

### For Fedora Silverblue or other atomic flavors

##### Fedora 43

Either download the [.repo](https://copr.fedorainfracloud.org/coprs/celestelove/lidm/repo/fedora-43/celestelove-lidm-fedora-43.repo) file to `/etc/yum.repos.d/` manually with your preferred HTTP client or run the following command to do it automatically (if you have curl installed):
```bash
sudo curl --output-dir "/etc/yum.repos.d/" --remote-name https://copr.fedorainfracloud.org/coprs/celestelove/lidm/repo/fedora-43/celestelove-lidm-fedora-43.repo
```

Then, refresh the package cache with:

```bash
sudo rpm-ostree refresh-md --force
```

#### Fedora Rawhide

Either download the [.repo](https://copr.fedorainfracloud.org/coprs/celestelove/lidm/repo/fedora-rawhide/celestelove-lidm-fedora-rawhide.repo) file to `/etc/yum.repos.d/` manually with your preferred HTTP client or run the following command to do it automatically (if you have curl installed):
```bash
sudo curl --output-dir "/etc/yum.repos.d/" --remote-name https://copr.fedorainfracloud.org/coprs/celestelove/lidm/repo/fedora-rawhide/celestelove-lidm-fedora-rawhide.repo
```

Then, refresh the package cache with:

```bash
sudo rpm-ostree refresh-md --force
```

## Install the Package

### For Fedora Workstation

Install lidm by using dnf5:

```bash
sudo dnf5 install lidm
```

Also, optionally install the SELinux rules for lidm:

```bash
sudo dnf5 install lidm-selinux
```

### For Fedora Silverblue or other atomic flavors

Install lidm by using rpm-ostree:

```bash
rpm-ostree install lidm
```

Also, optionally install the SELinux rules for lidm:

```bash
rpm-ostree install lidm-selinux
```
