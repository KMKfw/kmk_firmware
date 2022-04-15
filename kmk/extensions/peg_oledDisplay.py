import busio
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306
from kmk.extensions import Extension
import gc

class oled(Extension):
    def __init__(
        self,
        board,
        views,
        toDisplay: str = "TXT",
        oWidth: int = 128,
        oHeight: int = 32,
        flip:bool = False,
        
    ):
        displayio.release_displays()
        self._views=views
        self._toDisplay = toDisplay
        i2c = busio.I2C(board.SCL, board.SDA)
        self.width=oWidth,
        self.height=oHeight,
        self.rotation = 180 if flip else 0
        self._display = adafruit_displayio_ssd1306.SSD1306(displayio.I2CDisplay(i2c, device_address=0x3C),
         width=oWidth,
         height=oHeight,rotation=self.rotation)
        self._prevLayers = 0
        gc.collect()

    def returnCurrectRenderText(self,layer,singleView):
        # for now we only have static things and react to layers. But when we react to battery % and wpm we can handle the logic here
        if singleView[0]=="STATIC":
                return singleView[1][0]
        if singleView[0]=="LAYER":
                return singleView[1][layer]
        
        
    def renderOledTextLayer(self, layer):
        splash = displayio.Group()
        self._display.show(splash)
        splash.append(
            label.Label(terminalio.FONT,
            text=self.returnCurrectRenderText(layer,self._views[0]),
            color=0xFFFFFF, x=0, y=10))
        splash.append(
            label.Label(terminalio.FONT,
            text=self.returnCurrectRenderText(layer,self._views[1]),
            color=0xFFFFFF, x=64, y=10))
        splash.append(
            label.Label(terminalio.FONT,
            text=self.returnCurrectRenderText(layer,self._views[2]),
            color=0xFFFFFF, x=0, y=25))
        splash.append(
            label.Label(terminalio.FONT,
            text=self.returnCurrectRenderText(layer,self._views[3]),
            color=0xFFFFFF, x=64, y=25))
        gc.collect()
            
    def renderOledImgLayer(self, layer):
        splash = displayio.Group()
        self._display.show(splash)
        odb = displayio.OnDiskBitmap('/'+self.returnCurrectRenderText(layer,self._views[0]))
        image = displayio.TileGrid(odb, pixel_shader=odb.pixel_shader)
        splash.append(image)
        gc.collect()
            
       

    def updateOLED(self, sandbox):
        if self._toDisplay == "TXT":
            self.renderOledTextLayer(sandbox.active_layers[0])
        if self._toDisplay == "IMG":
            self.renderOledImgLayer(sandbox.active_layers[0])
        gc.collect()
     

    def on_runtime_enable(self, sandbox):
        return

    def on_runtime_disable(self, sandbox):
        return

    def during_bootup(self, sandbox):
        self.renderOledImgLayer(0)
        return

    def before_matrix_scan(self, sandbox):
        if sandbox.active_layers[0] != self._prevLayers:
            self._prevLayers = sandbox.active_layers[0]
            self.updateOLED(sandbox)
        return

    def after_matrix_scan(self, sandbox):

        return

    def before_hid_send(self, sandbox):
        return

    def after_hid_send(self, sandbox):
        return

    def on_powersave_enable(self, sandbox):
        return

    def on_powersave_disable(self, sandbox):
        return