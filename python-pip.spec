# TODO
# - can these be removed on linux?
#   site-packages/pip/_vendor/distlib/t32.exe
#   site-packages/pip/_vendor/distlib/t64.exe
#   site-packages/pip/_vendor/distlib/w32.exe
#   site-packages/pip/_vendor/distlib/w64.exe
#
# Conditional build:
%bcond_without	python2		# CPython 3.x module
%bcond_without	python3		# CPython 3.x module
%bcond_without	python3_default	# Use Python 3.x for pip executable
%bcond_without	apidocs		# Sphinx documentation
%bcond_with	tests		# test target (not included)

%if %{without python3}
%undefine	python3_default
%endif

%define		pypa_docs_theme_ver	d2e63fbfc62af3b7050f619b2f5bb8658985b931

%define 	module		pip
%define		pypi_name	pip
Summary:	A tool for installing and managing Python 2 packages
Summary(pl.UTF-8):	Narzędzie do instalowania i zarządzania pakietami Pythona 2
Name:		python-%{module}
Version:	18.1
Release:	3
License:	MIT
Group:		Libraries/Python
# Source0Download: https://pypi.python.org/simple/pip/
Source0:	https://pypi.debian.net/pip/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	75cad449ad62c88b22de317a26781714
Source2:        https://github.com/pypa/pypa-docs-theme/archive/%{pypa_docs_theme_ver}.tar.gz
# Source2-md5:	0261c95dc4e8bbbba674a512747ee1af
Source3:        https://github.com/python/python-docs-theme/archive/2018.2.tar.gz
# Source3-md5:	cb78b4116f7456070d39db0a3c5db16c
Patch0:		html_theme_path.patch
URL:		https://pip.pypa.io/
BuildRequires:	rpmbuild(macros) >= 1.710
%if %{with python2}
BuildRequires:	python-devel >= 1:2.6
BuildRequires:	python-modules >= 1:2.6
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-mock
BuildRequires:	python-pytest
BuildRequires:	python-scripttest >= 1.3
BuildRequires:	python-virtualenv >= 1.10
%endif
%endif
BuildRequires:	rpm-pythonprov
%{?with_apidocs:BuildRequires:	sphinx-pdg}
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-mock
BuildRequires:	python3-pytest
BuildRequires:	python3-scripttest >= 1.3
BuildRequires:	python3-virtualenv >= 1.10
%endif
%endif
Requires:	python-setuptools
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

%package -n python3-pip
Summary:	A tool for installing and managing Python 3 packages
Summary(pl.UTF-8):	Narzędzie do instalowania i zarządzania pakietami Pythona 3
Group:		Libraries/Python
Requires:	python3-setuptools

%description -n python3-pip
Pip is a replacement for easy_install. It uses mostly the same
techniques for finding packages, so packages that were made
easy_installable should be pip-installable as well.

%description -n python3-pip -l pl.UTF-8
Pip to zamiennik easy_install. Wykorzystuje w większości te same
techniki do wyszukiwania pakietów, więc pakiety, które dało się
zainstalować przez easy_install, powinny także dać się zainstalować
przy użyciu pipa.

%package -n pip
Summary:	A tool for installing and managing Python 3 packages
Summary(pl.UTF-8):	Narzędzie do instalowania i zarządzania pakietami Pythona 3
Group:		Development/Tools
%if %{with python3_default}
Requires:	python3-%{module} = %{version}-%{release}
%else
Requires:	python-%{module} = %{version}-%{release}
%endif
Conflicts:	%{name} < 7.1.2-3

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
%patch0 -p1
cd docs
tar -xf %{SOURCE2}
mv pypa-docs-theme-%{pypa_docs_theme_ver} pypa
tar -xf %{SOURCE3}
mv python-docs-theme-2018.2 python-docs-theme

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with apidocs}
cd docs/html
export PYTHONPATH=$(pwd)/../../build-2/lib:$(pwd)/../../build-3/lib; sphinx-build -b html . _build/html
cd ../..
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python3}
%py3_install

# RH compatibility
ln -sf pip3 $RPM_BUILD_ROOT%{_bindir}/python3-pip
%endif

%if %{with python2}
%py_install

%py_postclean

# RH compatibility
ln -sf pip2 $RPM_BUILD_ROOT%{_bindir}/python-pip
%endif

%if %{with python3_default}
ln -sf pip3 $RPM_BUILD_ROOT%{_bindir}/pip
%else
ln -sf pip2 $RPM_BUILD_ROOT%{_bindir}/pip
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS.txt LICENSE.txt README.rst
%attr(755,root,root) %{_bindir}/pip2
%attr(755,root,root) %{_bindir}/pip2.*
%attr(755,root,root) %{_bindir}/python-pip
%{py_sitescriptdir}/pip-%{version}-py*.egg-info
%{py_sitescriptdir}/pip
%endif

%if %{with python3}
%files -n python3-pip
%defattr(644,root,root,755)
%doc AUTHORS.txt LICENSE.txt README.rst
%attr(755,root,root) %{_bindir}/pip3
%attr(755,root,root) %{_bindir}/pip3.*
%attr(755,root,root) %{_bindir}/python3-pip
%{py3_sitescriptdir}/pip
%{py3_sitescriptdir}/pip-%{version}-py*.egg-info
%endif

%files -n pip
%defattr(644,root,root,755)
%doc AUTHORS.txt LICENSE.txt README.rst
%attr(755,root,root) %{_bindir}/pip

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc docs/html/_build/html/*
%endif
