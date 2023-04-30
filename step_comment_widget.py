from PySide2.QtWidgets import QWidget, QFrame, QHBoxLayout, QLabel, QVBoxLayout, QTextEdit, QLineEdit


#
# class Event:
#     def __init__(self, start, end):
#         self._start = start
#         self._end = end
#         self._previous_event = None
#         self._next_event = None
#
#     def add_event(self, event):
#         event._previous_event = self
#         self._next_event = event
#
#     def remove_event(self, event):
#         if self._next_event == event:
#             self._next_event = event._next_event
#             if event._next_event is not None:
#                 event._next_event._previous_event = self
#         elif self._next_event is not None:
#             self._next_event.remove_event(event)
#
#     @property
#     def start(self):
#         return self._start
#
#     @start.setter
#     def start(self, value):
#         self._start = value
#         self._update_subsequent_events()
#
#     @property
#     def end(self):
#         return self._end
#
#     @end.setter
#     def end(self, value):
#         self._end = value
#         self._update_subsequent_events()
#
#     @property
#     def previous_event(self):
#         return self._previous_event
#
#     @property
#     def next_event(self):
#         return self._next_event
#
#     def _update_subsequent_events(self):
#         if self._next_event is not None:
#             self._next_event.start = self._end
#             self._next_event._update_subsequent_events()


class StepCommentWidget(QWidget):
    def __init__(self, step_name, start, end, background_color="#00ffff",
                 border_color="#ffa500"):
        super().__init__()
        self._next_event = None
        self._previous_event = None
        self.start = start
        self.end = end
        self.step_name = step_name
        self.background_color = background_color
        self.border_color = border_color
        self.step_name = step_name


        # create a QFrame as the top-level widget and set its properties
        self.frame = QFrame(self)
        self.frame.setFrameStyle(QFrame.Box | QFrame.Plain)

        self.frame.setStyleSheet(f"background-color: {background_color}; border: 2px {border_color};")

        self.frame.setFixedWidth(200)
        self.frame.setFixedHeight(100)

        # create QLabel widgets for "Step Name", "Time From", and "Time To"

        step_name_label = QLabel(f"{step_name}", self.frame)
        time_from_label = QLineEdit(f"{start}", self.frame)

        time_to_label = QLineEdit(f"{end}", self.frame)

        # create a QHBoxLayout for the labels in the upper right corner
        labels_layout = QHBoxLayout()
        labels_layout.addWidget(time_from_label)
        labels_layout.addSpacing(10)
        labels_layout.addWidget(time_to_label)
        labels_layout.addStretch(1)

        # create a QHBoxLayout for the "Step Name" label in the upper left corner
        step_name_layout = QHBoxLayout()
        step_name_layout.addWidget(step_name_label)
        step_name_layout.addStretch(1)

        # create a QTextEdit widget for the center of the widget
        text_edit = QTextEdit(self.frame)
        text_edit.setStyleSheet("background-color: white; color: black;border: none;")
        text_edit.setContentsMargins(0, 0, 0, 0)
        text_edit.setProperty("show-editor-line", "false")

        # create a QVBoxLayout and add the label_layout and QTextEdit to it
        layout = QVBoxLayout()
        upper_layout = QHBoxLayout()
        upper_layout.addLayout(step_name_layout)
        upper_layout.addStretch(1)
        upper_layout.addLayout(labels_layout)
        layout.addLayout(upper_layout)
        layout.addWidget(text_edit)

        step_name_label.setStyleSheet("border: none;color: black")
        time_from_label.setStyleSheet("border: none;color: black")
        time_to_label.setStyleSheet("border: none;color: black")

        # set the layout for the top-level frame widget

        self.frame.setLayout(layout)

        # set the layout for the widget to a QVBoxLayout and add the top-level frame widget
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.frame)
        self.setLayout(main_layout)

    def add_event(self, event):
        event._previous_event = self
        self._next_event = event

    def remove_event(self, event):
        if self._next_event == event:
            self._next_event = event._next_event
            if event._next_event is not None:
                event._next_event._previous_event = self
        elif self._next_event is not None:
            self._next_event.remove_event(event)

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        self._start = value
        self._update_subsequent_events()

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value):
        self._end = value
        self._update_subsequent_events()

    @property
    def previous_event(self):
        return self._previous_event

    @property
    def next_event(self):
        return self._next_event

    def _update_subsequent_events(self):
        if self._next_event is not None:
            self._next_event.start = self._end
            self._next_event._update_subsequent_events()
