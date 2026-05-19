#!/bin/bash
set -e

pg_restore \
  -U user \
  -d postgres \
  /docker-entrypoint-initdb.d/mydb.dump
