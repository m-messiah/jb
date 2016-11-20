#!/bin/bash

ab -c 100 -n 20000 -T 'application/x-www-form-urlencoded' -p test  http://shortener.localdomain/
