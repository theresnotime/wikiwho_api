from django.conf.urls import url

from .views import WikiwhoApiView, schema_view

urlpatterns = [
    url(r'^$', schema_view, name='swagger'),
    url(r'^rev_content/page_id/(?P<page_id>[0-9]+)/$',
        WikiwhoApiView.as_view(actions={'get': 'get_rev_content_by_page_id'}), name='rev_content_page_id'),
    url(r'^rev_content/rev_id/(?P<rev_id>[0-9]+)/$',
        WikiwhoApiView.as_view(actions={'get': 'get_rev_content_by_rev_id'}), name='rev_content_rev_id'),
    url(r'^rev_content/(?P<article_title>.+)/(?P<start_rev_id>[0-9]+)/(?P<end_rev_id>[0-9]+)/$',
        WikiwhoApiView.as_view(actions={'get': 'get_range_rev_content'}), name='rev_content_slice'),
    url(r'^rev_content/(?P<article_title>.+)/(?P<rev_id>[0-9]+)/$',
        WikiwhoApiView.as_view(actions={'get': 'get_article_rev_content'}), name='rev_content_title_rev_id'),
    url(r'^latest_rev_content/(?P<article_title>.+)/$',
        WikiwhoApiView.as_view(actions={'get': 'get_rev_content_by_title'}), name='rev_content_title'),

    # url(r'^deleted/page_id/(?P<page_id>[0-9]+)/$',
    #     WikiwhoApiView.as_view(actions={'get': 'get_deleted_content_by_page_id'}), name='deleted_page_id'),
    # url(r'^deleted/(?P<article_title>.+)/$',
    #     WikiwhoApiView.as_view(actions={'get': 'get_deleted_content_by_title'}), name='deleted_article_title'),
    url(r'^all_content/page_id/(?P<page_id>[0-9]+)/$',
        WikiwhoApiView.as_view(actions={'get': 'get_all_content_by_page_id'}), name='all_page_id'),
    url(r'^all_content/(?P<article_title>.+)/$',
        WikiwhoApiView.as_view(actions={'get': 'get_all_content_by_title'}), name='all_article_title'),
    url(r'^rev_ids/page_id/(?P<page_id>[0-9]+)/$',
        WikiwhoApiView.as_view(actions={'get': 'get_rev_ids_by_page_id'}), name='rev_ids_page_id'),
    url(r'^rev_ids/(?P<article_title>.+)/$',
        WikiwhoApiView.as_view(actions={'get': 'get_rev_ids_by_title'}), name='rev_ids_title'),

    # Backwards compatibility (it does not not work for the Wikipedia page "NGC_5544/5")
    url(r'^rev_content/(?P<article_title>.+)/$',
        WikiwhoApiView.as_view(actions={'get': 'get_rev_content_by_title'}), name='rev_content_title'),
]
