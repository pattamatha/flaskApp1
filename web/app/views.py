from flask import (jsonify, render_template,
                   request, url_for, flash, redirect)
import json
from sqlalchemy.sql import text, desc
from app import app
from app import db
from app.models.contact import Contact
from app.models.blog import BlogEntry

@app.route('/')
def home():
    return "Flask says 'Hello world!'"


@app.route('/crash')
def crash():
    return 1/0


@app.route('/db')
def db_connection():
    try:
        with db.engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return '<h1>db works.</h1>'
    except Exception as e:
        return '<h1>db is broken.</h1>' + str(e)


@app.route('/lab04')
def lab04_bootstrap():
    return app.send_static_file('lab04_bootstrap.html')


@app.route('/lab10', methods=('GET', 'POST'))
def lab10_phonebook():
    if request.method == 'POST':
        result = request.form.to_dict()
        app.logger.debug(str(result))
        id_ = result.get('id', '')
        validated = True
        validated_dict = dict()
        valid_keys = ['firstname', 'lastname', 'phone']

        # validate the input
        for key in result:
            app.logger.debug(key, result[key])
            # screen of unrelated inputs
            if key not in valid_keys:
                continue

            value = result[key].strip()
            if not value or value == 'undefined':
                validated = False
                break
            validated_dict[key] = value

        if validated:
            app.logger.debug('validated dict: ' + str(validated_dict))
            # if there is no id: create a new contact entry
            if not id_:
                entry = Contact(**validated_dict)
                app.logger.debug(str(entry))
                db.session.add(entry)
            # if there is an id already: update the contact entry
            else:
                contact = Contact.query.get(id_)
                contact.update(**validated_dict)

            db.session.commit()

        return lab10_db_contacts()
    return app.send_static_file('lab10_phonebook.html')


@app.route("/lab10/contacts")
def lab10_db_contacts():
    contacts = []
    db_contacts = Contact.query.all()

    contacts = list(map(lambda x: x.to_dict(), db_contacts))
    app.logger.debug("DB Contacts: " + str(contacts))

    return jsonify(contacts)


@app.route('/lab10/remove_contact', methods=('GET', 'POST'))
def lab10_remove_contacts():
    app.logger.debug("LAB10 - REMOVE")
    if request.method == 'POST':
        result = request.form.to_dict()
        id_ = result.get('id', '')
        try:
            contact = Contact.query.get(id_)
            db.session.delete(contact)
            db.session.commit()
        except Exception as ex:
            app.logger.debug(ex)
            raise
    return lab10_db_contacts()


#?----------------- Lab11_microblog ---------------------------
@app.route('/lab11', methods=('GET', 'POST'))
def lab11_microblog():
    if request.method == 'POST':
        result = request.form.to_dict()
        app.logger.debug(str(result))
        id_ = result.get('id', '')
        validated = True
        validated_dict = dict()
        valid_keys = ['name', 'email', 'message']

        # validate the input
        for key in result:
            app.logger.debug(f"{key}, {result[key]}")
            # screen of unrelated inputs
            if key not in valid_keys:
                continue

            value = result[key].strip()
            if not value or value == 'undefined':
                validated = False
                break
            validated_dict[key] = value
        app.logger.debug(f"data = {str(validated_dict)}")
        
        if validated:
            app.logger.debug('validated dict: ' + str(validated_dict))
            # if there is no id: create a new contact entry
            if not id_:
                blog_entry = BlogEntry(**validated_dict)
                app.logger.debug(str(blog_entry))
                db.session.add(blog_entry)
            # if there is an id already: update the contact entry
            else:
                blog = BlogEntry.query.get(id_)
                blog.update(**validated_dict)

            db.session.commit()

        return lab11_db_contacts()

    return app.send_static_file('lab11_microblog.html')


@app.route("/lab11/blogs")
def lab11_db_contacts():
    blogs = []
    # ให้ DB เรียงตามเวลาที่มาช้ากว่า คือให้โพสที่เพิ่มทีหลังอยู่ด้านบนสุด
    db_blogs = BlogEntry.query.order_by(BlogEntry.date_created.desc()).all()

    blogs = list(map(lambda x: x.to_dict(), db_blogs))
    app.logger.debug("DB Contacts: " + str(blogs))

    return jsonify(blogs)