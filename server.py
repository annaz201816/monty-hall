from flask import Flask, render_template, request, redirect, url_for, session
from waitress import serve
from monty_hall import simulate_games
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/play', methods=['POST'])
def play():
    initial_choice = int(request.form['door'])
    doors = [1, 2, 3]
    prize_door = random.choice(doors)
    doors.remove(initial_choice)
    if prize_door in doors:
        doors.remove(prize_door)
    removed_door = random.choice(doors)
    remaining_door = [door for door in [1, 2, 3] if door not in [initial_choice, removed_door]][0]
    session['prize_door'] = prize_door
    session['initial_choice'] = initial_choice

    # Add logging for debugging
    app.logger.info(f"Initial choice: {initial_choice}, Removed door: {removed_door}, Remaining door: {remaining_door}, Prize door: {prize_door}")
    

    return render_template('switch.html', initial_choice=initial_choice, removed_door=removed_door, remaining_door=remaining_door)
    
@app.route('/switch', methods=['GET'])
def switch():
    # Render the switch.html template
    return render_template('switch.html')

@app.route('/result', methods=['POST'])
def result():
    try:
        # Ensure 'door' is present in the form data
        if 'door' not in request.form:
            raise ValueError("Missing 'door' in form data")

        # Get the final choice from the form
        final_choice = int(request.form['door'])

        # Log the final choice for debugging
        app.logger.info(f"Final choice received: {final_choice}")

        # Validate the final choice
        if final_choice not in [1, 2, 3]:
            raise ValueError(f"Invalid door choice: {final_choice}")

        # Retrieve session variables
        prize_door = session.get('prize_door')
        initial_choice = session.get('initial_choice')

        # Log session variables for debugging
        app.logger.info(f"Session variables - Prize door: {prize_door}, Initial choice: {initial_choice}")

        # Validate session variables
        if prize_door is None or initial_choice is None:
            raise ValueError("Session variables 'prize_door' or 'initial_choice' are missing")

        # Determine if the user switched and if they won
        change = (final_choice != initial_choice)
        win = (final_choice == prize_door)

        # Simulate games (ensure this function is implemented correctly)
        results = simulate_games(change)

        # Log the simulation results
        app.logger.info(f"Simulation results: {results}")

        # Validate the results structure
        if not isinstance(results, dict) or 'win' not in results or 'lose' not in results:
            raise ValueError("Invalid results structure from simulate_games")

        # Render the result page
        return render_template('result.html', win=win, change=change, results=results)

    except Exception as e:
        # Log the error for debugging
        app.logger.error(f"Error in /result: {e}")
        return "An error occurred", 500
    
    
if __name__ == '__main__':
    # app.run(host='0.0.0.0', debug=True)
    # serve(app, host="0.0.0.0", port=80, debug=True)

    # for runinng locally
    # app.run(debug=True)
    # serve(app, host="0.0.0.0", port=80)

    #for running on the web
    app.run(host="0.0.0.0", debug=True)

