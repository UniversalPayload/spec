.. SPDX-License-Identifier: CC-BY-4.0

.. _chapter-payload-image-format:

Chapter 2: Payload Image Format
===============================

The Payload, as a standalone component, needs to be properly loaded by Platform
Init into memory prior to execution. In this loading process, additional
processes might be required, such as assembling, rebasing, authenticating, etc.
Today, many Payloads use their own image formats (PE, ELF, FV, RAW, etc.), and
it is very challenging for a Platform Init to identify and support all of them.
To address this, FIT (Flat Image Tree) is chosen as a common Payload image
format to facilitate the loading process. Rather than using FIT as a container
for PE or ELF images, this specification uses FIT with flat binary images.
Platform Init does not need to worry about decoding PE, ELF, FV, etc.

FIT [FITspec]_ is a long-established format for packaging firmware, Linux
kernels, ramdisks, devicetrees along with configuration / metadata. It is
flexible enough to have been extended several times over the years, including
secure boot, FPGAs, multiple loadable firmware images, external hashed binaries,
etc.

The file format is basically a devicetree, although often large binaries are
'external' to the FIT with a pointer from the FIT itself.

This format has many advantages:

* Easy to dump and read (fdtdump)
* Easy to parse, just a small layer on top of libfdt, which is itself a small
  library
* Can also be implemented independently, as with fwupd
* But still can be extended for more complex use cases
* Provides full signature checking
* FDT is widely used and understood in the industry (Linux, U-Boot, Zephyr)
* Can support formats other than ELF if we want to allow that for simpler use
  cases (e.g. flat binary at a fixed load address)
* Supports packaging multiple binaries. Certain platforms do need to load
  multiple binaries, so this provides a motivation for using FIT

FIT has a lot of options. For the purposes of UPL a subset of FIT is supported.
See the FIT Schema for full details.


2.1 FIT Images
--------------

An image is something which can be loaded into memory and executed. Where
multiple images are loaded, only the first is executed; Platform Init loads the
other images and provides information about where they were loaded to the
executed image.

Images have various metadata associated with them, such as a timestamp, machine
architecture, project name and compression.

Each image has its own node. Image nodes may use any name, but must not include
'@' characters. At least one image must be present. There is no upper limit to
how many images may be present.


2.2 FIT Configurations
----------------------

A configuration is a collection of images for a given board or purpose. Each
configuration specifies an executable "firmware" image and optional "loadable"
images. All images are loaded before the "firmware" image is executed; and at
least one configuration must be present. There is no upper limit to how many
configurations may be present.

The default configuration is specified by a "default" property in the
/configuration node. Configuration nodes may use any name, but must not include
'@' characters. It is recommended that they be called "conf-1", "conf-2", etc.

Where multiple configuration nodes are present, the "compatible" property is
used by Platform Init to determine which configuration to use. This is a list of
"vendor,model" strings in order from most specific (or desirable) to least. This
may be used to support using the same FIT with many different boards, where
Platform Init understands the concept of a compatible string and can make this
determination.

Where no compatible string matches, for any configuration, the FIT cannot be
loaded and Platform Init should generate an error indicating that no
configuration matches, along with information about what compatible string(s) it
was looking for.

Where no compatible strings are present, or Platform Init does not support this
concept, the default configuration is used. In this case, there is no purpose to
providing multiple images. Future revisions of this specification may use this
to support configurations for different purposes, such as a recovery flow.


2.3 FIT Schema
--------------

UPL conforms to the FIT schema but adds some additional requirements. These will
be upstreamed to the FIT specification once finalized here.
The structure is quite simple:

* The root node holds an "images" subnode and a "configurations" subnode. These
  subnodes have no properties.
* The "images" node has one or more image subnodes
* The "configurations" node has one or more configuration subnodes.
  Configuration are collections of images

::

    / o image-tree
        └── description = "image description"
        └── timestamp = <12399321>
        └── #address-cells = <1>
        |
        o images
        | |
        | o image-1 {...}
        | o image-2 {...}
        | ...
        |
        o configurations
          └── default = "conf-1"
          |
          o conf-1 {...}
          o conf-2 {...}
          ...

Below are the allowable properties for each node. Required properties, which
must appear a valid UPL, are marked "(R)". Optional properties are marked "(O)".
Platform Init must support both classes of properties.

Nodes with properties are shown in the tables below:

.. note::

    Usage legend: R=Required, O=Optional, OR=Optional but Recommended,
    SD=See Definition

**Node: / (Root Node)**

.. tabularcolumns:: | p{3cm} p{0.75cm} p{2cm} p{9.5cm} |
.. table:: Node: /

   ======================= ===== ===================== ===============================================
   Property Name           Usage Value Type            Definition
   ======================= ===== ===================== ===============================================
   ``description``         R     string                General description of the Payload. This
                                                       may be displayed to the user.
   ``timestamp``           R     u32                   Last image modification time, as seconds
                                                       in POSIX time format\ :sup:`1`. This is updated by
                                                       any tool which creates or changes the FIT.
   ``size``                OR    u32                   Total FIT image size including the FIT itself
                                                       along with all the external images referenced by
                                                       it (with data-offset and data-size).
                                                       This size is required for parsing any loadable
                                                       binary that should be loaded together.
   ``align``               R     u32                   Required alignment for images. Each image
                                                       in the FIT is aligned to this value
                                                       ('data-offset' property). Platform Init
                                                       must ensure that each image is loaded to
                                                       an address with this alignment, if no
                                                       fixed load address is specified by the
                                                       image.
   ``spec-version``        OR    u32                   UPL image specification version in BCD
                                                       format
                                                       7 : 0 - Minor Version
                                                       15 : 8 - Major Version
                                                       31: 16 - Reserved
                                                       For revision v0.90, the value will be
                                                       0x0090.
   ``build-version``       O     u32                   Payload build revision.
                                                       Major.Minor.Revision.Build
                                                       The ImageRevision can be decoded as
                                                       follows:
                                                       7 : 0  - Build Number
                                                       15 :8  - Revision
                                                       23 :16 - Minor Version
                                                       31 :24 - Major Version
   ======================= ===== ===================== ===============================================

.. note:: 

   1. When we get closer to 2106 we can consider allowing 64-bit values.

**Node: /images/<name>**

.. tabularcolumns:: | p{3cm} p{0.75cm} p{2cm} p{9.5cm} |
.. table:: Node: /images/<name>

   ================= =========== ============ ==============================================
   Property Name     Usage       Value Type   Definition
   ================= =========== ============ ==============================================
   description       R           string       General description of the image. This may
                                              be displayed to the user.
   timestamp         O           u32          Last image modification time for this image,
                                              as seconds in POSIX time format.
   arch              R           string       Type of the architecture for which this
                                              image is intended:

                                              * 'x86"
                                              * "x86_64"
                                              * "arm"
                                              * "arm64"
                                              * "riscv"
                                              * "riscv64"
   type              R           string       Type of the image. Must be "flat_binary".
                                              Need it for compatibility with FIT spec.
   compression       O           string       Compression used to reduce image size:
                                              
                                              * "none" - no compression (default)
                                              * "lzma" - Lempel-Ziv-Markov chain-Algorithm,
                                              * "lz4" - Lempel-Ziv-4
                                              
                                              If Platform Init should not decompress the
                                              data when loading it, this must be set to
                                              "none".
   data-offset       R           u32          Offset of image data, measured from the end
                                              of the FIT metadata, i.e.
                                              fdt_totalsize(FIT) bytes after the start of
                                              the FIT, aligned to a 4-byte boundary.
   data-size         R           u32          Size of image data in bytes. For compressed
                                              images, this is the size of the compressed
                                              data. The size of the uncompressed data is
                                              stored in the 'uncomp-size' property.
   load              OR          u32 / u64    This should not normally be needed, since
                                              Payloads should be loadable to any suitable
                                              address.

                                              Where that is not possible: This is the
                                              required load address for the image. Value
                                              Type matches the machine word size. This
                                              must be provided for the 'firmware' image in
                                              a configuration, but is optional for others.
                                              Images without a load address can be loaded
                                              to any suitable location. They can also be
                                              left where they are in the FIT, i.e. not
                                              loaded at all.
   project           R           string       Type of the image, indicating which project
                                              produced it \ :sup:`3`:

                                              * "tianocore" - UEFI binary
                                              * "u-boot" - U-Boot
                                              * "op-tee" - Open Trusted Execution
                                                Environment
                                              * "opensbi" - RISC-V OpenSBI
                                              * "arm-trusted-firmware" - ARM Trusted
                                                Firmware
                                              * “linuxboot” - Linuxboot
   capabilities      O           string list  List of capabilities that the Payload has:
                                              (not defined) \ :sup:`4`
   producer          O           string       Indicates the build system and version
                                              which produced the FIT
   uncomp-size       OR          u32          Size of the uncompressed data in bytes. If
                                              the data is not compressed, this can be
                                              omitted.
   entry-start       O           u32 / u64    If required, this is the offset of the image
                                              entry point from the load address of the
                                              image. For example, a value of 0x10 means
                                              that the image entry point is 16 bytes after
                                              the start of the image. If omitted, a value
                                              of 0 is assumed.
   reloc-start       O           u32 / u64    If the image supports relocation, this is
                                              the offset of the start of the relocation
                                              data within the image.

                                              Relocation is described below here:
                                              :ref:`relocation`. This 'image'
                                              must be loaded to the "load" address, or manually
                                              relocated by Platform Init.
   ================= =========== ============ ==============================================

.. note:: 

   1. Devicetree stores values in big-endian format
   2. This string also indicates the word size of the target machine, i.e. 32
      or 64. The #address-cells feature of device tree is not used since it
      requires a unit address in each node name that matches the 'reg' property
      and requires that a 'reg' property be included in each node (rather than
      'load') which could be confusing. It is possible to omit the 'reg'
      property, but that results in a warning from the devicetree compiler dtc.
      Overall it seems better to use a separate mechanism, as is done here.
   3. Other project values will be allocated as needed and published in this
      specification
   4. Capability strings will be allocated as needed and published in this
      specification


**Node: /configurations**

.. tabularcolumns:: | p{3cm} p{0.75cm} p{2cm} p{9.5cm} |
.. table:: Node: /configurations

   ================= =========== ============ ==============================================
   Property Name     Usage       Value Type   Definition
   ================= =========== ============ ==============================================
   default           O           string       Node name of the default configuration.
   ================= =========== ============ ==============================================

**Node: /configurations/conf-n**

.. tabularcolumns:: | p{3cm} p{0.75cm} p{2cm} p{9.5cm} |
.. table:: Node: /configurations/conf-n

   ================= =========== ============ ==============================================
   Property Name     Usage       Value Type   Definition
   ================= =========== ============ ==============================================
   description       R           string       General description of the configuration. This
                                              may be displayed to the user.
   firmware          R           string       Image name of the primary Payload image. This
                                              must correspond to a subnode of the "images" node.
                                              NOTE: Platform Init jumps to the entry address
                                              of the 'firmware' image after ‘firmware’ and
                                              ‘loadables’ are loaded.
   loadables         SD          string list  List of additional Payload images could be
                                              separately loaded by Platform Init. Each must
                                              correspond to a subnode of the "images" node.
                                              This may be used to provide additional images
                                              required for the Payload to run, such as FV
                                              files, data files, secure OS, etc.
                                              This is not required if 'require-fit' is true,
                                              since the payload can access any part of the
                                              FIT without needing this property to indicate
                                              which images are needed.
   compatible        O           string list  List of compatible strings for Platform Init
                                              to use when selecting the best configuration,
                                              in order from most specific / desirable to
                                              least. This may be used to support using the
                                              same FIT with many different boards, where
                                              Platform Init understands the concept of a
                                              compatible string and can make this
                                              determination.
   require-fit       O           empty        The presence of this property means the whole
                                              fit image shall be loaded together before
                                              Platform Init calling payload entry.
   ================= =========== ============ ==============================================


2.3.1 Example FIT
~~~~~~~~~~~~~~~~~

Shown below is a FIT structure in source form (Image Tree Source) of a Tianocore
Payload. It shows three images and a single configuration: the main image
"tianocore" and 2 more images "uefi-fv" and "bds-fv". "uefi-fv" and "bds-fv" are
included to be used later by the main image after the main image is executed.

.. code-block:: none

   / {
    	description = “Uefi Payload”
    	timestamp = <0x00000000>
    	#address-cells = <0x02>;
    	size = <0x00385000>	
    	spec-version = <0x00000100>;
    	build-revision = <0x00010105>;
    	images {
    		tianocore {
    			description = "Tianocore edk2-stable202208";
    			timestamp = <0x00000000>
    			project = "tianocore";
    			arch = "x86_64";
    			type = "flat-binary";
    			capabilities = "smm-rebase", "...";
    			producer = "My company";
    			data-offset = <...data…>;
    			data-size = <...data…>;
    			reloc-start = <start offset of reloc table within data>;
    			entry-start = <0x121b10>;
    			load = <0x120000>;
    		};
    		uefi-fv {    // showing how to have multiple images
    	      description = "UEFI Firmware Volume";
    	      type = "flat-binary";
    			arch = "x86_64";
    			project = "tianocore";
    			compression = "lzma";
    			data-offset = <...data…>;
    			data-size = <...data…>;
    		};
    		bds-fv {
    			description = "BDS Firmware Volume";
    			type = "flat-binary";
    			arch = "x86_64";
    			project = "tianocore";
    		compression = "lzma";
    		data-offset = <...data…>;
    		data-size = <...data…>;
    	};
    };
    	configurations {
    		default = "conf-1";
    		conf-1 {
    			firmware = "tianocore"
    			require-fit;
    		};
    	};
    };


Note that FIT supports loading Linux, ramdisks and other types of data. These
are not addressed by this specification, since it is beyond the scope of the
Payload. Consideration will be given to these in version 2.0 of this
specification.


2.3.2 FIT External Data
~~~~~~~~~~~~~~~~~~~~~~~

When created in source form, the FIT includes a "data '' property in each image
node, which contains the contents of that image. When converted to binary form,
the '-E' flag is passed to mkimage to tell it to move the data outside the FDT
structure itself. This is convenient since it locates all the FDT metadata in
one place at the start of the FIT, with the image data at the end. In this case,
mkimage removes the "data" property and replaces it with "data-offset" and
"data-size" properties.

Each image in the FIT must be aligned to a 16-byte boundary, measured from the
start of the FIT.

**Additional images**

The FIT may include several images. Platform Init must load each of these to the
address provided.

If no load address is provided, Platform Init is free to load the image to any
suitable address.

When calling the Payload, Platform Init must provide the addresses to which each
image was loaded. This is done by updating the FIT load addresses for each
image. This allows Payload to access related images when it executes. For UEFI
these might include other firmware volumes (FVs).

All images must be loaded by Platform Init before execution of the Payload
starts. The Payload is not permitted to load additional images for its own use,
e.g. data files or firmware volumes. This ensures that a clean handoff is
completed, regardless of the boot media being used. Some reasons for this
include:

* It permits verifying all images before the Payload is started, since it may
  not be possible for the Payload to report an error if something is missing or
  cannot be found.
* It allows Platform Init to be in complete control of what is executed; this
  will become important when verification is added to this specification.
* It allows Platform Init to choose the boot media being used.

2.3.3 Loading Process Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here is an example of Platform Init loading EDK-II Payload:

#. Platform Init loads or locates the FIT, obtaining a pointer to its start
   address in memory
#. Platform Init looks up  "configurations" -> "firmware" -> "tianocore" to know
   it is the main firmware binary blob.
#. Either

   * Simple loading: When "configurations" ->”require-fit” present, Platform
     Init treats the whole FIT image as a single binary blob (no separate
     binary blob loading needed) and load the full FIT image to suitable
     address following FIT->size and FIT->align requirement. In this case, when
     Platform Init is calling the entry-offset of tianocore, it passes the
     handoff FDT to pass the addresses of the binary blobs within the FIT as
     per step 4.
   * Full  loading: Platform Init firstly loads the "tianocore" binary blob
     from the FIT “images” list to address in its "load", relocating if
     necessary. Note: if “tianocore”->“load” is not present, it means
     “tianocore” can be loaded to any suitable address. (no relocation needed).
     Platform Init then loads each desired binary blob listed by “loadables” to
     a suitable address.  The handoff FDT is used to pass the addresses of
     where things ended up as per step 4.

#. Platform Init sets up handoff information including the FIT address. When one
   of the “loadables” binary blobs is loaded by Platform Init, the FIT offset of
   that image node and the load address shall be reported as part of handoff
   information. Refer to :ref:`chapter-payload-handoff-format`
   /options/upl-image node for more information.
#. Platform Init calls the "tianocore" image entry point function (“load” +
   “entry-start” or “new base address” + “entry-start”), passing the handoff
   information along.
#. Tianocore starts executing, locates the firmware volumes and starts up
   normally.


2.3.4 Implementation
~~~~~~~~~~~~~~~~~~~~
To implement FIT, you can use libfdt, for example:

.. code-block:: c

   void *blob;
   int images, node;
   u32 offset, size;
   const char *comp;
   void *payload_data;

   // load FDT into blob
   images = fdt_subnode_offset(blob, 0, "images");
   node = fdt_subnode_offset(blob, images, "tianocore");
   comp = fdt_getprop(blob, node, "compression", NULL);
   offset = fdt_getprop32(blob, node, "data-offset");
   size = fdt_getprop32(blob, node, "data-size");
   payload_data = blob + align4(fdt_totalsize(blob)) + offset;

To generate a FIT there are many options. Some examples are:

* Use pylibfdt to build the image. Use 'pip install pylibfdt'. You will need
  swig (apt install swig). For Windows see https://www.swig.org/Doc1.3/Windows.html
  Make sure you set SWIG_DIR and SWIG_EXECUTABLE environment variables and that
  'swig' is on your path
* Create a Flat Image Tree file as above and compile it with dtc (https://manpages.ubuntu.com/manpages/trusty/man1/dtc.1.html)
* Use mkimage (https://manpages.ubuntu.com/manpages/xenial/man1/mkimage.1.html)
  to build it
* Completely optional, but for my complex cases, binman
  ('pip install binary-manager') can create FIT images (Linux only at present)

.. _relocation:

2.4 Relocation
--------------

2.4.1 Motivation
~~~~~~~~~~~~~~~~

.. warning::

   Relocation support is optional and only supports x86 for now.  Relocation
   support might be deprecated from V2.0 onwards. Further discussion on
   relocation will be needed after v1.0 achieved.

Ideally, the Payload should be able to run from any aligned address. This is
indicated by omitting the "load" property in the image node. In this case,
Platform Init chooses a suitable address and loads the Payload there.

If the Payload must run at a particular address, it specifies this in the "load"
property. Platform Init should try to honor this request. If it cannot, then the 
only solution is to relocate the Payload. This is possible using the relocation
information provided.

.. note::

   This is an undesirable situation. Payloads should be written to run at any
   address, where possible.

Payloads which cannot run at any address must provide relocation data. Otherwise
it may not be possible to load them. We see fixed load addresses with TF-A,
U-Boot, OpenSBI, etc. It is not possible to require everything in the world to
be self-relocating. Quite apart from the complexity of it, for debugging, etc.,
it does add some code. See for example Linux, where it has its own decompressor,
serial-output code, etc.

A 'clean' handoff is basically a jump from one lot of code to another, with the
minimum of cruft in between.

**Notes:**

* Platform Init may not be able to load the Payload to the requested load
  address. For example, if the load address is 0x120000, some Platform Init may
  have something else at that address. This is not desirable but it may occur.
  EDK-II in particular is accustomed to relocating its images.
* Relocation costs time. Provided that Platform Init can accommodate any
  provided loaded address, Platform Init may elect not to support relocation. In
  this case the image is loaded to the correct load address and run from there
* Relocation adds complexity to Platform Init since, if it cannot honor the
  requested load address, it must process the relocations to update the Payload
  image before starting it.
* On the other hand, self-relocation adds complexity to the Payload, since it
  must be capable of running at any address and relocating itself to the
  requested address.


2.4.2 Relocation Format
~~~~~~~~~~~~~~~~~~~~~~~

Relocation is supported by appending a table to the end of the image. The table
consists of a number of relocation records which can be processed by Platform
Init. The table forms part of the image and is included in the "data-size"
property.

A 'reloc-start' property is added to the image node to indicate where in the
image the relocation data starts. So the total size of the relocation data is
(data-size - reloc-start). Note that hashes include all data, including the
relocation part. This is important since relocation could render an image
inoperable if it were tampered with.

To use a load address other than that specified for the image, Platform Init
must process the relocation data, Platform Init:

#. Loads the functional part of the image into memory at the desired load
   address
#. Calculates the offset from the desired load address, reloc_offset
#. Scans the relocation table appended to the image, marked by reloc-start
#. For each relocation entry (type, offset, optional addend), applies the
   relocation operation <type> to offset <offset> of the loaded image
#. Once complete, the image is ready to run at the new load address required by
   Platform Init.

.. note::

   Another option was considered, with a relocation subnode with a separate
   data size and offset. This was considered more complex overall: it adds
   another subnode, meaning that the data to be hashed is potentially in
   two places. It also adds to tooling complexity. In particular, mkimage
   would need to be extended to support this. So having the relocation
   data inside the image data seems simpler overall.

.. code-block:: none

   / {
        upl-size = <0x003850000>
        compatible = "universal-payload";
        upl-version = <0x0100>;	// top 8 bits major, bottom 8 minor
        images {
		    tianocore {
			    description = "Tianocore edk2-stable202208";
			    …
			    data-offset = <payload offset>;
			    data-size = <payload size in bytes>
		        relocation {   // optional
			        data-size = <...>;
			        data-offset = <...>;
		        };
            };
        };
     };


2.4.3 Relocation Records
~~~~~~~~~~~~~~~~~~~~~~~~

Relocation records consist of two or three words. where the size of a word is
determined by the architecture (32- or 64-bit). The word size is determined by
the "arch" property of the image. Relocations are always in little-endian
format. Big-endian machines must byteswap each word.

.. note::

   Relocations may be expected to add 15% to the size of the binary.

The format is shown below:-

For 32-bit it is 8 or 12 bytes per record:

   ========== ============== ================================
   Offset     Name           Field
   ========== ============== ================================
   0          reloc_offset   offset into program
   4          index_and_type relocation type in lower 8 bits
                             symbol index (above that)
   8          addend         optional addend (depending on
                             relocation type)
   ========== ============== ================================

For 64-bit it is 16 or 24 bytes per record:

   =========== ============== ===================================
   Offset      Name           Field
   =========== ============== ===================================
   0           reloc_offset   offset into program
   8           index_and_type relocation type in lower 32 bits
                              symbol index (upper 64 bits)
   0x10        addend         optional addend (depending on
                              relocation type)
   =========== ============== ===================================

Available relocation types are defined below. These may include arch-specific
relocations and typically follow the values used by the ELF format. For now
only x86 is supported. This will be a unified list of supported relocations
(if other Arch also supports relocation):

   ========= ========== ===============================
   Arch      Value      Meaning
   ========= ========== ===============================
   x86       1          u32 sym_addr += reloc_offset
   x86       2          u64 sym_addr += reloc_offset
   ========= ========== ===============================
