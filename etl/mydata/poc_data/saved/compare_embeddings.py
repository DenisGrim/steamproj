#!/usr/bin/env python3
"""
Compare the distinctness of embeddings between two CSV files.
Calculates average pairwise distances within each CSV to determine which has more distinct vectors.
"""

import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist
import sys


def parse_embedding(emb_str):
    """Parse embedding string to numpy array, return None if empty/invalid."""
    if pd.isna(emb_str) or emb_str == '':
        return None
    
    try:
        # Handle different formats: "[1,2,3]" or "1,2,3"
        emb_str = emb_str.strip()
        if emb_str.startswith('[') and emb_str.endswith(']'):
            emb_str = emb_str[1:-1]
        
        values = [float(x.strip()) for x in emb_str.split(',')]
        return np.array(values)
    except:
        return None


def load_embeddings(csv_path):
    """Load embeddings from CSV file."""
    df = pd.read_csv(csv_path)
    
    if 'embedding' not in df.columns:
        raise ValueError(f"CSV {csv_path} does not have an 'embedding' column")
    
    embeddings = []
    for emb_str in df['embedding']:
        emb = parse_embedding(emb_str)
        if emb is not None:
            embeddings.append(emb)
    
    return np.array(embeddings) if embeddings else None


def calculate_avg_distance(embeddings):
    """Calculate average pairwise distance between embeddings."""
    if embeddings is None or len(embeddings) < 2:
        return None
    
    # Calculate all pairwise distances
    distances = pdist(embeddings, metric='euclidean')
    return np.mean(distances)


def main():
    if len(sys.argv) != 3:
        print("Usage: python compare_embeddings.py <csv1> <csv2>")
        sys.exit(1)
    
    csv1_path = sys.argv[1]
    csv2_path = sys.argv[2]
    
    print(f"Loading embeddings from {csv1_path}...")
    embeddings1 = load_embeddings(csv1_path)
    
    print(f"Loading embeddings from {csv2_path}...")
    embeddings2 = load_embeddings(csv2_path)
    
    if embeddings1 is None:
        print(f"No valid embeddings found in {csv1_path}")
        return
    if embeddings2 is None:
        print(f"No valid embeddings found in {csv2_path}")
        return
    
    print(f"\nCSV 1: {len(embeddings1)} valid embeddings")
    print(f"CSV 2: {len(embeddings2)} valid embeddings")
    
    avg_dist1 = calculate_avg_distance(embeddings1)
    avg_dist2 = calculate_avg_distance(embeddings2)
    
    print(f"\n{'='*60}")
    print(f"Average pairwise distance in CSV 1: {avg_dist1:.6f}")
    print(f"Average pairwise distance in CSV 2: {avg_dist2:.6f}")
    print(f"{'='*60}")
    
    if avg_dist1 > avg_dist2:
        difference = ((avg_dist1 - avg_dist2) / avg_dist2) * 100
        print(f"\n✓ CSV 1 has MORE DISTINCT vectors (embeddings are {difference:.1f}% more separated)")
    elif avg_dist2 > avg_dist1:
        difference = ((avg_dist2 - avg_dist1) / avg_dist1) * 100
        print(f"\n✓ CSV 2 has MORE DISTINCT vectors (embeddings are {difference:.1f}% more separated)")
    else:
        print(f"\n→ Both CSVs have equally distinct vectors")


if __name__ == "__main__":
    main()
