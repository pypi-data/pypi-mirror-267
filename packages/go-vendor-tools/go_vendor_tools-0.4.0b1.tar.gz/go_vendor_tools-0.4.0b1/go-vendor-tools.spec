# Copyright (C) 2024 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT
# License text: https://spdx.org/licenses/MIT

%bcond manpages 1
%global forgeurl https://gitlab.com/fedora/sigs/go/go-vendor-tools
%define tag v%{version_no_tilde %{quote:%nil}}

Name:           go-vendor-tools
Version:        0.4.0b1
%forgemeta
Release:        1%{?dist}
Summary:        Tools for handling Go library vendoring in Fedora

# BSD-3-Clause: src/go_vendor_tools/archive.py
License:        MIT AND BSD-3-Clause
URL:            %{forgeurl}
Source0:        %{forgesource}

BuildArch:      noarch

BuildRequires:  python3-devel

%if %{with manpages}
BuildRequires:  scdoc
%endif

Recommends:     (askalono-cli or trivy)


%global common_description %{expand:
go-vendor-tools provides tools and macros for handling Go library vendoring in
Fedora.}

%description %common_description


%package doc
Summary:        Documentation for go-vendor-tools
Enhances:       go-vendor-tools

%description doc %common_description


%prep
%autosetup -p1 %{forgesetupargs}


%generate_buildrequires
%pyproject_buildrequires -x test


%build
%pyproject_wheel
%if %{with manpages}
./doc/man/mkman.sh
%endif


%install
%pyproject_install
# TODO(anyone): Use -l flag once supported by EL 9.
%pyproject_save_files go_vendor_tools

# Install RPM macros
install -Dpm 0644 rpm/macros.go_vendor_tools -t %{buildroot}%{_rpmmacrodir}

# Install documentation
mkdir -p %{buildroot}%{_docdir}/go-vendor-tools-doc
cp -rL doc/* %{buildroot}%{_docdir}/go-vendor-tools-doc

# Install manpages
%if %{with manpages}
install -Dpm 0644 doc/man/*.1 -t %{buildroot}%{_mandir}/man1/
%endif


%check
%pytest


%files -f %{pyproject_files}
# Install top-level markdown files
%doc *.md
%license LICENSES/*
%{_bindir}/go_vendor*
%{_rpmmacrodir}/macros.go_vendor_tools
%if %{with manpages}
%{_mandir}/man1/go*.1*
%endif

%files doc
%doc %{_docdir}/go-vendor-tools-doc/

%pyproject_extras_subpkg -n go-vendor-tools all

%changelog
* Wed Apr 10 2024 Maxwell G <maxwell@gtmx.me> - 0.4.0b1-1
- Release 0.4.0b1.

* Thu Mar 28 2024 Maxwell G <maxwell@gtmx.me> - 0.3.0-1
- Release 0.3.0.

* Sat Mar 16 2024 Maxwell G <maxwell@gtmx.me> - 0.2.0-1
- Release 0.2.0.

* Sat Mar 09 2024 Maxwell G <maxwell@gtmx.me> - 0.1.0-1
- Release 0.1.0.

* Tue Mar 05 2024 Maxwell G <maxwell@gtmx.me> - 0.0.1-1
- Release 0.0.1.
