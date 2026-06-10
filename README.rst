Raspberry plugin
################

.. the following must be adapted to your developed package, links to pypi, github  description...

.. image:: https://img.shields.io/pypi/v/pymodaq_plugins_raspberry.svg
   :target: https://pypi.org/project/pymodaq_plugins_raspberry/
   :alt: Latest Version

.. image:: https://readthedocs.org/projects/pymodaq/badge/?version=latest
   :target: https://pymodaq.readthedocs.io/en/stable/?badge=latest
   :alt: Documentation Status

.. image:: https://github.com/PyMoDAQ/pymodaq_plugins_raspberry/workflows/Upload%20Python%20Package/badge.svg
   :target: https://github.com/PyMoDAQ/pymodaq_plugins_raspberry
   :alt: Publication Status

.. image:: https://github.com/PyMoDAQ/pymodaq_plugins_raspberry/actions/workflows/Test.yml/badge.svg
    :target: https://github.com/PyMoDAQ/pymodaq_plugins_raspberry/actions/workflows/Test.yml


Set of instrument plugins to be used from or on your Raspberry Pi.

This package merges the former ``pymodaq_plugins_raspberrypi3`` and
``pymodaq_plugins_raspberrypizero`` plugins into a single one. The differences
between boards (Raspberry Pi 3, Pi Zero, ...) are entirely described by
configuration: a sensor selects its driver, an actuator its control mode
(``PWM`` or ``DIGITAL``), so the same code base works with any test bench.

Authors
=======

* Sebastien J. Weber  (sebastien.weber@cnrs.fr)
* Fabien Villedieu (merge of the raspberrypi3 / raspberrypizero plugins)


Instruments
===========

Below is the list of instruments included in this plugin

Actuators
+++++++++

* **MoveRasp**: control of actuators (PWM or all-or-nothing) wired to a Raspberry,
  through a ZeroMQ link to the on-board server (see ``src_raspberry/``)

Viewer0D
++++++++

* **ViewRasp**: acquisition of I2C sensors (AHT10, TMP102, EMC2101, PT100, ...)
  wired to a Raspberry, through the same ZeroMQ link

Viewer2D
++++++++

* **picamera**: control of the integrated pi camera using the Picamera2 library

.. if needed use this field

    PID Models
    ==========


    Extensions
    ==========


Raspberry-side server
=====================

The ``MoveRasp`` / ``ViewRasp`` plugins talk to a server that must run **on the
Raspberry Pi**. Its source code lives in the ``src_raspberry/`` folder at the root
of this repository (it is a companion, non-packaged addition). It is organised in
interchangeable layers — ZeroMQ transport, JSON request handler, hardware backend —
each behind an interface, so the transport or the hardware communication can be
swapped without touching the rest. See ``src_raspberry/README.md`` for installation
and the JSON protocol.


Installation instructions
=========================

* PyMoDAQ’s version >= 5
* Tested on/with a Raspberry Pi 3 and a Raspberry Pi Zero
