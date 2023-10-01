from ._anvil_designer import Form1Template
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.repeating_panel_1.items =app_tables.ingredients.search()
    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    ingred, answer = anvil.server.call('ingredients')
    self.label_1.text = ingred + '\n' + answer
    
    pass

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call('spreadsheet')
    
    pass




