"""
Here's the intended output of this script, once you fill it in:

Welcome to shop1 fruit shop
Welcome to shop2 fruit shop
For orders:  [('apples', 1.0), ('oranges', 3.0)] best shop is shop1
For orders:  [('apples', 3.0)] best shop is shop2
"""

import shop
import numpy

def shopSmart(orderList, fruitShops):
    """
        orderList: List of (fruit, numPound) tuples
        fruitShops: List of FruitShops
    """
    totalPrice = [0] * len(fruitShops)
    for i in range(0, len(fruitShops)):
        totalPrice[i] = totalPrice[i] + fruitShops[i].getPriceOfOrder(orderList)
        Ind = totalPrice.index(min(totalPrice))
    return fruitShops[Ind]
    
def shopArbitrage(orderList, fruitShops):
    """
    input: 
        orderList: List of (fruit, numPound) tuples
        fruitShops: List of FruitShops
    output:
        maximum profit in amount
    """
    profitprice = 0
    price = []
    for i in range(0, len(orderList)):
        for j in range(0, len(fruitShops)):
            price =  price + [fruitShops[j].fruitPrices[orderList[i][0]]]
        profitprice = profitprice + orderList[i][1]* (max(price)-min(price))
    return profitprice

def shopMinimum(orderList, fruitShops):
    """
    input: 
        orderList: List of (fruit, numPound) tuples
        fruitShops: List of FruitShops
    output:
        Minimun cost of buying the fruits in orderList
    """
    profitprice = 0
    price = []
    for i in range(0, len(orderList)):
        for j in range(0, len(fruitShops)):
            price = price + [fruitShops[j].fruitPrices[orderList[i][0]]]
        profitprice = profitprice + orderList[i][1] *  min(price)
    return profitprice

if __name__ == '__main__':
  "This code runs when you invoke the script from the command line"
  orders = [('apples',1.0), ('oranges',3.0)]
  dir1 = {'apples': 2.0, 'oranges':1.0}
  shop1 =  shop.FruitShop('shop1',dir1)
  dir2 = {'apples': 1.0, 'oranges': 5.0}
  shop2 = shop.FruitShop('shop2',dir2)
  shops = [shop1, shop2]
  print("For orders ", orders, ", the best shop is", shopSmart(orders, shops).getName())
  orders = [('apples',3.0)]
  print("For orders: ", orders, ", the best shop is", shopSmart(orders, shops).getName())
