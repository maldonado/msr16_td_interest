#!/bin/bash
LIST=(ant jmeter camel gerrit hadoop log4j tomcat)
OUT=all_automated_classification.csv

COUNT=0
for item in ${LIST[@]}; do
    echo $item
    if [ ${COUNT} -eq 0 ]; then
        # for header
        gsed -n 1p ${item}_automated_classification.csv > ${OUT}
        gsed -i -e "s/^/project,/" ${OUT} 
    fi

    gsed -e "1d" ${item}_automated_classification.csv | gsed -e "s/^/${item},/" >> ${OUT}
    COUNT=$((${COUNT} + 1))
done