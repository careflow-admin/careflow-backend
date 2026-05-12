import unittest
from unittest.mock import patch

import app.utils.email as email_module


class TestEmailService(unittest.TestCase):
    def setUp(self) -> None:
        self._settings_patcher = patch.multiple(
            email_module,
            SMTP_HOST="smtp.gmail.com",
            SMTP_PORT=587,
            SMTP_USERNAME="user@example.com",
            SMTP_PASSWORD="app-password",
            SMTP_FROM_EMAIL="from@example.com",
            SMTP_FROM_NAME="CareFlow",
            SMTP_USE_TLS=True,
            SMTP_TIMEOUT=10,
        )
        self._settings_patcher.start()
        self.addCleanup(self._settings_patcher.stop)

    def test_send_email_success(self) -> None:
        with patch("app.utils.email.smtplib.SMTP") as smtp_mock:
            smtp_instance = smtp_mock.return_value.__enter__.return_value

            email_module.send_email("to@example.com", "Subject", "Body")

            smtp_mock.assert_called_once_with("smtp.gmail.com", 587, timeout=10)
            smtp_instance.starttls.assert_called_once()
            smtp_instance.login.assert_called_once_with(
                "user@example.com", "app-password"
            )
            smtp_instance.send_message.assert_called_once()

    def test_send_email_missing_settings(self) -> None:
        with patch.multiple(
            email_module,
            SMTP_USERNAME=None,
            SMTP_PASSWORD=None,
            SMTP_FROM_EMAIL="",
        ):
            with self.assertRaises(RuntimeError) as ctx:
                email_module.send_email("to@example.com", "Subject", "Body")

            self.assertIn("Missing SMTP settings", str(ctx.exception))

    def test_send_otp_email_uses_send_email(self) -> None:
        with patch("app.utils.email.send_email") as send_mock:
            email_module.send_otp_email("to@example.com", "123456")

            send_mock.assert_called_once()
            args = send_mock.call_args[0]
            self.assertEqual(args[0], "to@example.com")
            self.assertEqual(args[1], "Codigo OTP CareFlow")
            self.assertIn("123456", args[2])


if __name__ == "__main__":
    unittest.main()
