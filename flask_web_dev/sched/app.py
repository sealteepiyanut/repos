from flask import Flask
from flask import render_template, abort, jsonify, redirect
from flask import request, url_for
from sched.forms import AppointmentForm
from sched.models import Appointment


app = Flask(__name__)

app.debug = True

@app.route("/")
def index():
    return render_template("index.html")

@app.route('appointments/create', methods=['GET', 'POST'])
form = AppointmentForm(request.form)
if request.method == 'POST' and form.validate():
	appt = Appointment()
	form.populate_obj(appt)
	db.session.add(appt)
	db.session.commit()
	return redirect(url_for('appointment_list'))
return render_template('appointment/edit.html')



if __name__ == "__main__":
    app.run()


