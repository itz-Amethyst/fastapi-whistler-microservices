import hmac
import hashlib
import time
from user_service.config import settings

class OTPGenerator:
    
    def __init__(self, secret, digest=hashlib.sha1, digit=6, interval=30) -> None:
        self.secret = secret
        self.digest = digest
        self.digit = digit
        self.interval = interval
    
    def byte_secrets(self):
        return self.secret

    def int_to_bytestring(self, value, padding=8):
        result = bytearray() 
        while value != 0:
            result.append(value & 0xFF) 
            value >>= 8
        
        return bytes(bytearray(reversed(result)).rjust(padding, b'\0'))
    
    def generate_otp_algorithm(self, input: str) -> str:
        """
        Computed integer based on unix timestamp
        """
        if input < 0:
            raise ValueError("input must be positive integer")
        
        hasher = hmac.new(self.byte_secrets, self.int_to_bytestring(input), self.digest)
        hmac_hash = bytearray(hasher.digest())
        offset = hmac_hash[-1] & 0xF
        code = (
            (hmac_hash[offset] & 0x7F) << 24
            | (hmac_hash[offset + 1] & 0x7F) << 16
            | (hmac_hash[offset + 2] & 0x7F) << 8
            | (hmac_hash[offset + 3] & 0x7F)
        )

        str_code = str(code % 10 **self.digest)
        while len(str_code) < self.digest:
            str_code = "0" + str_code
        return str_code

    def generate_otp(self) -> str:
        current_time = int(time.time() / self.interval)
        return self.generate_otp(current_time)
    
generator = OTPGenerator(settings.OTP_SECRET_KEY)

# usecase
print(generator.generate_otp)