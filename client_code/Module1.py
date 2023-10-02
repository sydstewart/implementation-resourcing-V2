import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

def clear_form(self):
    self.Sys_PR.text = None
    self.Sys_Int.text = None
    self.Sys_Sys.text  = None 
    self.Sys_Ins.text = None
    
    self.SI_PR.text = None
    self.SI_Int.text = None
    self.SI_Sys.text  =None
    self.SI_Ins.text  =None 

    self.CON_PR.text = None
    self.CON_INT.text = None
    self.CON_SYS.text = None
    self.CON_INS.text = None

    self.SELL_SYS.text = None
    self.DM_SYS.text = None
    self.SELL_INT.text = None
    self.DM_INT.text = None
    self.SELL_SM.text = None
    self.DM_SM.text= None
    self.SELL_UPG.text = None
    self.DM_UP.text = None
  








def update_form(self):
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