import sys
import sdl2
import sdl2.ext

"""
#dial
import os
import sys
import sdl2.ext
from sdl2.sdlttf import TTF_FontLineSkip
from sdl2.ext import FontTTF

filepath = os.path.abspath(os.path.dirname(__file__))
RESOURCES = sdl2.ext.Resources(filepath, "resources")
BLACK_RGBA = (0, 0, 0, 255)
WHITE_RGBA = (255, 255, 255, 255)


def update_text(renderer, surface):
    # Create a texture for the surface and render it to the screen
    tx = sdl2.ext.Texture(renderer, surface)
    renderer.clear(BLACK_RGBA)
    renderer.copy(tx, dstrect=(10, 10)) # here to modify position of text
    renderer.present()


def run():
    # Initialize SDL2 and create a Window and Renderer
    sdl2.ext.init()
    window = sdl2.ext.Window("Font Rendering", size=(800, 500))
    renderflags = sdl2.SDL_RENDERER_SOFTWARE
    if "-hardware" in sys.argv:
        renderflags = (
            sdl2.SDL_RENDERER_ACCELERATED | sdl2.SDL_RENDERER_PRESENTVSYNC
        )
    renderer = sdl2.ext.Renderer(window, flags=renderflags)
    window.show()

    # Create and initialize a font to render text with
    fontpath = RESOURCES.get_path("tuffy.ttf")
    font = FontTTF(fontpath, "20px", WHITE_RGBA)

    # Add some additional font styles
    styles = ['default', 'small', 'red', 'large', 'bg_fill']
    font.add_style('small', '10px', WHITE_RGBA)
    font.add_style('red', '20px', (255, 0, 0))
    font.add_style('large', '35px', WHITE_RGBA)
    font.add_style('bg_fill', '20px', BLACK_RGBA, WHITE_RGBA)

    # Initialize font rendering options
    line_height = TTF_FontLineSkip(font.get_ttf_font())
    alignments = ["left", "center", "right"]
    align_idx = 0
    style_idx = 0
    
    story = ["Hi There!\n this is text.","Next dial","Last Dial"]
    id_story=0
    # Set a default string with which to render text
    txt = story[id_story]

    # Render the text and present it on the screen
    txt_rendered = font.render_text(txt, width=780)
    update_text(renderer, txt_rendered)

    # Tell SDL2 to start reading Text Editing events. This allows for proper
    # handling of unicode characters and modifier keys.
    sdl2.SDL_StartTextInput()

    # Create a simple event loop and wait for keydown, text editing, and quit events.
    running = True
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            update_txt = False
            if event.type == sdl2.SDL_QUIT:
                running = False
                break

            # Handle non-standard keyboard events
            elif event.type == sdl2.SDL_KEYDOWN:
                update_txt = True
                sdl_keysym = event.key.keysym.sym
                if sdl_keysym == sdl2.SDLK_RETURN:
                    id_story += 1
                    txt = story[id_story]
               

            # If txt has changed since the start of the loop, update the renderer
            if update_txt:
                align = alignments[align_idx]
                style = styles[style_idx]
                txt_rendered = font.render_text(
                    txt, style, width=780, line_h=line_height, align=align
                )
                update_text(renderer, txt_rendered)

    # Now that we're done, close everything down and quit SDL2
    font.close()
    renderer.destroy()
    window.close()
    sdl2.ext.quit()
    return 0

if __name__ == "__main__":
    sys.exit(run())


"""

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
