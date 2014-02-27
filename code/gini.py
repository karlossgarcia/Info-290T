#!/usr/bin/python
"""Script can be used to calculate the Gini Index of a column in a CSV file.

Classes are strings."""

import fileinput
import csv
import collections

(
    CMTE_ID, AMNDT_IND, RPT_TP, TRANSACTION_PGI, IMAGE_NUM, TRANSACTION_TP,
    ENTITY_TP, NAME, CITY, STATE, ZIP_CODE, EMPLOYER, OCCUPATION,
    TRANSACTION_DT, TRANSACTION_AMT, OTHER_ID, CAND_ID, TRAN_ID, FILE_NUM,
    MEMO_CD, MEMO_TEXT, SUB_ID
) = range(22)

CANDIDATES = {
    'P80003338': 'Obama',
    'P80003353': 'Romney',
}

data = {}

############### Set up variables
# TODO: declare datastructures

############### Read through files
for row in csv.reader(fileinput.input(), delimiter='|'):
    candidate_id = row[CAND_ID]
    if candidate_id not in CANDIDATES:
        continue

    candidate_name = CANDIDATES[candidate_id]
    zip_code = row[ZIP_CODE][:5]
    ###
    # TODO: save information to calculate Gini Index
    ##/
    if zip_code not in data:
        data[zip_code] = [0,0]
        if candidate_name == 'Obama':
            data[zip_code][0]+=1
        else:
            data[zip_code][1]+=1
    elif candidate_name == 'Obama':
        data[zip_code][0]+=1
    else:
        data[zip_code][1]+=1

obama_total = 0
romney_total = 0

for elem in data.values():
    obama_total += elem[0]
    romney_total += elem[1]

total_num = obama_total + romney_total


###
# TODO: calculate the values below:
gini = 0  # current Gini Index using candidate name as the class
gini = 1 - pow(obama_total/float(total_num),2) - pow(romney_total/float(total_num),2)
split_gini = 0  # weighted average of the Gini Indexes using candidate names, split up by zip code
##/
for key in data.keys():
    zip_obama = data[key][0]
    zip_romney = data[key][1]
    total_zip = zip_obama + zip_romney
    zip_gini = 1 - pow(zip_obama/float(total_zip),2) - pow(zip_romney/float(total_zip),2)
    split_gini += zip_gini * (total_zip/float(total_num))

print "Gini Index: %s" % gini
print "Gini Index after split: %s" % split_gini
