#!/bin/zsh

python3 /home/john/practice/node/backend/updateCsv.py
cd /home/john/practice/node/; knexReset; echo "localhost:4545"; node app.js