%global appdata_dir %{_datadir}/appdata

Name: vim-surround
Version: 2.1
Release: 1%{?dist}
Summary: Delete/change/add parentheses/quotes/XML-tags/much more with ease 
License: Vim
URL: http://www.vim.org/scripts/script.php?script_id=1697
Source0: https://github.com/tpope/vim-surround/archive/v%{version}/%{name}-%{version}.tar.gz

# Plug-in AppData for Gnome Software.
Source1: vim-surround.metainfo.xml
Requires: vim-common
Requires(post): %{_bindir}/vim
Requires(postun): %{_bindir}/vim
# Needed for AppData check.
BuildRequires: libappstream-glib
# Defines %%vimfiles_root_root
BuildRequires: vim-filesystem
BuildArch: noarch

%description
Surround.vim is all about "surroundings": parentheses, brackets, quotes, XML
tags, and more.  The plugin provides mappings to easily delete, change and add
such surroundings in pairs.

This plugin is very powerful for HTML and XML editing, a niche which currently
seems underfilled in Vim land.  (As opposed to HTML/XML *inserting*, for which
many plugins are available).  Adding, changing, and removing pairs of tags
simultaneously is a breeze.

%prep
%setup -q

%build


%install
mkdir -p %{buildroot}%{vimfiles_root}
cp -pr doc plugin %{buildroot}%{vimfiles_root}

# Install AppData.
mkdir -p %{buildroot}%{appdata_dir}
install -m 644 %{SOURCE1} %{buildroot}%{appdata_dir}

%check
# Check the AppData add-on to comply with guidelines.
appstream-util validate-relax --nonet %{buildroot}/%{_datadir}/appdata/*.metainfo.xml

%post
vim -c ":helptags %{vimfiles_root}/doc" -c :q &> /dev/null

%postun
> %{vimfiles_root}/doc/tags
vim -c ":helptags %{vimfiles_root}/doc" -c :q &> /dev/null

%files
%doc README.markdown
%{vimfiles_root}/doc/*
%{vimfiles_root}/plugin/*
%{appdata_dir}/vim-surround.metainfo.xml


%changelog

* Thu Sep 23 2021 Magnus Morton <magnus@morton.ai> - 2.1-1
- Initial package.
