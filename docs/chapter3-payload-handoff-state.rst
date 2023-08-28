.. SPDX-License-Identifier: CC-BY-4.0

.. _chapter-payload-handoff-state:

Chapter 3: Payload Handoff State
================================

3.1 Overview
------------

This section describes the machine state and register settings for handing over
control to the Payload. This is naturally architecture-specific but where
possible a similar approach is followed for each architecture.


3.2 Requirements for all architectures
--------------------------------------

* Interrupts must be disabled so that an interrupt during handover will not
  cause ambiguity as to whether Platform Init or Payload will service the
  interrupt
* DMA must be disabled, so as to avoid undefined behaviour.
* At least 16KB must be available on the stack as passed through to the
  Payload. The stack must be aligned as defined by the architecture. Payload
  can set up its own stack from available memory when necessary, so the
  Platform Init stack should only be used for initial setup.

Some general guidelines:

* Set as few things as possible, because across the range of architectures,
  and implementations, very little is constant
* If page tables are set up, try to use GiB pages and coarse mappings. Kernels
  will change them anyway. It is not essential that we exactly match the page
  tables to available memory; e.g., we might have 4.5 GiB of memory and set up
  page tables for 5 GiB. That is acceptable as long as we accurately report
  memory size to the payload.
* Correct memory maps are critical. E820 is not sufficient to describe memory
  maps across all architectures. 
* Define what parameters need to be passed to the first payload, e.g. a pointer
  to the root of a table as the first arg, etc. The number of parameters should
  be kept small.


3.3 Architecture
----------------

This describes the handoff register settings for each architecture:

3.3.1 ARM
~~~~~~~~~

Register calling:-

32-bit::

   r0: Reserved, must be zero
   r1: divided into the following fields:
      r1[23:0]: set to the TL signature (0x6e_d0ff)
      r1[31:24]: version of the register convention used. Set to 0 for the convention specified in this document.
   r2: Pointer to FDT
   r3: Reserved, must be zero
   r13: Stack pointer
   r14: Link register (for returning to Platform Init)

64-bit::

   x0: Pointer to FDT
   x1:  divided into the following fields:
      x1[23:0]: set to the TL signature (0x6e_d0ff)
      x1[31:24]: version of the register convention used. Set to 0 for the convention specified in this document.
      x1[63:32]: reserved, must be zero.
   x2: Reserved, must be zero
   x3: Reserved, must be zero
   sp: Stack pointer
   r14: Return value, for returning to Platform Init

Additionally:

* Unaligned access must be enabled.
* If MMU is enabled, MMU configuration must use only 4k pages and a single
  translation base register (TTBR0)


3.3.2 RISC-V
~~~~~~~~~~~~

We should follow this standard: https://github.com/riscv-software-src/opensbi/blob/master/docs/firmware/fw.md

::

   a0/x10: hartid
   a1/x11: device tree blob address in memory via a1 register. The address must be aligned to 8 bytes.
   Valid sp (stack pointer register) containing valid sp address
   MMU should be disabled


3.3.3 x86
~~~~~~~~~

**Instruction execution environment**

Regardless of the environment where the Platform Init runs, the processor is in
32bit protected mode when a 32bit payload starts, or in 64bit long-mode when a
64bit payload starts. The payload header contains the machine type information
that the payload supports.
The following sections provide a detailed description of the execution
environment when the payload starts.

**Registers**

* Direction flag in EFLAGs is clear so the string instructions process from low
  addresses to high addresses.
* All other general-purpose register states are undefined.
* Floating-point control word is initialized to 0x027F (all exceptions masked,
  double-precision, round-to-nearest).
* Multimedia-extensions control word (if supported) is initialized to 0x1F80
  (all exceptions
* Masked, round-to-nearest, flush to zero for masked underflow).
* CR0.EM is clear.
* CR0.TS is clear.

32-bit:

ESP + 4 points to the address of the FDT table for the 32bit payload.

64-bit:

RCX holds the address of the FDT table for the 64bit payload.

**Interrupt**

The hardware is initialized by the Platform Init such that no interrupt triggers
even when the payload sets the Interrupt Enable flag in EFLAGs.

**Page table**

* Selectors are set to be flat.
* Paging mode may be enabled for the 32bit payload. (have general term on how it
  could be enabled if enabling page mode).
* Paging mode is enabled for the 64bit payload.
* When paging is enabled, all memory space is identity mapped (virtual address
  equals physical address). The four-level page table is set up. The payload
  can choose to set up the five-level page table as needed.

**Stack**

The stack is 16-byte aligned and may be marked as non-executable in page table.

**Application processors**

Payload starts on the bootstrap processor. All application processors (on a
multiple-processor system) are in halt state.

Payload may re-initialize the application processors to support multi-thread
process and Platform Init multi-processor service may not work after the payload
phase in this case.
