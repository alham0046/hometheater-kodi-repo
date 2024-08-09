import xbmc
import xbmcgui
import xbmcaddon

ADDON = xbmcaddon.Addon()
DIALOG_PATH = 'special://home/addons/skin.arctic.horizon.2/1080i/'

class CustomDialog(xbmcgui.WindowXMLDialog):
    def __init__(self, *args, **kwargs):
        super(CustomDialog, self).__init__(*args, **kwargs)
        self.show_data = kwargs.get('show_data', {})
    
    def onInit(self):
        self.populate_seasons_and_episodes()
        self.show_season(1)

    def onClick(self, controlId):
        if controlId in self.season_buttons:
            season_number = self.season_buttons[controlId]
            self.show_season(season_number)
    
    def populate_seasons_and_episodes(self):
        self.season_buttons = {}
        
        season_y = 0
        for season_number, episodes in self.show_data.items():
            button_id = 100 + season_number
            list_id = 200 + season_number
            
            # Add season button
            season_button = xbmcgui.ControlButton(
                50 + (season_number - 1) * 160, 100, 150, 50, f'Season {season_number}',
                onClick=f'Container.SetFocus({list_id})'
            )
            self.addControl(season_button)
            self.season_buttons[button_id] = season_number
            
            # Add episodes list
            episode_list = xbmcgui.ControlList(50, 160, 600, 500, list_id)
            for episode in episodes:
                list_item = xbmcgui.ListItem(episode['title'])
                episode_list.addItem(list_item)
            self.addControl(episode_list)
            episode_list.setVisible(False)
        
    def show_season(self, season):
        for list_id in range(200, 200 + len(self.show_data)):
            self.getControl(list_id).setVisible(False)
        self.getControl(200 + season).setVisible(True)

def open_custom_dialog(show_data):
    custom_dialog = CustomDialog('WebSeriesView.xml', DIALOG_PATH, 'default', '1080i', show_data=show_data)
    custom_dialog.doModal()
    del custom_dialog

# Example usage
show_data = {
    1: [{'title': 'Episode 1'}, {'title': 'Episode 2'}],
    2: [{'title': 'Episode 1'}, {'title': 'Episode 2'}],
    3: [{'title': 'Episode 1'}, {'title': 'Episode 2'}]
}

open_custom_dialog(show_data)
