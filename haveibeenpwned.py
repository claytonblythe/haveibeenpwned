import hashlib
import requests

def get_hash_value(string_to_hash):
    hash_object = hashlib.sha1(str(string_to_hash).encode('utf-8'))
    return hash_object.hexdigest().upper()


def get_hash_prefix_suffix(hash_value):
    return hash_value[:5], hash_value[5:]


def get_hash_suffix_counts_from_api(hash_prefix):
    base_url = "https://api.pwnedpasswords.com/range/"
    r = requests.get(base_url+hash_prefix)
    return r.text.split()


def find_match( hash_suffix, suffix_counts):
    for entry in suffix_counts:
        suffix, count = entry.split(":")
        if suffix == hash_suffix:
            return True, count
    else:
        return False, 0


def main():
    string_password = input("Enter your password: ")
    hash_value = get_hash_value(string_password)
    hash_prefix, hash_suffix = get_hash_prefix_suffix(hash_value)
    suffix_counts = get_hash_suffix_counts_from_api(hash_prefix)
    found, count = find_match(hash_suffix, suffix_counts)
    if found:
        print(f"{string_password} was found")
        print(f"Hash: {hash_value}, {count} occurences")
    else:
        print(f"{string_password} was not found")


if __name__ == "__main__":
    main()