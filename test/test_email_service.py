import pytest
from app.services.emailService import SendEmailVerify

def test_send_verify():
    xender = "bastoutchakoura36@gmail.com"
    token = "test#token%"
    result = SendEmailVerify.sendVerify(token,xender)
    assert result == xender

def test_reset_verify():
    xender = "bastoutchakoura36@gmail.com"
    token = "test#token%"
    result = SendEmailVerify.resetverify(token,xender)
    assert result == xender