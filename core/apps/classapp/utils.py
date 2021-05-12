def calculate_discount(value, discounts, flag=False):
    temp_value = 0
    for discount in discounts:
        if flag and discount.limited:
            discount.count += 1
            discount.save()
        if discount.percent is None:
            temp_value += discount.value
        else:
            temp_value += value * discount.percent / 100
    return temp_value if temp_value <= value else value

        