import json
import os
import sys
import argparse
import chess
import chess.engine
import chess.pgn
import datetime

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Run chess engine games with specified configuration.')
parser.add_argument('--config', '-c', required=True, help='Path to the configuration file')
args = parser.parse_args()

# Read configuration file
config_file = args.config

if not os.path.exists(config_file):
    print(f"Configuration file {config_file} does not exist.")
    sys.exit(1)

with open(config_file, 'r') as f:
    config = json.load(f)

# Extract variables from config
lc0_path = config['lc0_path']
white_net = config['white_net']
black_net = config['black_net']
num_games = config['num_games']
pgn_file_name = config['pgn_file_name']
use_opening_book = config['use_opening_book']
opening_book = config.get('opening_book', '')
use_dropbox_upload = config['use_dropbox_upload']

engine1_options = config['engine1_options']
engine2_options = config['engine2_options']

depth_limit_w_nodes = config['depth_limit_w']
depth_limit_b_nodes = config['depth_limit_b']

# Handle Dropbox setup if needed
if use_dropbox_upload:
    import dropbox
    dropbox_params = config['dropbox_params']
    DROPBOX_ACCESS_TOKEN = dropbox_params.get('access_token')
    app_key = dropbox_params.get('app_key')
    app_secret = dropbox_params.get('app_secret')
    oauth2_refresh_token = dropbox_params.get('oauth2_refresh_token')

    dbx = dropbox.Dropbox(
        app_key=app_key,
        app_secret=app_secret,
        oauth2_refresh_token=oauth2_refresh_token
    )

# Set up the opening book or starting FENs
if use_opening_book:
    if not os.path.exists(opening_book):
        print(f"Opening book file {opening_book} does not exist.")
        sys.exit(1)
    with open(opening_book, 'r') as f:
        fens = [line.strip() for line in f if line.strip()]
else:
    fixed_start_fen = config.get('fixed_start_fen', chess.STARTING_FEN)
    fens = [fixed_start_fen]

# Replace 'white_net' and 'black_net' placeholders in engine options
def replace_net_paths(options):
    for key, value in options.items():
        if value == 'white_net':
            options[key] = white_net
        elif value == 'black_net':
            options[key] = black_net

replace_net_paths(engine1_options)
replace_net_paths(engine2_options)

# Initialize engines
engine1 = chess.engine.SimpleEngine.popen_uci(lc0_path)
engine2 = chess.engine.SimpleEngine.popen_uci(lc0_path)

# Configure engines
engine1.configure(engine1_options)
engine2.configure(engine2_options)

# Set node limits
depth_limit_w = chess.engine.Limit(nodes=depth_limit_w_nodes)
depth_limit_b = chess.engine.Limit(nodes=depth_limit_b_nodes)

# Open a PGN file to save the games
pgn_file = open(pgn_file_name, 'a')

# Load last saved progress, if available
if os.path.exists("progress.json"):
    with open("progress.json", "r") as f:
        progress_data = json.load(f)
        start_game = progress_data.get("game_number", 1)
else:
    start_game = 1

wins = 0
losses = 0
draws = 0

try:
    for game_number in range(start_game, num_games + 1):
        # Determine which FEN to use
        fen_index = (game_number - 1) % len(fens)
        start_fen = fens[fen_index]

        board = chess.Board(fen=start_fen)
        game = chess.pgn.Game()
        game.setup(board)
        node = game

        # Set game headers
        game.headers["Event"] = "Leela Queen Odds Training"
        game.headers["Site"] = "Local"
        game.headers["Date"] = datetime.datetime.now().strftime("%Y.%m.%d")
        game.headers["Round"] = str(game_number)
        game.headers["White"] = "LeelaZero_White"
        game.headers["Black"] = "LeelaZero_Black"

        game_drawn=0
        try:
            while not board.is_game_over():
                if (board.can_claim_fifty_moves()):
                    game_drawn=1
                    break
                if board.turn == chess.WHITE:
                    # White's turn
                    result = engine1.play(board, depth_limit_w)
                else:
                    # Black's turn
                    result = engine2.play(board, depth_limit_b)

                board.push(result.move)
                node = node.add_variation(result.move)
        except Exception as e:
            print(f"Exception during game {game_number}: {e}")
            # If an error occurs, skip to the next game
            continue

        # Game over, set the result
        if (game_drawn==1):
                game.headers["Result"] = "1/2-1/2"
        else:
                game.headers["Result"] = board.result()

        if (game_drawn==0):
            if board.result() == '1-0':
                wins += 1
            elif board.result() == '0-1':
                losses += 1
            else:
                draws += 1
        else:
            draws +=1

        # Calculate total games
        total_games = wins + draws + losses

        # Save the game to the PGN file
        print(game, file=pgn_file, end="\n\n")

        # Upload the PGN file to Dropbox every 100 games
        if use_dropbox_upload and total_games % 100 == 0:
            # Close the PGN file to ensure all data is written
            pgn_file.close()

            try:
                # Dropbox upload code
                with open(pgn_file_name, "rb") as f:
                    dropbox_path = f"/{pgn_file_name}"
                    dbx.files_upload(f.read(), dropbox_path, mode=dropbox.files.WriteMode.overwrite)
                    print(f"Uploaded {pgn_file_name} to Dropbox.")
            except dropbox.exceptions.ApiError as e:
                print(f"Failed to upload to Dropbox: {e}")

            # Reopen the PGN file in append mode for further writing
            pgn_file = open(pgn_file_name, "a")

        # Calculate total points earned
        total_points = wins + 0.5 * draws

        # Calculate scoring percentage
        scoring_percentage = (total_points / total_games) * 100
        print(f"Total Games: {total_games}")
        print(f"{wins} Wins, {draws} Draws, {losses} Losses")
        print("Scoring Percentage: {:.2f}%".format(scoring_percentage))

        # Update progress
        with open("progress.json", "w") as f:
            json.dump({"game_number": game_number + 1}, f)

finally:
    # Quit engines
    engine1.quit()
    engine2.quit()
    # Close PGN file
    pgn_file.close()
