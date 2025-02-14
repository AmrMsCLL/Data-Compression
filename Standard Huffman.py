class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None


def build_huffman_tree(text):
    freq = {char: text.count(char) for char in set(text)}
    # print(freq)

    nodes = [HuffmanNode(char, freq) for char, freq in freq.items()]

    while len(nodes) > 1:
        nodes.sort(key=lambda node: node.freq)
        left = nodes.pop(0)
        right = nodes.pop(0)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        nodes.append(merged)
    
    return nodes[0]


def build_codes(node, prefix="", code_map=None):
    if code_map is None:
        code_map = {}
    if node is None:
        return code_map  

    if node.char is not None: 
        code_map[node.char] = prefix

    build_codes(node.left, prefix + "0", code_map)
    build_codes(node.right, prefix + "1", code_map)
    # print (code_map)
    return code_map


def huffman_compress(input_file, output_file):
    with open(input_file, 'r') as file:
        text = file.read()
    
    root = build_huffman_tree(text)
    codes = build_codes(root)
    encoded_text = ''.join(codes[char] for char in text)
    
    with open(output_file, 'w') as file:
        file.write(f"{codes}\n")  
        file.write(encoded_text) 
    return root


def huffman_decompress(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()
        codes = eval(lines[0].strip())  
        encoded_text = lines[1].strip()  
    
    reverse_codes = {code: char for char, code in codes.items()}
    
    decoded_text = []
    current_code = ""
    for bit in encoded_text:
        current_code += bit
        if current_code in reverse_codes:  
            decoded_text.append(reverse_codes[current_code])
            current_code = ""  

    with open(output_file, 'w') as file:
        file.write(''.join(decoded_text))

input_file = "input.txt"
compressed_file = "compressed.txt"
decompressed_file = "decompressed.txt"

huffman_compress(input_file, compressed_file)
print(f"Compressed data written to {compressed_file}.")

huffman_decompress(compressed_file, decompressed_file)
print(f"Decompressed data written to {decompressed_file}.")