from flask import Flask
from data import db_session
from data.products import Products
from data.users import User
from flask_login import LoginManager
from forms.user import RegisterForm, LoginForm
from flask import render_template, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    app.run()


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form['submit_button'] == 'Войти':
            db_sess = db_session.create_session()
            user = User(
                email=form.email.data
            )
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            return redirect('/')
        elif form['submit_button'] == 'Регистрация':
            return redirect('/register')
    return render_template('login.html', title='login', form=form)


'''products = Products()
products.name = "Манчкин"
products.price = "700"
products.count = "20"
products.description = 'scawaw'
products.producer = "Hobby Games"
db_sess = db_session.create_session()
db_sess.add(products)
db_sess.commit()

products = Products()
products.name = "Манчкин 1"
products.price = "7030"
products.count = "202"
products.description = 'scawaw'
products.producer = "Hobby Games"
db_sess = db_session.create_session()
db_sess.add(products)
db_sess.commit()

products = Products()
products.name = "Манчкин 2"
products.price = "7020"
products.count = "201"
products.description = 'scawaw'
products.producer = "Hobby Games"
db_sess = db_session.create_session()
db_sess.add(products)
db_sess.commit()'''

if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    main()
