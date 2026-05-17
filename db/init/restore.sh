#!/bin/bash
set -e

pg_restore \
  -U user \
  -d mydb \
  /docker-entrypoint-initdb.d/mydb.dump
