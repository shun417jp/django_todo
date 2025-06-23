
from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Task


# Taskモデル用の入力フォーム
class TaskForm(forms.ModelForm):
    class Meta: # 構成・設定を指定できる（どのモデルと連携する、どのフィールドを使う、フォームの構成設定など）
        model = Task
        fields = ('title', 'description', 'start_date', 'end_date') # フォームに表示するフィールドを指定
        widgets = { # 特定のフィールドの見た目を指定 datetime-localによりHTMLにて日付＋時刻入力フィールドになる
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs): # フォームが生成されるときの初期化処理
        super().__init__(*args, **kwargs)

        self.fields["title"].widget.attrs = {'placeholder': 'タスク名'} # プレースホルダー（薄い説明文）を設定する
        self.fields["description"].widget.attrs = {'placeholder': '詳細'}

    # 項目別にバリデーションを追加する場合はclean_<項目名>とする
    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date') # フォームの入力値を安全に取得（バリデーション済みの値（形式ミス、日付の不正などがない））
        if start_date and start_date < timezone.now(): # start_dateが存在し、今の時間未満だった場合
            raise ValidationError("開始日を過去に設定することはできません。") # バリデーションエラー

        return start_date

    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        if end_date and end_date < timezone.now():
            raise ValidationError("終了日を過去に設定することはできません。")

        return end_date

    # 全体にバリデーションを追加する場合はcleanメソッドを作成する
    def clean(self):
        cleaned_data = super().clean() # 全ての入力データを取得
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date < start_date:
            self.add_error('end_date', '終了日は開始日より後の日付を設定する必要があります。')