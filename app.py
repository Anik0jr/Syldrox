from flask import Flask, request, jsonify
import time

app = Flask(name)

# ইউজারের ডাটাবেস
users = {}

def create_user(user_id, referrer_id=None):
    if user_id not in users:
        users[user_id] = {
            'balance': 0,
            'last_mine_time': 0,
            'referrals': [],
            'referrer': referrer_id
        }
        # যদি রেফারার থাকে, তাকে রেফারেল বোনাস দিন
        if referrer_id and referrer_id in users:
            users[referrer_id]['balance'] += 10  # রেফারারকে ১০ কয়েন বোনাস দেওয়া হবে
            users[referrer_id]['referrals'].append(user_id)

@app.route('/get_balance', methods=['POST'])
def get_balance():
    data = request.json
    user_id = data['user_id']
    create_user(user_id)
    
    return jsonify({'balance': users[user_id]['balance']})

@app.route('/mine', methods=['POST'])
def mine():
    data = request.json
    user_id = data['user_id']
    create_user(user_id)
    
    current_time = time.time()
    last_mine_time = users[user_id]['last_mine_time']
    
    if current_time - last_mine_time >= 3600:  # প্রতি ১ ঘণ্টায় মাইন করা যাবে
        users[user_id]['balance'] += 5
        users[user_id]['last_mine_time'] = current_time
        return jsonify({'message': 'Successfully mined 5 coins!'})
    else:
        return jsonify({'message': 'Please wait before mining again.'})

@app.route('/withdraw', methods=['POST'])
def withdraw():
    data = request.json
    user_id = data['user_id']
    create_user(user_id)

    if users[user_id]['balance'] >= 100:  # উইথড্রল করার জন্য ১০০ কয়েন প্রয়োজন
        users[user_id]['balance'] -= 100
        return jsonify({'message': 'Successfully withdrawn 100 coins!'})
    else:
        return jsonify({'message': 'Not enough balance to withdraw.'})

@app.route('/register', methods=['GET'])
def register():
    user_id = request.args.get('user_id')
    referrer_id = request.args.get('ref')  # রেফারার ID
    create_user(user_id, referrer_id)
    return jsonify({'message': 'Account created successfully!', 'user_id': user_id})

if name == 'main':
    app.run(debug=True)