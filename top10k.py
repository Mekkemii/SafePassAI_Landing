def load_common_passwords():
    with open("10k-most-common.txt", "r", encoding="utf-8") as f:
        return set(line.strip() for line in f)

COMMON_PASSWORDS = load_common_passwords()

def is_common_password(password):
    return password in COMMON_PASSWORDS
