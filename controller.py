from vpython import keysdown, scene, slider, rate, wtext, button, color, vec
from Layers.iso_layer import IsoLayer
from utils.draw_utils import KB_ROW_1, KB_ROW_2


class Controller:
    def __init__(self, layers=[]):
        # self.toggle_M = True
        self.layers = layers

        self.clayer = None

        self.sim_speed = slider(min=1, max=50, value=25, length=220, 
                                bind=self._set_rate, right=15)
        self.mtext = wtext(text=f"{self.sim_speed.value}\t")

        self.layertext = wtext(text="")

        self.clayer_bfuncs = []
        self.clayer_cfuncs = []

        self.action_kt = KeyTracker(key='x')
        self.c = 'c'



    def _set_rate(self, rate):
        self.mtext.text = f"{self.sim_speed.value}\t"


    def control(self):
        self.clayer : IsoLayer

        KD = keysdown()

        if 'p' in KD:
            for ob in scene.objects:
                print(ob)
                print(ob.opacity)

        rate(self.sim_speed.value)

        # self.tog_u.disabled = True
        # self.tog_vis.disabled = True
        # self.layertext.text = ''

        for n in range(len(self.layers)):
            nc = str(n+1)
            if nc in KD:
                self.clayer = self.layers[n]
                self.generate_button_array()


        if self.clayer != None:
            self.layertext.text = f'selected: layer_{nc} - updating={self.clayer.updating} - '
        
        r1_key = None
        r2_key = None

        for i, ch in enumerate(KB_ROW_2):
            if ch in KD:
                r2_key = i
        for i, ch in enumerate(KB_ROW_1):
            if ch in KD:
                r1_key = i

        
        for i, btn in enumerate(self.clayer_bfuncs):
            btn : button
            val = 1 / (i+1)
            btn.background = color.gray(0.5)
            # btn.background = color.hsv_to_rgb(vec(val,1,1))
            if i == r2_key:
                # print(btn.text)
                btn.text = btn.text
                btn.background = color.cyan

                if self.action_kt.register():
                    btn.background = color.red
                    btn.bind(mock_evt(btn.text))


        for i, btn in enumerate(self.clayer_cfuncs):
            btn : button
            val = 1 / (i+1)
            btn.background = color.gray(0.3)
            # btn.background = color.hsv_to_rgb(vec(val,1,1))
            if i == r1_key:
                # print(btn.text)
                btn.text = btn.text
                btn.background = color.cyan

                if self.c in KD:
                    btn.background = color.blue
                    btn.bind(mock_evt(btn.text))


            # self.tog_u.disabled = Falseaa
            # self.tog_vis.disabled = False
            
            # modval = round(self.clayer.mod_M,4)
            # if 'm' in KD:
            #     self.layertext.text += f' M = {modval}\t'
            #     if 'down' in KD:
            #         self.clayer.mod_M -= 0.01
            #     if 'up' in KD:
            #         self.clayer.mod_M += 0.01
                # self.clayer.mod_M = scene.mouse().pos.mag

        
    def proxy_layer_call(self, evt):
        if self.clayer != None:
            b_func = getattr(self.clayer, evt.text)
            b_func()
        

    def generate_button_array(self):
        for b in self.clayer_bfuncs:
            b : button
            b.delete()
        self.clayer_bfuncs.clear()

        object_methods = [method_name for method_name in dir(self.clayer)
                if callable(getattr(self.clayer, method_name)) and method_name[1] == 'b' and method_name[0] == '_']
        for label in object_methods:
 
            self.clayer_bfuncs.append(
                button(text=label, bind=self.proxy_layer_call)
            )
        


        for c in self.clayer_cfuncs:
            c : button
            c.delete()
        self.clayer_cfuncs.clear()

        object_methods = [method_name for method_name in dir(self.clayer)
                if callable(getattr(self.clayer, method_name)) and method_name[1] == 'c' and method_name[0] == '_']
        for label in object_methods:
 
            self.clayer_cfuncs.append(
                button(text=label, bind=self.proxy_layer_call)
            )


# import time
class KeyTracker():
    def __init__(self, key=' '):
        self.key = key
        self.held = False

    def register(self):
        # print(keysdown())a
        if self.key in keysdown() and not self.held:
            self.held = True
            return True
        elif self.held and self.key not in keysdown():
            self.held = False
        return False



class mock_evt:
    def __init__(self, text):
        self.text=text

