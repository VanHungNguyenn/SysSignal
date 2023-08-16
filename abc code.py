# def round_price(price, adigit):
#     return int(price * adigit) / adigit

# Làm tròn số
def round_price(price, adigit):
    return round(price * adigit) / adigit

print(round_price(0.008721, 1000000))