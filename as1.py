"""
2016253072 명수환(Myeong Suhwan)
"""

from math import ceil
from itertools import combinations
import time
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
        #print(len(transactions))
        #print(itemset)
        #time.sleep(10)
        
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
    """
	FILL UP HERE!
    Calculate support of an itemset by iterating over the frequent itemsets
    """
    return support_count


# This function generates a combination from the frequent itemsets of size (itemset_size - 1) and accepts joined itemsets if they share (itemset_size - 2) items
# param frequent_itemsets: The table of frequent itemsets discovered
# param itemset_size: The size of joined itemsets
# return: All valid joined itemsets
def generate_selectively_joined_itemsets(frequent_itemsets, itemset_size):
    # initial size - 2
    # print("joined - itemset size : ", itemset_size)  
    # Record seen_itemsets to prevent duplicates
    seen_itemsets = set() #?? * 봤던거 넣는거인듯 for duplicates #??????????????????????????????????????
    joined_itemsets = set()
    #! Now Working
    #print(frequent_itemsets[1][0])
    c = combinations(frequent_itemsets[itemset_size-1][0], itemset_size) # [1][0]
    #print(list(c))            
    for v in list(c):
        joined_itemsets.add(v)
    #print(joined_itemsets)
    
    """
	FILL UP HERE!
    Try all combinations of two itemsets from the table of frequent itemsets and join the pair if they share (itemset_size - 2) items
    Add each joined itemset to the list if it is not present in the list and discard it otherwise
    """
    return joined_itemsets # {('YEL027w', 'YNL271c'), ('YEL027w', 'YGL019w'), ('YGL019w', 'YNL271c')}


# This function checks all the subsets of selected itemsets whether they all are frequent or not and prunes the itemset if anyone of the subsets is not frequent
# param selected_itemsets: The itemsets which are needed to be checked
# param frequent_itemsets: The table of frequent itemsets discovered
# param itemset_size: The size of intended frequent itemsets
# return: The itemsets whose all subsets are frequent
def apply_apriori_pruning(selected_itemsets, frequent_itemsets, itemset_size):
    #! Now Working
    apriori_pruned_itemsets = set()
    #???
    #이전꺼를 확인해서,
    #selected(joined)에서 불가능한 조합이 있으면 pruning 해야함
    #pruning된 최종적인 itemsets를 반환
    
    # subset_count = len(list(selected_itemsets)[0]) # the number of element is the number of subset of size:(n-1) 

    # for super in selected_itemsets:
    #     count = 0
    #     super = set(super)
    #     for sub in join2:
    #         sub = set(sub)
    #         if sub.issubset(super):
    #             count +=1
                
    #         else:
    #             pass
    #     if(count < subset_count):
    #         print("Pruning : ", super)
    subset_count = len(list(selected_itemsets)[0]) # the number of element is the number of subset of size:(n-1)  or itemset_size+1?
    prun_list = list() #!
    for super in selected_itemsets:
        count = 0
        super = set(super)
        for sub in frequent_itemsets[itemset_size]:
            sub = set(sub)
            if sub.issubset(super):
                count +=1
                
            else:
                pass
        if(count < subset_count): #n-1인 부분집합 개수만큼 count가 있어야 Pruning되지 않는다.
            #print(itemset_size)
            #print(subset_count)
            #?print("Pruning : ", super)
            prun_list.append(tuple(super))
            #print(type(super))
            #// ! TODO : Pruning remove 인자로 튜플을 던질 수 있나..
            #selected_itemsets.remove(super)
    #print("pruning list")
    #print(prun_list)
    
    try:
        prun_set = set(prun_list[0])
        #print(prun_set)
        #print(selected_itemsets)
        prun_tup = tuple()
        for v in selected_itemsets:
            
            if prun_set == set(v):
                
                prun_tup += v
                #selected_itemsets.remove(v)

        #print(prun_tup)
        selected_itemsets.remove(prun_tup)
    except:
        pass
    print("finished pruning")
    print(selected_itemsets)
                

    """
    FILL UP HERE!
	Add each itemset to the list if all of its subsets are frequent and discard it otherwise
    """
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
    frequent_itemsets[itemset_size] = list()
    frequent_itemsets[itemset_size].append(frozenset())
    #frozenset -> not mutable
    # Frequent itemsets of size 1
    itemset_size += 1
    frequent_itemsets[itemset_size] = list()
    #print(items)
#? ******************************************************************
    support_itemsets = dict()

    for item in items: # * Size -1 item
        count = support(transactions, item)
        
        
        if count >= min_sup:
            # print("ITEM : ", item)
            # print("count : ", count)
            support_itemsets[item] = count
            frequent_itemsets[itemset_size].append(support_itemsets)
        
    print("-------------------")
    #print(frequent_itemsets[1][0]['YFL014w'])
    

    """
    FILL UP HERE!
    Find all frequent itemsets of size-1 and add them to the list
    size:1 ex) {YNL166c}
    and have to get Support value of size-1 - done but didn't store that support value
    and maybe eliminate those things less than min_sup - done
    """
#? ******************************************************************
    # Frequent itemsets of greater size
    itemset_size += 1 #now item size : 2
    #print(itemset_size)
    
    while frequent_itemsets[itemset_size - 1]: # While L_k is not empty
        frequent_itemsets[itemset_size] = list() # size-2
        #print(frequent_itemsets)
        candidate_itemsets = generate_candidate_itemsets(frequent_itemsets, itemset_size) # C_k
        
        pruned_itemset = set()
        """
        FILL UP HERE!
		Prune the candidate itemset if its support is less than minimum support
        pruned_itemset을 이용해 해당 안되는거 제거
        """
        frequent_itemsets[itemset_size] = pruned_itemset
        itemset_size += 1 # k <- k+1
        print("done")
        print(itemset_size) #? 왜 한번만도는거같지
    return frequent_itemsets


# This function writes all frequent itemsets along with their support to the output file with the given filename
# param filename: The name for the output file
# param frequent_itemsets_table: The dictionary which contains all frequent itemsets
# param transactions: The transactions from which the frequent itemsets are found
# return: void
def output_to_file(filename, frequent_itemsets_table, transactions):
    file = open(filename, 'w')
    for itemset_size in frequent_itemsets_table:
    
        # Do not print frequent itemsets of size 0 or 1
        if itemset_size == 0:
            continue
        if itemset_size == 1:
            continue
        
        # Print frequent itemsets of size 2 or larger 
        for freq_itemset in frequent_itemsets_table[itemset_size]:
            support_percent = (support(transactions, freq_itemset) / len(transactions)) * 100
            file.write('{0} {1:.2f}% support\n'.format(freq_itemset, support_percent))
    file.close()


# The main function
def main():
    input_filename = 'assignment1_input.txt'
    output_filename = 'assignment1_output.txt'
    cellular_functions, genes_set = get_input_data(input_filename)
    #print(len(cellular_functions)) #216
    
    min_sup = ceil(MIN_SUPPORT * len(cellular_functions)) # min_sup 8
    print(min_sup)
    
    frequent_itemsets_table = generate_all_frequent_itemsets(cellular_functions, genes_set, min_sup)
    output_to_file(output_filename, frequent_itemsets_table, cellular_functions)


if __name__ == '__main__':
    main()