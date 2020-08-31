import web
from Models import RegisterModel, LoginModel
from js.jquery import jquery

web.config.debug = False

urls = (
    '/', 'home',
    '/register', 'register',
    '/login', 'login',
    '/logout', 'logout',
    '/postregistration', 'PostRegistration',
    '/check-login', 'checklogin'
)

app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore("sessions"), initializer={'user': None})
session_data = session._initializer

render = web.template.render("Views/Templates", base="MainLayout", globals={'session': session_data,
                                                                            'current user': session_data["user"]})





# Classes/Routes


class home:
    def GET(self):
        return render.home()


class register:
    def GET(self):
        return render.register()


class login:
    def GET(self):
        return render.login()


class PostRegistration:
    def POST(self):
        data = web.input()

        reg_model = RegisterModel.RegisterModel()
        reg_model.insert_user(data)
        return data.username


class checklogin:
    def POST(self):
        data = web.input()
        login = LoginModel.LoginModel()
        isCorrect = login.check_user(data)

        if isCorrect:
            session_data["user"] = isCorrect
            return isCorrect

        return "Error"


class logout:
    def GET(self):
        session['user'] = None
        session_data['user'] = None

        session.kill()
        return "success"


if __name__ == "__main__":
    app.run()