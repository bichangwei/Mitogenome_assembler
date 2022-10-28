# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time: 2022/9/17 18:18
# @Author: Changwei Bi
# @Email: bichwei@163.com; bichwei@njfu.edu.cn
# @File: Get_mitogenome_from_assembly.py
 
'''
According to the input seed_ID, the extended loop information will be obtained
'''

import re
import argparse
import time
#import gzip

def get_all_connection_from_datafile():
    '''
    Function: The data in the file is decomposed to facilitate for later operation
    '''
    all_connections = []  # Stores information about the 5' end and 3' end of each ID  [{"68206 3'": "50193 5'"}, .....,{"92534 5'": "92436 3'"}]   all_connections
    simple_pairs = {}  # The complete ID of each contig and the corresponding shorthand form the dictionary as follows :{'1': 'contig00001',....., '92825': 'contig92825'}
    id_depth = {}  # Shorthand ID and sequencing depth for each contig
    for line in data_list:
        #Store information of each contig
        if re.match('[0-9]', line):
            temp_contig = line.strip().split()
            simple_id = re.sub('contig0*', '', temp_contig[1])
            simple_pairs[simple_id] = temp_contig[1]
            id_depth[simple_id] = temp_contig[3]
            pass

        #Find and store contig connections
        if re.match('C', line):
            connection = {}
            lid = ""
            lio = line.strip().split()
            contig_and_UTR1 = lio[1] + " " + lio[2]
            contig_and_UTR2 = lio[3] + " " + lio[4]  # Put the corresponding contig and edge number into the list
            connection[contig_and_UTR1] = contig_and_UTR2
            all_connections.append(connection)
    return simple_pairs, all_connections,id_depth


def seed_extend():
    '''
    dynamic_sampleIDs: a dynamic list, and the contigID of the UTR connection is added by loop.
    The initial element is the seed ID of the simplified version if seed='contig00002' dynamic_sampleIDs=['2']
    Carry on according to the seed sequence provided
    Contig with seed ID were connected by cycling
    ContigID stores the list
    Join proleptic_connection to a dictionary  proleptic_connection
    '''
    global dynamic_sampleIDs, simple_pairs,proleptic_connections
    for connection in all_connections:
        for left_contig, right_contig in connection.items():
            left_contig_id = left_contig.split()[0]
            left_contig_edge = left_contig.split()[1]
            right_contig_id = right_contig.split()[0]
            right_contig_edge = right_contig.split()[1]
            for sampleID in dynamic_sampleIDs:  # At first dynamic_sampleIDs had only the 4004 seed
                if int(left_contig_id) == int(sampleID):
                    proleptic_connection = {}
                    source = ""  # source :"contig*" + "edge"
                    source = left_contig_id + " " + left_contig_edge
                    target = ""  # target :"contig*" + "edge"
                    target = right_contig_id + " " + right_contig_edge
                    proleptic_connection[source] = target
                    proleptic_connections.append(proleptic_connection)
                    # Dynamic list proleptic_connections, the contig
                    # pairs generated in each cycle are stored in the list (the list composed of the dictionary proleptic_connection

                    if right_contig_id not in dynamic_sampleIDs:
                        dynamic_sampleIDs.append(right_contig_id)  # Dynamic list dynamic_sampleIDs, each cycle corresponding to

                        # the new contigID into the dynamic list, extend down
                        pass

                    pass
                elif int(right_contig_id) == int(sampleID):
                    proleptic_connection = {}
                    source_full = ""
                    source_full = right_contig_id + " " + right_contig_edge
                    target_full = ""
                    target_full = left_contig_id + " " + left_contig_edge
                    proleptic_connection[source_full] = target_full
                    proleptic_connections.append(proleptic_connection)
                    if left_contig_id not in dynamic_sampleIDs:
                        dynamic_sampleIDs.append(left_contig_id)

                        pass

                    pass
                pass
    return dynamic_sampleIDs, simple_pairs, proleptic_connections


def update_seed_extend():
    '''
    Automatically  updates to  seed_extend
    '''
    set1 = set()  #Set a set (non-duplicate) that stores contigs in all loops
    contig_connections= []  # The list stores contig connections
    n = 1
    while n != 0:
        seed_extend()
        for nl in proleptic_connections:
            for left, right in nl.items():
                r_temp_line = {}#The opposite of this contig_connection
                r_temp_line[right] = left
            t = tuple(nl.items())
            t1 = tuple(r_temp_line.items())
            if t not in set1 and t1 not in set1:
                set1.add(t)
                contig_connections.append(nl)
            pass
        if n != len(set1):
            n = len(set1)
        else:
            n = 0

    return contig_connections
if __name__ == '__main__':
    start_time = time.time()
    parser=argparse.ArgumentParser(description="According to the input seed_ID, the extended loop information is obtained")
    parser.add_argument("--ContigGraph","-c",help='454ContigGraph.txt: a file that can get all connections bewteen contigs.',type=str,required=False,default="454ContigGraph.txt")
    parser.add_argument("--AllContigs","-a",help='454AllContigs.fna: a file that can get all information of contigs.',type=str,required=False,default="454AllContigs.fna")
    parser.add_argument("--Output", "-o", help='Output file for visualizing in Bandage', type=str,required=False,default="Assembly_graph.gfa")
    parser.add_argument("--seeds","-s",help='SeedIDs for extending. Multiple parameters should be separated by Spaces. For example: 1 312 356',required=True,nargs='+')

    args=parser.parse_args()
    file_data_name=args.ContigGraph#Oiginal data file name
    file_data_fna_name=args.AllContigs
    file_result_name=args.Output#File name of the final result store
    with open(file_data_name, 'r') as fo:
        data_list = fo.readlines()
    print("Seeds extending......")
    # Result of get_all_connection_from_datafile
    simple_pairs = get_all_connection_from_datafile()[0]#{'1': 'contig00001',....., '92825': 'contig92825'}
    all_connections = get_all_connection_from_datafile()[1]  #  [{"68206 3'": "50193 5'"}, .....,{"92534 5'": "92436 3'"}]
    id_depth = get_all_connection_from_datafile()[2]  # Shorthand ID and sequencing depth for each contig
    proleptic_connections = []
    seed=[]
    seed = args.seeds  # seed_ID
    dynamic_sampleIDs = seed

    #Result of update_seed_extend
    contig_connections = update_seed_extend()  # The list stores contig connections
    for dynamic_sampleID in dynamic_sampleIDs:
        print("contig%s added"%(dynamic_sampleID))
    print("%d contigs are added"%(len(dynamic_sampleIDs)))
    seeds = set([])  # A collection used to store seeds

    f = open(file_result_name, 'w')

    for contig_connection in contig_connections:
        for left, right in contig_connection.items():
            seeds.add(simple_pairs[left.split()[0]])
            seeds.add(simple_pairs[right.split()[0]])
    #seeds = sorted(seeds)
    seeds=list(seeds)
    for i in range(0, len(seeds)):
        seeds[i] = re.sub('contig0*', '', seeds[i])
        seeds[i]=int(seeds[i])
    seeds=sorted(seeds)
    for i in range(0, len(seeds)):
        seeds[i] = str(seeds[i])
    #Enter the results into  file_result
    with gzip.open(file_data_fna_name, 'r') as fna:
        index_seeds = 0
        index_con = 0
        con = fna.readlines()
        #Output a sequence of seeds
        while index_seeds< len(seeds):
            if index_con >= len(con):
                break
            temp_list = con[index_con].split()
            temp_id = re.sub('>contig0*', '', temp_list[0])  # get_sample_id
            if re.match(seeds[ index_seeds], temp_id):
                f.write('S' + '\t')
                f.write(temp_id + '\t')
                temp_length = "".join(list(filter(str.isdigit, temp_list[1])))  #get contig_length
                index_con= index_con+ 1
                while index_con < len(con):
                    # input sequence
                    con[index_con].strip('\n')  # delete line break
                    f.write(con[index_con].strip('\n'))
                    index_con = index_con + 1
                    if index_con == len(con):
                        f.write('\t' + 'LN:i:' + temp_length + '\t')
                        temp_RC = str(int(temp_length) * float(id_depth[temp_id]))
                        f.write('RC:i:' + temp_RC + '\n')  ##
                        break
                    if (index_con < len(con)):
                        if (re.match('>contig0*', con[index_con])):
                            f.write('\t' + 'LN:i:' + temp_length + '\t')  ##1
                            temp_RC = str(int(temp_length) * float(id_depth[temp_id]))
                            f.write('RC:i:' + temp_RC + '\n')  ##
                            index_seeds=  index_seeds + 1
                            index_con = index_con - 1
                            break
            index_con = index_con + 1

        #Output connections between seeds
        for contig_connection in contig_connections:
            for left_contig, right_contig in contig_connection.items():
                f.write('L' + '\t' + left_contig.split()[0] + '\t')
                left_edge = left_contig.split()[1]
                right_edge = right_contig.split()[1]
                if left_contig.split()[1]!=right_contig.split()[1]:
                    if(left_contig.split()[1]=="3'"):
                        left_edge='+'
                        right_edge='+'
                    else:
                        left_edge='-'
                        right_edge='-'
                else:
                    if (left_contig.split()[1] == "3'"):
                        left_edge = '+'
                        right_edge = '-'
                    else:
                        left_edge= '-'
                        right_edge= '+'
                f.write(left_edge + '\t')
                f.write(right_contig.split()[0] + '\t')
                f.write(right_edge + '\t' + '0M' + '\n')
    f.close()
    end_time = time.time()
    print('Took %f second' % (end_time - start_time))

