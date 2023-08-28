.. SPDX-License-Identifier: CC-BY-4.0

References & Terminology
========================

Abbreviation
------------

For the purposes of this document, the following abbreviations apply:

   ================= ===========================================
   Abbreviation      Description
   ================= ===========================================
   FIT               Flat Image Tree
   FDT               Flattened Device Tree
   UPL               Universal Payload
   ================= ===========================================


Terminology
-----------

   ============= =========================================== ============================
   Term          Definition                                  Examples
   ============= =========================================== ============================
   Platform Init Set up the hardware and memory, so that the coreboot, EDK2, OpenSBI,
                 Payload can interact with that hardware to  oreboot, Slim Bootloader, U-Boot SPL
                 prepare for an OS boot. For some projects
                 this is referred to as bootloader.
   Payload       As part of system firmware, it mainly       EDK2, Grub, LILO, LinuxBoot, SeaBIOS,
                 initializes boot media and boots the OS.    U-Boot
                 For some projects it is referred as OS
                 Loader.
   ============= =========================================== ============================


References
----------

.. [DTspec] `DeviceTree Specification Release v0.4
   <https://github.com/devicetree-org/devicetree-specification/releases/tag/v0.4>`_

.. [FITspec] `Flat Image Tree Specification Release v0.8
   <https://github.com/open-source-firmware/flat-image-tree/releases/tag/v0.8>`_
