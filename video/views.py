from django.shortcuts import render, redirect

from service_api.models.videos import Video, VideoAttribute
from video.repository.video import register
from video.identifier import YouTubeVideoIdentifier
from video.forms import UpsertVideoForm, UpsertVideoAttributeForm


def video_list(requset):
    """動画リストを返す

    :param requset:
    :return:
    """
    return render(requset, 'cms/video/video_list.html', context={
        'videos': Video.objects.select_related('attribute__game__discipline', 'attribute__article', 'author')
                  .filter(enabled=True)})


def upsert_video(request):
    """指定の動画を収集する　

    :param request:
    :rtype render:
    """
    if request.method == 'POST':
        form = UpsertVideoForm(request.POST)
        if form.is_valid():
            platform_video_id = form.cleaned_data['platform_video_id']
            # 収集
            register(identifier=YouTubeVideoIdentifier(platform_video_id))
            return redirect('/video/')
        return render(request, 'cms/video/upsert_video.html', context={
            'form': form
        })
    return render(request, 'cms/video/upsert_video.html', context={
            'form': UpsertVideoForm()
    })


def upsert_video_attribute(request, video_id):
    """指定の動画を収集する　

    :param request:
    :param int video_id:
    :rtype render:
    """
    video_attribute = VideoAttribute.objects.filter(video_id=video_id).first()
    if request.method == 'POST':
        if video_attribute:
            form = UpsertVideoAttributeForm(request.POST, instance=VideoAttribute.objects.get(pk=video_id))
        else:
            form = UpsertVideoAttributeForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/video/')
        return render(request, 'cms/video/upsert_video_attribute.html', context={
            'form': form,
            'video_id': video_id
        })
    return render(request, 'cms/video/upsert_video_attribute.html', context={
        'form': UpsertVideoAttributeForm(instance=VideoAttribute.objects.get(pk=video_id))
        if video_attribute else UpsertVideoAttributeForm(),
        'video_id': video_id
    })
