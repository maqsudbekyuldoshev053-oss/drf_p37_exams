# from django.db.models import Model, CharField, ForeignKey, CASCADE, BooleanField, ManyToManyField
# from django_ckeditor_5.fields import CKEditor5Field
#
#
# class Skill(Model):
#     name = CharField(max_length=150)
#
#
# class Course(Model):
#     title = CharField(max_length=200)
#     description = CKEditor5Field()
#     is_published = BooleanField(db_default=False)
#     instructor = ForeignKey('apps.User', CASCADE, related_name="courses")
#     skills = ManyToManyField('apps.Skill', blank=True, related_name="courses")
#
#     def __str__(self):
#         return self.title
#
#
# class Enrollment(Model):
#     user = ForeignKey('apps.User', CASCADE, related_name="enrollments")
#     course = ForeignKey('apps.Course', CASCADE, related_name="enrollments")
#
#     class Meta:
#         unique_together = (
#             ('user', 'course'),
#         )
