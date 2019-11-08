#!/bin/bash
docker image build -t metroenergy/meep-api:0.1.1 .
docker image push metroenergy/meep-api:0.1.1
