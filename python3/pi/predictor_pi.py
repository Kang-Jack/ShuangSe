from threading import Barrier
import pifacecad
import  utils
from query_historical_data_lite import historical_data
from fetch_new_lottery_info import saveNewData2DB
from predictor_ss_lite import predictor_ss

class lottery_display(object):
    def __init__(self, cad):
        #self.stations = stations
        #self.station_index = station_index
        self.cad = cad
        #self.cad.lcd.store_custom_bitmap(TEMP_SYMBOL_INDEX, TEMP_SYMBOL)
        #self.cad.lcd.store_custom_bitmap(WIND_SYMBOL_INDEX, WIND_SYMBOL)
        self.cad.lcd.backlight_on()
        self.cad.lcd.blink_off()
        self.cad.lcd.cursor_off()
        self.historical_data = historical_data()
    @property
    def current_station(self):
        """Returns the current station dict."""
        return self.stations[self.station_index]

    def update_db(self, event=None):
        if debug: print('fetch records based on user option ')
        self.update("fetch","records")
        newdatacount = saveNewData2DB(50)
        #self.station_index = (self.station_index + 1) % len(self.stations)
        top_line =""
        if debug: print('generate txt file ')

        rs = []
        rs = self.historical_data.get_all_data()
        self.generate_txt(rs)
        bottom_line=""
        if newdatacount < 1:
            top_line = "No data updated!"
        else:
            top_line ="New data :"
            bottom_line =  "Add :" +str(newdatacount)+" data"
        self.update(top_line,bottom_line)

    def random_draw(self,event=None):
        if debug: print('predictor_ss')
        self.update("random","draw")
        b = predictor_ss()
        b.init_data()
        rs =  b.print_random()
        top_line,bottom_line = format_str(rs,"RAND")

        self.update(top_line,bottom_line)

    def best_draw(self,event=None):
        if debug: print('predictor_ss')
        self.update("best","draw")
        b = predictor_ss()
        b.init_data()
        rs = b.print_best_number()
        top_line, bottom_line = format_str(rs, "MAX")
        self.update(top_line,bottom_line)

    def update(self,top_line,bottom_line):
        self.cad.lcd.clear()
        self.cad.lcd.set_cursor(0, 0)
        self.cad.lcd.write(top_line)
        self.cad.lcd.set_cursor(0, 1)
        self.cad.lcd.write(bottom_line)

    def close(self):
        self.cad.lcd.clear()
        self.cad.lcd.backlight_off()


if __name__ == "__main__":

    debug = 1

    cad = pifacecad.PiFaceCAD()
    global lotterydisplay
    lotterydisplay = lottery_display(cad)
    lotterydisplay.update("display","inited")

    # listener cannot deactivate itself so we have to wait until it has
    # finished using a barrier.
    global end_barrier
    end_barrier = Barrier(2)

    # wait for button presses
    switchlistener = pifacecad.SwitchEventListener(chip=cad)
    switchlistener.register(4, pifacecad.IODIR_ON, end_barrier.wait)
    switchlistener.register(5, pifacecad.IODIR_ON, lotterydisplay.best_draw)
    switchlistener.register(
        6, pifacecad.IODIR_ON, lotterydisplay.random_draw)
    switchlistener.register(
        7, pifacecad.IODIR_ON, lotterydisplay.update_db)

    switchlistener.activate()
    end_barrier.wait()  # wait unitl exit

    # exit
    lotterydisplay.close()
    switchlistener.deactivate()
