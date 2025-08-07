# Contributing Translations
Open Scouting has support for multiple languages. Languages can be switched in the menu.

## Languages
The table below shows the currently supported languages and their translation progress

| Language | Code | Progress |
|----------|------|----------|
|English   |en    |100%      |
|Spanish   |es    |0%        |
|German    |de    |0%        |
|French    |fr    |0%        |
|Italian   |it    |0%        |


## Contributing
> ![NOTE]
> There is some software available to make the translation experience better, instead of having to edit a file directly. See [POEdit](https://poedit.net/) or [GNOME Translation Editor](https://wiki.gnome.org/Apps/Gtranslator)

When contributing translations, navigate to the `/scouting/locale/` folder, and find the language you'd like to contribute translations on. Edit the corresponding `django.po` and `djangojs.po` files with your changes, by changing each `msgstr` with the translated text, like so:

```po
#: main/templates/advanced_data/advanced_data.html:28
#: main/templates/index/authentication_box.html:83
msgid "Advanced Data View"
msgstr "Vista de datos avanzada"
```

Once you've made your changes, ensure to update the table above if you've made new translation progress. Finally, open a PR with your changes into `development`. Your new translations will be reviewed and eventually merged into the latest version of Open Scouting. Thank you for your contribution!

## Adding new languages
> ![IMPORTANT]
> Support has not yet been fully added for right to left languages. This is definitely something that needs added in future. If you wish to contribute a right to left language, please open an issue, and support for that will be prioritized

If your language isn't already added into Open Scouting, feel free to add it!

First, find the `LANGUAGES` setting in `settings.py`, and add your language to it:
```python
LANGUAGES = (
    ...
    ("es", _("Spanish")),
    ...
)
```

Next, create the .po file, for both the templates and JavaScript:
```bash
cd scouting
python manage.py makemessages -l es # Use the language code of your new language here
python manage.py makemessages -l es -d djangojs # For JavaScript
```

Now, subsequent runs of `python manage.py makemessages -all` and `python manage.py makemessages --all -d djangojs` (for JavaScript) will now update this file with any new translation strings

## Translation strings
For code contributors, you will need to mark strings in your templates and scripts as translatable, so they can be added to any `.po` files and eventually translated correctly.

Read through the [official django docs](https://docs.djangoproject.com/en/5.2/topics/i18n/) for how to do this. Once you've added your translation strings to templates and JavaScript files, run the following commands to add your new translation strings into the `.po` files:
```bash
python manage.py makemessages --all
python manage.py makemessages --all -d djangojs # For JavaScript
python manage.py compilemessages
```

Visual Studio Code users can also run the `Make and update translation files` task using the `Ctrl-Shift-P > Run Task`