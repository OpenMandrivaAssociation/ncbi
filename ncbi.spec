%define name	ncbi
%define major	6
%define minor	1
%define date	20050429
%define version	%{major}.%{minor}.%{date}
%define release	%mkrel 5
%define libname	%mklibname %{name} %{major}

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	NCBI software development toolkit
Group:		Sciences/Biology
License:	Public Domain
URL:		http://www.ncbi.nlm.nih.gov
Source0:	%{name}.tar.bz2
Source2:	%{name}.make.bz2
Source3:	%{name}.vibrate.bz2
Patch0:		%{name}-6.1.20050429.build.patch
Patch1:		%{name}-6.1.20050429.code.patch
Patch2:		%{name}-6.1.20050429.man.patch
Patch3:		%{name}-6.1.20050429.makefile.patch
Patch4:		ncbi_Jun2005_evalue.patch
BuildRequires:	X11-devel
BuildRequires:	lesstif-devel
BuildRequires:	libpcre-devel
BuildRequires:  libMesaGLU-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
NCBI SOFTWARE DEVELOPMENT TOOLKIT National Center for Biotechnology
Information Bldg 38A, NIH 8600 Rockville Pike Bethesda, MD 20894

The NCBI Software Development Toolkit was developed for the production
and distribution of GenBank, Entrez, BLAST, and related services by
NCBI. We make it freely available to the public without restriction to
facilitate the use of NCBI by the scientific community. However, please
understand that while we feel we have done a high quality job, this is
not commercial software. The documentation lags considerably behind the
software and we must make any changes required by our data production
needs. Nontheless, many people have found it a useful and stable basis
for a number of tools and applications.

%package blast
Summary:        Basic Local Alignment Search Tool
Requires:       %{libname} = %{version}-%{release}
Group:          Sciences/Biology

%description blast
The famous sequence alignment program. This is "official" NCBI version, #2. The
blastall executable allows you to give a nucleotide or protein sequence to the
program. It is compared against databases and a summary of matches is returned
to the user.

%package tools-bin
Summary:        NCBI text-based utilities
Requires:       %{libname} = %{version}-%{release}
Group:          Sciences/Biology

%description tools-bin
his package includes various utilities distributed with the NCBI C SDK. None of
the programs in this package require X; you can find the X-based utilities in
the ncbi-tools-x11 package. BLAST and related tools are in a separate package
(ncbi-blast).

%package tools-x11
Summary:        NCBI X-based utilities
Requires:       %{libname} = %{version}-%{release}
Group:          Sciences/Biology

%description tools-x11
This package includes some X-based utilities distributed with the NCBI C SDK:
Cn3D, Network Entrez, Sequin, ddv, and udv. These programs are not part of
ncbi-tools-bin because they depend on several additional library packages.

%package -n %{libname}
Summary:	Shared library for %{name}
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}

%description -n %{libname}
This package provides shared library for %{name}.

%package -n %{libname}-devel
Summary:        Development headers and libraries for %{name}
Group:          Development/C
Requires:       %{libname} = %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release}

%description -n %{libname}-devel
This package contains the symlinks, headers and object files needed to compile
and link programs which use %{name}.

%prep
%setup -q -n ncbi
bzcat %{SOURCE2} > Makefile
bzcat %{SOURCE3} > vibrate
%patch0 -p 1
%patch1 -p 1
%patch2 -p 1
%patch3 -p 0
%patch4 -p 1

%build
make \
%if %mdkversion<200600
        X11LIBDIR=%_prefix/X11R6/%_lib\
%else
        X11LIBDIR=%_libdir\
%endif
	NCBI_VERSION=%{major}.%{minor} \
	NCBI_VERSION_MAJOR=%{major} \
	NCBI_VERSION_MINOR=%{minor}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_datadir}/%name

%makeinstall \
%if %mdkversion<200600
	X11LIBDIR=%_prefix/X11R6/%_lib\
%else
	X11LIBDIR=%_libdir\
%endif
	NCBI_VERSION=%{major}.%{minor} \
	NCBI_VERSION_MAJOR=%{major} \
	NCBI_VERSION_MINOR=%{minor}

install -m 755 vibrate %{buildroot}%{_bindir}
cp -av build/ %{buildroot}/%{_datadir}/%name
cp -av demo/ %{buildroot}/%{_datadir}/%name

pushd %{buildroot}/%{_datadir}/%name/build/
rm -f *.c
rm -f *.h
popd

pushd %{buildroot}/%{_datadir}/%name/
ln -sf /usr/include/ncbi include
ln -sf %_libdir lib
popd

%clean
rm -rf %{buildroot}

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%files blast
%defattr(-,root,root)
%{_bindir}/bl2seq
%{_bindir}/blast
%{_bindir}/blastall
%{_bindir}/blastcl3
%{_bindir}/blastclust
%{_bindir}/blastpgp
%{_bindir}/copymat
%{_bindir}/fastacmd
%{_bindir}/formatdb
%{_bindir}/formatrpsdb
%{_bindir}/impala
%{_bindir}/makemat
%{_bindir}/megablast
%{_bindir}/rpsblast
%{_bindir}/seedtop
%{_mandir}/man1/bl2seq.1*
%{_mandir}/man1/blast.1*
%{_mandir}/man1/blast2.1*
%{_mandir}/man1/blastall.1*
%{_mandir}/man1/blastcl3.1*
%{_mandir}/man1/blastclust.1*
%{_mandir}/man1/blastpgp.1*
%{_mandir}/man1/copymat.1*
%{_mandir}/man1/fastacmd.1*
%{_mandir}/man1/formatdb.1*
%{_mandir}/man1/formatrpsdb.1*
%{_mandir}/man1/impala.1*
%{_mandir}/man1/makemat.1*
%{_mandir}/man1/megablast.1*
%{_mandir}/man1/rpsblast.1*
%{_mandir}/man1/seedtop.1*
%{_datadir}/%{name}/data

%files tools-bin
%defattr(-,root,root)
%{_bindir}/asn2asn
%{_bindir}/asn2ff
%{_bindir}/asn2xml
%{_bindir}/asn2gb
%{_bindir}/asn2idx
%{_bindir}/asn2all
%{_bindir}/asn2fsa
%{_bindir}/asnval
%{_bindir}/asndhuff
%{_bindir}/cdscan
%{_bindir}/checksub
%{_bindir}/debruijn
%{_bindir}/entrcmd
%{_bindir}/fa2htgs
%{_bindir}/findspl
%{_bindir}/gbseqget
%{_bindir}/gene2xml
%{_bindir}/getfeat	
%{_bindir}/getmesh
%{_bindir}/getpub
%{_bindir}/getseq
%{_bindir}/gil2bin
%{_bindir}/idfetch
%{_bindir}/indexpub
%{_bindir}/makeset
%{_bindir}/spidey
%{_bindir}/sortbyquote
%{_bindir}/tbl2asn
%{_bindir}/vecscreen
%{_bindir}/vibrate
%{_mandir}/man1/asn2asn.1*
%{_mandir}/man1/asn2ff.1*
%{_mandir}/man1/asn2xml.1*
%{_mandir}/man1/asn2gb.1*
%{_mandir}/man1/asn2idx.1*
%{_mandir}/man1/asn2all.1*
%{_mandir}/man1/asn2fsa.1*
%{_mandir}/man1/asnval.1*
%{_mandir}/man1/asndhuff.1*
%{_mandir}/man1/cdscan.1*
%{_mandir}/man1/checksub.1*
%{_mandir}/man1/debruijn.1*
%{_mandir}/man1/entrcmd.1*
%{_mandir}/man1/fa2htgs.1*
%{_mandir}/man1/findspl.1*
%{_mandir}/man1/fmerge.1*
%{_mandir}/man1/gbseqget.1*
%{_mandir}/man1/gene2xml.1*
%{_mandir}/man1/getfeat.1*
%{_mandir}/man1/getmesh.1*
%{_mandir}/man1/getpub.1*
%{_mandir}/man1/gil2bin.1*
%{_mandir}/man1/idfetch.1*
%{_mandir}/man1/indexpub.1*
%{_mandir}/man1/makeset.1*
%{_mandir}/man1/sortbyquote.1*
%{_mandir}/man1/spidey.1*
%{_mandir}/man1/tbl2asn.1*
%{_mandir}/man1/vecscreen.1*

%files tools-x11
%defattr(-,root,root)
%doc doc/*
%{_bindir}/Cn3D
%{_bindir}/Nentrez
%{_bindir}/Psequin
%{_bindir}/ddv
%{_bindir}/entrez2
%{_bindir}/netentcf
%{_bindir}/udv
%{_mandir}/man1/Nentrez.1*
%{_mandir}/man1/Psequin.1*
%{_mandir}/man1/ddv.1*
%{_mandir}/man1/entrez2.1*
%{_mandir}/man1/netentcf.1*
%{_mandir}/man1/udv.1*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_bindir}/asntool
%{_bindir}/errhdr
%{_libdir}/*.so
%{_libdir}/*.a
%{_includedir}/ncbi
%{_mandir}/man1/asntool.1*
%{_mandir}/man1/errhdr.1*
%{_datadir}/%{name}/demo
%{_datadir}/%{name}/build
%{_datadir}/%{name}/include
%{_datadir}/%{name}/lib

