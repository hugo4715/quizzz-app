import os
import bcrypt
import sqlite3
import jwt_utils
from flask_cors import CORS
from flask import Flask, request, jsonify

app = Flask(__name__)
CORS(app, send_wildcard=True)

url_prefix = os.getenv("FLASK_URL_PREFIX")
if url_prefix[-1] == "/":
    url_prefix = url_prefix[:-1]

admin_pw_hash = b'$2b$12$JKgC5/lPJrIFqpvRxmzxGe1jS8imVM9NaW.iOn/RDVYEEVtuYCvuK'
db_file = "db.sqlite"


# ---------- HELPERS ---------- #


class Question:
    def __init__(self,
                 title: str,
                 text: str,
                 image: str,
                 position: int,
                 possible_answers: list):
        self.title = title
        self.text = text
        self.image = image
        self.position = position
        self.possible_answers = possible_answers

    @classmethod
    def from_json(cls, question: dict):
        return cls(
            title=question["title"],
            text=question["text"],
            image=question["image"],
            position=question["position"],
            possible_answers=question["possibleAnswers"]
        )

    def to_json(self):
        return {
            "title": self.title,
            "text": self.text,
            "image": self.image,
            "position": self.position,
            "possibleAnswers": self.possible_answers
        }

    def insert_into_db(self):
        db_connection = sqlite3.connect("db.sqlite", isolation_level=None)
        db_cursor = sqlite3.Cursor(db_connection)
        db_connection.execute("begin")
        try:
            db_cursor.execute("select * from question where position = ?", (self.position,))
            if db_cursor.fetchone() is not None:
                # Offset by one all questions that are after the position
                db_connection.execute("update answer set question_position = question_position + 1 where "
                                      "question_position >= ?", (self.position,))
                db_connection.execute("update question set position = position + 1 where position >= ?",
                                      (self.position,))

            db_connection.executemany("insert into answer (text,correct,question_position) values (?,?,?)",
                                      [(a["text"], a["isCorrect"], self.position) for a in self.possible_answers])
            db_connection.execute("insert into question (title,text,image,position) values (?,?,?,?)",
                                  (self.title, self.text, self.image, self.position))
            db_connection.execute("commit")
        except sqlite3.Error:
            db_connection.execute("rollback")


def get_question_count():
    db_connection = sqlite3.connect("db.sqlite", isolation_level=None)
    db_cursor = sqlite3.Cursor(db_connection)

    db_connection.execute("begin")
    db_cursor.execute("select distinct position from question")
    db_connection.commit()

    return len(db_cursor.fetchall())


def get_question_local(qid):
    db_connection = sqlite3.connect("db.sqlite", isolation_level=None)
    db_cursor = sqlite3.Cursor(db_connection)

    db_connection.execute("begin")
    db_cursor.execute("select * from question where position=?", (qid,))
    db_connection.commit()

    returned_question = db_cursor.fetchone()
    if returned_question is None:
        return "Not found", 404

    db_connection.execute("begin")
    db_cursor.execute("select * from answer where question_position=?", (qid,))
    db_connection.commit()

    returned_answer = db_cursor.fetchall()
    if returned_answer is None:
        return "Not found", 404

    question_object = {
        "title": returned_question[1],
        "text": returned_question[2],
        "image": returned_question[3],
        "position": returned_question[4],
        "possibleAnswers": [{"text": a[1], "isCorrect": a[2] != 0} for a in returned_answer]
    }
    return question_object, 200


def delete_question_local(qid):
    # Only delete if the question exists
    if get_question_local(qid)[1] != 200:
        return "Not found", 404

    db_connection = sqlite3.connect("db.sqlite", isolation_level=None)
    db_connection.execute("begin")
    try:
        db_connection.execute("delete from answer where question_position=?", (qid,))
        db_connection.execute("delete from question where position=?", (qid,))
        # Decrement positions for questions that are after this one
        db_connection.execute("update answer set question_position = question_position - 1 where question_position > ?",
                              (qid,))
        db_connection.execute("update question set position = position - 1 where position > ?", (qid,))

        db_connection.execute("commit")
    except sqlite3.Error:
        db_connection.execute("rollback")
        return "Error", 500

    return "Success", 204


def update_question_local(qid, qjson):
    # Only update if the question exists
    if get_question_local(qid)[1] != 200:
        return "Not found", 404

    try:
        # Question position has changed
        if qjson["position"] != qid:
            delete_question_local(qid)
            # Offset all questions after the newly inserted one
            db_connection = sqlite3.connect("db.sqlite", isolation_level=None)
            db_connection.execute("begin")
            db_connection.execute("update answer set question_position = question_position + 1 where "
                                  "question_position >= ?", (qjson["position"],))
            db_connection.execute("update question set position = position + 1 where position >= ?", (qjson["position"],))
            db_connection.commit()

            question = Question.from_json(qjson)
            question.insert_into_db()

        # Just update the question values
        else:
            db_connection = sqlite3.connect("db.sqlite", isolation_level=None)
            db_connection.execute("begin")
            db_connection.execute("update question set title=?, text=?, image=? where position=?", (
                qjson["title"], qjson["text"], qjson["image"], qjson["position"]
            ))
            db_connection.commit()

        return "Success", 200
    except KeyError as e:
        print(e)
        return "Bad request", 400


def check_auth_error(r):
    user_token = str(r.headers.get("Authorization")).replace("Bearer ", "").strip()
    try:
        jwt_utils.decode_token(user_token)
    except jwt_utils.JwtError as e:
        return "Unauthorized: {}".format(e.message), 401

    return None


def create_participation(playername,score):
    db_connection = sqlite3.connect("db.sqlite", isolation_level=None)
    db_cursor = sqlite3.Cursor(db_connection)

    db_connection.execute("begin")
    db_cursor.execute("insert into score (playerName,score,date) values (?,?,current_timestamp);", (playername,score))
    db_connection.commit()
    print('Inserted new score for player ' + playername)


def truncate_participations():
    db_connection = sqlite3.connect("db.sqlite", isolation_level=None)
    db_cursor = sqlite3.Cursor(db_connection)

    db_connection.execute("begin")
    db_cursor.execute("delete from score", )
    db_connection.commit()
    print('Cleaned participations')

# ---------- PUBLIC PART ----------  #


@app.route(url_prefix + '/quiz-info', methods=['GET'])
def quiz_info():
    db_connection = sqlite3.connect("db.sqlite", isolation_level=None)
    db_cursor = sqlite3.Cursor(db_connection)
    db_connection.execute("begin")
    db_cursor.execute("select * from score order by score desc")
    db_connection.commit()
    return {"size": get_question_count(), "scores": [{"playerName": s[1], "score": s[2], "date": s[3]}
                                                     for s in db_cursor.fetchall()]}, 200


@app.route(url_prefix + '/questions/<qid>', methods=['GET'])
def get_question(qid):
    return get_question_local(qid)


@app.route(url_prefix + '/questions', methods=['GET'])
def get_all_questions():
    # Get a list of all questions from the DB
    db_connection = sqlite3.connect("db.sqlite", isolation_level=None)
    db_cursor = sqlite3.Cursor(db_connection)
    db_connection.execute("begin")
    db_cursor.execute("select * from question order by position")
    db_connection.commit()
    db_qid = [q[4] for q in db_cursor.fetchall()]
    question_list = []
    for qid in db_qid:
        question, error = get_question_local(qid)
        if error == 200:
            question_list.append(question)

    return jsonify(question_list), 200


@app.route(url_prefix + '/login', methods=['POST'])
def login():
    payload = request.get_json()
    try:
        password = str(payload["password"]).encode("utf-8")
        # Hashed password check
        if bcrypt.checkpw(password, admin_pw_hash):
            token = jwt_utils.build_token()
            if not isinstance(token, str):
                token = token.decode("utf-8")
            return {"token": token}, 200
    except KeyError:
        return "No password specified", 400
    return "Invalid password", 401

@app.route(url_prefix + '/participations', methods=['DELETE'])
def delete_participations():
    truncate_participations()
    return 'Ok', 204


@app.route(url_prefix + '/participations', methods=['POST'])
def participations():
    payload = request.get_json()
    try:
        username = payload['playerName']
        answers = payload['answers']
        question_count = get_question_count()
        if len(answers) != question_count:
            return "Bad request: expected {} answers".format(question_count), 400

        summary = []
        score = 0
        for i in range(0, question_count):
            question,code = get_question_local(i+1)
            was_correct = question['possibleAnswers'][answers[i]]['isCorrect']
            if was_correct:
                score += 1
            summary.append({
                'wasCorrect': was_correct,
                'correctAnswerPosition': [x for x in range(len(question['possibleAnswers'])) if question['possibleAnswers'][x]['isCorrect']][0]+1
            })
        create_participation(username, score)
        return {
            'answersSummaries': summary,
            'playerName': username,
            'score': score
        }, 200

    except KeyError as e:
        return "Bad request: {} not given".format(e), 400

# ---------- ADMINISTRATION PART ----------  #


@app.route(url_prefix + '/questions', methods=['POST'])
def create_question():
    try:
        auth_error = check_auth_error(request)
        if auth_error is not None:
            return auth_error

        question = Question.from_json(request.get_json())
        #print("Add question: {}".format(request.get_json()))
        question.insert_into_db()
        return "Success", 200

    except KeyError as e:
        return "Bad request: {} not given".format(e), 400


@app.route(url_prefix + '/questions/<qid>', methods=["PUT"])
def update_question(qid):
    auth_error = check_auth_error(request)
    if auth_error is not None:
        return auth_error

    return update_question_local(qid, request.get_json())


@app.route(url_prefix + '/questions/<qid>', methods=['DELETE'])
def delete_question(qid):
    auth_error = check_auth_error(request)
    if auth_error is not None:
        return auth_error

    return delete_question_local(qid)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
