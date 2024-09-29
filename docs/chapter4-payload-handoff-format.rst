.. SPDX-License-Identifier: CC-BY-4.0

.. _chapter-payload-handoff-format:

Chapter 4: Payload Handoff Format
=================================

Here we define the handoff information from Platform Init to Payload, which
takes the form of an devicetree blob. This section describes the bindings used
for each area addressed by this specification.

A devicetree is a tree data structure with nodes that describe the devices in a
system. Each node has exactly one parent except for the root node, which has no
parent. Each node has property/value pairs that describe the characteristics of
the device being presented. Properties consist of a name and a value. Property
names are strings of 1 to 31 characters. Property values are an array of zero or
more bytes that contain information associated with the property.

The sections below show which nodes should be passed from Platform Init and its
corresponding property / value. It does not change what is passed from the
Payload to the OS, but it is intended to avoid interfering with it, i.e. it uses
the same bindings where possible.

A pointer to the FIT is provided so that the running image can find other images
it needs and find out where they were loaded.

Note that properties indicated as 'u32 / u64' have a size determined by the
architecture, either 32 or 64 bits.

.. note::

    Usage legend: R=Required, O=Optional, OR=Optional but Recommended,
    SD=See Definition

Many of these sections refer to the Devicetree Specification [DTspec]_.

4.1 Standard Properties and Property Values
---------------------------------------------

4.1.1 Property Values
~~~~~~~~~~~~~~~~~~~~~

A property value is an array of zero or more bytes that contain information
associated with the property.

Properties might have an empty value if conveying true-false information. In
this case, the presence or absence of the property is sufficiently descriptive.

Here are list of standard value types defined by the DTSpec [DTspec]_:

.. tabularcolumns:: | p{4cm} p{12cm} |
.. _property-values-table:
.. table:: Property values
   :class: longtable

   ======================== ==================================================================
   Value                    Description
   ======================== ==================================================================
   ``<empty>``              Value is empty. Used for conveying true-false information, when
                            the presence or absence of the property itself is sufficiently
                            descriptive.
   ``<u32>``                A 32-bit integer in big-endian format. Example: the 32-bit value
                            0x11223344 would be represented in memory as:

                               ::

                                  address    11
                                  address+1  22
                                  address+2  33
                                  address+3  44
   ``<u64>``                Represents a 64-bit integer in big-endian format. Consists of
                            two ``<u32>`` values where the first value contains the most
                            significant bits of the integer and the second value contains
                            the least significant bits.

                            Example: the 64-bit value 0x1122334455667788 would be
                            represented as two cells as: ``<0x11223344 0x55667788>``.

                            The value would be represented in memory as:

                               ::

                                    address  11
                                  address+1  22
                                  address+2  33
                                  address+3  44
                                  address+4  55
                                  address+5  66
                                  address+6  77
                                  address+7  88
   ``<string>``             Strings are printable and null-terminated. Example: the string
                            "hello" would be represented in memory as:

                               ::

                                    address  68  'h'
                                  address+1  65  'e'
                                  address+2  6c  'l'
                                  address+3  6c  'l'
                                  address+4  6f  'o'
                                  address+5  00  '\0'
   ``<prop-encoded-array>`` Format is specific to the property. See the property definition.
   ``<phandle>``            A ``<u32>`` value. A *phandle* value is a way to reference another
                            node in the devicetree. Any node that can be referenced defines
                            a phandle property with a unique ``<u32>`` value. That number
                            is used for the value of properties with a phandle value
                            type.
   ``<stringlist>``         A list of ``<string>`` values concatenated together.

                            Example: The string list "hello","world" would be represented in
                            memory as:

                               ::

                                      address  68  'h'
                                    address+1  65  'e'
                                    address+2  6c  'l'
                                    address+3  6c  'l'
                                    address+4  6f  'o'
                                    address+5  00  '\0'
                                    address+6  77  'w'
                                    address+7  6f  'o'
                                    address+8  72  'r'
                                    address+9  6c  'l'
                                   address+10  64  'd'
                                   address+11  00  '\0'
   ======================== ==================================================================


4.1.2 Standard Properties
~~~~~~~~~~~~~~~~~~~~~~~~~~

[DTspec]_ defines a list of standard properties that is commonly used across
many DT nodes. Due to its enormous amount of details, please refer to [DTspec]_
Chapter 2.3 (Standard Properties) directly for the full details of each standard
properties.

Here is a list of example standard properties:

* compatible
* model
* phandle
* status
* #address-cells and #size-cells
* reg
* virtual-reg
* ranges
* dma-ranges

Here are the standard properties that are used for this spec:

.. _sp_acsc:

4.1.2.1 #address-cells and #size-cells
""""""""""""""""""""""""""""""""""""""""

Property name: ``#address-cells``, ``#size-cells``

Value type: ``<u32>``

Description:

   The *#address-cells* and *#size-cells* properties may be used in any
   device node that has children in the devicetree hierarchy and describes
   how child device nodes should be addressed. The *#address-cells*
   property defines the number of ``<u32>`` cells used to encode the address
   field in a child node's *reg* property. The *#size-cells* property
   defines the number of ``<u32>`` cells used to encode the size field in a
   child node’s *reg* property.

   Here are some important notes:

   * The *#address-cells* and *#size-cells* properties are not inherited from 
     ancestors in the devicetree. They shall be explicitly defined.

   * A spec-compliant boot program shall supply *#address-cells* and
     *#size-cells* on all nodes that have children.

   * If missing, it should be assumed that a default value of 2 for
     *#address-cells*, and a value of 1 for *#size-cells*.

Example:

   See the following devicetree excerpt:

   .. code-block:: dts

      soc {
         #address-cells = <1>;
         #size-cells = <1>;

         serial@4600 {
            compatible = "ns16550";
            reg = <0x4600 0x100>;
            clock-frequency = <0>;
            interrupts = <0xA 0x8>;
            interrupt-parent = <&ipic>;
         };
      };

   In this example, the *#address-cells* and *#size-cells* properties of the
   ``soc`` node are both set to 1. This setting specifies that one cell is
   required to represent an address and one cell is required to represent the
   size of nodes that are children of this node.

   The serial device *reg* property necessarily follows this specification
   set in the parent (``soc``) node—the address is represented by a single cell
   (0x4600), and the size is represented by a single cell (0x100).


.. _sp_reg:

4.1.2.2 reg
""""""""""""""

Property name: ``reg``

Property value: ``<prop-encoded-array>`` encoded as an arbitrary number of
(*address*, *length*) pairs.

Description:

   The *reg* property describes the address of the device’s resources
   within the address space defined by its parent bus. Most commonly this
   means the offsets and lengths of memory-mapped IO register blocks, but
   may have a different meaning on some bus types. Addresses in the address
   space defined by the root node are CPU real addresses.

   The value is a *<prop-encoded-array>*, composed of an arbitrary number
   of pairs of address and length, *<address length>*. The number of
   *<u32>* cells required to specify the address and length are
   bus-specific and are specified by the *#address-cells* and *#size-cells*
   properties in the parent of the device node. If the parent node
   specifies a value of 0 for *#size-cells*, the length field in the value
   of *reg* shall be omitted.

Example:

   Suppose a device within a system-on-a-chip has two blocks of registers, a
   32-byte block at offset 0x3000 in the SOC and a 256-byte block at offset
   0xfe00. The *reg* property would be encoded as follows (assuming
   *#address-cells* and *#size-cells* values of 1):

      ``reg = <0x3000 0x20 0xfe00 0x100>;``


.. _sp_ranges:

4.1.2.3 ranges
""""""""""""""""

Property name: ``ranges``

Value type: ``<empty>`` or ``<prop-encoded-array>`` encoded as an arbitrary
number of (*child-bus-address*, *parent-bus-address*, *length*) triplets.

Description:

   The *ranges* property provides a means of defining a mapping or
   translation between the address space of the bus (the child address
   space) and the address space of the bus node’s parent (the parent
   address space).

   The format of the value of the *ranges* property is an arbitrary number
   of triplets of (*child-bus-address*, *parent-bus-address*, *length*)

   * The *child-bus-address* is a physical address within the child bus'
     address space. The number of cells to represent the address is bus
     dependent and can be determined from the *#address-cells* of this node
     (the node in which the *ranges* property appears).
   * The *parent-bus-address* is a physical address within the parent bus'
     address space. The number of cells to represent the parent address is
     bus dependent and can be determined from the *#address-cells* property
     of the node that defines the parent’s address space.
   * The *length* specifies the size of the range in the child’s address space. 
     The number of cells to represent the size can be determined from the
     *#size-cells* of this node (the node in which the *ranges* property
     appears).

   If the property is defined with an ``<empty>`` value, it specifies that the
   parent and child address space is identical, and no address translation
   is required.

   If the property is not present in a bus node, it is assumed that no
   mapping exists between children of the node and the parent address
   space.

Address Translation Example:

   .. code-block:: dts

       soc {
          compatible = "simple-bus";
          #address-cells = <1>;
          #size-cells = <1>;
          ranges = <0x0 0xe0000000 0x00100000>;

          serial@4600 {
             device_type = "serial";
             compatible = "ns16550";
             reg = <0x4600 0x100>;
             clock-frequency = <0>;
             interrupts = <0xa 0x8>;
             interrupt-parent = <&ipic>;
          };
       };

   The ``soc`` node specifies a *ranges* property of

      ``<0x0 0xe0000000 0x00100000>;``

   This property value specifies that for a 1024 KB range of address space,
   a child node addressed at physical 0x0 maps to a parent address of
   physical 0xe0000000. With this mapping, the ``serial`` device node can
   be addressed by a load or store at address 0xe0004600, an offset of
   0x4600 (specified in *reg*) plus the 0xe0000000 mapping specified in
   *ranges*.


.. _sp_dma-ranges:

4.1.2.4 dma-ranges
""""""""""""""""""""

Property name: `dma-ranges``

Value type: ``<empty>`` or ``<prop-encoded-array>`` encoded as an arbitrary
number of (*child-bus-address*, *parent-bus-address*, *length*) triplets.

Description:

   The *dma-ranges* property is used to describe the direct memory access (DMA)
   structure of a memory-mapped bus whose devicetree parent can be accessed from
   DMA operations originating from the bus. It provides a means of defining a
   mapping or translation between the physical address space of the bus and the
   physical address space of the parent of the bus.

   The format of the value of the *dma-ranges* property is an arbitrary number
   of triplets of (*child-bus-address*, *parent-bus-address*, *length*). Each
   triplet specified describes a contiguous DMA address range.

   * The *child-bus-address* is a physical address within the child bus'
     address space. The number of cells to represent the address is bus
     dependent and can be determined from the *#address-cells* of this node
     (the node in which the *dma-ranges* property appears).
   * The *parent-bus-address* is a physical address within the parent bus'
     address space. The number of cells to represent the parent address is
     bus dependent and can be determined from the *#address-cells* property
     of the node that defines the parent’s address space.
   * The *length* specifies the size of the range in the child’s address space. 
     The number of cells to represent the size can be determined from the
     *#size-cells* of this node (the node in which the *dma-ranges* property
     appears).



4.2 UPL Devicetree Nodes
---------------------------------------------

Here is the list of devicetree nodes for UPL usage:

4.2.1 Node: / (Root Node) (R)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tabularcolumns:: | p{3cm} p{0.75cm} p{2cm} p{9.5cm} |
.. table:: Node: /

   ================= =========== ============ ======================================================
   Property          Usage       Value Type   Definition
   ================= =========== ============ ======================================================
   #address-cells    R           u32          Specifies the number of <u32> cells to represent the
                                              address in the reg property in children of root.
   #size-cells       R           u32          Specifies the number of <u32> cells to represent the
                                              size in the reg property in children of root.
   ================= =========== ============ ======================================================


4.2.2 Node: /options/upl-params (R)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These are the generic parameters / settings of the UPL payload.

.. tabularcolumns:: | p{3cm} p{0.75cm} p{2cm} p{9.5cm} |
.. table:: Node: /options/upl-params

   ================= =========== ============ ======================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
   Property          Usage       Value Type   Definition
   ================= =========== ============ ======================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
   compatible        R           string       "upl"
   boot-mode         O           string list  For supporting different Payload boot flows. These influence how the payload runs. Note that this is not intended to support multiple Payloads.
                                              This string list is not meant to be prescriptive and only serves as an example data handoff, as long as Payload is able to recognise the value. Furthermore,
                                              Payload is not required to support all of the boot modes. For boot modes those are not supported by Payload, Payload can just ignore them without any specific
                                              actions. This property could be further refined in the future revisions.

                                              * “normal” means booting with full functionality, from power off.
                                              * “fast” means fast boot with no configuration change or minimal functionality.
                                              * “full", "diag” means booting with full functionality plus diagnostics functions.
                                              * “default” means booting with “reset to default” flow (for example, boot from RTC battery power failure).
                                              * “s4” means resuming from ACPI S4 state (resume from disk).
                                              * “factory” means booting with manufacturing mode.
                                              * “s3” means resuming from ACPI S3 state (resume from memory).
   addr-width        O           u32          52 means host address width is 52 bits. 46 means address width is 46 bits.
                                              This is mainly used by Payloads when initializing page tables. This can avoid the payload needing to access the SoC directly to obtain this information.
   pci-enum-done     O           empty        When pci-enum-done present, payload will skip PCI resource assignment and it will use pci-rb node information to create internal resource map to ensure no conflict
                                              usage of those in-used PCI resources during payload execution.

                                              When pci-enum-done not present, payload may do the PCI enumeration to assign resources basing on pci-rb node information, and could also create resource map too.

                                              In some payloads, a simple PCI enumeration may still be executed even with “pci-enum-done” to collect PCI device information and bind corresponding drivers to
                                              provide services and functionality. 
                                              (for example, find out network controller and bind network driver to support network functionality)
   ================= =========== ============ ======================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================


4.2.3 Node: /options/upl-image@<addr> (R)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The behavior of Platform Init when loading a FIT cannot always be known at build
time. For example:

* Platform Init may select one of several configurations when loading the
  Payload; the configuration chosen may depend on the hardware that it is
  running on
* Platform Init may load images to any address if there is no 'load' property in
  the image.

The Payload may need to know where one of the images ended up in memory, or
which configuration was chosen. It cannot find this out by itself. The
'image' node provides information to help with these problems.

.. tabularcolumns:: | p{4cm} p{0.75cm} p{4cm} p{6.5cm} |
.. table:: Node: /options/upl-images@<addr>

   ================= =========== ================== ======================================================================================================================================================================
   Property          Usage       Value Type         Definition
   ================= =========== ================== ======================================================================================================================================================================
   reg               SD          prop-encoded array Address and size of FIT image that was loaded and executed to reach this point. This is required if the Payload must have access to the FIT to operate, e.g., if
                                                    Platform Init does not load the images to a new address. Otherwise, it is optional.
   conf-offset       O           u32                Offset within FIT of the configuration node that was selected.
   ================= =========== ================== ======================================================================================================================================================================


4.2.4 Node: /options/upl-image/image@<addr> (O)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This node is only required if Platform Init loaded the images to different
addresses. In the case where the FIT is used in-place, this is not needed.

The name of this node must match the name of the corresponding image node in the
FIT. This provides information about the loaded images.

Each loaded image has a separate node created with the following properties:

.. tabularcolumns:: | p{3cm} p{0.75cm} p{2cm} p{9.5cm} |
.. table:: /options/upl-image/image@<addr>

   ================= =========== ================== ======================================================================================================================================================================
   Property          Usage       Value Type         Definition
   ================= =========== ================== ======================================================================================================================================================================
   reg               R           prop-encoded array Address and size that the image was actually loaded to. This is normally the same as the image load address within the FIT, but can be different if anything was
                                                    relocated, or if the FIT did not provide a load address.
   offset            O           u32                Offset within FIT of the image node for this image.
   description       R           string             Description value for this image from the FIT.
   ================= =========== ================== ======================================================================================================================================================================


4.2.5 Node: /pci (R)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Payload may need below FDT nodes for collecting PCI devices information on the
system for binding corresponding drivers to provide services and functionality.

There could be 2 or more root bridge nodes and even the same PCI segment may be
shared by several root bridges. In this case ecam-base-addr in the PCI root
bridge node is important for payload to know how to access each root bridge as
well as what segment they belong to. (by masking bus/dev/func, the same
ecam-base-addr will be the same segment root bridges).

Under each root bridge node, there could be several root ports and/or PCI
devices listed as its child nodes. Please refer the example use case below for
reference implementation.

The PCI bindings in this node must follow this specification - the IEEE Std
1275-1994 Standard for Boot (Initialization Configuration) Firmware
[PCIBusBinding]_ with some restrictions.

As the #address-cells is always 3, the child / PCI address has to be presented
in this format, **per PCI Bus Binding spec** [PCIBusBinding]_:

* The non-prefetchable and prefetchable memory windows must each be exactly
  256MB (0x10000000) in size.
* The prefetchable memory window must be immediately adjacent to the
  non-prefetcable memory window.

Here is a bitmap of the 3-cell address which is followed by the explanation of
each bit:

* Cell 1: npt000ss bbbbbbbb dddddfff rrrrrrrr
* Cell 2: hhhhhhhh hhhhhhhh hhhhhhhh hhhhhhhh
* Cell 3: llllllll llllllll llllllll llllllll

Notes:

* n: 0 if the address is relocatable, 1 otherwise
* p: 1 if the addressable region is "prefetchable", 0 otherwise
* t: 1 if the address is aliased (for non-relocatable I/O), below 1 MB (for
  Memory), or below 64 KB (for relocatable I/O)
* ss: space code

  * 00: configuration space
  * 01: I/O space
  * 10: 32 bit memory space
  * 11: 64 bit memory space

* bbbbbbbb: The PCI bus number
* ddddd: The device number
* fff: The function number
* rrrrrrrr: Register number. Not used.

.. Long table support added to prevent table overflow in latex pdf generation

.. tabularcolumns:: | p{3cm} p{0.75cm} p{2cm} p{9.5cm} |
.. table:: /pci/<pci-device>@<ecam-base-address>
   :widths: auto
   :class: longtable

   ================= =========== ==================== ======================================================================================================================================================================================================================================================================================================================================================================================================================================
   Property Name     Usage       Value Type           Definition
   ================= =========== ==================== ======================================================================================================================================================================================================================================================================================================================================================================================================================================
   compatible        R           string list          To determine what kind of driver should be applied to the device. It should be in the form of <manufacturer>,<model>. But for historical reason,
                                                      <model> alone also works for common used devices. For this spec, 'pci-rb' is recommended to specify it is a PCI root brige node.
   #address-cells    R           u32                  Indicates the number of cells used in addresses in the handoff.

                                                      Per PCI Bus Binding spec [PCIBusBinding]_, **this value must be 3**.
   #size-cells       R           u32                  Indicates the number of cells used for sizes in the handoff.

                                                      Per PCI Bus Binding spec [PCIBusBinding]_, **this value must be 2**.
   bus-range         SD          prop-encoded-array   Contains 2 cells, each encoded as with encode-int, the first representing the loweest bus number of the PCI bus implemented by the bus controller
                                                      represented by this node (the secondary bus number in PCI-to-PCI bridge nomenclature), and the second representing the largest bus number of any
                                                      PCI bus in the portion of the PCI domain that is subordinate to this node (the subordinate bus number in PCI-to-PCI bridge nomenclature).

                                                      This is required for Payload to do a simple PCI scan to build a PCI device database for providing functionality/service drivers (graphics, USB,
                                                      SATA…)

                                                      This property is mandatory for a PCI root bridge node.
   reg               R           prop-encoded-array   Refer to here for generic definition: :ref:`sp_reg`

                                                      Indicates an address range that are used by the PCI devices under the current bridge. It is a range that the CPU (parent bus) can access. The
                                                      form of reg is <[address1 size1] [address2 size2] [address3 size3] ...>. As the reg data presents the address range in the parent memory space,
                                                      so it is the parent's cell count of address and size used.
   ranges            SD          prop-encoded-array   Refer to here for generic definition: :ref:`sp_ranges`
                                 or empty             
                                                      For this node, ranges data is in the form of PCI address, CPU address, PCI size. The cells of PCI address is the value of #address-cells in PCI
                                                      node (3). The cells of CPU address is the value of #address-cells in the parent node. The cells of PCI size is the value of #size-cells in PCI
                                                      node (2).

                                                      The data is used to define IO, prefetchable/non-prefetchable MMIO resources that can be utilized for the root bridge which can be assigned to
                                                      downstream devices.
                                                      
                                                      The ranges include those MMIO or IO which are already assigned to downstream devices and available for future new devices.

                                                      If the property is defined with an <empty> value, it specifies that the parent and child address space is identical, and no address translation is required.

                                                      If the property is not present in a bus node, it is assumed that no mapping exists between children of the node and the parent address space.
   dma-ranges        O           prop-encoded-array   Refer to here for generic definition: :ref:`sp_dma-ranges`
                                 or empty             
                                                      Define the DMA address width capability of the root bridge. If only below 4GB region was defined, the payload may assume above 4GB DMA is not
                                                      supported.
   ================= =========== ==================== ======================================================================================================================================================================================================================================================================================================================================================================================================================================

An example showing multiple top-level PCI nodes each with its own bus range:

.. code-block:: dts

   
   //1st pci-rb in its separate segment of PCIEXBAR 0xC0000000
   pci-rb0@c0000000 {
      compatible = "pci-rb";
      #address-cells = <3>;
      #size-cells = <2>;
      bus-range = <0x01 0xdf>;
      reg = <0x0 0xc0000000 0x1 0x0000000>; // whole ECAM region in this root bridge
      ranges = <...>;
      //several root ports
      //properties
   };

   // 2nd pci-rb in the shared segment base of PCIEXBAR 0xE0000000
   pci-rb1@e0000000 {
      compatible = "pci-rb";
      #address-cells = <3>;
      #size-cells = <2>;
      bus-range = <0x24 0x4b>;
      reg = <0x0 0xe0000000 0x0 0x8000000>; //whole ECAM region in this root bridge

      //non-reloc/non-prefetch/mmio, child-addr, parent-addr, length
      ranges = <0x82000000 0x0 0x92000000 0x0 0x92000000 0x0 0x10BC0000

      //non-reloc/non-prefetch/mmio, child-addr, parent-addr, length
      0x82000000 0x2040 0x00000000 0x2040 0x00000000 0x1 0x40000000

      //non-reloc/32bit/io, child-addr, parent-addr, length
      0x81000000 0x0 0x4000 0x0 0x4000 0x0 0x2000>;

      //non-reloc/non-prefetch/memory, child-addr, parent-addr, length
      //indicate rb1 does not support above 4GB DMA
      dma-ranges = <0x82000000 0x0 0x0 0x0 0x0 0x1 0x0>; // 0 ~ 4GB

      //first root port is B0:D0:F0
      rootport0@0,0 {
         #address-cells = <3>;
         #size-cells = <2>;
         reg = <...>;
         /* MMIO, IO resource assigned to this root port that can be consumed by
         its downstream devices. */
         ranges; 
      };
   };

   /* The 3rd pci-rb in the shared segment base of PCIEXBAR 0xE0000000 (starting
   from 0xE8000000) */
   pci-rb2@e8000000 {
      compatible = "pci-rb";
      #address-cells = <3>;
      #size-cells = <2>;
      bus-range = <0x81 0xc8>;
      reg = <0x0 0xe8000000 0x0 0x8000000>; //whole ECAM region in this root bridge
      //MMIO, IO resource owned by this root bridge
      ranges = <...>;

      //non-reloc/non-prefetch/memory, child-addr, parent-addr, length
      //indicate rb2 does not support above 4GB DMA
      dma-ranges = <0x82000000 0x0 0x0 0x0 0x0 0x1 0x0>; // 0 ~ 4GB

      //first root port is B128: D0: F0
      rootport0@0,0 {
         reg = <...>;
         /* MMIO, IO resource assigned to this root port that can be consumed by
         its downstream devices. */
         ranges;
      };
   };


4.2.6 Node: /isa (O)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are different kinds of buses each using their own addressing scheme. Among
them are usually memory addresses, legacy I/O Ports and PCIe. In summary
one needs to surround the node using legacy I/O ports with a “isa” bus node.

For clarification, this node can be used for LPC and eSPI devices, as from
software pespective, both are ISA compatible.

.. tabularcolumns:: | p{3cm} p{0.75cm} p{2cm} p{9.5cm} |
.. table:: Node: /isa

   ================= =========== =================== ==============================================
   Property Name     Usage       Value Type          Definition
   ================= =========== =================== ==============================================
   compatible        R           string              "isa"
   #address-cells    R           u32                 2
   #size-cells       R           u32                 1
   ranges            SD          prop-encoded-array  Refer to here for generic definition:
                                 or empty            :ref:`sp_ranges`
                                                     
                                                     Required for memory accesses or memory mapped
                                                     I/O space. Optional if only indirect I/O is
                                                     supported. Not required for legacy I/O.
   ================= =========== =================== ==============================================

Specific legacy I/O devices are descirbed in child nodes. For UPL usage, only
serial console is supported for now - further legacy I/O devices can be expended
later if required. Please refer to :ref:`serial_console` for serial console use
cases.

For its child node, 'reg' property is required, and it is in the format of:
<(enum) (address) (size)>; and here is the usage for the `enum`:
* 0x0   # memory address
* 0x1   # I/O address


.. _serial_console:

4.2.7 Node: Serial Console Device (SD)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This refers to the debug / log console, where Payload can setup and use the same
UART controller as Platform Init for seamless debug output. There can be more
than one UART controller defined, and the '/chosen' node must include a
'stdout-path' property pointing to this device when it is used, as per
[DTspec]_.

This node is mandatory if a serial device is available and initialized by
Platform Init.

.. tabularcolumns:: | p{3cm} p{0.75cm} p{2cm} p{9.5cm} |
.. table:: Node: serial@<addr>

   ================= =========== ================== ======================================================================================================================================================================
   Property Name     Usage       Value Type         Definition
   ================= =========== ================== ======================================================================================================================================================================
   compatible        R           string list        Compatible string for hardware.
                                                    Currently, these compatible strings are supported:
                                                    ns16550a, ns16550, ns8250, ns16450
   clock-frequency   R           u32                Frequency (in Hz) of the baud rate generator’s input clock.
   current-speed     R           u32                Current serial device speed in bits per second.
   reg               R           prop-encoded-array Physical address of the registers device within the address space of the parent. The form of reg is
                                                    <[address] [size]>
   reg-shift         O           u32                log2 of distance between the discrete device registers. If unspecified, the default value is 0, meaning 1 byte apart.
   reg-offset        O           u32                Offset of the registers from the base address. The default value is 0, meaning no offset.
   reg-io-width      O           u32                Register width in bytes. Valid values are 1, 2 and 4. The default value is 1, meaning byte width.
   virtual-reg       SD          u32 or u64         Specifies an effective address that maps to the first physical address specified in the reg property. This property is
                                                    required if this device node is the system’s console.
   ================= =========== ================== ======================================================================================================================================================================


Example below shows a legacy I/O serial device and an MMIO serial device:

.. code-block:: dts

   
   // Legacy I/O serial device
   isa {
      compatible = "isa";
      #address-cells = <2>;
      #size-cells = <1>;

      serial@3f8 {
         compatible = "ns16550";
         reg-io-width = <1>;
         reg = <1 0x3f8 8>;
         clock-frequency = <0x1c2000>;
         current-speed = <115200>;
      };
   };

   // MMIO serial device
   serial@fe037000 {
      compatible = "ns16550a";
      reg-io-width = <4>;
      reg = /bits 64/ <0xfe037000 0x80>;
      clock-frequency = <0x1c2000>;
      current-speed = <1500000>;
   };


Another example showing an MMIO serial device under PCI node:

.. code-block:: dts

   
   pci-rb0 {
      compatible = "pci";
      #address-cells = <3>;
      #size-cells = <2>;
      ...
      serial@fe037000 {
         compatible = "ns16550a";
         reg-io-width = <4>;
         //non-prefetchable, non-relocable, non-aliased 32bit MMIO
         reg = <0x82000000 0 0xfe037000 0 0x80>;
         clock-frequency = <0x1c2000>;
         current-speed = <1500000>;
      };
   };


4.2.8 Node: framebuffer (for Display) (SD)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Normally only one framebuffer is provided in the handoff. It should be the
'primary' one (if such a concept exists in the system) and visible to the user.
A 'display0' alias should provide the full path to the device. Where the device
itself is not represented in the devicetree, the 'display0' alias should point
to the simple-framebuffer node.

Look at the display0 alias. If this is a simple-framebuffer, then use that
If not, search for a node with the "simple-framebuffer" compatible string, which
has a 'display' property matching the display0 alias.

Note: If more than one framebuffer/ display device exist, the stdout-path in 
'chosen' node must point to the freamebuffer node preferred to be used by the
payload (in the case that only a single display output is supported by payload).

.. tabularcolumns:: | p{3cm} p{0.75cm} p{2cm} p{9.5cm} |
.. table:: Node: framebuffer@<addr>

   ================= =========== ================== ======================================================================================================================================================================
   Property Name     Usage       Value Type         Definition
   ================= =========== ================== ======================================================================================================================================================================
   compatible        R           string             simple-framebuffer.
   reg               R           prop-encoded-array Graphic frame buffer’s base address and size.
   width             R           u32                pixels in the X dimension.
   height            R           u32                pixels in the Y dimension.
   stride            R           u32                bytes per line of pixels.
   format            R           string             * `a8b8g8r8` - 32-bit pixels, d[31:24]=a, d[23:16]=b, d[15:8]=g, d[7:0]=r
                                                    * `a8r8g8b8` - 32-bit pixels, d[31:24]=a, d[23:16]=r, d[15:8]=g, d[7:0]=b
                                                    * `a16b16g16r16` - 64-bit pixels, d[63:48]=a, d[47:32]=r, d[31:16]=g, d[15:0]=b
   redmask           R           u32                mask to red color intensity.
   greenmask         R           u32                mask to green color intensity.
   bluemask          R           u32                mask to blue color intensity.
   reservedmask      R           u32                mask to reserved color intensity.
   pixelsperscanline R           u32                number of pixel elements per video memory line.
   display           R           string             Point to the PCI graphics device which provides this framebuffer as the primary display device.
   ================= =========== ================== ======================================================================================================================================================================

Example below shows how framebuffer node is generated:

Example 1 (non-PCI):

.. code-block:: dts

   
   // Optional alias
   aliases {
      display0 = &framebuffer0;
   };

   framebuffer0: framebuffer@b0000000 {
      compatible = "simple-framebuffer";
      reg =<0x0 0xb0000000 0x040 0x500000>;
      width = <1280>;
      height = <1024>;
      format = "a8r8g8b8";
   };


Example 2: (PCI)

.. code-block:: dts

   
   // Optional alias
   aliases {
      display0 = &gma;
   };

   pcie@10000000 {
      compatible = "pci-host-ecam-generic";
      reg = <...>
      ranges = <...>;
      pcie@8 {
         /* Root port 00:01.0 */
         reg = <0x00000800 0 0 0 0>;
         ranges = <...>;
         gma: gma@2,0 {
            /* gfx device 01:00.0 */
            reg = <0x00010000 0 0 0 0>;
         };
      };
   };

   framebuffer@b0000000 {
      compatible = "simple-framebuffer";
      reg = <0xb0000000>; // or use the BAR to access the framebuffer
      // these likely come from EDID talking to the panel
      width = <3840>;
      height = <2160>;
      format = "a8r8g8b8";
      display = <&gma>;
   };



4.2.9 Node: chosen (R)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For details about chosen node, please refer to [DTspec]_ Chapter 3.6 for the
chosen node usage. For the UPL usecase, please refer to the example below:

.. note::

   In this case the stdout is printed to two serial ports and one graphical
   framebuffer simultaneously.

.. code-block:: dts

   
   chosen {
      bootargs = "root=/dev/nfs rw nfsroot=192.168.1.1 console=ttyS0,115200";
      stdout-path = "/soc/serial0", "/soc/serial1", "/soc/framebuffer1";
   };


4.2.10 Node: /options/upl-custom (O)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Since the firmware sometimes might require additional/ customized information to
be passed in due to some very specific use cases (for example, the vendor might
add specific data to be consumed by Payload for specific setup or driver use
cases like Intel CSME Features), hence custom nodes are allowed here for the
flexibility. If the node data becomes common or popular enough in the future,
we can create a separate node later for that node data.

4.2.11 Node: /memory (R)
~~~~~~~~~~~~~~~~~~~~~~~~

The memory node is required to describe the physical-memory layout for the
system. If a system has multiple ranges of memory, multiple memory nodes can
be created, or the ranges can be specified in the reg property of a single
memory node. See the Devicetree Specification ("/memory node" section) for
details.

.. tabularcolumns:: | p{3cm} p{0.75cm} p{2cm} p{9.5cm} |
.. table:: Node: memory@<base_address>

  =================== ===== ============== ======================================
  Property Name       Usage Value Type     Definition
  =================== ===== ============== ======================================
  device_type         R     string         Value shall be 'memory'
  reg                 R     prop-encoded-  Specify system memory region range.
                            array          Consists of an arbitrary number of
                                           address and size pairs that specify
                                           the physical address and size of the
                                           memory ranges.
  initial-mapped-area O     prop-encoded-  <u64 - effective address, u64 - 
                            array          physical address, u32 - size>.
                                           Specifies the address and size of the
                                           Initial Mapped Area.
  hotpluggable        O     boolean        Specifies an explicit hint to the
                                           operating system that this memory may
                                           potentially be removed later.
  ecc-detection-bits  O     u32            If present, this indicates the number
                                           of bits of memory error which can be
                                           detected and reported by the Error-
                                           Correction Code (ECC) memory subsystem
                                           (typically 0, 1 or 2)
  ecc-correction-bits O     u32            If present, this indicates the number
                                           of bits of memory error which can be
                                           corrected by the Error-Correction Code
                                           (ECC) memory subsystem (typically 0, 1
                                           or 2)
  =================== ===== ============== ======================================


Example::

    #address-cells = 2;
    #size-cells = 2;
    memory@0 {
        reg = /bits 64/ <0x00 0xa0000>;
        device_type = "memory";
    };
    memory@100000 {
        reg = /bits 64/ <0x100000 0x500000>;
        device_type = "memory";
        ecc-detection-bits = <1>;
        ecc-correction-bits = <1>;
    };
    memory@500000 {
        reg = /bits 64/ <0x500000 0x5e8d0000>;
        device_type = "memory";
    };

Example::

    #address-cells = 2;
    #size-cells = 2;
    memory@000000000 {
        device_type = "memory";
        reg = /bits 64/ < 0x000000000 0x80000000 >;
        attribute = < 0x0000000000000001 >;
    };
    memory@1000000000 {
        device_type = "memory";
        reg = < 0x000000001 0x00000000 0x00000001 0x00000000 >;
        attribute = < 0x0000000000000000 >;
    };


4.2.12 Node: reserved-memory (R)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Both the reserved memory description models, namely **simple descriptor (Memory
Reservation Block)** and **standard descriptor (reserved memory node)** are
supported to provide information about memory which is not available for use.
Payload shall exclude reserved memory from normal usage.

If Memory Reservation Block is used, payload is free to chose default attributes
it wants to assign to this block. What is guaranteed is that this memory will be
provided to OS as "reserved" memory. No memory optimisations (such as reclaim
etc.) will be possible. On the other hand, standard reserved memory node will
provide better control over memory range handling in firmware.

For further information on Memory Reservation Block, please refer to [DTspec]_
Chapter 5.3.

Here are the table description for standard reserved memory node. One can create
child nodes describing particular reserved (excluded from normal use) memory
regions. Such memory regions are usually designed for the special usage by
various device drivers.

Each child of the reserved-memory node specifies one or more regions of reserved
memory. Each child node may either use a 'reg' property to specify a specific
range of reserved memory, or a 'size' property with optional constraints to
request a dynamically allocated block of memory.

Following the generic-names recommended practice, node names should reflect the
purpose of the node (ie. "framebuffer" or "dma-pool"). Unit address (@<address>)
should be appended to the name if the node is a static allocation.

.. tabularcolumns:: | p{3cm} p{0.75cm} p{2cm} p{9.5cm} |
.. table:: Node: reserved-memory

  ================ =========== =================== ======================================================
   Property Name   Usage       Value Type          Definition
  ================ =========== =================== ======================================================
   #address-cells  R           u32                 Refer to here for generic definition: :ref:`sp_acsc`
   #size-cells     R           u32                 Refer to here for generic definition: :ref:`sp_acsc`
   ranges          SD          prop-encoded-array  Refer to here for generic definition: :ref:`sp_ranges`
                               or empty
  ================ =========== =================== ======================================================

Child Node:

.. tabularcolumns:: | p{3cm} p{0.75cm} p{2cm} p{9.5cm} |
.. table:: Node: name@<base_address>

  =============== ======= =============== =====================================
   Property Name   Usage   Value Type      Definition
  =============== ======= =============== =====================================
   reg              R      u32 / 64 array Specify memory region of reserved
                                          memory
   no-map           O      boolean        If present, indicates the operating
                                          system must not create a virtual
                                          mapping of the region
   compatible       O      string list    *See definition below*
  =============== ======= =============== =====================================

**Compatible string list for Child Node:**

This is used to describe memory type for UPL usage. One of the example usage is
that Payload will be aware of where pre-installed ACPI tables or NVS regions are
and will adopt them for supporting additional ACPI table installation from
payload phase. Those boot-code / boot-data regions from Platform Init will be
reported to OS as usable memory without waste. Similarly, runtime-code /
runtime-data may be provided by Platform Init for supporting firmware runtime
services that will be used by OS. All of the below are optional and can be
skipped if unsupported by the platform.


  ================== ======================================================
  Compatible string       Description
  ================== ======================================================
    acpi              Memory that holds ACPI tables
    acpi-nvs          ACPI NVS buffer information
    boot-code         Memory that holds firmware phase drivers and will be
                      released to the OS when firmware boot phase finishes
                      (for example with a UEFI payload when ExitBootService
                      signaled).
    boot-data         Memory that holds firmware phase data consumed by drivers
                      and will be released to the OS when firmware boot phase
                      finishes (for example with a UEFI payload when
                      ExitBootService signaled).
    runtime-code      Runtime service code memory region which will be used
                      by OS runtime services.
    runtime-data      Runtime service data memory region which will be used
                      by OS runtime services.
    special-purpose   Specific-purpose memory (e.g.: HBM or CXL). The memory
                      is earmarked for specific purposes such as for specific
                      device drivers or applications.
                      
                      This attribute serves as a hint to the OS to avoid
                      allocating this memory for core OS data or code that
                      can not be relocated. Prolonged use of this memory for
                      purposes other than the intended purpose may result in
                      suboptimal platform performance.
    smbios            If Platform Init has created a SMBIOS data buffer, this
                      will have the SMBIOS data buffer region information.
                      SMBIOS 3.0 or above must be supported by payload.
  ================== ======================================================

Example::

    reserved-memory {
        #size-cells = <0x02>;
        #address-cells = <0x02>;
        mmio@fe000000 {
            reg = <0x00 0xfe000000 0x00 0x1000000>;
        };
        memory@78000000 {
            reg = <0x00 0x78000000 0x00 0x8000000>;
            no-map;
        };
        memory@a0000 {
            reg = <0x00 0xa0000 0x00 0x60000>;
            no-map;
        };
        memory@47168000 {
            compatible = "acpi";
            reg = <0x00 0x47168000 0x00 0x90000>;
        };
        memory@471f8000 {
            compatible = "acpi-nvs";
            reg = <0x00 0x471F8000 0x00 0x8000>;
        };
    };
