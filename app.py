import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from re import fullmatch
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Gets user id
    uid = session["user_id"]

    # Sets dictionary with the data which will get set in the template
    stockUserData = {
        "symbol": [],
        "price": [],
        "amount": [],
        "worthTotal": []
    }

    # Queries database to get all owned stocks
    stocksQuery = db.execute("SELECT StockSymbol, StockAmount FROM OwnedStocks WHERE PersonID=? ORDER BY StockSymbol ASC", uid)

    # If the user doesn't own any stocks it renders newUser.html
    if len(stocksQuery) == 0:
        return render_template("newUser.html")

    # Sets variables in the dictionary
    totalWorthStocks = 0
    for stockQuery in stocksQuery:
        stockSymbol = stockQuery["StockSymbol"]
        stockAmount = int(stockQuery["StockAmount"])

        # Looks up the price of the stock
        priceLookup = lookup(stockSymbol)
        stockPrice = int(priceLookup["price"])

        # Gets the worth of the stock and all of the stocks combined
        stockWorthTotal = stockPrice * stockAmount
        totalWorthStocks += stockWorthTotal

        # Adds variables to the dictionary
        stockUserData["symbol"].append(stockSymbol)
        stockUserData["price"].append(usd(stockPrice))
        stockUserData["amount"].append(stockAmount)
        stockUserData["worthTotal"].append(usd(stockWorthTotal))

    # Gets the amount of different stocks that the user owns
    amountDifferentStocks = len(stockUserData["symbol"])

    # Queries the database for the amount of cash that the user has
    cashQuery = db.execute("SELECT cash FROM users WHERE id=?", uid)
    cash = cashQuery[0]["cash"]

    # Renders portfolio.html with the data gathered above
    return render_template("portfolio.html", amountDifferentStocks=amountDifferentStocks, stockUserData=stockUserData, cash=usd(cash), totalWorthStocks=usd(totalWorthStocks))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        # Gets form data
        stockSymbol = request.form.get("symbol").upper()

        # Verifies user input
        try:
            stockAmount = int(request.form.get("shares"))
        except:
            return apology("Stock amount isn't an integer", 400)
        if not stockSymbol:
            return apology("Must provide stock symbol", 400)
        elif not stockAmount:
            return apology("Must provide stock amount", 400)

        # Looks up stock data
        resultLookup = lookup(stockSymbol)

        # Checks if the stock symbol is valid
        if resultLookup == None:
            return apology("Stock symbol not found", 400)

        # Checks if the user put in a positive number as stock amount
        if stockAmount < 1:
            return apology("Amount of shares must be larger than 0", 400)

        # Calculates transaction amount
        stockPrice = resultLookup["price"]
        transactionAmount = stockPrice * stockAmount

        # Calculates cash in bank account of the user
        uid = session["user_id"]
        resultCashDBQuery = db.execute("SELECT cash FROM users WHERE id=?", uid)

        # Checks if query was successful
        if len(resultCashDBQuery) != 1:
            return apology("User not found", 400)

        # Calculates remaining cash
        cash = int(resultCashDBQuery[0]["cash"])
        cashLeft = cash - transactionAmount

        # Checks if theres enough money for the transaction
        if cashLeft < 0:
            return apology("Not enough money in your account", 400)

        # Adds the transaction into transaction database
        transferDate = datetime.now()
        transferType = "buy"
        db.execute("INSERT INTO Purchases (StockPrice, StockAmount, StockSymbol, TransferAmount, TransferDate, TransferType, PersonID) VALUES (?,?,?,?,?,?,?);", stockPrice, stockAmount, stockSymbol, transactionAmount, transferDate, transferType, uid)

        # Updates the cash that the user has in their account
        db.execute("UPDATE users SET cash=? WHERE id=?;", cashLeft, uid)

        # Gets the stockAmount that the user already had in their account
        resultStockQuery = db.execute("SELECT StockAmount FROM OwnedStocks WHERE PersonID=? AND StockSymbol=?", uid, stockSymbol)

        # Checks if the query returned anything
        resultStockQueryLen = len(resultStockQuery)
        if resultStockQueryLen == 1:
            queryStockAmount = int(resultStockQuery[0]["StockAmount"])
            newStockAmount = queryStockAmount + stockAmount

            # Removes the existing row in database and replaces it with the updated stock amount
            db.execute("DELETE FROM OwnedStocks WHERE PersonID=? AND StockSymbol=?;", uid, stockSymbol)
            db.execute("INSERT INTO OwnedStocks (PersonID, StockSymbol, StockAmount) VALUES (?,?,?);", uid, stockSymbol, newStockAmount)
        else:
            # Adds new row into database with the stock amount
            db.execute("INSERT INTO OwnedStocks (PersonID, StockSymbol, StockAmount) VALUES (?,?,?);", uid, stockSymbol, stockAmount)

        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # Gets user id
    uid = session["user_id"]

    # Gets purchase history of the user
    purchaseHistoryQuery = db.execute("SELECT StockSymbol, StockAmount, StockPrice, TransferDate, TransferType FROM Purchases WHERE PersonID=? ORDER BY TransferDate DESC;", uid)

    # Checks if the user hasn't made any purchases
    if len(purchaseHistoryQuery) == 0:
        return render_template("noHistory.html")

    # Renders table with purchase data
    return render_template("history.html", purchaseHistory=purchaseHistoryQuery)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        # Gets form data
        stockSymbol = request.form.get("symbol").upper()

        # Verifies user input
        if not stockSymbol:
            return apology("Must provide stock symbol", 400)

        # Lookup of the stockSymbol
        resultLookup = lookup(stockSymbol)

        # Checks if the lookup was unsuccessful
        if resultLookup == None:
            return apology("Stock symbol not found", 400)
        else:
            # Renders webpage with table of stockdata
            return render_template("quoted.html", stockname=resultLookup["name"], stockprice=usd(resultLookup["price"]), stocksymbol=stockSymbol)

    else:
        # Shows form
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Gets form data
        username = request.form.get('username')
        password = request.form.get('password')
        passwordConfirmation = request.form.get('confirmation')
        regEx = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"

        # Verifies user input
        if not username:
            return apology("Must provide username", 400)
        elif not password:
            return apology("Must provide password", 400)
        elif not passwordConfirmation:
            return apology("Must repeat your password", 400)
        elif passwordConfirmation != password:
            return apology("Passwords don't match", 400)
        elif not fullmatch(regEx, password):
            return apology("Password must be at least 8 characters and use at least one digit, special character, lower and uppercase English letter", 400)
        else:
            # Hashes password
            pwHash = generate_password_hash(password)

            # Adds user to database
            db.execute("INSERT or IGNORE INTO users (username, hash) VALUES (?, ?);", username, pwHash)

            rows = db.execute("SELECT * FROM users WHERE username =? AND hash=?;", username, pwHash)
            if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
                return apology("This username has already been taken", 400)

            # Sets session
            session["user_id"] = rows[0]["id"]
            return redirect("/")
    else:
        return render_template("registration.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        # Gets user id
        uid = session["user_id"]

        # Gets form data
        stockSymbol = request.form.get("symbol")

        # Verifies user input
        try:
            sharesAmount = int(request.form.get("shares"))
        except:
            return apology("Shares amount isn't an integer", 400)

        if not stockSymbol:
            return apology("Must provide stock symbol", 400)
        elif not sharesAmount:
            return apology("Must provide an amount of shares", 400)
        elif sharesAmount < 1:
            return apology("Amount of shares must be larger than 1", 400)

        # Queries database for amount of owned shares
        checkOwnedStocksQuery = db.execute("SELECT StockAmount FROM OwnedStocks WHERE PersonID=? AND StockSymbol=?", uid, stockSymbol)

        # Checks if the user has any shares
        if len(checkOwnedStocksQuery) != 1:
            return apology("You can't sell something which you don't own", 400)

        # Calculates how many shares the user has left after selling
        ownedStockAmount = int(checkOwnedStocksQuery[0]["StockAmount"])
        ownedStockAmountLeft = ownedStockAmount - sharesAmount

        # Checks if the user doesn't have enough shares
        if ownedStockAmountLeft < 0:
            return apology("You can't sell more stocks than you own", 400)

        # Adds the transaction into transaction database
        transferDate = datetime.now()
        transferType = "sell"
        stockPriceQuery = lookup(stockSymbol)
        stockPrice = stockPriceQuery["price"]
        transactionAmount = stockPrice * sharesAmount

        db.execute("INSERT INTO Purchases (StockPrice, StockAmount, StockSymbol, TransferAmount, TransferDate, TransferType, PersonID) VALUES (?,?,?,?,?,?,?);", stockPrice, sharesAmount, stockSymbol, transactionAmount, transferDate, transferType, uid)

        # Gets the amount of cash that the user has in their account
        cashQuery = db.execute("SELECT cash FROM users WHERE id=?", uid)
        cash = cashQuery[0]["cash"]
        cashLeft = cash + transactionAmount

        # Updates the cash that the user has in their account
        db.execute("UPDATE users SET cash=? WHERE id=?;", cashLeft, uid)

        # Removes the existing row in database and replaces it with the updated stock amount
        if ownedStockAmountLeft != 0:
            db.execute("DELETE FROM OwnedStocks WHERE PersonID=? AND StockSymbol=?;", uid, stockSymbol)
            db.execute("INSERT INTO OwnedStocks (PersonID, StockSymbol, StockAmount) VALUES (?,?,?);", uid, stockSymbol, ownedStockAmountLeft)
        else:
            db.execute("DELETE FROM OwnedStocks WHERE PersonID=? AND StockSymbol=?;", uid, stockSymbol)

        return redirect("/")
    else:
        # Gets user id
        uid = session["user_id"]

        # Queries the database to get all of the owned stock symbols
        symbols = db.execute("SELECT StockSymbol FROM OwnedStocks WHERE PersonID=? ORDER BY StockSymbol ASC", uid)

        # Checks if the user has stocks
        if len(symbols) == 0:
            return render_template("noStocks.html")

        return render_template("sell.html", symbols=symbols)