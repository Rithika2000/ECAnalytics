import pypyodbc as odbc
from faker import Faker
import random
import decimal
import datetime
from datetime import timedelta



# Initialize Faker to generate random data
fake = Faker()

DRIVER_NAME = "SQL SERVER"
SERVER_NAME = "LAPTOP-QDKVIQOK\SQLEXPRESS"
DATABASE_NAME = "ecanalytics"

connection_string = f"""
   DRIVER={{{DRIVER_NAME}}};
   SERVER={SERVER_NAME};
   DATABASE={DATABASE_NAME};
   Trust_Connection=yes;
"""

def delete_insert_data(connection, cursor):
    cursor.execute("DELETE FROM dbo.Address;")
    cursor.execute("DELETE FROM dbo.Payment;")
    cursor.execute("DELETE FROM dbo.Orders;")
    cursor.execute("DELETE FROM dbo.Shipper;")
    cursor.execute("DELETE FROM dbo.Sellers;")
    cursor.execute("DELETE FROM dbo.Wishlist;")
    cursor.execute("DELETE FROM dbo.ShoppingCart;")
    cursor.execute("DELETE FROM dbo.Offer;")
    cursor.execute("DELETE FROM dbo.Discount;")
    cursor.execute("DELETE FROM dbo.Rating;")
    cursor.execute("DELETE FROM dbo.Product;")
    cursor.execute("DELETE FROM dbo.Category;")
    cursor.execute("DELETE FROM dbo.Buyers;")
    cursor.execute("DELETE FROM dbo.Membership;")
    cursor.execute("DELETE FROM dbo.Users;")
    connection.commit()
    
    def randomly_weighted_random_date(start_year, end_year):
        weights = [random.uniform(0.5, 1.5) for _ in range(start_year, end_year + 1)]  # Random weights for each year
        selected_year = random.choices(range(start_year, end_year + 1), weights=weights, k=1)[0]
        
        current_year = datetime.datetime.now().year
        start_date = datetime.date(selected_year, 1, 1)
        end_date = datetime.date(selected_year, 12, 31) if selected_year != current_year else datetime.datetime.now().date()

        return fake.date_between(start_date=start_date, end_date=end_date)
    
    def non_uniform_random_quantity(min_value, max_value):
        if random.random() < 0.5:  # 50% chance to choose lower range
            return random.randint(min_value, max_value // 2)
        else:  # 50% chance to choose the full range
            return random.randint(min_value, max_value)

    # Insert new data into Users
    existing_names = set()
    for _ in range(15000):  # Assuming we want to create 100 random users
        user_fname = fake.first_name()
        user_lname = fake.last_name()
        if (user_fname, user_lname) not in existing_names:
            existing_names.add((user_fname, user_lname))

            user_id = 'US' + fake.unique.lexify(text='??????', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
            user_type = random.choice(['B', 'S'])  # Assuming these are your user types
            password = fake.password()
            date_created = randomly_weighted_random_date(2018, 2023)

            cursor.execute(
                "INSERT INTO dbo.Users (UserID, UserFName, UserLName, USER_TYPE, Password, DateCreated) VALUES (?, ?, ?, ?, ?, ?);",
                (user_id, user_fname, user_lname, user_type, password, date_created)
            )
    
    # Insert new data into Membership
    membership_types = ['Student', 'Gold', 'Platinum']
    for _ in range(10):  # Assuming we want to create 50 random memberships
        membership_id = 'ME' + fake.unique.lexify(text='??????', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
        membership_type = fake.random_element(elements=membership_types)

        cursor.execute(
            "INSERT INTO dbo.Membership (MembershipID, MembershipType) VALUES (?, ?);",
            (membership_id, membership_type)
        )
    
    # Insert new data into Buyers
    cursor.execute("SELECT UserID FROM dbo.Users WHERE USER_TYPE = 'B';")
    user_ids = [row[0] for row in cursor.fetchall()]  # Accessing by index

    cursor.execute("SELECT MembershipID FROM dbo.Membership;")
    membership_ids = [row[0] for row in cursor.fetchall()]
    
    used_user_ids = set()

    for _ in range(len(user_ids)):  # Insert a buyer for each 'B' type user
        while True:
            user_id = random.choice(user_ids)
            if user_id not in used_user_ids:
                used_user_ids.add(user_id)
                break
        buyer_id = 'BU' + fake.unique.lexify(text='??????', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
        user_type = 'B'  # As per your CHECK constraint
        membership_id = random.choice(membership_ids)
        phone = fake.phone_number()
        phone = phone[:15]
        email = fake.email()

        cursor.execute(
            "INSERT INTO dbo.Buyers (BuyerID, UserID, USER_TYPE, MembershipID, Phone, Email) VALUES (?, ?, ?, ?, ?, ?);",
            (buyer_id, user_id, user_type, membership_id, phone, email)
        )

    # Insert new data into Categories
    categories = {
        'Men': {
            'Topwear': ['T-Shirts', 'Casual Shirts', 'Formal Shirts', 'Sweatshirts', 'Sweaters', 'Jackets', 'Blazers & Coats', 'Suits', 'Rain Jackets'],
            'Bottomwear': ['Jeans', 'Casual Trousers', 'Formal Trousers', 'Shorts', 'Track Pants & Joggers'],
            'Footwear': ['Casual Shoes', 'Sports Shoes', 'Formal Shoes', 'Sneakers', 'Sandals & Floaters', 'Flip Flops', 'Socks'],
            'Innerwear & Sleepwear': ['Briefs & Trunks', 'Boxers', 'Vests', 'Sleepwear & Loungewear', 'Thermals']
        },
        'Women': {
            'Western Wear': ['Dresses', 'Tops', 'Tshirts', 'Jeans', 'Trousers & Capris', 'Shorts & Skirts', 'Co-ords' 'Playsuits', 'Jumpsuits', 'Shrugs', 'Sweaters & Sweatshirts', 'Jackets & Coats', 'Blazers & Waistcoats'],
            'Lingerie & Sleepwear': ['Bra', 'Briefs', 'Shapewear', 'Sleepwear & Loungewear', 'Swimwear', 'Camisoles & Thermals'],
            'Footwear': ['Flats', 'Casual Shoes', 'Heels', 'Boots', 'Sports Shoes & Floaters'],
            'Jewellery': ['Fashion Jewellery', 'Fine Jewellery', 'Earrings']
        }
    }

    for _ in range(20):  # Assuming we want to create 10 random Category
        Main_Category = fake.random_element(elements=('Men', 'Women'))
        Category = fake.random_element(elements=list(categories[Main_Category].keys()))
        Sub_Categories = categories[Main_Category][Category]

        # Insert each sub-category as a separate row
        for Sub_Category in Sub_Categories:
            category_id = 'CA' + fake.unique.lexify(text='??????', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
            cursor.execute(
                "INSERT INTO dbo.Category (CategoryID, MainCategory, Category, SubCategory) VALUES (?, ?, ?, ?);",
                (category_id, Main_Category, Category, Sub_Category)
            )


    # Insert new data inro Products
    cursor.execute("SELECT CategoryID FROM dbo.Category;")
    Category_ids = [row[0] for row in cursor.fetchall()]

    brand_names = [
        "Gucci", "Prada", "Louis Vuitton", "Chanel", "Armani", "Versace", "Dolce & Gabbana", "Burberry", "Hermes", "Fendi",
        "Balenciaga", "Saint Laurent", "Givenchy", "Valentino", "Dior", "Ralph Lauren", "Tommy Hilfiger", "Calvin Klein", "Michael Kors", "Tory Burch",
        "Coach", "Kate Spade", "Alexander McQueen", "Marc Jacobs", "Stella McCartney", "Jimmy Choo", "Christian Louboutin", "Manolo Blahnik", "Hugo Boss", "Kenzo",
        "Moschino", "Balmain", "Zara", "H&M", "Uniqlo", "Gap", "Levi's", "Diesel", "Lacoste", "Ted Baker",
        "Vivienne Westwood", "Off-White", "Moncler", "Stone Island", "Bape", "Supreme", "Paul Smith", "Ermenegildo Zegna", "Max Mara", "Comme Des Garçons"
    ]


    for _ in range(5000):  # Insert 5000 random products
        product_id = 'PR' + fake.unique.lexify(text='??????', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
        category_id = random.choice(Category_ids)
        product_brand = random.choice(brand_names)  # Select a brand name randomly
        quantity = random.randint(1, 100)
        unit_price = decimal.Decimal(f"{random.uniform(0.99, 999.99):.2f}")
        units_in_stock = non_uniform_random_quantity(0, 50)
        units_in_order = non_uniform_random_quantity(0, 20)
        date = randomly_weighted_random_date(2018, 2023)

        cursor.execute(
            "INSERT INTO dbo.Product (ProductID, CategoryID, ProductBrand, Quantity, UnitPrice, UnitsInStock, UnitsInOrder, Date) VALUES (?, ?, ?, ?, ?, ?, ?, ?);",
            (product_id, category_id, product_brand, quantity, unit_price, units_in_stock, units_in_order, date)
        )

    
    # Insert new data into Ratings
    cursor.execute("SELECT UserID FROM dbo.Users;")
    user_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT ProductID FROM dbo.Product;")
    product_ids = [row[0] for row in cursor.fetchall()]

    for _ in range(1000):  # Insert 100 random reviews
        rating_id = 'RA' + fake.unique.lexify(text='??????', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
        user_id = random.choice(user_ids)
        product_id = random.choice(product_ids)
        rating = random.randint(1, 5)  # Assuming rating is on a scale of 1 to 5

        cursor.execute(
            "INSERT INTO dbo.Rating (RatingID, UserID, ProductID, Rating) VALUES (?, ?, ?, ?);",
            (rating_id, user_id, product_id, rating)
        )
    
    # Insert new data into Discount
    for _ in range(50):  # Insert 20 random discounts
        discount_id = 'DI' + fake.unique.lexify(text='??????', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')

        # Generate a random discount percentage between 0.00 and 100.00
        discount_percent = round(random.uniform(0, 90), 2)
        discount_percent = decimal.Decimal(discount_percent).quantize(decimal.Decimal('0.00'))

        cursor.execute(
            "INSERT INTO dbo.Discount (DiscountID, DiscountPrecent) VALUES (?, ?);",
            (discount_id, discount_percent)
        )
    
    # Insert new data into Offer
    cursor.execute("SELECT ProductID FROM dbo.Product;")
    product_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT DiscountID FROM dbo.Discount;")
    discount_ids = [row[0] for row in cursor.fetchall()]

    for _ in range(300):  # Insert 30 random offers
        offer_id = 'OF' + fake.unique.lexify(text='??????', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
        product_id = random.choice(product_ids)
        discount_id = random.choice(discount_ids)

        cursor.execute(
            "INSERT INTO dbo.Offer (OfferID, ProductID, DiscountID) VALUES (?, ?, ?);",
            (offer_id, product_id, discount_id)
        )
    
    # Insert new data into Shopping Cart
    cursor.execute("SELECT UserID FROM dbo.Users;")
    user_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT ProductID FROM dbo.Product;")
    product_ids = [row[0] for row in cursor.fetchall()]

    for _ in range(2000):  # Insert 50 random shopping cart items
        shopping_cart_id = 'SC' + fake.unique.lexify(text='??????', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
        user_id = random.choice(user_ids)
        product_id = random.choice(product_ids)
        item_quantity = random.randint(1, 100)
        item_status = random.choice(['Available', 'Out of Stock'])  # Random order status
        Shopping_status = random.choice(['Order Placed', 'Order Pending'])

        cursor.execute(
            "INSERT INTO dbo.[ShoppingCart] (ShoppingCartID, UserID, ProductID, ItemQuantity, ItemStatus, ShoppingStatus) VALUES (?, ?, ?, ?, ?, ?);",
            (shopping_cart_id, user_id, product_id, item_quantity, item_status, Shopping_status)
        )
    
    # Insert new data in Wishlist
    cursor.execute("SELECT UserID FROM dbo.Users;")
    user_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT ProductID FROM dbo.Product;")
    product_ids = [row[0] for row in cursor.fetchall()]

    for _ in range(2000):  # Insert 100 random wishlist items
        wishlist_id = 'WL' + fake.unique.lexify(text='??????', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
        user_id = random.choice(user_ids)
        product_id = random.choice(product_ids)

        cursor.execute(
            "INSERT INTO dbo.Wishlist (WishlistID, UserID, ProductID) VALUES (?, ?, ?);",
            (wishlist_id, user_id, product_id)
        )

    # Insert new data into Sellers
    cursor.execute("SELECT UserID FROM dbo.Users WHERE USER_TYPE = 'S';")
    user_ids = [row[0] for row in cursor.fetchall()]

    for user_id in user_ids:  # Use existing UserIDs with USER_TYPE 'S'
        seller_id = 'SE' + fake.unique.lexify(text='??????', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
        company_name = fake.company()
        phone = fake.phone_number()[:15]
        email = fake.email()

        cursor.execute(
            "INSERT INTO dbo.Sellers (SellerID, UserID, USER_TYPE, CompanyName, Phone, Email) VALUES (?, ?, 'S', ?, ?, ?);",
            (seller_id, user_id, company_name, phone, email)
        )

    # Insert new data into Shipper
    for _ in range(100):  # Insert 20 random shippers
        shipper_id = 'SH' + fake.unique.lexify(text='??????', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
        shipper_name = fake.company()
        contact_name = fake.name()
        phone = fake.phone_number()[:15]

        cursor.execute(
            "INSERT INTO dbo.Shipper (ShipperID, ShipperName, ContactName, Phone) VALUES (?, ?, ?, ?);",
            (shipper_id, shipper_name, contact_name, phone)
        )
    
    # Insert new data into Orders
    cursor.execute("SELECT UserID FROM dbo.Users;")
    user_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT ShipperID FROM dbo.Shipper;")
    shipper_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT ShoppingCartID FROM dbo.ShoppingCart;")
    shopping_cart_ids = [row[0] for row in cursor.fetchall()]

    for _ in range(2000):  # Insert 50 random orders
        order_id = 'OR' + fake.unique.lexify(text='??????', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
        user_id = random.choice(user_ids)
        shipper_id = random.choice(shipper_ids)
        shopping_cart_id = random.choice(shopping_cart_ids)
        order_date = randomly_weighted_random_date(2018, 2023)

        order_status = random.choice(['Pending', 'Completed', 'Cancelled'])
        amount = random.randint(100, 5000)

        cursor.execute(
            "INSERT INTO dbo.Orders (OrderID, UserID, ShipperID, ShoppingCartID, OrderDate, OrderStatus, Amount) VALUES (?, ?, ?, ?, ?, ?, ?);",
            (order_id, user_id, shipper_id, shopping_cart_id, order_date, order_status, amount)
        )
    
    # Insert into Payment
    cursor.execute("SELECT OrderID FROM dbo.Orders;")
    order_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT OfferID FROM dbo.Offer;")
    offer_ids = [row[0] for row in cursor.fetchall()]

    for order_id in order_ids:  # One payment per order
        payment_id = 'PA' + fake.unique.lexify(text='??????', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
        payment_type = random.choice(['Cash', 'Card'])
        offer_id = random.choice(offer_ids)
        invoice_amount = decimal.Decimal(f"{random.uniform(0.99, 999.99):.2f}")
        payment_status = random.choice(['Awaiting Payment', 'Payment Received', 'Processing', 'Shipped', 'In Transit', 'Out for Delivery', 'Delivered', 'Cancelled'])

        cursor.execute(
            "INSERT INTO dbo.Payment (PaymentID, OrderID, Payment_Type, OfferID, InvoiceAmount, PaymentStatus) VALUES (?, ?, ?, ?, ?, ?);",
            (payment_id, order_id, payment_type, offer_id, invoice_amount, payment_status)
        )

    
    # Insert new data into Address
    cursor.execute("SELECT UserID FROM dbo.Users;")
    user_ids = [row[0] for row in cursor.fetchall()]

    for user_id in user_ids:
        address_id = 'AD' + fake.unique.lexify(text='??????', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
        address_type = random.choice(['Home', 'Work', 'Other'])
        address_line1 = fake.street_address()
        city = fake.city()
        province = fake.state()
        country = fake.country()[:45]
        postal_code = fake.postcode()

        cursor.execute(
            "INSERT INTO dbo.Address (AddressID, UserID, Address_Type, AddressLine1, City, Province, Country, PostalCode) VALUES (?, ?, ?, ?, ?, ?, ?, ?);",
            (address_id, user_id, address_type, address_line1, city, province, country, postal_code)
        )


    # Commit the new data to the database
    connection.commit()

# Main execution
if __name__ == "__main__":
    # Establish a connection to your database
    with odbc.connect(connection_string) as conn:
        with conn.cursor() as cursor:
            delete_insert_data(conn, cursor)
    
    print("Database has been refreshed with new data.")
