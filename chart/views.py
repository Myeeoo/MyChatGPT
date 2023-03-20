from django.shortcuts import render
import openai
openai.api_key = "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" # 替换为你的API Key

def generate_text(request):
    prompt = request.GET.get('prompt') # 获取用户输入的prompt

    # 使用OpenAI API生成文本
    response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=prompt,
      temperature=0.5,
      max_tokens=2048,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )

    generated_text = response.choices[0].text # 从API响应中获取生成的文本

    return render(request, 'chart/generate_text.html', {'generated_text': generated_text})
