from django.db import models


class TranslationManager(models.Manager):
    def get_translation_model(self):
        return self.model.get_translation_model()

    def get_translation_model_reverse_field_name(self):
        return self.model.get_translation_model_reverse_field_name()

    def get_translation_model_field_names(self, reverse=False, m2m=False,
                                          own=True):
        return self.model.get_translation_model_field_names(reverse, m2m, own)

    def get_annotate_params(self):
        reverse_name = self.get_translation_model_reverse_field_name()
        fields = self.get_translation_model_field_names()
        annotate_params = {}
        for f in fields:
            annotate_params[f] = models.F('{}__{}'.format(reverse_name, f))
        return annotate_params

    def get_queryset(self):
        q = super(TranslationManager, self).get_queryset()
        q = q.annotate(**self.get_annotate_params())
        return q.all()


class TranslationMixin(models.Model):
    translation_model = None

    @classmethod
    def get_translation_model(cls):
        return cls.translation_model

    @classmethod
    def get_translation_model_field_names(cls, reverse=False, m2m=False,
                                          own=True):
        TransModel = cls.get_translation_model()
        all_fields = set([
            f.name
            for f in TransModel._meta.get_fields()
        ])
        pk_fields = set([
            f.name for f in TransModel._meta.get_fields()
            if f.primary_key
        ])
        own_fields = set([
            f.name
            for f in TransModel._meta.get_fields()
            if not f.is_relation and not (f.one_to_many or f.one_to_one)
        ])
        reverse_fields = {
            f.name
            for f in TransModel._meta.get_fields()
            if (f.is_relation or f.many_to_one)
        }
        m2m_fields = {
            f.attname
            for f in TransModel._meta.get_fields()
            if f.many_to_many and not f.auto_created
        }
        result = all_fields.difference(pk_fields)
        if not reverse:
            result = result.difference(reverse_fields)
        if not m2m:
            result = result.difference(m2m_fields)
        if not own:
            result = result.difference(own_fields)
        return list(result)

    @classmethod
    def get_translation_model_reverse_field_name(cls):
        reverse_fields = cls.get_translation_model_field_names(
            reverse=True, m2m=False, own=False)
        if len(reverse_fields) > 1:
            raise Exception('Translation model must define only one relation. '
                            'Foreign key to main model')
        if len(reverse_fields) == 0:
            raise Exception('Translation model must define foreign key '
                            'relation to main model')

        TransModel = cls.get_translation_model()
        for f in cls._meta.get_fields():
            if f.related_model == TransModel:
                return f.related_query_name
        else:
            raise Exception('Reverse relation does not exists in Main model')

    class Meta:
        abstract = True


class LangMixin(models.Model):
    lang = models.CharField(max_length=256)

    class Meta:
        abstract = True


class ContentTranslationFields(models.Model):
    name = models.CharField(max_length=256)
    full_name = models.CharField(max_length=256)
    description = models.TextField()

    class Meta:
        abstract = True


class ContentTranslation(ContentTranslationFields, LangMixin):
    main_model = models.ForeignKey(
        to='Content', on_delete=models.CASCADE,
        related_query_name='translation', related_name='translation'
    )


class Content(TranslationMixin):
    translation_model = ContentTranslation
    objects = TranslationManager()
