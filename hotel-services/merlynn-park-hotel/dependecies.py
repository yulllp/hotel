from datetime import date
from decimal import Decimal
from nameko.extensions import DependencyProvider

import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling

class DatabaseWrapper:

    connection = None

    def __init__(self, connection):
        self.connection = connection
    
    #access hotel data
    #get hotel detail
    def get_hotel(self):
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT * FROM hotel"
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        return self.convert_dates_to_strings(result)
    
    #get all room type
    def get_room_types(self):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        sql = "SELECT * FROM room_type rt"
        cursor.execute(sql)
        for row in cursor.fetchall():
        # Convert any Decimal objects to floats
            for key, value in row.items():
                if isinstance(value, Decimal):
                    row[key] = float(value)
            result.append(row)
        self.connection.commit()
        cursor.close()
        return self.convert_dates_to_strings(result)
    
    #get room type by id
    def get_room_type_by_id(self, id):
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT * FROM room_type rt WHERE rt.id = %s"
        cursor.execute(sql, (id,))
        result = cursor.fetchone()
        self.connection.commit()
        cursor.close()
        return self.convert_dates_to_strings(result)
    
    #get all room
    def get_rooms(self):
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT * FROM room r"
        cursor.execute(sql)
        result = cursor.fetchone()
        self.connection.commit()
        cursor.close()
        return self.convert_dates_to_strings(result)
    
    #get rooms by type id
    def get_rooms_by_type_id(self, id):
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT * FROM room r LEFT JOIN room_type rt WHERE rt.id = %s"
        cursor.execute(sql, (id,))
        result = cursor.fetchone()
        self.connection.commit()
        cursor.close()
        return self.convert_dates_to_strings(result)
    
    #get all reservation with its reservation rooms 
    def get_reservations(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            result = []
            reservations = {}
            sql = "SELECT r.id, r.booking_id, r.check_in_date, r.check_out_date, rr.room_id, ro.number FROM reservation r JOIN resv_room rr ON r.id = rr.resv_id JOIN room ro ON rr.room_id = ro.id"
            cursor.execute(sql)
            for row in cursor.fetchall():
                reservation_id = row['id']
                if reservation_id not in reservations:
                    reservations[reservation_id] = {
                        'id': row['id'],
                        'booking_id': row['booking_id'],
                        'check_in_date': row['check_in_date'].strftime('%Y-%m-%d'),
                        'check_out_date': row['check_out_date'].strftime('%Y-%m-%d'),
                        'rooms': []
                    }
                room_details = {
                    'room_id': row['room_id'],
                    'number': row['number']
                }
                reservations[reservation_id]['rooms'].append(room_details)
            result = list(reservations.values())
            self.connection.commit()
            cursor.close()
            return result

        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    #get reservation with its reservation rooms by id
    def get_reservation_by_id(self, id):
        try:
            cursor = self.connection.cursor(dictionary=True)
            reservation = None
            sql = "SELECT r.id, r.booking_id, r.check_in_date, r.check_out_date, rr.room_id, ro.number FROM reservation r JOIN resv_room rr ON r.id = rr.resv_id JOIN room ro ON rr.room_id = ro.id WHERE r.id = %s"
            cursor.execute(sql, (id,))
            for row in cursor.fetchall():
                if reservation is None:
                    reservation = {
                        'id': row['id'],
                        'booking_id': row['booking_id'],
                        'check_in_date': row['check_in_date'].strftime('%Y-%m-%d'),
                        'check_out_date': row['check_out_date'].strftime('%Y-%m-%d'),
                        'rooms': []
                    }
                room_details = {
                    'room_id': row['room_id'],
                    'number': row['number']
                }
                reservation['rooms'].append(room_details)
            self.connection.commit()
            cursor.close()
            return reservation

        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    
    #for booking service
    #add new reservation
    def add_reservation(self, booking_id, type_room, check_in_date, check_out_date, total_room):
        # try:
            #find available room based on check in & out date and room type
            cursor = self.connection.cursor(dictionary=True)
            result = []
            sql = """
                SELECT r.* FROM room_type rt JOIN room r ON rt.id = r.type_id WHERE rt.id = %s AND r.id NOT IN 
                ( SELECT rr.room_id FROM resv_room rr JOIN reservation resv ON rr.resv_id = resv.id 
                WHERE resv.check_in_date < %s AND resv.check_out_date > %s )
                """
            cursor.execute(sql, (type_room, check_out_date, check_in_date))
            for row in cursor.fetchall():
                 result.append(row)
            
            #insert new reservation data
            sql = "INSERT INTO reservation (booking_id, check_in_date, check_out_date) VALUES (%s, %s, %s)"
            cursor.execute(sql, (booking_id, check_in_date, check_out_date))
            id = cursor.lastrowid

            #assign new room for the new reservation
            sql = "INSERT INTO resv_room (resv_id, room_id) VALUES (%s, %s)"
            for i, room in enumerate(result):
                if i < total_room:
                    print(room)
                    cursor.execute(sql, (id, room['id']))
                else:
                    break
            self.connection.commit()
            cursor.close()
            return {'message': 'reservation created successfully','status': 200}
        
        # except Exception as e:
            # error_message = str(e)
            # return {'error': error_message}
    
    #get the quantity of available rooms for re-checking before booking
    def get_room_type_availability_count_by_id(self, check_in_date, check_out_date, type_room):
        #find available room based on check in & out date and room type
        cursor = self.connection.cursor(dictionary=True)
        result = []
        count = 0
        sql = """
                SELECT r.* FROM room_type rt JOIN room r ON rt.id = r.type_id WHERE rt.id = %s AND r.id NOT IN 
                ( SELECT rr.room_id FROM resv_room rr JOIN reservation resv ON rr.resv_id = resv.id 
                WHERE resv.check_in_date < %s AND resv.check_out_date > %s )
                """
        cursor.execute(sql, (type_room, check_out_date, check_in_date))
        for row in cursor.fetchall():
                result.append(row)
        for i in result:
            count += 1
        
        self.connection.commit()
        cursor.close()
        return count
    
    #for searching service
    #get all room type data with the total available rooms
    def get_room_type_availability(self, check_in_date, check_out_date):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        data = self.get_room_types() 
        for row in data:
            count = 0
            #find available room based on check in & out date and room type
            sql = """
                SELECT r.* FROM room_type rt JOIN room r ON rt.id = r.type_id WHERE rt.id = %s AND r.id NOT IN 
                ( SELECT rr.room_id FROM resv_room rr JOIN reservation resv ON rr.resv_id = resv.id 
                WHERE resv.check_in_date < %s AND resv.check_out_date > %s )
                """
            cursor.execute(sql, (row['id'], check_out_date, check_in_date))

            #count each room_types availability
            for i in cursor.fetchall():
                count += 1
            result.append(count)

        #combine the data with the total available room
        for index, room in enumerate(data):
            room['available_room'] = result[index]

        return self.convert_dates_to_strings(data)
    
    def convert_dates_to_strings(self, data):
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, date):
                    data[key] = value.isoformat()
        return data

class Database(DependencyProvider):

    connection_pool = None

    def __init__(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="database_pool",
                pool_size=10,
                pool_reset_session=True,
                host='localhost',
                database='merlynn_park_hotel',
                user='root',
                password=''
            )
        except Error as e :
            print ("Error while connecting to MySQL using Connection pool ", e)

    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())