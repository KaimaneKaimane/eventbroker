class Base:
    _ID = 0

    def __init__(self, event_time):
        self.id = Base._ID
        Base._ID += 1

        self.event_time = event_time

    def __str__(self):
        return 'id: ' + str(self.id) + '\nevent_time: ' + str(self.event_time)
