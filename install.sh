#!/usr/bin/env bash

sudo cp voteService /etc/init.d/voteService
sudo chmod +x /etc/init.d/voteService
sudo update-rc.d voteService defaults
