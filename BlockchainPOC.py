import hashlib
import csv
def is_constraint_met(strng):
    if strng[0] == "0" and strng[1] == "0" and len(strng) == 64:
        return True
    else:
        return False

def is_nonce_in_list_and_update(number,csvfile="nonce.csv"):
    switch = None
    with open(csvfile, "ab+") as csvfile:
        buffer = csv.reader(csvfile)
        for row in buffer:
            if int(row[0].strip()) == number:
                return True
        wr = csv.writer(csvfile, dialect="excel")
        wr.writerow([number])
        return False

def hash_of_block(block_no,number,content,previous_hash):
    return hashlib.sha256(str(block_no)+str(number)+str(content)+str(previous_hash)).hexdigest()

def generate_legal_nonce(block_no,content,previous_hash):
    number_candidate = 0
    if is_constraint_met(previous_hash):    
        while True:
            candidate_hash = hash_of_block(block_no,number_candidate,content,previous_hash)
            if is_constraint_met(candidate_hash):
                if is_nonce_in_list_and_update(number_candidate) == False:
                    return number_candidate, candidate_hash
            number_candidate += 1
    else:
        raise Exception("Invalid previous hash")
        
# csv file predstavlja lanac

def initiate_chain(filename="chain.csv"):
    seed_line = ["1","133", "init", "00000000000000001e8d6829a8a21adc5d38d0a473b144b6765798e61f98bd1d", "004b034284d53df28a17460a4e53ada4db72b7fd2fe4a0f6289c28997d603582"]
    with open(filename, "ab") as filename:
        wr = csv.writer(filename, dialect="excel")
        wr.writerow(seed_line)
    
def get_previous_block_no_and_hash(csv_chain_file="chain.csv"):
    with open(csv_chain_file) as csvfile:
        listacsv=[]    
        buffer = csv.reader(csvfile)
        for row in buffer:
            listacsv.append(row)
    lastline = listacsv[-1]
    #print lastline
    return (lastline[0],lastline[4])
    
def write_legal_block_to_chain(content,chainfile="chain.csv"):#treba dodati if_constraint_met, jer ce ovo ici i kod dodavanja na peerove
    pre_block_no, prev_hash = get_previous_block_no_and_hash(chainfile)
    curr_nonce, curr_hash = generate_legal_nonce(pre_block_no + 1, content, prev_hash)
    to_file = [str(pre_block_no + 1),str(curr_nonce),str(content), str(prev_hash), str(curr_hash)]
    with open(chainfile, "ab") as outfile:
        wr = csv.writer(outfile, dialect="excel")
        wr.writerow(to_file)

def verify_chain(chainfile="chain.csv"):
    with open(chainfile) as csvfile:   
        buffer = csv.reader(csvfile)
        counter = 0
        last_row_curr_hash = ""
        for row in buffer:
            if counter>0:
                if is_constraint_met(row[3])==False or is_constraint_met(row[4]) == False:
                    return False
                if counter>1:
                    if row[3]!=last_row_curr_hash:
                        return False
                last_row_curr_hash = row[4]
            counter += 1
    return True
    

   
## POKRETANJE
# Prvi put se pokrece s         
#
# initiate_chain()
#
# koji stvara prvu liniju. Nakon toga se dodaje sadrzaj u obliku stringa s     
#
# write_legal_block_to_chain("trololo")
#
# Ovo generira legalni clan lanca sa sadrzajem trololo. Lanac se nalazi u chain.csv. Lanac (csv file) je moguce veificirati s print verify_chain("chain.csv")
# Legalnost cijelog lanca se verificira tako da se usporede s peerovima (dovoljno je usporediti samo zadnji hash u lancu i oni kojih ima najvise dobivaju), ali to je na todo listi


##TODO
#def propagate_to_peers:
#def verify_across_peers:









