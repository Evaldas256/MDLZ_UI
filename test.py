from step_comment_widget import StepCommentWidget

a1=StepCommentWidget(step_name='geras',start='10',end='20')
a2=StepCommentWidget(step_name='geras',start='19',end='30')
a3=StepCommentWidget(step_name='geras',start='29',end='35')


a1.add_event(a2)
a2.add_event(a3)

print(a2.end)