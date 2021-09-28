"""
2016253072 명수환(Myeong Suhwan)
"""

from math import ceil, comb
from itertools import combinations

MIN_SUPPORT = 0.035

# This function reads a file under filename and extracts all transactions and a set of distinct items
# param filename: The name of the input file (should provide path if necessary)
# return: A dictionary of transactions and a set of distinct items
def get_input_data(filename): #return cellular_functions, genes_set
    input_file = open(filename, 'r')
    transactions = dict()
    itemset = set()
    for line in input_file:
        splitted = line.split()
        trans_id = splitted[0]
        trans_items = splitted[1:]
        transactions[trans_id] = trans_items
        itemset.update(trans_items)
        
        
    return transactions, itemset


# This function calculates support of the itemset from transactions
# param transactions: All transactions in a dictionary
# param itemset: The itemset to calculate support
# return: The support count of the itemset
def support(transactions, itemset):
    support_count = 0
    # itemset means like {1,2,3,4} 
        
    for v in transactions:
        if itemset in transactions[v]:
            support_count += 1
        
        if type(itemset) is tuple:
            flag = True
            for i in range(len(itemset)):
                if itemset[i] not in transactions[v]:
                    flag = False
            if flag is True:
                support_count += 1

    return support_count


# This function generates a combination from the frequent itemsets of size (itemset_size - 1) and accepts joined itemsets if they share (itemset_size - 2) items
# param frequent_itemsets: The table of frequent itemsets discovered
# param itemset_size: The size of joined itemsets
# return: All valid joined itemsets
def generate_selectively_joined_itemsets(frequent_itemsets, itemset_size):    
    #seen_itemsets = set() # Didn't use this set
    joined_itemsets = set()

    print(frequent_itemsets)    
    index = itemset_size - 1 # init value : index = 1
    print("itemset size : ",itemset_size)
    if itemset_size == 2:
        c = combinations(frequent_itemsets[index][0], 2) # using size-1, make size-2
        list_comb = list(c)
        print(list_comb)
        for v in list_comb:
            joined_itemsets.add(v)
    elif itemset_size > 2:
        
        
        #print("index : ", index)
        c3 = combinations(frequent_itemsets[index][0], 2)
        l3 = list(c3)
        #print(l3)
        t3 = tuple(l3)
        for i in range(len(l3)):
            test = t3[i][0] + t3[i][1]
            tmp_set = tuple(set(test))
            if(len(tmp_set) == itemset_size):
                joined_itemsets.add(tmp_set)
            else:
                #!print(tmp_set," is deleted.")
                pass
    

    tmp_joined_itemsets = list(joined_itemsets)

    for v in tmp_joined_itemsets: # * To remove the items duplicated, Use sort()
        tmp_v = list(v)
        print(tmp_v)
        joined_itemsets.remove(tuple(tmp_v))
        tmp_v.sort()
        print(tmp_v)
        joined_itemsets.add(tuple(tmp_v))
    
    print("[Joined itemsets]")
    print(joined_itemsets)

    return joined_itemsets # {('YEL027w', 'YNL271c'), ('YEL027w', 'YGL019w'), ('YGL019w', 'YNL271c')}


# This function checks all the subsets of selected itemsets whether they all are frequent or not and prunes the itemset if anyone of the subsets is not frequent
# param selected_itemsets: The itemsets which are needed to be checked
# param frequent_itemsets: The table of frequent itemsets discovered
# param itemset_size: The size of intended frequent itemsets
# return: The itemsets whose all subsets are frequent
def apply_apriori_pruning(selected_itemsets, frequent_itemsets, itemset_size):
    
    apriori_pruned_itemsets = set()
    
    selected_list = list(selected_itemsets)
    if not selected_itemsets:
        return None
    subset_count = len(selected_list[0]) # the number of element is the number of subset of size:(n-1)
    print("subset count : ",subset_count)
    prun_list = list()
    for super in selected_itemsets:
        count = 0
        super = set(super)
        
        
        for sub in frequent_itemsets[itemset_size-1]:
            
            
            #print("\n sub: ",sub,"super: ",super)
            for sub_element in sub:
                
                sub_element = set(sub_element)
                if sub_element.issubset(super):
                    print(sub_element," is subset of ", super)
                    count += 1
                else:
                    pass
            
            print("\n")
            
        if(count < subset_count): #n-1인 부분집합 개수만큼 count가 있어야 Pruning되지 않는다.
            #print("count : ",count , " subset_count : ", subset_count)
            #print("Pruning : ", super)
            prun_list.append(tuple(super))
        print("count : ",count , " subset_count : ", subset_count)
            
    try:
        prun_set = set(prun_list[0])
        prun_tup = tuple()
        for v in selected_itemsets:
            if prun_set == set(v):
                prun_tup += v
                
        selected_itemsets.remove(prun_tup)
    except:
        pass
    
    apriori_pruned_itemsets = selected_itemsets
    return apriori_pruned_itemsets


# This function generates candidate itemsets of size (itemset_size) by selective joining and apriori pruning
# param frequent_itemsets: The table of frequent itemsets discovered
# param itemset_size: The size of intended frequent itemsets
# return: candidate itemsets formed by selective joining and apriori pruning
def generate_candidate_itemsets(frequent_itemsets, itemset_size):
    joined_itemsets = generate_selectively_joined_itemsets(frequent_itemsets, itemset_size) # * joined itemset
    candidate_itemsets = apply_apriori_pruning(joined_itemsets, frequent_itemsets, itemset_size) # * get candidate itemsets after pruning

    return candidate_itemsets


# This function generates a table of itemsets with all frequent items from transactions based on a given minimum support
# param transactions: The transactions based upon which support is calculated
# param items: The unique set of items present in the transaction
# param min_sup: The minimum support to find frequent itemsets
# return: The table of all frequent itemsets of different sizes
def generate_all_frequent_itemsets(transactions, items, min_sup):
    
    frequent_itemsets = dict()
    itemset_size = 0
    frequent_itemsets[itemset_size] = list() # index 0
    frequent_itemsets[itemset_size].append(frozenset())
    
    itemset_size += 1
    frequent_itemsets[itemset_size] = list() # index 1
    
#? ******************************************************************
    support_itemsets = dict()
    
    for item in items: # * Size -1 item
        
        count = support(transactions, item)
        
        
        if count >= min_sup:
            # print("ITEM : ", item)
            # print("count : ", count)
            support_itemsets[item] = count
            
            
    frequent_itemsets[itemset_size].append(support_itemsets)    

    # Frequent itemsets of greater size
    itemset_size += 1 #now item size : 2
    #print(itemset_size)
    # * Generate All Frequent Itemsets(L2, L3 ...)
    while frequent_itemsets[itemset_size - 1]: # While L_k is not empty
        print("start")
        frequent_itemsets[itemset_size] = list() # size-2
        #print(frequent_itemsets)
        
        candidate_itemsets = generate_candidate_itemsets(frequent_itemsets, itemset_size) # C_k
        if not candidate_itemsets:
            break
        print("Generated Candidate Itemsets . . . ")
        #print(candidate_itemsets)
        
        support_itemsets = dict()
        
        #print("cand_len : ", len(candidate_itemsets))
        i=1
        for item in candidate_itemsets: # * Size - n item #! Getting support of candidate_itemsets
            
            #print("Progress : {:.5f}%".format(i*100/len(candidate_itemsets)))
            i += 1
            count = support(transactions, item)
            support_itemsets[item] = count
            
        frequent_itemsets[itemset_size].append(support_itemsets)    
        
        #print(frequent_itemsets)
        
        #pruned_itemset = set() # ! 기존에 있던 코드
        pruned_itemset = dict() # ? dict여도 while을 끝낼 수 있음.
        for v in support_itemsets:
            #print(support_itemsets[v])
            if support_itemsets[v] < min_sup:
                #pruned_itemset.add(v)
                pruned_itemset[v] = support_itemsets[v] # Change: Pruned set을 삭제할 것들의 set으로 만듦

        #frequent_itemsets[itemset_size] = list()
        #print(frequent_itemsets)
        #print(pruned_itemset)

        for v in pruned_itemset:
            del frequent_itemsets[itemset_size][0][v]
            #!print(v,"is pruned.")
        #frequent_itemsets[itemset_size] = pruned_itemset
        itemset_size += 1 # k <- k+1
        
        
    return frequent_itemsets


# This function writes all frequent itemsets along with their support to the output file with the given filename
# param filename: The name for the output file
# param frequent_itemsets_table: The dictionary which contains all frequent itemsets
# param transactions: The transactions from which the frequent itemsets are found
# return: void
def output_to_file(filename, frequent_itemsets_table, transactions):
    file = open(filename, 'w')
    print("======================================================================")
    
    for itemset_size in frequent_itemsets_table:
    
        # Do not print frequent itemsets of size 0 or 1
        if itemset_size == 0: #frozenset
            continue
        if itemset_size == 1: #size-1
            continue
        
        # Print frequent itemsets of size 2 or larger 
        for freq_itemset in frequent_itemsets_table[itemset_size]:
            #print(freq_itemset)
            for item in freq_itemset:
                #support_percent = (support(transactions, freq_itemset) / len(transactions)) * 100
                support_percent = (support(transactions, item) / len(transactions)) * 100
                print(item,'{:.2f}%'.format(support_percent))
                #file.write('{0} {1:.2f}% support\n'.format(freq_itemset, support_percent))
                file.write('{0} {1:.2f}% support\n'.format(item, support_percent))
    file.close()
    print("Finished to print to output file : ", filename)


# The main function
def main():
    input_filename = 'assignment1_input.txt'
    #input_filename = 'test_input.txt'
    output_filename = 'assignment1_output.txt'
    cellular_functions, genes_set = get_input_data(input_filename)
    #print("gene sets length: ",len(genes_set))
    
    min_sup = ceil(MIN_SUPPORT * len(cellular_functions)) # min_sup 8
    
    frequent_itemsets_table = generate_all_frequent_itemsets(cellular_functions, genes_set, min_sup)
    print(frequent_itemsets_table)
    output_to_file(output_filename, frequent_itemsets_table, cellular_functions)


if __name__ == '__main__':
    main()