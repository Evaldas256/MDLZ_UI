class EventChain:
    def __init__(self):
        self.head = None

    def add_event(self, start_time, end_time):
        new_event = Event(start_time, end_time)
        if self.head is None:
            self.head = new_event
        else:
            current_event = self.head
            while current_event.next_event is not None:
                current_event = current_event.next_event
            current_event.next_event = new_event

    def delete_event(self, event):
        if self.head == event:
            self.head = event.next_event
        else:
            current_event = self.head
            while current_event.next_event is not event:
                current_event = current_event.next_event
            current_event.next_event = event.next_event

        # Adjust start/end times if necessary
        if event.next_event is not None:
            event.next_event.start_time = event.start_time
        if current_event.end_time != current_event.next_event.start_time:
            current_event.end_time = current_event.next_event.start_time


class Event:
    def __init__(self, start_time, end_time, color):
        self.start_time = start_time
        self.end_time = end_time
        self.next_event = None
        self.color = color

    def update_start_time(self, new_start_time):
        # Update start time of current event
        self.start_time = new_start_time

        # Update end time of previous event if necessary
        if self.next_event is not None:
            prev_end_time = self.start_time
            if self.next_event.start_time != prev_end_time:
                self.next_event.update_start_time(prev_end_time)

    def update_end_time(self, new_end_time):
        # Update end time of current event
        self.end_time = new_end_time

        # Update start time of next event if necessary
        if self.next_event is not None:
            next_start_time = self.end_time
            if self.next_event.start_time != next_start_time:
                self.next_event.update_start_time(next_start_time)
