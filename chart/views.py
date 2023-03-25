import openai
from django.http import JsonResponse
from django.shortcuts import render
from transformers import pipeline
import subprocess
from django.http import HttpResponse
import sys


from .train import train_model

from .models import User, Message

openai.api_key = "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"  # 替换为你的API Key

from .train import train_model


def train(request):

    if request.method == 'POST':

        epochs = request.POST['epochs']
        lr = request.POST['lr']
        subprocess.run([sys.executable, 'train_model.py', str(epochs), str(lr)])
        subprocess.Popen(['python3', 'chart/train.py', epochs, lr])
        return HttpResponse("Training started!")
    else:
        return render(request, 'train.html')

def chatbot(request):
    # 加载预训练模型
    model = pipeline("text-generation", model="gpt2")

    # 获取用户输入
    user_input = request.GET.get("input")

    # 生成回复消息
    response = model(user_input, max_length=50, do_sample=True)[0]["generated_text"]

    # 返回回复消息
    return JsonResponse({"response": response})


def indexBOT(request):
    if request.method == 'POST':
        text = request.POST['text']
        prompt = f"User:{text}\nAI:"
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            temperature=0.5,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["\n", "User:", "AI:"]
        )
        message = response.choices[0].text.strip()
        return JsonResponse({'message': message})
    return render(request, 'indexBOT.html')


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
        #     davinci: 最强大、最通用的模型，可用于生成各种类型的文本，包括文章、对话、代码等。是OpenAI
        # API中唯一收费的模型，使用时需要花费相应的API令牌。
        # curie: 比davinci稍弱，但也可用于生成多种类型的文本。与davinci一样，是OpenAI
        # API中的高级模型，也需要使用API令牌。
        # babbage: 面向程序员的模型，可用于自动生成代码和文档。
        # ada: 面向自然语言处理（NLP）任务的模型，如问答、翻译等。
        # text - davinci - 002: 与davinci类似，但速度更快、更便宜，可以更好地用于实时应用程序。
        engine="text-davinci-002",
        prompt=prompt,
        temperature=1,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["User:", "AI:"],
        n=1,
        ##language="zh-CN"
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
