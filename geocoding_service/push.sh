#!/bin/bash
docker image build -t metroenergy/meep-geocode:0.0.3 .
docker image push metroenergy/meep-geocode:0.0.3
