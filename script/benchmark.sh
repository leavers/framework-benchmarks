#!/bin/bash

set -e

echo ----- /hello -----

echo -- 1st round \(wrk -t10 -c1000 -d30s http://localhost:8080/async/hello\) --
wrk -t10 -c1000 -d30s http://localhost:8080/hello
echo -- 1st round ended --
sleep 10

echo -- 2st round \(wrk -t10 -c1000 -d30s http://localhost:8080/async/hello\) --
wrk -t10 -c1000 -d30s http://localhost:8080/hello
echo -- 2nd round ended --
sleep 10

echo -- 3rd round \(wrk -t10 -c1000 -d30s http://localhost:8080/async/hello\) --
wrk -t10 -c1000 -d30s http://localhost:8080/hello
echo -- 3rd round ended --

echo ----- /hello ended -----
echo
