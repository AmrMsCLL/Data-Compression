# Compression Algorithms

Five classic compression schemes implemented from scratch in Python — no compression libraries,
one self-contained file each. Written for the Data Compression course at FCAI, Cairo University.

| File | Algorithm | Type |
| :--- | :--- | :--- |
| [`Standard Huffman.py`](Standard%20Huffman.py) | Huffman coding | Lossless, entropy |
| [`Arithmetic.py`](Arithmetic.py) | Arithmetic coding | Lossless, entropy |
| [`LZW.py`](LZW.py) | Lempel–Ziv–Welch | Lossless, dictionary |
| [`lz77.py`](lz77.py) | LZ77 sliding window | Lossless, dictionary |
| [`VQ.py`](VQ.py) | Vector Quantization (LBG) | Lossy, images |

## Sample inputs

`input.txt` is a plain-text sample for Huffman, LZW and LZ77. `arithmetic_input.txt` carries the
symbol model that Arithmetic coding needs, in the format shown below.

## Requirements

Huffman, Arithmetic, LZW and LZ77 need only the standard library. Vector Quantization needs:

```sh
pip install -r requirements.txt
```

## Huffman

Builds a frequency table, merges the two lowest-frequency nodes until one tree remains, then walks
it to assign a prefix code per character.

```sh
python "Standard Huffman.py" input.txt compressed.txt decompressed.txt
```

The compressed file holds the code map on the first line and the bit string on the second. Both
are written as text, so it demonstrates the coding rather than producing a smaller file on disk.

## Arithmetic

Narrows the interval `[0, 1)` symbol by symbol and emits the midpoint as a single float. Symbol
ranges are supplied rather than derived, so the input file carries the model:

```
a 0.0 0.5
b 0.5 0.8
c 0.8 1.0
message: abcab
```

```sh
python Arithmetic.py arithmetic_input.txt
```

The interval is tracked in a 64-bit float, so precision is the binding limit: with the three-symbol
model in `arithmetic_input.txt` it round-trips up to 31 symbols, and beyond that the interval
collapses below what a float can represent and decoding fails. That is inherent to carrying the
range in a float rather than a bug in the coder.

## LZW

Starts from a 128-entry ASCII dictionary and adds every new sequence it meets, emitting integer
codes.

```sh
python LZW.py input.txt compressed.txt decompressed.txt
```

## LZ77

Slides a 20-byte window back over the input looking for the longest match, emitting
`(offset, length, next_char)` triples.

```sh
python lz77.py            # runs a built-in demo string
python lz77.py input.txt  # or compress a file
```

## Vector Quantization

The lossy one. Splits a grayscale image into 4×4 blocks, trains a codebook with the
**Linde–Buzo–Gray** algorithm — start from the mean block, split each centroid by `±ε`, then
iterate nearest-centroid assignment until distortion converges — and stores only the codebook plus
one index per block.

```sh
python VQ.py test.png compressed.json decompressed.png
```

Defaults to a 64-entry codebook over 4×4 blocks, which is 16 pixels reduced to one byte of index.
