from cipher.caesar import ALPHABET

class CaesarCipher:
    def __init__(self):
        self.alphabet = ALPHABET

    
    def encrypt_text(self, test: str, key: int) -> str:
        alphabet_len = len(self.alphabet)
        text = test.upper()
        encrypted_text = []
        for letter in text:
            letter_index = self.alphabet.index(letter)
            outdoor_index = (letter_index + key) % alphabet_len
            output_letter = self.alphabet[outdoor_index]
            encrypted_text.append(output_letter)
        return "".join(encrypted_text)
    
    def decrypt_text(self, test: str, key: int) -> str:
        alphabet_len = len(self.alphabet)
        text = test.upper()
        decrypted_text = []
        for letter in text:
            letter_index = self.alphabet.index(letter)
            outdoor_index = (letter_index - key) % alphabet_len
            output_letter = self.alphabet[outdoor_index]
            decrypted_text.append(output_letter)
        return "".join(decrypted_text)
    
    
            
        
       
        