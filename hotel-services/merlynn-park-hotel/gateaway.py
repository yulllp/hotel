import json
from nameko.rpc import RpcProxy
from nameko.web.handlers import http

class GatewayService:
    name = 'gateaway'

    hotel_rpc = RpcProxy('merlynn_park_hotel')

    @http('GET', '/merlynn_park_hotel')
    def get_hotel(self, request):
        hotel = self.hotel_rpc.get_hotel()
        return json.dumps(hotel)
    
    @http('GET', '/merlynn_park_hotel/room_type')
    def get_room_types(self, request):
        type = self.hotel_rpc.get_room_types()
        return json.dumps(type)
    
    @http('GET', '/merlynn_park_hotel/room_type/<int:id>')
    def get_room_types(self, request, id):
        type = self.hotel_rpc.get_room_type_by_id(id=id)
        return json.dumps(type)
    
    @http('GET', '/merlynn_park_hotel/rooms')
    def get_rooms(self, request):
        rooms = self.hotel_rpc.get_rooms()
        return json.dumps(rooms)
    
    @http('GET', '/merlynn_park_hotel/room_type/<int:id>/rooms')
    def get_rooms_by_type_id(self, request, id):
        rooms = self.hotel_rpc.get_rooms_by_type_id(id=id)
        return json.dumps(rooms)
    
    @http('GET', '/merlynn_park_hotel/reservation')
    def get_reservations(self, request):
        response = self.hotel_rpc.get_reservations()
        return json.dump(response)
    
    @http('GET', '/merlynn_park_hotel/reservation/<int:id>')
    def get_reservations(self, request, id):
        response = self.hotel_rpc.get_reservations_by_id(id=id)
        return json.dumps(response)
    
    #booking service
    @http('POST', '/merlynn_park_hotel/reservation')
    def add_reservation(self, request, type_room, check_in_date, check_out_date, total_room):
        data = request.get_data(as_text=True)
        booking_data = json.loads(data)
        booking_id = booking_data.get('booking_id')
        check_in_date = booking_data.get('check_in_date')
        check_out_date = booking_data.get('check_out_date')
        type_room = booking_data.get('type_id')
        total_room = booking_data.get('total_room')
        response = self.hotel_rpc.add_reservation(type_room=type_room, check_in_date=check_in_date, check_out_date=check_out_date, total_room=total_room)
        return json.dumps(response)
    
    @http('GET', '/merlynn_park_hotel/room_type/<string:check_in_date>&<string:check_out_date>&<int:id>')
    def get_room_type_availability_count_by_id(self, request, check_in_data, check_out_date, type_room):
        response = self.hotel_rpc.get_room_type_availability_count_by_id(check_in_data=check_in_data, check_out_date=check_out_date, type_room=type_room)
        return json.dumps(response)
    
    #search service
    @http('GET', '/merlynn_park_hotel/room_type/<string:check_in_date>&<string:check_out_date>')
    def get_room_type_availability(self, request, check_in_data, check_out_date):
        response = self.hotel_rpc.get_room_type_availability(check_in_data=check_in_data, check_out_date=check_out_date)
        return json.dumps(response)