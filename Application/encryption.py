# Encryption
# Encrypt Rail Fence
def encrypt(text, rails=3):
    encrypted_text = ""
    for i in range(rails):
        encrypted_text += text[i::rails]
    return encrypted_text

# Decrypt Rail Fence
def decrypt(text, rails=3):
    decrypted_text = [''] * len(text)
    index = 0
    for i in range(rails):
        for j in range(i, len(text), rails):
            decrypted_text[j] = text[index]
            index += 1
    return ''.join(decrypted_text)