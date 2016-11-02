# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import io
# import logging
from datetime import datetime, timedelta
from django.conf import settings
from six.moves import cPickle as pickle
import os
from time import time
# from builtins import open
from wikiwho.models import Article, Revision, RevisionParagraph, Paragraph, ParagraphSentence, Sentence, \
    SentenceToken, Token
from wikiwho.wikiwho_simple import Wikiwho
from .utils import pickle_, get_latest_revision_and_page_id, create_wp_session
from wikiwho import structures

session = create_wp_session()


class WPHandlerException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


class WPHandler(object):
    def __init__(self, article_title, pickle_folder='', save_pickle=True, *args, **kwargs):
        # super(WPHandler, self).__init__(article_title, pickle_folder=pickle_folder, *args, **kwargs)
        self.article_title = article_title
        self.article_db_title = ''
        self.revision_ids = []
        self.wikiwho = None
        self.pickle_folder = pickle_folder
        self.pickle_path = ''
        self.saved_rvcontinue = ''
        self.article_obj = None
        self.latest_revision_id = None
        self.page_id = None
        self.save_pickle = save_pickle

    def __enter__(self):
        # time1 = time()
        # logging.debug("--------")
        # logging.debug(self.article_title)

        # save as first letter in uppercase and ' 's are replaced by '_'
        self.article_db_title = (self.article_title[:1].upper() + self.article_title[1:]).replace(" ", "_")
        self.article_obj = Article.objects.filter(title=self.article_db_title).first()
        # TODO get all article with this title and check with page_id (even there is one article in db),
        # then update titles of other articles with other page ids by using wp api (celery task)
        # articles = [a for a in Article.objects.filter(title=self.article_db_title)]
        # for article in articles:
        #     if article.id == page_id:
        #         self.article_obj = article
        #         articles.remove(article)
        #         break
        # if articles:
        #     update_titles_task(articles)
        self.latest_revision_id, self.page_id = get_latest_revision_and_page_id(self.article_title)
        self.saved_rvcontinue = self.article_obj.rvcontinue if self.article_obj else '0'

        if self.save_pickle:
            # logging.debug("trying to load pickle")
            pickle_folder = self.pickle_folder or settings.PICKLE_FOLDER
            self.pickle_path = "{}/{}.p".format(pickle_folder, self.article_db_title.replace("/", "0x2f"))  # 0x2f is UTF-8 hex of /
            if os.path.exists(self.pickle_path):
                create_new = False
            else:
                pickle_folder = self.pickle_folder or settings.PICKLE_FOLDER_2
                self.pickle_path = "{}/{}.p".format(pickle_folder, self.article_db_title.replace("/", "0x2f"))
                create_new = not os.path.exists(self.pickle_path)
            if create_new:
                # a new pickle in secondary disk will be created
                self.wikiwho = Wikiwho(self.article_title)
                self.wikiwho.page_id = self.page_id
            else:
                with io.open(self.pickle_path, 'rb') as f:
                    self.wikiwho = pickle.load(f)
                    # print(self.article_title, '-> saved_rvcontinue:', self.wikiwho.rvcontinue)
            self.saved_rvcontinue = self.wikiwho.rvcontinue

        # time2 = time()
        # print("Execution time enter: {}".format(time2-time1))
        return self

    def handle(self, revision_ids, format_='json', is_api=True):
        # time1 = time()
        # check if article exists
        if self.latest_revision_id is None:
            raise WPHandlerException('The article ({}) you are trying to request does not exist'.format(self.article_title))
        self.revision_ids = revision_ids or [self.latest_revision_id]

        # holds the last revision id which is saved. 0 for new article
        rvcontinue = self.saved_rvcontinue

        if self.revision_ids[-1] >= int(rvcontinue.split('|')[-1]):
            # if given rev_id is bigger than saved one
            # logging.debug("STARTING NOW")
            headers = {'User-Agent': settings.WP_HEADERS_USER_AGENT,
                       'From': settings.WP_HEADERS_FROM}
            # Login request
            url = 'https://en.wikipedia.org/w/api.php'
            # revisions: Returns revisions for a given page
            params = {'titles': self.article_title, 'action': 'query', 'prop': 'revisions',
                      'rvprop': 'content|ids|timestamp|sha1|comment|flags|user|userid',
                      'rvlimit': 'max', 'format': format_, 'continue': '', 'rvdir': 'newer'}

            if not self.article_obj:
                self.wikiwho = Wikiwho(self.article_title)
                self.wikiwho.page_id = self.page_id
            else:
                t = time()
                # self.wikiwho = Wikiwho(self.article_title)
                # self.wikiwho.page_id = self.article_obj.id
                # assert self.wikiwho.page_id == page_id
                # self.wikiwho.rvcontinue = self.article_obj.rvcontinue
                # self.wikiwho.spam = self.article_obj.spam
                # self.wikiwho.revision_curr = structures.Revision()
                # # for revision in self.article_obj.revisions.select_related('editor').values():
                # revisions = self.article_obj.revisions.select_related('editor').order_by('timestamp')
                # revisions_count = revisions.count()
                # for i, rev in enumerate(revisions):
                #     revision = structures.Revision()
                #     for rp in rev.paragraphs.select_related('paragraph').order_by('position'):
                #         paragraph = structures.Paragraph()
                #         paragraph.id = rp.paragraph.id
                #         paragraph.hash_value = rp.paragraph.hash_value
                #         for ps in rp.paragraph.sentences.select_related('sentence').order_by('position'):
                #             sentence = structures.Sentence()
                #             sentence.id = ps.sentence.id
                #             sentence.hash_value = ps.sentence.hash_value
                #             if sentence.hash_value in self.wikiwho.sentences_ht:
                #                 self.wikiwho.sentences_ht[sentence.hash_value].append(sentence)
                #             else:
                #                 self.wikiwho.sentences_ht.update({sentence.hash_value: [sentence]})
                #
                #             if i == revisions_count - 1 or True:  # TODO remove True
                #                 for st in ps.sentence.tokens.select_related('label_revision', 'label_revision__editor').order_by('position'):
                #                     word = structures.Word()
                #                     word.value = st.token
                #                     word.token_id = st.token_id
                #                     word.revision = st.label_revision.id
                #                     word.author_id = st.label_revision.editor.wikipedia_id
                #                     sentence.words.append(word)
                #                     # get last internal id for new added tokens in new revisions
                #                     self.wikiwho.token_id = st.token_id  # TODO is this right way?
                #                 if sentence.hash_value in paragraph.sentences:
                #                     paragraph.sentences[sentence.hash_value].append(sentence)
                #                 else:
                #                     paragraph.sentences.update({sentence.hash_value: [sentence]})
                #                 paragraph.ordered_sentences.append(sentence.hash_value)
                #
                #         if paragraph.hash_value in self.wikiwho.paragraphs_ht:
                #             self.wikiwho.paragraphs_ht[paragraph.hash_value].append(paragraph)
                #         else:
                #             self.wikiwho.paragraphs_ht.update({paragraph.hash_value: [paragraph]})
                #
                #         if paragraph.hash_value in revision.paragraphs:
                #             revision.paragraphs[paragraph.hash_value].append(paragraph)
                #         else:
                #             revision.paragraphs.update({paragraph.hash_value: [paragraph]})
                #         revision.ordered_paragraphs.append(paragraph.hash_value)
                #
                #         if i == revisions_count - 1 or True:  # TODO remove True
                #             if paragraph.hash_value in self.wikiwho.revision_curr.paragraphs:
                #                 self.wikiwho.revision_curr.paragraphs[paragraph.hash_value].append(paragraph)
                #             else:
                #                 self.wikiwho.revision_curr.paragraphs.update({paragraph.hash_value: [paragraph]})
                #             self.wikiwho.revision_curr.ordered_paragraphs.append(paragraph.hash_value)
                #
                #     revision.wikipedia_id = rev.id
                #     revision.contributor_id = rev.editor.wikipedia_id
                #     revision.contributor_name = rev.editor.name
                #     revision.time = rev.timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')
                #     revision.length = rev.length
                #     self.wikiwho.revisions[rev.id] = revision  # only ids are enough to continue analyzing  # TODO check this
                #     if i == revisions_count - 1:
                #         self.wikiwho.revision_curr.wikipedia_id = rev.id
                #         self.wikiwho.revision_curr.contributor_id = rev.editor.wikipedia_id
                #         self.wikiwho.revision_curr.contributor_name = rev.editor.name
                #         self.wikiwho.revision_curr.time = rev.timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')
                #         self.wikiwho.revision_curr.length = rev.length
                print('loading ww obj from db: ', time() - t)

        while self.revision_ids[-1] >= int(rvcontinue.split('|')[-1]):
            # continue downloading as long as we reach to the given rev_id limit
            # if rvcontinue > self.revision_ids[-1], it means this rev_id is saved,
            # so no calculation is needed
            # logging.debug('doing partial download')
            # logging.debug(rvcontinue)

            if rvcontinue != '0' and rvcontinue != '1':
                params['rvcontinue'] = rvcontinue
            try:
                # TODO ? get revisions until revision_ids[-1], check line: elif not pages.get('revision')
                # params.update({'rvendid': self.revision_ids[-1]})  # gets from beginning
                result = session.get(url=url, headers=headers, params=params).json()
            except Exception as e:
                if is_api:
                    raise WPHandlerException('HTTP Response error! Try again later!'.format(self.article_title))
                else:
                    # if not api query, raise the original exception
                    raise e

            if 'error' in result:
                raise WPHandlerException('Wikipedia API returned the following error:' + str(result['error']))
            # if 'warnings' in result:
            #   raise WPHandlerException('Wikipedia API returned the following warning:" + result['warnings']))
            if 'query' in result:
                pages = result['query']['pages']
                if "-1" in pages:
                    raise WPHandlerException('The article ({}) you are trying to request does not exist!'.format(self.article_title))
                # elif not pages.get('revision'):
                #     raise WPHandlerException(message="End revision ID does not exist!")
                try:
                    # pass first item in pages dict
                    _, page = result['query']['pages'].popitem()
                    self.wikiwho.analyse_article(page.get('revisions', []))
                    # self.wikiwho.analyse_article(six.next(six.itervalues(result['query']['pages'])).
                    #                              get('revisions', []))
                except Exception as e:
                    # if there is a problem, save article until last given unproblematic rev_id
                    # import traceback
                    # traceback.print_exc()
                    self._save_article_into_db()
                    if self.save_pickle:
                        self.wikiwho.clean_attributes()
                        pickle_(self.wikiwho, self.pickle_path)
                    # TODO raise exception if it comes from wikiwho code
                    # logging.exception(self.article_title)
                    # traceback.print_exc()
                    raise WPHandlerException("Some problems with the JSON returned by Wikipedia!")
            if 'continue' not in result:
                # hackish: create a rvcontinue with last revision id of this article
                if self.wikiwho.revision_curr.time == 0:
                    # if # revisions < 500 and all revisions were detected as spam
                    # wikiwho object holds no information (it is in initial status, rvcontinue=0)
                    self.wikiwho.rvcontinue = '1'  # assign 1 to be able to save this article without any revisions
                else:
                    timestamp = datetime.strptime(self.wikiwho.revision_curr.time, '%Y-%m-%dT%H:%M:%SZ') \
                                + timedelta(seconds=1)
                    self.wikiwho.rvcontinue = timestamp.strftime('%Y%m%d%H%M%S') \
                                              + "|" \
                                              + str(self.wikiwho.revision_curr.wikipedia_id + 1)
                # print wikiwho.rvcontinue
                break
            rvcontinue = result['continue']['rvcontinue']
            self.wikiwho.rvcontinue = rvcontinue  # used at end to decide if there is new revisions to be saved
            # print rvcontinue

        # logging.debug('final rvcontinue ' + str(self.wikiwho.rvcontinue))

        # time2 = time()
        # print("Execution time handle: {}".format(time2-time1))

    def _save_article_into_db(self):
        if not self.article_obj:
            self.article_obj = Article.objects.create(id=self.wikiwho.page_id,
                                                      title=self.article_db_title,
                                                      spam=self.wikiwho.spam,
                                                      rvcontinue=self.wikiwho.rvcontinue)
        elif self.article_obj.rvcontinue != self.wikiwho.rvcontinue and self.article_obj.spam != self.wikiwho.spam:
            self.article_obj.rvcontinue = self.wikiwho.rvcontinue
            self.article_obj.spam = self.wikiwho.spam
            self.article_obj.save(update_fields=['rvcontinue', 'spam'])
        elif self.article_obj.rvcontinue != self.wikiwho.rvcontinue:
            self.article_obj.rvcontinue = self.wikiwho.rvcontinue
            self.article_obj.save(update_fields=['rvcontinue'])
        elif self.article_obj.spam != self.wikiwho.spam:
            self.article_obj.spam = self.wikiwho.spam
            self.article_obj.save(update_fields=['spam'])
        if self.wikiwho.revisions_to_save:
            Revision.objects.bulk_create(self.wikiwho.revisions_to_save, batch_size=1000000)
        if self.wikiwho.tokens_to_save:
            Token.objects.bulk_create(self.wikiwho.tokens_to_save.values(), batch_size=1000000)
        if self.wikiwho.sentences_to_save:
            Sentence.objects.bulk_create(self.wikiwho.sentences_to_save, batch_size=1000000)
        if self.wikiwho.paragraphs_to_save:
            Paragraph.objects.bulk_create(self.wikiwho.paragraphs_to_save, batch_size=1000000)
        if self.wikiwho.sentencetokens_to_save:
            SentenceToken.objects.bulk_create(self.wikiwho.sentencetokens_to_save, batch_size=1000000)
        if self.wikiwho.paragraphsentences_to_save:
            ParagraphSentence.objects.bulk_create(self.wikiwho.paragraphsentences_to_save, batch_size=1000000)
        if self.wikiwho.revisionparagraphs_to_save:
            RevisionParagraph.objects.bulk_create(self.wikiwho.revisionparagraphs_to_save, batch_size=1000000)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        If the context was exited without an exception, all three arguments will be None.
        If an exception is supplied, and the method wishes to suppress the exception (i.e., prevent it from being
        propagated), it should return a true value. Otherwise, the exception will be processed normally upon exit
        from this method.
        Note that __exit__() methods should not reraise the passed-in exception; this is the caller’s responsibility.
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        # time1 = time()
        # print(exc_type, exc_val, exc_tb)
        # logging.debug(self.wikiwho.rvcontinue, self.saved_rvcontinue)
        # logging.debug(wikiwho.lastrev_date)
        if self.wikiwho.rvcontinue != self.saved_rvcontinue:
            # if there is a new revision or first revision of the article
            self._save_article_into_db()
            if self.save_pickle:
                self.wikiwho.clean_attributes()
                pickle_(self.wikiwho, self.pickle_path)
        # return True
        # time2 = time()
        # print("Execution time exit: {}".format(time2-time1))
