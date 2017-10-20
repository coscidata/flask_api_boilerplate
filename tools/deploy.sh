#!/bin/bash

remote=${1-origin}
branch=${2-master}

ssh user@ip << EOF
  git --work-tree=/data/app --git-dir=/data/app/.git fetch --all --prune
  git --work-tree=/data/app --git-dir=/data/app/.git reset --hard $remote/$branch
  sudo systemctl restart app
EOF
