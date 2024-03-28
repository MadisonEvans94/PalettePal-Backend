# test_image_processing.py
# from utils import image  # Assuming your image.py is inside a utils directory
from image_utils import image
import matplotlib.pyplot as plt


def main():
    client_request = image.simulate_image_upload("./assets/test-image.png")
    clusters = image.process_clusters(client_request["image"], 3)
    print(clusters)


if __name__ == "__main__":
    main()
