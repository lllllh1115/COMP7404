"""
Run python autograder.py 
"""


def average(priceList):
    """Return the average price of a set of fruit"""
    """*** YOUR CODE HERE ***"""
    pricelista = set(priceList)
    return sum(pricelista) / len(pricelista)
