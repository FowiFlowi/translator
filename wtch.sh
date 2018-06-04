#!/bin/bash

while true; do
  sleep 0.01
  ./translator.py -p input --lexer --syntaxer --generator
  inotifywait -qq -r -e modify .;
  echo '---'
done
