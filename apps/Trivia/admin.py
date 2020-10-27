from django.contrib import admin

from .models import *



class QuestionInline(admin.TabularInline):
    model=Question

class QuizAdmin(admin.ModelAdmin):
    inlines=[QuestionInline,]
    list_display=("name","user",)

class MultiChoiceAnswerInline(admin.TabularInline):
    model=MultiChoiceAnswer

class MultiChoiceQuestionAdmin(admin.ModelAdmin):
    inlines=[MultiChoiceAnswerInline,]
    list_display=("question",)

# Register your models here.
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question)
admin.site.register(MultiChoiceQuestion, MultiChoiceQuestionAdmin)
admin.site.register(TextQuestion)