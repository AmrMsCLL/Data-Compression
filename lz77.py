class LZ77:
    def __init__(self, window_size=20):
        self.window_size = window_size

    def compress(self, data):
        compressed_data = []
        i = 0 
        
        while i < len(data):
            match_offset = 0
            match_length = 0
            
            start = max(0, i - self.window_size)
            for j in range(start, i):
                length = 0
                while (length < self.window_size and 
                       i + length < len(data) and 
                       data[j + length] == data[i + length]):
                    length += 1

                if length > match_length or (length == match_length and (i - j) < match_offset):
                    match_offset = i - j
                    match_length = length

            if match_length > 0:
                next_char = data[i + match_length] if i + match_length < len(data) else ''
                compressed_data.append((match_offset, match_length, next_char))
                i += match_length + 1
            else:
                compressed_data.append((0, 0, data[i]))
                i += 1
        
        return compressed_data

    def decompress(self, compressed_data):
        decompressed_data = []
        
        for offset, length, char in compressed_data:
            if offset == 0 and length == 0:
                decompressed_data.append(char)
            else:
                start = len(decompressed_data) - offset
                for j in range(length):
                    decompressed_data.append(decompressed_data[start + j])
                decompressed_data.append(char)
        
        return ''.join(decompressed_data)

data = "abaababaabbbbbbbbbbbba"
lz77 = LZ77(window_size=20)
compressed = lz77.compress(data)
decompressed = lz77.decompress(compressed)

print("Original:", data)
print("Compressed:", compressed)
print("Decompressed:", decompressed)