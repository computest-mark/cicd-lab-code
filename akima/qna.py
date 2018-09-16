from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from akima.auth import login_required
from akima.db import get_db

bp = Blueprint('qna', __name__)

@bp.route('/')
def index():
    db = get_db()
    questions = db.execute(
        'SELECT q.id, question, answer, created, author_id, username'
        ' FROM qna q JOIN user u ON q.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('qna/index.html', questions=questions)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']
        error = None

        if not question:
            error = 'Question is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO qna (question, answer, author_id)'
                ' VALUES (?, ?, ?)',
                (question, answer, g.user['id'])
            )
            db.commit()
            return redirect(url_for('qna.index'))

    return render_template('qna/create.html')

def get_question_by_id(id, check_author=True):
    question = get_db().execute(
        'SELECT q.id, question, answer, created, author_id, username'
        ' FROM qna q JOIN user u ON q.author_id = u.id'
        ' WHERE q.id = ?',
        (id,)
    ).fetchone()

    if question is None:
        abort(404, "question id {0} doesn't exist.".format(id))

    if check_author and question['author_id'] != g.user['id']:
        abort(403)

    return question

def get_question(q):
    question = get_db().execute(
        'SELECT q.id, question, answer, created, author_id, username'
        ' FROM qna q JOIN user u ON q.author_id = u.id'
        ' WHERE q.question = ?',
        (q,)
    ).fetchone()

    if question is None:
        abort(404, "question '{0}' doesn't exist.".format(q))

    return question

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    question = get_question_by_id(id)

    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']
        error = None

        if not question:
            error = 'question is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE qna SET question = ?, answer = ?'
                ' WHERE id = ?',
                (question, answer, id)
            )
            db.commit()
            return redirect(url_for('qna.index'))

    return render_template('qna/update.html', question=question)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_question_by_id(id)
    db = get_db()
    db.execute('DELETE FROM question WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('qna.index'))

@bp.route('/<question>', methods=('GET',))
def answer(question):
    q = get_question(question)
    return q['answer']
