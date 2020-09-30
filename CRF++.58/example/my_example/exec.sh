#!/bin/sh
../../crf_learn -c 10.0 template train.data model
../../crf_test  -v1 -m model test.data

rm -f model
