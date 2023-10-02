from ._anvil_designer import Form2Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# from ..Module1 import update_form
from ..Module2  import update_form

class Form2(Form2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # self.scenario_dropdown.items= [(str(row['Scenario_Desc']), row) for row in app_tables.scenario.search(tables.order_by('Scenario_Desc'))]
    # Any code you write here will run before the form opens.
    update_form(self)
 
  def create_scenario_button_click(self, **event_args):
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
    
    DM_SYS = self.DM_SYS.text
    DM_INT = self.DM_INT.text
    DM_SM = self.DM_SM.text
    DM_UP = self.DM_UP.text


    
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


  
  
#==============================================================
  # Update Tables from Form
#==========================================================

   
  def update_scenario_button_click(self, **event_args):
      # """This method is called when the button is clicked"""
    # if self.scenario_dropdown.selected_value != None:
    
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
      
          projects_row = app_tables.projects.get(Scenario = Scen_row, projects='Systems')
          projects_row['Selling_price'] = self.SELL_SYS.text
          projects_row['Demand'] = self.DM_SYS.text
          projects_row = app_tables.projects.get(Scenario = Scen_row, projects='Standalone Interfaces')
          projects_row['Selling_price'] = self.SELL_INT.text
          projects_row['Demand'] = self.DM_INT.text
          projects_row = app_tables.projects.get(Scenario = Scen_row, projects='Server Moves')
          projects_row['Selling_price'] = self.SELL_SM.text
          projects_row['Demand'] = self.DM_SM.text
          projects_row = app_tables.projects.get(Scenario = Scen_row, projects='Upgrades')
          projects_row['Selling_price'] = self.SELL_UPG.text
          projects_row['Demand'] = self.DM_UP.text
          pass
    # else:
    #         clear_form(self)
      
  def calculate_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    Scen_row = app_tables.scenario.get(ScenarioID = 1)
    update_form(self)
    anvil.server.call('calculate_projects', Scen_row)
    pass

  









 


