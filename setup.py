try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='robots',
    version='1.2',
    description='Pylons app to receive SMS from SonicMobile',
    author='Sam Sargeant',
    author_email='sam@resultpath.com',
    url='http://www.resultpath.com/',
    install_requires=[
        "Pylons>=1.0",
	"feedparser>=4.0"
    ],
    setup_requires=["PasteScript>=1.6.3"],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'robots': ['i18n/*/LC_MESSAGES/*.mo']},
    #message_extractors={'robots': [
    #        ('**.py', 'python', None),
    #        ('templates/**.mako', 'mako', {'input_encoding': 'utf-8'}),
    #        ('public/**', 'ignore', None)]},
    zip_safe=False,
    paster_plugins=['PasteScript', 'Pylons'],
    entry_points="""
    [paste.app_factory]
    main = robots.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,
)
