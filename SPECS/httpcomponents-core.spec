Name:           httpcomponents-core
Summary:        Set of low level Java HTTP transport components for HTTP services
Version:        4.4.10
Release:        3%{?dist}
License:        ASL 2.0
URL:            http://hc.apache.org/
Source0:        http://www.apache.org/dist/httpcomponents/httpcore/source/httpcomponents-core-%{version}-src.tar.gz
# Expired test certificates. Backported from upstream commit 8caeb927a.
Patch0:         0001-Re-generated-expired-test-certificates.patch

BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  mvn(commons-logging:commons-logging)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.commons:commons-lang3)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.httpcomponents:httpcomponents-parent:pom:)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:  mvn(org.mockito:mockito-core)


%description
HttpCore is a set of low level HTTP transport components that can be
used to build custom client and server side HTTP services with a
minimal footprint. HttpCore supports two I/O models: blocking I/O
model based on the classic Java I/O and non-blocking, event driven I/O
model based on Java NIO.

The blocking I/O model may be more appropriate for data intensive, low
latency scenarios, whereas the non-blocking model may be more
appropriate for high latency scenarios where raw data throughput is
less important than the ability to handle thousands of simultaneous
HTTP connections in a resource efficient manner.

%package        javadoc
Summary:        API documentation for %{name}

%description    javadoc
%{summary}.


%prep
%setup -q

%patch0 -p1

# Random test failures on ARM -- 100 ms sleep is not eneough on this
# very performant arch, lets make it 2 s
sed -i '/Thread.sleep/s/100/2000/' httpcore-nio/src/test/java/org/apache/http/nio/integration/TestHttpAsyncHandlers.java

%pom_remove_plugin :maven-checkstyle-plugin
%pom_remove_plugin :apache-rat-plugin
%pom_remove_plugin :maven-source-plugin
%pom_remove_plugin :maven-javadoc-plugin

# we don't need these artifacts right now
%pom_disable_module httpcore-osgi
%pom_disable_module httpcore-ab

# OSGify modules
for module in httpcore httpcore-nio; do
    %pom_xpath_remove "pom:project/pom:packaging" $module
    %pom_xpath_inject "pom:project" "<packaging>bundle</packaging>" $module
    %pom_remove_plugin :maven-jar-plugin $module
    %pom_xpath_inject "pom:build/pom:plugins" "
        <plugin>
          <groupId>org.apache.felix</groupId>
          <artifactId>maven-bundle-plugin</artifactId>
          <extensions>true</extensions>
          <configuration>
            <instructions>
              <Export-Package>*</Export-Package>
              <Private-Package></Private-Package>
              <Automatic-Module-Name>org.apache.httpcomponents.$module</Automatic-Module-Name>
              <_nouses>true</_nouses>
            </instructions>
          </configuration>
        </plugin>" $module
done

# install JARs to httpcomponents/ for compatibility reasons
# several other packages expect to find the JARs there
%mvn_file ":{*}" httpcomponents/@1

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENSE.txt NOTICE.txt README.txt RELEASE_NOTES.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt

%changelog
* Mon Jul 23 2018 Michael Simacek <msimacek@redhat.com> - 4.4.10-3
- Fix failing tests

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Michael Simacek <msimacek@redhat.com> - 4.4.10-1
- Update to upstream version 4.4.10

* Mon Mar 19 2018 Michael Simacek <msimacek@redhat.com> - 4.4.9-4
- Fix FTBFS (weak encryption in tests)

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.4.9-3
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 16 2018 Michael Simacek <msimacek@redhat.com> - 4.4.9-1
- Update to upstream version 4.4.9

* Sun Oct 22 2017 Michael Simacek <msimacek@redhat.com> - 4.4.8-1
- Update to upstream version 4.4.8

* Tue Sep 19 2017 Michael Simacek <msimacek@redhat.com> - 4.4.7-1
- Update to upstream version 4.4.7

* Fri Sep 15 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.4.6-5
- Try to workaround test failures on ARM

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Feb 23 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.4.6-3
- Remove unneeded maven-javadoc-plugin invocation

* Tue Feb 07 2017 Michael Simacek <msimacek@redhat.com> - 4.4.6-2
- Remove useless plugins

* Thu Jan 12 2017 Michael Simacek <msimacek@redhat.com> - 4.4.6-1
- Update to upstream version 4.4.6

* Fri Jun 24 2016 Michael Simacek <msimacek@redhat.com> - 4.4.5-2
- Change license to just ASL 2.0

* Thu Jun 23 2016 Michael Simacek <msimacek@redhat.com> - 4.4.5-1
- Update to upstream version 4.4.5

* Wed Jun 15 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.4.4-3
- Regenerate build-requires

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov  2 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.4.4-1
- Update to upstream version 4.4.4

* Wed Sep  9 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.4.3-1
- Update to upstream version 4.4.3

* Mon Sep 07 2015 Michael Simacek <msimacek@redhat.com> - 4.4.2-1
- Update to upstream version 4.4.2

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Mar 19 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.4.1-1
- Update to upstream version 4.4.1

* Mon Jan 19 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.4-1
- Update to upstream version 4.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.3.2-2
- Remove BuildRequires on maven-surefire-provider-junit4

* Mon May 12 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.3.2-1
- Update to upstream version 4.3.2

* Tue Sep 03 2013 Michal Srb <msrb@redhat.com> - 4.3-1
- Update to upstream version 4.3

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 10 2013 Michal Srb <msrb@redhat.com> - 4.2.4-4
- Fix license tag (CC-BY added)

* Fri May 17 2013 Alexander Kurtakov <akurtako@redhat.com> 4.2.4-3
- Fix bundle plugin configuration to produce sane manifest.
- Do not duplicate javadoc files list.

* Mon Mar 25 2013 Michal Srb <msrb@redhat.com> - 4.2.4-2
- Build with xmvn

* Mon Mar 25 2013 Michal Srb <msrb@redhat.com> - 4.2.4-1
- Update to upstream version 4.2.4

* Mon Feb 25 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.3-3
- Add missing BR: maven-local

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec  3 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.3-1
- Update to upstream version 4.2.3

* Fri Oct  5 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.2-1
- Update to upstream version 4.2.2

* Mon Aug 27 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 4.2.1-3
- Remove mockito from Requires (not needed really)
- BR on mockito is now conditional on Fedora

* Fri Jul 27 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.1-2
- Install NOTICE.txt file
- Fix javadir directory ownership
- Preserve timestamps

* Mon Jul 23 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.1-1
- Update to upstream version 4.2.1
- Convert patches to POM macros

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Mar 23 2012 Krzysztof Daniel <kdaniel@redhat.com> 4.1.4-1
- Update to latest upstream (4.1.4)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 16 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 4.1.3-1
- Update to latest upstream (4.1.3)

* Tue Jul 26 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 4.1.2-1
- Update to latest upstream (4.1.2)

* Mon Jul  4 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 4.1.1-2
- Fix forgotten add_to_maven_depmap

* Fri Jul  1 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 4.1.1-1
- Update to latest upstream (4.1.1)
- Use new maven macros
- Tweaks according to new guidelines
- Enable tests again (seem to work OK even in koji now)

* Tue Mar 15 2011 Severin Gehwolf <sgehwolf@redhat.com> 4.1-6
- Explicitly set PrivatePackage to the empty set, so as to
  export all packages.

* Fri Mar 11 2011 Alexander Kurtakov <akurtako@redhat.com> 4.1-5
- Bump release to fix my mistake with the release.

* Thu Mar 10 2011 Alexander Kurtakov <akurtako@redhat.com> 4.1-3
- Export all packages.

* Fri Feb 18 2011 Alexander Kurtakov <akurtako@redhat.com> 4.1-2
- Don't use basename it's part of coreutils.

* Fri Feb 18 2011 Alexander Kurtakov <akurtako@redhat.com> 4.1-4
- Install into %%{_javadir}/httpcomponents. We will use it for client libs too.
- Proper osgi info.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 4.1-2
- Added license to javadoc subpackage

* Fri Dec 17 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 4.1-1
- Initial package
