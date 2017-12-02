from time import sleep
from threading import Barrier
import pifacecommon
import pifacecad
from query_historical_data_lite import historical_data
from fetch_new_lottery_info import saveNewData2DB
from predictor_ss_lite import predictor_ss

class lottery_display(object):
    def __init__(self, cad, stations, station_index=0):
        #self.stations = stations
        #self.station_index = station_index
        self.cad = cad
        #self.cad.lcd.store_custom_bitmap(TEMP_SYMBOL_INDEX, TEMP_SYMBOL)
        #self.cad.lcd.store_custom_bitmap(WIND_SYMBOL_INDEX, WIND_SYMBOL)
        self.cad.lcd.backlight_on()
        self.cad.lcd.blink_off()
        self.cad.lcd.cursor_off()

    @property
    def current_station(self):
        """Returns the current station dict."""
        return self.stations[self.station_index]

    def fetch_new_data(self, event=None):
        newdatacount = saveNewData2DB(50)
        #self.station_index = (self.station_index + 1) % len(self.stations)
        top_line =""
        bottom_line=""
        if newdatacount < 1:
            top_line = "No data updated!"
        else:
            top_line ="New data :"
            bottom_line =  "Add :" +str(newdatacount)+" data"
        self.update(top_line,bottom_line)

    def previous_station(self, event=None):
        self.station_index = (self.station_index - 1) % len(self.stations)
        self.update()

    def update(self, top_line,bottom_line,event=None):
        self.cad.lcd.clear()
        self.cad.lcd.set_cursor(0, 0)
        self.cad.lcd.write(top_line)
        self.cad.lcd.set_cursor(0, 1)
        self.cad.lcd.write(bottom_line)

    def close(self):
        self.cad.lcd.clear()
        self.cad.lcd.backlight_off()

def generate_txt(rs):
    #rs = historical_data.get_all_data()
    #drinks['beer_servings'] = drinks.beer_servings.astype(float)
    #df =df.Series([2:8], dtype='int64')
    df = DataFrame(rs).sort_index(ascending=False)
    df[2] = df[2].astype('int64')
    df[3] = df[3].astype('int64')
    df[4] = df[4].astype('int64')
    df[5] = df[5].astype('int64')
    df[6] = df[6].astype('int64')
    df[7] = df[7].astype('int64')
    df[8] = df[8].astype('int64')
    df.insert(0, 'year', df[0].astype(str).str[:4])

    #print (df.head(5))
    #df.insert(0, 'year', dfi)
    #df = DataFrame(rs)
    df.to_csv(r'./123.txt', header=None, index=True, sep=' ', mode='w',encoding ='utf-8')


if __name__ == "__main__":

        debug = 1
        startNo = ''
        endNo = ''
        singleY = ''

        if debug: print('update new 50 records to db ')
        newdatacount = saveNewData2DB(50)

        if debug: print('fetch records based on user option ')
        historical_data = historical_data()

        rs = []

        if startNo != '' and endNo != '':
            rs = historical_data.get_data_indentifier_range(startNo, endNo)
        elif singleY != '':
            rs = historical_data.get_one_year_data(singleY)
        else:
            rs = historical_data.get_all_data()
        if debug: print('generate txt file ')
        generate_txt(rs)
        if debug: print('predictor_ss')
        b = predictor_ss()
        b.init_data()
        print_all(b)




    cad = pifacecad.PiFaceCAD()
    global lotterydisplay
    lotterydisplay = lottery_display(cad, stations)
    lotterydisplay.update()

    # listener cannot deactivate itself so we have to wait until it has
    # finished using a barrier.
    global end_barrier
    end_barrier = Barrier(2)

    # wait for button presses
    switchlistener = pifacecad.SwitchEventListener(chip=cad)
    switchlistener.register(4, pifacecad.IODIR_ON, end_barrier.wait)
    switchlistener.register(5, pifacecad.IODIR_ON, lotterydisplay.update)
    switchlistener.register(
        6, pifacecad.IODIR_ON, lotterydisplay.previous_station)
    switchlistener.register(
        7, pifacecad.IODIR_ON, lotterydisplay.fetch_new_data)

    switchlistener.activate()
    end_barrier.wait()  # wait unitl exit

    # exit
    lotterydisplay.close()
    switchlistener.deactivate()
