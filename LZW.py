import sys


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

    with open(output_file_path, 'w', encoding='utf-8', newline='') as file:
        file.write("".join(result))

    print("Decompression complete. Decompressed data saved to", output_file_path)


if __name__ == "__main__":
    argv = sys.argv[1:]
    input_file = argv[0] if len(argv) > 0 else "input.txt"
    compressed_file = argv[1] if len(argv) > 1 else "compressed.txt"
    decompressed_file = argv[2] if len(argv) > 2 else "decompressed.txt"

    lzw_compress(input_file, compressed_file)
    lzw_decompress(compressed_file, decompressed_file)
