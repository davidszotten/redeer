from django import forms

from redeer.feeds.models import Group, Feed, Item


def as_choices(iterable):
    return [(value, value) for value in iterable]

# sadly, 'as' is a keyword, so we need this
MarkFormBase = type('MarkFormBase', (forms.Form, ), {
    'mark': forms.ChoiceField(
        choices=as_choices(['item', 'feed', 'group'])),
    'as': forms.ChoiceField(
        choices=as_choices(['read', 'unread', 'saved', 'unsaved'])),
    'id': forms.IntegerField(),
})

class MarkForm(MarkFormBase):
    models = {
        'item': Item,
        'feed': Feed,
        'group': Group,
    }

    def clean(self):
        data = self.cleaned_data
        if 'mark' not in data or 'as' not in data:
            # not valid anyway
            return

        if data['mark'] != 'item' and 'saved' in data['as']:
            raise forms.ValidationError('Only items can be saved')

        return data

    def do_action(self):
        if not self.is_valid():
            return

        data = self.cleaned_data

        mark = data['mark']
        mark_as = data['as']
        pk = data['id']
        model = self.models[mark]
        value = (not mark_as.startswith('un'))

        if mark_as.endswith('read'):
            entry = model.objects.get(pk=pk)
            entry.mark_read(value)

        if mark_as.endswith('saved'):
            # this must be an Item
            entry = Item.objects.filter(pk=pk).update(is_saved=value)
