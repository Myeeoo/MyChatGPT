import openai
from django.shortcuts import render

from .models import User, Message

openai.api_key = "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"  # 替换为你的API Key


def home(request):
    return render(request, 'home.html')


def generate_text(request):
    prompt = request.GET.get('prompt')  # 获取用户输入的prompt

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

    generated_text = response.choices[0].text  # 从API响应中获取生成的文本

    return render(request, 'chart/generate_text.html', {'generated_text': generated_text})


def generate_response(text):
    prompt = f"User:{text}\nAI:"
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    message = response.choices[0].text.strip()
    return message


def index(request):
    if request.method == 'POST':
        user = User.objects.get(email='feijifr@qq.com')
        message = Message(user=user, text=request.POST['message'])
        message.save()
        bot_message = generate_response(request.POST['message'])
        bot = User.objects.get(email='chatgpt@qq.com')
        bot_message = Message(user=bot, text=bot_message)
        bot_message.save()
    messages = Message.objects.order_by('-created_at')[:10]
    return render(request, 'index.html', {'messages': messages})
