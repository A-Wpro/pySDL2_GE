'''

#DONE
    -button 100%
    -narative box 70%
    -Animator 15% 


#TODO
    -synchro button/animator
    -loader saver
    -settings
    -prototype
    -
    

'''


import sys
import sdl2
import sdl2.ext
import os
from sdl2.sdlttf import TTF_FontLineSkip
from sdl2.ext import FontTTF


BLACK = sdl2.ext.Color(0, 0, 0)
GREY = sdl2.ext.Color(30, 30, 30)
WHITE = sdl2.ext.Color(255, 255, 255)
class SoftwareRenderSystem(sdl2.ext.SoftwareSpriteRenderSystem):
    def __init__(self, window):
        super(SoftwareRenderSystem, self).__init__(window)

    def render(self, components):
        sdl2.ext.fill(self.surface, BLACK)
        super(SoftwareRenderSystem, self).render(components)


class TextureRenderSystem(sdl2.ext.TextureSpriteRenderSystem):
    def __init__(self, renderer):
        super(TextureRenderSystem, self).__init__(renderer)
        self.renderer = renderer

    def render(self, components):
        tmp = self.renderer.color
        self.renderer.color = BLACK
        self.renderer.clear()
        self.renderer.color = tmp
        super(TextureRenderSystem, self).render(components)


# A callback for the Button.motion event.
def onmotion(button, event):
    going_out = 0.2
    edge_right = (button.position[1]+button.surface.h-int(button.surface.h*going_out))
    edge_left = (button.position[0]+int(button.surface.w*going_out))
    edge_bot = (button.position[0]+button.surface.w-int(button.surface.w*going_out))
    edge_up = (button.position[1]+int(button.surface.h*going_out))
    if edge_bot < event.motion.x or  edge_right < event.motion.y or edge_left > event.motion.x or  edge_up > event.motion.y:
        button.surface = sdl2.ext.image.load_bmp(RESOURCES.get_path("button"+str(button.id)+".bmp"))
    else:
        button.surface = sdl2.ext.image.load_bmp(RESOURCES.get_path("button"+str(button.id)+"_hover.bmp"))

def del_all_button():
    global buttons
    buttons = []

    
    
# A callback for the Button.click event.
def onclick(button, event):
    global buttons
    global uifactory
    print("GO to ", + button.id_link)
    renderer = buttons[0].text_obj.renderer

    if button.id_link == 1 :
        
        del_all_button()
        btn_pos = (35,62)
        buttons.append(ge_create_button(uifactory,"button",1,btn_pos[0],btn_pos[1],4,text_box(renderer,"txt", posx = btn_pos[0], posy = btn_pos[1])))
                
                
    button.surface = sdl2.ext.image.load_bmp(RESOURCES.get_path("button"+str(button.id)+"_down.bmp"))

def onreleased(button, event):
    button.surface = sdl2.ext.image.load_bmp(RESOURCES.get_path("button"+str(button.id)+".bmp"))

def onpressed(button, event):
    button.surface = sdl2.ext.image.load_bmp(RESOURCES.get_path("button"+str(button.id)+"_down.bmp"))


def ge_create_button(uifactory, bname, id_compo, posx, posy, id_link, text_obj):
    button = uifactory.from_image(sdl2.ext.BUTTON,RESOURCES.get_path(bname+str(id_compo)+".bmp"),id_compo,id_link,text_obj)
    button.position = posx, posy
    
    button.motion += onmotion
    button.pressed += onpressed
    button.released += onreleased
    button.click += onclick
    button.text_obj.update_text()
    
    return button

stylesfont = ['default', 'small', 'red', 'large', 'bg_fill']
class text_box():
    def __init__(self, renderer, txt, styles = "default", fontname = "tuffy.ttf", color_text = BLACK, color_bg = WHITE ,posx=400, posy=400):
        self.renderer = renderer
        self.fontpath = RESOURCES.get_path(fontname)
        self.color_text = color_text
        self.color_bg = color_bg
        self.font = FontTTF(self.fontpath, "20px", self.color_text)
        self.line_height = TTF_FontLineSkip(self.font.get_ttf_font())
        self.alignments = ["left", "center", "right"]
        self.align_idx = 0
        self.style_idx = 0
        self.txt = txt
        self.posx = posx
        self.posy = posy
        self.styles = styles

    
    def __call__(self):
        # Add some additional font styles

        self.font.add_style('small', '10px', self.color_text)
        self.font.add_style('red', '20px', (255, 0, 0))
        self.font.add_style('large', '35px', self.color_text)
        #self.font.add_style('bg_fill', '20px', self.color_text, self.color_bg)
        


    def update_text(self):
        if "-hardware" in sys.argv:
            renderflags = (
                sdl2.SDL_RENDERER_ACCELERATED | sdl2.SDL_RENDERER_PRESENTVSYNC
            )
            
               
            factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=self.renderer)
        else:
            renderflags = sdl2.SDL_RENDERER_SOFTWARE
            factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)         
            renderer = self.renderer 
        # Create a texture for the surface and render it to the screen
        surface = self.font.render_text(self.txt, "default")
        sp = factory.from_surface(surface)
        sp.x = self.posx
        sp.y = self.posy
        return sp
 
def make_list_sprite(fname,nb_frame,factory):
    tmp = []
    for i in range(1,nb_frame):
        tmp.append(factory.from_image(RESOURCES.get_path(fname+str(i)+".bmp")))
    
    return tmp

    
class animasprite():
    def __init__(self,list_sprites,id_compo,index_sprite,pos_sprites):
        self.list_sprites = list_sprites
        self.nb_sprites = len(list_sprites)
        self.id_compo = id_compo
        self.index_sprite = index_sprite
        self.pos_sprites = pos_sprites
    
    def __call__(self):
        for sp in self.list_sprites:
            sp.x = self.pos_sprites[0]
            sp.y = self.pos_sprites[1]


    
def deep_bg(state, factory):
    bg_sprite = ""
    if state == 0:
        bg_sprite = factory.from_image(RESOURCES.get_path("bg.bmp"))
        bg_sprite.depth = -10
        return bg_sprite
    return factory.from_image(RESOURCES.get_path("bg.bmp"))
    
def all_txt_to_render(buttons,nara_box):
    tmp = []
    for btn in buttons:
        tmp.append(btn.text_obj.update_text())
    tmp.append(nara_box.update_text())
    return tmp
    
filepath = os.path.abspath(os.path.dirname(__file__))
RESOURCES = sdl2.ext.Resources(filepath, "resources")
global buttons 
global uifactory
buttons = []
uifactory = ""

    
def run():
    global frame_number 
    frame_number = 0
    global uifactory

    
    sdl2.ext.init()
    window = sdl2.ext.Window("UI Elements", size=(800, 600))
    window.show()
    world = sdl2.ext.World()
    
    if "-hardware" in sys.argv:
        print("Using hardware acceleration")
        renderflags = (
            sdl2.SDL_RENDERER_ACCELERATED | sdl2.SDL_RENDERER_PRESENTVSYNC
        )
        
        renderer = sdl2.ext.Renderer(window, flags=renderflags)  
        factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)
    else:
        print("Using software rendering")
        renderflags = sdl2.SDL_RENDERER_SOFTWARE
        factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)         
        renderer = sdl2.ext.Renderer(window, flags=renderflags)  

    if factory.sprite_type == sdl2.ext.SOFTWARE:
        spriterenderer = SoftwareRenderSystem(window)
    else:
        spriterenderer = TextureRenderSystem(renderer)
    world.add_system(spriterenderer)
    uifactory = sdl2.ext.UIFactory(factory)
###########-------------------- things that do not change go up
    


    
    #button
    for i in range(0,3):
        btn_pos = (20,i*75)
        buttons.append(ge_create_button(uifactory,"button",0,btn_pos[0],btn_pos[1],i,text_box(renderer,"Button" + str(i),posx = btn_pos[0], posy = btn_pos[1])))

    #anime
    ani1 = animasprite(make_list_sprite("sq",4,factory),5,1,(26,98))
        
    
        
      
    story = ["Hi There!\n this is text.","Next dial","Last Dial"]
    id_story=0
    txt = story[id_story]
    nara = text_box(renderer,txt,stylesfont[0], posx = 10, posy = 500)
    nara.update_text()
        
    spriterenderer = factory.create_sprite_render_system(window)


    uiprocessor = sdl2.ext.UIProcessor()

    running = True
    while running:
        if frame_number == 60:
            frame_number = 0
        else:
            frame_number += 1
        events = sdl2.ext.get_events()
        for event in events:
            update_txt = False
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            # Handle events
            elif event.type == sdl2.SDL_KEYDOWN:
                update_txt = True
                sdl_keysym = event.key.keysym.sym
                if sdl_keysym == sdl2.SDLK_RETURN:
                    id_story += 1
                    nara.txt = story[id_story]
            
    ### Update here (after event)
            # If txt has changed since the start of the loop, update the renderer
            if update_txt:
                nara.update_text()
            # Pass the SDL2 events to the UIProcessor, which takes care of
            # the user interface logic.

            uiprocessor.dispatch(buttons, event)


#### here we "print" on screen
            
            #----------- etoffer la gestion du nu index selon frame
        index_anim = 0
        if frame_number < 20:
            index_anim = 0
        elif frame_number >= 20 and frame_number < 40:
            index_anim = 2
        else:
            index_anim =-1
            #----------- etoffer la gestion du nu index selon frame

        # Render all user interface elements on the window.
        bg = [deep_bg(0,factory)]
        
        txt_to_render = all_txt_to_render(buttons,nara)
        txt_to_render.append(buttons[0].text_obj.update_text())
        to_render = bg  +  buttons + txt_to_render + [ani1.list_sprites[index_anim]]

        #to_render = to_render.sort(key=lambda x: x.depth)
        spriterenderer.render((to_render))


        

    # Now that we're done, close everything down and quit SDL2
    nara.font.close()
    renderer.destroy()
    window.close()
    sdl2.ext.quit()
    return 0



if __name__ == "__main__":
    sys.exit(run())
