def lzw_compress(input_file_path, output_file_path):
    dictionary = {chr(i): i for i in range(128)}
    result = []
    w = ""

    with open(input_file_path, 'r', encoding='utf-8') as file:
        data = file.read()

    for c in data: 
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc] = len(dictionary)
            w = c

    if w:
        result.append(dictionary[w])

    with open(output_file_path, 'w') as file:
        file.write(" ".join(str(code) for code in result))

    print("Compression complete. Compressed data saved to", output_file_path)

def lzw_decompress(input_file_path, output_file_path):
    dictionary = {i: chr(i) for i in range(128)}
    result = []

    with open(input_file_path, 'r') as file:
        compressed_data = [int(code) for code in file.read().split()]

    w = chr(compressed_data.pop(0))
    result.append(w)

    for code in compressed_data:
        if code in dictionary:
            entry = dictionary[code]
        elif code == len(dictionary):
            entry = w + w[0]
        else:
            raise ValueError("Invalid compressed code")

        result.append(entry)
        dictionary[len(dictionary)] = w + entry[0]
        w = entry

    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write("".join(result))

    print("Decompression complete. Decompressed data saved to", output_file_path)

input_file = r'C:\Users\AmrSherieyCLL\Desktop\Compression\Input.txt'
compressed_file = r'C:\Users\AmrSherieyCLL\Desktop\Compression\CompressedOut.txt'
decompressed_file = r'C:\Users\AmrSherieyCLL\Desktop\Compression\DeCompressedOut.txt'

lzw_compress(input_file, compressed_file)

lzw_decompress(compressed_file, decompressed_file)
