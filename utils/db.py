import math
import random


def get_random_indeces(max_range: int, seed="seed", limit=50, padding=0) -> list:
    """
    generate paginted pseudo random indeces

    :param max_range: length of the list to be scanned for random indeces
    :param seed: seed for the random function (needed for pagination)
    :param limit: maximum number of indeces
    :param padding: amount of padding before evaluating indeces
    :return: list of pseudo random indeces
    """
    # initiate random seed
    random.seed(a=seed)

    def phi(n: int) -> list:
        """
        return all coprime number of n (Euler totient)

        :param n: number to evaluate coprime against
        :return: list of coprime number of n
        """
        return_value = []
        for k in range(1, n + 1):
            if math.gcd(n, k) == 1:
                return_value.append(k)
        return return_value

    def get_random_step(length: int) -> int:
        """
        get a random value coprime with the length of the range to scan

        :param length:
        :return: a random coprime number of the length that can be used a step in the
        """
        p = phi(length)
        return p[random.randint(0, len(p)-1)]

    # set offset from seed
    offset = random.randint(0, max_range)
    # get a random step from seed (coprime with max_range)
    step = get_random_step(max_range)
    # set the starting index to padding if provided, 0 otherwise
    index = padding if padding else 0

    # build list of random indeces
    indeces = []
    for i in range(index, index + limit):
        indeces.append(((i * step + offset) % max_range) + 1)

    return indeces
