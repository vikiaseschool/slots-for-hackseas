from flask import Flask, render_template, request, session, jsonify
from functions import check_winnings, get_winnings_value, get_win_song, get_slot
app = Flask(__name__)
app.secret_key = '##########'

@app.route('/')
def index():
    credit = session.get('credit', 500)
    bet = session.get('bet', 2.0)
    slot_symbols = get_slot()

    return render_template('index.html', credit=credit, bet=bet, slot_symbols=slot_symbols, winnings=[], winnings_value=0,
                           win_song=None)

@app.route('/spin', methods=['POST'])
def spin():
    credit = session.get('credit', 500)
    bet = session.get('bet', 2.0)

    bet_action = request.form.get('bet_action')
    if bet_action == 'plus' and bet < 5.0:
        bet += 0.25
    elif bet_action == 'minus' and bet > 0.25:
        bet -= 0.25

    slot_symbols = get_slot()

    winnings = check_winnings(slot_symbols)
    winnings_value = get_winnings_value(winnings)
    win_song = get_win_song(winnings)

    if winnings:
        credit += winnings_value * bet
    else:
        credit -= bet
    session['credit'] = credit
    session['bet'] = bet

    return render_template('index.html', credit=credit, bet=bet, slot_symbols=slot_symbols, winnings=winnings, winnings_value=winnings_value, win_song=win_song)

@app.route('/change_bet', methods=['POST'])
def change_bet():
    bet_action = request.form.get('bet_action')
    bet = session.get('bet', 2.0)

    if bet_action == 'plus' and bet < 5.0:
        bet += 0.25
    elif bet_action == 'minus' and bet > 0.25:
        bet -= 0.25

    session['bet'] = bet

    return jsonify({'bet': bet})

if __name__ == '__main__':
    app.run(debug=True)
