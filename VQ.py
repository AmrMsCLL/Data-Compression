import numpy as np
import cv2
import json
import os
os.chdir(r'd:\University stuff\Y3\Y2T1\Data Compression\Compression Algorithms\VQ')

def divide_into_blocks(image, block_size):
    h, w = image.shape
    blocks = []
    for i in range(0, h, block_size):
        for j in range(0, w, block_size):
            block = image[i:i+block_size, j:j+block_size]
            if block.shape == (block_size, block_size):
                blocks.append(block.flatten())
    return np.array(blocks), (h, w)

def reconstruct_from_blocks(blocks, image_shape, block_size):
    h, w = image_shape
    image = np.zeros((h, w), dtype=np.uint8)
    idx = 0
    for i in range(0, h, block_size):
        for j in range(0, w, block_size):
            if idx < len(blocks):
                block = blocks[idx].reshape((block_size, block_size))
                image[i:i+block_size, j:j+block_size] = block
                idx += 1
    return image

def lbg_algorithm(blocks, codebook_size, epsilon=0.01):
    centroids = np.mean(blocks, axis=0).reshape(1, -1)
    
    while len(centroids) < codebook_size:
        centroids = np.vstack((centroids * (1 + epsilon), centroids * (1 - epsilon)))
        
        prev_distortion = float('inf')
        while True:
            distances = np.linalg.norm(blocks[:, np.newaxis] - centroids, axis=2)
            labels = np.argmin(distances, axis=1)
            
            new_centroids = np.array([blocks[labels == i].mean(axis=0) if len(blocks[labels == i]) > 0 else centroids[i]
                                      for i in range(len(centroids))])
            
            distortion = np.sum((blocks - new_centroids[labels]) ** 2)
            
            if abs(prev_distortion - distortion) < epsilon:
                break
            centroids = new_centroids
            prev_distortion = distortion
    
    return centroids, labels

def compress_image(image_path, block_size, codebook_size, output_file):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    blocks, image_shape = divide_into_blocks(image, block_size)
    
    codebook, labels = lbg_algorithm(blocks, codebook_size)
    
    compressed_data = {
        'shape': image_shape,
        'block_size': block_size,
        'codebook': codebook.tolist(),
        'labels': labels.tolist()
    }
    
    with open(output_file, 'w') as f:
        json.dump(compressed_data, f)
    print(f"Image compressed and saved to {output_file}")

def decompress_image(compressed_file, output_image):
    with open(compressed_file, 'r') as f:
        data = json.load(f)
    
    shape = tuple(data['shape'])
    block_size = data['block_size']
    codebook = np.array(data['codebook'])
    labels = np.array(data['labels'])
    
    blocks = codebook[labels]
    image = reconstruct_from_blocks(blocks, shape, block_size)
    
    cv2.imwrite(output_image, image)
    print(f"Image decompressed and saved to {output_image}")

compress_image('test.png', block_size=4, codebook_size=64, output_file='compressed.json')
decompress_image('compressed.json', output_image='decompressed_image.png')
