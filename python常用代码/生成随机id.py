import hashlib

def stable_hash(input_str):
    sha256 = hashlib.sha256()
    sha256.update(input_str.encode('utf-8'))
    return sha256.hexdigest()

id = stable_hash("光照杧果是喜温好光果树，在光照充足的地区或年份，花芽分化期早，有利于授粉受精和果实生长发育")
print(id)
if id == '27721e76412dc3f5206fc40cecf61afb7e150eb28c6386a37b34377ba39e72c9':
    print("true")
else:
    print("false")