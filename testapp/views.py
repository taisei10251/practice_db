from testapp import app
from flask import jsonify
from flask import request
import sqlite3
import os

#index
@app.route('/')
def index():
    return "入退室管理"

#テスト
@app.route('/test')
def test():
    return "これはテストページですわ"

#メンバー一覧を取得するAPI
@app.route('/members',methods=['GET'])
def members():
    #実行ファイルのディレクトリを取得して、データベースファイルのパスを作成
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dbname = os.path.join(base_dir, 'club_room.db')

    #データベースに接続して、membersテーブルから全ての行を取得
    conn = sqlite3.connect(dbname)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM members')
    rows = c.fetchall()
    conn.close()

    members =[dict(row) for row in rows]
    
    return jsonify(members)

#データを受け取ってDBにINSERTするAPI
@app.route('/members', methods=['POST'])
def add_member():
     #実行ファイルのディレクトリを取得して、データベースファイルのパスを作成
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dbname = os.path.join(base_dir, 'club_room.db')

    #JSONデータ取得
    data = request.get_json()
    name = data.get('name')
    student_id = data.get('student_id')
    card_id = data.get('card_id')
    role = data.get('role')

    #データベースに接続して、membersテーブルに新しい行を挿入
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute("INSERT INTO members (name, student_id, card_id, role) VALUES (?, ?, ?, ?)", (name, student_id, card_id, role))
    conn.commit()
    conn.close()

    if not name or not student_id or not card_id or not role:
        return jsonify({'error': 'Missing required fields'}), 400
    else:
        return jsonify({'message': 'Member added successfully'}),201

