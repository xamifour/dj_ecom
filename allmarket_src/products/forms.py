from django import forms

from products.models import Review


RATING_CHOICES = (
    ('FIVESTAR', '5 Stars'),
    ('FOURSTAR', '4 Stars'),
    ('THREESTAR', '3 Stars'),
    ('TWOSTAR', '2 Stars'),
    ('ONESTAR', '1 Star'),
)


#Forms Here

class ReviewForm(forms.ModelForm):

    review_rating = forms.ChoiceField(widget=forms.Select, choices=RATING_CHOICES)
    class Meta:
        model      = Review
        fields     = '__all__'
        exclude    = ['product',]


'''
class ReviewForm(forms.Form):
    review_subject   = forms.CharField()
    review_rating = forms.ChoiceField(widget=forms.Select, choices=RATING_CHOICES)
    review_comment   = forms.CharField(widget=forms.Textarea(attrs={'rows': 8}))
''' 