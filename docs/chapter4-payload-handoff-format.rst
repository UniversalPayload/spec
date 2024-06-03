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

    'Usage' legend for nodes: R=Required, O=Optional, OR=Optional but
     Recommended, SD=See Definition

Many of these sections reference the Devicetree Specification [DTspec]_.

TBD (Nodes)

4.2.8 Node: /memory (R)
~~~~~~~~~~~~~~~~~~~~~~~

The memory node is required to describe the physical-memory layout for the
system. If a system has multiple ranges of memory, multiple memory nodes can
be created, or the ranges can be specified in the reg property of a single
memory node. See the Devicetree Specification ("/memory node" section) for
details.

.. tabularcolumns:: | p{3cm} p{0.75cm} p{2cm} p{9.5cm} |
.. table:: Node: memory@base_address

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


4.2.9 Node: reserved-memory (R)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The /reserved-memory node provides information about memory which is not available
for use. Payload shall exclude reserved memory from normal usage. One can create
child nodes describing particular reserved (excluded from normal use) memory
regions. Such memory regions are usually designed for the special usage by various
device drivers.

.. tabularcolumns:: | p{3cm} p{0.75cm} p{2cm} p{9.5cm} |
.. table:: Node: reserved-memory

  ================ =========== ============ =====================================
   Property Name       Usage     Value Type      Definition
  ================ =========== ============ =====================================
   #address-cells       R
   #size-cells          R
   ranges
  ================ =========== ============ =====================================

Child Node:

.. tabularcolumns:: | p{3cm} p{0.75cm} p{2cm} p{9.5cm} |
.. table:: Node: name@xxx

  =============== ======= =============== =====================================
   Property Name   Usage   Value Type      Definition
  =============== ======= =============== =====================================
   reg              R      u32 / 64 array  Specify memory region of reserved
                                           memory
   no-map           O      boolean         If present, indicates the operating
                                           system must not create a virtual
                                           mapping of the region
   compatible       O      string list
  =============== ======= =============== =====================================

Child Nodes for Payload Memory Types:
One of the example usage is that UEFI Payload will be aware of where pre-installed
acpi tables or NVS regions are and will adopt them for supporting additional ACPI
table installation from payload phase. Those boot-code/boot-data regions from
PlatformInit will be reported to UEFI OS as usable memory without waste. Similarly
runtime-code/runtime-data may be provided by PlatformInit for supporting UEFI
runtime services that will be used by UEFI OS. All of the below are optional
and can be skipped if unsupported by the platform. 


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
                      by OS runtime service
    runtime-data      Runtime service data memory region which will be used
                      by OS runtime service.
    smbios            If PlatformInit has created a SMBIOS data buffer, this
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
