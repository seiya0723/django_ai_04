from django.shortcuts import render,redirect

## Create your views here.
#from django.shortcuts import render
from django.views import View

from .models import Design
from .forms import DesignForm

import magic

ALLOWED_MIME    = [ "image/vnd.adobe.photoshop","application/postscript" ]

class illustView(View):

    def get(self, request, *args, **kwargs):

        #スペース区切りしない普通の検索(スペースも文字列として扱われる)
        if "search" in request.GET:
            designs = Design.objects.filter(title__contains=request.GET["search"])
        else:
            #Designクラスを使用し、DBへアクセス、データ全件閲覧
            designs = Design.objects.all()

        """
        #スペース区切りにした検索(検索キーワードをスペースで区切り、検索を実行)
        if "search" in request.GET:

            #(1)キーワードが空欄もしくはスペースのみの場合、ページにリダイレクト
            if request.GET["search"] == "" or request.GET["search"].isspace():
                return redirect("illust:index")

            #(2)キーワードをリスト化させる(複数指定の場合に対応させるため)
            search      = request.GET["search"].replace("　"," ")
            search_list = search.split(" ")

            #(3)クエリを作る
            query       = Q()
            for word in search_list:
                #TIPS:AND検索の場合は&を、OR検索の場合は|を使用する。
                query &= Q(title__contains=word)

            #(4)作ったクエリを実行
            designs        = Design.objects.filter(query)
        else:
            designs    = Design.objects.all()
        """

        button1     = "Prev"
        data        = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        category    = "カテゴリ−１"
        category2   = "カテゴリ−2"
        category3   = "カテゴリ−3"

        context = {
                   "button1":button1,
                   "data":data,
                   "category1":category,
                   "category2": category2,
                   "category3": category3,

                   "designs":designs,
                   }

        return render(request,"illust/index.html",context)

    def post(self, request, *args, **kwargs):

        if "file" not in request.FILES:
            return redirect("illust:index")

        mime_type = magic.from_buffer(request.FILES["file"].read(1024), mime=True)
        print(mime_type)

        #mime属性の保存(後のサムネイル生成処理に繋げる)
        copied          = request.POST.copy()
        copied["mime"]  = mime_type


        form = DesignForm(copied, request.FILES)


        if form.is_valid():
            print("バリデーションOK ")

            if mime_type in ALLOWED_MIME:
                result  = form.save()
            else:
                print("このファイルは許可されていません")
                return redirect("illust:index")
        else:
            print("バリデーションNG")
            return redirect("illust:index")


        #======ここから先、サムネイル作成処理==========

        #処理結果のIDを元に、サムネイルの保存を行い、thumbnailに保存したパスを指定する
        design          = Design.objects.filter(id=result.id).first()

        #upload_to、settings内にあるMEDIA_ROOTを読み取り、そこに画像ファイルを保存。
        from django.conf import settings
        #path            = Design.file.field.upload_to
        path            = Design.thumbnail.field.upload_to
        thumbnail_path  = path + str(design.id) + ".png"
        full_path       = settings.MEDIA_ROOT + "/" + thumbnail_path 

        #フォトショップの場合
        if design.mime == "image/vnd.adobe.photoshop":
            from psd_tools import PSDImage
            image   = PSDImage.open(settings.MEDIA_ROOT + "/" + str(design.file))
            image.composite().save(full_path)

        #イラストレーターの場合
        elif design.mime == "application/postscript":
            from PIL import Image
            image   = Image.open(settings.MEDIA_ROOT + "/" + str(design.file))
            image.save(full_path)
        else:
            return redirect("illust:index")

        design.thumbnail   = thumbnail_path
        design.save()


        return redirect("illust:index")

index   = illustView.as_view()
