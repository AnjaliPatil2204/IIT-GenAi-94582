#Q3:Given a CSV file Products.csv with columns: Write a Python program to:
#a) Read the CSV
#b) Print each row in a clean format
#c) Total number of rows
#d) Total number of products priced above 500
#e) Average price of all products
#f) List all products belonging to a specific category (user input)
#g) Total quantity of all items in stock
import pandas as pd
# a) Read the CSV
df = pd.read_csv('Products.csv')

# b) Print each row in a clean format
for index, row in df.iterrows():
    print(f"ProductID: {row['product_id']}")
    print(f"ProductName: {row['product_name']}")
    print(f"Category: {row['category']}")
    print(f"Price: {row['price']}")
    print(f"Quantity: {row['quantity']}")
    print("-" * 40)
# c) Total number of rows
total_rows = len(df)
print(f"Total number of rows: {total_rows}")

# d) Total number of products priced above 500
products_above_500 = df[df['price'] > 500]
total_above_500 = len(products_above_500)
print(f"Total number of products priced above 500: {total_above_500}")

# e) Average price of all products
average_price = df['price'].mean()
print(f"Average price of all products: {average_price}")

# f) List all products belonging to a specific category (user input)
category_input = input("Enter a category to filter products: ")
filtered_products = df[df['category'].str.lower() == category_input.lower()]

print(f"Products in category '{category_input}':")
for index, row in filtered_products.iterrows():
    print(f"ProductID: {row['product_id']}")
    print(f"ProductName: {row['product_name']}")
    print(f"Category: {row['category']}")
    print(f"Price: {row['price']}")
    print(f"Quantity: {row['quantity']}")
    print("-" * 40)
# g) Total quantity of all items in stock
total_quantity = df['quantity'].sum()
print(f"Total quantity of all items in stock: {total_quantity}")
