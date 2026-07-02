from flask import Flask, render_template, request,session,redirect,url_for,flash
import mysql.connector

app = Flask(__name__)
app.secret_key="library123"

# MySQL Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Iswarya@2006",
    database="library_db"
)

cursor = conn.cursor()

# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Registration Page
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        department = request.form["department"]
        password = request.form["password"]

        query = """
        INSERT INTO students(name, email, department, password)
        VALUES(%s, %s, %s, %s)
        """

        values = (name, email, department, password)

        cursor.execute(query, values)
        conn.commit()

        flash("✅Registration Successful! Please Login")
        return redirect(url_for("login"))

    return render_template("register.html")


# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        query = """
        SELECT * FROM students
        WHERE email=%s AND password=%s
        """

        values = (email, password)

        cursor.execute(query, values)

        user = cursor.fetchone()

        if user:
            session["name"]=user[1]
            return redirect(url_for("dashboard"))

        else:
            return "Invalid Email or Password!"

    return render_template("login.html")



@app.route("/dashboard")
def dashboard():
    
    if "name" not in session:
        return redirect(url_for("login"))
    cursor.execute("select count(*) from books")  
    Total_books=cursor.fetchone()
    cursor.execute("select sum(quantity) from books")
    Total=cursor.fetchone()

    
    return render_template("dashboard.html",  name=session["name"],Titles=Total_books[0],Copies=Total[0] )

@app.route("/add_book", methods=["GET", "POST"])
def add_book():

    if request.method == "POST":

        title = request.form["title"]
        author = request.form["author"]
        quantity = request.form["quantity"]

        query = """
        INSERT INTO books(title, author, quantity)
        VALUES(%s, %s, %s)
        """

        values = (title, author, quantity)

        cursor.execute(query, values)
        conn.commit()

        flash("📚Book Added Successfully!")
        return redirect(url_for("view_books"))

    return render_template("add_book.html")    

@app.route("/view_books")
def view_books():
    if "name" not in session:
        return redirect(url_for("login"))

    cursor.execute( "SELECT * FROM books")

    books = cursor.fetchall()

    return render_template("view_books.html", books=books)

@app.route("/delete_book/<int:id>") 
def delete_book(id):
  
    query = "DELETE FROM books WHERE book_id=%s"

    cursor.execute(query, (id,))
    conn.commit()

    flash("🗑️Book Deleted Successfully!")
    return(url_for("view_books"))
    
@app.route("/update_book/<int:id>", methods=["GET", "POST"])
def update_book(id):

    if request.method == "POST":

        title = request.form["title"]
        author = request.form["author"]
        quantity = request.form["quantity"]

        query = """
        UPDATE books
        SET title=%s, author=%s, quantity=%s
        WHERE book_id=%s
        """

        values = (title, author, quantity, id)

        cursor.execute(query, values)
        conn.commit()

        flash("✏️Book Updated Successfully!")
        return redirect(url_for("view_books"))

    cursor.execute(
        "SELECT * FROM books WHERE book_id=%s",
        (id,)
    )

    book = cursor.fetchone()

    return render_template(
        "update_book.html",
        book=book
    )
@app.route("/issue_book/<int:id>")
def issue_book(id): 
    query = "select quantity from books where book_id=%s"
    cursor.execute(query,(id,))
    result=cursor.fetchone()
    quantity=result[0]      
    if quantity > 0: 
       query = "update books set quantity=quantity-1 where book_id=%s"
       cursor.execute(query,(id,))
       conn.commit()
       flash("🔁Book Issued Successfully")
       return redirect(url_for("view_books"))
    else:
        return render_template("books_not_available.html")

@app.route("/return_book/<int:id>")
def return_book(id): 
    query = "select quantity from books where book_id=%s"
    cursor.execute(query,(id,))
    result=cursor.fetchone()
    quantity=result[0]      
    if quantity >=0: 
       query = "update books set quantity=quantity+1 where book_id=%s"
       cursor.execute(query,(id,))
       conn.commit()
       flash("🔁Book Returned Successfully")
       return redirect(url_for("view_books"))
    else:
        return render_template("books_not_available.html")

@app.route("/logout")
def logout():
    session.pop("name", None)
    return redirect(url_for("login"))

@app.route("/search_book", methods=["GET", "POST"])
def search_book():

    if request.method == "POST":

        search_type = request.form["search_type"]
        keyword = request.form["keyword"]

        if search_type == "title":
             query = """SELECT * FROM books WHERE title LIKE %s"""
        else:
             query = """SELECT * FROM books WHERE author LIKE %s"""
        cursor.execute(query,("%" + keyword + "%",))

        book = cursor.fetchone()

        if book:
            return render_template("search_result.html",book=book)

        else:
            return render_template("book_not_found.html")

    return render_template("search_book.html")            
if __name__ == "__main__":
    app.run(debug=True)
