import base64, string
import tarfile, os, sys

#### info ####
wigner_key = "amiraliliya"
tar_archive_filename = "code"
#### info ####

####################### wigner.py #######################
def convert_key(string, key):
    return ((len(string) // len(key)) * key) + key[:(len(string) % len(key))]

def xor_encode(a, key):
    return chr(ord(a) ^ ord(key))

def xor_decode(out, key):
    a1 = ord(key)
    b1 = 0
    n = ord(out)
    t = 0
    while n > 0 or a1 > 0:
        if (n & 1 and (not (a1 & 1))) or (not (n & 1) and a1 & 1):
            b1 += 1 << t

        n >>= 1
        a1 >>= 1
        t += 1

    return chr(b1)

table_chrs = string.ascii_letters + string.digits
b64_chrs = "=+/"

def encode(string, key):
    my_key = convert_key(string, key)

    output_string = ""
    for sch, kch in zip(string, my_key):
        output_string += xor_encode(sch, kch)
    string = output_string

    string = base64.b64encode(string.encode()).decode()
    my_key = convert_key(string, key)
    output_string = ""
    bi = 0
    for sch, kch in zip(string, my_key):
        if sch in table_chrs:
            output_string += table_chrs[(table_chrs.index(sch) + table_chrs.index(kch) + len(table_chrs)) % len(table_chrs)]
        elif sch in b64_chrs:
            output_string += b64_chrs[(b64_chrs.index(sch) + (bi + 1) + len(b64_chrs)) % len(b64_chrs)]
            bi += 1
            bi %= (len(b64_chrs) - 1)
        else:
            output_string += sch

    return output_string

def decode(string, key):
    my_key = convert_key(string, key)

    output_string = ""
    bi = 0
    for sch, kch in zip(string, my_key):
        if sch in table_chrs:
            output_string += table_chrs[(table_chrs.index(sch) - table_chrs.index(kch) + len(table_chrs)) % len(table_chrs)]
        elif sch in b64_chrs:
            output_string += b64_chrs[(b64_chrs.index(sch) - (bi + 1) + len(b64_chrs)) % len(b64_chrs)]
            bi += 1
            bi %= (len(b64_chrs) - 1)
        else:
            output_string += sch
    output_string = base64.b64decode(output_string.encode()).decode()

    string = output_string
    my_key = convert_key(string, key)
    output_string = ""
    for sch, kch in zip(string, my_key):
        output_string += xor_decode(sch, kch)

    return output_string

####################### wigner.py #######################


####################### encrypt.py #######################
def encrypt_cypher(string):

    with open(tar_archive_filename, "w", encoding="utf-8") as file:
        file.write(string)

    with tarfile.open("encrypted.tar.gz", "w:gz") as file:
        file.add(tar_archive_filename)

    with open("encrypted.tar.gz", "rb") as file:
        out = file.read()
    os.remove(tar_archive_filename)
    os.remove("encrypted.tar.gz")

    return out

def encrypt(string):
    string = encrypt_cypher(string)

    cypher = base64.b64encode(string).decode()
    my_key = convert_key(cypher, wigner_key)
    cypher = "".join([xor_encode(a, key) for a, key in zip(cypher, my_key)])
    cypher = encode(cypher, wigner_key)

    return cypher

####################### encrypt.py #######################


####################### decrypt.py #######################
def decrypt_cypher(bin_string):
    with open("encrypted.tar.gz", "wb") as file:
        file.write(bin_string)

    with tarfile.open("encrypted.tar.gz") as file:
        
        import os
        
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(file)

    with open(tar_archive_filename, encoding="utf-8") as file:
        out = cypher = file.read()
    os.remove(tar_archive_filename)
    os.remove("encrypted.tar.gz")

    return out

def decrypt(cypher):
    plain = decode(cypher, wigner_key)
    my_key = convert_key(plain, wigner_key)
    plain = "".join([xor_decode(a, key) for a, key in zip(plain, my_key)])
    plain = base64.b64decode(plain.encode())
    plain = decrypt_cypher(plain)

    return plain
####################### decrypt.py #######################

usage = f"""wigner encryption system

USAGE
    python {os.path.basename(__file__)} -e | --encrypt <string>
    python {os.path.basename(__file__)} -d | --decrypt <string>
"""

if __name__ == "__main__":
    if len(sys.argv) == 1: print(usage)
    elif "-h" in sys.argv[1] or "--help" in sys.argv[1]: print(usage)
    else:
        try:
            option = sys.argv[1]
            string = sys.argv[2]

            if option == "-e" or option == "--encrypt":
                print(encrypt(string))

            elif option == "-d" or option == "--decrypt":
                print(decrypt(string))

        except:
            print("incorrect usage of program")
            print(usage)
            sys.exit(1)
