from mongoengine import connect

uri = 'mongodb+srv://gogochristofour:Ge19tmYnthBIPLoO@atkachenko53.tdi5dtu.mongodb.net/?retryWrites=true&w=majority'

connect(db='pyweb8', host=uri, ssl=True)

