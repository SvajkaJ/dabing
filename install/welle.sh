#!/bin/bash

# Change path to welle
mkdir ~/welle.io/build
cd ~/welle.io/build && cmake ~/welle.io -DRTLSDR=1 -DBUILD_WELLE_IO=OFF
cd ~/welle.io/build && make
cd ~/welle.io/build && sudo make install
