#!/bin/bash
# Autor: SvajkaJ
# Date:  10.2.2022


# CREATE USER and DATABASE
# as a superuser postgres
sudo -u postgres psql -c "CREATE USER pi WITH PASSWORD 'slovensko' NOSUPERUSER"
sudo -u postgres psql -c "CREATE DATABASE dabing OWNER pi"


# CREATE TABLE
# as a user pi
psql -d dabing -c "CREATE TABLE IF NOT EXISTS dabing (id SERIAL NOT NULL PRIMARY KEY, snr REAL, ber REAL, power REAL, fiber REAL, signal BOOLEAN, sync BOOLEAN, tstz TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP(0))"


# TEST
#psql -d dabing -c "INSERT INTO dabing (ber, snr, power, fiber, signal, sync) VALUES (0.1, 0.2, 0.3, 0.4, TRUE, FALSE)"
#psql -d dabing -c "SELECT * FROM dabing"

