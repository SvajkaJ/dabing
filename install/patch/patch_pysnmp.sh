#!/bin/bash
# This will only work when the rfc1902 will never be changed
# btw. library pysnmp is no longer maintained (should be ok)
cat ~/dabing/install/patch/rfc1902__patched.py > ~/.local/lib/python3*/site-packages/pysnmp/smi/rfc1902.py
