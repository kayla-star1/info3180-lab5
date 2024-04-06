"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app
from flask import render_template, request, jsonify, send_file,Flask
import os
from werkzeug.utils import secure_filename
from app.forms import MovieForm
from app.models import db, Movie
from flask_wtf.csrf import generate_csrf
import json

app = Flask(__name__)

###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

@app.route('/api/v1/movies', methods =['POST'])
def movies():
    form = MovieForm()
    if form.validate_on_submit():
        [title,poster, description, token] = form 
        poster_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(poster.data.filename))
        poster.data.save(poster_path)
        
        movie = Movie(title=title.data, poster=secure_filename(poster.data.filename), description=description.data)
        
        db.session.add(movie)
        db.session.commit()
        
        data ={
            "message": "Movie Successfully added",
            "title": movie.title,
            "poster": movie.poster,
            "description": movie.description
        }
        return json.dumps(data)    
    else:
        errors = form_errors(form)
        data ={"errors": errors}
        return jsonify({"errors": errors})
    
@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})

def get_poster(filename):
    return "https://127.0.0.1:8080/" + os.path.join(app.config["STATIC_FOLDER"], secure_filename(filename))

@app.route('/api/v1/movies', methods=['GET'])
def add_movies():
    raw_data= db.session.query(Movie).all()
    data=list(map(lambda x:
        {
            "id": x.id,
            "title": x.title,
            "description": x.description,
            "poster": get_poster(x.poster)
        }, raw_data))
    return jsonify(data)

###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)