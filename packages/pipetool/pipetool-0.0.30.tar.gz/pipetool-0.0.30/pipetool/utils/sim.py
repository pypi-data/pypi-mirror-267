import numpy as np
# cos相似度
def cos_sim(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity between two vectors.

    :param a: The first vector.
    :param b: The second vector.
    :return: Cosine similarity between two vectors.
    """
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

