from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()
grass_texture = load_texture('assets/grass_block.png')
stone_texture = load_texture('assets/stone_block.png')
brick_texture = load_texture('assets/brick_block.png')
dirt_texture = load_texture('assets/dirt_block.png')
sky_texture = load_texture('assets/skybox.png')
arm_texture = load_texture('assets/arm_texture.png')
punch_sound = Audio('assets/punch_sound', loop=False, autoplay=False)


block_pick = 1
chunk = 13

window.title = 'Minecraft Python Edition'


def update():
	global block_pick

	if held_keys['left mouse'] or held_keys['right mouse']:
		hand.active()
	else:
		hand.passive()

	if held_keys['1']: block_pick = 1
	if held_keys['2']: block_pick = 2
	if held_keys['3']: block_pick = 3
	if held_keys['4']: block_pick = 4


class Voxel(Button):
	def __init__(self, position = (0,0,0), texture = grass_texture):
		super().__init__(
			parent = scene,
			position = position,
			model = 'assets/block',
			origin_y = 0.5,
			texture = texture,
			color = color.color(0,0,random.uniform(0.9,1)),
			scale = 0.5)

	def input(self,key):
		if self.hovered:
			if key == 'left mouse down':
			
				punch_sound.play()
				
				if block_pick == 1: 
					voxel = Voxel(position = self.position + mouse.normal, texture = grass_texture)
				if block_pick == 2: 
					voxel = Voxel(position = self.position + mouse.normal, texture = stone_texture)
				if block_pick == 3: 
					voxel = Voxel(position = self.position + mouse.normal, texture = brick_texture)
				if block_pick == 4: 
					voxel = Voxel(position = self.position + mouse.normal, texture = dirt_texture)
                
			if key == 'right mouse down':
				punch_sound.play()
				destroy(self)

class Sky(Entity):
	def __init__(self):
		super().__init__(
			parent = scene,
			model = 'sphere',
			texture = sky_texture,
			scale = 150,
			double_sided = True)

class Hand(Entity):
	def __init__(self):
		super().__init__(
			parent = camera.ui,
			model = 'assets/arm',
			texture = arm_texture,
			scale = 0.2,
			rotation = Vec3(150,-10,0),
			position = Vec2(0.4,-0.6))

	def active(self):
		self.position = Vec2(0.3,-0.5)

	def passive(self):
		self.position = Vec2(0.4,-0.6)

class Inventory(Entity):
    def __init__(self):
        super().__init__(
			parent = camera.ui,
			model ='quad',
			scale =(.5, .8),
			origin =(-.5, .5),
			position = (-.3, .4),
            texture = 'white_cube',                                     
            texture_scale = (5,8),                                      
            color = color.dark_gray 
		)
        self.item_parent = Entity(parent=self, scale=(1/5,1/8))   
        
    def append(self, item):
        icon = Draggable(                                                  
            parent = inventory.item_parent,
            model = 'quad',
            texture = item,                                             
            color = color.white,                                        
            origin = (-.5,.5),
            position = self.find_free_spot(),
            z = -.1,
        )
        name = item.replace('_', ' ').title()                           
        icon.tooltip = Tooltip(name)                                    
        icon.tooltip.background.color = color.color(0,0,0,.8)
        
        def drop():
            icon.x = int(icon.x)
            icon.y = int(icon.y)
    	def drag():
         	icon.org_pos = (icon.x, icon.y)
         	icon.z -= .01

    	def drop():
			
        icon.x = int(icon.x)
        	icon.y = int(icon.y)
        	icon.z += .01
         
        
        	if icon.x < 0 or icon.x >= 1 or icon.y > 0 or icon.y <= -1:
            	icon.position = (icon.org_pos)
            	return
		for c in self.children

    	icon.drag = drag       
    	icon.drop = drop  

    
	
    def find_free_spot(self):                                                      
        taken_spots = [(int(e.x), int(e.y)) for e in self.item_parent.children]    
        for y in range(8):                                                         
            for x in range(5):                                                     
                if not (x,-y) in taken_spots:                                      
                    return (x,-y)
                
                          



for z in range(chunk):
	for x in range(chunk):
		voxel = Voxel(position = (x,0,z))



if __name__ == '__main__':
    player = FirstPersonController()
    sky = Sky()
    hand = Hand()
    inventory = Inventory()
    def add_item():                                                                  
        inventory.append(random.choice(('bag', 'bow_arrow', 'gem', 'orb', 'sword'))) 

    for i in range(7):                                                  
        add_item()                                                      

    add_item_button = Button(                                           
        scale = (.1,.1),                                                
        x = -.5,                                                        
        color = color.lime.tint(-.25),                                  
        text = '+',                                                     
        tooltip = Tooltip('Add random item'),                           
        on_click = add_item                                             
        )      
    app.run()

