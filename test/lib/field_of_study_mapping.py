#Administrative Practice
adminstrative_practice = ['Administrativei Practice']
#Business Management &amp; Organization
business_managent_and_organization = ['Business Management & Organization', 'BUSINESS MAN AGEMENT', 'Business Management', 'Business Mgmt and Org']
#Communications
communications = ['Communications']
#Computer Science
computer_science = ['Computer Science', 'Cybersecurity Update']
#Economics
economics = ['Economics']
#Ethics - Behavioral
ethics_behavioral = ['Ethics - Behavioral', 'Behavioral Ethics', 'Professional Ethics', 'Professional Development', 'Behavioral']
#Ethics - Regulatory
ethics_regulatory = ['Ethics - Regulatory', 'Regulatory Ethics', 'State Ethics', 'Ethics (Regulatory)', 'Ethics/Regulatory Ethics', 'Regulatory', 'Ethics']
#Finance
finance = [ 'Finance-Technical', 'Finance']
#Marketing
marketing = ['Marketing']
#Mathematics
mathematcis = ['Mathematics']
#Personal Development
personal_development = ['Personal Development', 'Personal']
#Personnel/Human Resources
personnel_human_resources = ['Personnel/Human Resources', 'Personnel/Human Resource', 'Personnel/HR', 'Personnel']
#Production
production = ['Production']
#Specialized Knowledge &amp; Applications
specialized_knowledge_and_applications = ['Specialized Knowledge and Applications', 'Specialized Knowledge & Applications', 'Specialized Knowledge and Application', 'Specialized Knowledge & Application']
#Social Environment of Business
social_env = ['Social Environment of Business']
#Statistics
stats = ['Statistics']
#Accounting
accounting = ['Accounting & Auditing', 'Accounting and Auditing', 'Accounting & Auditing / Tax', 'Accounting', 'ACCOUNTING', 'A&A']
#Accounting - Governmental
accouting_governmental = ['Accounting - Governmental', 'Accounting Governmental', 'Forensic Accounting', 'Forensic Accounting — Technical', 'Governmental Accounting', 'Accounting (Governmental)',]
#Auditing
auditing = ['Auditing', 'AUDITING', 'Audit', 'Auditing - Webinar']
#Auditing - Governmental
auditing_governmental = ['Auditing - Governmental', 'Auditing Governmental', 'Auditing (Governmental)']
#Business Law
business_law = ['Business Law', 'Laws & Rules Ethics', 'Fraud']
#Management Advisory Services
management_advisory_services = ['Management Advisory Services', 'Management Services', 'Management Advisory Services Basic Level']
#Taxes
taxes = ['Taxes', 'TAXES', 'Tax', 'Taxation', 'Taxes (in NY Taxation)']
#Communications and Marketing
comm_and_marketing = ['Communications and Marketing', 'Communications & Marketing']
#Specialized Knowledge
specialise_knowledge = ['Specialized Knowledge', 'Specialized Knowledge']
#Information Technology
information_tech = ['Information Technology', 'Informational Technology']
#Computer Software &amp; Applications
computer_software_app = ['Computer Software & Applications', 'Computer Software and Applications', 'Computer Software & Applications — Non-Technical']
#None
no_match = ['Fraud']



field_of_studies = [{'name': 'Administrative Practice', 'values': adminstrative_practice }, {'name': 'Business Management & Organization', 'values': business_managent_and_organization }, {'name': 'Computer Science', 'values': computer_science}, {'name': 'Economics','values': economics}, {'name': 'Ethics - Behavioral', 'values': ethics_behavioral}, {'name': 'Ethics - Regulatory', 'values': ethics_regulatory}, {'name': 'Finance', 'values': finance}, {'name': 'Mathematics', 'values': mathematcis}, {'name': 'Personal Development', 'values': personal_development}, {'name': 'Personnel/Human Resources', 'values': personnel_human_resources}, {'name': 'Production', 'values': production}, {'name': 'Specialized Knowledge & Applications', 'values': specialized_knowledge_and_applications}, {'name': 'Social Environment of Business', 'values': social_env}, {'name': 'Statistics', 'values': stats}, {'name': 'Accounting - Governmental', 'values': accouting_governmental},  {'name': 'Accounting', 'values': accounting}, {'name': 'Auditing - Governmental', 'values': auditing_governmental}, {'name': 'Auditing', 'values': auditing}, {'name': 'Business Law', 'values': business_law}, {'name': 'Management Advisory Services', 'values': management_advisory_services}, {'name': 'Taxes', 'values': taxes}, {'name': 'Communications and Marketing', 'values': comm_and_marketing}, {'name': 'Specialized Knowledge', 'values': specialise_knowledge}, {'name': 'Information Technology', 'values': information_tech}, {'name': 'Computer Software & Applications', 'values': computer_software_app}, { 'name': 'Communications', 'values': communications}, {'name': 'Marketing', 'values': marketing} ]



def find_fos_match(fos):
		#print(f"--->MAPPING_FOS--->FOS---->{fos}--")
		updated_fos = []
		for extracted_fos in fos:
				for mapping_fos in field_of_studies:
						#print(f"MAPPING_FOS---->{mapping_fos['name']}")
						flag = False
						for fi in mapping_fos['values']:
								if fi.lower() in extracted_fos.lower():
											#print(f"---fi--{fi}---extracted_fos-->{extracted_fos}")
											updated_fos.append(mapping_fos['name'])
											flag = True
											break
						if flag:
								break


		updated_fos = list(set(updated_fos))
		return updated_fos

