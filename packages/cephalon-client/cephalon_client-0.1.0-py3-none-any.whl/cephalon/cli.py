import rich_click as click
from email_validator import validate_email, EmailNotValidError
from cephalon.meta import __version__, __package__
from cephalon.core import client
from cephalon.credentials import Credentials
from cephalon import console, utils

cc = client()

yes = lambda answer: answer[0].lower() == "y"


@click.group(name="cephalon")
@click.version_option(__version__, prog_name=__package__)
def entry(): ...


# @entry.command(name="auth")
# def auth_setup():
#     # todo: add tos agreement

#     title = "\nUsing the CLI to setup auth will save your credentials in plain text on your local system. "
#     console.write(title, color="yellow")
#     answer = console.visible_input("\nAre you sure you want to continue? \\[yes/no]")
#     if not yes(answer):
#         return

#     if Credentials.exists():
#         answer = console.visible_input(
#             "\nOverwrite the existing credentials.toml file? \\[yes/no]"
#         )
#         if yes(answer):
#             console.write(
#                 "Deleting existing credentials...", color="sky_blue1", style="italic"
#             )
#             Credentials.clear()
#             console.write("Successfully deleted.", color="green", style="italic")
#         else:
#             return

#     print()
#     answer = console.visible_input("Do you already have an account? \\[yes/no]")
#     if yes(answer):
#         raise NotImplementedError()
#     else:

#         email_is_valid: bool = False
#         while not email_is_valid:
#             print()
#             try:
#                 email = console.visible_input("Enter your email address.")
#                 print()
#                 console.write("Validating email...", color="sky_blue1", style="italic")
#                 email = validate_email(email).normalized
#                 Credentials(email=email).save()
#                 email_is_valid = True
#                 console.write(
#                     "Email validation succeeded.", color="green", style="italic"
#                 )
#             except EmailNotValidError as error:
#                 console.write(str(error), color="red", style="italic")
#         console.write(
#             "Generating secure password...",
#             "sky_blue1",
#             style="italic",
#         )
#         password = utils.generate_secure_password()
#         Credentials(email=email, password=password).save()
#         console.write(
#             "Successfully generated and saved password.",
#             color="green",
#             style="italic",
#         )
#         console.write("Submitting API request...", color="sky_blue1", style="italic")
#         result = cc.auth.register(email=email, password=password)
#         if result.is_err():
#             console.write(
#                 "Registration request failed. Try again later or submit a GitHub issue.",
#                 color="red",
#                 style="italic",
#             )
#         else:
#             console.write(
#                 "Registration request succeeded.", color="green", style="italic"
#             )
#             email_confirmed: bool = False
#             count = 0
#             while not email_confirmed:
#                 code = console.visible_input(
#                     "Please enter the 6 digit confirmation code sent to your email."
#                 )
#                 console.write(
#                     "Submitting API request...", color="sky_blue1", style="italic"
#                 )
#                 result = cc.auth.confirm(email=email, code=code)
#                 if result.is_ok():
#                     console.write(
#                         "Confirmation request succeeded.", color="green", style="italic"
#                     )
#                     email_confirmed = True
#                 elif count == 3:
#                     console.write(
#                         "There seems to be a problem, please try again later.",
#                         color="red",
#                         style="italic",
#                     )
#                     return
#                 else:
#                     console.write(
#                         "Confirmation request failed, resending confirmation code.",
#                         color="yellow",
#                         style="italic",
#                     )
#                     cc.auth.resend(email=email)
#             console.write("Account confirmed, starting automatic software token setup.")
#             mfa_result = cc.auth.setup(email=email, password=password)
