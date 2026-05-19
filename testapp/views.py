from testapp import app
from flask import jsonify
from flask import request
from datetime import datetime, timezone, timedelta
import sqlite3
import os

def get_db():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dbname = os.path.join(base_dir, 'club_room.db')
    conn = sqlite3.connect(dbname)
    conn.row_factory = sqlite3.Row
    return conn

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
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM members')
    rows = c.fetchall()
    conn.close()

    members =[dict(row) for row in rows]
    
    return jsonify(members)

#メンバーを追加するAPI
@app.route('/members', methods=['POST'])
def add_member():
     #実行ファイルのディレクトリを取得して、データベースファイルのパスを作成
    conn = get_db()
    c = conn.cursor()

    #JSONデータ取得
    data = request.get_json()
    name = data.get('name')
    student_id = data.get('student_id')
    card_id = data.get('card_id')
    role = data.get('role')

    #必須項目のタプル
    required = ('name', 'student_id', 'card_id', 'role')

    #全ての必須項目が入力されているか確認(不足なら400エラーを返す)
    if not all(data.get(field) for field in required):
        return jsonify({'message': '全ての項目を入力してください'}),400
    

    #データベースに接続して、membersテーブルに新しい行を挿入
    c.execute("INSERT INTO members (name, student_id, card_id, role) VALUES (?, ?, ?, ?)", (name, student_id, card_id, role))
    conn.commit()
    conn.close()

    return jsonify({'message': 'メンバーを追加しました'}),201

#IDを指定してメンバーを削除するAPI
@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    #実行ファイルのディレクトリを取得して、データベースファイルのパスを作成
    conn = get_db()
    c = conn.cursor()
    c.execute('DELETE FROM members WHERE id = ?', (member_id,))

    #削除された行数が0なら、404エラーを返す
    if c.rowcount == 0: 
        conn.commit()
        conn.close()
        return jsonify({'message': 'メンバーが見つかりませんでした。'}),404
    
    conn.commit()
    conn.close()

    return jsonify({'message': 'メンバーを削除しました'}),200

#logsテーブルを取得するAPI
@app.route('/logs', methods=['GET'])
def logs():
    #実行ファイルのディレクトリを取得して、データベースファイルのパスを作成
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM logs')
    rows = c.fetchall()
    conn.close()

    logs =[dict(row) for row in rows]
    
    return jsonify(logs)

#logsテーブルにデータを追加するAPI
@app.route('/logs', methods=['POST'])
def add_log():
    #実行ファイルのディレクトリを取得して、データベースファイルのパスを作成
    conn = get_db()
    c = conn.cursor()

    #JSONデータ取得
    data = request.get_json()
    card_id = data.get('card_id')
    name = data.get('name')

    #必須項目のタプル
    required = ('card_id', 'name')

    #全ての必須項目が入力されているか確認(不足なら400エラーを返す)
    if not all(data.get(field) for field in required):
        return jsonify({'message': '全ての項目を入力してください'}),400
    
    #データベースに接続して、logsテーブルに新しい行を挿入
    c.execute("INSERT INTO logs (card_id, name) VALUES (?, ?)", (card_id, name))
    conn.commit()
    conn.close()

    return jsonify({'message': 'ログを追加しました'}),201

@app.route('/logs/<int:log_id>', methods=['PUT'])
def update_log(log_id):
    #実行ファイルのディレクトリを取得して、データベースファイルのパスを作成
    conn = get_db()
    c = conn.cursor()
    JST = timezone(timedelta(hours=9))
    now = datetime.now(JST)
    c.execute("UPDATE logs SET exited_at = ? WHERE id = ?", (now, log_id))

    if c.rowcount == 0:
        conn.commit()
        conn.close()
        return jsonify({'message': 'ログが見つかりませんでした。'}),404

    conn.commit()
    conn.close()

    return jsonify({'message': 'ログを更新しました'}),200
