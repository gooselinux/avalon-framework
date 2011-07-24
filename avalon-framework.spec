# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define _with_gcj_support 1

%define gcj_support %{?_with_gcj_support:1}%{!?_with_gcj_support:%{?_without_gcj_support:0}%{!?_without_gcj_support:%{?_gcj_support:%{_gcj_support}}%{!?_gcj_support:0}}}
%define short_name    framework
%define short_Name    Avalon

Name:        avalon-%{short_name}
Version:     4.1.4
Release:     7%{?dist}
Epoch:       0
Summary:     Java components interfaces
License:     ASL 1.1
Url:         http://avalon.apache.org/%{short_name}/
Group:       Development/Libraries
Source0:     http://www.apache.org/dist/avalon/framework/v4.1.4/Avalon-4.1.4-src.tar.gz
Patch1:        %{name}-target.patch
Requires:    xml-commons-apis >= 1.3
Requires:    xalan-j2
BuildRequires:    ant
BuildRequires:    junit
BuildRequires:    avalon-logkit
BuildRequires:    xml-commons-apis >= 1.3
BuildRequires:    jpackage-utils >= 0:1.5
%if ! %{gcj_support}
BuildArch:    noarch
%endif
BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if %{gcj_support}
BuildRequires:       java-gcj-compat-devel
Requires(post):      java-gcj-compat
Requires(postun):    java-gcj-compat
%endif

%description
The Avalon framework consists of interfaces that define relationships
between commonly used application components, best-of-practice pattern
enforcements, and several lightweight convenience implementations of the
generic components.
What that means is that we define the central interface Component. We
also define the relationship (contract) a component has with peers,
ancestors and children.

%package manual
Summary:      Manual for %{name}
Group:        Documentation

%description manual
Documentation for %{name}.

%package javadoc
Summary:      Javadoc for %{name}
Group:        Documentation

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{short_Name}-%{version}
%patch1 -p1
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;

# Fix for wrong-file-end-of-line-encoding problem
for i in `find docs -iname "*.html"`; do sed -i 's/\r//' $i; done
for i in `find docs -iname "*.css"`; do sed -i 's/\r//' $i; done
for i in `find docs -iname "*.xml"`; do sed -i 's/\r//' $i; done
sed -i 's/\r//' README.txt
sed -i 's/\r//' LICENSE.txt
sed -i 's/\r//' KEYS
sed -i 's/\r//' docs/api/package-list

%build
export CLASSPATH=%(build-classpath avalon-logkit junit log4j junit)
ant all
ant -Dfailonerror=false javadocs

%install
rm -rf $RPM_BUILD_ROOT
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
install -m 644 target/lib/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
cp -pr target/javadocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
# create unversioned symlinks
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} ${jar/-%{version}/}; done)

ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%if %{gcj_support}
%postun
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%files
%defattr(0644,root,root,0755)
%doc KEYS LICENSE.txt README.txt
%{_javadir}/*.jar

%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}/avalon-framework-4.1.4.jar.*
%endif

%files manual
%defattr(0644,root,root,0755)
%doc docs/*

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

%changelog
* Mon Jan 11 2010 Andrew Overholt <overholt@redhat.com> 0:4.1.4-7
- Remove spurious Requires(post,postun) for old ghost symlinks
- Fix Group tags to shut rpmlint up

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:4.1.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:4.1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:4.1.4-4
- drop repotag
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:4.1.4-3jpp.14
- Autorebuild for GCC 4.3

* Thu Mar 08 2007 Permaine Cheung <pcheung at redhat.com> - 0:4.1.4-2jpp.14
- rpmlint cleanup.

* Thu Aug 10 2006 Matt Wringe <mwringe at redhat.com> - 0:4.1.4-2jpp.13
- Add missing javadoc requires

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 0:4.1.4-2jpp_12fc
- Rebuilt

* Wed Jul 19 2006 Matt Wringe <mwringe at redhat.com> - 0:4.1.4-2jpp_11fc
- Removed separate definition of name, version and release.

* Wed Jul 19 2006 Matt Wringe <mwringe at redhat.com> - 0:4.1.4-2jpp_10fc
- Added conditional native compling.

* Thu Jun  8 2006 Deepak Bhole <dbhole@redhat.com> - 0:4.1.4-2jpp_9fc
- Updated description for fix to Bug# 170999

* Mon Mar  6 2006 Jeremy Katz <katzj@redhat.com> - 0:4.1.4-2jpp_8fc
- stop scriptlet spew

* Wed Dec 21 2005 Gary Benson <gbenson@redhat.com> 0:4.1.4-2jpp_7fc
- Rebuild again

* Thu Dec 15 2005 Gary Benson <gbenson@redhat.com> 0:4.1.4-2jpp_6fc
- Rebuild for new gcj.

* Thu Nov  4 2004 Gary Benson <gbenson@redhat.com> 0:4.1.4-2jpp_5fc
- Build into Fedora.

* Thu Oct 28 2004 Gary Benson <gbenson@redhat.com> 0:4.1.4-2jpp_4fc
- Bootstrap into Fedora.

* Thu Sep 30 2004 Andrew Overholt <overholt@redhat.com> 0:4.1.4-2jpp_3rh
- Remove avalon-logkit as a Requires

* Mon Mar  8 2004 Frank Ch. Eigler <fche@redhat.com> 0:4.1.4-2jpp_2rh
- RH vacuuming part II

* Fri Mar  5 2004 Frank Ch. Eigler <fche@redhat.com> 0:4.1.4-2jpp_1rh
- RH vacuuming

* Fri May 09 2003 David Walluck <david@anti-microsoft.org> 0:4.1.4-2jpp
- update for JPackage 1.5

* Fri Mar 21 2003 Nicolas Mailhot <Nicolas.Mailhot (at) JPackage.org> 4.1.4-1jpp
- For jpackage-utils 1.5
- Forrest is not used right now

* Tue May 07 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 4.1.2-3jpp 
- hardcoded distribution and vendor tag
- group tag again

* Thu May 2 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 4.1.2-2jpp 
- distribution tag
- group tag

* Sun Feb 03 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 4.1.2-1jpp 
- 4.1.2
- section macro

* Thu Jan 17 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 4.1-2jpp
- versioned dir for javadoc
- no dependencies for manual and javadoc packages
- requires xml-commons-apis

* Wed Dec 12 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 4.1-1jpp
- 4.1
- Requires and BuildRequires xalan-j2

* Wed Dec 5 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 4.0-4jpp
- javadoc into javadoc package

* Wed Nov 21 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 4.0-3jpp
- changed extension --> jpp

* Sat Oct 6 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 4.0-2jpp
- first unified release
- used original tarball

* Thu Sep 13 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 4.0-1mdk
- first Mandrake release
