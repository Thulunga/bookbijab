from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


ENV = 'prod'


if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:user123/book_server'
    
    
else: 
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://wzuubfmfvhgyjb:a48e0c4ebe66f37e020a436c177f99a863ac1e9650a04012d1acf3bd5d7cc86e@ec2-18-214-140-149.compute-1.amazonaws.com:5432/dba09fq30p8n1u'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']
       # print(customer, dealer, rating, comments)
        if customer == '' or dealer == '':
            return render_template('index.html', message="please enter required fields")          
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer, dealer, rating, comments)
            db.session.add(data)
            db.session.commit()
            return render_template('success.html')
        return render_template('index.html', message='You have already submitted feedback')









if __name__ == '__main__':
    #app.debug = True
    app.run()