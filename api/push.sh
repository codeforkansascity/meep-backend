#!/bin/bash
docker image build -t metroenergy/meep-api:0.1.0 .
docker image push metroenergy/meep-api:0.1.0
