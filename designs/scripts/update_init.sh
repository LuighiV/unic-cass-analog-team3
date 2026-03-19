#! /bin/bash

# WARNING!!
# Be cautious when calling this file, should be run inside docker environment
# Replaces the .bashrc file from the container with a customized one from the
# repository

cp ~/.bashrc ~/.bashrc.bk.$(date +%s)
cp ~/designs/.config/.bashrc ~/.bashrc
