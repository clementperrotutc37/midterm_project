from scapy.all import rdpcap
from PIL import Image
import numpy as np
import sys

# Fonction pour traiter un flux réseau et le convertir en image 28x28
def process_packet_data(packet_data, max_size=784):
    # Convertir les données en bytes
    byte_data = bytes(packet_data)

    # Trimmer ou ajouter des 0x00 pour que la taille soit exactement de 784 bytes
    if len(byte_data) > max_size:
        byte_data = byte_data[:max_size]
    else:
        byte_data = byte_data + b'\x00' * (max_size - len(byte_data))

    # Conversion en tableau numpy de taille 28x28
    image_data = np.frombuffer(byte_data, dtype=np.uint8).reshape((28, 28))
    
    # Création d'une image à partir du tableau numpy
    image = Image.fromarray(image_data, mode='L')  # 'L' pour image en niveaux de gris
    return image

# Fonction pour lire un fichier PCAP et traiter chaque paquet
def pcap_to_images(pcap_file):
    packets = rdpcap(pcap_file)
    images = []

    for packet in packets:
        # Extraction des données brutes de chaque paquet
        raw_data = bytes(packet)
        # Traitement et conversion en image
        image = process_packet_data(raw_data)
        images.append(image)
    
    return images

# Exemple d'utilisation
if len(sys.argv) != 2:
    print("Usage: python pcap_to_image.py <path_to_pcap_file>")
    sys.exit(1)

pcap_file = sys.argv[1]
images = pcap_to_images(pcap_file)

# Sauvegarder les images dans un dossier
for i, img in enumerate(images):
    img.save(f'image_{i}.png')
    print(f'Image {i} enregistrée.')
