import streamlit as st
from datetime import datetime
import json
import pandas as pd


from utils.openai_helpers import perform_parsing
from utils.json_visualizer import filter_json, render_json
from styles.md import markdown_string
from pathlib import Path
import inspect
import time

# Data ingestion
st.set_page_config(page_title="Excel Editor", layout="wide")
uploaded = st.file_uploader("Upload a file", type=["xlsx", "xls", "csv"])
if uploaded:
    if "data" not in st.session_state:
        suffix = Path(uploaded.name).suffix.lower()
        if suffix == ".csv":
            df = pd.read_csv(uploaded)
        else:
            df = pd.read_excel(uploaded)    
        text = df.to_csv(index=False)                

        # AI Call
        with st.spinner("Parsing file", show_time=True):
            data = perform_parsing(text)
            # {'high_level_info': {'title': 'Procedure For Replacing Servers', 'mop_start_date': '2028-07-09 00:00:00', 'mop_end_date': '2028-07-11 00:00:00', 'mop_daily_start_time': '16:30', 'mop_daily_end_time': '0:30', 'time_standard': 'CDT', 'risk_level': '3'}, 'work_scope': 'This is the work scope for changing some servers withing a data hall.', 'planned_impact': 'Nile Web Services Z3 Buckets may stop working.', 'potential_impact': 'Extended loss of B side utility for Loops 2 and 3.', 'stop_work': 'The Supervisor and any other participant executing this Procedure, has the right to stop/halt all work being performed, if they deem necessary.', 'facility_info': {'customer': 'CloudFire', 'project_number': '', 'change_control_number': '765420', 'site': '1 Infinity Way, New York', 'contacts': [{'name': 'Gavin Newsom', 'company_name': 'California Oil', 'phone': '718-888-8888', 'email': 'Gavin@Caloil.com'}, {'name': 'Magrat Thatcher', 'company_name': 'Nvidia', 'phone': '718-888-8888', 'email': 'Maggie@nvidia.com'}, {'name': 'Winston Churchill', 'company_name': 'Nvidia', 'phone': '718-888-8888', 'email': 'Winnie@@nvidia.com'}, {'name': 'Tony Blair', 'company_name': 'Nile Web Services', 'phone': '718-888-8888', 'email': 'Tony@nws.com'}, {'name': 'Bill Clinton', 'company_name': 'Nile Web Services', 'phone': '718-888-8888', 'email': 'Bill@nws.com'}]}, 'administrative_signoff': 'I, [Manager’s Name], acknowledge that I have reviewed and approved the Method of Procedure (MOP) for the work described herein. By signing this document, I accept full responsibility for ensuring that the work is executed according to the procedures outlined, and that all safety, operational, and quality standards are met. I understand that I am accountable for the proper completion of this work and will take all necessary steps to ensure its successful and compliant execution.', 'effects': {'critical_facility': [{'equipment_or_system': 'Active Data Hall', 'checked': 'Yes', 'description': 'Data Hall 3'}, {'equipment_or_system': 'Electrical Utility Equipment', 'checked': 'Yes', 'description': 'Circuit breaker 6'}, {'equipment_or_system': 'Critical Power Distribution', 'checked': 'Yes', 'description': 'Switchgears 1-10'}, {'equipment_or_system': 'Uninterruptible Power Supply (UPS)', 'checked': 'Yes', 'description': 'UPS'}, {'equipment_or_system': 'Critical Cooling System', 'checked': 'Yes', 'description': 'Critical cooling will be transferred to alternate source'}, {'equipment_or_system': 'Fire Detection System', 'checked': 'Yes', 'description': 'Vesdas will be disabled'}, {'equipment_or_system': 'Fire Alarm System Remote Monitoring', 'checked': 'Yes', 'description': "System will be set to respond to 'full fire only'"}, {'equipment_or_system': 'Fire System Impaired/ Contact Insurance', 'checked': 'Yes', 'description': 'Impairment with insurance company will be generated'}, {'equipment_or_system': 'Building Management System (BMS)', 'checked': 'Yes', 'description': 'Alarms will be received while switching'}, {'equipment_or_system': 'General Building Spaces (Interior/Exterior)', 'checked': 'Yes', 'description': 'Electrical Switchgear rooms'}]}, 'risks': {'assumptions': ['Establish MOP Supervisor to run MOP, initial and Date task details and upload to RFC when MOP is completed.', 'Only one critical piece of equipment may be worked on at a time in a single line up or Room.', 'Only necessary personnel needed to accommodate scope permitted in critical equipment rooms.', 'Personnel shall not contact existing, live equipment within rooms unless specified in MOP.', 'Receptacles for power to be established by MOP Supervisor and identified to [Name Redacted]-OPS during pre-execution/MOP opening. Under no circumstances will receptacles attached to existing equipment (i.e. RPP) be permitted for use during MOP.', 'Dust containment measures are required for any actions that could generate dust or air particle generation including core drilling. This may require VESDA units in the area to be put in bypass and fire system be placed on test.', 'Any deviation from this approved MOP must be reviewed, approved and accepted by [Name Redacted] OPS.', 'All personnel involved in the procedure have read and agree to adhere to the MOP document.', 'All personnel involved shall always work from the hard copy of the approved MOP and the MOP supervisor is responsible for keeping the approved MOP in the work area.', '(Insert additional assumptions if necessary.)']}, 'ppe_requirements': {'safety_briefing': "Safety briefing must be conducted prior to each day's activities.", 'standard_required': [{'head': 5, 'energized_electrical_work': 'No'}, {'eyes': 'Safety Glasses'}, {'hearing': 'Ear Plugs', 'electrical_ppe_category': 'Category 4 40cal/cm²'}, {'shoes': 'Composite Toe'}, {'glove_type': 'Cut Level A4'}, {'reflective_vest': 'Yes'}]}, 'steps': {'pre_execution': [{'step_number': 1, 'type_of_work': 'Administrative', 'task_description': 'Established MOP Manager ; Supervisor to run MOP, initial and Date task details and upload to RFC when MOP is completed.'}, {'step_number': 2, 'type_of_work': 'Administrative', 'task_description': 'Verify Operations team and Vendor (if applicable) have access to Work Area(s).'}, {'step_number': 3, 'type_of_work': 'Administrative', 'task_description': 'Confirm that customer communications regarding the Change Request have been sent out via Service Now, if applicable.'}, {'step_number': 4, 'type_of_work': 'Administrative', 'task_description': "Review JHA with all parties involved. If the work takes longer than one day, this task must be performed daily before beginning work. The JHA must be signed each time it's reviewed by the party(ies) that will be performing the work and the MOP supervisor."}], 'execution_of_work': [{'step_number': 1, 'type_of_work': 'Administrative', 'task_description': "Contractor/MOP Supervisor and techs. Will arrive onsite and sign in @ OP's Office."}, {'step_number': 2, 'type_of_work': 'Communication', 'task_description': "OP's/Mop Supervisor will review steps of MOP, and order of operations for the day."}, {'step_number': 3, 'type_of_work': 'Safety', 'task_description': 'All parties involved will review, acknowledge, and agree to all the safety reguirements set forth in the JSA/JHA provided. All parties will sign and date.'}], 'end_of_workday': [{'step_number': 1, 'type_of_work': 'Administrative', 'task_description': 'Confirm all systems affected are Normal with no alarms present.'}, {'step_number': 3, 'type_of_work': 'Administrative', 'task_description': 'MOP Supervisor will ensure that all required work is complete and satisfactory prior to contacting Contractor/[Name Redacted] OPS for MOP Close-Out.'}]}, 'back_out_procedures': {'back_out_conditions': 'Back-out procedures will commence immediately if any problem/failure occurs that impacts critical systems or customer operations.', 'steps': [{'step_number': 2, 'type_of_work': 'Administrative', 'task_description': 'If the nature of the problem includes flooding, fire, or threat to personnel safety, Refer to the Site Emergency Action Plan.'}, {'step_number': 3, 'type_of_work': 'Administrative', 'task_description': 'Corrective actions will be taken to restore the equipment and/or critical operations/systems with coordination from [Name Redacted] OPS.'}]}, 'mop_completion_sign_off': 'I acknowledge that I have executed this Method of Procedure (MOP) for the work described herein. By signing this document, I accept full responsibility for ensuring that the work has been carried out according to the outlined procedures and that all safety, operational, and quality standards were met. I understand that I am accountable for the proper completion of this work.', 'document_revision_control': {'circulation': 'Internal Use Only', 'document_version': 'v0.1', 'document_owner': 'Nile', 'classification': 'Dems'}}
        st.session_state.data = data

    

    # Styling for visuals
    st.markdown(markdown_string(), unsafe_allow_html=True)

    # Search and display
    search_term = st.text_input("Search Parsed Data", key="search_term")
    filtered = filter_json(st.session_state.data, search_term)
    edited = render_json(filtered)
    

    if "reloaded" not in st.session_state:
        st.session_state.reloaded = True
        st.rerun()

    st.download_button(
        label="Download Data",
        file_name="data.json",
        mime="application/json",
        data=json.dumps(st.session_state.data),
    )
    