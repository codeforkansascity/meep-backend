#!/bin/bash
docker exec -it meep-backend_api_1 pytest ../tests/$1
