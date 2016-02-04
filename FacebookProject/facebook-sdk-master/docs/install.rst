============
Installation
============

The SDK currently supports Python 2.6, 2.7, 3.3, 3.4, and 3.5. The `requests`_
package is required.

We recommend using `pip`_ and `virtualenv`_ to install the SDK. Please note
that the SDK's Python package is called **facebook-sdk**: ::

Installing from Git
===================

For the newest features, you should install the SDK directly from Git.

.. code-block::

    virtualenv facebookenv
    source facebookenv/bin/activate
    pip install -e git+https://github.com/pythonforfacebook/facebook-sdk.git#egg=facebook-sdk

Installing a Released Version
=============================

If your application requires maximum stability, you will want to use a version
of the SDK that has been officially released.

.. code-block::

    virtualenv facebookenv
    source facebookenv/bin/activate
    pip install facebook-sdk

.. _requests: https://pypi.python.org/pypi/requests
.. _pip: http://www.pip-installer.org/
.. _virtualenv: http://www.virtualenv.org/
