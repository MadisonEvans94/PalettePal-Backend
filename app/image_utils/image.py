from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import io


def open_image(image_file: io.BytesIO) -> Image.Image:
    """
    Open an image using PIL.
    Args:
        image_file (io.BytesIO): A file-like object containing the image.
    Returns:
        PIL.Image: An Image object.
    """

    try:
        image_file.seek(0)
        image = Image.open(image_file)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        return image
    except Exception as e:
        raise


def process_image(image: Image):

    # Define a new width for the image, maintaining aspect ratio
    new_width = 100
    aspect_ratio = image.height / image.width
    new_height = int(new_width * aspect_ratio)

    # Resize the image
    resized_image = image.resize((new_width, new_height))

    # Convert PIL image to a numpy array
    image_np = np.asarray(resized_image)
    image_reshape = image_np.reshape(-1, 3)

    # Normalize pixel values by dividing by 255
    image_reshape = image_reshape / 255.0

    return image_reshape


def rgb_to_hex(rgb):
    """Converts an RGB color to Hex format"""
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def rgb_kmeans(image_np,  k):

    kmeans = KMeans(n_clusters=k, init='k-means++', n_init='auto', max_iter=10,
                    tol=0.0001, verbose=0, random_state=None, copy_x=True, algorithm='lloyd').fit(image_np)

    # Convert cluster centers back to RGB format
    clusters = kmeans.cluster_centers_ * 255

    # Round the values and convert to integers
    clusters = np.rint(clusters).astype(int)

    # Count the pixels in each cluster
    labels = kmeans.labels_
    cluster_sizes = [np.sum(labels == i) for i in range(k)]

    return clusters, cluster_sizes


def process_clusters(image_file: io.BytesIO):
    try:
        image_pil = open_image(image_file)
        image_np = process_image(image_pil)
        all_clusters = []
        all_cluster_sizes = []

        # Perform K-means clustering for k=1 to 6
        for k in range(1, 7):
            clusters, cluster_sizes = rgb_kmeans(image_np, k)
            hex_clusters = [rgb_to_hex(tuple(cluster)) for cluster in clusters]
            all_clusters.append(hex_clusters)
            all_cluster_sizes.append(cluster_sizes)

        return all_clusters, all_cluster_sizes
    except Exception as e:
        raise
