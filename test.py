import sys
import sdl2
import sdl2.ext


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
    
# A callback for the Button.click event.
def onclick(button, event):
    button.surface = sdl2.ext.image.load_bmp(RESOURCES.get_path("button"+str(button.id)+"_down.bmp"))

def onreleased(button, event):
    button.surface = sdl2.ext.image.load_bmp(RESOURCES.get_path("button"+str(button.id)+".bmp"))

def onpressed(button, event):
    button.surface = sdl2.ext.image.load_bmp(RESOURCES.get_path("button"+str(button.id)+"_down.bmp"))

def onnoevent(button, event):
    print("no event")

def ge_create_button(uifactory, bname, id_compo, posx, posy):
    button = uifactory.from_image(sdl2.ext.BUTTON,RESOURCES.get_path(bname+str(id_compo)+".bmp"),id_compo)
    button.position = posx, posy
    
    button.motion += onmotion
    button.pressed += onpressed
    button.released += onreleased
    button.click += onclick
    
    return button


RESOURCES = sdl2.ext.Resources(__file__, "resources")
def run():

    sdl2.ext.init()
    window = sdl2.ext.Window("UI Elements", size=(800, 600))
    window.show()

    if "-hardware" in sys.argv:
        print("Using hardware acceleration")
        renderer = sdl2.ext.Renderer(window)
        factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)
    else:
        print("Using software rendering")
        factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)

   
    uifactory = sdl2.ext.UIFactory(factory)

    buttons = []
    
    for i in range(0,3):
        buttons.append(ge_create_button(uifactory,"button",i,20,i*75))

    


    spriterenderer = factory.create_sprite_render_system(window)


    uiprocessor = sdl2.ext.UIProcessor()

    running = True
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            # Pass the SDL2 events to the UIProcessor, which takes care of
            # the user interface logic.
            uiprocessor.dispatch(buttons, event)

        # Render all user interface elements on the window.
        spriterenderer.render((buttons))

    sdl2.ext.quit()
    return 0


if __name__ == "__main__":
    sys.exit(run())