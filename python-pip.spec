#
# Conditional build:
%bcond_with	tests	# do not perform "make test"
%bcond_without	python3 # CPython 3.x module

%define 	module	pip
Summary:	A tool for installing and managing Python packages
Name:		python-%{module}
Version:	1.3.1
Release:	1
License:	MIT
Group:		Development/Libraries
URL:		http://www.pip-installer.org
Source0:	http://pypi.python.org/packages/source/p/pip/%{module}-%{version}.tar.gz
# Source0-md5:	cbb27a191cebc58997c4da8513863153
# Sent to dstufft (upstream)
Patch0:		0001-fix-for-http-bugs.python.org-issue17980-in-code-back.patch
BuildRequires:	python-devel
BuildRequires:	python-setuptools
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
%endif
Requires:	python-setuptools
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Pip is a replacement for easy_install. It uses mostly the same
techniques for finding packages, so packages that were made
easy_installable should be pip-installable as well.

%package -n python3-pip
Summary:	A tool for installing and managing Python3 packages
Group:		Development/Libraries
Requires:	python3-setuptools

%description -n python3-pip
Pip is a replacement for easy_install. It uses mostly the same
techniques for finding packages, so packages that were made
easy_installable should be pip-installable as well.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1

%{__sed} -i '1d' pip/__init__.py

%if %{with python3}
set -- *
install -d py3
cp -a "$@" py3
%endif

%build
%{__python} setup.py build

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

# Change the name of the python3 pip executable in order to not conflict with
# the python2 executable
mv $RPM_BUILD_ROOT%{_bindir}/pip $RPM_BUILD_ROOT%{__python}3-pip

# after changing the pip-python binary name, make a symlink to the old name,
# that will be removed in a later version
# https://bugzilla.redhat.com/show_bug.cgi?id=855495
ln -s python3-pip $RPM_BUILD_ROOT%{_bindir}/pip-python3

# The install process creates both pip and pip-<python_abiversion> that seem to
# be the same. Remove the extra script
%{__rm} $RPM_BUILD_ROOT%{_bindir}/pip-3*
cd -
%endif

%{__python} setup.py install \
	--optimize=2 \
	--skip-build \
	--root $RPM_BUILD_ROOT

%py_postclean

# The install process creates both pip and pip-<python_abiversion> that seem to
# be the same. Since removing pip-* also clobbers pip-python3, just remove pip-2*
%{__rm} $RPM_BUILD_ROOT%{_bindir}/pip-2*

# The pip executable no longer needs to be renamed to avoid conflict with perl-pip
# https://bugzilla.redhat.com/show_bug.cgi?id=958377
# However, we'll keep a python-pip alias for now
ln -s pip $RPM_BUILD_ROOT%{__python}-pip

# after changing the pip-python binary name, make a symlink to the old name,
# that will be removed in a later version
# https://bugzilla.redhat.com/show_bug.cgi?id=855495
ln -s pip $RPM_BUILD_ROOT%{_bindir}/pip-python

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/*
%attr(755,root,root) %{_bindir}/pip
%attr(755,root,root) %{_bindir}/pip-python
%attr(755,root,root) %{_bindir}/python-pip
%{py_sitescriptdir}/pip-%{version}-py*.egg-info
%{py_sitescriptdir}/pip

%if %{with python3}
%files -n python3-pip
%defattr(644,root,root,755)
%doc docs/*
%attr(755,root,root) %{_bindir}/pip-python3
%attr(755,root,root) %{_bindir}/python3-pip
%{py3_sitescriptdir}/pip
%{py3_sitescriptdir}/pip-%{version}-py*.egg-info
%endif
