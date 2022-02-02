#!/bin/bash
#
# CPort - a new port manager for Calmira Linux
# Copyright (C) 2021, 2022 Michail Krasnov <linuxoid85@gmail.com>
#
# ports.sh
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Project Page: http://github.com/Linuxoid85/cport
# Michail Krasnov (aka Linuxoid85) linuxoid85@gmail.com
#

set -Eeuo

function g_msg() {
    dialog --backtitle " cport " $@
}

function g_dialog() {
    g_msg --title " Dialog " --yesno "Continue?" 0 0

    case "$?" in
        0)     echo "OK"
        1|255) echo "Aborted!"; exit 1
        *)     echo "Uknown answer..."; exit 1
    esac
}

function dialog() {
    echo -n "> Continue? (y/n) "
    read run

    if [[ $run -eq "y" ]]; then
        echo "OK"
    else
        echo "Aborted!"
        exit 1
    fi
}

# Function for logging port instruction scripts
# MSG Format:
#  [ TIME ] - level - message
# USAGE:
# log_msg $LEVEL $MESSAGE
function log_msg() {
    LOG="/var/log/cport_ports.log"
    msg="[ ${time} ] - $1 - $2"

    echo $msg > $LOG
}