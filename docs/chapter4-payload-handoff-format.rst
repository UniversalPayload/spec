.. SPDX-License-Identifier: CC-BY-4.0

.. _chapter-payload-handoff-format:

Chapter 4: Payload Handoff Format
=================================

Here we define the handoff information from Platform Init to Payload, and it
takes the form of an devicetree blob. This section describes the bindings used
for each area addressed by this specification.

A devicetree is a tree data structure with nodes that describe the devices in a
system. Each node has exactly one parent except for the root node, which has no
parent. Each node has property/value pairs that describe the characteristics of
the device being presented. Properties consist of a name and a value. Property
names are strings of 1 to 31 characters, property value is an array of zero or
more bytes that contain information associated with the property.

The sections below show what nodes should be passed from Platform Init and its
corresponding property / value. It does not change what is passed from the
Payload to the OS, but it is intended to avoid interfering with it, i.e. it uses
the same bindings where possible.

A pointer to the FIT is provided so that the running image can find other images
it needs and find out where they were loaded.

Note that properties indicated as 'u32 / u64' have a side determined by the
architecture, either 32 or 64 bits.

.. note::

    'Usage' legend for nodes: R=Required, O=Optional, OR=Optional but
     Recommended, SD=See Definition

Many of these sections reference the Devicetree Specification [DTspec]_.

TBD (Nodes)
