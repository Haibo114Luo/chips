from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 玩家模型：记录用户名、初始金额、当前余额、当前局下注额
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    start_amount = db.Column(db.Float, nullable=False)
    current_amount = db.Column(db.Float, nullable=False)  # 玩家余额
    current_bet = db.Column(db.Float, default=0.0, nullable=False)  # 当前局下注

# 注册玩家接口
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

    new_player = Player(
        username=username,
        start_amount=start_amount,
        current_amount=start_amount,
        current_bet=0.0
    )
    db.session.add(new_player)
    db.session.commit()

    return jsonify({'message': '玩家注册成功'}), 200

# 更新玩家余额接口（赢输后更新余额）
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

    return jsonify({'message': '玩家余额更新成功'}), 200

# 更新玩家下注接口（只更新当前局下注额）
@app.route('/update_bet', methods=['POST'])
def update_bet():
    data = request.get_json()
    username = data.get('username')
    current_bet = data.get('current_bet')
    
    if username is None or current_bet is None:
        return jsonify({'error': '缺少用户名或当前下注'}), 400

    player = Player.query.filter_by(username=username).first()
    if not player:
        return jsonify({'error': '未找到该玩家'}), 404

    try:
        current_bet = float(current_bet)
    except ValueError:
        return jsonify({'error': '当前下注必须为数字'}), 400

    player.current_bet = current_bet
    db.session.commit()

    return jsonify({'message': '下注更新成功'}), 200

# 底池统计接口：计算所有玩家当前下注额之和
@app.route('/pot', methods=['GET'])
def get_pot():
    players = Player.query.all()
    total_pot = sum(player.current_bet for player in players)
    return jsonify({'pot': total_pot}), 200

# 获取所有玩家数据接口（用于侧边菜单显示玩家余额）
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
