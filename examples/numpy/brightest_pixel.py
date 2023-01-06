import numpy as np

def find_brightest_pixels(image: np.ndarray) -> List[Tuple[int, int]]:
    # Find the indices of the brightest pixels
    row_indices, col_indices = np.where(image == np.amax(image))
    
    # Zip the row and col indices into a list of tuples
    brightest_pixels = list(zip(row_indices, col_indices))
    
    return brightest_pixels
