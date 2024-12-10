correct_phone_numbers = [
    "+79261234567",
    "89261234567",
    "79261234567",
    "+7 926 123 45 67",
    "8(926)123-45-67",
    "123-45-67",
    "9261234567",
    "79261234567",
    "(495)1234567",
    "(495) 123 45 67",
    "89261234567",
    "8-926-123-45-67",
    "8 927 1234 234",
    "8 927 12 12 888",
    "8 927 12 555 12",
    "8 927 123 8 123",
]

wrong_numbers = [
    # wrong type
    "some_text",
    # wrong format
    "+1 123 456 7890",  # invalid country code
    "202.555.0456",
    "+44 20 7946 0958",
    "+33 1 70 90 12 34",
    "+91-98765 43210",
    "1 (800) 555-9876",
]
