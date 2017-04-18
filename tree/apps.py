from django.apps import AppConfig


class TreeConfig(AppConfig):
    name = 'tree'

    def ready(self):
    	import tree.signals
