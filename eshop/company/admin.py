from django.contrib import admin

from .models import MixinsModel, Company, Bank, BankAccount, CompanyBankAccount


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "address",
        "city",
        "postal_code",
        "country",
        "phone",
        "email",
        "is_legal_address",
    )
    list_filter = ("is_legal_address",)
    search_fields = ("name",)


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "swift")
    search_fields = ("name",)


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ("id", "account_number")


@admin.register(CompanyBankAccount)
class CompanyBankAccountAdmin(admin.ModelAdmin):
    list_display = ("id", "bank", "company", "bank_account")
    list_filter = ("bank", "company", "bank_account")
