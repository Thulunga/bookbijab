from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


ENV = 'env'


if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user3:user123@localhost:5432/book'
    
    
else: 
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://gclvverlpkcsrr:f80a78070fcc2ebce6e03ebd00c2bc71dbfb12771066bf851adde21f040fc4ae@ec2-54-224-120-186.compute-1.amazonaws.com:5432/dcgq70g7jok1j0'

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