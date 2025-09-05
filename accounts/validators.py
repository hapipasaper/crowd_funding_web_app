import re
from django.core.exceptions import ValidationError

def egypt_phone_validator(value: str):
    """يتحقق من أرقام المحمول المصرية: تبدأ بـ 010/011/012/015 ويكون طولها 11 رقم."""
    if not re.fullmatch(r'01[0-2,5]\d{8}', value or ''):
        raise ValidationError('رقم موبايل مصري غير صالح. مثال: 01012345678')