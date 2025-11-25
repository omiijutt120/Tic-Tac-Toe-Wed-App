from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "replace-this-with-a-secure-random-key"

WIN_COMBOS = (
    (0,1,2), (3,4,5), (6,7,8),
    (0,3,6), (1,4,7), (2,5,8),
    (0,4,8), (2,4,6)
)

def new_game():
    return {"board": [""] * 9, "player": "X", "winner": None}

def check_winner(board):
    for a,b,c in WIN_COMBOS:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    if all(cell != "" for cell in board):
        return "Tie"
    return None

@app.route("/", methods=["GET", "POST"])
def index():
    if "game" not in session:
        session["game"] = new_game()

    game = session["game"]

    if request.method == "POST":
        if game["winner"] is None:
            move = request.form.get("cell")
            if move and move.isdigit():
                idx = int(move)
                if 0 <= idx < 9 and game["board"][idx] == "":
                    game["board"][idx] = game["player"]
                    game["winner"] = check_winner(game["board"])
                    if game["winner"] is None:
                        game["player"] = "O" if game["player"] == "X" else "X"
        session["game"] = game
        return redirect(url_for("index"))

    return render_template("index.html", board=game["board"], player=game["player"], winner=game["winner"])

@app.route("/reset", methods=["POST"])
def reset():
    session["game"] = new_game()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
