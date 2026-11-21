# TODO
# - can these be removed on linux?
#   site-packages/pip/_vendor/distlib/t32.exe
#   site-packages/pip/_vendor/distlib/t64.exe
#   site-packages/pip/_vendor/distlib/w32.exe
#   site-packages/pip/_vendor/distlib/w64.exe
#
# Conditional build:
%bcond_without	doc		# Sphinx documentation
%bcond_with	tests		# test suite (not included in sdist)

%define		module		pip
Summary:	A tool for installing and managing Python 3 packages
Summary(pl.UTF-8):	Narzędzie do instalowania i zarządzania pakietami Pythona 3
Name:		python3-%{module}
Version:	26.3
Release:	1
License:	MIT
Group:		Libraries/Python
# Source0Download: https://pypi.python.org/simple/pip/
Source0:	https://files.pythonhosted.org/packages/source/p/pip/%{module}-%{version}.tar.gz
# Source0-md5:	329592944207f872a94cb63da2b978f0
URL:		https://pip.pypa.io/
BuildRequires:	python3-devel >= 1:3.9
BuildRequires:	python3-build
BuildRequires:	python3-flit_core >= 3.11
BuildRequires:	python3-flit_core < 4
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.9
%if %{with tests}
BuildRequires:	python3-cryptography
BuildRequires:	python3-freezegun
BuildRequires:	python3-proxy.py
BuildRequires:	python3-pytest >= 7.0
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-pytest-rerunfailures
BuildRequires:	python3-pytest-subket
BuildRequires:	python3-pytest-xdist
BuildRequires:	python3-scripttest >= 1.3
BuildRequires:	python3-setuptools
BuildRequires:	python3-tomli-w
BuildRequires:	python3-virtualenv >= 20.0
BuildRequires:	python3-werkzeug
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-furo
BuildRequires:	python3-myst_parser
BuildRequires:	python3-sphinx_copybutton
BuildRequires:	python3-sphinx_inline_tabs
BuildRequires:	python3-sphinx_issues
BuildRequires:	python3-sphinxcontrib-towncrier >= 0.2.0
BuildRequires:	sphinx-pdg-3 >= 7.0
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
%py3_build_pyproject

%if %{with tests}
TODO when tests available
%endif

%if %{with doc}
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
%doc AUTHORS.txt LICENSE.txt NEWS.rst README.rst SECURITY.md
%attr(755,root,root) %{_bindir}/pip3
%{_bindir}/python3-pip
%{py3_sitescriptdir}/pip
%{py3_sitescriptdir}/pip-%{version}.dist-info

%files -n pip
%defattr(644,root,root,755)
%doc AUTHORS.txt LICENSE.txt README.rst
%{_bindir}/pip

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/html/_build/html/{_images,_static,cli,development,reference,topics,ux-research-design,*.html,*.js}
%endif
