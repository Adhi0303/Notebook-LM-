import os
import sys
from dotenv import load_dotenv
from google import genai
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import numpy as np

# Load the API key
load_dotenv()
client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))

def create_visualization():
    print("========================================")
    print("  AI GRAPH VISUALIZER  ")
    print("========================================\n")
    
    # 1. Pick words from 3 completely distinct categories
    words = [
        "Dog", "Cat", "Puppy", "Kitten",        # Animals
        "Car", "Truck", "Motorcycle", "Bus",    # Vehicles
        "Apple", "Banana", "Orange", "Grape"    # Fruits
    ]

    print("1. Sending words to Google Gemini to get 768-dimension coordinates...")
    embeddings = []
    for word in words:
        result = client.models.embed_content(
            model="gemini-embedding-2",
            contents=word,
            config={"output_dimensionality": 768}
        )
        embeddings.append(result.embeddings[0].values)

    # 2. We cannot draw 768 dimensions on a flat screen. 
    # We use an algorithm called PCA to crush 768 dimensions down to 2 dimensions (X and Y)
    print("2. Crushing 768 dimensions down to 2D (X, Y) so human eyes can see it...")
    pca = PCA(n_components=2)
    reduced_embeddings = pca.fit_transform(embeddings)

    # 3. Draw the map!
    print("3. Drawing the map...")
    plt.figure(figsize=(10, 8))
    
    # Plot the dots
    plt.scatter(reduced_embeddings[:, 0], reduced_embeddings[:, 1], c='red', s=100)

    # Add the text labels next to the dots
    for i, word in enumerate(words):
        plt.annotate(word, (reduced_embeddings[i, 0] + 0.005, reduced_embeddings[i, 1] + 0.005), fontsize=14, fontweight='bold')

    plt.title("The AI's Brain: Semantic Meaning Mapped Geometrically", fontsize=16)
    plt.grid(True, linestyle='--', alpha=0.5)

    # Save the image
    save_path = r"C:\Users\suriy\.gemini\antigravity-ide\brain\97fc49e2-ba80-436a-bd09-be2f5ae38cdf\scratch\embeddings_graph.png"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, bbox_inches='tight')
    print(f"\nGraph successfully saved to: {save_path}")

if __name__ == "__main__":
    create_visualization()
