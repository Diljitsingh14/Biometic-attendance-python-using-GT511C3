from models import constrains,Model
structs = [
    {"name":"id","type":"INTEGER","constrains":[constrains["primary key"]]},
    {"name":"name","type":"varchar(100)","constrains":[constrains['not null'],constrains["default"]]},
    {"name":"finger_print","type":"INTEGER","constrains":[constrains['not null'],constrains['unique']]},
    {"name":"class","type":"varchar(100)","constrains":[constrains['not null']]},

]
student = Model("Students")
try:
    student.migrate(structs)
except:
    pass
