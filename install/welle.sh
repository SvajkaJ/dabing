#!/bin/bash

# Change path to welle
mkdir ~/welle/build
cd ~/welle/build && cmake ~/welle -DRTLSDR=1 -DBUILD_WELLE_IO=OFF
cd ~/welle/build && make
cd ~/welle/build && sudo make install
