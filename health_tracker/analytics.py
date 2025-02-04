def sleep_analysis(sleep_hours, sleep_interruptions):
    result = {}
    avg_sleep_hours = sum(sleep_hours) / len(sleep_hours)
    avg_sleep_interruptions = sum(sleep_interruptions) / len(sleep_interruptions)

    result['Average sleep hours'] = round(avg_sleep_hours, 2)
    result['Average number of interruptions'] = round(avg_sleep_interruptions)

    if 6.5 <= avg_sleep_hours < 10 and avg_sleep_interruptions <= 3:
        result[
            'Sleep quality conclusion'] = 'Your average sleep duration and number of interruptions are within normal limits.'
    elif avg_sleep_hours < 6.5 and avg_sleep_interruptions <= 3:
        result['Sleep quality conclusion'] = 'You should set aside more time for sleep.'
    elif avg_sleep_hours >= 10 and avg_sleep_interruptions <= 3:
        result[
            'Sleep quality conclusion'] = 'Your average sleep duration is higher than average. This is not always a good thing.'
    elif 6 <= avg_sleep_hours < 10 and avg_sleep_interruptions > 3:
        result[
            'Sleep quality conclusion'] = 'Your sleep quality is not very good. Try to eliminate possible causes of interruptions or consult a doctor.'
    else:
        result[
            'Sleep quality conclusion'] = 'It looks like you have serious sleep problems that can negatively affect your health. You should see a doctor as soon as possible.'
    return result


def activity_analysis(burnt_kcal, consumed_kcal, gender, weight, height, age):
    result = {}
    avg_burnt_kcal = sum(burnt_kcal) / len(burnt_kcal)
    avg_consumed_kcal = sum(consumed_kcal) / len(consumed_kcal)

    bmi = weight / ((height / 100) ** 2)
    result['BMI'] = round(bmi, 2)
    if bmi <= 18.5:
        result['Explanation of BMI'] = 'Your body mass index is low.'
    elif bmi <= 24.9:
        result['Explanation of BMI'] = 'Your body mass index is within normal limits.'
    elif bmi <= 29.9:
        result['Explanation of BMI'] = 'You are overweight.'
    else:
        result['Explanation of BMI'] = 'It looks like you are obese, see a doctor.'

    c = 5 if gender == "M" else -161
    bmr = (10 * weight) + (6.25 * height) - (5 * age) + c
    activity_coefficient = (bmr + avg_burnt_kcal) / bmr
    if activity_coefficient <= 1.2:
        result['Activity level'] = 'Your activity level is minimal. Incorporate physical activity into your routine.'
    elif activity_coefficient <= 1.375:
        result['Activity level'] = 'Your activity level is low. Try to move more.'
    elif activity_coefficient <= 1.55:
        result['Activity level'] = 'Your activity level is normal.'
    elif activity_coefficient <= 1.725:
        result['Activity level'] = 'Your activity level is high. Do not forget to take breaks and watch your diet!'
    else:
        result['Activity level'] = 'Your activity level is very high! Not recommended on a permanent basis'

    kcal_intake_norm = bmr * activity_coefficient
    result['Calorie intake norm'] = round(kcal_intake_norm)
    result['Average calorie intake'] = round(avg_consumed_kcal)
    if avg_consumed_kcal > kcal_intake_norm + 200:
        result['Diet advice'] = 'It looks like your calorie intake is higher than normal.'
    elif avg_consumed_kcal <= kcal_intake_norm - 150:
        result['Diet advice'] = 'Your calorie intake is below normal. You should increase it.'
    else:
        result['Diet advice'] = 'Your calorie intake is normal. Keep up!'
    return result
