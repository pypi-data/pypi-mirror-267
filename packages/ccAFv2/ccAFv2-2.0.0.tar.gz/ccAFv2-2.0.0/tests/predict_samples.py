##########################################################
## OncoMerge:  predict_samples.py                       ##
##  ______     ______     __  __                        ##
## /\  __ \   /\  ___\   /\ \/\ \                       ##
## \ \  __ \  \ \___  \  \ \ \_\ \                      ##
##  \ \_\ \_\  \/\_____\  \ \_____\                     ##
##   \/_/\/_/   \/_____/   \/_____/                     ##
## @Developed by: Plaisier Lab                          ##
##   (https://plaisierlab.engineering.asu.edu/)         ##
##   Arizona State University                           ##
##   242 ISTB1, 550 E Orange St                         ##
##   Tempe, AZ  85281                                   ##
## @Author:  Chris Plaisier, Samantha O'Connor          ##
## @License:  GNU GPLv3                                 ##
##                                                      ##
## If this program is used in your analysis please      ##
## mention who built it. Thanks. :-)                    ##
##########################################################

##########################################
## Load Python packages for classifiers ##
##########################################

# General
import scanpy as sc
import ccAFv2


#####################
## Test prediction ##
#####################

U5hNSC = sc.read_h5ad('../data/U5_normalized_ensembl_all_genes.h5ad')
U5hNSC_labels = ccAFv2.predict_labels(U5hNSC, species='human', gene_id='ensembl')

PCW8 = sc.read_h5ad('../data/W8-1_normalized_ensembl.h5ad')
PCW8_labels = ccAFv2.predict_labels(PCW8, species='human', gene_id='ensembl')

