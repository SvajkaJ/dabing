#!/bin/bash
# Autor: SvajkaJ
# Date:  19.3.2022

# Make sure to leave no spaces around the equal sign.
# Otherwise, Bash will treat the variable name as a program to execute, and the = as its first parameter!

# ------------------------------- #
# ---------- CONSTANTS ---------- #
# ------------------------------- #

APT_PACKAGES=("python3" "python3-pip" "git" "postgresql" "postgresql-server-dev-all" "rtl-sdr" "cmake" "libfftw3-dev" "librtlsdr-dev" "libfaad-dev" "libmp3lame-dev" "libmpg123-dev" "libpq-dev" "libpqxx-dev" "alsa-utils" "libasound2-dev" "lame" "nginx")
PIP_PACKAGES=("pysnmp" "flask" "flask-cors" "flask-expects-json" "uptime" "uwsgi" "psycopg2")
SDR="Realtek Semiconductor Corp. RTL2838 DVB-T"

APT_STATE=("${APT_PACKAGES[@]/*/2}")
PIP_STATE=("${PIP_PACKAGES[@]/*/2}")

DEFAULT_COLOUR="\033[0;37m"
RED_COLOUR="\033[1;31m"
YELLOW_COLOUR="\033[1;33m"
GREEN_COLOUR="\033[1;32m"

# -------------------------------------------------- #
# ---------- CONFIGURING FILE PERMISSIONS ---------- #
# -------------------------------------------------- #

# Changing the access permissions of files
chmod +x ~/dabing/install/nginx.sh
chmod +x ~/dabing/install/postgresql.sh
chmod +x ~/dabing/install/welle.sh
chmod +x ~/dabing/install/patch/patch_pysnmp.sh
chmod +x ~/dabing/*.py # all .py files in dabing directory
touch ~/dabing/install/setup.log

# ----------------------------------------- #
# ---------- INSTALLING PACKAGES ---------- #
# ----------------------------------------- #

sudo apt-get update

echo -e "${YELLOW_COLOUR}COMMENCING INSTALLATION!${DEFAULT_COLOUR}"
PAD_LENGTH=20
for INDEX in ${!APT_PACKAGES[@]}
do
    printf "Installing: ${APT_PACKAGES[$INDEX]}"
    sudo apt-get -y install ${APT_PACKAGES[$INDEX]} >/home/pi/dabing/install/setup.log
    if [[ $? > 0 ]]
    then
        printf "%*.s ${RED_COLOUR}FAIL${DEFAULT_COLOUR}\n" $(($PAD_LENGTH - ${#APT_PACKAGES[$INDEX]}))
        APT_STATE[$INDEX]=0
    else
        printf "%*.s ${GREEN_COLOUR}SUCCESS${DEFAULT_COLOUR}\n" $(($PAD_LENGTH - ${#APT_PACKAGES[$INDEX]}))
        APT_STATE[$INDEX]=1
    fi
done

for INDEX in ${!PIP_PACKAGES[@]}
do
    printf "Installing: ${PIP_PACKAGES[$INDEX]}"
    pip3 install ${PIP_PACKAGES[$INDEX]} >/home/pi/dabing/install/setup.log
    if [[ $? > 0 ]]
    then
        printf "%*.s ${RED_COLOUR}FAIL${DEFAULT_COLOUR}\n" $(($PAD_LENGTH - ${#PIP_PACKAGES[$INDEX]}))
        PIP_STATE[$INDEX]=0
    else
        printf "%*.s ${GREEN_COLOUR}SUCCESS${DEFAULT_COLOUR}\n" $(($PAD_LENGTH - ${#PIP_PACKAGES[$INDEX]}))
        PIP_STATE[$INDEX]=1
    fi
done

# Setting up Postgres
~/dabing/install/postgresql.sh

# Welle.io
git clone https://github.com/SvajkaJ/welle.io ~/welle.io
~/dabing/install/welle.sh

# Patch pysnmp
~/dabing/install/patch/patch_pysnmp.sh

# Setting up systemd
~/dabing/install/systemd.sh

# Setting up nginx
~/dabing/install/nginx.sh

echo -e "${YELLOW_COLOUR}INSTALLATION FINISHED!${DEFAULT_COLOUR}\n"
echo -e "If you want to see the output of the installation process, check setup.log in ~/dabing/install directory!\n"

# ------------------------------------ #
# ---------- HARDWARE SETUP ---------- #
# ------------------------------------ #

echo -e "${YELLOW_COLOUR}LOOKING FOR CONNECTED HARDWARE!${DEFAULT_COLOUR}"
PAD_LENGTH=45
ALL_HARDWARE=1

# SDR is required!
printf "Required: ${SDR}"
cmd="$(lsusb | grep "${SDR}")"
if [[ ${#cmd} != 0 ]]
then
    printf "%*.s ${GREEN_COLOUR}CONNECTED${DEFAULT_COLOUR}\n" $(($PAD_LENGTH - ${#SDR}))
else
    printf "%*.s ${RED_COLOUR}DISCONNECTED${DEFAULT_COLOUR}\n" $(($PAD_LENGTH - ${#SDR}))
    ALL_HARDWARE=0
fi

if [[ ${ALL_HARDWARE} == 0 ]]
then
    echo -e "${RED_COLOUR}Connect required hardware!${DEFAULT_COLOUR}"
fi

# --------------------------------------------- #
# ---------- SETUP FINISHED - REBOOT ---------- #
# --------------------------------------------- #

echo -e "${YELLOW_COLOUR}Would you like to reboot now? [Y/N] ${DEFAULT_COLOUR}"
read -p "" REBOOT
if [[ ${REBOOT} == "Y" ]]
then
    echo -e "\n${YELLOW_COLOUR}REBOOTING!${DEFAULT_COLOUR}"
    sudo reboot now
else
    echo -e "\n${RED_COLOUR}REBOOT RASPBERRY BEFORE PROCEEDING!${DEFAULT_COLOUR}"
fi