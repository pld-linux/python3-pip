# TODO
# - can these be removed on linux?
#   site-packages/pip/_vendor/distlib/t32.exe
#   site-packages/pip/_vendor/distlib/t64.exe
#   site-packages/pip/_vendor/distlib/w32.exe
#   site-packages/pip/_vendor/distlib/w64.exe
#
# Conditional build:
%bcond_without	python3 # CPython 3.x module
%bcond_without	apidocs	# Sphinx documentation

%define 	module	pip
Summary:	A tool for installing and managing Python 2 packages
Summary(pl.UTF-8):	Narzędzie do instalowania i zarządzania pakietami Pythona 2
Name:		python-%{module}
Version:	7.1.0
Release:	1
License:	MIT
Group:		Development/Libraries
# Source0Download: https://pypi.python.org/pypi/pip
Source0:	http://pypi.python.org/packages/source/p/pip/%{module}-%{version}.tar.gz
# Source0-md5:	d935ee9146074b1d3f26c5f0acfd120e
URL:		http://www.pip-installer.org/
BuildRequires:	python-devel >= 1:2.6
BuildRequires:	python-modules >= 1:2.6
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
%{?with_apidocs:BuildRequires:	sphinx-pdg}
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-setuptools
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
Group:		Development/Libraries
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

# remove unneeded shebang
%{__sed} -i '1d' pip/__init__.py

%if %{with python3}
set -- *
install -d py3
cp -a "$@" py3
%endif

%build
%{__python} setup.py build

%if %{with apidocs}
%{__make} -C docs html
%endif

%if %{with python3}
cd py3
%{__python3} setup.py build
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python3}
cd py3
%{__python3} setup.py install \
	--optimize=2 \
	--skip-build \
	--root $RPM_BUILD_ROOT

# remove pip3.x, keep just pip3
%{__rm} $RPM_BUILD_ROOT%{_bindir}/pip%{py3_ver}

# RH compatibility
ln -sf pip3 $RPM_BUILD_ROOT%{_bindir}/python3-pip
cd -
%endif

%{__python} setup.py install \
	--optimize=2 \
	--skip-build \
	--root $RPM_BUILD_ROOT

%py_postclean

# remove pip2.x, keep just pip2
%{__rm} $RPM_BUILD_ROOT%{_bindir}/pip%{py_ver}

# RH compatibility
ln -sf pip $RPM_BUILD_ROOT%{_bindir}/python-pip

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS.txt CHANGES.txt LICENSE.txt README.rst
%attr(755,root,root) %{_bindir}/pip
%attr(755,root,root) %{_bindir}/pip2
%attr(755,root,root) %{_bindir}/python-pip
%{py_sitescriptdir}/pip-%{version}-py*.egg-info
%{py_sitescriptdir}/pip

%if %{with python3}
%files -n python3-pip
%defattr(644,root,root,755)
%doc AUTHORS.txt CHANGES.txt LICENSE.txt README.rst
%attr(755,root,root) %{_bindir}/pip3
%attr(755,root,root) %{_bindir}/python3-pip
%{py3_sitescriptdir}/pip
%{py3_sitescriptdir}/pip-%{version}-py*.egg-info
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
