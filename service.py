from flask import Flask, jsonify, request, render_template, url_for
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError
from models import User, Advertisement, Session

app = Flask('test_application')

class HtttpError(Exception):
	def __init__(self, status_code: int, message: str):
		self.status_code = status_code
		self.message = message

@app.errorhandler(HtttpError)
def error_handler(error: HtttpError):
	response = jsonify({'error': error.message})
	response.status_code = error.status_code
	return response

def get_user_by_id(user_id):
	user = request.session.get(User, user_id)
	if user is None :
		raise HtttpError(status_code=404, message='user is None')
	return user

def add_user(user: User):
	try:
		request.session.add(user)
		request.session.commit()
	except IntegrityError : 
		raise HtttpError(status_code=409, message='user already exists')

def get_adv_by_id(adv_id):
	adv = request.session.get(Advertisement, adv_id)
	if adv is None :
		raise HtttpError(status_code=404, message='advertisement is None')
	return adv

def add_adv(adv: Advertisement):
	try:
		request.session.add(adv)
		request.session.commit()
	except IntegrityError :
		raise HtttpError(status_code=409, message='error')


@app.before_request
def before_request():
	session = Session()
	request.session = session
						
@app.after_request
def after_request(response):
	request.session.close()
	return response

					
class UserView(MethodView):
	
    @property
    def session(self):
        return request.session
	
    def get(self, user_id):
        user = get_user_by_id(user_id)
        return jsonify(user.make_dict)

    def post(self):
        json_data = request.json     
        user = User(**json_data)        
        add_user(user)
        return jsonify(user.make_dict)

class AdvertisementView(MethodView):
	
    @property
    def session(self):
        return request.session

    def get(self, adv_id):
        adv = get_adv_by_id(adv_id)
        return jsonify(adv.make_dict)

    def post(self):
        json_data = request.json     
        adv = Advertisement(**json_data)        
        add_adv(adv)
        return jsonify(adv.make_dict)

    def delete(self, adv_id):
        adv = get_adv_by_id(adv_id)
        self.session.delete(adv)
        self.session.commit()
        return jsonify(adv.make_dict)



user_view = UserView.as_view('user_view')
adv_view = AdvertisementView.as_view('adv_view')


app.add_url_rule(rule='/user/<int:user_id>/', view_func=user_view, methods=['GET'])
app.add_url_rule(rule='/user/', view_func=user_view, methods=['POST'])

app.add_url_rule(rule='/advertisement/<int:adv_id>/', view_func=adv_view, methods=['GET', 'DELETE'])
app.add_url_rule(rule='/advertisement/', view_func=adv_view, methods=['POST'])


if __name__=='__main__':
    app.run()