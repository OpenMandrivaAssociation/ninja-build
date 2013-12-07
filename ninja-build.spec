Name:           ninja-build
Version:        1.4.0
Release:        4
Group:          Development/Other
Summary:        A small build system with a focus on speed

License:        ASL 2.0
URL:            http://martine.github.com/ninja/
Source0:        https://github.com/martine/ninja/archive/v%{version}.tar.gz
Source1:        ninja.vim

BuildRequires:  asciidoc
BuildRequires:  gtest-devel
BuildRequires:  re2c
BuildRequires:  xsltproc

%description
Ninja is a small build system with a focus on speed. It differs from other
build systems in two major respects: it is designed to have its input files
generated by a higher-level build system, and it is designed to run builds as
fast as possible.

%prep
%setup -q -n ninja-%{version}

%build
CFLAGS="%{optflags}"
export CFLAGS
./bootstrap.py --verbose -- --debug
./ninja -v manual
./ninja -v ninja_test


%check
# workaround possible too low default limits
ulimit -n 2048
ulimit -u 2048

./ninja_test


%install
# TODO: Install ninja_syntax.py?
install -p -m 755 -d %{buildroot}%{_bindir}
install -p -m 755 ninja %{buildroot}%{_bindir}/ninja

install -p -m 755 -d %{buildroot}%{_docdir}/%{name}-%{version}
install -p -m 644 doc/manual.html %{buildroot}%{_docdir}/%{name}-%{version}/manual.html

install -p -m 755 -d %{buildroot}%{_sysconfdir}/bash_completion.d
install -p -m 644 misc/bash-completion %{buildroot}%{_sysconfdir}/bash_completion.d/ninja-bash-completion

install -p -m 755 -d %{buildroot}%{_datadir}/emacs/site-lisp
install -p -m 644 misc/ninja-mode.el %{buildroot}%{_datadir}/emacs/site-lisp/ninja-mode.el

install -p -m 755 -d %{buildroot}%{_datadir}/vim/vimfiles/syntax
install -p -m 644 misc/ninja.vim %{buildroot}%{_datadir}/vim/vimfiles/syntax/ninja.vim
install -p -m 755 -d %{buildroot}%{_datadir}/vim/vimfiles/ftdetect
install -p -m 644 %{SOURCE1} %{buildroot}%{_datadir}/vim/vimfiles/ftdetect/ninja.vim

install -p -m 755 -d %{buildroot}%{_datadir}/zsh/site-functions
install -p -m 644 misc/zsh-completion %{buildroot}%{_datadir}/zsh/site-functions/_ninja


%files
%doc COPYING README
%{_bindir}/ninja
%{_docdir}/%{name}-%{version}/manual.html
# bash-completion does not own this
%{_sysconfdir}/bash_completion.d/
%{_datadir}/emacs/site-lisp/ninja-mode.el
%{_datadir}/vim/vimfiles/syntax/ninja.vim
%{_datadir}/vim/vimfiles/ftdetect/ninja.vim
# zsh does not have a -filesystem package
%{_datadir}/zsh/
