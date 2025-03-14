"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken, Katie Byers.
"""

from flask import Flask, render_template, redirect, flash, session, request
import jinja2

import melons
import customers

app = Flask(__name__)

# A secret key is needed to use Flask sessioning features
app.secret_key = 'this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.
app.jinja_env.undefined = jinja2.StrictUndefined

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melon_list = melons.get_all()
    return render_template("all_melons.html",
                           melon_list=melon_list)


@app.route("/melon/<melon_id>")
def show_melon(melon_id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = melons.get_by_id(melon_id)
    print(melon)
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/add_to_cart/<melon_id>")
def add_to_cart(melon_id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Melon successfully added to
    cart'."""

    # TODO: Finish shopping cart functionality

    # The logic here should be something like:
    #
    # - check if a "cart" exists in the session, and create one (an empty
    #   dictionary keyed to the string "cart") if not
    # - check if the desired melon id is the cart, and if not, put it in
    # - increment the count for that melon id by 1
    # - flash a success message
    # - redirect the user to the cart page


    if 'cart' not in session:
        session['cart'] = {}

    session['cart'][melon_id] = session['cart'].get(melon_id, 0) + 1 
    # print(melon)

    melon = melons.get_by_id(melon_id)

    flash(f'Successfully added {melon.common_name} to your cart!')

    # print(session['cart'])

    return redirect('/cart')


@app.route("/cart")
def show_shopping_cart():
    """Display content of shopping cart."""

    # TODO: Display the contents of the shopping cart.

    # The logic here will be something like:
    #
    # - get the cart dictionary from the session
    # - create a list to hold melon objects and a variable to hold the total
    #   cost of the order
    # - loop over the cart dictionary, and for each melon id:
    #    - get the corresponding Melon object
    #    - compute the total cost for that type of melon
    #    - add this to the order total
    #    - add quantity and total cost as attributes on the Melon object
    #    - add the Melon object to the list created above
    # - pass the total order cost and the list of Melon objects to the template
    #
    # Make sure your function can also handle the case wherein no cart has
    # been added to the session

    melons_in_cart = []
    order_tally = 0

    # if 'cart' not in session:
    #     session['cart'] = {}

    # From solution which is sleeker
    cart = session.get('cart', {})

    # for melon_id in session['cart']:
    for melon_id, quantity in cart.items():
        # Get melon ID and add quantity and total price
        melon = melons.get_by_id(melon_id)
        # melon.quantity = session['cart'][melon_id]
        melon.quantity = quantity
        melon.total_price = quantity * melon.price

        # Add the melon to the melons cart
        melons_in_cart.append(melon)

        # Add total to the order tally
        order_tally += melon.total_price
        print(f"this is the total price: {order_tally}")

    #     print(melon.common_name)
    # print(f"this is melons in cart {melons_in_cart}")
    # print(f"this is session['cart'] {session['cart']}")
    

    return render_template("cart.html", melons_in_cart=melons_in_cart,
                           tally=order_tally)


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    # TODO: Need to implement this!

    # The logic here should be something like:
    #
    # - get user-provided name and password from request.form
    # - use customers.get_by_email() to retrieve corresponding Customer
    #   object (if any)
    # - if a Customer with that email was found, check the provided password
    #   against the stored one
    # - if they match, store the user's email in the session, flash a success
    #   message and redirect the user to the "/melons" route
    # - if they don't, flash a failure message and redirect back to "/login"
    # - do the same if a Customer with that email doesn't exist


    email = request.form.get("email")

    if customers.get_by_email(email):
        customer = customers.get_by_email(email)
        
        # If password is correct
        if customer.is_correct_password(request.form.get("password")) :
            session['logged_in_customer_email'] = email
            flash("Login Successful!")

            return redirect('/melons')
        
        # If password is incorrect
        else: 
            flash("Incorrect password.")
            return redirect('/login')
        
    else:
        flash("No customer with that email found.")
        return redirect('/login')


@app.route("/logout")
def process_logout():
    """Log the customer out of their session"""

    session['logged_in_customer_email'] = None

    flash("Logged out")

    return redirect('/melons')
    


@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=6061)
