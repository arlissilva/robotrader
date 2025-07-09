#!/bin/bash
echo "Escolha onde rodar:"
echo "1 - Localhost"
echo "2 - Docker"
read opt
if [ "$opt" = "1" ]; then
  python3 robot_trader/main.py
else
  docker compose up --build
fi