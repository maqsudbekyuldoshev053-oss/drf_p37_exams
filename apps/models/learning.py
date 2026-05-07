# from django.db.models import Model, CharField, ForeignKey, CASCADE, PositiveIntegerField, DecimalField, BooleanField
# from django.db.models.constraints import UniqueConstraint
#
#
# class Course(Model):
#     title = CharField(max_length=255)
#     author = ForeignKey('apps.User', CASCADE, related_name='courses')
#     price = DecimalField(max_digits=10, decimal_places=2)
#
# class Lesson(Model):
#     course = ForeignKey('apps.Course', CASCADE, related_name='lessons')
#     title = CharField(max_length=255)
#     order = PositiveIntegerField()
#     is_preview = BooleanField(default=False)
#
#     class Meta:
#         constraints = [UniqueConstraint(
#             fields=['course', 'order'],
#             name='unique_lesson_order_course'
#         )
#         ]
#         ordering  = ['order']
#
#
# class Enrolment(Model):
#     user = ForeignKey('apps.User', CASCADE, related_name='enrolments')
#     course = ForeignKey('apps.Course', CASCADE, related_name='enrolments')
#     completed = BooleanField(default=False)
#
#     class Meta:
#         unique_together = (
#             ('user', 'course'),
#         )
#
#
#
#
#
#
