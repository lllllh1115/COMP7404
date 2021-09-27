"""
To run this script, type

  python buyLotsOfFruit.py
  
Once you have correctly implemented the buyLotsOfFruit function,
the script should produce the output:

Cost of [('apples', 2.0), ('pears', 3.0), ('limes', 4.0)] is 12.25
"""

fruitPrices = {'apples':2.00, 'oranges': 1.50, 'pears': 1.75,
              'limes':0.75, 'strawberries':1.00}
import numpy as np
def buyLotsOfFruit(orderList):
    """
        orderList: List of (fruit, numPounds) tuples
            
    Returns cost of order
    """ 
    totalCost = 0.0
    for i in range(0, len(orderList)):
        if orderList[i][0] in fruitPrices:
            totalCost = totalCost + orderList[i][1]*fruitPrices[orderList[i][0]]
        else:
            print("There is a bug!")
            return None
    return totalCost
    
# Main Method    
if __name__ == '__main__':
    "This code runs when you invoke the script from the command line"
    orderList = [ ('apples', 2.0), ('pears', 3.0), ('limes', 4.0),('Nothing',5.0) ]
    print('Cost of', orderList, 'is', buyLotsOfFruit(orderList))