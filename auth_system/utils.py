# from django.contrib.auth.tokens import PasswordResetTokenGenerator
#
# class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
#     def _make_hash_value(self, user, timestamp):
#         return str(user.pk) + str(timestamp) + str(user.email)
#
#     def is_token_valid(self, user, token):
#
#         if not self.check_token(user, token):
#             return False
#
#         token_timestamp = self._num_days(self._today())
#         user_timestamp = self._num_days(user.date_joined)
#
#         return (token_timestamp - user_timestamp) <= 1
#
# account_activation_token = AccountActivationTokenGenerator()
