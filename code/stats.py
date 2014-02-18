#!/usr/bin/python
"""This script can be used to analyze data in the 2012 Presidential Campaign,
available from ftp://ftp.fec.gov/FEC/2012/pas212.zip - data dictionary is at
http://www.fec.gov/finance/disclosure/metadata/DataDictionaryContributionstoCandidates.shtml
"""

import fileinput
import csv
import math

total = 0.0
dMin = 0.0
dMax = 0.0
dMean = 0.0
numDonors = 0
candID = {}
candidates = {}
donations = []
for row in csv.reader(fileinput.input(), delimiter='|'):
    donation = float(row[14])
    donorID = row[16]
    if donation < 0:
        donation = donation * -1
    if fileinput.isfirstline():
        dMin = donation
    total += donation
    if dMin >= donation:
        dMin = donation
    if dMax <= donation:
        dMax = donation
    donations.append(donation)
    if donorID not in candidates:
        candidates[donorID] = [donation]
    else:
        candidates[donorID].append(donation)
    numDonors += 1


dMean = total / numDonors
donations.sort()
dMedian = donations[int(math.floor(len(donations)/2))]
tmp = [pow(x-dMean,2) for x in donations]
stndDev = math.sqrt(sum(tmp)/len(tmp))

        ###
        # TODO: calculate other statistics here
        # You may need to store numbers in an array to access them together
        ##/

###
# TODO: aggregate any stored numbers here
#
##/

##### Print out the stats
print "Total: %s" % total
print "Minimum: %s" % dMin
print "Maximum: %s" % dMax
print "Mean: %s" % dMean
print "Median: %s" % dMedian
# square root can be calculated with N**0.5
print "Standard Deviation: %s" % stndDev

##### Comma separated list of unique candidate ID numbers
print "Candidates: %s" % candidates.keys()

def minmax_normalize(value):
    """Takes a donation amount and returns a normalized value between 0-1. The
    normilzation should use the min and max amounts from the full dataset"""
    ###
    # TODO: replace line below with the actual calculations
    norm = value
    ###/
    norm = norm/dMax
    return norm

##### Normalize some sample values
print "Min-max normalized values: %r" % map(minmax_normalize, [2500, 50, 250, 35, 8, 100, 19])

def z_score(value):
    "computes z-score for a donors total donation compared to the entire sample size"
    return (value-dMean)/stndDev

def candidate_stats(values):
    """
    schema
    candidates = { 'CANDIDATEID' : { 'Total':1 , 'Minimum':0, 'Maximum':1,
                                     'Mean':1, 'Median':1, 'Standard-Deviation':0,
                                     'Z-score':1 } 
                                     .... }
    """
    ret = {}
    for key in values.viewkeys():
        cdonations = values[key]
        cMean = sum(cdonations)/len(cdonations)
        cdonations.sort()
        cMedian = cdonations[int(math.floor(len(cdonations)/2))]
        tmp = [pow(x-dMean,2) for x in cdonations]
        stndDev = math.sqrt(sum(tmp)/len(tmp))
        ret[key] = { 'Total':sum(cdonations), 'Minimum':min(cdonations), 'Maximum':max(cdonations), 'Mean':cMean, 'Median':cMedian, 'Standard Deviation':stndDev, 'Z-score':z_score(sum(cdonations))}
    return ret

print "Candidate stats: %s" % candidate_stats(candidates)
