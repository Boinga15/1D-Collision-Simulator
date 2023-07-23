class Object:
    def __init__(self, x, size, mass, velocity):
        self.x = x
        self.size = size
        self.mass = mass
        self.velocity = velocity
        self.collidedWith = []
        
        self.forgetTimer = 0
        self.collisions = 0