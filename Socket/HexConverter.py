import re
__author__ = 'ardzoht'

class HexConverter():
    #testing the info that is sent from the socket
    msg = 'F012W1000000000000000R11C100S1000000000A11000000R21C200S1000000000A12000000'

    def convert(self, message):
        return_str = ""
        if message[0] == 'F':
            f_data_hex = message[1:7]
            w_data_hex = message[8:40]
            f_data = "F"

            f_data += self.hex_to_str(f_data_hex)
            w_data = self.whex_to_str(w_data_hex)
            return_str += f_data+'W'+w_data+'R'

            no_of_areas = f_data[3]

            for index in xrange(int(no_of_areas)):
                r_data_hex = message[(41+(index*48)):45+(index*48)]
                r_data = self.hex_to_str(r_data_hex)
                return_str += r_data+'C'
                no_of_sensors = int(r_data[1])
                sc_data_hex = message[46+(index*48):52+(index*48)]
                sc_data = self.hex_to_str(sc_data_hex)
                return_str += sc_data+'S'
                for index2 in xrange(index,int(no_of_sensors)+index):
                    s_data_hex = message[53+(index2*48):72+(index2*48)]
                    s_data = self.hex_to_str(s_data_hex)
                    return_str += s_data+'A'

                    a_data_hex = message[74+(index2*48):88+(index*48)]
                    a_data = self.hex_to_str(a_data_hex)
                    return_str += a_data+'R'
            print return_str[:-1]
            return return_str[:-1]


    def hex_to_str(self, msg):
        new_str = ""
        for (first, second) in zip(msg[0::2], msg[1::2]):
            pair = first+second
            data = int(pair, 16)
            new_str += str(data)
        return new_str

    def whex_to_str(selfs, msg):
        node = str(int(msg[0:2], 16))
        radiation = str(int(msg[2:6], 16))
        humidity = str(int(msg[6:8], 16)) + str(int(msg[8:10], 16))
        temperature = str(int(msg[10:12], 16)) + str(int(msg[12:14], 16))
        wind = str(int(msg[14:16], 16)) + str(int(msg[16:18], 16))
        rain = str(int(msg[18:22], 16))
        eto = str(int(msg[22:24], 16)) + str(int(msg[24:26], 16))
        battery = str(int(msg[26:28], 16))
        rssi = str(int(msg[28:30], 16))
        error_c = str(int(msg[30:32], 16))
        new_str = node+radiation+humidity+temperature+wind+rain+eto+battery+rssi+error_c
        return new_str

