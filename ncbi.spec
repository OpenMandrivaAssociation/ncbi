# This spec is more or less a straight adaptation of the Debian build
# by Aaron Ucko, version 6.1.20061015-2. All patches except the 
# mpiBlast patch come from Debian. If updating, please check Debian 
# build and consider merging any changes since 6.1.20061015-2, they
# are likely needed / useful here too.

%define name		ncbi
%define major		6
%define minor		1
%define date		20061015
%define version		%{major}.%{minor}.%{date}
%define release		%mkrel 4
%define libname		%mklibname %{name} %{major}
%define develname	%mklibname %{name} -d

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	NCBI software development toolkit
Group:		Sciences/Biology
License:	Public Domain
URL:		http://www.ncbi.nlm.nih.gov
Source0:	%{name}.tar.gz
Source2:	ncbi.make.bz2
Source3:	ncbi.vibrate.bz2
# From Debian
Patch0:		ncbi-6.1.20061015-debian-build.patch
Patch1:		ncbi-6.1.20061015-debian-code.patch
Patch2:		ncbi-6.1.20061015-debian-man.patch
# From mpiBlast (CVS)
Patch4:		ncbi_May2006_evalue.patch
BuildRequires:	X11-devel
BuildRequires:	lesstif-devel
BuildRequires:	pcre-devel
BuildRequires:  mesaglu-devel
BuildRequires:	png-devel
# As the Debian maintainer says, GNU make gets confused by ncbi's
# horrible makefiles, so we use BSD make instead. The correct fix
# would be to sort out the makefiles, but no-one feels much like
# diving into THAT thorn bush.
BuildRequires:	pmake
BuildRequires:	tcsh
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

%package -n %{develname}
Summary:        Development headers and libraries for %{name}
Group:          Development/C
Requires:       %{libname} = %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release}
Obsoletes:	%{mklibname ncbi 6 -d}

%description -n %{develname}
This package contains the symlinks, headers and object files needed to compile
and link programs which use %{name}.

%prep
%setup -q -n ncbi
bzcat %{SOURCE2} > Makefile
bzcat %{SOURCE3} > vibrate
%patch0 -p 1
%patch1 -p 1
%patch2 -p 1
%patch4 -p 1
#%patch5 -p1 -b .bash

%build
perl -pi -e "s,CMD='make,CMD='/usr/bin/pmake,g" make/makedis.csh
perl -pi -e 's,lregexp,lpcre,g' make/makedemo.unx

pushd build
ln -s ../make/*.unx .
ln -s ../make/ln-if-absent .
mv makeall.unx makefile

# temporary fix for bug #32013: can be removed when that is resolved
export LS_COLORS=""

# Debian build process begins here

export NCBI_LBSM_SRC=ncbi_lbsmd_stub.c
export NCBI_LBSM_OBJ=ncbi_lbsmd_stub.o
export LD_LIBRARY_PATH="%_builddir/ncbi/shlib:$(LD_LIBRARY_PATH)"

pmake all 	X11LIBDIR=%_libdir \
		NCBI_VERSION=%{major}.%{minor} \
		NCBI_VERSION_MAJOR=%{major} \
		NCBI_VERSION_MINOR=%{minor} \
		LCL=lnx LDFLAGS1="%{optflags}" RAN="ranlib" OTHERLIBS="-lm" \
		VIBLIBS="-lXm -lXmu -lXt -lX11" VIBFLAG="-DWIN_MOTIF" \
		NCBI_LINKINGLIBDIR="../shlib -L../lib" \
		CFLAGS1="-c %{optflags} -D_PNG -fPIC" \
		LIB4=libvibrant.a LIB20=libncbidesk.a LIB28=libvibgif.a \
		LIB30=libncbicn3d.a LIB45=libddvlib.a LIB400=libvibrantOGL.a LIB3000=libncbicn3dOGL.a

pmake -f makenet.unx X11LIBDIR=%_libdir \
		NCBI_VERSION=%{major}.%{minor} \
		NCBI_VERSION_MAJOR=%{major} \
		NCBI_VERSION_MINOR=%{minor} \
		LCL=lnx LDFLAGS1="%{optflags}" RAN="ranlib" OTHERLIBS="-lm" \
		VIBLIBS="-lXm -lXmu -lXt -lX11" VIBFLAG="-DWIN_MOTIF" \
		NCBI_LINKINGLIBDIR="../shlib -L../lib" \
		CFLAGS1="-c %{optflags} -fPIC" NETENTREZVERSION="2.02c2ASN1SPEC6" \
		BLIB31=libvibnet.a OGLLIBS="-lGLU -lGL -lpng" all libncbimla.a libnetblast.a libncbitxc2.a libncbiid1.a shlib

pmake all LCL=lnx X11LIBDIR=%_libdir \
		NCBI_VERSION=%{major}.%{minor} \
		NCBI_VERSION_MAJOR=%{major} \
		NCBI_VERSION_MINOR=%{minor} \
		LDFLAGS1="%{optflags}" RAN="ranlib" OTHERLIBS="-lm" \
		VIBLIBS="-lXm -lXmu -lXt -lX11" VIBFLAG="-DWIN_MOTIF" \
		NCBI_LINKINGLIBDIR="../shlib -L../lib" \
		CFLAGS1="-c %{optflags} -D_PNG" \
		LIB4=libvibrant.a LIB20=libncbidesk.a LIB28=libvibgif.a \
		LIB30=libncbicn3d.a LIB45=libddvlib.a LIB400=libvibrantOGL.a LIB3000=libncbicn3dOGL.a

pmake -f makedemo.unx X11LIBDIR=%_libdir \
		NCBI_VERSION=%{major}.%{minor} \
		NCBI_VERSION_MAJOR=%{major} \
		NCBI_VERSION_MINOR=%{minor} \
		LCL=lnx LDFLAGS1="%{optflags}" RAN="ranlib" OTHERLIBS="-lm" \
		NCBI_LINKINGLIBDIR="../shlib -L../lib" \
		CFLAGS1="-c %{optflags}" VIBLIBS= VIBFLAG= LIB50=-lpcre

pmake -f makedemo.unx X11LIBDIR=%_libdir \
		NCBI_VERSION=%{major}.%{minor} \
		NCBI_VERSION_MAJOR=%{major} \
		NCBI_VERSION_MINOR=%{minor} \
		LCL=lnx LDFLAGS1="%{optflags}" RAN="ranlib" OTHERLIBS="-lm" \
		NCBI_LINKINGLIBDIR="../shlib -L../lib" \
		CFLAGS1="-c %{optflags}" VIBLIBS= VIBFLAG= THREAD_OBJ="ncbithr.o" THREAD_OTHERLIBS="-lpthread" \
		blast blastall blastall_old blastpgp seedtop megablast rpsblast blastclust

pmake -f makenet.unx X11LIBDIR=%_libdir \
		NCBI_VERSION=%{major}.%{minor} \
		NCBI_VERSION_MAJOR=%{major} \
		NCBI_VERSION_MINOR=%{minor} \
		LCL=lnx LDFLAGS1="%{optflags}" RAN="ranlib" OTHERLIBS="-lm" \
		VIBLIBS="-lXm -lXmu -lXt -lX11" VIBFLAG="-DWIN_MOTIF" \
		NCBI_LINKINGLIBDIR="../shlib -L../lib" \
		CFLAGS1="-c %{optflags}" THREAD_OBJ="ncbithr.o" THREAD_OTHERLIBS="-lpthread" \
		NETENTREZVERSION="2.02c2ASN1SPEC6" BLIB31=libvibnet.a \
		OGLLIBS= VIBLIBS= VIB="Psequin sbtedit Nentrez udv ddv blastcl3 idfetch bl2seq asn2gb tbl2asn gene2xml entrez2 gbseqget asn2all asn2asn asn2fsa asn2xml asnval cleanasn insdseqget nps2gps spidey trna2sap trna2tbl Cn3D"

# ends here

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_datadir}/%name

%makeinstall \
	X11LIBDIR=%_libdir\
	NCBI_VERSION=%{major}.%{minor} \
	NCBI_VERSION_MAJOR=%{major} \
	NCBI_VERSION_MINOR=%{minor}

# remove useless binaries - from Debian build again
rm -f %{buildroot}%{_bindir}/*test*
rm -f %{buildroot}%{_bindir}/*demo*
rm -f %{buildroot}%{_bindir}/dosimple
rm -f %{buildroot}%{_bindir}/ncbisort
rm -f %{buildroot}%{_bindir}/getseq
rm -f %{buildroot}%{_bindir}/cdscan

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

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files blast
%defattr(-,root,root)
%{_bindir}/bl2seq
%{_bindir}/blast
%{_bindir}/blastall
%{_bindir}/blastall_old
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
%{_mandir}/man1/blastall_old.1*
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
%{_bindir}/cleanasn
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
%{_bindir}/gil2bin
%{_bindir}/idfetch
%{_bindir}/indexpub
%{_bindir}/insdseqget
%{_bindir}/makeset
%{_bindir}/nps2gps
%{_bindir}/spidey
%{_bindir}/sortbyquote
%{_bindir}/tbl2asn
%{_bindir}/trna2sap
%{_bindir}/trna2tbl
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
%{_mandir}/man1/cleanasn.1*
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
%{_mandir}/man1/insdseqget.1*
%{_mandir}/man1/makeset.1*
%{_mandir}/man1/nps2gps.1*
%{_mandir}/man1/sortbyquote.1*
%{_mandir}/man1/spidey.1*
%{_mandir}/man1/tbl2asn.1*
%{_mandir}/man1/trna2sap.1*
%{_mandir}/man1/trna2tbl.1*
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
%{_bindir}/sbtedit
%{_bindir}/udv
%{_mandir}/man1/Nentrez.1*
%{_mandir}/man1/Psequin.1*
%{_mandir}/man1/ddv.1*
%{_mandir}/man1/entrez2.1*
%{_mandir}/man1/netentcf.1*
%{_mandir}/man1/sbtedit.1*
%{_mandir}/man1/udv.1*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{develname}
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

