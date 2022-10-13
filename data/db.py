import sqlite3


conn = sqlite3.connect("data/db.db")
cursor = conn.cursor()


def get_next_question(user_id):
	result = cursor.execute("""SELECT answer_id, question_id FROM Statistics 
							   WHERE user_id = ?
							   ORDER BY id DESC""", (user_id,)).fetchall()

	try:
		question_id = result[0][1] + 1
	except IndexError:
		question_id = 1

	result = cursor.execute("""SELECT text FROM Question 
							   WHERE id = ?""", (question_id,)).fetchone()
	if result is None:
		return None
	text = result[0]
	return {"text": text, "id": question_id}


def get_answers():
	result = cursor.execute("""SELECT name, id FROM Answer
							   ORDER BY id ASC""").fetchall()
	data = {}
	for answer in result:
		data[answer[1]] = answer[0] # key - id, val - name
	return data

def add_statistics(user_id, answer_id, question_id):
	cursor.execute("""INSERT INTO Statistics
           (user_id, answer_id, question_id) 
           VALUES (?, ?, ?)""", (user_id, answer_id, question_id))
	conn.commit()


def get_answer_id(text):
	result = cursor.execute("""SELECT id FROM Answer
							   WHERE name = ?""", (text,)).fetchone()
	return result[0]


def get_result(user_id):
	result = cursor.execute("""SELECT id FROM Statistics
							   WHERE (answer_id = 5 or answer_id = 4) and user_id = ?""", (user_id,)).fetchall()
	return len(result)


def delete_last(user_id):
	result = cursor.execute("""SELECT answer_id, question_id FROM Statistics 
							   WHERE user_id = ?
							   ORDER BY datetime DESC""", (user_id,)).fetchall()
	try:
		question_id = result[0][1]
		cursor.execute("DELETE FROM Statistics WHERE question_id = ?", (question_id,))
		conn.commit()
	except IndexError:
		pass


def del_stat(user_id):
	cursor.execute("DELETE FROM Statistics WHERE user_id = ?", (user_id,))
	conn.commit()