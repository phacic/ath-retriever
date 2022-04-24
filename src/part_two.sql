#
# Find all customers in Berlin 

SELECT * FROM Customers
WHERE City="Berlin";

#
# Find all customers in Mexico City

SELECT * FROM Customers
WHERE City="México D.F.";


#
# Find avg price of all products
SELECT AVG(Price) AS AveragePrice FROM Products;


#
# Find number of products that Have price = 18
SELECT Count(ProductID) AS NumberOfProducts
FROM Products
WHERE Price="18";

#
# Find orders between 1996-08-01 and 1996-09-06
SELECT * FROM [Orders]
WHERE OrderDate > "1996-08-01" AND OrderDate < "1996-09-06";

#
# Find customers with more than 3 orders
SELECT Customers.*,  COUNT() AS TotalOrders 
    FROM Customers INNER JOIN Orders ON Customers.customerid=Orders.CustomerID 
    GROUP BY Customers.customerid HAVING TotalOrders > 3


#
# Find all customers that are from the same city
SELECT DISTINCT City, Group_Concat(c.customerId) as CustomerIDs FROM Customers c GROUP BY City
