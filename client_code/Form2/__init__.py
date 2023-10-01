from ._anvil_designer import Form2Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Form2(Form2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.scenario_dropdown.items= [(str(row['Scenario_Desc']), row) for row in app_tables.scenario.search(tables.order_by('Scenario_Desc'))]
    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    Sys_PR = self.Sys_PR.text
    Sys_Int = self.Sys_Int.text
    Sys_Sys = self.Sys_Sys.text
    Sys_Ins= self.Sys_Ins.text
    print(str(Sys_PR) + ' ' + str(Sys_Int) + ' ' + str(Sys_Sys) + ' ' + str(Sys_Ins))
    SI_PR = self.SI_PR.text
    SI_Int = self.SI_Int.text
    SI_Sys = self.SI_Sys.text
    SI_Ins= self.SI_Ins.text

    SM_PR = self.SM_PR.text
    SM_Int = self.SM_Int.text
    SM_Sys = self.SM_Sys.text
    SM_Ins= self.SM_Ins.text
    
    UP_PR = self.UP_PR.text
    UP_Int = self.UP_Int.text
    UP_Sys = self.UP_Sys.text
    UP_Ins= self.UP_Ins.text

    
    app_tables.days_effort.add_row(projects= "Systems",
                          PreReqs = Sys_PR,
                          Interfacing = Sys_Int,
                          System_config= Sys_Sys,
                          Installing = Sys_Ins)
                       
    app_tables.days_effort.add_row(projects= "Standalone Interfaces",
                          PreReqs = SI_PR,
                          Interfacing = SI_Int,
                          System_config= SI_Sys,
                          Installing = SI_Ins)

    app_tables.days_effort.add_row(projects= "Server Moves",
                          PreReqs = SM_PR,
                          Interfacing = SM_Int,
                          System_config= SM_Sys,
                          Installing = SM_Ins)
    app_tables.days_effort.add_row(projects= "Upgrades",
                          PreReqs = UP_PR,
                          Interfacing = UP_Int,
                          System_config= UP_Sys,
                          Installing = UP_Ins)

  #====================================================
  #Populate Form from Tables
  #==================================================
  def scenario_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    # Days_effort
    #____________________
    data = app_tables.days_effort.search(Scenario=self.scenario_dropdown.selected_value)
    for row in data:
      print(row['projects'],row['PreReqs'],row['Interfacing'],row['System_config'],row['Installing'])
      if row['projects'] == 'Systems':
        self.Sys_PR.text = row['PreReqs']
        self.Sys_Int.text = row['Interfacing']
        self.Sys_Sys.text = row['System_config']
        self.Sys_Ins.text = row['Installing']

      if row['projects'] == 'Standalone Interfaces':
        self.SI_PR.text = row['PreReqs']
        self.SI_Int.text = row['Interfacing']
        self.SI_Sys.text = row['System_config']
        self.SI_Ins.text = row['Installing']
        
      if row['projects'] == 'Server Moves':
        self.SM_PR.text = row['PreReqs']
        self.SM_Int.text = row['Interfacing']
        self.SM_Sys.text = row['System_config']
        self.SM_Ins.text = row['Installing']
        
      if row['projects'] == 'Upgrades':
        self.UP_PR.text = row['PreReqs']
        self.UP_Int.text = row['Interfacing']
        self.UP_Sys.text = row['System_config']
        self.UP_Ins.text = row['Installing']
    pass
    data = app_tables.constraints.search(Scenario=self.scenario_dropdown.selected_value)
    for row in data:
        if row['Resource'] == 'PreReqs':
             self.CON_PR.text =row['Constraint'] 
        if row['Resource'] == 'Interfacing':
             self.CON_INT.text  = row['Constraint']
        if row['Resource'] == 'Systems_config':
             self.CON_SYS.text = row['Constraint'] 
        if row['Resource'] == 'Installing': 
            self.CON_INS.text = row['Constraint'] 
    data = app_tables.selling_prices.search(Scenario=self.scenario_dropdown.selected_value)
    for row in data:
        if row['projects'] == 'Systems':
             self.SELL_SYS.text =row['Selling_price'] 
        if row['projects'] == 'Standalone Interfaces':
             self.SELL_INT.text  = row['Selling_price']
        if row['projects'] == 'Server Moves':
             self.SELL_SM.text = row['Selling_price'] 
        if row['projects'] == 'Upgrades': 
            self.SELL_UPG.text = row['Selling_price'] 

#==============================================================
  # Update Tables from Form
#==========================================================

  
  def update_scenario_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    
    Scen_row = app_tables.scenario.get(ScenarioID = 1)
    days_effort_row = app_tables.days_effort.get(Scenario = Scen_row, projects = 'Systems')
    days_effort_row['PreReqs'] = self.Sys_PR.text
    days_effort_row['Interfacing'] = self.Sys_Int.text 
    days_effort_row['System_config'] = self.Sys_Sys.text   
    days_effort_row['Installing'] = self.Sys_Ins.text
    
    days_effort_row = app_tables.days_effort.get(Scenario = Scen_row, projects = 'Standalone Interfaces')
    days_effort_row['PreReqs'] = self.SI_PR.text
    days_effort_row['Interfacing'] = self.SI_Int.text 
    days_effort_row['System_config'] = self.SI_Sys.text   
    days_effort_row['Installing'] = self.SI_Ins.text   

    constraint_row = app_tables.constraints.get(Scenario = Scen_row, Resource='PreReqs')
    constraint_row['Constraint'] = self.CON_PR.text
    constraint_row = app_tables.constraints.get(Scenario = Scen_row, Resource='Interfacing')
    constraint_row['Constraint'] = self.CON_INT.text
    constraint_row = app_tables.constraints.get(Scenario = Scen_row, Resource='Systems_config')
    constraint_row['Constraint'] = self.CON_SYS.text
    constraint_row = app_tables.constraints.get(Scenario = Scen_row, Resource='Installing')
    constraint_row['Constraint'] = self.CON_INS.text

    selling_price_row = app_tables.selling_prices.get(Scenario = Scen_row, projects='Systems')
    selling_price_row['Selling_price'] = self.SELL_SYS.text
    selling_price_row = app_tables.selling_prices.get(Scenario = Scen_row, projects='Standalone Interfaces')
    selling_price_row['Selling_price'] = self.SELL_INT.text
    selling_price_row = app_tables.selling_prices.get(Scenario = Scen_row, projects='Server Moves')
    selling_price_row['Selling_price'] = self.SELL_SM.text
    selling_price_row = app_tables.selling_prices.get(Scenario = Scen_row, projects='Upgrades')
    selling_price_row['Selling_price'] = self.SELL_UPG.text
    pass

  def calculate_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    Scen_row = app_tables.scenario.get(ScenarioID = 1)
    anvil.server.call('calculate_projects', Scen_row)
    pass




 


