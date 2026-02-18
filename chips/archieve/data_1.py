from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 定义玩家模型，记录用户名、起始金额和当前金额
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    start_amount = db.Column(db.Float, nullable=False)
    current_amount = db.Column(db.Float, nullable=False)

# 注册玩家接口：新增记录
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    start_amount = data.get('start_amount')
    
    if username is None or start_amount is None:
        return jsonify({'error': '缺少用户名或起始金额'}), 400

    # 检查用户名是否已存在
    if Player.query.filter_by(username=username).first():
        return jsonify({'error': '用户名已存在'}), 400

    try:
        start_amount = float(start_amount)
    except ValueError:
        return jsonify({'error': '起始金额必须为数字'}), 400

    new_player = Player(username=username, start_amount=start_amount, current_amount=start_amount)
    db.session.add(new_player)
    db.session.commit()

    return jsonify({'message': '玩家注册成功'}), 200

# 更新玩家金额接口：修改当前金额
@app.route('/update', methods=['POST'])
def update():
    data = request.get_json()
    username = data.get('username')
    current_amount = data.get('current_amount')
    
    if username is None or current_amount is None:
        return jsonify({'error': '缺少用户名或当前金额'}), 400

    player = Player.query.filter_by(username=username).first()
    if not player:
        return jsonify({'error': '未找到该玩家'}), 404

    try:
        current_amount = float(current_amount)
    except ValueError:
        return jsonify({'error': '当前金额必须为数字'}), 400

    player.current_amount = current_amount
    db.session.commit()

    return jsonify({'message': '玩家金额更新成功'}), 200

# 获取所有玩家数据接口
@app.route('/players', methods=['GET'])
def get_players():
    players = Player.query.all()
    players_data = [{
        'username': player.username,
        'start_amount': player.start_amount,
        'current_amount': player.current_amount
    } for player in players]
    return jsonify(players_data), 200

# 清空所有玩家数据接口
@app.route('/clear', methods=['POST'])
def clear_players():
    try:
        num_rows_deleted = db.session.query(Player).delete()
        db.session.commit()
        return jsonify({'message': f'已清空 {num_rows_deleted} 条玩家数据'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # 使用 host='0.0.0.0' 允许局域网中其他设备访问
    app.run(debug=True, host='0.0.0.0', port=5000)
