from flask import Flask,render_template,url_for,request,session,redirect, flash,jsonify
import bcrypt
from flask_pymongo import PyMongo
from pymongo import ALL

app = Flask(__name__)

app.config['MONGODB_NAME'] = 'database_name'
app.config['MONGO_URI'] = "mongodb+srv://url_for_database_connection"

mongo = PyMongo(app)

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html')
    return render_template('index.html')

@app.route('/index')
def main():
    return render_template('index.html')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'username' : request.form['username']})
        if login_user:
            if bcrypt.checkpw(request.form['password'].encode('utf-8'), login_user['password']):
                session['username'] = request.form['username']
                return redirect(url_for('index'))
            flash('Invalid Username/Password','warning')
            return render_template('login.html')
    return render_template('login.html')

@app.route('/register' , methods=['POST','GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'username' : request.form['username']})
        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'username':request.form['username'],'email': request.form['email'],'password': hashpass})
            session['username'] = request.form['username']
            return render_template('index.html')
        return render_template('index.html')
    return render_template('login.html')

@app.route('/dashboard' , methods=['POST','GET'])
def dashboard():
    if request.method == 'POST':
        places = mongo.db.places
        existing_place = places.find_one({'name' : request.form['name']})
        if existing_place is None:
            places.insert({'name' : request.form['name'],'imgUrl': request.form['imgUrl'],'address': request.form['address'], 'temp': request.form['temp'], 'budget': request.form['budget'], 'about': request.form['about']})
            return render_template('dashboard.html')
        flash('Place Already exist!','success')
        return render_template('dashboard.html')
    return render_template('dashboard.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    places = mongo.db.places
    mycity = request.args.get('city')
    query = {'city': request.args.get('city'),'temp': request.args.get('temp'),'budget' : request.args.get('budget')}
    all_documents = places.find(query)
    return render_template('destination.html', all_documents=all_documents, mycity=mycity)
    #return render_template('destination.html', query=query)

@app.route('/output/<name>', methods=['GET'])
def output(name):
    if 'username' in session:
        raj = name
        places = mongo.db.places
        all_output = places.find_one({'name': raj})
        return  render_template('output.html', all_output=all_output)
    return render_template('login.html')

if __name__ == '__main__':
    app.secret_key = b'secret_key'
    app.run(debug=True)
