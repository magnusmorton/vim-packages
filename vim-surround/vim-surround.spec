%global appdata_dir %{_datadir}/appdata

Name: vim-surround
Version: 2.1
Release: 1%{?dist}
Summary: Delete/change/add parentheses/quotes/XML-tags/much more with ease 
License: Vim
URL: http://www.vim.org/scripts/script.php?script_id=1697
Source0: https://github.com/tpope/vim-surround/archive/v%{version}/%{name}-%{version}.tar.gz

# Plug-in AppData for Gnome Software.
# https://github.com/tpope/vim-commentary/pull/52
# Upstream does not seem interested in merging. 
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
Surround.vim is all about "surroundings": parentheses, brackets, quotes, XML tags, and more.  The plugin provides mappings to easily delete, change and add such surroundings in pairs.  While it works under Vim 6, much of the functionality requires Vim 7.

Examples follow.  It is difficult to provide good examples in the variable width font of this site; check the documentation for more.

Press cs"' (that's c, s, double quote, single quote) inside

"Hello world!"

to change it to

'Hello world!'

Now press cs'<q> to change it to

<q>Hello world!</q>

To go full circle, press cst" to get

"Hello world!"

To remove the delimiters entirely, press ds" .

Hello world!

Now with the cursor on "Hello", press ysiw] (iw is a text object).

[Hello] world!

Let's make that braces and add some space (use "}" instead of "{" for no space): cs]{

{ Hello } world!

Now wrap the entire line in parentheses with yssb or yss) .

({ Hello } world!)

Revert to the original text: ds{ds)

Hello world!

Emphasize hello: ysiw<em>

<em>Hello</em> world!

Finally, let's try out visual mode. Press a capital V (for linewise visual mode)
followed by S<p>.

<p>
  Hello world!
</p>

This plugin is very powerful for HTML and XML editing, a niche which currently seems underfilled in Vim land.  (As opposed to HTML/XML *inserting*, for which many plugins are available).  Adding, changing, and removing pairs of tags simultaneously is a breeze.

The "." command will work with ds, cs, and yss if you install repeat.vim, vimscript #2136.

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
