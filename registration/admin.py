
from django.contrib import admin
from .models import Team, Player


class PlayerInline(admin.TabularInline):
    model = Player
    extra = 0
    readonly_fields = ("name", "email", "branch", "year")


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):

    list_display = (
        "team_id",
        "team_type",
        "payment_status",
        "created_at",
        "email_sent",
    )

    search_fields = ("team_id",)

    list_filter = ("team_type", "payment_status", "email_sent")

    ordering = ("-created_at",)

    inlines = [PlayerInline]


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):

    list_display = ("name", "email", "team", "branch", "year")

    search_fields = ("name", "email", "team__team_id")

    list_filter = ("branch", "year")
