import random
import os

from flask import(
	Flask, 
	request, session,
	url_for, render_template, redirect, abort
)

#Create a Flask application object
app = Flask(__name__)

# session variable are stored clien-side(on the user´s browser).
# The content of these variables is encrypted, so users can´t actually
# read this contents. They could edit the session data, but because it 
# would ot be "signed" whit the secrecret key below, the server would
# reject is as invalid.
# You need to set a secret key (random text) and keep it secret!
app.secret_key = '123456789'

"""The path to the directory containing our images.
we will store a list of image file names in a session variable."""
IMAGE_DIR = app.static_folder

#####################
## Helper functions##
#####################

def init_game():
	#initialize a new deck (a list of filenames)
	image_name = os.listdir(IMAGE_DIR)
	#shuffle the deck
	random.shuffle(image_name) # modifica sobre la misma lista
	#store in the user´s session
	#session is a special global object that Flask provides
	#which exposes the basic session management functionality
	session['images'] = image_name

def select_from_deck():
	try:
		image_name = session['images'].pop()
	except indexError:
		image_name = None #Sentinel
	return image_name


#####################
### View functions###
#####################

@app.route('/' )
def index():
	init_game()
	return render_template("index.html")

@app.route('/draw')
def draw_card():
	if 'images' not in session:
		abort(400)
	image_name = select_from_deck()
	if image_name is None:
		return render_template("gameover.html")
	return render_template("showcard.html", image_name=image_name)

if __name__ == '__main__':
	app.run(debug=False)




