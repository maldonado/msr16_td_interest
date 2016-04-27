#!/bin/bash
LIST=(ant jmeter)
OUT=all_automated_classification.csv

COUNT=0
for item in ${LIST[@]}; do
    echo $item
    if [ ${COUNT} -eq 0 ]; then
        # for header
        sed -n 1p ${item}_automated_classification.csv > ${OUT}
        sed -i -e "s/^/project,/" ${OUT}
    fi

    sed -e "1d" ${item}_automated_classification.csv | sed -e "s/^/${item},/" >> ${OUT}
    COUNT=$((${COUNT} + 1))
done