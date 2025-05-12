from django.contrib import admin
from .models import Achievement, UserAchievement, Challenge, UserChallengeProgress
from .models import Skin

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display  = ('name', 'trigger_type', 'target_value')
    list_filter   = ('trigger_type',)
    search_fields = ('name', 'description', 'slug')
    ordering      = ('trigger_type', 'target_value')

@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ('user', 'achievement', 'unlocked_at')
    # autocomplete_fields = ('user', 'achievement')  # opcional

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display  = ('name', 'metric', 'start', 'end', 'target_value')
    list_filter   = ('metric',)
    search_fields = ('name', 'description', 'slug')
    ordering      = ('-start',)

@admin.register(UserChallengeProgress)
class UserChallengeProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'challenge', 'progress', 'completed', 'claimed')
    # autocomplete_fields = ('user', 'challenge')   # opcional



@admin.register(Skin)
class SkinAdmin(admin.ModelAdmin):
    list_display = ('name','slug')
    search_fields = ('name','slug')