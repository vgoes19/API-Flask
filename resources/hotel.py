from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required


class Hoteis(Resource):
    def get(self):
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}

class Hotel(Resource):

    #Arguments required for hotel
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="Name is required")
    argumentos.add_argument('estrelas', type=float, required=True, help="Stars is required")
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')


    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found'}, 404 #not found
    
    @jwt_required()
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel ID '{}' already exists".format(hotel_id)}, 400 #bad request

        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save'}, 500 #internal server error
        return hotel.json()


    @jwt_required()
    def put(self, hotel_id):

        dados = Hotel.argumentos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)

        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200 #success
        hotel = HotelModel(hotel_id, **dados) #embrulhando os dados com **kwargs
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save'}, 500 #internal server error
        return hotel.json, 201 #created
    

    @jwt_required()
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'An internal error ocurred trying to delete'}, 500 #internal server error
            return {'message': 'Hotel deleted'}
        return {'message': 'Hotel not found'}, 404