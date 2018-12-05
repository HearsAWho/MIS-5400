# https://www.tutorialspoint.com/flask/flask_sqlite.htm

from flask import Flask, render_template, request
import sqlite3 as sql
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html'), 200

@app.route('/enternew')
def new_entry():
    return render_template('reit.html'), 200

@app.route('/delete')
def del_entry():
    return render_template('delete.html'), 200


@app.route('/item',methods = ['POST'])
def addrec():
    try:
        ticker = request.form['tkr']
        name = request.form['name']
        price = request.form['price']
        divYield = request.form['div']
        mktCap = request.form['cap']
        pe = request.form['pe']
        payout = request.form['payout']

        with sql.connect("reit.db") as con:
            cur = con.cursor()

            cur.execute("INSERT INTO AllReits (ticker,name,price,divYield,mktCap,pe,payout) VALUES (?,?,?,?,?,?,?)",(ticker,name,price,divYield,mktCap,pe,payout) )

            con.commit()
            msg = "Record successfully added"
    except:
        con.rollback()
        msg = "error in insert operation"

    finally:
        return render_template("result.html",msg = msg)
        con.close()


@app.route('/item', methods = ['GET'])
def item():
    con = sql.connect("reit.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM AllReits LIMIT 1000")

    rows = cur.fetchall();
    return render_template("list.html",rows = rows)


@app.route('/item/<string:id>', methods=['GET'])
def item_by_id(id):
   con = sql.connect("reit.db")
   con.row_factory = sql.Row

   cur = con.cursor()
   cur.execute("SELECT * FROM AllReits WHERE ticker = (?)", [id])

   rows = cur.fetchall()
   return render_template("list.html", rows=rows)

@app.route('/item/<string:id>', methods=['DELETE'])
def delete_by_id(id):
    try:
        con = sql.connect("reit.db")
        cur = con.cursor()
        cur.execute("DELETE FROM AllReits WHERE ticker = (?);", [id])
        con.commit() # sqlite does not have implicit commit.
        return 'success', 200
    except Exception as e:
        return abort(500)
        con.close()

if __name__ == '__main__':
    app.run(debug = True)