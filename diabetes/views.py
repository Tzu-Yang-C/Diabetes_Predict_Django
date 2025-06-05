from django.shortcuts import render
import joblib
import os
from django.views.decorators.csrf import csrf_exempt

# 載入模型
model_path = os.path.join(os.path.dirname(__file__), 'model', 'diabetes_dataset_model4.joblib')
model = joblib.load(model_path)

def get_suggestion(probability):
    if probability >= 50:
        return '您可能有糖尿病風險，建議儘早就醫。'
    elif probability >= 20:
        return '風險偏高，建議注意飲食與運動。'
    else:
        return '風險較低，請持續保持健康生活。'

@csrf_exempt
def predict_view(request):
    if request.method == 'POST':
        data = request.POST

        # 檢查是否有欄位為空
        required_fields = ['gender', 'age', 'hypertension', 'heart_disease', 'smoking_history', 'bmi', 'blood_glucose_level']
        missing_fields = [field for field in required_fields if not data.get(field)]

        if missing_fields:
            return render(request, 'index.html', {
                'error': '請填寫所有欄位。',
                'form_data': data,
                'probability': None,
                'suggestion': None
            })

        try:
            features = [[
                int(data['gender']),
                float(data['age']),
                int(data['hypertension']),
                int(data['heart_disease']),
                int(data['smoking_history']),
                float(data['bmi']),
                float(data['blood_glucose_level']),
            ]]
            prediction = model.predict_proba(features)[:, 1]
            prob = round(prediction[0] * 100, 1)
            suggestion = get_suggestion(prob)

            return render(request, 'index.html', {
                'probability': f"{prob}%",
                'suggestion': suggestion,
                'form_data': data,
                'error': None
            })

        except Exception as e:
            return render(request, 'index.html', {
                'error': f"資料格式錯誤：{str(e)}",
                'form_data': data,
                'probability': None,
                'suggestion': None
            })

    # GET 請求顯示空表單
    return render(request, 'index.html', {
        'form_data': {},
        'error': None,
        'probability': None,
        'suggestion': None
    })