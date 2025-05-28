
from flask import Flask, render_template, request
from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.railfence import RailFenceCipher
from cipher.playfair import PlayFairCipher
from cipher.transposition import TranspositionCipher

app = Flask(__name__)

# Inline Vigenère Cipher implementation
def vigenere_encrypt_text(text, key):
    """Temporary Vigenère encryption within app.py."""
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    text = ''.join(c.upper() for c in text if c.isalpha())
    key = ''.join(c.upper() for c in key if c.isalpha())
    if not key:
        return "Lỗi: Khóa phải chứa ít nhất một chữ cái."
    if not text:
        return "Lỗi: Văn bản gốc không chứa chữ cái hợp lệ."
    
    extended_key = (key * (len(text) // len(key) + 1))[:len(text)]
    ciphertext = ''
    
    for p, k in zip(text, extended_key):
        p_idx = alphabet.index(p)
        k_idx = alphabet.index(k)
        c_idx = (p_idx + k_idx) % 26
        ciphertext += alphabet[c_idx]
    
    return ciphertext

def vigenere_decrypt_text(text, key):
    """Temporary Vigenère decryption within app.py."""
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    text = ''.join(c.upper() for c in text if c.isalpha())
    key = ''.join(c.upper() for c in key if c.isalpha())
    if not key:
        return "Lỗi: Khóa phải chứa ít nhất một chữ cái."
    if not text:
        return "Lỗi: Văn bản mã hóa không chứa chữ cái hợp lệ."
    
    extended_key = (key * (len(text) // len(key) + 1))[:len(text)]
    plaintext = ''
    
    for c, k in zip(text, extended_key):
        c_idx = alphabet.index(c)
        k_idx = alphabet.index(k)
        p_idx = (c_idx - k_idx) % 26
        plaintext += alphabet[p_idx]
    
    return plaintext

# Inline Rail Fence Cipher implementation
def railfence_encrypt_text(text, key):
    """Temporary Rail Fence encryption within app.py."""
    if not text:
        return "Lỗi: Văn bản gốc không chứa ký tự hợp lệ."
    if not isinstance(key, int) or key < 2:
        return "Lỗi: Số hàng phải là số nguyên lớn hơn hoặc bằng 2."
    
    text = ''.join(c for c in text.upper() if c.isalnum())
    if not text:
        return "Lỗi: Văn bản gốc không chứa ký tự hợp lệ."
    
    rails = [''] * key
    row = 0
    direction = 1
    
    for char in text:
        rails[row] += char
        row += direction
        if row == 0 or row == key - 1:
            direction *= -1
    
    return ''.join(rails)

def railfence_decrypt_text(text, key):
    """Temporary Rail Fence decryption within app.py."""
    if not text:
        return "Lỗi: Văn bản mã hóa không chứa ký tự hợp lệ."
    if not isinstance(key, int) or key < 2:
        return "Lỗi: Số hàng phải là số nguyên lớn hơn hoặc bằng 2."
    
    text = ''.join(c for c in text.upper() if c.isalnum())
    if not text:
        return "Lỗi: Văn bản mã hóa không chứa ký tự hợp lệ."
    
    n = len(text)
    rail_lengths = [0] * key
    row = 0
    direction = 1
    
    for _ in range(n):
        rail_lengths[row] += 1
        row += direction
        if row == 0 or row == key - 1:
            direction *= -1
    
    rails = []
    start = 0
    for length in rail_lengths:
        rails.append(text[start:start + length])
        start += length
    
    result = []
    row = 0
    direction = 1
    rail_idx = [0] * key
    
    for _ in range(n):
        result.append(rails[row][rail_idx[row]])
        rail_idx[row] += 1
        row += direction
        if row == 0 or row == key - 1:
            direction *= -1
    
    return ''.join(result)

# Inline Playfair Cipher implementation
def playfair_encrypt_text(text, key):
    """Temporary Playfair encryption within app.py."""
    text = ''.join(c.upper() for c in text if c.isalpha()).replace('J', 'I')
    key = ''.join(c.upper() for c in key if c.isalpha()).replace('J', 'I')
    if not key:
        return "Lỗi: Khóa phải chứa ít nhất một chữ cái."
    if not text:
        return "Lỗi: Văn bản gốc không chứa chữ cái hợp lệ."
    
    alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
    key = ''.join(dict.fromkeys(key))
    matrix_chars = key + ''.join(c for c in alphabet if c not in key)
    matrix = [list(matrix_chars[i:i+5]) for i in range(0, 25, 5)]
    
    digraphs = []
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1 < len(text) else 'X'
        if a == b:
            digraphs.append(a + 'X')
            i += 1
        else:
            digraphs.append(a + b)
            i += 2
    if len(text) % 2 == 1:
        digraphs[-1] = digraphs[-1][0] + 'X'
    
    ciphertext = ''
    for digraph in digraphs:
        a, b = digraph
        row_a, col_a = next((r, c) for r in range(5) for c in range(5) if matrix[r][c] == a)
        row_b, col_b = next((r, c) for r in range(5) for c in range(5) if matrix[r][c] == b)
        
        if row_a == row_b:
            ciphertext += matrix[row_a][(col_a + 1) % 5] + matrix[row_b][(col_b + 1) % 5]
        elif col_a == col_b:
            ciphertext += matrix[(row_a + 1) % 5][col_a] + matrix[(row_b + 1) % 5][col_b]
        else:
            ciphertext += matrix[row_a][col_b] + matrix[row_b][col_a]
    
    return ciphertext

def playfair_decrypt_text(text, key):
    """Temporary Playfair decryption within app.py."""
    text = ''.join(c.upper() for c in text if c.isalpha()).replace('J', 'I')
    key = ''.join(c.upper() for c in key if c.isalpha()).replace('J', 'I')
    if not key:
        return "Lỗi: Khóa phải chứa ít nhất một chữ cái."
    if not text:
        return "Lỗi: Văn bản mã hóa không chứa chữ cái hợp lệ."
    if len(text) % 2 != 0:
        return "Lỗi: Văn bản mã hóa phải có độ dài chẵn."
    
    alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
    key = ''.join(dict.fromkeys(key))
    matrix_chars = key + ''.join(c for c in alphabet if c not in key)
    matrix = [list(matrix_chars[i:i+5]) for i in range(0, 25, 5)]
    
    plaintext = ''
    for i in range(0, len(text), 2):
        a, b = text[i:i+2]
        row_a, col_a = next((r, c) for r in range(5) for c in range(5) if matrix[r][c] == a)
        row_b, col_b = next((r, c) for r in range(5) for c in range(5) if matrix[r][c] == b)
        
        if row_a == row_b:
            plaintext += matrix[row_a][(col_a - 1) % 5] + matrix[row_b][(col_b - 1) % 5]
        elif col_a == col_b:
            plaintext += matrix[(row_a - 1) % 5][col_a] + matrix[(row_b - 1) % 5][col_b]
        else:
            plaintext += matrix[row_a][col_b] + matrix[row_b][col_a]
    
    return plaintext

# Inline Transposition Cipher implementation
def transposition_encrypt_text(text, key):
    """Temporary Transposition encryption within app.py."""
    if not text:
        return "Lỗi: Văn bản gốc không chứa ký tự hợp lệ."
    if not isinstance(key, int) or key < 2:
        return "Lỗi: Số cột phải là số nguyên lớn hơn hoặc bằng 2."
    
    text = ''.join(c for c in text.upper() if c.isalnum())
    if not text:
        return "Lỗi: Văn bản gốc không chứa ký tự hợp lệ."
    
    # Calculate rows and pad text with X if needed
    n = len(text)
    cols = key
    rows = (n + cols - 1) // cols
    padded_text = text + 'X' * (rows * cols - n)
    
    # Create grid
    grid = [padded_text[i:i+cols] for i in range(0, len(padded_text), cols)]
    
    # Read columns to form ciphertext
    ciphertext = ''
    for col in range(cols):
        for row in range(rows):
            ciphertext += grid[row][col]
    
    return ciphertext

def transposition_decrypt_text(text, key):
    """Temporary Transposition decryption within app.py."""
    if not text:
        return "Lỗi: Văn bản mã hóa không chứa ký tự hợp lệ."
    if not isinstance(key, int) or key < 2:
        return "Lỗi: Số cột phải là số nguyên lớn hơn hoặc bằng 2."
    
    text = ''.join(c for c in text.upper() if c.isalnum())
    if not text:
        return "Lỗi: Văn bản mã hóa không chứa ký tự hợp lệ."
    
    n = len(text)
    cols = key
    rows = n // cols
    if n % cols != 0:
        return "Lỗi: Độ dài văn bản mã hóa không phù hợp với số cột."
    
    # Create empty grid
    grid = [['' for _ in range(cols)] for _ in range(rows)]
    
    # Fill grid column by column
    idx = 0
    for col in range(cols):
        for row in range(rows):
            grid[row][col] = text[idx]
            idx += 1
    
    # Read rows to form plaintext
    plaintext = ''
    for row in range(rows):
        plaintext += ''.join(grid[row])
    
    # Remove padding Xs
    return plaintext.rstrip('X')

# Route for homepage
@app.route('/')
def home():
    return render_template('index.html')

# Routes for Caesar Cipher
@app.route('/caesar')
def caesar():
    return render_template('caesar.html')

@app.route('/encrypt', methods=['POST'])
def caesar_encrypt():
    text = request.form['inputPlainText']
    key_input = request.form['inputKeyPlain']
    
    try:
        key = int(key_input)
        if key < 0:
            return "Lỗi: Khóa phải là số nguyên không âm.<br/><a href='/caesar'>Quay lại</a>"
    except ValueError:
        return "Lỗi: Khóa phải là một số nguyên hợp lệ.<br/><a href='/caesar'>Quay lại</a>"
    
    caesar = CaesarCipher()
    encrypted_text = caesar.encrypt_text(text, key)
    return f"Văn bản gốc: {text}<br/>Khóa: {key}<br/>Văn bản mã hóa: {encrypted_text}<br/><a href='/caesar'>Quay lại</a>"

@app.route('/decrypt', methods=['POST'])
def caesar_decrypt():
    text = request.form['inputCipherText']
    key_input = request.form['inputKeyCipher']
    
    try:
        key = int(key_input)
        if key < 0:
            return "Lỗi: Khóa phải là số nguyên không âm.<br/><a href='/caesar'>Quay lại</a>"
    except ValueError:
        return "Lỗi: Khóa phải là một số nguyên hợp lệ.<br/><a href='/caesar'>Quay lại</a>"
    
    caesar = CaesarCipher()
    decrypted_text = caesar.decrypt_text(text, key)
    return f"Văn bản mã hóa: {text}<br/>Khóa: {key}<br/>Văn bản giải mã: {decrypted_text}<br/><a href='/caesar'>Quay lại</a>"

# Routes for Vigenère Cipher
@app.route('/vigenere')
def vigenere():
    return render_template('vigenere.html')

@app.route('/vigenere_encrypt', methods=['POST'])
def vigenere_encrypt():
    text = request.form['inputPlainText']
    key = request.form['inputKeyPlain']
    
    try:
        vigenere = VigenereCipher()
        encrypted_text = vigenere.encrypt_text(text, key)
    except AttributeError:
        encrypted_text = vigenere_encrypt_text(text, key)
    
    return f"Văn bản gốc: {text}<br/>Khóa: {key}<br/>Văn bản mã hóa: {encrypted_text}<br/><a href='/vigenere'>Quay lại</a>"

@app.route('/vigenere_decrypt', methods=['POST'])
def vigenere_decrypt():
    text = request.form['inputCipherText']
    key = request.form['inputKeyCipher']
    
    try:
        vigenere = VigenereCipher()
        decrypted_text = vigenere.decrypt_text(text, key)
    except AttributeError:
        decrypted_text = vigenere_decrypt_text(text, key)
    
    return f"Văn bản mã hóa: {text}<br/>Khóa: {key}<br/>Văn bản giải mã: {decrypted_text}<br/><a href='/vigenere'>Quay lại</a>"

# Routes for Rail Fence Cipher
@app.route('/railfence')
def railfence():
    return render_template('railfence.html')

@app.route('/railfence_encrypt', methods=['POST'])
def railfence_encrypt():
    text = request.form['inputPlainText']
    key_input = request.form['inputKeyPlain']
    
    try:
        key = int(key_input)
        if key < 2:
            return "Lỗi: Số hàng phải là số nguyên lớn hơn hoặc bằng 2.<br/><a href='/railfence'>Quay lại</a>"
    except ValueError:
        return "Lỗi: Số hàng phải là một số nguyên hợp lệ.<br/><a href='/railfence'>Quay lại</a>"
    
    try:
        railfence = RailFenceCipher()
        encrypted_text = railfence.encrypt_text(text, key)
    except AttributeError:
        encrypted_text = railfence_encrypt_text(text, key)
    
    return f"Văn bản gốc: {text}<br/>Số hàng: {key}<br/>Văn bản mã hóa: {encrypted_text}<br/><a href='/railfence'>Quay lại</a>"

@app.route('/railfence_decrypt', methods=['POST'])
def railfence_decrypt():
    text = request.form['inputCipherText']
    key_input = request.form['inputKeyCipher']
    
    try:
        key = int(key_input)
        if key < 2:
            return "Lỗi: Số hàng phải là số nguyên lớn hơn hoặc bằng 2.<br/><a href='/railfence'>Quay lại</a>"
    except ValueError:
        return "Lỗi: Số hàng phải là một số nguyên hợp lệ.<br/><a href='/railfence'>Quay lại</a>"
    
    try:
        railfence = RailFenceCipher()
        decrypted_text = railfence.decrypt_text(text, key)
    except AttributeError:
        decrypted_text = railfence_decrypt_text(text, key)
    
    return f"Văn bản mã hóa: {text}<br/>Số hàng: {key}<br/>Văn bản giải mã: {decrypted_text}<br/><a href='/railfence'>Quay lại</a>"

# Routes for Playfair Cipher
@app.route('/playfair')
def playfair():
    return render_template('playfair.html')

@app.route('/playfair_encrypt', methods=['POST'])
def playfair_encrypt():
    text = request.form['inputPlainText']
    key = request.form['inputKeyPlain']
    
    try:
        playfair = PlayFairCipher()
        encrypted_text = playfair.encrypt_text(text, key)
    except AttributeError:
        encrypted_text = playfair_encrypt_text(text, key)
    
    return f"Văn bản gốc: {text}<br/>Khóa: {key}<br/>Văn bản mã hóa: {encrypted_text}<br/><a href='/playfair'>Quay lại</a>"

@app.route('/playfair_decrypt', methods=['POST'])
def playfair_decrypt():
    text = request.form['inputCipherText']
    key = request.form['inputKeyCipher']
    
    try:
        playfair = PlayFairCipher()
        decrypted_text = playfair.decrypt_text(text, key)
    except AttributeError:
        decrypted_text = playfair_decrypt_text(text, key)
    
    return f"Văn bản mã hóa: {text}<br/>Khóa: {key}<br/>Văn bản giải mã: {decrypted_text}<br/><a href='/playfair'>Quay lại</a>"

# Routes for Transposition Cipher
@app.route('/transposition')
def transposition():
    return render_template('transposition.html')

@app.route('/transposition_encrypt', methods=['POST'])
def transposition_encrypt():
    text = request.form['inputPlainText']
    key_input = request.form['inputKeyPlain']
    
    try:
        key = int(key_input)
        if key < 2:
            return "Lỗi: Số cột phải là số nguyên lớn hơn hoặc bằng 2.<br/><a href='/transposition'>Quay lại</a>"
    except ValueError:
        return "Lỗi: Số cột phải là một số nguyên hợp lệ.<br/><a href='/transposition'>Quay lại</a>"
    
    try:
        transposition = TranspositionCipher()
        encrypted_text = transposition.encrypt_text(text, key)
    except AttributeError:
        encrypted_text = transposition_encrypt_text(text, key)
    
    return f"Văn bản gốc: {text}<br/>Số cột: {key}<br/>Văn bản mã hóa: {encrypted_text}<br/><a href='/transposition'>Quay lại</a>"

@app.route('/transposition_decrypt', methods=['POST'])
def transposition_decrypt():
    text = request.form['inputCipherText']
    key_input = request.form['inputKeyCipher']
    
    try:
        key = int(key_input)
        if key < 2:
            return "Lỗi: Số cột phải là số nguyên lớn hơn hoặc bằng 2.<br/><a href='/transposition'>Quay lại</a>"
    except ValueError:
        return "Lỗi: Số cột phải là một số nguyên hợp lệ.<br/><a href='/transposition'>Quay lại</a>"
    
    try:
        transposition = TranspositionCipher()
        decrypted_text = transposition.decrypt_text(text, key)
    except AttributeError:
        decrypted_text = transposition_decrypt_text(text, key)
    
    return f"Văn bản mã hóa: {text}<br/>Số cột: {key}<br/>Văn bản giải mã: {decrypted_text}<br/><a href='/transposition'>Quay lại</a>"

# Main function
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
