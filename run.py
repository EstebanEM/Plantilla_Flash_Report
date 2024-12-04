from flask import (
    Flask,
    jsonify,
    request,
    render_template,
    Blueprint,
    copy_current_request_context,
)
from flask_mail import Mail, Message
import threading


app = Flask(__name__, template_folder="template")

# Configuración de Flask-Mail
app.config["MAIL_SERVER"] = "smtp.office365.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = "practicante@skanhawk.com"  # Cambiar por el correo
app.config["MAIL_PASSWORD"] = "p4sant3sen420@"  # Cambiar por el pass del correo


mail = Mail(app)


# Crear un Blueprint
flash_report_blueprint = Blueprint("flash_report", __name__)


def send_mail(user_email, username):
    msg = Message(
        "📢 FLASH-REPORT  📢",
        sender="practicante@skanhawk.com",  # Cambiar por el correo
        recipients= [user_email],
    )
    msg.html = render_template("flash_report.html", username=username)
    mail.send(msg)


@flash_report_blueprint.route("/api/flash_report/send", methods=["POST"])
def flas_report_send():
    try:
        datos = request.json

        @copy_current_request_context
        def send_message(email, user):
            send_mail(email, user)

        # email = ["afforero@skanhawk.com", "practicante@skanhawk.com", "lmejia@skanhawk.com"]
        email =  "practicante@skanhawk.com"

        userN = "Andres"
        sender = threading.Thread(
            name="mail_sender", target=send_message, args=(email, userN)
        )
        sender.start()

        response = jsonify({"test": datos})
        return response

    except Exception as e:
        return jsonify({"Error": str(e)}), 500


# Registrar Blueprint
app.register_blueprint(flash_report_blueprint)


if __name__ == "__main__":
    app.run(debug=True, port=8051)
