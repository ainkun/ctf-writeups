#!/bin/bash

file=$(cat enc_flag)


file=$(echo $file | base64 -d | tr -d '\n')


echo $file