class ArithmeticCoding:
    def __init__(self, probabilities):
        self.probabilities = probabilities

    def compress(self, message):
        low = 0.0
        high = 1.0
        for symbol in message:
            pRange = high - low
            symbol_low, symbol_high = self.probabilities[symbol]
            high = low + pRange * symbol_high
            low = low + pRange * symbol_low
        return (low + high) / 2

    def decompress(self, code, message_length):
        low = 0.0
        high = 1.0
        decoded_message = []
        for _ in range(message_length):
            pRange = high - low
            value = (code - low) / pRange
            # print(value)
            for symbol, (symbol_low, symbol_high) in self.probabilities.items():
                if symbol_low <= value < symbol_high:
                    decoded_message.append(symbol)
                    high = low + pRange * symbol_high
                    low = low + pRange * symbol_low
                    break
        return ''.join(decoded_message)


def main():
    with open("Input.txt", "r") as f:
        lines = f.readlines()
    
    probabilities = {}
    message = None
    
    for line in lines:
        if "message:" in line.lower():
            message = line.split(":")[1].strip()
        else:
            symbol, low, high = line.strip().split()
            probabilities[symbol] = (float(low), float(high))
    
    if message is None:
        raise ValueError("Message not found in input file.")

    ac = ArithmeticCoding(probabilities)

    compressed_code = ac.compress(message)

    with open("Compressed.txt", "w") as f:
        f.write(str(compressed_code))

    print(f"Compressed Succesfully")

    decompressed_message = ac.decompress(compressed_code, len(message))

    with open("Decompressed.txt", "w") as f:
        f.write(decompressed_message)

    print(f"Decompressed Succesfully")


main()