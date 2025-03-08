"""Customers at Hackbright."""


class Customer:
    """Ubermelon customer."""

    # TODO: need to implement this
    def __init__(self, f_name, l_name, email, password):
        """Initialize customer"""
        self.f_name = f_name
        self.l_name = l_name
        self.email = email
        self.password = hash(password)

    
    def __repr__(self):
        """Print first name and email of customer"""

        return (f"Customer name: {self.f_name}, email: {self.email}")
    

    def is_correct_password(self, password):
        """Check if the input password matches the saved hashed password"""

        return hash(password) == self.password


def get_by_email(email):
    """Return the Customer object attached to the input email"""

    if email in customers:
        return customers[email]


    
def read_customers(filepath='customers.txt'):
    """Input the customers from text file into dictionary
    
        Dictionary will be {email: Customer object}
    """

    customers = {}

    with open(filepath, 'r') as file:
        for line in file:
            # Save each element into the relevant variables
            (
                f_name,
                l_name,
                email,
                password
            ) = line.strip().split('|')

            # Create the dict key value using the class
            customers[email] = Customer(f_name, l_name, email, password)

    return customers

customers = read_customers()



