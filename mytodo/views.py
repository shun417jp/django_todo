from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from .models import Task
from .forms import TaskForm
from django.shortcuts import redirect



# Create your views here.

class IndexView(View):
    def get(self, request):
        # todoリストを取得
        todo_list = Task.objects.all()
        context = {"todo_list": todo_list}

        # テンプレートをレンダリング
        return render(request, "mytodo/index.html", context)
#ビュークラスをインスタンス化
index = IndexView.as_view()

class AddView(View):
   def get(self, request):
       # 空のフォームを作成してテンプレートに渡す
       form = TaskForm()
       return render(request, "mytodo/add.html", {
           'form': form,
           'object': None  # yesnoフィルター用に明示的にNoneを渡す
       })

   def post(self, request, *args, **kwargs):
       # 登録処理
       # 入力データをフォームに渡す
       form = TaskForm(request.POST)
       # 入力データに誤りがないかチェック
       is_valid = form.is_valid()

       # データが正常であれば
       if is_valid:
           # モデルに登録
           form.save()
           return redirect('/')

       # データが正常じゃない
       return render(request, 'mytodo/add.html', {
           'form': form,
           'object': None  # エラー時もyesnoフィルター用にNoneを渡す
       })

       
add = AddView.as_view()
class Update_task_complete(View):
    def post(self, request, *args, **kwargs):
        task_id = request.POST.get('task_id')

        task = Task.objects.get(id=task_id)
        task.complete = not task.complete
        task.save()

        return redirect('/')

update_task_complete = Update_task_complete.as_view()

class EditView(View):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        form = TaskForm(instance=task)
        return render(request, "mytodo/add.html", {
            'form': form,
            'object': task  # yesnoフィルター用（編集なのでobjectを渡す）
        })

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request, 'mytodo/add.html', {
            'form': form,
            'object': task
        })

edit = EditView.as_view()

def delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.delete()
        return redirect('/')
    return redirect('delete_confirm', pk=pk)  # 万一GETでアクセスされた場合の保険

def delete_confirm(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'mytodo/delete_confirm.html', {'task': task})

