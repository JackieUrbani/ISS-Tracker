import vpython as vp
import math
import requests

# North based on current facing direction, 0-forwards, 1-left, 2-backwards, 3-right
north = 3

LAT_HOME = 44.479307
LNG_HOME = 360-73.206923

lat_iss = 0
lng_iss = 0

#ball = vp.sphere(radius=0)
t = 0
dt = 0.1
R = 5

#arrow = vp.arrow(pos = vp.vector(0, 0, 0), 
                 #color = vp.vector(1, 0, 1),
                 #axis = ball.pos)
                 
def align_to_north():
    if north == 0:
        ball.pos = R * vp.vector(0,0,-R)
    if north == 1:
        ball.pos = R * vp.vector(-R,0,0)
    if north == 2:
        ball.pos = R * vp.vector(0,0,R)
    if north == 3:
        ball.pos = R * vp.vector(R,0,0)

def get_iss_position():
    # Get current ISS position
    req_iss = requests.get('http://api.open-notify.org/iss-now.json')
    dict = req_iss.json()
    lat_lng = dict['iss_position']
    # save the current ISS  possition in new variables
    lat_iss = float(lat_lng['latitude'])
    lng_iss = float(lat_lng['longitude'])
    if lat_iss < 0:
        lat_iss = 360 + lat_iss
    if lng_iss < 0:
        lng_iss = 360 + lng_iss
    return lat_iss, lng_iss

def deg2rad(deg):
    return deg * (math.pi/180)

def get_line_differences(lat_home, lng_home, lat_other, lng_other):
    lat_diff = (lat_home - lat_other) / 22.5
    lng_diff = (lng_home - lng_other) / 22.5
    return lat_diff, lng_diff
    
def get_angle_differences(lat_home, lng_home, lat_other, lng_other):
    lat_diff = (lat_home - lat_other)
    lng_diff = (lng_home - lng_other)
    return lat_diff, lng_diff

def getDistance(lat_iss, lng_iss, lat_home, lng_home):
    R = 6371  # Radius of the earth in km
    dLat = deg2rad(lat_home-lat_iss)  # deg2rad below
    dLng = deg2rad(lng_home-lng_iss)
    a = sin(dLat/2) * sin(dLat/2) + cos(deg2rad(lat_iss)) * \
        cos(deg2rad(lat_home)) * sin(dLng/2) * sin(dLng/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    d = R * c  # Distance in km to Home
    return d

earth_rad = 1
earth = vp.sphere(radius=earth_rad, opacity=1, color=vp.vector(1,1,1), texture="earth_wrap.png")

phi = deg2rad(LNG_HOME)
theta = deg2rad(-LAT_HOME)
x = earth_rad * math.sin(phi) * math.cos(theta)
y = earth_rad * math.sin(phi) * math.sin(theta)
z = earth_rad * math.cos(phi)
home = vp.sphere(pos=vp.vector(x, y, z), radius=0.05, color=vp.vector(1,1,1))

lat_iss, lng_iss = get_iss_position()
phi = deg2rad(lng_iss)
theta = deg2rad(-lat_iss)
x = earth_rad * 1.5 * math.sin(phi) * math.cos(theta)
y = earth_rad * 1.5 * math.sin(phi) * math.sin(theta)
z = earth_rad * 1.5 * math.cos(phi)
iss = vp.sphere(pos=vp.vector(x, y, z), radius=0.05, color=vp.vector(1,0,0), make_trail=True)

while (True):
    vp.rate(5)
    #ball.pos = R * vp.vector(math.cos(t),math.sin(t),0)
    #align_to_north()
    #arrow.axis = ball.pos
    
    lat_iss, lng_iss = get_iss_position()
    #print(lat_iss, lng_iss)
    phi = deg2rad(lng_iss)
    theta = deg2rad(-lat_iss)
    x = earth_rad * 1.5 * math.sin(phi) * math.cos(theta)
    y = earth_rad * 1.5 * math.sin(phi) * math.sin(theta)
    z = earth_rad * 1.5 * math.cos(phi)
    iss.pos = vp.vector(x, y, z)
    #print(get_angle_differences(LAT_HOME, LNG_HOME, lat_iss, lng_iss))
    
    t = t + dt