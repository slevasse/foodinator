
class recipe_list_generator:

    def __init__(self, configuration = None):
        if configuration is None:
            self.configuration = {'name': 'init',
                                  'adult count': 0,
                                  'baby count': 0,
                                  'day count': 0,
                                  'breakfast': False,
                                  'lunch': False,
                                  'dinner': False,
                                  'fika': False,
                                  'fixed breakfast': [],
                                  'default tag': [],
                                  'requested tag': []}
        self.selected_recipe_list = []
        
