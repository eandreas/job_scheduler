#!/bin/bash


job_file=/home/eandreas/job_scheduler/config.dat

job_year=$(cat ${job_file} | awk '{print $0}')
echo $job_year
