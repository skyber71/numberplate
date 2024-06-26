from django.shortcuts import render
from .forms import ArrayInputForm

@method_decorator(csrf_exempt, name='dispatch')
class PredictView(View):
    def get(self, request, *args, **kwargs):
        form = ArrayInputForm()
        return render(request, 'recognition/index.html', {'form': form})

    def post(self, request, *args, **kwargs):
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                array = data['array']
            else:
                form = ArrayInputForm(request.POST)
                if form.is_valid():
                    array = json.loads(form.cleaned_data['array'])
                else:
                    return JsonResponse({'status': 'error', 'message': 'Invalid form data'}, status=400)
            
            prediction = model.predict([array])
            result = ''.join(prediction)
            
            response = {
                'status': 'success',
                'prediction': result
            }
            return JsonResponse(response)
        
        except Exception as e:
            response = {
                'status': 'error',
                'message': str(e)
            }
            return JsonResponse(response, status=400)
