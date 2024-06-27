# Document master project for the Universal Payload Specification #

The latest release of the specification can be found at
https://universalpayload.github.io/spec

This [repository](https://github.com/UniversalPayload/spec) holds
the source for the generation of the Universal Payload Specification using Sphinx
and LaTeX.

## Build Instructions

Requirements:
* Sphinx: http://sphinx-doc.org/contents.html
    * version 7 or later (tested on 7.3.7)
* LaTeX (and pdflatex, and various LaTeX packages)
* Graphviz (in particular, "dot"): http://www.graphviz.org/
* Furo: https://pypi.org/project/furo/
    * version 2024.5.6 or later

On Debian and Ubuntu:

>```
># apt-get install python3-sphinx texlive texlive-latex-extra libalgorithm-diff-perl \
>                  texlive-humanities texlive-generic-recommended graphviz \
>                  texlive-generic-extra
>```
>
>If the version of python3-sphinx installed is too old, then an additional
>new version can be installed with the Python package installer:
>
>```
>$ apt-get install python3-pip
>$ pip3 install --user --upgrade Sphinx
>$ export SPHINXBUILD=~/.local/bin/sphinx-build
>```
>
>Since it is currently using Sphinx Furo theme for the doc interface,
>install Furo with:
>
>```
>$ pip3 install furo
>```
>
>You will need latexdiff v1.2.1 or later to create the changebars PDF version
>of the document.
>Until distributions catch up with the latest release you will need to install
>it directly from the github repo.
>
>```
>$ git clone https://github.com/ftilmann/latexdiff
>$ export PATH=$PWD/latexdiff/:$PATH
>```
>
>Export SPHINXBUILD (see above) if Sphinx was installed with pip3 --user, then follow Make commands below

On Mac OS X:

> Install [MacTeX](http://tug.org/mactex/) for LaTeX support
>```
>$ brew install --cask mactex
>```
>
> Install pip3 using [brew](http://brew.sh) if you do not have it:
>```
>$ brew install python3
>```
>Install Sphinx
>```
>pip3 install --user --upgrade Sphinx
>Or
>sudo pip3 install --upgrade Sphinx
>```
>
>Since it is currently using Sphinx Furo theme for the doc interface,
>install Furo with:
>
>```
>$ pip3 install furo
>```
>
>If you are using [brew](http://brew.sh) then you can install graphviz like this:
>```
>brew install graphviz
>```
>If you are using [macports](https://www.macports.org/) then you can install graphviz like this:
>```
>$ sudo port install graphviz
>```

Make commands:

>```
>$ make latexpdf # For generating pdf
>$ make html # For generating a hierarchy of html pages
>$ make singlehtml # For generating a single html page
>```

Output goes in ./build subdirectory.

## License ##
The content of this Universal Payload (UPL) Specification is licensed under the
Creative Commons Attribution 4.0 International License. It is attributed to The
Universal Payload Project Team, the original version can be found [here](https://github.com/UniversalScalableFirmware/documentation/blob/b8ab9a4d873fc37b5095382f52557a7613db60b0/source/2_universal_payload.rst#L21).

You may obtain a copy of the License at
http://creativecommons.org/licenses/by/4.0/

Unless stated otherwise, the sample code examples in this document are released
to you under the Apache License, Version 2.0.

## Copyright ##

Copyright 2021 Intel Corporation  
Copyright 2023 9elements GmbH

THIS SPECIFICATION IS PROVIDED "AS IS" WITH NO WARRANTIES WHATSOEVER, 
INCLUDING ANY WARRANTY OF MERCHANTABILITY, NONINFRINGEMENT, FITNESS 
FOR ANY PARTICULAR PURPOSE, OR ANY WARRANTY OTHERWISE ARISING OUT OF 
ANY PROPOSAL, SPECIFICATION OR SAMPLE. 

Questions pertaining to this document, or the terms or conditions of its
provision, should be addressed to:

9elements GmbH  
Kortumstraße 19-21  
44787 Bochum  
Germany  
Attn: Universal Payload Workgroup

## Contributions ##
Please submit all patches by creating pull request at https://github.com/UniversalPayload/spec

Contributions to the Universal Payload Specification are managed by the
gatekeepers, Lean Sheng Tan <sheng.tan@9elements.com>, Simon Glass <sjg@google.com>,
Vincent Zimmer <vincent.zimmer@intel.com>

Anyone can contribute to the Universal Payload Specification. Contributions to
this project should conform to the `Developer Certificate of Origin` as defined
at http://elinux.org/Developer_Certificate_Of_Origin. Commits to this project
need to contain the following line to indicate the submitter accepts the DCO:
```
Signed-off-by: Your Name <your_email@domain.com>
```
By contributing in this way, you agree to the terms as follows:
```
Developer Certificate of Origin
Version 1.1

Copyright (C) 2004, 2006 The Linux Foundation and its contributors.
660 York Street, Suite 102,
San Francisco, CA 94110 USA

Everyone is permitted to copy and distribute verbatim copies of this
license document, but changing it is not allowed.


Developer's Certificate of Origin 1.1

By making a contribution to this project, I certify that:

(a) The contribution was created in whole or in part by me and I
    have the right to submit it under the open source license
    indicated in the file; or

(b) The contribution is based upon previous work that, to the best
    of my knowledge, is covered under an appropriate open source
    license and I have the right under that license to submit that
    work with modifications, whether created in whole or in part
    by me, under the same open source license (unless I am
    permitted to submit under a different license), as indicated
    in the file; or

(c) The contribution was provided directly to me by some other
    person who certified (a), (b) or (c) and I have not modified
    it.

(d) I understand and agree that this project and the contribution
    are public and that a record of the contribution (including all
    personal information I submit with it, including my sign-off) is
    maintained indefinitely and may be redistributed consistent with
    this project or the open source license(s) involved.
```
