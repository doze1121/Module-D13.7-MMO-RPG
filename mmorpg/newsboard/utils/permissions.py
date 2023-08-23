from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from newsboard.models import Post


class IsAuthorMixin(LoginRequiredMixin):

    def get_pk_list(self, dict_):
        pks = []
        for pk in dict_:
            pks.append(pk.get('pk'))
        return pks

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        post_pk = kwargs.get('post_pk')
        comment_pk = kwargs.get('comment_pk')

        if post_pk:
            pks_dict = request.user.post_set.all().values('pk')
            if post_pk not in self.get_pk_list(pks_dict):
                return self.handle_no_permission()

            return super().dispatch(request, *args, **kwargs)

        elif comment_pk:
            pks_dict = request.user.comment_set.all().values('pk')

            if comment_pk not in self.get_pk_list(pks_dict):
                return self.handle_no_permission()
            return super().dispatch(request, *args, **kwargs)

        return self.handle_no_permission()


class NotIsAuthorMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        post = Post.objects.filter(pk=kwargs.get('post_pk')).first()

        if post:
            if post in request.user.post_set.all():
                return redirect('newsboard:home')
        return super().dispatch(request, *args, **kwargs)