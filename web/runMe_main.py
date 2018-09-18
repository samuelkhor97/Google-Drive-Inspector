#run this file
import os
from bottle import route, run, template,static_file,request

@route('/static/login.html') # or @route('/login')
@route('/login')
def login():
    return '''<form action="/login" method="post">
        Email: <br>
        <input name="email" type=" text"><br>
        Password: <br>
        Password: <input name="password" type="password"><br>
        <input value="Login" type="submit" />
    </form>'''

# temporary check_login function
emails = ["email", "mail"]
passwords = ["password", "pass"]
def check_login(email, password):
    if email in emails and password in passwords:
        return True
    else:
        return False

@route('/static/login.html',method='POST')
@route('/login',method='POST')
def do_login():
    email = request.forms.get('email')
    password = request.forms.get('password')
    if check_login(email,password):
        return page('page2.html')
    else:
        return "<p>Login Failed!</p>"


@route("/static/<filepath>") # this way, all requests for static file can be routed easily (but not the best way though),
# eg. http://localhost:7878/static/style.css is handled , where filepath='style.css'
def page(filepath):
    return static_file(filepath, root="/Users/Clarisse/Downloads/bottle_example/bottle-0.12.13/UI implementation") 

run(host="127.0.0.1",port=8080,debug=True)

