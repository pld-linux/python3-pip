# TODO
# - can these be removed on linux?
#   site-packages/pip/_vendor/distlib/t32.exe
#   site-packages/pip/_vendor/distlib/t64.exe
#   site-packages/pip/_vendor/distlib/w32.exe
#   site-packages/pip/_vendor/distlib/w64.exe
#
# Conditional build:
%bcond_with	apidocs		# Sphinx documentation (needs network?)
%bcond_with	tests		# test target (not included in sdist)

%ifarch x32
%undefine with_apidocs
%endif

%define		module		pip
%define		pypi_name	pip
Summary:	A tool for installing and managing Python 3 packages
Summary(pl.UTF-8):	Narzędzie do instalowania i zarządzania pakietami Pythona 3
Name:		python3-%{module}
Version:	25.0.1
Release:	4
License:	MIT
Group:		Libraries/Python
# Source0Download: https://pypi.python.org/simple/pip/
Source0:	https://pypi.debian.net/pip/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	1bf81564bf9738efbe48439c230f25bf
URL:		https://pip.pypa.io/
BuildRequires:	python3-devel >= 1:3.5
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-mock
BuildRequires:	python3-pytest
BuildRequires:	python3-scripttest >= 1.3
BuildRequires:	python3-virtualenv >= 1.10
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with apidocs}
BuildRequires:	python3-furo
BuildRequires:	python3-sphinx_copybutton
BuildRequires:	python3-sphinx_inline_tabs
BuildRequires:	python3-sphinxcontrib-towncrier
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-setuptools
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Pip is a replacement for easy_install. It uses mostly the same
techniques for finding packages, so packages that were made
easy_installable should be pip-installable as well.

%description -l pl.UTF-8
Pip to zamiennik easy_install. Wykorzystuje w większości te same
techniki do wyszukiwania pakietów, więc pakiety, które dało się
zainstalować przez easy_install, powinny także dać się zainstalować
przy użyciu pipa.

%package -n pip
Summary:	A tool for installing and managing Python 3 packages
Summary(pl.UTF-8):	Narzędzie do instalowania i zarządzania pakietami Pythona 3
Group:		Development/Tools
Requires:	python3-%{module} = %{version}-%{release}
Conflicts:	python-pip < 7.1.2-3

%description -n pip
Pip is a replacement for easy_install. It uses mostly the same
techniques for finding packages, so packages that were made
easy_installable should be pip-installable as well.

%description -n pip -l pl.UTF-8
Pip to zamiennik easy_install. Wykorzystuje w większości te same
techniki do wyszukiwania pakietów, więc pakiety, które dało się
zainstalować przez easy_install, powinny także dać się zainstalować
przy użyciu pipa.

%package apidocs
Summary:	Documentation for Python pip modules and installer
Summary(pl.UTF-8):	Dokumentacja instalatora i modułów Pythona pip
Group:		Documentation

%description apidocs
Documentation for Python pip modules and installer.

%description apidocs -l pl.UTF-8
Dokumentacja instalatora i modułów Pythona pip.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build_pyproject %{?with_tests:test}

%if %{with apidocs}
PYTHONPATH=$(pwd)/src \
sphinx-build-3 -b html docs/html docs/html/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

# RH compatibility
ln -sf pip3 $RPM_BUILD_ROOT%{_bindir}/python3-pip

ln -sf pip3 $RPM_BUILD_ROOT%{_bindir}/pip

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS.txt LICENSE.txt README.rst
%attr(755,root,root) %{_bindir}/pip3
%attr(755,root,root) %{_bindir}/python3-pip
%{py3_sitescriptdir}/pip
%{py3_sitescriptdir}/pip-%{version}.dist-info

%files -n pip
%defattr(644,root,root,755)
%doc AUTHORS.txt LICENSE.txt README.rst
%attr(755,root,root) %{_bindir}/pip

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc docs/html/_build/html/*
%endif
