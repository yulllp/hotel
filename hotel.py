from nameko.rpc import rpc
import dependecies


class HotelService:
    name = 'merlynn_park_hotel'

    database = dependecies.Database()

    @rpc
    def get_hotel(self):
        hotel = self.database.get_hotel()
        return hotel
    
    @rpc
    def get_room_types(self):
        type = self.database.get_room_types()
        return type
    
    @rpc
    def get_room_type_by_id(self, id):
        type = self.database.get_room_type_by_id(id=id)
        return type
    
    @rpc
    def get_rooms(self):
        rooms = self.database.get_rooms()
        return rooms
    
    @rpc
    def get_rooms_by_type_id(self, id):
        rooms = self.database.get_rooms_by_type_id(id)
        return rooms
    
    @rpc
    def get_reservations(self):
        response = self.database.get_reservations()
        return response
    
    @rpc
    def get_reservation_by_id(self, id):
        response = self.database.get_reservation_by_id(id=id)
        return response
    
    @rpc
    def add_reservation(self, booking_id, type_room, check_in_date, check_out_date, total_room):
        response = self.database.add_reservation(booking_id=booking_id, type_room=type_room, check_in_date=check_in_date, check_out_date=check_out_date, total_room=total_room)
        return response
    
    @rpc
    def get_room_type_availability(self, check_in_date, check_out_date):
        response = self.database.get_room_type_availability(check_in_date=check_in_date, check_out_date=check_out_date)
        return response
    
    @rpc
    def get_room_type_availability_count_by_id(self, check_in_date, check_out_date, type_room):
        response = self.database.get_room_type_availability_count_by_id(check_in_date=check_in_date, check_out_date=check_out_date, type_room=type_room)
        return response