import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
#====================================================
#Populate Form from Tables
#==================================================
def update_form(self):

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
    
    # load constraints
    #++++++++++++++++++++++++++++++++++++++++++++++++++++
    data = app_tables.constraints.search(Scenario=self.scenario_dropdown.selected_value)
    for row in data:
        if row['Resource'] == 'PreReqs':
            self.CON_PR.text =row['Constraint'] 
            self.PR_USED.text = row['Used'] 
        if row['Resource'] == 'Interfacing':
            self.CON_INT.text  = row['Constraint']
            self.INT_USED.text = row['Used'] 
        if row['Resource'] == 'Systems_config':
            self.CON_SYS.text = row['Constraint'] 
            self.SYS_USED.text = row['Used'] 
        if row['Resource'] == 'Installing': 
            self.CON_INS.text = row['Constraint'] 
            self.INS_USED.text = row['Used'] 
  
    # Load projects info
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    data = app_tables.projects.search(Scenario=self.scenario_dropdown.selected_value)
    for row in data:
        if row['projects'] == 'Systems':
            self.SELL_SYS.text =row['Selling_price'] 
            self.DM_SYS.text = row['Demand']
            self.SYS_PRJ.text = row['Projected']
        if row['projects'] == 'Standalone Interfaces':
            self.SELL_INT.text  = row['Selling_price']
            self.DM_INT.text = row['Demand']
            self.INT_PRJ.text = row['Projected']
        if row['projects'] == 'Server Moves':
            self.SELL_SM.text = row['Selling_price'] 
            self.DM_SM.text = row['Demand']
            self.SM_PRJ.text = row['Projected']
        if row['projects'] == 'Upgrades': 
            self.SELL_UPG.text = row['Selling_price'] 
            self.DM_UP.text = row['Demand']
            self.UPG_PRJ.text = row['Projected']

